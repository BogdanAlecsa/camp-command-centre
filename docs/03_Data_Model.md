# Database and Data Model

Camp is the root entity.

Most MVP data belongs to a specific camp.

The app is local-first and currently uses SQLite through SQLAlchemy.

---

## Current Status

The data model has moved beyond the original starter model.

The app now includes working models for:

- Camp
- Person
- Section
- Team
- Team Membership
- Task
- Task Assignment
- Task Phase
- Task Category
- Activity
- Programme Session
- Programme Session Staff
- Camp Risk Assessment
- Camp Risk Control
- Activity Risk Assessment
- Activity Risk Control

Some future models are still deferred.

---

## Core Data Principle

Camp Command Centre should be camp-centred.

A camp owns its planning data.

Examples:

- people
- sections
- teams
- tasks
- activities
- programme sessions
- risk assessments

This keeps each camp self-contained.

---

## People Are Camp-Specific

The app does not currently maintain a permanent global young person database.

People are stored against a specific camp.

This is deliberate for the MVP.

It supports the idea that each camp has its own candidate roster and final attendee list.

Future versions may add reusable people or contact import workflows, but this should be handled carefully because of privacy and data protection.

---

## Person

A Person represents someone connected to a camp.

Person types include:

- Young Person
- Parent/Guardian
- Leader
- Helper
- Young Leader
- Visitor

Current person fields include:

- first name
- last name
- person type
- home section
- section unit / six / patrol / leader unit
- provisional flag
- attendance status
- information source
- email
- phone
- role notes
- primary contact details
- emergency contact details
- allergies
- allergy action
- medication
- medical notes
- dietary requirements

---

## Candidate Roster

People in the app are not necessarily confirmed attendees.

A person may be:

- Provisional
- Invited
- Attending
- Not attending
- No response
- Unknown

This supports two planning approaches:

1. Plan early using provisional placeholders.
2. Import people from OSM and then update attendance later.

Operational outputs should eventually filter people by attendance status.

For example, an emergency contact list should normally include attending people only.

---

## Provisional People

A provisional person is a placeholder.

Example:

- Cubs YP01
- Cubs YP02
- Scouts YP01

Provisional people allow planning before names are known.

A provisional person can later be replaced with a real person while keeping existing links.

This is important because provisional people may already be used in:

- teams
- task assignments
- programme planning
- tent groups later

---

## Section

A Section represents a Scout section or similar grouping within a camp.

Default sections include:

- Squirrels
- Beavers
- Cubs
- Scouts
- Explorers
- Young Leaders
- Leaders / Adults
- Other

A person may have one home section.

Sections are used to group people on the People page and should become the normal entry point for section-specific OSM imports.

---

## Section Unit

The Person model includes a section unit field.

This is a neutral field used to store OSM group/unit information.

Examples:

- Cub Six
- Scout Patrol
- Leader unit
- Young Leader unit

Different sections use different names for their sub-groups, so the app should not assume everything is called a Six or a Patrol.

The section unit is stored as useful reference data.

It should not automatically create Teams yet.

A future workflow may allow the organiser to convert OSM section units into teams.

---

## Information Source

People can store where their information came from.

Useful source values include:

- Manual Entry
- Provisional
- OSM Member File
- OSM Event Export
- Camp Form later
- Leader Update later

This matters because imported information should not blindly overwrite manual corrections.

---

## Attendance Status

Attendance status is now separate from person type.

Suggested attendance statuses:

- Provisional
- Invited
- Attending
- Not attending
- No response
- Withdrawn
- Unknown

OSM event attendance imports should update attendance status without overwriting unrelated person data.

---

## Contact and Health Fields

The Person model currently includes camp-relevant contact and health fields.

These include:

- primary contact name
- primary contact relationship
- primary contact phone
- primary contact email
- emergency contact name
- emergency contact relationship
- emergency contact phone
- emergency contact email
- allergies
- allergy action
- medication
- medical notes
- dietary requirements

These fields are useful for camp planning and emergency preparation.

They are sensitive and should be handled carefully in future exports, archives and reports.

---

## Team

A Team is a camp organisation group.

Examples:

- Leader Team
- Helper Team
- Tent Group
- Patrol/Six
- Activity Group
- Duty Team
- Transport Group
- Custom

People can belong to multiple teams.

Teams are separate from Sections.

Sections describe where a person belongs organisationally.

Teams describe how people are grouped for a specific camp purpose.

---

## Team Membership

Team Membership links people to teams.

A person can be in more than one team.

For example, one person could be in:

- Cubs section
- Red tent group
- Saturday breakfast duty team
- Archery activity group

---

## Task

A Task represents something that needs doing for the camp.

Tasks include:

- title
- description
- category
- phase
- priority
- status
- due date
- notes

Tasks may be assigned to people or teams.

---

## Task Assignment

Task Assignment links tasks to people and/or teams.

This allows one task to be owned by:

- one person
- one team
- multiple people
- multiple teams

The task module currently supports printable task sheets and work packs.

---

## Task Phase

Task phases organise tasks by when they are needed.

Example phases:

- Early Planning
- Preparation
- Final Week
- Camp Setup
- During Camp
- Pack Down
- After Camp

Task phases are reusable within a camp.

---

## Task Category

Task categories organise tasks by area.

Example categories:

- Venue
- People & Forms
- Programme
- Equipment
- Food
- Transport
- Documents
- Safety / Risk
- Communications
- Finance
- General

Some categories refer to future modules, but they are useful now for organising tasks.

---

## Activity

An Activity represents something that can be scheduled in the programme.

Activities may include:

- name
- description
- default duration
- default location
- activity lead
- supporting adults notes
- equipment notes
- risk notes
- wet weather alternative
- badge notes

Activities can be linked to programme sessions.

---

## Programme Session

A Programme Session represents a scheduled block in the camp programme.

A session may include:

- date
- start time
- end time
- title
- session type
- linked activity
- participant team/group
- lead person
- location
- notes
- rotation information

Programme sessions are used to generate printable programme outputs.

---

## Programme Session Staff

Programme Session Staff links extra people to a programme session.

This allows a session to have:

- lead person
- supporting adults
- parent helpers
- young leaders
- first aider
- observer
- other roles

This is separate from the main session lead.

---

## Risk Assessment Models

Risk assessment data is included as a safety backbone inside the MVP.

Current models include:

- Camp Risk Assessment
- Camp Risk Control
- Activity Risk Assessment
- Activity Risk Control

Risk assessments have status and source information.

Risk controls describe what could go wrong, who is at risk, what controls are in place and what review action may be needed.

Important note:

The app helps organise risk assessment information.

It does not replace official Scouts approval processes.

---

## OSM Import Data

The app currently supports OSM import workflows.

OSM member import can update person profile fields.

OSM event attendance import can update attendance status.

OSM imports should be treated as a source of data, not as absolute truth.

Manual corrections should be protected unless the organiser explicitly chooses to overwrite existing non-blank fields.

---

## Future Forms Data

Forms are deferred.

Future form responses should become structured database records, not just uploaded PDFs.

Possible future form data:

- consent
- medical updates
- dietary updates
- travel permissions
- activity permissions
- emergency contact confirmation

Forms should update camp-specific records.

They should not automatically overwrite historical data without review.

---

## Future Export Records

Export records are deferred.

A future export record may track:

- export type
- camp
- date/time
- created by
- file type
- included data categories
- whether sensitive fields were included

This may become important for archive, backup and privacy reasons.

---

## Future Camp Lifecycle

Camp should eventually support lifecycle states:

- Planning
- Active
- Completed
- Archived

Archived camps should be removed from normal working views but restorable if needed.

This is not current MVP work.

---

## Key Decisions

- Camp is the root entity.
- People are currently camp-specific records.
- Contacts are currently stored on Person records for MVP simplicity.
- Sections are separate from Teams.
- Section unit is stored as reference data, not automatically converted into Teams.
- OSM imports should fill or update camp data only after preview.
- Manual corrections should not be overwritten by default.
- Sensitive data should be excluded from templates and off by default in future archives.
- Templates are copied, never live-linked.
- Forms are future structured data, not just documents.