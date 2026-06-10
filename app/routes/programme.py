from datetime import date, datetime, time
import re
from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    Activity,
    ActivityRiskAssessment,
    Camp,
    Person,
    PresenceWindow,
    ProgrammeSession,
    ProgrammeSessionBackup,
    ProgrammeSessionStaff,
    Section,
    Team,
    TeamMembership,
)

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[1]
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))



def programme_type_class(session_type: str | None):
    value = (session_type or "Other").strip().lower()
    value = value.replace("&", "and")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "other"


templates.env.globals["programme_type_class"] = programme_type_class


PROGRAMME_STAFF_ROLES = [
    "Lead",
    "Supporting Adult",
    "Parent Helper",
    "Young Leader",
    "First Aider",
    "Observer",
    "Other",
]

PROGRAMME_BACKUP_REASONS = [
    "Wet weather",
    "Too hot",
    "Low light / darkness",
    "Activity overrun",
    "Equipment unavailable",
    "Instructor unavailable",
    "Low energy / tired group",
    "Behaviour reset",
    "Other",
]



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



def get_session_staff(db: Session, camp: Camp, session: ProgrammeSession):
    staff_rows = (
        db.query(ProgrammeSessionStaff, Person)
        .join(Person, Person.id == ProgrammeSessionStaff.person_id)
        .filter(
            ProgrammeSessionStaff.camp_id == camp.id,
            ProgrammeSessionStaff.programme_session_id == session.id,
            Person.camp_id == camp.id,
        )
        .order_by(ProgrammeSessionStaff.role, Person.last_name, Person.first_name)
        .all()
    )

    session_staff = []

    for staff, person in staff_rows:
        presence_info = get_person_session_presence_info(
            db,
            camp,
            person,
            session,
        )

        session_staff.append(
            {
                "staff": staff,
                "person": person,
                "display_name": person_display_name(person),
                "is_present_at_session_start": presence_info["present_at_start"],
                "is_expected_for_full_session": presence_info["expected_for_full_session"],
                "presence_warning": presence_info["warning"],
            }
        )

    return session_staff


PROGRAMME_STAFF_PERSON_TYPES = [
    "Leader",
    "Helper",
    "Young Leader",
    "Parent/Guardian",
    "Visitor",
]


def get_programme_session_interval(session: ProgrammeSession):
    return (
        datetime.combine(session.session_date, session.start_time),
        datetime.combine(session.session_date, session.end_time),
    )


def get_presence_windows_for_scope(
    db: Session,
    camp: Camp,
    scope_type: str,
    scope_id: int | None,
):
    query = db.query(PresenceWindow).filter(
        PresenceWindow.camp_id == camp.id,
        PresenceWindow.scope_type == scope_type,
    )

    if scope_id is None:
        query = query.filter(PresenceWindow.scope_id.is_(None))
    else:
        query = query.filter(PresenceWindow.scope_id == scope_id)

    return query.order_by(
        PresenceWindow.starts_at,
        PresenceWindow.ends_at,
        PresenceWindow.id,
    ).all()


def get_effective_presence_windows_for_person(
    db: Session,
    camp: Camp,
    person: Person,
):
    presence_sources = [("person", person.id)]

    home_section = None

    if person.home_section_id:
        home_section = (
            db.query(Section)
            .filter(
                Section.id == person.home_section_id,
                Section.camp_id == camp.id,
            )
            .first()
        )

    if home_section is not None:
        presence_sources.append(("section", home_section.id))

        if home_section.participating_group_id is not None:
            presence_sources.append(
                ("participating_group", home_section.participating_group_id)
            )

    presence_sources.append(("camp", None))

    for scope_type, scope_id in presence_sources:
        windows = get_presence_windows_for_scope(db, camp, scope_type, scope_id)

        if windows:
            return windows

    return []


def format_presence_time_for_session(value: datetime | None, session: ProgrammeSession):
    if value is None:
        return ""

    if value.date() == session.session_date:
        return value.strftime("%H:%M")

    return value.strftime("%d %b %H:%M")


def get_person_session_presence_info(
    db: Session,
    camp: Camp,
    person: Person,
    session: ProgrammeSession,
):
    session_starts_at, session_ends_at = get_programme_session_interval(session)
    windows = get_effective_presence_windows_for_person(db, camp, person)

    expected_windows_at_start = [
        window
        for window in windows
        if (window.status or "").strip() == "Expected"
        and window.starts_at <= session_starts_at
        and window.ends_at > session_starts_at
    ]

    if not expected_windows_at_start:
        return {
            "present_at_start": False,
            "expected_for_full_session": False,
            "leave_time": None,
            "warning": "Not expected at session start",
        }

    best_window = max(expected_windows_at_start, key=lambda window: window.ends_at)

    if best_window.ends_at >= session_ends_at:
        return {
            "present_at_start": True,
            "expected_for_full_session": True,
            "leave_time": None,
            "warning": "",
        }

    leave_time = format_presence_time_for_session(best_window.ends_at, session)

    return {
        "present_at_start": True,
        "expected_for_full_session": False,
        "leave_time": best_window.ends_at,
        "warning": f"Leaves at {leave_time} before session ends",
    }


def person_is_expected_for_session_interval(
    db: Session,
    camp: Camp,
    person: Person,
    session: ProgrammeSession,
):
    return get_person_session_presence_info(
        db,
        camp,
        person,
        session,
    )["expected_for_full_session"]


def get_available_session_staff_people(
    db: Session,
    camp: Camp,
    session: ProgrammeSession | None = None,
):
    people = (
        db.query(Person)
        .filter(
            Person.camp_id == camp.id,
            Person.person_type.in_(PROGRAMME_STAFF_PERSON_TYPES),
        )
        .order_by(Person.person_type, Person.last_name, Person.first_name)
        .all()
    )

    if session is None:
        return people

    assigned_staff_person_ids = {
        person_id
        for (person_id,) in (
            db.query(ProgrammeSessionStaff.person_id)
            .filter(
                ProgrammeSessionStaff.camp_id == camp.id,
                ProgrammeSessionStaff.programme_session_id == session.id,
            )
            .all()
        )
    }

    available_people = []

    for person in people:
        if person.id in assigned_staff_person_ids:
            continue

        presence_info = get_person_session_presence_info(
            db,
            camp,
            person,
            session,
        )

        if not presence_info["present_at_start"]:
            continue

        # Temporary display-only attributes used by the Jinja dropdown.
        person.session_presence_warning = presence_info["warning"]
        available_people.append(person)

    return available_people

def get_session_staff_lookup(db: Session, camp: Camp, sessions):
    session_ids = [session.id for session in sessions]

    lookup = {session_id: [] for session_id in session_ids}

    if not session_ids:
        return lookup

    staff_rows = (
        db.query(ProgrammeSessionStaff, Person)
        .join(Person, Person.id == ProgrammeSessionStaff.person_id)
        .filter(
            ProgrammeSessionStaff.camp_id == camp.id,
            ProgrammeSessionStaff.programme_session_id.in_(session_ids),
            Person.camp_id == camp.id,
        )
        .order_by(
            ProgrammeSessionStaff.programme_session_id,
            ProgrammeSessionStaff.role,
            Person.last_name,
            Person.first_name,
        )
        .all()
    )

    for staff, person in staff_rows:
        lookup.setdefault(staff.programme_session_id, []).append(
            {
                "staff_id": staff.id,
                "person_id": person.id,
                "display_name": person_display_name(person),
                "person_type": person.person_type,
                "role": staff.role,
                "notes": staff.notes,
            }
        )

    return lookup


def build_programme_warnings(
    db: Session,
    camp: Camp,
    sessions,
    person_names,
    team_names,
    risk_statuses,
    session_staff_by_session_id,
):
    from collections import defaultdict

    warnings = []
    assigned_by_person = defaultdict(dict)

    def session_detail(session: ProgrammeSession):
        group_name = (
            team_names.get(session.participant_team_id, "Unknown group")
            if session.participant_team_id
            else "Whole camp"
        )
        return (
            f"{session.session_date} "
            f"{session.start_time.strftime('%H:%M')}–{session.end_time.strftime('%H:%M')} · "
            f"{session.title} · {group_name}"
        )

    def is_lead_staff_item(staff_item):
        return (staff_item.get("role") or "").strip().lower() == "lead"

    def is_adult_lead_staff_item(staff_item):
        if not is_lead_staff_item(staff_item):
            return False

        person_type = (staff_item.get("person_type") or "").strip().lower()
        return person_type in {"leader", "helper"}

    lead_person_ids = {
        staff_item["person_id"]
        for session in sessions
        for staff_item in session_staff_by_session_id.get(session.id, [])
        if is_lead_staff_item(staff_item)
    }

    lead_people_by_id = {}

    if lead_person_ids:
        lead_people = (
            db.query(Person)
            .filter(
                Person.camp_id == camp.id,
                Person.id.in_(lead_person_ids),
            )
            .all()
        )

        lead_people_by_id = {person.id: person for person in lead_people}

    for session in sessions:
        session_assignments = {}

        for staff_item in session_staff_by_session_id.get(session.id, []):
            session_assignments.setdefault(staff_item["person_id"], set()).add(staff_item["role"])

        for person_id, roles in session_assignments.items():
            assigned_by_person[person_id][session.id] = {
                "session": session,
                "roles": sorted(roles),
            }

        lead_items = [
            staff_item
            for staff_item in session_staff_by_session_id.get(session.id, [])
            if is_lead_staff_item(staff_item)
        ]

        adult_lead_items = [
            staff_item
            for staff_item in lead_items
            if is_adult_lead_staff_item(staff_item)
        ]

        non_adult_lead_items = [
            staff_item
            for staff_item in lead_items
            if not is_adult_lead_staff_item(staff_item)
        ]

        if not session_assignments:
            warnings.append(
                {
                    "severity": "high",
                    "title": "No staff assigned",
                    "detail": session_detail(session),
                    "url": f"/camps/{camp.id}/programme/{session.id}/edit",
                }
            )

        if not lead_items:
            warnings.append(
                {
                    "severity": "high",
                    "title": "No Lead assigned",
                    "detail": session_detail(session),
                    "url": f"/camps/{camp.id}/programme/{session.id}/edit",
                }
            )
        elif not adult_lead_items:
            warnings.append(
                {
                    "severity": "high",
                    "title": "No adult Lead assigned",
                    "detail": session_detail(session),
                    "url": f"/camps/{camp.id}/programme/{session.id}/edit",
                }
            )

        for lead_item in non_adult_lead_items:
            lead_name = lead_item.get("display_name") or "Unknown person"
            person_type = lead_item.get("person_type") or "Unknown type"

            warnings.append(
                {
                    "severity": "medium",
                    "title": f"Lead role assigned to {person_type}: {lead_name}",
                    "detail": f"{session_detail(session)} · Adult Lead still required",
                    "url": f"/camps/{camp.id}/programme/{session.id}/edit",
                }
            )

        if adult_lead_items:
            full_session_adult_lead_count = 0
            adult_lead_presence_problems = []

            for lead_item in adult_lead_items:
                lead_person = lead_people_by_id.get(lead_item["person_id"])
                lead_name = lead_item.get("display_name") or "Unknown person"

                if lead_person is None:
                    adult_lead_presence_problems.append(f"{lead_name} could not be found")
                    continue

                presence_info = get_person_session_presence_info(
                    db,
                    camp,
                    lead_person,
                    session,
                )

                if presence_info["expected_for_full_session"]:
                    full_session_adult_lead_count += 1
                    continue

                if not presence_info["present_at_start"]:
                    adult_lead_presence_problems.append(
                        f"{lead_name} is not expected at session start"
                    )
                else:
                    adult_lead_presence_problems.append(
                        f"{lead_name} {presence_info['warning'][0].lower()}{presence_info['warning'][1:]}"
                    )

            if full_session_adult_lead_count == 0:
                detail = session_detail(session)

                if adult_lead_presence_problems:
                    detail = f"{detail} · {'; '.join(adult_lead_presence_problems)}"

                warnings.append(
                    {
                        "severity": "high",
                        "title": "No adult Lead present for the full session",
                        "detail": detail,
                        "url": f"/camps/{camp.id}/programme/{session.id}/edit",
                    }
                )
            else:
                for problem in adult_lead_presence_problems:
                    warnings.append(
                        {
                            "severity": "medium",
                            "title": "Adult Lead coverage note",
                            "detail": f"{session_detail(session)} · {problem}",
                            "url": f"/camps/{camp.id}/programme/{session.id}/edit",
                        }
                    )

        if session.activity_id:
            risk_status = risk_statuses.get(session.activity_id, "Not Started")

            if risk_status != "Approved":
                warnings.append(
                    {
                        "severity": "medium",
                        "title": f"Risk assessment not approved: {risk_status}",
                        "detail": session_detail(session),
                        "url": f"/camps/{camp.id}/activities/{session.activity_id}/risk-assessment",
                    }
                )

    for person_id, assignments in assigned_by_person.items():
        items = list(assignments.values())

        for i, first in enumerate(items):
            for second in items[i + 1:]:
                a = first["session"]
                b = second["session"]

                if a.session_date != b.session_date:
                    continue

                overlaps = a.start_time < b.end_time and b.start_time < a.end_time

                if not overlaps:
                    continue

                person_name = person_names.get(person_id, "Unknown person")

                warnings.append(
                    {
                        "severity": "high",
                        "title": f"Staffing clash: {person_name}",
                        "detail": f"{session_detail(a)} overlaps with {session_detail(b)}",
                        "url": f"/camps/{camp.id}/programme",
                    }
                )

    severity_order = {"high": 0, "medium": 1, "low": 2}
    warnings.sort(key=lambda item: (severity_order.get(item["severity"], 99), item["title"], item["detail"]))

    return warnings


def pluralise_person_type(person_type: str, count: int):
    if count == 1:
        return person_type

    irregular = {
        "Young Person": "Young People",
        "Person": "People",
    }

    if person_type in irregular:
        return irregular[person_type]

    if person_type.endswith("y"):
        return f"{person_type[:-1]}ies"

    if person_type.endswith("s"):
        return person_type

    return f"{person_type}s"


def format_person_type_counts(counts):
    preferred_order = [
        "Leader",
        "Helper",
        "Young Leader",
        "Young Person",
        "Parent/Guardian",
        "Visitor",
    ]

    parts = []

    for person_type in preferred_order:
        count = counts.get(person_type, 0)

        if count:
            parts.append(f"{count} {pluralise_person_type(person_type, count)}")

    for person_type in sorted(set(counts) - set(preferred_order)):
        count = counts.get(person_type, 0)

        if count:
            parts.append(f"{count} {pluralise_person_type(person_type, count)}")

    return ", ".join(parts) if parts else "None"


def get_session_participant_people(db: Session, camp: Camp, session: ProgrammeSession):
    query = (
        db.query(Person)
        .filter(
            Person.camp_id == camp.id,
            Person.person_type == "Young Person",
        )
    )

    if session.participant_team_id:
        query = (
            query.join(TeamMembership, TeamMembership.person_id == Person.id)
            .filter(
                TeamMembership.camp_id == camp.id,
                TeamMembership.team_id == session.participant_team_id,
            )
        )

    return (
        query.distinct()
        .order_by(Person.last_name, Person.first_name)
        .all()
    )


def build_session_cover_summary(
    db: Session,
    camp: Camp,
    session: ProgrammeSession,
    session_staff,
):
    from collections import Counter

    participant_start_counts = Counter()
    participant_full_counts = Counter()

    unique_people_at_start = set()
    unique_people_full_session = set()
    unique_people_leaving_early = set()

    staff_person_ids = {
        item["person"].id
        for item in session_staff
        if item.get("person") is not None
    }

    for person in get_session_participant_people(db, camp, session):
        # If someone is explicitly assigned as staff, count them as staff/support,
        # not as an activity participant.
        if person.id in staff_person_ids:
            continue

        presence_info = get_person_session_presence_info(
            db,
            camp,
            person,
            session,
        )

        if presence_info["present_at_start"]:
            participant_start_counts[person.person_type] += 1
            unique_people_at_start.add(person.id)

        if presence_info["expected_for_full_session"]:
            participant_full_counts[person.person_type] += 1
            unique_people_full_session.add(person.id)

        if presence_info["present_at_start"] and not presence_info["expected_for_full_session"]:
            unique_people_leaving_early.add(person.id)

    staff_person_type_start_counts = Counter()
    staff_person_type_full_counts = Counter()
    staff_role_start_counts = Counter()
    staff_role_full_counts = Counter()

    staff_leaving_early = []
    adult_leads_at_start = []
    adult_leads_full_session = []

    for item in session_staff:
        staff = item["staff"]
        person = item["person"]
        role = (staff.role or "Other").strip() or "Other"
        role_key = role.lower()
        person_type = (person.person_type or "Unknown").strip() or "Unknown"
        display_name = item.get("display_name") or person_display_name(person)

        presence_info = get_person_session_presence_info(
            db,
            camp,
            person,
            session,
        )

        if presence_info["present_at_start"]:
            staff_person_type_start_counts[person_type] += 1
            staff_role_start_counts[role] += 1
            unique_people_at_start.add(person.id)

        if presence_info["expected_for_full_session"]:
            staff_person_type_full_counts[person_type] += 1
            staff_role_full_counts[role] += 1
            unique_people_full_session.add(person.id)

        if presence_info["present_at_start"] and not presence_info["expected_for_full_session"]:
            unique_people_leaving_early.add(person.id)

            if presence_info["warning"]:
                staff_leaving_early.append(
                    f"{display_name} {presence_info['warning'][0].lower()}{presence_info['warning'][1:]}"
                )

        if role_key == "lead" and person_type in {"Leader", "Helper"}:
            if presence_info["present_at_start"]:
                adult_leads_at_start.append(display_name)

            if presence_info["expected_for_full_session"]:
                adult_leads_full_session.append(display_name)

    return {
        "total_people_at_start": len(unique_people_at_start),
        "total_people_full_session": len(unique_people_full_session),
        "people_leaving_early_count": len(unique_people_leaving_early),
        "participants_at_start": format_person_type_counts(participant_start_counts),
        "participants_full_session": format_person_type_counts(participant_full_counts),
        "staff_person_types_at_start": format_person_type_counts(staff_person_type_start_counts),
        "staff_person_types_full_session": format_person_type_counts(staff_person_type_full_counts),
        "staff_roles_at_start": format_person_type_counts(staff_role_start_counts),
        "staff_roles_full_session": format_person_type_counts(staff_role_full_counts),
        "staff_leaving_early": "; ".join(staff_leaving_early) if staff_leaving_early else "None",
        "assigned_staff_count": len(session_staff),
        "adult_leads_at_start": ", ".join(adult_leads_at_start) if adult_leads_at_start else "",
        "adult_leads_full_session": ", ".join(adult_leads_full_session) if adult_leads_full_session else "",
        "adult_lead_ok": bool(adult_leads_at_start),
        "adult_lead_full_session_ok": bool(adult_leads_full_session),
    }


def build_session_roll_call(
    db: Session,
    camp: Camp,
    session: ProgrammeSession,
    session_staff,
    team_names,
):
    participant_rows = []
    staff_rows = []

    staff_person_ids = {
        item["person"].id
        for item in session_staff
        if item.get("person") is not None
    }

    participant_group = (
        team_names.get(session.participant_team_id, "Unknown group")
        if session.participant_team_id
        else "Whole camp"
    )

    for person in get_session_participant_people(db, camp, session):
        if person.id in staff_person_ids:
            continue

        presence_info = get_person_session_presence_info(
            db,
            camp,
            person,
            session,
        )

        if not presence_info["present_at_start"]:
            continue

        participant_rows.append(
            {
                "display_name": person_display_name(person),
                "person_type": person.person_type,
                "session_role": "Participant",
                "group": participant_group,
                "presence": presence_info["warning"] or "Expected full session",
                "notes": "",
            }
        )

    for item in session_staff:
        staff = item["staff"]
        person = item["person"]

        presence_info = get_person_session_presence_info(
            db,
            camp,
            person,
            session,
        )

        if not presence_info["present_at_start"]:
            continue

        staff_rows.append(
            {
                "display_name": item.get("display_name") or person_display_name(person),
                "person_type": person.person_type,
                "session_role": staff.role or "Session Staff",
                "group": "Session Staff",
                "presence": presence_info["warning"] or "Expected full session",
                "notes": staff.notes or "",
            }
        )

    participant_rows.sort(key=lambda row: row["display_name"])
    staff_rows.sort(key=lambda row: (row["session_role"], row["display_name"]))

    return {
        "participants": participant_rows,
        "staff": staff_rows,
        "total_at_start": len(participant_rows) + len(staff_rows),
    }


def ensure_programme_session_backup_schema(db: Session) -> None:
    columns = db.execute(text("PRAGMA table_info(programme_session_backup)")).mappings().all()

    if not columns:
        return

    column_names = {column["name"] for column in columns}

    if "activity_id" not in column_names:
        db.execute(text("ALTER TABLE programme_session_backup ADD COLUMN activity_id INTEGER"))
        db.commit()


def get_session_backup_plans(db: Session, camp: Camp, session: ProgrammeSession):
    ensure_programme_session_backup_schema(db)

    return (
        db.query(ProgrammeSessionBackup)
        .filter(
            ProgrammeSessionBackup.camp_id == camp.id,
            ProgrammeSessionBackup.programme_session_id == session.id,
        )
        .order_by(
            ProgrammeSessionBackup.sort_order,
            ProgrammeSessionBackup.title,
            ProgrammeSessionBackup.id,
        )
        .all()
    )


def migrate_legacy_session_leads(
    db: Session,
    camp: Camp,
    session: ProgrammeSession | None = None,
) -> None:
    query = db.query(ProgrammeSession).filter(
        ProgrammeSession.camp_id == camp.id,
        ProgrammeSession.lead_person_id.isnot(None),
    )

    if session is not None:
        query = query.filter(ProgrammeSession.id == session.id)

    sessions = query.all()
    changed = False

    for programme_session in sessions:
        legacy_lead_person_id = programme_session.lead_person_id

        if legacy_lead_person_id is None:
            continue

        person = (
            db.query(Person)
            .filter(
                Person.id == legacy_lead_person_id,
                Person.camp_id == camp.id,
            )
            .first()
        )

        if person is not None:
            existing_staff = (
                db.query(ProgrammeSessionStaff)
                .filter(
                    ProgrammeSessionStaff.camp_id == camp.id,
                    ProgrammeSessionStaff.programme_session_id == programme_session.id,
                    ProgrammeSessionStaff.person_id == person.id,
                )
                .first()
            )

            if existing_staff is None:
                db.add(
                    ProgrammeSessionStaff(
                        camp_id=camp.id,
                        programme_session_id=programme_session.id,
                        person_id=person.id,
                        role="Lead",
                        notes="Migrated from legacy Lead Person field",
                    )
                )
                changed = True
            else:
                current_role = (existing_staff.role or "").strip().lower()

                if current_role != "lead":
                    existing_staff.role = "Lead"

                    if existing_staff.notes:
                        if "Migrated from legacy Lead Person field" not in existing_staff.notes:
                            existing_staff.notes = (
                                existing_staff.notes.rstrip()
                                + "\nMigrated from legacy Lead Person field"
                            )
                    else:
                        existing_staff.notes = "Migrated from legacy Lead Person field"

                    changed = True

        programme_session.lead_person_id = None
        changed = True

    if changed:
        db.commit()


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

    session_staff_by_session_id = get_session_staff_lookup(db, camp, sessions)

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
            "session_staff_by_session_id": session_staff_by_session_id,
            "programme_warnings": build_programme_warnings(
                db,
                camp,
                sessions,
                person_names,
                team_names,
                risk_statuses,
                session_staff_by_session_id,
            ),
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

    migrate_legacy_session_leads(db, camp, session)
    session_staff = get_session_staff(db, camp, session)
    session_cover_summary = build_session_cover_summary(
        db,
        camp,
        session,
        session_staff,
    )

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
            "session_staff": session_staff,
            "session_cover_summary": session_cover_summary,
            "backup_plans": get_session_backup_plans(db, camp, session),
            "backup_reasons": PROGRAMME_BACKUP_REASONS,
            "available_staff_people": get_available_session_staff_people(db, camp, session),
            "staff_roles": PROGRAMME_STAFF_ROLES,
        },
    )


@router.get("/camps/{camp_id}/programme/{session_id}/print/roll-call", response_class=HTMLResponse)
async def print_session_roll_call(
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

    migrate_legacy_session_leads(db, camp, session)
    session_staff = get_session_staff(db, camp, session)
    session_cover_summary = build_session_cover_summary(
        db,
        camp,
        session,
        session_staff,
    )
    roll_call = build_session_roll_call(
        db,
        camp,
        session,
        session_staff,
        team_names,
    )

    return templates.TemplateResponse(
        "programme/print_session_roll_call.html",
        {
            "request": request,
            "camp": camp,
            "session": session,
            "activity_names": activity_names,
            "team_names": team_names,
            "session_cover_summary": session_cover_summary,
            "roll_call": roll_call,
        },
    )


@router.post("/camps/{camp_id}/programme/{session_id}/backup/add")
async def add_programme_session_backup(
    camp_id: int,
    session_id: int,
    title: str = Form(""),
    activity_id: str = Form(""),
    reason: str = Form(""),
    location: str = Form(""),
    duration_minutes: str = Form(""),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    session = (
        db.query(ProgrammeSession)
        .filter(ProgrammeSession.id == session_id, ProgrammeSession.camp_id == camp_id)
        .first()
    )

    if session is None:
        return RedirectResponse(url=f"/camps/{camp_id}/programme", status_code=303)

    ensure_programme_session_backup_schema(db)

    clean_title = title.strip()
    selected_activity_id = None
    selected_activity_name = ""

    if activity_id.strip():
        try:
            possible_activity_id = int(activity_id)
        except ValueError:
            possible_activity_id = None

        if possible_activity_id is not None:
            selected_activity = (
                db.query(Activity)
                .filter(
                    Activity.id == possible_activity_id,
                    Activity.camp_id == camp_id,
                )
                .first()
            )

            if selected_activity is not None:
                selected_activity_id = selected_activity.id
                selected_activity_name = selected_activity.name or ""

    if selected_activity_id or clean_title:
        parsed_duration = None

        if duration_minutes.strip():
            try:
                parsed_duration = int(duration_minutes)
            except ValueError:
                parsed_duration = None

        next_sort_order = (
            db.query(ProgrammeSessionBackup)
            .filter(
                ProgrammeSessionBackup.camp_id == camp_id,
                ProgrammeSessionBackup.programme_session_id == session_id,
            )
            .count()
        )

        backup_plan = ProgrammeSessionBackup(
            camp_id=camp_id,
            programme_session_id=session_id,
            title=clean_title or selected_activity_name,
            activity_id=selected_activity_id,
            reason=reason.strip() or None,
            location=location.strip() or None,
            duration_minutes=parsed_duration,
            notes=notes.strip() or None,
            sort_order=next_sort_order,
        )

        db.add(backup_plan)
        db.commit()

    return RedirectResponse(
        url=f"/camps/{camp_id}/programme/{session_id}",
        status_code=303,
    )


@router.post("/camps/{camp_id}/programme/{session_id}/backup/{backup_id}/delete")
async def delete_programme_session_backup(
    camp_id: int,
    session_id: int,
    backup_id: int,
    db: Session = Depends(get_db),
):
    backup_plan = (
        db.query(ProgrammeSessionBackup)
        .filter(
            ProgrammeSessionBackup.id == backup_id,
            ProgrammeSessionBackup.camp_id == camp_id,
            ProgrammeSessionBackup.programme_session_id == session_id,
        )
        .first()
    )

    if backup_plan is not None:
        db.delete(backup_plan)
        db.commit()

    return RedirectResponse(
        url=f"/camps/{camp_id}/programme/{session_id}",
        status_code=303,
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

    migrate_legacy_session_leads(db, camp, session)
    session_staff = get_session_staff(db, camp, session)
    available_staff_people = get_available_session_staff_people(db, camp, session)

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
            "session_staff": session_staff,
            "available_staff_people": available_staff_people,
            "staff_roles": PROGRAMME_STAFF_ROLES,
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
            "session_staff_by_session_id": get_session_staff_lookup(db, camp, sessions),
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

    session_staff_by_session_id = get_session_staff_lookup(db, camp, sessions)

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

        staff_summary = []
        seen_staff = set()

        for item in schedule["sessions"]:
            for staff_item in session_staff_by_session_id.get(item.id, []):
                key = (staff_item["person_id"], staff_item["role"])
                if key in seen_staff:
                    continue

                seen_staff.add(key)
                staff_summary.append(staff_item)

        schedule["staff_summary"] = staff_summary

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
            "session_staff_by_session_id": session_staff_by_session_id,
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
            "session_staff_by_session_id": get_session_staff_lookup(db, camp, sessions),
        },
    )





@router.get("/camps/{camp_id}/programme/print/leader-board", response_class=HTMLResponse)
async def print_leader_location_board(
    request: Request,
    camp_id: int,
    db: Session = Depends(get_db),
):
    from collections import defaultdict
    from datetime import time as day_time

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
            ProgrammeSession.end_time,
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

    session_ids = [session.id for session in sessions]

    lead_person_ids = {
        session.lead_person_id
        for session in sessions
        if session.lead_person_id is not None
    }

    people_by_id = {}

    if lead_person_ids:
        for person in (
            db.query(Person)
            .filter(Person.camp_id == camp.id, Person.id.in_(lead_person_ids))
            .all()
        ):
            people_by_id[person.id] = person

    session_staff_lookup = defaultdict(list)

    if session_ids:
        staff_rows = (
            db.query(ProgrammeSessionStaff, Person)
            .join(Person, Person.id == ProgrammeSessionStaff.person_id)
            .filter(
                ProgrammeSessionStaff.camp_id == camp.id,
                ProgrammeSessionStaff.programme_session_id.in_(session_ids),
                Person.camp_id == camp.id,
            )
            .order_by(
                ProgrammeSessionStaff.programme_session_id,
                ProgrammeSessionStaff.role,
                Person.last_name,
                Person.first_name,
            )
            .all()
        )

        for staff, person in staff_rows:
            people_by_id[person.id] = person
            session_staff_lookup[staff.programme_session_id].append(
                {
                    "person_id": person.id,
                    "role": staff.role or "Supporting Adult",
                }
            )

    def role_sort_key(role: str):
        order = {
            "Lead": 0,
            "Supporting Adult": 1,
            "Parent Helper": 2,
            "Young Leader": 3,
            "First Aider": 4,
            "Observer": 5,
            "Other": 6,
        }
        return order.get(role, 99)

    def session_assignments(session: ProgrammeSession):
        assigned = {}

        if session.lead_person_id is not None and session.lead_person_id in people_by_id:
            assigned.setdefault(session.lead_person_id, set()).add("Lead Person")

        for item in session_staff_lookup.get(session.id, []):
            assigned.setdefault(item["person_id"], set()).add(item["role"])

        return [
            {
                "person_id": person_id,
                "roles": sorted(roles, key=role_sort_key),
            }
            for person_id, roles in assigned.items()
        ]

    assignments_by_session_id = {
        session.id: session_assignments(session)
        for session in sessions
    }

    assigned_person_ids = sorted(
        {
            assignment["person_id"]
            for assignments in assignments_by_session_id.values()
            for assignment in assignments
        }
    )

    board_people = []

    for person_id in assigned_person_ids:
        person = people_by_id.get(person_id)

        if person is None:
            continue

        board_people.append(
            {
                "id": person.id,
                "name": person_display_name(person),
                "person_type": person.person_type,
            }
        )

    board_people.sort(key=lambda item: item["name"])

    sessions_by_date = defaultdict(list)

    for session in sessions:
        sessions_by_date[session.session_date].append(session)

    def overlaps(session, slot):
        return session.start_time < slot["end_time"] and session.end_time > slot["start_time"]

    days = []

    for session_date, day_sessions in sorted(sessions_by_date.items()):
        time_slots = []

        for session in day_sessions:
            slot_exists = any(
                slot["start_time"] == session.start_time
                and slot["end_time"] == session.end_time
                for slot in time_slots
            )

            if not slot_exists:
                time_slots.append(
                    {
                        "start_time": session.start_time,
                        "end_time": session.end_time,
                    }
                )

        time_slots = sorted(time_slots, key=lambda slot: (slot["start_time"], slot["end_time"]))

        periods = [
            {
                "label": "Morning / AM",
                "columns": [
                    slot for slot in time_slots
                    if slot["start_time"] < day_time(12, 0)
                ],
            },
            {
                "label": "Afternoon & Evening / PM",
                "columns": [
                    slot for slot in time_slots
                    if slot["start_time"] >= day_time(12, 0)
                ],
            },
        ]

        chunks = []

        for period in periods:
            columns = period["columns"]

            if not columns:
                continue

            rows = []

            for person in board_people:
                cells = []

                for column in columns:
                    cell_items = []

                    for session in day_sessions:
                        if not overlaps(session, column):
                            continue

                        matching_assignments = [
                            assignment
                            for assignment in assignments_by_session_id.get(session.id, [])
                            if assignment["person_id"] == person["id"]
                        ]

                        for assignment in matching_assignments:
                            cell_items.append(
                                {
                                    "session": session,
                                    "roles": ", ".join(assignment["roles"]),
                                }
                            )

                    cells.append(cell_items)

                if any(cells):
                    rows.append(
                        {
                            "name": person["name"],
                            "person_type": person["person_type"],
                            "cells": cells,
                        }
                    )

            unassigned_cells = []

            for column in columns:
                cell_items = []

                for session in day_sessions:
                    if not overlaps(session, column):
                        continue

                    if not assignments_by_session_id.get(session.id):
                        cell_items.append(
                            {
                                "session": session,
                                "roles": "No staff assigned",
                            }
                        )

                unassigned_cells.append(cell_items)

            if any(unassigned_cells):
                rows.append(
                    {
                        "name": "Unassigned",
                        "person_type": "",
                        "cells": unassigned_cells,
                    }
                )

            if rows:
                chunks.append(
                    {
                        "label": period["label"],
                        "columns": columns,
                        "rows": rows,
                    }
                )

        days.append(
            {
                "session_date": session_date,
                "chunks": chunks,
            }
        )

    return templates.TemplateResponse(
        "programme/print_leader_board.html",
        {
            "request": request,
            "camp": camp,
            "days": days,
            "team_names": team_names,
        },
    )


@router.post("/camps/{camp_id}/programme/{session_id}/staff/add")
async def add_programme_session_staff(
    camp_id: int,
    session_id: int,
    person_id: int = Form(...),
    role: str = Form("Supporting Adult"),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return RedirectResponse(url="/", status_code=303)

    session = (
        db.query(ProgrammeSession)
        .filter(ProgrammeSession.id == session_id, ProgrammeSession.camp_id == camp.id)
        .first()
    )

    if session is None:
        return RedirectResponse(url=f"/camps/{camp.id}/programme", status_code=303)

    person = (
        db.query(Person)
        .filter(Person.id == person_id, Person.camp_id == camp.id)
        .first()
    )

    if person is None:
        return RedirectResponse(url=f"/camps/{camp.id}/programme/{session.id}", status_code=303)

    clean_role = role.strip() or "Supporting Adult"

    if clean_role not in PROGRAMME_STAFF_ROLES:
        clean_role = "Other"

    existing = (
        db.query(ProgrammeSessionStaff)
        .filter(
            ProgrammeSessionStaff.camp_id == camp.id,
            ProgrammeSessionStaff.programme_session_id == session.id,
            ProgrammeSessionStaff.person_id == person.id,
        )
        .first()
    )

    if existing:
        existing.role = clean_role
        existing.notes = notes.strip() or None
    else:
        db.add(
            ProgrammeSessionStaff(
                camp_id=camp.id,
                programme_session_id=session.id,
                person_id=person.id,
                role=clean_role,
                notes=notes.strip() or None,
            )
        )

    db.commit()

    return RedirectResponse(url=f"/camps/{camp.id}/programme/{session.id}", status_code=303)


@router.post("/camps/{camp_id}/programme/{session_id}/staff/{staff_id}/edit")
async def update_programme_session_staff(
    camp_id: int,
    session_id: int,
    staff_id: int,
    role: str = Form(...),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    staff_item = (
        db.query(ProgrammeSessionStaff)
        .filter(
            ProgrammeSessionStaff.id == staff_id,
            ProgrammeSessionStaff.camp_id == camp_id,
            ProgrammeSessionStaff.programme_session_id == session_id,
        )
        .first()
    )

    if staff_item is not None:
        clean_role = role.strip()
        staff_item.role = clean_role or staff_item.role
        staff_item.notes = notes.strip() or None
        db.commit()

    return RedirectResponse(
        url=f"/camps/{camp_id}/programme/{session_id}",
        status_code=303,
    )

@router.post("/camps/{camp_id}/programme/{session_id}/staff/{staff_id}/delete")
async def delete_programme_session_staff(
    camp_id: int,
    session_id: int,
    staff_id: int,
    db: Session = Depends(get_db),
):
    staff = (
        db.query(ProgrammeSessionStaff)
        .filter(
            ProgrammeSessionStaff.id == staff_id,
            ProgrammeSessionStaff.camp_id == camp_id,
            ProgrammeSessionStaff.programme_session_id == session_id,
        )
        .first()
    )

    if staff is not None:
        db.delete(staff)
        db.commit()

    return RedirectResponse(url=f"/camps/{camp_id}/programme/{session_id}", status_code=303)
