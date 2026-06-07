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
9. Add Risk Assessments
10. Generate Printable Outputs

The workflow is not yet a full readiness system, but the main building blocks now exist.

---

## Core Planning Flow

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

Operational outputs should later be able to filter to the correct people, usually Attending only.

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

The app also supports a more data-driven workflow using OSM exports.

This workflow is:

1. Import all members for a section from OSM
2. Store them as the camp candidate roster
3. Import the OSM event attendance export
4. Update each person's attendance status
5. Use attendance status to decide who appears in operational outputs

This is useful when OSM already contains the section membership and event attendance data.

---

## 6. Sections

People are grouped by home section.

Default sections include:

- Squirrels
- Beavers
- Cubs
- Scouts
- Explorers
- Young Leaders
- Leaders / Adults
- Other

The People page groups people by section.

Future import actions should sit inside each section block, so the target section is clear and accidental imports into the wrong section are less likely.

---

## 7. Teams and Groups

Teams are used for camp organisation.

A person can belong to multiple teams.

Examples:

- leader team
- helper team
- tent group
- patrol or six
- activity group
- duty team
- transport group

Section units from OSM, such as Cub Sixes or Scout Patrols, are currently stored as reference data.

They should not automatically create teams yet.

A future improvement may allow the organiser to convert OSM units into teams.

---

## 8. Tasks and Assignments

Tasks help organise preparation and delivery.

Tasks may be assigned to:

- individuals
- teams
- multiple people

Tasks can be grouped by:

- status
- phase
- category
- assignee

The app currently supports printable task sheets and work packs.

Future improvements should include reusable task templates and stronger readiness summaries.

---

## 9. Activities

Activities describe what may happen during the camp.

Activities may include:

- description
- duration
- location
- activity lead
- supporting adults
- equipment notes
- risk notes
- wet weather alternative
- badge notes

Activities can be linked into the programme.

Future improvements should include reusable activity templates.

---

## 10. Programme

Programme sessions schedule activities and other camp events.

Programme sessions may include:

- date
- time
- activity
- participant group
- location
- lead person
- supporting staff
- session type
- notes

Current programme outputs include:

- full programme
- group schedules
- leader schedules
- activity leader schedules
- leader board

Future improvements should include better rotation planning, clash detection and easier editing.

---

## 11. Risk Assessments

Risk assessments are included as a safety backbone inside the MVP.

The app supports:

- camp-level risk assessment
- activity-level risk assessment
- risk controls
- risk assessment status
- risk assessment print views
- risk assessment pack

Important note:

The app assists with organising risk assessment information.

It does not replace official Scouts approval processes.

---

## 12. Printable Outputs

The app already supports several printable outputs.

Examples:

- person task sheets
- team task sheets
- task work packs
- programme printouts
- risk assessment print pack

Future outputs should include a more joined-up camp file.

Possible future packs:

- parent pack
- leader pack
- emergency/contact list
- attending young people list
- programme pack
- risk assessment pack
- task pack

---

## 13. Readiness

Readiness is the long-term direction.

The app should eventually answer:

Are we ready?

Readiness should be based on real information from the app, not manually maintained checklists.

Potential readiness areas:

- people and attendance
- missing contact details
- missing emergency contacts
- missing medical/dietary information
- incomplete tasks
- programme gaps
- missing risk assessments
- staffing gaps
- missing documents
- unresolved warnings

Readiness scoring should not be built until the underlying data is reliable.

---

## Current Immediate Priorities

The next practical workflow improvements are:

1. Safer section-level OSM member imports
2. Safer section-level OSM attendance imports
3. Attendance summaries and filters
4. Import review improvements
5. Bulk move people between sections

These should be completed before starting larger deferred modules.

---

## Deferred Workflow Areas

Do not build these yet:

- Food
- Transport
- Finance
- Forms
- Communications
- Full compliance module
- Incident and welfare logging
- Online multi-user mode
- Export/import/archive implementation

These are future modules and should wait until the Phase 1 core workflow is stable.

---

## Close Camp and Archive

Future workflow stages should include:

1. Planning
2. Active
3. Completed
4. Archived

Completed camps should remain visible while close-down actions are finished.

Archived camps should be removed from normal working views but restorable if needed.

This belongs to a later phase.