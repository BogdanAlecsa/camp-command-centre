# Imports and Exports

The app currently supports early import workflows and several printable outputs.

Imports and exports are critical because leaders already use OSM, spreadsheets and printable paperwork.

---

## OSM Member Import

The app supports OSM member import workflows.

Current capabilities include:

- bulk member import preview
- bulk member import apply
- matching by name inside a selected section
- updating existing people
- replacing provisional people
- creating new people
- importing useful camp information

Imported fields include:

- names
- contact information
- primary contact
- emergency contact
- allergies
- medication
- medical notes
- dietary requirements
- section unit / six / patrol / leader unit

---

## OSM Attendance Import

The app includes groundwork for OSM event attendance import.

Attendance mapping:

- Yes → Attending
- No → Not attending
- Invited → Invited
- blank → No response

This should become a central part of the candidate roster workflow.

---

## Import UX Rules

Imports must be safe.

The app should make it hard to accidentally import data into the wrong section.

Good future import behaviour:

1. Import button is inside the section block.
2. Target section is pre-selected and visually obvious.
3. Preview clearly shows what will happen.
4. User can review update/create/replace/skip decisions.
5. Apply step gives a clear result summary.

---

## Provisional People and Imports

Provisional people are important for early planning.

An import should be able to replace placeholders with real data.

Example:

- Cubs YP01 becomes Sophie Smith
- linked tasks, teams and programme group data are preserved

This is more useful than deleting and recreating planning data.

---

## Printable Outputs

Current printable outputs include:

- task sheets
- team work packs
- full programme
- group programme
- leader programme
- activity leader schedule
- leader location board
- session roll call

Printables are operational documents.

They must be simple, robust and readable.

---

## Programme Print Output Rules

Programme print packs should distinguish audiences.

Parent / young person programme:

- show the main plan
- avoid internal backup details
- avoid operational clutter

Leader / internal programme:

- show operational notes
- show session staff / leads
- show backup plans quietly
- show risk and cover warnings where useful

Session roll call:

- show expected people
- show roles and presence warnings
- include tick boxes
- avoid unnecessary programme clutter

---

## Backup Plans in Outputs

Backup plans should not appear as full timetable items.

They should appear, where appropriate, as quiet support text:

```text
Backup: Indoor quiz — Wet weather · Hall · 45 min
```

This should be added to leader/internal programme printables after the print routes have tests or careful manual checks.

---

## Future Exports

Future export ideas:

- camp file export
- PDF pack
- CSV export
- JSON backup/export
- archive pack after camp
- import/export templates

A full export/import/archive system is deferred.
