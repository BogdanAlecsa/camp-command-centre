from datetime import date, time
from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    Activity,
    ActivityRiskAssessment,
    Camp,
    Person,
    ProgrammeSession,
    Team,
    TeamMembership,
)

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[1]
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

PROGRAMME_SESSION_TYPES = [
    "Activity",
    "Meal",
    "Travel",
    "Setup / Pack Down",
    "Free Time",
    "Leader / Admin",
    "Whole Camp",
    "Group Rotation",
    "Other",
]


def get_latest_camp(db: Session):
    return db.query(Camp).order_by(Camp.start_date.desc()).first()


def parse_optional_int(value: str | None):
    value = (value or "").strip()

    if not value:
        return None

    parsed = int(value)
    return parsed if parsed > 0 else None


def person_display_name(person: Person | None):
    if person is None:
        return "Not set"

    return f"{person.first_name} {person.last_name}"


def get_programme_form_options(db: Session, camp: Camp):
    activities = (
        db.query(Activity)
        .filter(Activity.camp_id == camp.id)
        .order_by(Activity.name)
        .all()
    )

    teams = (
        db.query(Team)
        .filter(Team.camp_id == camp.id)
        .order_by(Team.team_type, Team.name)
        .all()
    )

    people = (
        db.query(Person)
        .filter(Person.camp_id == camp.id)
        .order_by(Person.person_type, Person.last_name, Person.first_name)
        .all()
    )

    return activities, teams, people


def get_activity_risk_status_map(db: Session, camp: Camp, activities: list[Activity]):
    risk_statuses = {activity.id: "Not Started" for activity in activities}

    activity_ids = [activity.id for activity in activities]

    if not activity_ids:
        return risk_statuses

    risks = (
        db.query(ActivityRiskAssessment)
        .filter(
            ActivityRiskAssessment.camp_id == camp.id,
            ActivityRiskAssessment.activity_id.in_(activity_ids),
        )
        .all()
    )

    for risk in risks:
        risk_statuses[risk.activity_id] = risk.status

    return risk_statuses


def get_programme_lookup_maps(db: Session, camp: Camp):
    activities, teams, people = get_programme_form_options(db, camp)

    activity_names = {activity.id: activity.name for activity in activities}
    team_names = {team.id: team.name for team in teams}
    person_names = {person.id: person_display_name(person) for person in people}
    risk_statuses = get_activity_risk_status_map(db, camp, activities)

    return activities, teams, people, activity_names, team_names, person_names, risk_statuses


def build_rotation_summaries(sessions_by_date: dict):
    summaries_by_date = {}

    for session_date, day_sessions in sessions_by_date.items():
        rotation_groups = {}

        for session in day_sessions:
            if not session.rotation_group:
                continue

            rotation = rotation_groups.setdefault(session.rotation_group, {})
            slot_number = session.rotation_slot_number or 0
            rotation.setdefault(slot_number, []).append(session)

        day_summaries = []

        for rotation_name, slots in rotation_groups.items():
            slot_summaries = []

            for slot_number, slot_sessions in sorted(slots.items()):
                sorted_sessions = sorted(
                    slot_sessions,
                    key=lambda item: (
                        item.start_time,
                        item.participant_team_id or 0,
                        item.title,
                    ),
                )

                slot_summaries.append(
                    {
                        "slot_number": slot_number if slot_number else None,
                        "start_time": sorted_sessions[0].start_time,
                        "end_time": sorted_sessions[0].end_time,
                        "sessions": sorted_sessions,
                    }
                )

            day_summaries.append(
                {
                    "rotation_name": rotation_name,
                    "slots": slot_summaries,
                }
            )

        summaries_by_date[session_date] = day_summaries

    return summaries_by_date


@router.get("/programme", response_class=HTMLResponse)
async def programme_page(request: Request, db: Session = Depends(get_db)):
    camp = get_latest_camp(db)

    if camp is None:
        return templates.TemplateResponse("programme.html", {"request": request})

    return RedirectResponse(url=f"/camps/{camp.id}/programme", status_code=303)


@router.get("/camps/{camp_id}/programme", response_class=HTMLResponse)
async def camp_programme_list(
    request: Request,
    camp_id: int,
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Camp not found."},
            status_code=404,
        )

    sessions = (
        db.query(ProgrammeSession)
        .filter(ProgrammeSession.camp_id == camp.id)
        .order_by(
            ProgrammeSession.session_date,
            ProgrammeSession.start_time,
            ProgrammeSession.participant_team_id,
            ProgrammeSession.title,
        )
        .all()
    )

    sessions_by_date = {}

    for session in sessions:
        sessions_by_date.setdefault(session.session_date, []).append(session)

    rotation_summaries_by_date = build_rotation_summaries(sessions_by_date)

    (
        activities,
        teams,
        people,
        activity_names,
        team_names,
        person_names,
        risk_statuses,
    ) = get_programme_lookup_maps(db, camp)

    return templates.TemplateResponse(
        "programme/list.html",
        {
            "request": request,
            "camp": camp,
            "sessions": sessions,
            "sessions_by_date": sessions_by_date,
            "rotation_summaries_by_date": rotation_summaries_by_date,
            "activity_names": activity_names,
            "team_names": team_names,
            "person_names": person_names,
            "risk_statuses": risk_statuses,
        },
    )


@router.get("/camps/{camp_id}/programme/new", response_class=HTMLResponse)
async def new_programme_session_form(
    request: Request,
    camp_id: int,
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Camp not found."},
            status_code=404,
        )

    activities, teams, people = get_programme_form_options(db, camp)

    return templates.TemplateResponse(
        "programme/new.html",
        {
            "request": request,
            "camp": camp,
            "activities": activities,
            "teams": teams,
            "people": people,
            "session_types": PROGRAMME_SESSION_TYPES,
            "error": None,
        },
    )


@router.post("/camps/{camp_id}/programme/new")
async def create_programme_session(
    request: Request,
    camp_id: int,
    session_date: date = Form(...),
    start_time: time = Form(...),
    end_time: time = Form(...),
    title: str = Form(""),
    session_type: str = Form("Activity"),
    activity_id: str = Form(""),
    participant_team_id: str = Form(""),
    lead_person_id: str = Form(""),
    location: str = Form(""),
    notes: str = Form(""),
    rotation_group: str = Form(""),
    rotation_slot_number: str = Form(""),
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Camp not found."},
            status_code=404,
        )

    activities, teams, people = get_programme_form_options(db, camp)

    if end_time <= start_time:
        return templates.TemplateResponse(
            "programme/new.html",
            {
                "request": request,
                "camp": camp,
                "activities": activities,
                "teams": teams,
                "people": people,
                "session_types": PROGRAMME_SESSION_TYPES,
                "error": "The end time must be after the start time.",
            },
            status_code=400,
        )

    if session_date < camp.start_date or session_date > camp.end_date:
        return templates.TemplateResponse(
            "programme/new.html",
            {
                "request": request,
                "camp": camp,
                "activities": activities,
                "teams": teams,
                "people": people,
                "session_types": PROGRAMME_SESSION_TYPES,
                "error": "The session date must fall within the camp dates.",
            },
            status_code=400,
        )

    selected_activity_id = parse_optional_int(activity_id)
    selected_team_id = parse_optional_int(participant_team_id)
    selected_lead_id = parse_optional_int(lead_person_id)

    selected_activity = None

    if selected_activity_id:
        selected_activity = (
            db.query(Activity)
            .filter(Activity.id == selected_activity_id, Activity.camp_id == camp.id)
            .first()
        )

    clean_title = title.strip()

    if not clean_title and selected_activity:
        clean_title = selected_activity.name

    if not clean_title:
        return templates.TemplateResponse(
            "programme/new.html",
            {
                "request": request,
                "camp": camp,
                "activities": activities,
                "teams": teams,
                "people": people,
                "session_types": PROGRAMME_SESSION_TYPES,
                "error": "Add a title, or choose an activity so the title can be taken from the activity.",
            },
            status_code=400,
        )

    session = ProgrammeSession(
        camp_id=camp.id,
        session_date=session_date,
        start_time=start_time,
        end_time=end_time,
        title=clean_title,
        session_type=session_type,
        activity_id=selected_activity_id,
        participant_team_id=selected_team_id,
        lead_person_id=selected_lead_id,
        location=location.strip() or None,
        notes=notes.strip() or None,
        rotation_group=rotation_group.strip() or None,
        rotation_slot_number=parse_optional_int(rotation_slot_number),
    )

    db.add(session)
    db.commit()

    return RedirectResponse(url=f"/camps/{camp.id}/programme", status_code=303)


@router.get("/camps/{camp_id}/programme/{session_id}", response_class=HTMLResponse)
async def programme_session_detail(
    request: Request,
    camp_id: int,
    session_id: int,
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Camp not found."},
            status_code=404,
        )

    session = (
        db.query(ProgrammeSession)
        .filter(ProgrammeSession.id == session_id, ProgrammeSession.camp_id == camp.id)
        .first()
    )

    if session is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Programme session not found."},
            status_code=404,
        )

    (
        activities,
        teams,
        people,
        activity_names,
        team_names,
        person_names,
        risk_statuses,
    ) = get_programme_lookup_maps(db, camp)

    return templates.TemplateResponse(
        "programme/detail.html",
        {
            "request": request,
            "camp": camp,
            "session": session,
            "activity_names": activity_names,
            "team_names": team_names,
            "person_names": person_names,
            "risk_statuses": risk_statuses,
        },
    )


@router.post("/camps/{camp_id}/programme/{session_id}/delete")
async def delete_programme_session(
    camp_id: int,
    session_id: int,
    db: Session = Depends(get_db),
):
    session = (
        db.query(ProgrammeSession)
        .filter(ProgrammeSession.id == session_id, ProgrammeSession.camp_id == camp_id)
        .first()
    )

    if session is not None:
        db.delete(session)
        db.commit()

    return RedirectResponse(url=f"/camps/{camp_id}/programme", status_code=303)


@router.get("/camps/{camp_id}/programme/{session_id}/edit", response_class=HTMLResponse)
async def edit_programme_session_form(
    request: Request,
    camp_id: int,
    session_id: int,
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Camp not found."},
            status_code=404,
        )

    session = (
        db.query(ProgrammeSession)
        .filter(ProgrammeSession.id == session_id, ProgrammeSession.camp_id == camp.id)
        .first()
    )

    if session is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Programme session not found."},
            status_code=404,
        )

    activities, teams, people = get_programme_form_options(db, camp)

    return templates.TemplateResponse(
        "programme/edit.html",
        {
            "request": request,
            "camp": camp,
            "session": session,
            "activities": activities,
            "teams": teams,
            "people": people,
            "session_types": PROGRAMME_SESSION_TYPES,
            "error": None,
        },
    )


@router.post("/camps/{camp_id}/programme/{session_id}/edit")
async def update_programme_session(
    request: Request,
    camp_id: int,
    session_id: int,
    session_date: date = Form(...),
    start_time: time = Form(...),
    end_time: time = Form(...),
    title: str = Form(""),
    session_type: str = Form("Activity"),
    activity_id: str = Form(""),
    participant_team_id: str = Form(""),
    lead_person_id: str = Form(""),
    location: str = Form(""),
    notes: str = Form(""),
    rotation_group: str = Form(""),
    rotation_slot_number: str = Form(""),
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Camp not found."},
            status_code=404,
        )

    session = (
        db.query(ProgrammeSession)
        .filter(ProgrammeSession.id == session_id, ProgrammeSession.camp_id == camp.id)
        .first()
    )

    if session is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Programme session not found."},
            status_code=404,
        )

    activities, teams, people = get_programme_form_options(db, camp)

    if end_time <= start_time:
        return templates.TemplateResponse(
            "programme/edit.html",
            {
                "request": request,
                "camp": camp,
                "session": session,
                "activities": activities,
                "teams": teams,
                "people": people,
                "session_types": PROGRAMME_SESSION_TYPES,
                "error": "The end time must be after the start time.",
            },
            status_code=400,
        )

    if session_date < camp.start_date or session_date > camp.end_date:
        return templates.TemplateResponse(
            "programme/edit.html",
            {
                "request": request,
                "camp": camp,
                "session": session,
                "activities": activities,
                "teams": teams,
                "people": people,
                "session_types": PROGRAMME_SESSION_TYPES,
                "error": "The session date must fall within the camp dates.",
            },
            status_code=400,
        )

    selected_activity_id = parse_optional_int(activity_id)
    selected_team_id = parse_optional_int(participant_team_id)
    selected_lead_id = parse_optional_int(lead_person_id)

    selected_activity = None

    if selected_activity_id:
        selected_activity = (
            db.query(Activity)
            .filter(Activity.id == selected_activity_id, Activity.camp_id == camp.id)
            .first()
        )

    clean_title = title.strip()

    if not clean_title and selected_activity:
        clean_title = selected_activity.name

    if not clean_title:
        return templates.TemplateResponse(
            "programme/edit.html",
            {
                "request": request,
                "camp": camp,
                "session": session,
                "activities": activities,
                "teams": teams,
                "people": people,
                "session_types": PROGRAMME_SESSION_TYPES,
                "error": "Add a title, or choose an activity so the title can be taken from the activity.",
            },
            status_code=400,
        )

    session.session_date = session_date
    session.start_time = start_time
    session.end_time = end_time
    session.title = clean_title
    session.session_type = session_type
    session.activity_id = selected_activity_id
    session.participant_team_id = selected_team_id
    session.lead_person_id = selected_lead_id
    session.location = location.strip() or None
    session.notes = notes.strip() or None
    session.rotation_group = rotation_group.strip() or None
    session.rotation_slot_number = parse_optional_int(rotation_slot_number)

    db.commit()

    return RedirectResponse(url=f"/camps/{camp.id}/programme/{session.id}", status_code=303)


@router.get("/camps/{camp_id}/programme/print/full", response_class=HTMLResponse)
async def print_full_programme(
    request: Request,
    camp_id: int,
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Camp not found."},
            status_code=404,
        )

    sessions = (
        db.query(ProgrammeSession)
        .filter(ProgrammeSession.camp_id == camp.id)
        .order_by(
            ProgrammeSession.session_date,
            ProgrammeSession.start_time,
            ProgrammeSession.participant_team_id,
            ProgrammeSession.title,
        )
        .all()
    )

    sessions_by_date = {}

    for session in sessions:
        sessions_by_date.setdefault(session.session_date, []).append(session)

    rotation_summaries_by_date = build_rotation_summaries(sessions_by_date)

    (
        activities,
        teams,
        people,
        activity_names,
        team_names,
        person_names,
        risk_statuses,
    ) = get_programme_lookup_maps(db, camp)

    return templates.TemplateResponse(
        "programme/print_full.html",
        {
            "request": request,
            "camp": camp,
            "sessions": sessions,
            "sessions_by_date": sessions_by_date,
            "rotation_summaries_by_date": rotation_summaries_by_date,
            "activity_names": activity_names,
            "team_names": team_names,
            "person_names": person_names,
            "risk_statuses": risk_statuses,
        },
    )


@router.get("/camps/{camp_id}/programme/print/groups", response_class=HTMLResponse)
async def print_group_programmes(
    request: Request,
    camp_id: int,
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Camp not found."},
            status_code=404,
        )

    all_sessions = (
        db.query(ProgrammeSession)
        .filter(ProgrammeSession.camp_id == camp.id)
        .order_by(
            ProgrammeSession.session_date,
            ProgrammeSession.start_time,
            ProgrammeSession.participant_team_id,
            ProgrammeSession.title,
        )
        .all()
    )

    participant_team_types = [
        "Patrol/Six",
        "Activity Group",
        "Tent Group",
    ]

    teams = (
        db.query(Team)
        .join(TeamMembership, TeamMembership.team_id == Team.id)
        .join(Person, Person.id == TeamMembership.person_id)
        .filter(
            Team.camp_id == camp.id,
            Team.team_type.in_(participant_team_types),
            Person.person_type == "Young Person",
        )
        .distinct()
        .order_by(Team.team_type, Team.name)
        .all()
    )

    (
        activities,
        all_teams,
        people,
        activity_names,
        team_names,
        person_names,
        risk_statuses,
    ) = get_programme_lookup_maps(db, camp)

    schedules = []

    for team in teams:
        team_sessions = [
            session
            for session in all_sessions
            if session.participant_team_id is None
            or session.participant_team_id == team.id
        ]

        sessions_by_date = {}

        for session in team_sessions:
            sessions_by_date.setdefault(session.session_date, []).append(session)

        schedules.append(
            {
                "team": team,
                "sessions": team_sessions,
                "sessions_by_date": sessions_by_date,
            }
        )

    return templates.TemplateResponse(
        "programme/print_groups.html",
        {
            "request": request,
            "camp": camp,
            "schedules": schedules,
            "activity_names": activity_names,
            "team_names": team_names,
            "person_names": person_names,
            "risk_statuses": risk_statuses,
        },
    )



@router.get("/camps/{camp_id}/programme/print/activity-leaders", response_class=HTMLResponse)
async def print_activity_leader_schedules(
    request: Request,
    camp_id: int,
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Camp not found."},
            status_code=404,
        )

    sessions = (
        db.query(ProgrammeSession)
        .filter(
            ProgrammeSession.camp_id == camp.id,
            ProgrammeSession.activity_id.isnot(None),
        )
        .order_by(
            ProgrammeSession.session_date,
            ProgrammeSession.start_time,
            ProgrammeSession.rotation_group,
            ProgrammeSession.activity_id,
            ProgrammeSession.participant_team_id,
            ProgrammeSession.title,
        )
        .all()
    )

    (
        activities,
        teams,
        people,
        activity_names,
        team_names,
        person_names,
        risk_statuses,
    ) = get_programme_lookup_maps(db, camp)

    schedules_by_key = {}

    for session in sessions:
        schedule_kind = "rotation" if session.rotation_group else "single"

        key = (
            schedule_kind,
            session.activity_id,
            session.rotation_group or "",
            session.location or "",
            session.lead_person_id or 0,
        )

        schedule = schedules_by_key.get(key)

        if schedule is None:
            schedule = {
                "schedule_kind": schedule_kind,
                "activity_id": session.activity_id,
                "activity_name": activity_names.get(session.activity_id, session.title),
                "rotation_group": session.rotation_group,
                "location": session.location,
                "lead_person_id": session.lead_person_id,
                "lead_name": person_names.get(session.lead_person_id, "Unassigned lead")
                if session.lead_person_id
                else "Unassigned lead",
                "sessions": [],
            }
            schedules_by_key[key] = schedule

        schedule["sessions"].append(session)

    schedules = list(schedules_by_key.values())

    for schedule in schedules:
        schedule["sessions"] = sorted(
            schedule["sessions"],
            key=lambda item: (
                item.session_date,
                item.start_time,
                item.rotation_slot_number or 0,
                item.participant_team_id or 0,
                item.title,
            ),
        )

        schedule["start_time"] = min(item.start_time for item in schedule["sessions"])
        schedule["end_time"] = max(item.end_time for item in schedule["sessions"])
        schedule["start_date"] = min(item.session_date for item in schedule["sessions"])
        schedule["end_date"] = max(item.session_date for item in schedule["sessions"])

    schedules = sorted(
        schedules,
        key=lambda item: (
            item["start_date"],
            item["start_time"],
            item["activity_name"],
            item["rotation_group"] or "",
        ),
    )

    return templates.TemplateResponse(
        "programme/print_activity_leaders.html",
        {
            "request": request,
            "camp": camp,
            "schedules": schedules,
            "activity_names": activity_names,
            "team_names": team_names,
            "person_names": person_names,
            "risk_statuses": risk_statuses,
        },
    )



@router.get("/camps/{camp_id}/programme/print/leader", response_class=HTMLResponse)
async def print_leader_programme(
    request: Request,
    camp_id: int,
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Camp not found."},
            status_code=404,
        )

    sessions = (
        db.query(ProgrammeSession)
        .filter(ProgrammeSession.camp_id == camp.id)
        .order_by(
            ProgrammeSession.session_date,
            ProgrammeSession.start_time,
            ProgrammeSession.rotation_group,
            ProgrammeSession.rotation_slot_number,
            ProgrammeSession.participant_team_id,
            ProgrammeSession.title,
        )
        .all()
    )

    (
        activities,
        teams,
        people,
        activity_names,
        team_names,
        person_names,
        risk_statuses,
    ) = get_programme_lookup_maps(db, camp)

    sessions_by_date = {}
    for session in sessions:
        sessions_by_date.setdefault(session.session_date, []).append(session)

    days = []

    for session_date, day_sessions in sessions_by_date.items():
        normal_sessions = []
        rotation_groups = {}

        for session in day_sessions:
            if session.rotation_group:
                rotation = rotation_groups.setdefault(
                    session.rotation_group,
                    {
                        "name": session.rotation_group,
                        "start_time": session.start_time,
                        "end_time": session.end_time,
                        "bases": {},
                    },
                )

                if session.start_time < rotation["start_time"]:
                    rotation["start_time"] = session.start_time
                if session.end_time > rotation["end_time"]:
                    rotation["end_time"] = session.end_time

                base_key = (
                    session.activity_id or 0,
                    session.location or "",
                    session.lead_person_id or 0,
                )

                base = rotation["bases"].setdefault(
                    base_key,
                    {
                        "activity_id": session.activity_id,
                        "activity_name": activity_names.get(session.activity_id, session.title),
                        "location": session.location,
                        "lead_name": person_names.get(session.lead_person_id, "Unassigned lead")
                        if session.lead_person_id
                        else "Unassigned lead",
                        "slots": [],
                    },
                )

                base["slots"].append(session)
            else:
                normal_sessions.append(session)

        rotation_blocks = []

        for rotation_name, rotation in rotation_groups.items():
            bases = list(rotation["bases"].values())

            for base in bases:
                base["slots"] = sorted(
                    base["slots"],
                    key=lambda s: (
                        s.rotation_slot_number or 0,
                        s.start_time,
                        s.participant_team_id or 0,
                    ),
                )

            bases = sorted(
                bases,
                key=lambda b: (
                    b["activity_name"],
                    b["location"] or "",
                    b["lead_name"],
                ),
            )

            rotation_blocks.append(
                {
                    "block_type": "rotation",
                    "name": rotation_name,
                    "start_time": rotation["start_time"],
                    "end_time": rotation["end_time"],
                    "bases": bases,
                }
            )

        rotation_blocks = sorted(
            rotation_blocks,
            key=lambda item: (item["start_time"], item["name"])
        )

        blocks = []

        for session in normal_sessions:
            blocks.append(
                {
                    "block_type": "session",
                    "start_time": session.start_time,
                    "end_time": session.end_time,
                    "session": session,
                }
            )

        blocks.extend(rotation_blocks)

        blocks = sorted(
            blocks,
            key=lambda item: (
                item["start_time"],
                1 if item["block_type"] == "rotation" else 0,
            ),
        )

        days.append(
            {
                "session_date": session_date,
                "blocks": blocks,
            }
        )

    return templates.TemplateResponse(
        "programme/print_leader.html",
        {
            "request": request,
            "camp": camp,
            "days": days,
            "activity_names": activity_names,
            "team_names": team_names,
            "person_names": person_names,
            "risk_statuses": risk_statuses,
        },
    )
