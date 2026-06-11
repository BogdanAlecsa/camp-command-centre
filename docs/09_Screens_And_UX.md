# Screens and UX

The app should feel like a guided planning tool, not a database front end.

Screens should help the organiser make practical decisions.

---

## Current Screen Areas

Current early-MVP screen areas include:

- dashboard
- camp list/detail/edit
- people list/detail/edit
- provisional people
- sections
- participating groups
- teams
- tasks
- task command centre
- activities
- programme
- presence
- risk assessments
- OSM import/update screens
- printable outputs

---

## UX Principle

Use practical language.

Good workflow language:

- Create Camp
- Add People
- Import from OSM
- Update Attendance
- Create Teams
- Add Tasks
- Build Programme
- Add Session Staff
- Add Backup Plan
- Check Risk Assessments
- Print Packs

Avoid making users think like database administrators.

---

## People UI

People pages should support:

- clear grouping by section
- attendance status
- opening person profile
- editing person details
- profile completeness
- medical/dietary visibility where appropriate
- OSM import/update workflows
- provisional planning

Where a page already has an **Open profile** button, names should remain plain text.

Avoid turning every name into an underlined hyperlink.

---

## Inline Action Pattern

The preferred table action pattern is inline buttons:

```text
Open profile | Edit | Remove
```

This is now used in areas such as:

- team members
- session staff
- backup plans

Buttons should stay compact and aligned.

Avoid stacked action buttons inside table cells unless the screen is very narrow.

---

## Programme Session UI

Session detail should show:

- main session details
- session cover summary
- backup plans
- session staff
- presence warnings
- roll-call button

This page is an operational hub for a single session.

---

## Session Cover Card

The Session Cover card should be compact and readable.

It should show:

- total people at start
- total people for full session
- people leaving early
- participant counts
- staff counts
- staff role counts
- adult lead status
- staff leaving early

This is not the same as ratio compliance.

It is operational session awareness.

---

## Backup Plans UI

Backup plans should be visible but not overpower the main programme.

The session detail page should show full backup details.

Print outputs should show backup plans only where helpful and in muted style.

Backup plans should be editable inline.

---

## Risk Assessment UI

Risk assessment UI needs improvement.

Current issue:

A programme or activity may not need a standalone RA because it is covered by:

- event RA
- site RA
- generic RA
- simple low-risk judgement

Future RA UI should ask:

```text
How is this covered?
```

instead of only:

```text
Which RA is attached?
```

Suggested field:

- RA coverage mode
- details / justification

---

## Print UX

Print pages should be treated as field documents.

Rules:

- avoid clutter
- use readable font sizes
- avoid heavy borders
- avoid broken table splits where possible
- show operational data only to the right audience
- keep parent-facing outputs clean

Print route changes should be tested every time.

---

## Visual Style

The app should stay plain, calm and practical.

Good UI:

- cards
- compact tables
- clear muted text
- restrained warnings
- buttons with consistent alignment
- operational printouts

Avoid:

- excessive icons
- noisy colours
- link-heavy tables
- giant forms without grouping
- hidden duplicate sources of truth
