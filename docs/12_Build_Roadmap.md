# Build Roadmap

This document records the practical build order for Camp Command Centre.

The roadmap should keep development focused and prevent the app from spreading too thin too early.

---

## Current Position

Camp Command Centre is now a working early Phase 1 MVP.

It has moved beyond the original clickable prototype.

Current working areas include:

- Camps
- People
- Sections
- Teams
- Tasks
- Activities
- Programme
- Risk assessments
- Printable outputs
- OSM member import
- OSM attendance import groundwork

The current focus is not adding large new modules.

The current focus is making the People, Sections and OSM import workflow safer and clearer.

---

## Current Phase

Current phase:

Phase 1 MVP — Core Camp Planning

Current active milestone:

People, Sections and OSM Import Workflows

The immediate goal is to make the app safe enough to use with real camp people and attendance data.

---

## Phase 1 MVP Scope

Phase 1 focuses on the core camp planning workflow.

Included:

- Camp setup
- People
- Sections
- Teams
- Tasks and assignments
- Activities
- Programme
- Risk assessments
- Basic printable outputs
- OSM people import
- OSM attendance import

Not included yet:

- Food
- Transport
- Finance
- Full forms workflow
- Communications
- Full compliance module
- Incident/welfare logging
- Online multi-user mode
- Export/import/archive implementation

---

## Milestone 5C — People, Sections and OSM

The current build area is Milestone 5C.

This milestone exists because reliable people and attendance data are the foundation for many later modules.

Food, transport, finance, forms, communications and readiness all depend on knowing who is involved and who is actually attending.

---

## Completed or Mostly Completed in 5C

Already introduced:

- Section model
- Default sections
- People grouped by section
- Home section on people
- Section unit / Six / Patrol / Leader unit storage
- Provisional people
- Replace provisional person workflow
- Attendance status
- Information source tracking
- Primary contact fields
- Emergency contact fields
- Allergy, medication, medical and dietary fields
- Profile completeness checks
- Person-level OSM member update
- Bulk OSM member import preview
- Bulk OSM member import apply
- OSM event attendance parser
- OSM attendance import groundwork
- Better file-selection feedback on upload screens

---

## Current Problem to Fix

The current OSM import workflow works, but it is still too easy to import into the wrong section.

The import buttons are too global.

The target section is selected using a dropdown.

This creates a real risk of importing a Cubs file into Squirrels, or a Scouts file into Cubs.

This must be fixed before heavy use with real data.

---

## Milestone 5C4 — Safer Section-Level OSM Imports

This is the next build milestone.

Goal:

Move OSM import actions into each section block.

Each section should have its own import buttons.

Example:

Cubs:

- Import/update Cubs from OSM member export
- Update Cubs attendance from OSM event export

Scouts:

- Import/update Scouts from OSM member export
- Update Scouts attendance from OSM event export

The target section should be obvious and fixed by the route.

Preferred routes:

- /camps/{camp_id}/sections/{section_id}/osm-member-import
- /camps/{camp_id}/sections/{section_id}/osm-attendance-update

The page should clearly say:

You are importing into: Cubs

Success criteria:

- OSM member import buttons appear inside each section block
- OSM attendance import buttons appear inside each section block
- The normal workflow no longer depends on manually selecting the target section from a dropdown
- The import page clearly shows which section is being updated

---

## Milestone 5C5 — Attendance Summaries and Filters

Goal:

Make the People page usable once full section rosters have been imported.

Add attendance summaries by section.

Example:

Cubs:

- Attending: 18
- Invited: 4
- Not attending: 6
- No response: 2
- Provisional: 0

Add People page filters:

- All
- Attending
- Invited
- Not attending
- No response
- Provisional
- Missing profile information

Success criteria:

- each section shows attendance counts
- user can filter people by attendance status
- user can quickly find missing information

---

## Milestone 5C6 — Import Review Improvements

Goal:

Make import preview clearer and safer.

Each imported row should show what will happen before Apply is pressed.

Possible row actions:

- Update existing person
- Replace provisional person
- Create new person
- Skip
- Needs manual review

Rules:

- Do not overwrite existing non-blank manual fields by default
- Allow overwrite only with explicit confirmation
- Flag duplicate-name matches
- Flag unmatched rows
- Show import result summary after apply

Success criteria:

- organiser can see exactly what Apply will do
- duplicate matches are not guessed
- import result summary is shown after apply

---

## Milestone 5C7 — Bulk Move People Between Sections

Goal:

Add a recovery tool for mistakes.

Needed workflow:

1. Select multiple people
2. Choose target section
3. Move selected people

This is useful if an import is applied to the wrong section or if section assignments need correcting.

Success criteria:

- multiple people can be selected
- selected people can be moved to another section
- move action is confirmed before applying

---

## Milestone 5C8 — Duplicate Name Handling

Goal:

Improve matching safety during imports.

If more than one person has the same normalised first and last name in the target section, the importer should not guess.

It should show:

Needs manual review

Future review screen should allow the organiser to choose the correct match.

Success criteria:

- duplicate names are detected
- import does not update ambiguous matches automatically
- user is warned clearly

---

## Milestone 5C9 — People Workflow Polish

Goal:

Make the People module feel clean and reliable.

Possible improvements:

- clearer section headers
- better attendance/status badges
- better missing-profile indicators
- better person detail layout
- clearer OSM source information
- better handling of provisional people
- better action placement

Success criteria:

- People page remains readable with several sections imported
- important warnings are visible but not overwhelming
- action buttons appear where users expect them

---

## Phase 1 Programme Improvements

Programme already has a useful early MVP.

Later improvements:

- better rotation planner workflow
- better clash detection
- better section/group filtering
- better leader/staff allocation view
- better print layouts
- easier programme editing

Do not prioritise this before safer OSM imports unless a bug blocks use.

---

## Phase 1 Task Improvements

Tasks are already one of the strongest modules.

Later improvements:

- reusable task templates
- better task dashboard summaries
- checklist items inside tasks
- dependency tracking
- better readiness roll-up
- better work pack formatting

Do not overcomplicate tasks too early.

---

## Phase 1 Risk Assessment Improvements

Risk assessment support exists as a safety backbone.

Later improvements:

- risk assessment templates
- clearer review workflow
- better print layout
- link risk status into readiness summaries
- duplicate/reuse risk assessments

Important note:

The app assists with organising risk assessment information.

It does not replace official Scouts approval processes.

---

## Phase 1 Camp Dashboard Improvements

The camp dashboard should eventually become the command centre.

Useful dashboard summaries:

- attendance by section
- missing profile information
- urgent tasks
- blocked tasks
- programme warnings
- risk assessment status
- next actions
- useful print buttons

Do not build a full readiness score yet.

Start with practical summaries and warnings.

---

## Phase 2 — Forms, Communications and Documents

Deferred until the Phase 1 core is stable.

Possible future work:

- parent/carer forms
- medical updates
- consent forms
- emergency contact confirmation
- joining instructions
- reminders
- leader messages
- helper messages
- document checklist
- parent pack
- leader pack
- camp file

Forms should become structured data, not just uploaded PDFs.

---

## Phase 3 — Food, Transport and Finance

Deferred.

Possible future work:

Food:

- meal planning
- dietary summaries
- shopping lists
- cooking rota

Transport:

- drivers
- vehicles
- passengers
- pickup arrangements
- equipment loads

Finance:

- budget
- payments
- expenses
- receipts
- treasurer report

These depend on reliable attendance data.

---

## Phase 4 — Compliance and Readiness

Deferred.

Possible future work:

- Nights Away Permit details
- NAN status
- DBS/training/first aid reminders
- required document tracking
- readiness warnings
- readiness dashboard

Important principle:

The app can assist compliance tracking.

It must not replace official Scouts approval processes.

---

## Phase 5 — Site, Lessons Learned and Advanced Reporting

Deferred.

Possible future work:

- site planning
- maps
- zones
- emergency points
- post-camp review
- lessons learned
- advanced reports
- improved printable packs

---

## Phase 5D — Export / Import / Archive System

Deferred.

Do not build now.

Future file types may include:

- .ccctemplate
- .cccarchive
- .cccbackup

Design principles:

- no user-facing JSON exports
- app-managed encryption
- sensitive archive fields off by default
- templates exclude personal data
- backups support disaster recovery

Future camp lifecycle states:

- Planning
- Active
- Completed
- Archived

---

## Phase 6 — Online Deployment and Collaboration

Deferred.

Possible future work:

- login
- users
- roles
- permissions
- camp-specific access
- online hosting
- PostgreSQL
- parent/carer form links
- helper task updates

Do not build online multi-user mode until the local-first MVP is stable.

---

## Current Build Order

Recommended next build order:

1. Move OSM member import buttons into section blocks
2. Move OSM attendance import buttons into section blocks
3. Add section-specific import routes
4. Show strong target-section warning on import pages
5. Improve import preview action labels
6. Add import result summaries
7. Add attendance summaries by section
8. Add People page attendance filters
9. Add bulk move between sections
10. Improve duplicate-name handling
11. Polish People page UX
12. Improve camp dashboard summaries
13. Improve programme warnings
14. Add task templates
15. Add readiness checks only after data is reliable

---

## Do Not Start Yet

Do not start these yet:

- Food module
- Transport module
- Finance module
- Full forms workflow
- Communications module
- Full compliance module
- Incident/welfare logging
- Online multi-user deployment
- Export/import/archive implementation

These are important, but not next.

---

## Summary

The app is currently in the middle of Phase 1 MVP.

The foundation is good.

The next work should make the existing People, Sections and OSM workflows safe, clear and reliable.

Do not spread into large new modules until the current workflow is trustworthy.