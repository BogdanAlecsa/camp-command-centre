from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.database import Base, SessionLocal, engine
from app.models import Camp, Person, ProgrammeSession, ProgrammeSessionStaff


CAMP_NAME = "Sample 3-Day Scout Camp"


def get_camp(db):
    camp = db.query(Camp).filter(Camp.name == CAMP_NAME).first()
    if camp is None:
        raise RuntimeError(f"Could not find camp named {CAMP_NAME!r}.")
    return camp


def get_person(db, camp, first_name, last_name):
    person = (
        db.query(Person)
        .filter(
            Person.camp_id == camp.id,
            Person.first_name == first_name,
            Person.last_name == last_name,
        )
        .first()
    )

    if person is None:
        raise RuntimeError(f"Could not find person: {first_name} {last_name}")

    return person


def find_session(db, camp, *title_parts, slot=None):
    query = db.query(ProgrammeSession).filter(ProgrammeSession.camp_id == camp.id)

    for part in title_parts:
        query = query.filter(ProgrammeSession.title.ilike(f"%{part}%"))

    if slot is not None:
        query = query.filter(ProgrammeSession.rotation_slot_number == slot)

    session = query.order_by(
        ProgrammeSession.session_date,
        ProgrammeSession.start_time,
        ProgrammeSession.title,
    ).first()

    if session is None:
        raise RuntimeError(f"Could not find session containing {title_parts}, slot={slot}")

    return session


def add_staff(db, camp, session, person, role, notes=None):
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
        existing.role = role
        existing.notes = notes
    else:
        db.add(
            ProgrammeSessionStaff(
                camp_id=camp.id,
                programme_session_id=session.id,
                person_id=person.id,
                role=role,
                notes=notes,
            )
        )


def main():
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        camp = get_camp(db)

        alice = get_person(db, camp, "Alice", "Morgan")
        ben = get_person(db, camp, "Ben", "Taylor")
        cara = get_person(db, camp, "Cara", "Jenkins")
        emma = get_person(db, camp, "Emma", "Shaw")
        felix = get_person(db, camp, "Felix", "Brown")

        db.query(ProgrammeSessionStaff).filter(
            ProgrammeSessionStaff.camp_id == camp.id
        ).delete(synchronize_session=False)

        arrival = find_session(db, camp, "Arrival")
        campfire = find_session(db, camp, "Opening Campfire")
        lunch = find_session(db, camp, "Lunch")
        lights_out = find_session(db, camp, "Lights Out")
        reflection = find_session(db, camp, "Reflection Circle")

        fox_pioneering_slot_1 = find_session(db, camp, "Fox Patrol", "Pioneering", slot=1)
        falcon_pioneering_slot_2 = find_session(db, camp, "Falcon Patrol", "Pioneering", slot=2)

        arrival.lead_person_id = alice.id
        campfire.lead_person_id = ben.id
        lunch.lead_person_id = cara.id

        # Deliberate warning: no lead and no staff.
        lights_out.lead_person_id = None

        # Deliberate warning: no lead, but has staff.
        reflection.lead_person_id = None

        add_staff(db, camp, arrival, cara, "Lead", "Registration and setup support.")
        add_staff(db, camp, arrival, felix, "Young Leader", "Help welcome young people.")

        add_staff(db, camp, campfire, alice, "Supporting Adult", "Support campfire supervision.")
        add_staff(db, camp, lunch, ben, "Supporting Adult", "Help with lunch service.")

        # Deliberate clash: Cara is already leading Backwoods at the same slot.
        add_staff(db, camp, fox_pioneering_slot_1, cara, "Supporting Adult", "Deliberate clash test.")

        # Deliberate clash: Felix is already leading Woodland at this slot.
        add_staff(db, camp, falcon_pioneering_slot_2, felix, "Supporting Adult", "Deliberate clash test.")

        add_staff(db, camp, reflection, felix, "First Aider", "Present for evening reflection.")

        db.commit()

        print("Programme staff test data seeded.")
        print("Added normal staff assignments.")
        print("Added deliberate clash warnings.")
        print("Added missing lead / missing staff examples.")


if __name__ == "__main__":
    main()
