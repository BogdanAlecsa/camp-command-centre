# Screens and UX

The app should feel like a guided camp planning tool, not like a database system.

The user experience should make the next useful action obvious, reduce mistakes, and help organisers understand what still needs attention.

---

## Current Status

The app now has working screens for the main early-MVP areas:

- camp list
- camp detail
- people list
- person detail
- person edit
- provisional people
- sections
- teams
- tasks
- task command centre
- activities
- programme
- risk assessments
- OSM member import
- OSM attendance import groundwork
- printable outputs

The screens are usable, but some workflows still need safety and polish.

The highest-priority UX issue is the OSM import workflow.

---

## UX Principle

The app should guide the organiser through practical camp planning.

It should avoid making the user think like a database administrator.

Good workflow language:

- Create Camp
- Add People
- Import this Section from OSM
- Update Attendance
- Create Teams
- Add Tasks
- Build Programme
- Check Risk Assessments
- Print Packs

Avoid technical or internal language where possible.

---

## Camp Dashboard

The camp dashboard should become the organiser's main command centre.

It should eventually show:

- camp details
- people/attendance summary
- missing profile information
- task summary
- programme summary
- risk assessment summary
- warnings
- next actions
- useful print/export buttons

The dashboard should answer:

What needs my attention now?

Current dashboard/navigation works, but it needs stronger summaries later.

---

## People Page

The People page is now a key workflow screen.

It should show people grouped by section.

Each section should eventually show:

- section name
- number of people
- attendance summary
- missing profile summary
- section-specific actions

The People page should support:

- viewing all people
- filtering by attendance status
- filtering by missing information
- opening a person
- printing person/task sheets
- creating provisional people
- importing OSM data
- updating attendance

---

## Section Blocks

Section blocks should become the normal place for section-specific actions.

Each section block should eventually include:

- Add person to this section
- Create provisional people for this section
- Import/update this section from OSM member export
- Update this section attendance from OSM event export
- Move selected people to another section later

This is safer than having one global import button at the top.

The target section should be obvious.

---

## OSM Import UX

The current OSM import tools work, but the UX needs improvement.

The main problem is that the user can accidentally choose the wrong target section.

The next UX improvement should be section-specific imports.

Instead of this:

- Click global Bulk Import from OSM
- Choose section from dropdown
- Upload file

Use this:

- Open Cubs section block
- Click Import/update Cubs from OSM
- Upload file
- Preview
- Apply

The import page should clearly say:

You are importing into: Cubs

---

## OSM Member Import Review

The import preview should clearly show what will happen before Apply is pressed.

Each row should show an action:

- Update existing person
- Replace provisional person
- Create new person
- Skip
- Needs manual review

This is more useful than only showing whether a row matched.

The user should not have to guess what Apply will do.

---

## OSM Attendance Import Review

The attendance import should show:

- OSM row name
- current matched person
- current attendance status
- new attendance status
- warning if no match
- warning if duplicate match

Attendance import should be easy to run repeatedly as OSM responses change.

The user should trust that it only updates attendance, not contact or medical information.

---

## File Upload Feedback

File upload screens should give immediate feedback when a file is selected.

Good behaviour:

- button disabled until file selected
- text says No file selected yet
- after selection, show selected file name
- button changes to Preview selected export
- user previews before applying

This was added to OSM upload screens and should be used consistently.

---

## Import Safety

Import screens must be careful because they can change many people at once.

Safety rules:

- preview before apply
- do not overwrite existing non-blank fields by default
- make target section clear
- show per-row action
- show result summary after apply
- flag duplicate names
- flag unmatched rows
- allow rows to be skipped

Bulk imports should never feel like a blind upload.

---

## Import Result Summary

After applying an import, show a clear result summary.

Example:

- Updated: 12
- Replaced provisional: 3
- Created: 4
- Skipped: 1
- Needs review: 2

This should appear on the People page or import result page.

It should be visible enough that the organiser knows what happened.

---

## Attendance Summaries

Once OSM event attendance import is used, the People page should show attendance summaries.

Example:

Cubs:

- Attending: 18
- Invited: 4
- Not attending: 6
- No response: 2
- Provisional: 0

This summary should help the organiser understand the state of each section quickly.

---

## People Filters

People filters should be simple and useful.

Suggested filters:

- All
- Attending
- Invited
- Not attending
- No response
- Provisional
- Missing profile information

These filters become important after importing full section rosters.

---

## Profile Completeness UX

The app now tracks missing profile information.

This should be visible but not overwhelming.

Good UX:

- show a small missing count badge in lists
- show detailed missing fields on person detail
- provide a clear Update Profile button
- avoid crowding the main People table

The missing information view should help the organiser fix issues quickly.

---

## Section Unit Display

The app stores section unit, such as Six or Patrol.

This should not be shown on the main People list by default because it makes the table too busy.

It should be visible on:

- person detail
- person edit
- import preview
- future team/group tools

Keep the People list focused.

---

## Tables

Tables should stay readable.

Avoid adding too many columns.

If information is useful but not always needed, show it in:

- detail pages
- expandable rows
- badges
- summaries
- filters
- import preview screens

Crowded tables are harder to use during real camp planning.

---

## Buttons and Actions

Buttons should be placed where the action belongs.

Examples:

Global People actions:

- Add Person
- Create Provisional People
- Sections
- Back to Camp

Section-specific actions:

- Import this section from OSM
- Update this section attendance
- Add person to this section

Person-specific actions:

- Edit Person
- Replace Provisional
- Update from OSM
- Print

This reduces mistakes.

---

## Print UX

Printable outputs should be easy to find and clearly labelled.

Current print outputs include:

- person task sheets
- team task sheets
- programme outputs
- risk assessment outputs

Future print outputs should be grouped into packs:

- parent pack
- leader pack
- task pack
- risk assessment pack
- camp file

Print pages should avoid showing editing controls.

---

## Risk Assessment UX

Risk assessment screens should be practical and not intimidating.

They should help users capture:

- what could go wrong
- who is at risk
- controls
- review notes
- status

Risk assessment print views should be clean and useful.

Important note:

The app assists with organising risk assessment information.

It does not replace official Scouts approval processes.

---

## Programme UX

Programme screens should help users understand the day.

Current programme list by day is useful.

Future improvements:

- better visual timeline
- easier session editing
- better group filtering
- better rotation editing
- stronger warnings
- cleaner print layouts

Do not overcomplicate the programme screen before the People/OSM workflow is safer.

---

## Task UX

Task screens should help users act.

Good task UX:

- show what is assigned
- show what is blocked
- show what is unassigned
- show what is due soon
- make work packs easy to print

The task system should not become too complicated too early.

---

## Mobile UX

The app is mainly being built for desktop/browser use.

However, some users may view pages on tablets or phones.

Pages should remain readable on smaller screens where reasonable.

Tables may need responsive behaviour later.

---

## Error Messages

Error messages should be plain and specific.

Bad:

Something went wrong.

Better:

This OSM export could not be read. Please upload an .xlsx OSM member export.

Good error messages should say:

- what happened
- why it matters
- what the user can do next

---

## Confirmation Messages

The app should confirm important actions.

Examples:

- import applied
- person created
- provisional person replaced
- task saved
- risk assessment updated
- programme session deleted

For destructive actions, confirmation should be stronger.

---

## Current UX Priorities

The immediate UX priorities are:

1. Move OSM import buttons into section blocks
2. Add section-specific import routes
3. Show target section clearly on import pages
4. Improve per-row import action labels
5. Add import result summaries
6. Add attendance summaries by section
7. Add People page filters
8. Add bulk move between sections

---

## Deferred UX Areas

Do not focus on these yet:

- advanced dashboard design
- full drag/drop programme editing
- full online collaboration UX
- parent portal UX
- full export/archive UX
- mobile-first redesign

These can come later.

---

## Summary

The app should be practical, calm and hard to misuse.

The next UX work should make the People, Sections and OSM import flow safer and clearer before expanding into large new modules.