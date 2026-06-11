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
- Participating Group
- Presence Window
- Team
- Team Membership
- Task
- Task Assignment
- Task Phase
- Task Category
- Activity
- Programme Session
- Programme Session Staff
- Programme Session Backup
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
- session staff
- backup plans
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

## Section

A Section represents a Scout section or adult grouping.

Examples:

- Squirrels
- Beavers
- Cubs
- Scouts
- Explorers
- Young Leaders
- Leaders / Adults

Sections may be connected to participating groups.

People can inherit presence expectations through their home section.

---

## Participating Group

Participating Groups are useful when a camp includes multiple sections, scout groups or OSM sources.

They help organise imports and attendance expectations.

Presence can be set at participating group level.

---

## Presence Window

PresenceWindow records when a person, section, participating group or whole camp is expected.

Scope types include:

- camp
- participating_group
- section
- person

Presence is used by the Programme Planner to decide whether someone is available for a session.

The current logic uses the most specific available presence source.

Order of precedence:

1. Person
2. Section
3. Participating Group
4. Camp

---

## Team and Team Membership

A Team represents an organisational grouping.

A person can belong to multiple teams.

Team Membership links people to teams and stores:

- role in team
- notes

This is used for patrols, tent groups, duty teams, activity groups and leader/helper teams.

---

## Task and Task Assignment

A Task represents something that needs doing.

Task Assignment links tasks to:

- people
- teams

The assignment model supports task ownership and future reporting.

---

## Activity

An Activity is a reusable activity definition.

Activity data includes:

- name
- description
- duration
- default location
- activity lead
- equipment notes
- risk notes
- wet weather alternative

Activities can be scheduled as programme sessions.

Activities can also be linked from session backup plans.

---

## Programme Session

A Programme Session is a scheduled timetable item.

It includes:

- camp_id
- session_date
- start_time
- end_time
- title
- session_type
- activity_id
- participant_team_id
- lead_person_id
- location
- notes
- rotation_group
- rotation_slot_number

Important note:

`lead_person_id` is a legacy field and should not be used as the source of truth in new UI logic.

The source of truth for session leads is:

```text
ProgrammeSessionStaff.role == "Lead"
```

The legacy field is kept temporarily for database compatibility and migration safety.

---

## Programme Session Staff

Programme Session Staff links people to a programme session as operational staff.

Fields include:

- camp_id
- programme_session_id
- person_id
- role
- notes

Roles include:

- Lead
- Supporting Adult
- Parent Helper
- Young Leader
- First Aider
- Observer
- Other

This supports multiple leads and multiple support staff per session.

Young Leaders can be staff operationally, but they must not count as adults for mandatory ratios.

---

## Programme Session Backup

Programme Session Backup stores fallback plans attached to a session.

Fields include:

- camp_id
- programme_session_id
- optional activity_id
- title
- reason
- location
- duration_minutes
- notes
- sort_order

A backup can be:

- linked to an existing Activity
- entered as lightweight custom text

Backups do not change the main programme timetable.

---

## Risk Assessment Models

The app currently has:

- Camp Risk Assessment
- Camp Risk Control
- Activity Risk Assessment
- Activity Risk Control

Risk assessment work should evolve to support coverage modes.

Suggested future RA coverage model:

- specific RA attached
- covered by event RA
- covered by site RA
- covered by generic RA
- not required / low-risk
- details / justification

This avoids forcing a fake standalone RA for every minor item.

---

## Schema Evolution Note

The app currently uses SQLite and `Base.metadata.create_all()`.

Some schema evolution has been handled pragmatically.

Before wider use, the project should introduce a more deliberate migration strategy, probably Alembic or a lightweight internal migration layer.
