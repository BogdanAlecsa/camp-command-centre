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
- Participating groups
- Teams
- Tasks
- Activities
- Programme
- Presence windows
- Session staffing
- Backup plans
- Risk assessments
- Printable outputs
- OSM member import
- OSM attendance import groundwork

---

## Current Phase

Current phase:

**Phase 1 MVP — Core Camp Planning**

Current active focus:

**Programme reliability, print packs, risk coverage and readiness foundations**

---

## Recently Completed Milestones

### Programme Staffing

Completed:

- Session Staff model
- Session Staff roles
- adult Lead distinction
- presence-aware staff dropdown
- staff leaving early warnings
- inline Open profile / Edit / Remove actions
- migration path away from legacy Lead Person field

### Session Cover and Roll Call

Completed:

- session cover card
- unique total people at start
- unique total people for full session
- people leaving early count
- participants/staff breakdown
- adult Lead status
- session roll-call printable

### Backup Plans

Completed:

- backup plans attached to sessions
- backup reasons
- optional linked Activity
- location/duration/notes
- add/edit/remove backup plans

---

## Immediate Short-Term Plan

### 1. Stabilise programme print packs

Do this next.

Tasks:

- add tests/smoke checks for print routes
- carefully convert print lead display to Session Staff Lead(s)
- carefully add muted backup summaries to leader/internal printables
- avoid parent-facing clutter
- make one print route/template change at a time

Priority print routes:

1. leader programme
2. full programme
3. group programmes
4. activity leader schedules
5. leader board
6. roll call

### 2. Risk Assessment coverage mode

Add an RA coverage model so the app can say:

- specific RA attached
- covered by event RA
- covered by site RA
- covered by generic RA
- not required / low-risk
- needs review

Add a details/justification field.

Make printables show the coverage clearly.

### 3. Clean up legacy Lead Person

Continue removing remaining UI/template dependency on `lead_person_id`.

The database column can stay temporarily.

The user-facing model should be Session Staff role = Lead.

### 4. Add basic route/template tests

Start with smoke tests for:

- programme list
- programme detail
- print full
- print groups
- print leader
- print activity leaders
- roll call

This will prevent repeated print regressions.

---

## Medium-Term Plan

### 5. Nights Away ratio design

Do not rush this.

Design first.

Rules:

- only applies to Nights Away / residential events
- Young Leaders count as young people for ratios
- Young Leaders do not count as adult cover
- ratio checks should be evaluated by actual supervision group/session where groups are separated
- campwide checks are useful but not sufficient

Likely model:

- ratio applicability by camp type
- section/group ratio settings
- session supervision mode
- adult cover count
- young person count
- warnings

### 6. People and OSM workflow polish

Improve:

- section-level OSM import buttons
- safer target section selection
- import preview clarity
- attendance summaries by section
- attendance filters
- duplicate-name handling
- bulk move between sections

### 7. Programme rotation builder

Improve rotation creation so the user can generate sessions more easily.

Possible features:

- choose groups
- choose activities
- choose slots
- generate rotation table
- review before applying

### 8. Dashboard/readiness foundations

Add dashboard cards for:

- people summary
- attendance summary
- missing data
- task status
- programme warnings
- risk assessment status
- print pack readiness

---

## Long-Term Plan

### Phase 2

- stronger readiness system
- forms/document handling
- communications templates
- improved exports/archive packs

### Phase 3

- food and catering
- transport
- finance

### Phase 4

- compliance and Nights Away checks
- ratio engine
- permit/NAN readiness support

### Phase 5

- site planning
- equipment planning
- accommodation
- lessons learned

### Phase 6

- online deployment
- user accounts
- collaborative editing
- PostgreSQL
- audit trail
- backups

---

## Development Discipline

Before each merge:

```bash
python -m compileall app scripts
git status
```

For print-related changes:

1. run compile check
2. open every affected print route
3. check browser and server logs
4. commit only when all affected print routes load

Create a fresh branch for each focused milestone.
