# Project Status

## Current Phase

**Phase 1 MVP — Core Camp Planning**

## Current Milestone

**Programme, presence-aware staffing, roll-call outputs and backup planning**

The app is now a working early MVP with a usable core workflow.

The current build has moved substantially beyond the original starter skeleton.

---

## Current Working Areas

Implemented or substantially working:

- Camp setup
- People records
- Sections
- Participating groups
- Teams and team memberships
- Tasks and task assignments
- Task command centre
- Activities
- Activity risk assessments
- Camp risk assessments
- Programme sessions
- Programme rotations
- Presence windows
- Presence-aware session staffing
- Session Staff roles
- Adult Lead warning logic
- Session headcount card
- Session roll-call printable
- Programme session backup plans
- Backup plans linked to existing activities
- Inline edit/remove patterns for session staff and backup plans
- OSM member import
- OSM attendance import groundwork
- Printable task and programme outputs

---

## Recently Completed

### Programme Staffing

- Added Session Staff model and UI.
- Session Staff can have roles such as Lead, Supporting Adult, Parent Helper, Young Leader and First Aider.
- Staff selection is presence-aware.
- People not present at the start of a session are hidden from the staff dropdown.
- People present at the start but leaving before the end remain selectable with a warning.
- Already assigned staff are shown with presence warnings.
- Staff rows include Open profile, Edit and Remove actions.

### Lead Handling

- The old single Lead Person field is being retired.
- Lead responsibility is now represented through Session Staff role = Lead.
- Adult Lead checks distinguish adults from Young Leaders.
- Young Leaders may assist operationally but do not count as adult Lead cover.
- Legacy Lead Person data is migrated/ignored as part of the transition.

### Session Cover

- Session detail page now shows operational cover.
- It includes unique total headcounts, participant counts, staff counts and adult lead status.
- Counts are unique people, not category sums, so the same person is not counted twice.

### Roll Call

- Added Session Roll Call printable.
- Roll call includes participants and session staff.
- It includes role, person type, presence status and tick boxes.

### Backup Plans

- Added session-level Backup Plans.
- Backup plans can be free text or linked to an existing Activity.
- Backup plans can be edited and removed.
- Backup plans do not alter the main programme timetable.

---

## Known Current Issues / Technical Debt

These should be handled before expanding too far:

1. **Programme print packs need careful follow-up**
   - Printables are working again after repair.
   - Backup plan display in printables should be reintroduced carefully, one print route/template at a time.
   - Print packs should fully move away from legacy Lead Person fields and use Session Staff Leads.

2. **Risk Assessment coverage needs better modelling**
   - Some sessions/activities may have a specific RA.
   - Some may be covered by event RA, site RA or generic RA.
   - Some may not need a separate RA.
   - The UI and printables need to show this clearly.

3. **Nights Away ratio engine not yet implemented**
   - Ratios apply to Nights Away / residential events.
   - Young Leaders count as young people for ratios.
   - Adult ratio cover should be evaluated by actual supervision group/session where groups are separated.

4. **Schema evolution is still informal**
   - SQLite schema changes are currently handled pragmatically.
   - A future migration strategy is needed before wider use.

5. **Tests are still light**
   - There should be basic route/template smoke tests.
   - Print routes especially need tests to prevent repeated regressions.

---

## Immediate Next Development Order

1. Finish repair/cleanup around programme print packs.
2. Add quiet backup-plan display to leader/internal printables only.
3. Convert remaining print lead displays to Session Staff Lead(s).
4. Add Risk Assessment coverage mode.
5. Add basic tests for programme detail and print routes.
6. Design Nights Away ratio engine before coding it.

---

## Merge Status

Main repository should now contain the current working feature set.

Use a fresh branch for the next development stage.
