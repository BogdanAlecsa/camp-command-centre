from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.database import SessionLocal
from app.models import Camp, ParticipatingGroup, Section, Person


SAMPLE_CAMP_NAME = "Sample 3-Day Scout Camp"


GROUPS = [
    {
        "name": "1st Northfield Scout Group",
        "contact_name": "Sam River",
        "contact_email": "sam.river@example.test",
        "contact_phone": "07123 100001",
        "sort_order": 1,
        "notes": "Main organising group for the sample camp.",
    },
    {
        "name": "3rd Brookvale Scout Group",
        "contact_name": "Avery Glen",
        "contact_email": "avery.glen@example.test",
        "contact_phone": "07123 100002",
        "sort_order": 2,
        "notes": "Visiting group used for multi-group testing.",
    },
    {
        "name": "8th Hilltop Scout Group",
        "contact_name": "Robin Ash",
        "contact_email": "robin.ash@example.test",
        "contact_phone": "07123 100003",
        "sort_order": 3,
        "notes": "Second visiting group used for section and people testing.",
    },
    {
        "name": "Empty Test Group",
        "contact_name": None,
        "contact_email": None,
        "contact_phone": None,
        "sort_order": 99,
        "notes": "Deliberately empty group for group delete testing.",
    },
]


SECTIONS = [
    ("1st Northfield Scout Group", "Cubs", "Cubs", 1, "Home Cubs section."),
    ("1st Northfield Scout Group", "Scouts", "Scouts", 2, "Home Scouts section."),
    ("1st Northfield Scout Group", "Adult Volunteers", "Adults", 3, "Leaders, helpers and young leaders."),
    ("3rd Brookvale Scout Group", "Cubs", "Cubs", 1, "Visiting Cubs section."),
    ("3rd Brookvale Scout Group", "Scouts", "Scouts", 2, "Visiting Scouts section."),
    ("8th Hilltop Scout Group", "Cubs", "Cubs", 1, "Visiting Cubs section."),
    ("8th Hilltop Scout Group", "Scouts", "Scouts", 2, "Visiting Scouts section."),
    ("8th Hilltop Scout Group", "Empty Test Section", "Other", 99, "Deliberately empty section for section delete testing."),
]


PERSON_SECTION_MAP = {
    "Rowan Vale": ("1st Northfield Scout Group", "Adult Volunteers"),
    "Nico Hart": ("1st Northfield Scout Group", "Adult Volunteers"),
    "Mina Brook": ("1st Northfield Scout Group", "Adult Volunteers"),
    "Toby Finch": ("1st Northfield Scout Group", "Adult Volunteers"),
    "Isla Park": ("1st Northfield Scout Group", "Adult Volunteers"),
    "Owen Pike": ("1st Northfield Scout Group", "Adult Volunteers"),

    "Jasper Reed": ("1st Northfield Scout Group", "Cubs"),
    "Maya Stone": ("1st Northfield Scout Group", "Cubs"),
    "Harry Vale": ("1st Northfield Scout Group", "Scouts"),

    "Noah Field": ("3rd Brookvale Scout Group", "Cubs"),
    "Lily Brook": ("3rd Brookvale Scout Group", "Cubs"),
    "Sofia Lane": ("3rd Brookvale Scout Group", "Scouts"),
    "Leo Moss": ("3rd Brookvale Scout Group", "Scouts"),

    "Amelia Quinn": ("8th Hilltop Scout Group", "Cubs"),
    "Oscar Hale": ("8th Hilltop Scout Group", "Scouts"),
    "Grace Rowan": ("8th Hilltop Scout Group", "Scouts"),
}


PROVISIONAL_PEOPLE = {"Noah Field", "Lily Brook"}

ATTENDANCE_BY_NAME = {
    "Noah Field": "Maybe",
    "Lily Brook": "Unknown",
    "Oscar Hale": "Invited",
    "Grace Rowan": "Attending",
}


def full_name(person: Person) -> str:
    return f"{person.first_name} {person.last_name}"


def main() -> None:
    with SessionLocal() as db:
        camp = db.query(Camp).filter(Camp.name == SAMPLE_CAMP_NAME).first()

        if not camp:
            raise SystemExit(
                f"Could not find '{SAMPLE_CAMP_NAME}'. Run scripts/seed_dream_camp.py first."
            )

        # Remove existing group/section seed data for this camp.
        people = db.query(Person).filter(Person.camp_id == camp.id).all()
        for person in people:
            person.home_section_id = None
            person.section_unit = None

        db.query(Section).filter(Section.camp_id == camp.id).delete(synchronize_session=False)
        db.query(ParticipatingGroup).filter(ParticipatingGroup.camp_id == camp.id).delete(synchronize_session=False)
        db.flush()

        groups_by_name = {}

        for row in GROUPS:
            group = ParticipatingGroup(
                camp_id=camp.id,
                name=row["name"],
                group_type="Scout Group",
                contact_name=row["contact_name"],
                contact_email=row["contact_email"],
                contact_phone=row["contact_phone"],
                sort_order=row["sort_order"],
                is_active=True,
                notes=row["notes"],
            )
            db.add(group)
            db.flush()
            groups_by_name[group.name] = group

        sections_by_key = {}

        for group_name, section_name, section_type, sort_order, notes in SECTIONS:
            section = Section(
                camp_id=camp.id,
                participating_group_id=groups_by_name[group_name].id,
                name=section_name,
                section_type=section_type,
                sort_order=sort_order,
                is_active=True,
                notes=notes,
            )
            db.add(section)
            db.flush()
            sections_by_key[(group_name, section_name)] = section

        assigned_count = 0

        for person in people:
            name = full_name(person)
            section_key = PERSON_SECTION_MAP.get(name)

            if not section_key:
                continue

            section = sections_by_key[section_key]
            person.home_section_id = section.id
            person.section_unit = section.name
            person.information_source = "Dream Camp group/section seed"
            person.is_provisional = name in PROVISIONAL_PEOPLE

            if name in ATTENDANCE_BY_NAME:
                person.attendance_status = ATTENDANCE_BY_NAME[name]
            elif person.person_type == "Young Person":
                person.attendance_status = "Attending"

            assigned_count += 1

        db.commit()

        print(f"Updated {SAMPLE_CAMP_NAME}.")
        print(f"Created {len(GROUPS)} participating groups.")
        print(f"Created {len(SECTIONS)} sections.")
        print(f"Assigned {assigned_count} people to sections.")
        print("Included Empty Test Group and Empty Test Section for delete testing.")


if __name__ == "__main__":
    main()