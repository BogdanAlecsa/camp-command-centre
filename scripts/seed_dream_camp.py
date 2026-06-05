from datetime import date
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


from sqlalchemy import text

from app.database import Base, SessionLocal, engine
from app.models import (
    Camp,
    Person,
    Team,
    TeamMembership,
    Task,
    TaskAssignment,
    TaskPhase,
    TaskCategory,
)


SAMPLE_CAMP_NAME = "Sample 3-Day Scout Camp"


PHASES = [
    ("Early Planning", "Early decisions, booking, permissions and outline planning.", 1),
    ("Preparation", "Main preparation work before the final week.", 2),
    ("Final Week", "Final checks and jobs in the last week before camp.", 3),
    ("Camp Setup", "Arrival, setup and site preparation.", 4),
    ("During Camp", "Jobs and checks while camp is running.", 5),
    ("Pack Down", "Packing away, cleaning and checking the site.", 6),
    ("After Camp", "Returns, follow-up, reviews and payments.", 7),
]


CATEGORIES = [
    ("Venue", "Site, booking, access and venue-related arrangements.", 1),
    ("People & Forms", "Permissions, medical details, dietary information and attendance.", 2),
    ("Programme", "Activities, rotations, activity leads and programme preparation.", 3),
    ("Equipment", "Group kit, activity kit, storage, loading and returns.", 4),
    ("Food", "Menus, shopping, cooking and dietary handling.", 5),
    ("Transport", "Vehicles, drivers, passengers, trailers and loading plans.", 6),
    ("Documents", "Leader packs, parent information, lists and printed outputs.", 7),
    ("Safety / Risk", "Risk assessments, first aid, emergency arrangements and safety checks.", 8),
    ("Communications", "Messages to parents, leaders, helpers and other contacts.", 9),
    ("Finance", "Payments, costs, receipts and reimbursements.", 10),
    ("General", "Useful fallback for tasks that do not clearly belong elsewhere.", 11),
]


PEOPLE = [
    ("Alice", "Morgan", "Leader", "alice@example.com", "07123 000001"),
    ("Ben", "Taylor", "Leader", "ben@example.com", "07123 000002"),
    ("Cara", "Jenkins", "Helper", "cara@example.com", "07123 000003"),
    ("Dylan", "Reed", "Helper", "dylan@example.com", "07123 000004"),
    ("Emma", "Shaw", "Leader", "emma@example.com", "07123 000005"),
    ("Felix", "Brown", "Young Leader", "felix@example.com", "07123 000006"),
    ("Jack", "Green", "Young Person", "", ""),
    ("Maya", "Patel", "Young Person", "", ""),
    ("Noah", "Evans", "Young Person", "", ""),
    ("Sofia", "Clark", "Young Person", "", ""),
    ("Leo", "Walker", "Young Person", "", ""),
    ("Amelia", "Hall", "Young Person", "", ""),
    ("Oscar", "Wright", "Young Person", "", ""),
    ("Grace", "King", "Young Person", "", ""),
    ("Harry", "Scott", "Young Person", "", ""),
    ("Lily", "Adams", "Young Person", "", ""),
]


TEAMS = [
    ("Camp Leadership Team", "Leader Team", "Overall camp leadership and decision making."),
    ("Programme Team", "Activity Group", "Plans and runs the activity programme."),
    ("Catering Team", "Duty Team", "Food, cooking, hygiene and kitchen jobs."),
    ("Quartermaster Team", "Helper Team", "Equipment, stores, loading and repairs."),
    ("Transport Team", "Transport Group", "Vehicles, drivers, passengers and kit movement."),
    ("Fox Patrol", "Patrol/Six", "Young person patrol group."),
    ("Otter Patrol", "Patrol/Six", "Young person patrol group."),
    ("Falcon Patrol", "Patrol/Six", "Young person patrol group."),
]


TASKS = [
    # title, phase, category, priority, status, due, description, notes, assignee kind, assignee name
    ("Confirm campsite booking and arrival window", "Early Planning", "Venue", "High", "Done", date(2026, 7, 1), "Confirm booking, arrival time, access arrangements and site contact details.", "", "person", "Alice Morgan"),
    ("Check Nights Away permit holder details", "Early Planning", "Safety / Risk", "Urgent", "In Progress", date(2026, 7, 5), "Confirm the named permit holder and camp leadership arrangements.", "Sample data only — replace with real approval details.", "person", "Alice Morgan"),
    ("Draft parent information email", "Early Planning", "Communications", "Normal", "Done", date(2026, 7, 8), "Prepare parent email with dates, venue, kit list, timings and contact arrangements.", "", "person", "Ben Taylor"),
    ("Collect consent, medical and dietary information", "Preparation", "People & Forms", "Urgent", "In Progress", date(2026, 7, 20), "Check forms and chase missing information before camp.", "Make dietary summary for catering team.", "team", "Camp Leadership Team"),
    ("Prepare camp risk assessment pack", "Preparation", "Safety / Risk", "Urgent", "In Progress", date(2026, 7, 22), "Prepare activity, site, fire, cooking and general camp risk assessments.", "Must be reviewed by the real leadership team.", "person", "Emma Shaw"),
    ("Create emergency contact sheet", "Preparation", "Documents", "High", "To Do", date(2026, 7, 25), "Create a printable emergency contact sheet for leaders.", "", "person", "Cara Jenkins"),
    ("Create patrol duty rota", "Preparation", "Programme", "Normal", "To Do", date(2026, 7, 26), "Allocate washing up, water collection, tidying and flag duties.", "", "team", "Programme Team"),
    ("Build wide game clue packs", "Preparation", "Programme", "Normal", "To Do", date(2026, 7, 28), "Prepare laminated clue cards, map extracts and patrol envelopes.", "", "team", "Programme Team"),
    ("Check group tents and spare pegs", "Preparation", "Equipment", "High", "To Do", date(2026, 7, 28), "Check tents, poles, pegs, mallets and repair kit.", "Include one spare patrol tent.", "team", "Quartermaster Team"),
    ("Create food menu and shopping list", "Preparation", "Food", "High", "In Progress", date(2026, 7, 29), "Prepare menu for Friday evening to Sunday lunch.", "Include vegetarian and allergy-safe options.", "team", "Catering Team"),
    ("Confirm drivers and vehicle loading plan", "Preparation", "Transport", "High", "To Do", date(2026, 7, 30), "Confirm drivers, passenger groups and equipment transport.", "", "team", "Transport Team"),
    ("Prepare leader briefing notes", "Final Week", "Documents", "High", "To Do", date(2026, 8, 2), "Prepare a one-page leader briefing covering programme, roles and emergency arrangements.", "", "person", "Alice Morgan"),
    ("Print patrol lists and tent groups", "Final Week", "Documents", "Normal", "To Do", date(2026, 8, 3), "Print patrol lists, tent groups and duty rota.", "", "person", "Ben Taylor"),
    ("Final weather check and programme adjustment", "Final Week", "Safety / Risk", "High", "To Do", date(2026, 8, 5), "Check forecast and adjust activities if needed.", "Prepare wet weather alternatives.", "person", "Emma Shaw"),
    ("Pack first aid kit and medication storage box", "Final Week", "Safety / Risk", "Urgent", "To Do", date(2026, 8, 5), "Check first aid kit, accident book and medication storage arrangements.", "", "person", "Cara Jenkins"),
    ("Load trailer with tents and cooking kit", "Final Week", "Equipment", "High", "To Do", date(2026, 8, 6), "Load tents, tables, stoves, water carriers, cool boxes and activity equipment.", "", "team", "Quartermaster Team"),
    ("Buy fresh food", "Final Week", "Food", "High", "To Do", date(2026, 8, 6), "Buy fresh food and pack cool boxes.", "", "team", "Catering Team"),
    ("Set up leader tent and first aid point", "Camp Setup", "Venue", "High", "To Do", date(2026, 8, 7), "Set up leader area, first aid point and information board.", "", "team", "Camp Leadership Team"),
    ("Pitch patrol tents", "Camp Setup", "Equipment", "High", "To Do", date(2026, 8, 7), "Support patrols to pitch tents safely and check guy lines.", "", "team", "Quartermaster Team"),
    ("Run arrival register and pocket money check", "Camp Setup", "People & Forms", "Normal", "To Do", date(2026, 8, 7), "Register arrivals, check contact details and note any updates.", "", "person", "Dylan Reed"),
    ("Friday evening campfire", "During Camp", "Programme", "Normal", "To Do", date(2026, 8, 7), "Run opening campfire, songs and patrol challenge briefing.", "", "team", "Programme Team"),
    ("Saturday breakfast duty", "During Camp", "Food", "Normal", "To Do", date(2026, 8, 8), "Prepare breakfast and supervise washing up.", "", "team", "Catering Team"),
    ("Saturday morning pioneering bases", "During Camp", "Programme", "High", "To Do", date(2026, 8, 8), "Run three rotating pioneering bases with simple lashings and teamwork challenges.", "Sample low-risk placeholder; check real rules and supervision.", "team", "Programme Team"),
    ("Saturday afternoon woodland navigation", "During Camp", "Programme", "High", "To Do", date(2026, 8, 8), "Run patrol navigation challenge within agreed site boundaries.", "Boundary briefing required.", "person", "Felix Brown"),
    ("Saturday evening wide game", "During Camp", "Programme", "High", "Blocked", date(2026, 8, 8), "Run a wide game using clue packs and patrol teams.", "Blocked until route and boundaries are confirmed.", "team", "Programme Team"),
    ("Daily fire and stove safety check", "During Camp", "Safety / Risk", "Urgent", "To Do", date(2026, 8, 8), "Check cooking area, water buckets, stove placement and fuel storage.", "", "person", "Emma Shaw"),
    ("Sunday Scouts Own / reflection", "During Camp", "Programme", "Normal", "To Do", date(2026, 8, 9), "Short reflection session before packing down.", "", "person", "Ben Taylor"),
    ("Pack down patrol tents", "Pack Down", "Equipment", "High", "To Do", date(2026, 8, 9), "Dry, check and pack tents where possible.", "", "team", "Quartermaster Team"),
    ("Final site sweep", "Pack Down", "Venue", "High", "To Do", date(2026, 8, 9), "Check campsite for litter, lost property and damage before departure.", "", "team", "Camp Leadership Team"),
    ("Return borrowed equipment", "After Camp", "Equipment", "Normal", "To Do", date(2026, 8, 12), "Return borrowed kit and record any missing or damaged items.", "", "team", "Quartermaster Team"),
    ("Send thank-you and lost property message", "After Camp", "Communications", "Normal", "To Do", date(2026, 8, 12), "Message parents with thanks, lost property and any follow-up notes.", "", "person", "Ben Taylor"),
    ("Reconcile camp expenses", "After Camp", "Finance", "Normal", "To Do", date(2026, 8, 15), "Collect receipts and prepare simple cost summary.", "", "person", "Dylan Reed"),
    ("Hold leader review", "After Camp", "General", "Normal", "To Do", date(2026, 8, 20), "Review what worked, what should change, and template improvements.", "", "", ""),
    ("Confirm archery provider paperwork", "Preparation", "Safety / Risk", "High", "To Do", date(2026, 7, 31), "Placeholder task for checking external provider paperwork if this activity is used.", "Deliberately unassigned to test unassigned sheets.", "", ""),
]


def ensure_schema():
    Base.metadata.create_all(bind=engine)

    with engine.begin() as connection:
        for table_name in ["task_phase", "task_category"]:
            columns = [
                row[1]
                for row in connection.execute(text(f"PRAGMA table_info({table_name})"))
            ]

            if columns and "description" not in columns:
                connection.execute(
                    text(f"ALTER TABLE {table_name} ADD COLUMN description TEXT")
                )


def delete_existing_sample(db):
    existing = db.query(Camp).filter(Camp.name == SAMPLE_CAMP_NAME).first()

    if existing is None:
        return

    camp_id = existing.id

    db.query(TaskAssignment).filter(TaskAssignment.camp_id == camp_id).delete()
    db.query(Task).filter(Task.camp_id == camp_id).delete()
    db.query(TeamMembership).filter(TeamMembership.camp_id == camp_id).delete()
    db.query(Team).filter(Team.camp_id == camp_id).delete()
    db.query(Person).filter(Person.camp_id == camp_id).delete()
    db.query(TaskPhase).filter(TaskPhase.camp_id == camp_id).delete()
    db.query(TaskCategory).filter(TaskCategory.camp_id == camp_id).delete()
    db.query(Camp).filter(Camp.id == camp_id).delete()

    db.commit()


def main():
    ensure_schema()

    with SessionLocal() as db:
        delete_existing_sample(db)

        camp = Camp(
            name=SAMPLE_CAMP_NAME,
            camp_type="Campsite Camp",
            start_date=date(2026, 8, 7),
            end_date=date(2026, 8, 9),
            venue_name="Willowbrook Scout Campsite",
            camp_leader="Alice Morgan",
            permit_holder="Alice Morgan",
            status="Planning",
            notes=(
                "Sample data for testing Camp Command Centre. "
                "This is POR-aware placeholder content only and is not a real approval pack."
            ),
        )

        db.add(camp)
        db.commit()
        db.refresh(camp)

        for name, description, sort_order in PHASES:
            db.add(
                TaskPhase(
                    camp_id=camp.id,
                    name=name,
                    description=description,
                    sort_order=sort_order,
                    is_active=True,
                )
            )

        for name, description, sort_order in CATEGORIES:
            db.add(
                TaskCategory(
                    camp_id=camp.id,
                    name=name,
                    description=description,
                    sort_order=sort_order,
                    is_active=True,
                )
            )

        db.commit()

        people_by_name = {}

        for first_name, last_name, person_type, email, phone in PEOPLE:
            person = Person(
                camp_id=camp.id,
                first_name=first_name,
                last_name=last_name,
                person_type=person_type,
                email=email or None,
                phone=phone or None,
                role_notes=None,
            )
            db.add(person)
            db.flush()
            people_by_name[f"{first_name} {last_name}"] = person

        teams_by_name = {}

        for name, team_type, description in TEAMS:
            team = Team(
                camp_id=camp.id,
                name=name,
                team_type=team_type,
                description=description,
            )
            db.add(team)
            db.flush()
            teams_by_name[name] = team

        memberships = {
            "Camp Leadership Team": ["Alice Morgan", "Ben Taylor", "Emma Shaw"],
            "Programme Team": ["Ben Taylor", "Emma Shaw", "Felix Brown"],
            "Catering Team": ["Cara Jenkins", "Dylan Reed"],
            "Quartermaster Team": ["Dylan Reed", "Felix Brown"],
            "Transport Team": ["Alice Morgan", "Dylan Reed"],
            "Fox Patrol": ["Jack Green", "Maya Patel", "Noah Evans"],
            "Otter Patrol": ["Sofia Clark", "Leo Walker", "Amelia Hall"],
            "Falcon Patrol": ["Oscar Wright", "Grace King", "Harry Scott", "Lily Adams"],
        }

        for team_name, member_names in memberships.items():
            for member_name in member_names:
                db.add(
                    TeamMembership(
                        camp_id=camp.id,
                        team_id=teams_by_name[team_name].id,
                        person_id=people_by_name[member_name].id,
                        role_in_team=None,
                        notes=None,
                    )
                )

        db.commit()

        for (
            title,
            phase,
            category,
            priority,
            status,
            due_date,
            description,
            notes,
            assignee_kind,
            assignee_name,
        ) in TASKS:
            task = Task(
                camp_id=camp.id,
                title=title,
                description=description or None,
                category=category or None,
                phase=phase or None,
                priority=priority,
                status=status,
                due_date=due_date,
                notes=notes or None,
            )
            db.add(task)
            db.flush()

            if assignee_kind == "person":
                db.add(
                    TaskAssignment(
                        camp_id=camp.id,
                        task_id=task.id,
                        assigned_person_id=people_by_name[assignee_name].id,
                        assigned_team_id=None,
                        assignment_notes=None,
                    )
                )

            elif assignee_kind == "team":
                db.add(
                    TaskAssignment(
                        camp_id=camp.id,
                        task_id=task.id,
                        assigned_person_id=None,
                        assigned_team_id=teams_by_name[assignee_name].id,
                        assignment_notes=None,
                    )
                )

        db.commit()

        print(f"Created sample camp: {camp.name}")
        print(f"Camp ID: {camp.id}")
        print(f"Open: /camps/{camp.id}")


if __name__ == "__main__":
    main()
