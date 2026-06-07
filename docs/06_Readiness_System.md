# Readiness System

The Readiness System helps organisers answer:

Are we ready?

Readiness is the long-term direction of Camp Command Centre.

It should help leaders see what is complete, what is missing, what is risky and what still needs attention before camp.

---

## Current Status

A full Readiness System is not built yet.

The app now has many of the data foundations needed for readiness, including:

- camp details
- people
- sections
- attendance status
- profile completeness checks
- teams
- tasks
- task statuses
- activities
- programme sessions
- programme warnings
- risk assessments
- risk assessment statuses
- printable outputs

The current priority is to make the underlying data reliable before building readiness scoring.

Readiness should not be a manually maintained checklist if the app already has the data.

---

## Core Principle

Readiness should be calculated from real app data wherever possible.

For example:

If a person has no emergency contact, the app should know that from the Person record.

If an activity has no risk assessment, the app should know that from the Activity and Risk Assessment records.

If a task is blocked, the app should know that from the Task status.

Avoid asking users to tick a separate readiness box when the app can infer the issue from existing information.

---

## Readiness Question

The system should help answer:

- Are the people ready?
- Is attendance clear?
- Are key details missing?
- Are teams/groups organised?
- Is the programme complete?
- Are activities prepared?
- Are risk assessments ready?
- Are tasks complete?
- Are print/export packs ready?
- Are there unresolved warnings?

---

## Readiness Categories

Future readiness categories may include:

- Camp Details
- People and Attendance
- Contacts and Medical Information
- Sections and Teams
- Programme
- Activities
- Tasks
- Risk Assessments
- Documents
- Adult / Staffing Checks
- Communications
- Outputs and Packs
- Close-down later

---

## Issue Levels

Useful issue levels:

- Critical
- Warning
- Information

## Critical

Critical means the camp should not be considered ready until the issue is resolved.

Examples:

- attending young person missing emergency contact
- activity missing required risk assessment
- no leader assigned to an important programme session
- critical task blocked
- required adult cover missing

## Warning

Warning means the camp may still proceed, but the organiser should review the issue.

Examples:

- invited person has no attendance response
- non-urgent task overdue
- programme session has no location
- dietary information is incomplete
- activity equipment notes are missing

## Information

Information means something useful to know, but not necessarily a problem.

Examples:

- several people are marked Not attending
- a programme session has optional notes
- an activity has a wet weather alternative
- a task is complete but not checked

---

## People and Attendance Readiness

People readiness should consider:

- provisional people still present
- attendance not confirmed
- missing emergency contacts
- missing contact details
- missing allergy information
- missing medication information
- missing medical notes
- missing dietary requirements
- duplicate names needing review
- people imported into the wrong section
- people with incomplete profiles

The People page already has profile completeness checks.

Future readiness should build on that rather than duplicating it.

---

## Candidate Roster and Readiness

The People module now works as a candidate roster.

This means readiness checks must understand attendance status.

For example:

An emergency contact missing for an Attending young person is more serious than the same missing field for someone marked Not attending.

Suggested readiness logic:

- Attending: include in operational readiness checks
- Invited: show as warning or pending
- No response: show as pending
- Not attending: exclude from most operational checks
- Provisional: show as planning warning
- Unknown: show as warning until reviewed

---

## Section Readiness

Section readiness should help answer:

- how many people are attending in each section?
- how many are invited?
- how many have no response?
- how many are provisional?
- how many have missing profile data?
- are people in the correct section?

This is why attendance summaries and filters are a near-term priority.

---

## Team Readiness

Team readiness should consider:

- required teams created
- people assigned to teams
- teams with too few people
- teams with no leader or responsible adult
- people not assigned to any needed group
- duplicate or conflicting team memberships

Future accommodation, transport and duty-team features can build on this.

---

## Task Readiness

Task readiness should consider:

- incomplete tasks
- blocked tasks
- overdue tasks
- unassigned tasks
- urgent tasks not done
- Safety / Risk tasks not done
- People & Forms tasks not done
- Programme tasks not done

Tasks are one of the strongest foundations for readiness.

The future readiness system should use the task module rather than creating a separate manual checklist.

---

## Programme Readiness

Programme readiness should consider:

- empty programme days
- gaps in the programme
- overlapping sessions
- sessions with no lead person
- sessions with no location
- sessions with no participant group
- activities without risk assessments
- activities without equipment notes
- sessions with too few supporting adults
- leader clashes

The Programme module already has some warning concepts.

Future readiness should bring these warnings into the camp dashboard.

---

## Activity Readiness

Activity readiness should consider:

- activity lead assigned
- supporting adults identified
- equipment notes complete
- risk notes complete
- wet weather alternative added where useful
- risk assessment status
- programme sessions linked correctly

Activities can become reusable planning assets later.

---

## Risk Assessment Readiness

Risk readiness should consider:

- camp-level risk assessment exists
- camp-level risk assessment status
- activity-level risk assessment exists where needed
- activity-level risk assessment status
- controls added
- unresolved review actions
- risk assessments needing update

Important note:

The app helps organise risk assessment information.

It does not replace official Scouts approval processes.

---

## Document and Output Readiness

Document/output readiness should consider whether required packs have been generated or reviewed.

Possible future checks:

- parent pack prepared
- leader pack prepared
- programme printed/exported
- team task sheets printed/exported
- emergency/contact list printed/exported
- risk assessment pack printed/exported
- final information prepared

This should come after the output system is more mature.

---

## Adult / Staffing Readiness

Adult/staffing readiness is deferred but important.

Possible checks:

- camp leader assigned
- permit holder recorded
- first aider identified
- enough adults for activities
- session leads assigned
- supporting adults assigned
- young leader roles clear
- helper roles clear

This must be handled carefully and should not claim to replace official Scouts rules.

---

## Communications Readiness

Communications readiness is deferred.

Possible future checks:

- parents/carers have received joining instructions
- leaders have received leader pack
- helpers have received task information
- missing information reminders sent
- final event information sent

This should wait until the Communications module exists.

---

## Dashboard

The future Camp Dashboard should show readiness clearly.

Useful dashboard sections:

- attendance summary
- missing profile information
- open urgent tasks
- blocked tasks
- programme warnings
- risk assessment status
- print/export status
- next actions

The dashboard should not just show a score.

It should show what needs doing next.

---

## Readiness Score

A readiness score may be useful later, but it should not be the first version.

A single percentage can hide important problems.

Example:

A camp may be 95% ready but still missing one critical emergency contact.

Better first version:

- Critical issues
- Warnings
- Information
- Next actions

Only add a score later if it genuinely helps.

---

## Readiness and Future Modules

Future modules will add more readiness inputs.

Examples:

Food readiness:

- menu complete
- dietary needs reviewed
- shopping list complete
- cooking rota complete

Transport readiness:

- drivers assigned
- passenger lists complete
- collection arrangements confirmed
- equipment loads planned

Finance readiness:

- payments tracked
- budget reviewed
- expenses recorded

These should wait until those modules exist.

---

## Current Priority

Do not build the full Readiness System yet.

Current priorities remain:

1. Safer section-level OSM member imports
2. Safer section-level OSM attendance imports
3. Attendance summaries and filters
4. Import review improvements
5. Bulk move people between sections

These priorities make the people and attendance data reliable.

Reliable data is needed before readiness can be trusted.

---

## First Readiness Features to Build Later

When ready, start with simple, useful checks:

1. Missing emergency contacts for attending young people
2. Missing medical/allergy/dietary information for attending young people
3. Provisional people still present
4. Invited or no-response people needing review
5. Unassigned tasks
6. Blocked tasks
7. Activities missing risk assessments
8. Programme sessions with no lead
9. Programme sessions with no location
10. Risk assessments not ready

These are practical and directly useful.

---

## Summary

Readiness is the long-term purpose of the app, but it should be built carefully.

The system should not ask users to maintain a separate readiness checklist if the app already has the information.

First, make the core People, Sections, Tasks, Programme and Risk Assessment data reliable.

Then use that data to show what still needs doing.