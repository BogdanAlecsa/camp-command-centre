# Planning Workflow

The workflow guides users but does not lock them into a fixed wizard.

Users can return to earlier sections at any time.

If an earlier change affects later work, the app should mark affected areas as needing review.

---

## Current Workflow Position

The app currently supports a practical early-MVP camp planning workflow:

1. Create Camp
2. Add or import People
3. Organise People into Sections
4. Create Teams
5. Create Tasks
6. Assign Tasks
7. Create Activities
8. Build Programme
9. Assign Session Staff
10. Add Backup Plans
11. Add Risk Assessments
12. Generate Printable Outputs

The workflow is not yet a full readiness system, but the main building blocks now exist.

---

## 1. Create Camp

The organiser creates a camp, sleepover or Nights Away event.

Camp setup includes basic details such as:

- camp name
- dates
- camp type
- venue
- permit holder
- camp leader
- key notes

Future improvements may include a guided setup wizard, but the app should not force users through a rigid process.

---

## 2. Add People

People may be added in three ways:

1. Manually
2. As provisional placeholders
3. From OSM imports

This is important because camp planning often starts before the final list of attendees is known.

---

## 3. Candidate Roster

People in the app are not always final attendees.

The People module should be treated as a camp candidate roster.

A person may be:

- Provisional
- Invited
- Attending
- Not attending
- No response
- Unknown

This allows the organiser to import a whole section from OSM, then later update attendance using an OSM event export.

Operational outputs should increasingly filter to the correct people, usually Attending only.

---

## 4. Provisional Planning

The app supports provisional people.

Example:

- Cubs YP01
- Cubs YP02
- Cubs YP03

These placeholders allow planning to start before names are known.

Provisional people can be used for:

- task assignments
- teams
- tent groups
- programme groups
- planning numbers

Later, a provisional person can be replaced with a real person while preserving existing links.

---

## 5. OSM-Based Planning

The app supports a data-driven workflow using OSM exports.

This workflow is:

1. Import all members for a section from OSM.
2. Store them as the camp candidate roster.
3. Import the OSM event attendance export.
4. Update each person's attendance status.
5. Use attendance status to decide who appears in operational outputs.

This is useful when OSM already contains the section membership and event attendance data.

---

## 6. Create Teams

Teams are used for practical planning.

Examples:

- patrols/sixes
- tent groups
- duty teams
- leader teams
- activity groups
- transport groups

A person may belong to multiple teams.

Team membership can be edited without removing and re-adding the person.

---

## 7. Create and Assign Tasks

Tasks represent work needed before or during camp.

Tasks can be assigned to:

- people
- teams

Task status is updated automatically in key cases:

- assigning a task can move it to Assigned
- removing all assignments can return it to Unassigned/Planned where appropriate

Task outputs support:

- personal task sheets
- team work packs
- camp task summaries

---

## 8. Build Programme

Programme sessions are scheduled blocks.

A session may have:

- a linked activity
- a participant group/team
- a location
- staff
- backup plans
- notes
- rotation metadata

Programme planning should support both simple timetables and activity rotations.

---

## 9. Assign Session Staff

Session Staff is the operational staffing model for sessions.

A session can have multiple staff members.

Staff have roles such as:

- Lead
- Supporting Adult
- Parent Helper
- Young Leader
- First Aider
- Observer
- Other

This replaces the old single Lead Person concept.

The app should treat Session Staff role = Lead as the source of truth for session leads.

---

## 10. Check Session Cover

Session cover currently checks:

- total people at session start
- total people for full session
- participants at start
- participants for full session
- assigned staff at start
- assigned staff for full session
- staff roles at start
- staff roles for full session
- adult Lead at start
- adult Lead for full session

Young Leaders can be session staff operationally, but they are not adult Lead cover.

---

## 11. Add Backup Plans

Backup plans are optional fallbacks attached to a programme session.

They are useful for:

- wet weather
- heat
- low light
- equipment problems
- instructor unavailable
- overruns
- low energy
- behaviour reset

A backup plan can be linked to an existing Activity or entered as lightweight text.

Backup plans do not alter the main timetable.

---

## 12. Print Operational Outputs

Printables are used in the field.

The app should support:

- full programme
- leader programme
- group programme
- activity leader schedule
- leader board
- session roll call
- task sheets
- work packs

Print routes need particular care because small template mistakes can break important outputs.

---

## Workflow Principle

The app should allow early messy planning, then gradually tighten the data.

Planning often starts with unknowns.

The app should make unknowns visible rather than block planning completely.
