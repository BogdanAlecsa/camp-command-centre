# Programme Planner

The Programme Planner helps organise the timetable for a camp, sleepover or Nights Away event.

It is one of the core MVP modules.

---

## Current Programme Features

The Programme module currently supports:

- creating sessions
- editing sessions
- deleting sessions
- linking sessions to activities
- assigning participant teams/groups
- setting date, start time and end time
- locations
- notes
- session types
- rotation groups
- rotation slot numbers
- programme printables
- session detail pages
- session staff
- session backup plans
- session headcount and roll-call output

---

## Programme Session

A programme session is a scheduled block of time.

Examples:

- wide game
- breakfast
- hike
- setup
- pack down
- free time
- leader/admin time
- activity rotation base
- travel slot

A session may link to an Activity, but it does not have to.

This allows both reusable activities and simple timetable notes.

---

## Session Types

Current session types include:

- Activity
- Meal
- Travel
- Setup / Pack Down
- Free Time
- Leader / Admin
- Whole Camp
- Group Rotation
- Other

Session type affects display/styling and helps print packs become more useful.

---

## Rotation Planning

The Programme module includes support for rotation groups and slot numbers.

This allows leaders to create a set of sessions that form a rotation.

Future improvements should make rotation creation more guided and less manual.

---

## Session Staff

Session Staff is the current operational staffing model.

A session can have multiple staff members.

Each staff member has:

- person
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

The old single Lead Person field is no longer the correct user-facing model.

The source of truth for leads should be:

```text
ProgrammeSessionStaff.role == "Lead"
```

---

## Adult Lead Rule

A session can have one or more Leads.

For adult cover, a Lead only counts as adult cover if the person type is:

- Leader
- Helper

Young Leaders may be assigned as staff or even help run the activity, but they are not adult Lead cover.

The app should warn if:

- no adult Lead is assigned
- the adult Lead is not expected at session start
- no adult Lead is present for the full session

---

## Presence-Aware Staffing

Session staffing uses presence windows.

When adding staff to a session:

- people not present at session start are hidden from the staff dropdown
- people present at start but leaving before the end remain selectable with a warning
- assigned staff remain visible in the session staff table with warnings

This prevents obvious staffing mistakes without making planning impossible.

---

## Session Cover Card

The session detail page includes a cover summary.

It shows:

- total people at start
- total people for full session
- people leaving before session ends
- participants at start
- participants for full session
- assigned staff by person type at start
- assigned staff by person type for full session
- assigned staff by session role at start
- assigned staff by session role for full session
- staff leaving early
- adult Lead at start
- adult Lead for full session

Counts are unique person counts.

This prevents double-counting someone who might otherwise appear in more than one category.

---

## Session Roll Call

A session can generate a roll-call printable.

The roll call includes:

- session staff
- participants
- person type
- session role
- group
- presence status
- notes
- tick boxes

This is intended for practical roll calls during camp.

---

## Backup Plans

Backup plans are attached to a session.

They are for fallback planning, not for changing the main timetable.

Backup reasons include:

- Wet weather
- Too hot
- Low light / darkness
- Activity overrun
- Equipment unavailable
- Instructor unavailable
- Low energy / tired group
- Behaviour reset
- Other

A backup can link to an existing Activity or be a custom lightweight entry.

Backup fields include:

- linked Activity
- title
- reason
- location
- approximate duration
- notes

Backup plans can currently be added, edited and removed.

---

## Backup Plans in Printables

Desired behaviour:

- parent/young person programme: hide backups
- leader/internal programme: show backups quietly
- session roll call: usually hide backups
- session detail page: show full backup details

Suggested print style:

```text
Wide Game
Backup: Indoor quiz — Wet weather · Hall · 45 min
```

This needs to be added carefully to print templates one at a time.

---

## Print Packs

Programme print outputs include:

- full programme
- group programmes
- activity leader schedules
- leader programme
- leader location board
- session roll call

Print routes and templates must be handled cautiously.

Recent work showed that broad automated patching can break print routes.

Future print changes should be made one route/template at a time with smoke testing after each change.

---

## Next Programme Improvements

Short-term:

1. Add backup plan display to leader/internal printables only.
2. Convert remaining print lead displays to Session Staff Leads.
3. Add tests/smoke checks for all programme print routes.
4. Improve RA coverage display for sessions and activities.
5. Consider a clearer session staff summary in list views.

Medium-term:

1. Better rotation builder.
2. Session supervision mode for ratio checks.
3. Nights Away ratio warnings.
4. Programme readiness review.
5. Programme export packs.
