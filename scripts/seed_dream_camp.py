from datetime import date, time

# Demo data rule:
# Names, emails and phone numbers in this file must be fictional.
# Do not use names from real leaders, parents, school contacts, Scouts contacts,
# previous chats, or real OSM exports.

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
    Activity,
    ProgrammeSession,
    CampRiskAssessment,
    CampRiskControl,
    ActivityRiskAssessment,
    ActivityRiskControl,
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
    ("Rowan", "Vale", "Leader", "rowan.vale@example.test", "07123 000001"),
    ("Nico", "Hart", "Leader", "nico.hart@example.test", "07123 000002"),
    ("Mina", "Brook", "Helper", "mina.brook@example.test", "07123 000003"),
    ("Toby", "Finch", "Helper", "toby.finch@example.test", "07123 000004"),
    ("Isla", "Park", "Leader", "isla.park@example.test", "07123 000005"),
    ("Owen", "Pike", "Young Leader", "owen.pike@example.test", "07123 000006"),
    ("Jasper", "Reed", "Young Person", "", ""),
    ("Maya", "Stone", "Young Person", "", ""),
    ("Noah", "Field", "Young Person", "", ""),
    ("Sofia", "Lane", "Young Person", "", ""),
    ("Leo", "Moss", "Young Person", "", ""),
    ("Amelia", "Quinn", "Young Person", "", ""),
    ("Oscar", "Hale", "Young Person", "", ""),
    ("Grace", "Rowan", "Young Person", "", ""),
    ("Harry", "Vale", "Young Person", "", ""),
    ("Lily", "Brook", "Young Person", "", ""),
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



ACTIVITIES = [
    (
        "Arrival, Register and Site Setup",
        "Welcome young people, complete arrival register, allocate patrol areas and support initial tent pitching.",
        90,
        "Main camping field",
        "Rowan Vale",
        "All available leaders support arrival, luggage movement and tent setup.",
        "Register, patrol lists, tent allocation sheet, mallets, spare pegs, first aid point sign.",
        "Keep vehicles and young people separated. Confirm boundaries before free movement around site.",
        "Use activity shelter for registration and delay tent pitching until weather improves.",
        "Supports Outdoor Challenge and teamwork/logistics discussions.",
    ),
    (
        "Opening Campfire",
        "Opening campfire with songs, patrol introductions and weekend briefing.",
        60,
        "Campfire circle",
        "Nico Hart",
        "One adult supervises seating area while another manages fire area.",
        "Fire bucket, water, song cards, torch, camp blanket, fire lighting kit.",
        "Fire area controlled by adults. Clear safety boundary. Water available.",
        "Indoor/group shelter campfire-style songs and skits without real fire.",
        "Supports creative participation, confidence and community elements.",
    ),
    (
        "Pioneering Skills Bases",
        "Rotating bases covering knots, lashings and a small team construction challenge.",
        120,
        "Activity field",
        "Isla Park",
        "Three adult-supported bases plus Young Leader support for demonstrations.",
        "Ropes, spars, gloves, example knots, base instruction cards.",
        "Check lifting, splinters, trip hazards and safe dismantling. Keep structures low for this sample activity.",
        "Knot relay and table-top mini-pioneering challenge under shelter.",
        "Supports Outdoor Challenge, Skills Challenge and pioneering-related badge work.",
    ),
    (
        "Woodland Navigation Trail",
        "Patrol navigation challenge using simple map symbols, bearings and checkpoint cards.",
        90,
        "Woodland trail",
        "Owen Pike",
        "Adults positioned at agreed checkpoints and boundaries.",
        "Maps, checkpoint cards, pencils, clipboards, radios or phones for adults.",
        "Boundary briefing required. Adults know route and sweep procedure. Weather and daylight checked.",
        "Map-symbol treasure hunt inside the activity shelter.",
        "Supports Navigator staged activity badge and Outdoor Challenge elements.",
    ),
    (
        "Wide Game: Lost Expedition",
        "Evening patrol wide game using clues, teamwork and controlled site boundaries.",
        75,
        "Main field and marked woodland edge",
        "Nico Hart",
        "Adults supervise boundaries and clue stations.",
        "Clue envelopes, high-vis markers, torches, whistle, boundary map.",
        "Only run inside agreed area. Clear stop signal. Extra care in poor light.",
        "Indoor mystery challenge with clue stations around the hall/shelter.",
        "Supports Teamwork Challenge and problem-solving elements.",
    ),
    (
        "Backwoods Cooking Taster",
        "Simple outdoor cooking activity using safe preparation and supervised cooking area.",
        90,
        "Cooking area",
        "Mina Brook",
        "Catering team supports hygiene and setup.",
        "Handwash station, food ingredients, utensils, chopping boards, foil, stove/fire setup as appropriate.",
        "Food hygiene, allergies, burns and sharp tools need explicit supervision.",
        "Shelter-based cooking using stoves if site rules and supervision allow.",
        "Supports Outdoor Challenge and cooking/skills-related badge work.",
    ),
    (
        "Scouts Own / Reflection",
        "Short reflective session about teamwork, kindness, challenge and what was learned at camp.",
        30,
        "Quiet area near flagpole",
        "Rowan Vale",
        "One adult leads, others support group discussion.",
        "Prompt cards or short reading, camp blanket if used.",
        "Choose a quiet safe area away from vehicle movement and cooking areas.",
        "Run inside the activity shelter.",
        "Supports reflection, values and teamwork discussions.",
    ),
    (
        "Pack Down and Site Sweep Challenge",
        "Patrol-led pack down, lost property check and final site sweep.",
        90,
        "Whole site",
        "Toby Finch",
        "Adults check tents, stores and site areas before departure.",
        "Bin bags, lost property box, tent bags, equipment checklist.",
        "Manual handling, pegs, wet canvas and vehicle movement need supervision.",
        "Use shelter to sort kit and delay packing wet tents if needed.",
        "Supports responsibility, teamwork and camp skills.",
    ),
]


TASKS = [
    # title, phase, category, priority, status, due, description, notes, assignee kind, assignee name
    ("Confirm campsite booking and arrival window", "Early Planning", "Venue", "High", "Done", date(2026, 7, 1), "Confirm booking, arrival time, access arrangements and site contact details.", "", "person", "Rowan Vale"),
    ("Check Nights Away permit holder details", "Early Planning", "Safety / Risk", "Urgent", "In Progress", date(2026, 7, 5), "Confirm the named permit holder and camp leadership arrangements.", "Sample data only — replace with real approval details.", "person", "Rowan Vale"),
    ("Draft parent information email", "Early Planning", "Communications", "Normal", "Done", date(2026, 7, 8), "Prepare parent email with dates, venue, kit list, timings and contact arrangements.", "", "person", "Nico Hart"),
    ("Collect consent, medical and dietary information", "Preparation", "People & Forms", "Urgent", "In Progress", date(2026, 7, 20), "Check forms and chase missing information before camp.", "Make dietary summary for catering team.", "team", "Camp Leadership Team"),
    ("Prepare camp risk assessment pack", "Preparation", "Safety / Risk", "Urgent", "In Progress", date(2026, 7, 22), "Prepare activity, site, fire, cooking and general camp risk assessments.", "Must be reviewed by the real leadership team.", "person", "Isla Park"),
    ("Create emergency contact sheet", "Preparation", "Documents", "High", "To Do", date(2026, 7, 25), "Create a printable emergency contact sheet for leaders.", "", "person", "Mina Brook"),
    ("Create patrol duty rota", "Preparation", "Programme", "Normal", "To Do", date(2026, 7, 26), "Allocate washing up, water collection, tidying and flag duties.", "", "team", "Programme Team"),
    ("Build wide game clue packs", "Preparation", "Programme", "Normal", "To Do", date(2026, 7, 28), "Prepare laminated clue cards, map extracts and patrol envelopes.", "", "team", "Programme Team"),
    ("Check group tents and spare pegs", "Preparation", "Equipment", "High", "To Do", date(2026, 7, 28), "Check tents, poles, pegs, mallets and repair kit.", "Include one spare patrol tent.", "team", "Quartermaster Team"),
    ("Create food menu and shopping list", "Preparation", "Food", "High", "In Progress", date(2026, 7, 29), "Prepare menu for Friday evening to Sunday lunch.", "Include vegetarian and allergy-safe options.", "team", "Catering Team"),
    ("Confirm drivers and vehicle loading plan", "Preparation", "Transport", "High", "To Do", date(2026, 7, 30), "Confirm drivers, passenger groups and equipment transport.", "", "team", "Transport Team"),
    ("Prepare leader briefing notes", "Final Week", "Documents", "High", "To Do", date(2026, 8, 2), "Prepare a one-page leader briefing covering programme, roles and emergency arrangements.", "", "person", "Rowan Vale"),
    ("Print patrol lists and tent groups", "Final Week", "Documents", "Normal", "To Do", date(2026, 8, 3), "Print patrol lists, tent groups and duty rota.", "", "person", "Nico Hart"),
    ("Final weather check and programme adjustment", "Final Week", "Safety / Risk", "High", "To Do", date(2026, 8, 5), "Check forecast and adjust activities if needed.", "Prepare wet weather alternatives.", "person", "Isla Park"),
    ("Pack first aid kit and medication storage box", "Final Week", "Safety / Risk", "Urgent", "To Do", date(2026, 8, 5), "Check first aid kit, accident book and medication storage arrangements.", "", "person", "Mina Brook"),
    ("Load trailer with tents and cooking kit", "Final Week", "Equipment", "High", "To Do", date(2026, 8, 6), "Load tents, tables, stoves, water carriers, cool boxes and activity equipment.", "", "team", "Quartermaster Team"),
    ("Buy fresh food", "Final Week", "Food", "High", "To Do", date(2026, 8, 6), "Buy fresh food and pack cool boxes.", "", "team", "Catering Team"),
    ("Set up leader tent and first aid point", "Camp Setup", "Venue", "High", "To Do", date(2026, 8, 7), "Set up leader area, first aid point and information board.", "", "team", "Camp Leadership Team"),
    ("Pitch patrol tents", "Camp Setup", "Equipment", "High", "To Do", date(2026, 8, 7), "Support patrols to pitch tents safely and check guy lines.", "", "team", "Quartermaster Team"),
    ("Run arrival register and pocket money check", "Camp Setup", "People & Forms", "Normal", "To Do", date(2026, 8, 7), "Register arrivals, check contact details and note any updates.", "", "person", "Toby Finch"),
    ("Friday evening campfire", "During Camp", "Programme", "Normal", "To Do", date(2026, 8, 7), "Run opening campfire, songs and patrol challenge briefing.", "", "team", "Programme Team"),
    ("Saturday breakfast duty", "During Camp", "Food", "Normal", "To Do", date(2026, 8, 8), "Prepare breakfast and supervise washing up.", "", "team", "Catering Team"),
    ("Saturday morning pioneering bases", "During Camp", "Programme", "High", "To Do", date(2026, 8, 8), "Run three rotating pioneering bases with simple lashings and teamwork challenges.", "Sample low-risk placeholder; check real rules and supervision.", "team", "Programme Team"),
    ("Saturday afternoon woodland navigation", "During Camp", "Programme", "High", "To Do", date(2026, 8, 8), "Run patrol navigation challenge within agreed site boundaries.", "Boundary briefing required.", "person", "Owen Pike"),
    ("Saturday evening wide game", "During Camp", "Programme", "High", "Blocked", date(2026, 8, 8), "Run a wide game using clue packs and patrol teams.", "Blocked until route and boundaries are confirmed.", "team", "Programme Team"),
    ("Daily fire and stove safety check", "During Camp", "Safety / Risk", "Urgent", "To Do", date(2026, 8, 8), "Check cooking area, water buckets, stove placement and fuel storage.", "", "person", "Isla Park"),
    ("Sunday Scouts Own / reflection", "During Camp", "Programme", "Normal", "To Do", date(2026, 8, 9), "Short reflection session before packing down.", "", "person", "Nico Hart"),
    ("Pack down patrol tents", "Pack Down", "Equipment", "High", "To Do", date(2026, 8, 9), "Dry, check and pack tents where possible.", "", "team", "Quartermaster Team"),
    ("Final site sweep", "Pack Down", "Venue", "High", "To Do", date(2026, 8, 9), "Check campsite for litter, lost property and damage before departure.", "", "team", "Camp Leadership Team"),
    ("Return borrowed equipment", "After Camp", "Equipment", "Normal", "To Do", date(2026, 8, 12), "Return borrowed kit and record any missing or damaged items.", "", "team", "Quartermaster Team"),
    ("Send thank-you and lost property message", "After Camp", "Communications", "Normal", "To Do", date(2026, 8, 12), "Message parents with thanks, lost property and any follow-up notes.", "", "person", "Nico Hart"),
    ("Reconcile camp expenses", "After Camp", "Finance", "Normal", "To Do", date(2026, 8, 15), "Collect receipts and prepare simple cost summary.", "", "person", "Toby Finch"),
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

        optional_columns = [
            ("activity", "badge_notes", "TEXT"),
        ]

        for table_name, column_name, column_type in optional_columns:
            columns = [
                row[1]
                for row in connection.execute(text(f"PRAGMA table_info({table_name})"))
            ]

            if columns and column_name not in columns:
                connection.execute(
                    text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
                )


def delete_existing_sample(db):
    existing = db.query(Camp).filter(Camp.name == SAMPLE_CAMP_NAME).first()

    if existing is None:
        return

    camp_id = existing.id

    activity_risk_ids = [
        row.id
        for row in db.query(ActivityRiskAssessment)
        .filter(ActivityRiskAssessment.camp_id == camp_id)
        .all()
    ]

    if activity_risk_ids:
        db.query(ActivityRiskControl).filter(
            ActivityRiskControl.risk_assessment_id.in_(activity_risk_ids)
        ).delete(synchronize_session=False)

    camp_risk_ids = [
        row.id
        for row in db.query(CampRiskAssessment)
        .filter(CampRiskAssessment.camp_id == camp_id)
        .all()
    ]

    if camp_risk_ids:
        db.query(CampRiskControl).filter(
            CampRiskControl.risk_assessment_id.in_(camp_risk_ids)
        ).delete(synchronize_session=False)

    db.query(ActivityRiskAssessment).filter(ActivityRiskAssessment.camp_id == camp_id).delete()
    db.query(CampRiskAssessment).filter(CampRiskAssessment.camp_id == camp_id).delete()

    db.query(TaskAssignment).filter(TaskAssignment.camp_id == camp_id).delete()
    db.query(Task).filter(Task.camp_id == camp_id).delete()
    db.query(TeamMembership).filter(TeamMembership.camp_id == camp_id).delete()
    db.query(Team).filter(Team.camp_id == camp_id).delete()
    db.query(Person).filter(Person.camp_id == camp_id).delete()
    db.query(TaskPhase).filter(TaskPhase.camp_id == camp_id).delete()
    db.query(TaskCategory).filter(TaskCategory.camp_id == camp_id).delete()
    db.query(ProgrammeSession).filter(ProgrammeSession.camp_id == camp_id).delete()
    db.query(Activity).filter(Activity.camp_id == camp_id).delete()
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
            camp_leader="Rowan Vale",
            permit_holder="Rowan Vale",
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
            "Camp Leadership Team": ["Rowan Vale", "Nico Hart", "Isla Park"],
            "Programme Team": ["Nico Hart", "Isla Park", "Owen Pike"],
            "Catering Team": ["Mina Brook", "Toby Finch"],
            "Quartermaster Team": ["Toby Finch", "Owen Pike"],
            "Transport Team": ["Rowan Vale", "Toby Finch"],
            "Fox Patrol": ["Jasper Reed", "Maya Stone", "Noah Field"],
            "Otter Patrol": ["Sofia Lane", "Leo Moss", "Amelia Quinn"],
            "Falcon Patrol": ["Oscar Hale", "Grace Rowan", "Harry Vale", "Lily Brook"],
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


        activities_by_name = {}

        for (
            name,
            description,
            default_duration_minutes,
            default_location,
            lead_name,
            supporting_adults_notes,
            equipment_notes,
            risk_notes,
            wet_weather_alternative,
            badge_notes,
        ) in ACTIVITIES:
            lead = people_by_name.get(lead_name)

            activity = Activity(
                camp_id=camp.id,
                name=name,
                description=description,
                default_duration_minutes=default_duration_minutes,
                default_location=default_location,
                activity_lead_id=lead.id if lead else None,
                supporting_adults_notes=supporting_adults_notes,
                equipment_notes=equipment_notes,
                risk_notes=risk_notes,
                wet_weather_alternative=wet_weather_alternative,
                badge_notes=badge_notes,
            )

            db.add(activity)
            db.flush()
            activities_by_name[name] = activity

        db.commit()


        # Programme sessions demonstrate whole-camp blocks, manual blocks,
        # group-specific sessions and a simple rotation pattern.
        programme_sessions = [
            (date(2026, 8, 7), time(18, 0), time(19, 30), "Arrival, Register and Site Setup", "Setup / Pack Down", "Arrival, Register and Site Setup", None, "Main camping field", "Rowan Vale", "Whole-camp arrival and setup.", None, None),
            (date(2026, 8, 7), time(19, 45), time(20, 45), "Opening Campfire", "Whole Camp", "Opening Campfire", None, "Campfire circle", "Nico Hart", "Whole-camp opening activity.", None, None),
            (date(2026, 8, 7), time(21, 30), time(22, 0), "Lights Out", "Leader / Admin", None, None, "Tent areas", "Rowan Vale", "Quiet time and overnight routine.", None, None),

            (date(2026, 8, 8), time(8, 0), time(8, 45), "Breakfast", "Meal", None, None, "Kitchen shelter", "Mina Brook", "Whole-camp breakfast.", None, None),

            (date(2026, 8, 8), time(9, 15), time(10, 15), "Fox Patrol — Pioneering Skills Bases", "Group Rotation", "Pioneering Skills Bases", "Fox Patrol", "Activity field", "Isla Park", "Rotation slot 1.", "Saturday morning bases", 1),
            (date(2026, 8, 8), time(9, 15), time(10, 15), "Otter Patrol — Woodland Navigation Trail", "Group Rotation", "Woodland Navigation Trail", "Otter Patrol", "Woodland trail", "Owen Pike", "Rotation slot 1.", "Saturday morning bases", 1),
            (date(2026, 8, 8), time(9, 15), time(10, 15), "Falcon Patrol — Backwoods Cooking Taster", "Group Rotation", "Backwoods Cooking Taster", "Falcon Patrol", "Cooking area", "Mina Brook", "Rotation slot 1.", "Saturday morning bases", 1),

            (date(2026, 8, 8), time(10, 30), time(11, 30), "Fox Patrol — Woodland Navigation Trail", "Group Rotation", "Woodland Navigation Trail", "Fox Patrol", "Woodland trail", "Owen Pike", "Rotation slot 2.", "Saturday morning bases", 2),
            (date(2026, 8, 8), time(10, 30), time(11, 30), "Otter Patrol — Backwoods Cooking Taster", "Group Rotation", "Backwoods Cooking Taster", "Otter Patrol", "Cooking area", "Mina Brook", "Rotation slot 2.", "Saturday morning bases", 2),
            (date(2026, 8, 8), time(10, 30), time(11, 30), "Falcon Patrol — Pioneering Skills Bases", "Group Rotation", "Pioneering Skills Bases", "Falcon Patrol", "Activity field", "Isla Park", "Rotation slot 2.", "Saturday morning bases", 2),

            (date(2026, 8, 8), time(11, 45), time(12, 45), "Fox Patrol — Backwoods Cooking Taster", "Group Rotation", "Backwoods Cooking Taster", "Fox Patrol", "Cooking area", "Mina Brook", "Rotation slot 3.", "Saturday morning bases", 3),
            (date(2026, 8, 8), time(11, 45), time(12, 45), "Otter Patrol — Pioneering Skills Bases", "Group Rotation", "Pioneering Skills Bases", "Otter Patrol", "Activity field", "Isla Park", "Rotation slot 3.", "Saturday morning bases", 3),
            (date(2026, 8, 8), time(11, 45), time(12, 45), "Falcon Patrol — Woodland Navigation Trail", "Group Rotation", "Woodland Navigation Trail", "Falcon Patrol", "Woodland trail", "Owen Pike", "Rotation slot 3.", "Saturday morning bases", 3),

            (date(2026, 8, 8), time(13, 0), time(14, 0), "Lunch", "Meal", None, None, "Kitchen shelter", "Mina Brook", "Whole-camp lunch.", None, None),
            (date(2026, 8, 8), time(14, 30), time(16, 0), "Wide Game: Lost Expedition", "Whole Camp", "Wide Game: Lost Expedition", None, "Main field and woodland boundary", "Nico Hart", "Whole-camp afternoon activity.", None, None),
            (date(2026, 8, 8), time(19, 0), time(19, 45), "Reflection Circle", "Whole Camp", "Reflection Circle", None, "Campfire circle", "Rowan Vale", "Evening reflection.", None, None),

            (date(2026, 8, 9), time(8, 0), time(8, 45), "Breakfast", "Meal", None, None, "Kitchen shelter", "Mina Brook", "Whole-camp breakfast.", None, None),
            (date(2026, 8, 9), time(9, 30), time(11, 0), "Pack Down and Site Check", "Setup / Pack Down", "Pack Down and Site Check", None, "Whole site", "Rowan Vale", "Whole-camp pack down.", None, None),
        ]

        for (
            session_date,
            start_time,
            end_time,
            title,
            session_type,
            activity_name,
            team_name,
            location,
            lead_name,
            notes,
            rotation_group,
            rotation_slot_number,
        ) in programme_sessions:
            activity = activities_by_name.get(activity_name) if activity_name else None
            team = teams_by_name.get(team_name) if team_name else None
            lead = people_by_name.get(lead_name) if lead_name else None

            db.add(
                ProgrammeSession(
                    camp_id=camp.id,
                    session_date=session_date,
                    start_time=start_time,
                    end_time=end_time,
                    title=title,
                    session_type=session_type,
                    activity_id=activity.id if activity else None,
                    participant_team_id=team.id if team else None,
                    lead_person_id=lead.id if lead else None,
                    location=location,
                    notes=notes,
                    rotation_group=rotation_group,
                    rotation_slot_number=rotation_slot_number,
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


        camp_risk = CampRiskAssessment(
            camp_id=camp.id,
            title=f"{camp.name} Risk Assessment",
            status="Draft",
            prepared_by="Rowan Vale",
            review_date=date(2026, 8, 1),
            site_notes="Sample campsite risk notes covering boundaries, vehicle movement, camping areas and site rules.",
            overnight_notes="Sample overnight notes covering tent groups, leader availability, night-time arrangements and welfare checks.",
            supervision_notes="Sample supervision notes. Replace with real ratios, roles and local arrangements.",
            emergency_notes="Sample emergency notes covering first aid point, emergency contact list, site address and nearest access point.",
            communication_notes="Sample communication notes covering leader briefing, parent contact process and emergency escalation.",
        )
        db.add(camp_risk)
        db.flush()

        for order, hazard, who, controls, further, responsible in [
            (
                1,
                "Vehicle movement on arrival and departure",
                "Young people, adults and visitors could be struck or separated from the group.",
                "Arrival area supervised. Young people directed away from vehicle movement. Unloading controlled by adults.",
                "Confirm site-specific parking and unloading procedure before camp.",
                "Camp Leadership Team",
            ),
            (
                2,
                "Night-time movement around site",
                "Young people could trip, become disorientated or enter restricted areas.",
                "Boundaries explained. Torches required. Leaders available overnight. Clear toilet route agreed.",
                "Review lighting and route after arrival.",
                "Rowan Vale",
            ),
            (
                3,
                "Cooking and hot water",
                "Burns, scalds or food hygiene issues.",
                "Cooking area controlled. Handwashing available. Adults supervise stoves and hot water.",
                "Check dietary summary and site cooking rules before final menu.",
                "Catering Team",
            ),
        ]:
            db.add(
                CampRiskControl(
                    risk_assessment_id=camp_risk.id,
                    sort_order=order,
                    hazard=hazard,
                    who_might_be_harmed=who,
                    controls_in_place=controls,
                    further_controls_needed=further,
                    responsible_person=responsible,
                )
            )

        db.commit()

        activity_risk_seed = {
            "Opening Campfire": [
                ("Fire and hot embers", "Young people and adults could be burned.", "Fire area supervised by adults. Clear boundary. Water available.", "Check site fire rules and weather conditions.", "Nico Hart"),
                ("Smoke irritation", "Participants may be affected by smoke.", "Position seating with wind direction considered. Move participants if needed.", "Use no-fire alternative if conditions are poor.", "Nico Hart"),
            ],
            "Pioneering Skills Bases": [
                ("Falling spars or unstable structures", "Young people could be struck or trapped.", "Low-level sample structures only. Adult supervision at each base.", "Check all equipment before use.", "Isla Park"),
                ("Rope burns, splinters and trips", "Hands and feet could be injured.", "Gloves available. Clear work areas. Demonstrate safe handling.", "Replace damaged spars or ropes.", "Isla Park"),
            ],
            "Wide Game: Lost Expedition": [
                ("Running in low light", "Young people may trip or collide.", "Boundaries set. Stop signal explained. Adults supervise key points.", "Review terrain and daylight before running.", "Programme Team"),
                ("Young person leaves agreed area", "Young person could become separated from group.", "Clear boundaries, patrol grouping and adult sweep procedure.", "Add visible boundary markers.", "Programme Team"),
            ],
            "Backwoods Cooking Taster": [
                ("Burns from stoves or hot food", "Young people and adults could be burned.", "Cooking area supervised. Clear hot-zone. Adults control lighting and fuel.", "Confirm site cooking rules.", "Mina Brook"),
                ("Food allergy or hygiene issue", "Participants with allergies could be harmed.", "Dietary information checked. Handwashing station used. Ingredients controlled.", "Final check against real medical/dietary forms.", "Catering Team"),
            ],
        }

        for activity_name, rows in activity_risk_seed.items():
            activity = activities_by_name.get(activity_name)
            if not activity:
                continue

            risk = ActivityRiskAssessment(
                camp_id=camp.id,
                activity_id=activity.id,
                source_type="Created in app",
                status="Draft",
                leader_in_charge="Sample activity lead",
                prepared_by="Rowan Vale",
                review_date=date(2026, 8, 1),
                overall_notes="Sample activity risk assessment. Replace with real controls and review before use.",
            )
            db.add(risk)
            db.flush()

            for order, (hazard, who, controls, further, responsible) in enumerate(rows, start=1):
                db.add(
                    ActivityRiskControl(
                        risk_assessment_id=risk.id,
                        sort_order=order,
                        hazard=hazard,
                        who_might_be_harmed=who,
                        controls_in_place=controls,
                        further_controls_needed=further,
                        responsible_person=responsible,
                    )
                )

        # External provider example for testing third-party checks.
        provider_activity = activities_by_name.get("Woodland Navigation Trail")
        if provider_activity:
            risk = ActivityRiskAssessment(
                camp_id=camp.id,
                activity_id=provider_activity.id,
                source_type="External provider",
                status="Ready for Review",
                leader_in_charge="Owen Pike",
                prepared_by="Rowan Vale",
                review_date=date(2026, 8, 1),
                provider_name="Willowbrook Outdoor Learning Team",
                provider_contact="booking@example.test / ref NAV-2026-SAMPLE",
                provider_risk_assessment_received=True,
                provider_insurance_checked=True,
                provider_qualification_checked=True,
                provider_reference="Sample reference: provider RA and insurance saved in Group Drive. Replace with real evidence location.",
                scout_led_parts_notes="Group remains responsible for travel to/from the activity area, handover, headcounts and welfare before/after the provider-led session.",
                overall_notes="Sample external provider record.",
            )
            db.add(risk)

        db.commit()

        print(f"Created sample camp: {camp.name}")
        print(f"Camp ID: {camp.id}")
        print(f"Open: /camps/{camp.id}")


if __name__ == "__main__":
    main()
