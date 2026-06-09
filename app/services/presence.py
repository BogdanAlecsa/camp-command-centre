from __future__ import annotations

from datetime import datetime, time
from typing import Iterable

from app.models import Camp, ParticipatingGroup, Person, PresenceWindow, Section


SCOPE_CAMP = "camp"
SCOPE_GROUP = "participating_group"
SCOPE_SECTION = "section"
SCOPE_PERSON = "person"

PRESENT_STATUSES = {"Expected", "Partial", "Attending"}


def scope_key(scope_type: str, scope_id: int | None):
    return (scope_type, scope_id or 0)


def build_presence_window_lookup(windows: Iterable[PresenceWindow]):
    lookup = {}

    for window in windows:
        lookup.setdefault(scope_key(window.scope_type, window.scope_id), []).append(window)

    for items in lookup.values():
        items.sort(key=lambda item: (item.starts_at, item.ends_at, item.id))

    return lookup


def fallback_camp_window(camp: Camp):
    starts_at = datetime.combine(camp.start_date, time(0, 0))
    ends_at = datetime.combine(camp.end_date, time(23, 59))

    return {
        "starts_at": starts_at,
        "ends_at": ends_at,
        "status": "Expected",
        "notes": "Fallback from camp dates. Add a camp presence rule to set proper arrival/departure times.",
    }


def get_effective_presence_windows(
    *,
    camp: Camp,
    person: Person,
    section_lookup: dict[int, Section],
    group_lookup: dict[int, ParticipatingGroup],
    windows_by_scope,
):
    person_windows = windows_by_scope.get(scope_key(SCOPE_PERSON, person.id), [])
    if person_windows:
        return {
            "source_type": SCOPE_PERSON,
            "source_label": "Person override",
            "windows": person_windows,
        }

    section = section_lookup.get(person.home_section_id) if person.home_section_id else None

    if section:
        section_windows = windows_by_scope.get(scope_key(SCOPE_SECTION, section.id), [])
        if section_windows:
            return {
                "source_type": SCOPE_SECTION,
                "source_label": f"Section override: {section.name}",
                "windows": section_windows,
            }

        group = group_lookup.get(section.participating_group_id) if section.participating_group_id else None

        if group:
            group_windows = windows_by_scope.get(scope_key(SCOPE_GROUP, group.id), [])
            if group_windows:
                return {
                    "source_type": SCOPE_GROUP,
                    "source_label": f"Group override: {group.name}",
                    "windows": group_windows,
                }

    camp_windows = windows_by_scope.get(scope_key(SCOPE_CAMP, None), [])
    if camp_windows:
        return {
            "source_type": SCOPE_CAMP,
            "source_label": "Camp default",
            "windows": camp_windows,
        }

    return {
        "source_type": "fallback",
        "source_label": "Camp date fallback",
        "windows": [fallback_camp_window(camp)],
    }


def window_contains_at(window, at_time: datetime):
    starts_at = window["starts_at"] if isinstance(window, dict) else window.starts_at
    ends_at = window["ends_at"] if isinstance(window, dict) else window.ends_at
    status = window["status"] if isinstance(window, dict) else window.status

    if status not in PRESENT_STATUSES:
        return False

    return starts_at <= at_time < ends_at


def is_expected_present(effective_presence, at_time: datetime):
    return any(window_contains_at(window, at_time) for window in effective_presence["windows"])


def format_window(window):
    starts_at = window["starts_at"] if isinstance(window, dict) else window.starts_at
    ends_at = window["ends_at"] if isinstance(window, dict) else window.ends_at
    status = window["status"] if isinstance(window, dict) else window.status
    notes = window["notes"] if isinstance(window, dict) else window.notes

    return {
        "starts_at": starts_at,
        "ends_at": ends_at,
        "status": status,
        "notes": notes,
    }
