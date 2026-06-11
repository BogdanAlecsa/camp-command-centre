# Readiness System

The Readiness System is the long-term answer to the question:

**Are we ready?**

It is not yet a full implemented module.

Current work provides many of the data sources that a readiness engine will later use.

---

## Current Readiness Signals

The app already has several useful signals:

- missing person information
- attendance status
- task status
- programme sessions
- programme staff cover
- adult Lead warnings
- presence warnings
- risk assessment status
- backup plans
- print outputs

These are not yet combined into a full readiness score.

---

## Readiness Should Be Practical

Readiness should not become a decorative dashboard.

It should answer questions leaders actually care about:

- do we know who is coming?
- do we have enough adult cover?
- are key sessions staffed?
- do sessions have adult leads?
- do we have fallback plans?
- are risk assessments done or covered?
- are critical tasks complete?
- have we printed what we need?
- are there unresolved warnings?

---

## Suggested Readiness Areas

Future readiness categories:

1. People and attendance
2. Medical/dietary information
3. Programme
4. Session cover
5. Risk assessments
6. Tasks
7. Equipment
8. Food
9. Transport
10. Documents and approvals
11. Print packs
12. Finance

Not all categories are MVP.

---

## Programme Readiness

Programme readiness should include:

- sessions planned
- sessions with missing activity/location
- sessions with missing adult Lead
- sessions where adult Lead is not present for full session
- sessions with staff leaving early
- sessions with no backup plan where a backup would be useful
- high-risk activities missing RA coverage

---

## Risk Assessment Readiness

Risk assessment readiness must not assume every session needs its own RA.

Future RA coverage modes:

- Specific RA attached
- Covered by event RA
- Covered by site RA
- Covered by generic RA
- Not required / low-risk
- Needs review

Each should allow a details/justification field.

Printables should show the coverage clearly.

---

## Nights Away Ratio Readiness

Mandatory ratio checks should apply only to Nights Away / residential events.

Important principle:

```text
Young Leaders can help operationally,
but they are still young people for ratios.
```

Ratio checks should eventually consider:

- campwide attendance
- section/group attendance
- separated supervision group/session attendance
- adult cover present at the relevant time
- risk assessment requirements for closer supervision

This requires careful design and should not be rushed into a quick patch.

---

## Readiness Levels

A future readiness item could use simple levels:

- OK
- Warning
- Needs review
- Missing
- Not applicable

This is more useful than a single percentage score.

---

## MVP Readiness Approach

For now, the app should focus on useful local warnings instead of a full readiness engine.

Examples:

- no adult Lead assigned
- adult Lead leaves before session ends
- person not expected at session start
- risk assessment missing or not reviewed
- task unassigned
- task overdue

A full readiness dashboard can come later.
