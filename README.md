# Camp Command Centre

Camp Command Centre is a local-first, browser-based camp planning and operations tool for Scout camps, sleepovers and other Nights Away events.

It is designed to help Scout leaders answer five practical questions:

1. What are we doing?
2. Who is involved?
3. Who is responsible?
4. What have we forgotten?
5. Are we ready?

The app is currently being built as a Python/FastAPI MVP that can run locally or inside GitHub Codespaces.

---

## Current Project Status

Current phase:

**Phase 1 MVP — Core Camp Planning**

Current milestone:

**People, Sections and OSM Import Workflows**

The project has moved beyond the original clickable prototype. It now has working early-MVP functionality for:

- Camps
- People
- Sections
- Teams
- Tasks and assignments
- Activities
- Programme sessions
- Risk assessments
- Printable task, programme and risk outputs
- OSM member import
- OSM event attendance import groundwork

The current priority is not to start large new modules. The current priority is to make the People, Sections and OSM workflows safe, clear and reliable enough for real camp data.

---

## What Has Been Built

### Camp Setup

Implemented:

- Create camps
- View camps
- Edit camp details
- Navigate from a camp into the main planning areas

Still to improve:

- Better camp dashboard
- Camp setup wizard
- Camp duplication/templates later

---

### People

Implemented:

- Add people
- Edit people
- View person details
- Group people by section
- Provisional people
- Replace provisional person with real details
- Profile completeness checks
- Attendance status
- Information source tracking
- Contact, emergency, allergy, medication, medical and dietary fields

People can currently represent both:

- real known people
- provisional placeholders for early planning

This supports two camp setup workflows:

1. Create provisional people first, then replace them later.
2. Import people from OSM first, then update attendance from an OSM event export.

Still to improve:

- Safer section-level import buttons
- Attendance summaries and filters
- Better duplicate-name handling
- Bulk move people between sections
- Better import review before applying changes

---

### Sections

Implemented:

- Section model
- Default sections
- People grouped by section
- Home section assigned to each person

Default sections include:

- Squirrels
- Beavers
- Cubs
- Scouts
- Explorers
- Young Leaders
- Leaders / Adults
- Other

Still to improve:

- Put OSM import buttons inside each section block
- Pre-select target section during imports
- Make it harder to import a file into the wrong section

---

### OSM Member Import

Implemented:

- Person-level OSM member update
- Bulk OSM member import preview
- Bulk OSM member import apply
- Matching by name inside the selected section
- Updating existing people
- Replacing provisional people
- Creating new people from unmatched rows
- Importing useful camp fields from OSM:
  - names
  - phone/email
  - primary contact
  - emergency contact
  - allergies
  - medication
  - medical notes
  - dietary requirements

The importer also stores the OSM section unit / six / patrol / leader unit internally.

Still to improve:

- Move import button into each section
- Make the target section very obvious
- Show per-row action clearly before apply:
  - update existing
  - replace provisional
  - create new
  - skip
- Better result summary after import

---

### OSM Event Attendance Import

Implemented groundwork:

- Parser for OSM event attendance exports
- Attendance mapping:
  - Yes to Attending
  - No to Not attending
  - Invited to Invited
  - blank to No response

Still to improve:

- Full browser testing
- Section-level attendance import buttons
- Attendance summaries by section
- Attendance filters on the People page

---

### Teams

Implemented:

- Create teams
- Edit teams
- Add/remove team members
- View team details
- View team task summary
- Print team task sheets

Still to improve:

- Better bulk group creation
- Possible future link between OSM sixes/patrols and teams

---

### Tasks and Assignments

Implemented:

- Create tasks
- Edit tasks
- Assign tasks to people
- Assign tasks to teams
- Task statuses
- Task phases
- Task categories
- Task command centre
- Printable task sheets and work packs

Still to improve:

- Task templates
- Better readiness summaries
- Better dependency display

---

### Activities and Programme

Implemented:

- Activities
- Programme sessions
- Session types
- Activity leads
- Supporting adults/session staff
- Participant groups
- Rotation summary
- Programme warnings
- Printable programme views

Still to improve:

- Better rotation planner
- Easier programme editing
- Clash detection
- Better filtering by section/group

---

### Risk Assessments

Implemented:

- Camp-level risk assessment
- Activity-level risk assessment
- Risk controls
- Risk status/source tracking
- Printable risk assessment views
- Risk assessment pack

Important note:

The app helps organise risk assessment information. It does not replace official Scouts approval processes.

Still to improve:

- Risk assessment templates
- Better review workflow
- Link risk status into future readiness summaries

---

## Current Priority List

Next build priorities:

1. Safer section-level OSM member imports
2. Safer section-level OSM attendance imports
3. Attendance summaries and filters
4. Import review improvements
5. Bulk move people between sections

Do not start these yet:

- Food
- Transport
- Finance
- Forms
- Communications
- Full compliance module
- Incident/welfare logging
- Online multi-user mode

Those are deferred until the Phase 1 core workflow is more stable.

---

## Deferred Roadmap Note

A future export/import/archive system is planned for later.

This is not current work.

Future file types may include:

- .ccctemplate — reusable camp template
- .cccarchive — archived camp
- .cccbackup — full app backup

Design principles:

- No user-facing JSON exports
- App-managed encryption
- Sensitive archive fields off by default
- Future camp states:
  - Planning
  - Active
  - Completed
  - Archived

---

## Running in GitHub Codespaces

In the Codespaces terminal, run:

    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Open the forwarded port when Codespaces offers it.

---

## Running Locally

Create and activate a virtual environment.

On Windows:

    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    python -m uvicorn app.main:app --reload

On Mac/Linux:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python -m uvicorn app.main:app --reload

Then open:

    http://127.0.0.1:8000

---

## Development Philosophy

Camp Command Centre is not intended to be just a spreadsheet replacement or a generic database frontend.

It is intended to become a guided planning and operations tool that helps leaders prepare, run and close camps with less duplication, fewer missed jobs and clearer shared information.

Current rule:

**Finish and stabilise the Phase 1 MVP before expanding into large deferred modules.**
## Developer seed data

To rebuild the sample Dream Camp data during development, run:

    python scripts/reset_dream_camp.py

This recreates the sample camp, then adds participating groups, sections and section assignments for the sample people.

The generated data is fictional demo data only. Do not use real names, real contacts, OSM exports or previous chat examples in seed data.
