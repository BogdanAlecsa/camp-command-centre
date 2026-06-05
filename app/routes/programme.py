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
