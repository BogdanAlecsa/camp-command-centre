from datetime import datetime, time, timedelta
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.database import Base, SessionLocal, engine
from app.models import Camp, ParticipatingGroup, Person, PresenceWindow, Section


SAMPLE_CAMP_NAME = "Sample 3-Day Scout Camp"


def combine(day, hour, minute=0):
    return datetime.combine(day, time(hour, minute))


def full_name(person):
    return f"{person.first_name} {person.last_name}".strip()


def main():
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        camp = db.query(Camp).filter(Camp.name == SAMPLE_CAMP_NAME).first()

        if camp is None:
            raise SystemExit(f"Could not find '{SAMPLE_CAMP_NAME}'. Run reset_dream_camp.py first.")

        db.query(PresenceWindow).filter(PresenceWindow.camp_id == camp.id).delete(synchronize_session=False)
        db.flush()

        day0 = camp.start_date
        day1 = camp.start_date + timedelta(days=1)
        day2 = camp.start_date + timedelta(days=2)

        groups = {
            group.name: group
            for group in db.query(ParticipatingGroup).filter(ParticipatingGroup.camp_id == camp.id).all()
        }

        sections = {
            (groups_by_name.name if (groups_by_name := db.get(ParticipatingGroup, section.participating_group_id)) else "", section.name): section
            for section in db.query(Section).filter(Section.camp_id == camp.id).all()
        }

        people = {
            full_name(person): person
            for person in db.query(Person).filter(Person.camp_id == camp.id).all()
        }

        def add_window(scope_type, scope_id, starts_at, ends_at, status="Expected", notes=None):
            db.add(
                PresenceWindow(
                    camp_id=camp.id,
                    scope_type=scope_type,
                    scope_id=scope_id,
                    starts_at=starts_at,
                    ends_at=ends_at,
                    status=status,
                    notes=notes,
                )
            )

        # Camp default: full weekend, but with realistic arrival/departure times.
        add_window(
            "camp",
            None,
            datetime.combine(camp.start_date, camp.start_time or time(18, 0)),
            datetime.combine(camp.end_date, camp.end_time or time(14, 0)),
            notes="Default camp presence window from camp setup.",
        )

        # Group override: Hilltop joins on Saturday morning.
        hilltop = groups.get("8th Hilltop Scout Group")
        if hilltop:
            add_window(
                "participating_group",
                hilltop.id,
                combine(day1, 9, 30),
                combine(day2, 14, 0),
                notes="Hilltop group arrives Saturday morning.",
            )

        # Section override: Brookvale Scouts leave earlier on Sunday.
        brookvale_scouts = sections.get(("3rd Brookvale Scout Group", "Scouts"))
        if brookvale_scouts:
            add_window(
                "section",
                brookvale_scouts.id,
                combine(day0, 18, 0),
                combine(day2, 10, 0),
                notes="Brookvale Scouts depart before Sunday lunch.",
            )

        # Person exceptions.
        person_exceptions = {
            "Mina Brook": (combine(day0, 18, 0), combine(day1, 20, 0), "Leaves after Saturday evening programme."),
            "Noah Field": (combine(day1, 10, 0), combine(day2, 14, 0), "Late arrival on Saturday morning."),
            "Toby Finch": (combine(day1, 9, 0), combine(day1, 17, 0), "Day helper on Saturday only."),
            "Owen Pike": (combine(day1, 18, 0), combine(day2, 14, 0), "Young Leader joins from Saturday evening."),
        }

        for name, (starts_at, ends_at, notes) in person_exceptions.items():
            person = people.get(name)
            if person:
                add_window(
                    "person",
                    person.id,
                    starts_at,
                    ends_at,
                    notes=notes,
                )

        db.commit()

        print("Seeded Dream Camp presence windows.")
        print("Camp default plus group, section and person overrides added.")


if __name__ == "__main__":
    main()
