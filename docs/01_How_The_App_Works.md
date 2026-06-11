# How The App Works

Camp Command Centre is organised around a Camp.

A Camp is the main working object.

Everything else belongs to a Camp or supports planning that Camp.

---

## Current App Structure

The current early-MVP app includes:

```text
Camp
 ├── People
 ├── Sections
 ├── Participating Groups
 ├── Teams
 ├── Tasks
 ├── Activities
 ├── Programme
 ├── Presence Windows
 ├── Risk Assessments
 ├── Printable Outputs
 └── OSM Imports
```

Future modules will add more areas later, but these are the current working foundations.

---

## Camp

A Camp represents one camp, sleepover, residential event, Nights Away event or similar activity.

A Camp contains:

- basic camp details
- people
- sections
- participating groups
- teams
- tasks
- activities
- programme sessions
- risk assessments
- printable outputs

The app is camp-centred.

This means that when a user is working, they are usually working inside one selected camp.

---

## People

People are stored against a specific camp.

The People module supports:

- young people
- leaders
- helpers
- young leaders
- parents/guardians
- visitors

People can be added manually, created as provisional placeholders, or imported from OSM.

A person can have:

- home section
- section unit
- person type
- attendance status
- information source
- contact details
- emergency contact details
- medical/allergy/dietary notes
- task assignments
- team memberships
- presence windows

---

## Candidate Roster

The People list is not only a final attendee list.

It is a candidate roster for the camp.

A person may be:

- Provisional
- Invited
- Attending
- Not attending
- No response
- Unknown

This allows the organiser to start planning before the final attendee list is confirmed.

It also allows the organiser to import all members from OSM and then use an OSM event export to update who is actually attending.

---

## Sections and Participating Groups

Sections represent the Scout section or adult grouping.

Examples:

- Beavers
- Cubs
- Scouts
- Explorers
- Young Leaders
- Leaders / Adults

Participating Groups allow more structure where a camp includes multiple groups or imported OSM sections.

Presence can inherit from camp, participating group, section or person level.

---

## Teams

Teams are planning groups.

Examples:

- tent groups
- patrols/sixes
- duty teams
- activity groups
- leader teams
- transport groups

A person may belong to multiple teams.

Teams can be used for tasks and programme participant groups.

---

## Tasks

Tasks are camp preparation and operations actions.

Tasks can be assigned to people or teams.

Tasks support:

- status
- priority
- phase
- category
- notes
- due date
- assignments
- task sheets / work packs

---

## Activities

Activities are reusable things that can be placed into the programme.

Activities can have:

- description
- duration
- location
- activity lead
- equipment notes
- risk notes
- wet weather alternative
- risk assessment information

Activities can also be linked from backup plans.

---

## Programme Sessions

Programme sessions are scheduled blocks in the camp timetable.

A session has:

- date
- start and end time
- title
- type
- optional linked activity
- optional participant team/group
- location
- notes
- rotation information

Sessions also have operational data:

- session staff
- staff roles
- adult lead checks
- presence-aware warnings
- backup plans
- session cover summary
- roll-call printable

---

## Presence Windows

Presence windows describe when people, sections, participating groups or the whole camp are expected to be present.

The app uses this to answer practical questions:

- is this person expected at the start of this session?
- will this person be present for the full session?
- does this person leave before the session ends?
- should this person appear in the staff dropdown?

Presence is currently used most visibly in programme session staffing.

---

## Risk Assessments

The app includes early risk assessment models and screens.

Current risk assessment handling is useful but needs better coverage logic.

Future risk assessment work should support:

- specific activity RA
- covered by event RA
- covered by site RA
- covered by generic RA
- not required / low-risk
- details / justification

This matters because not every programme item needs its own standalone RA.

---

## Printable Outputs

The app has practical printable outputs for:

- tasks
- team work packs
- programme
- group schedules
- leader schedules
- activity leader schedules
- leader board
- session roll calls

Print outputs must be treated as field documents.

They should be clear, robust and not overly clever.
