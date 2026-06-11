# Next Steps

This document captures the current short-term and long-term plan.

---

## Short-Term Plan

### 1. Stabilise programme print packs

This is the next practical priority.

The printables are important operational outputs and have already shown they are easy to break.

Immediate actions:

- create smoke tests for all programme print routes
- convert one print template at a time to use Session Staff Lead(s)
- add quiet backup plan summaries to leader/internal print templates
- keep parent/young person outputs clean
- avoid broad regex patches across all print routes/templates

Suggested order:

1. `print_leader.html`
2. `print_full.html`
3. `print_groups.html`
4. `print_activity_leaders.html`
5. `print_leader_board.html`
6. `print_session_roll_call.html` if needed

### 2. Add RA coverage mode

Risk assessment logic needs to become more realistic.

Current issue:

A programme item may not need a specific RA because it is already covered by:

- event RA
- site RA
- generic RA
- existing activity RA
- low-risk judgement

Suggested fields:

- coverage mode
- linked RA if relevant
- details / justification
- review status

Suggested coverage modes:

- Specific RA attached
- Covered by event RA
- Covered by site RA
- Covered by generic RA
- Not required / low-risk
- Needs review

Printables should show this clearly.

### 3. Finish lead-person cleanup

The source of truth should be:

```text
ProgrammeSessionStaff.role == "Lead"
```

Remaining work:

- search for old `lead_person_id` UI/display usage
- remove or ignore it in templates
- keep database column temporarily
- add tests to confirm session staff leads are displayed correctly

### 4. Add basic smoke tests

Start with route rendering tests.

Minimum test list:

- dashboard
- people list
- team detail
- programme list
- programme detail
- print full
- print groups
- print leader
- print activity leaders
- leader board
- session roll call

The goal is not perfect test coverage yet.

The goal is to catch broken templates before merging.

---

## Medium-Term Plan

### 5. Nights Away ratio design

Ratios should not be patched in quickly.

Important rules:

- apply only to Nights Away / residential events
- Young Leaders count as young people
- Young Leaders do not count as adult cover
- session/supervision-group checks matter most when groups are separated
- campwide checks are useful but not sufficient

Suggested concept:

```text
Supervision Ratio Check
```

Each programme session could later have a supervision mode:

- uses shared camp supervision
- requires own supervision cover
- off-site / separated group
- higher supervision required by risk assessment

### 6. Programme rotation improvements

The current rotation support works but is still manual.

Future builder:

- choose participant groups
- choose activities
- choose time slots
- generate sessions
- review before saving

### 7. OSM import workflow polish

Make imports safer:

- section-level import buttons
- obvious target section
- import preview with action labels
- clear apply results
- attendance summaries
- duplicate handling

### 8. Dashboard readiness cards

Add practical dashboard summaries:

- people attending
- missing profile information
- medical/dietary alerts
- tasks incomplete
- programme warnings
- RA status
- print pack readiness

---

## Long-Term Plan

### Food and Catering

Depends on reliable headcounts, attendance and dietary data.

Future features:

- meal plan
- dietary summary
- shopping list
- quantity calculation
- cooking plan

### Transport

Depends on attendance, presence windows and groups.

Future features:

- passenger lists
- vehicles
- drivers
- equipment loads
- collection arrangements

### Finance

Future features:

- budget
- payments
- spend tracking
- receipts
- cost summary

### Documents and Forms

Future features:

- form collection
- structured responses
- parent packs
- leader packs
- camp file

### Compliance

Future features:

- NAN readiness
- permit readiness
- first aid cover
- adult checks
- ratio checks
- required documents

### Online Deployment

Deferred until local MVP is stable.

Future changes:

- PostgreSQL
- user accounts
- permissions
- hosted deployment
- audit trail
- backups
