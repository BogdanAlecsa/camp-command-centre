from datetime import datetime, time
from pathlib import Path
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Camp, ParticipatingGroup, Person, PresenceWindow, Section
from app.services.presence import (
    SCOPE_CAMP,
    SCOPE_GROUP,
    SCOPE_PERSON,
    SCOPE_SECTION,
    build_presence_window_lookup,
    format_window,
    get_effective_presence_windows,
    is_expected_present,
)


BASE_DIR = Path(__file__).resolve().parents[1]
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter()


def parse_datetime_local(value: str | None):
    value = (value or "").strip()

    if not value:
        return None

    return datetime.fromisoformat(value)


def display_name(person: Person):
    return f"{person.first_name} {person.last_name}".strip()


def format_dt(value: datetime):
    return value.strftime("%a %d %b %H:%M")



def presence_redirect_url(camp_id: int, at_time: str | None = None):
    if at_time:
        return f"/camps/{camp_id}/presence?" + urlencode({"at_time": at_time})
    return f"/camps/{camp_id}/presence"


def parse_scope_ref(scope_ref: str):
    scope_type, _, raw_scope_id = (scope_ref or "").partition(":")
    scope_id = int(raw_scope_id) if raw_scope_id else None
    return scope_type, scope_id


def validate_presence_scope(db: Session, camp: Camp, scope_type: str, scope_id: int | None):
    if scope_type == SCOPE_CAMP:
        return None

    if scope_type == SCOPE_GROUP:
        return (
            db.query(ParticipatingGroup)
            .filter(ParticipatingGroup.id == scope_id, ParticipatingGroup.camp_id == camp.id)
            .first()
        )

    if scope_type == SCOPE_SECTION:
        return (
            db.query(Section)
            .filter(Section.id == scope_id, Section.camp_id == camp.id)
            .first()
        )

    if scope_type == SCOPE_PERSON:
        return (
            db.query(Person)
            .filter(Person.id == scope_id, Person.camp_id == camp.id)
            .first()
        )

    return None


@router.post("/camps/{camp_id}/presence/rules/add")
async def add_presence_rule(
    camp_id: int,
    scope_ref: str = Form(...),
    starts_at: str = Form(...),
    ends_at: str = Form(...),
    status: str = Form("Expected"),
    notes: str = Form(""),
    return_at_time: str = Form(""),
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return RedirectResponse(url="/camps", status_code=303)

    try:
        scope_type, scope_id = parse_scope_ref(scope_ref)
        clean_starts_at = datetime.fromisoformat(starts_at)
        clean_ends_at = datetime.fromisoformat(ends_at)
    except ValueError:
        return RedirectResponse(url=presence_redirect_url(camp.id, return_at_time), status_code=303)

    allowed_statuses = {"Expected", "Partial", "Not Attending", "Unknown"}
    clean_status = status if status in allowed_statuses else "Expected"

    if clean_starts_at >= clean_ends_at:
        return RedirectResponse(url=presence_redirect_url(camp.id, return_at_time), status_code=303)

    if scope_type != SCOPE_CAMP and validate_presence_scope(db, camp, scope_type, scope_id) is None:
        return RedirectResponse(url=presence_redirect_url(camp.id, return_at_time), status_code=303)

    db.add(
        PresenceWindow(
            camp_id=camp.id,
            scope_type=scope_type,
            scope_id=scope_id,
            starts_at=clean_starts_at,
            ends_at=clean_ends_at,
            status=clean_status,
            notes=notes.strip() or None,
        )
    )
    db.commit()

    return RedirectResponse(url=presence_redirect_url(camp.id, return_at_time), status_code=303)


@router.post("/camps/{camp_id}/presence/rules/{rule_id}/delete")
async def delete_presence_rule(
    camp_id: int,
    rule_id: int,
    return_at_time: str = Form(""),
    db: Session = Depends(get_db),
):
    rule = (
        db.query(PresenceWindow)
        .filter(PresenceWindow.id == rule_id, PresenceWindow.camp_id == camp_id)
        .first()
    )

    if rule:
        db.delete(rule)
        db.commit()

    return RedirectResponse(url=presence_redirect_url(camp_id, return_at_time), status_code=303)


@router.get("/camps/{camp_id}/presence", response_class=HTMLResponse)
async def presence_dashboard(
    request: Request,
    camp_id: int,
    at_time: str | None = None,
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Camp not found."},
            status_code=404,
        )

    try:
        selected_at = parse_datetime_local(at_time)
    except ValueError:
        selected_at = None

    if selected_at is None:
        selected_at = datetime.combine(camp.start_date, time(18, 0))

    people = (
        db.query(Person)
        .filter(Person.camp_id == camp.id)
        .order_by(Person.person_type, Person.last_name, Person.first_name)
        .all()
    )

    sections = (
        db.query(Section)
        .filter(Section.camp_id == camp.id)
        .order_by(Section.sort_order, Section.name)
        .all()
    )

    groups = (
        db.query(ParticipatingGroup)
        .filter(ParticipatingGroup.camp_id == camp.id)
        .order_by(ParticipatingGroup.sort_order, ParticipatingGroup.name)
        .all()
    )

    windows = (
        db.query(PresenceWindow)
        .filter(PresenceWindow.camp_id == camp.id)
        .order_by(PresenceWindow.scope_type, PresenceWindow.scope_id, PresenceWindow.starts_at)
        .all()
    )

    section_lookup = {section.id: section for section in sections}
    group_lookup = {group.id: group for group in groups}
    windows_by_scope = build_presence_window_lookup(windows)

    present_rows = []
    absent_rows = []

    for person in people:
        section = section_lookup.get(person.home_section_id) if person.home_section_id else None
        group = group_lookup.get(section.participating_group_id) if section and section.participating_group_id else None

        effective_presence = get_effective_presence_windows(
            camp=camp,
            person=person,
            section_lookup=section_lookup,
            group_lookup=group_lookup,
            windows_by_scope=windows_by_scope,
        )

        row = {
            "person": person,
            "display_name": display_name(person),
            "section_name": section.name if section else "No section",
            "group_name": group.name if group else "No group",
            "source_label": effective_presence["source_label"],
            "windows": [format_window(window) for window in effective_presence["windows"]],
        }

        if is_expected_present(effective_presence, selected_at):
            present_rows.append(row)
        else:
            absent_rows.append(row)

    present_by_group = {}
    present_by_section = {}
    present_by_type = {}

    for row in present_rows:
        present_by_group[row["group_name"]] = present_by_group.get(row["group_name"], 0) + 1
        present_by_section[row["section_name"]] = present_by_section.get(row["section_name"], 0) + 1
        present_by_type[row["person"].person_type] = present_by_type.get(row["person"].person_type, 0) + 1

    summary_groups = sorted(present_by_group.items(), key=lambda item: item[0])
    summary_sections = sorted(present_by_section.items(), key=lambda item: item[0])
    summary_types = sorted(present_by_type.items(), key=lambda item: item[0])

    # Young Leaders are under 18. They may help, but they must not be counted
    # as responsible adult cover.
    responsible_adult_types = {"Leader", "Helper"}
    present_responsible_adult_count = sum(
        1 for row in present_rows if row["person"].person_type in responsible_adult_types
    )
    present_young_leader_count = sum(
        1 for row in present_rows if row["person"].person_type == "Young Leader"
    )
    present_young_person_count = sum(
        1 for row in present_rows if row["person"].person_type == "Young Person"
    )

    rule_rows = []

    for window in windows:
        if window.scope_type == SCOPE_CAMP:
            scope_label = "Camp default"
        elif window.scope_type == SCOPE_GROUP:
            group = group_lookup.get(window.scope_id)
            scope_label = f"Group: {group.name}" if group else f"Group #{window.scope_id}"
        elif window.scope_type == SCOPE_SECTION:
            section = section_lookup.get(window.scope_id)
            scope_label = f"Section: {section.name}" if section else f"Section #{window.scope_id}"
        elif window.scope_type == SCOPE_PERSON:
            person = db.get(Person, window.scope_id)
            scope_label = f"Person: {display_name(person)}" if person else f"Person #{window.scope_id}"
        else:
            scope_label = window.scope_type

        rule_rows.append(
            {
                "rule_id": window.id,
                "scope_label": scope_label,
                "window": format_window(window),
            }
        )

    return templates.TemplateResponse(
        "presence/dashboard.html",
        {
            "request": request,
            "camp": camp,
            "selected_at": selected_at,
            "selected_at_input": selected_at.strftime("%Y-%m-%dT%H:%M"),
            "present_rows": present_rows,
            "absent_rows": absent_rows,
            "summary_groups": summary_groups,
            "summary_sections": summary_sections,
            "summary_types": summary_types,
            "present_responsible_adult_count": present_responsible_adult_count,
            "present_young_leader_count": present_young_leader_count,
            "present_young_person_count": present_young_person_count,
            "rule_rows": rule_rows,
            "groups": groups,
            "sections": sections,
            "people": people,
            "group_lookup": group_lookup,
            "presence_statuses": ["Expected", "Partial", "Not Attending", "Unknown"],
            "rule_default_start_input": datetime.combine(camp.start_date, time(18, 0)).strftime("%Y-%m-%dT%H:%M"),
            "rule_default_end_input": datetime.combine(camp.end_date, time(14, 0)).strftime("%Y-%m-%dT%H:%M"),
            "format_dt": format_dt,
        },
    )
