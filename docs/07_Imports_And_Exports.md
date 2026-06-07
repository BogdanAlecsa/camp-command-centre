# Imports and Exports

The app should make it easy to get data in and useful information out, without exposing users to fragile internal data formats.

Imports and exports should support the way Scout camps are actually planned:

- information may arrive gradually
- some people may be provisional at first
- OSM data is section-based
- attendance may change after people have already been imported
- sensitive information must be handled carefully

---

## Current Status

The app now has early working support for:

- person-level OSM member import
- bulk OSM member import preview
- bulk OSM member import apply
- OSM event attendance import groundwork
- printable outputs for tasks, teams, programme and risk assessments

The import system is still early and must be made safer before relying on it heavily with real camp data.

---

## OSM Member Import

OSM member exports are used to import or update people in a camp.

The current importer can read useful camp fields from an OSM member export, including:

- first name
- last name
- email
- phone
- primary contact
- emergency contact
- allergies
- medication
- medical notes
- dietary requirements
- section unit / six / patrol / leader unit

The app stores the OSM unit internally as a neutral section unit field.

Examples:

- Cubs may use Six names
- Scouts may use Patrol names
- Leaders may appear under a Leaders unit
- Young Leaders may appear under Young Leaders / YLs

The importer can suggest person type from the OSM unit:

- Leader units suggest Leader
- Young Leaders / YLs suggest Young Leader
- otherwise the selected default type is used, usually Young Person

---

## Bulk OSM Member Import Workflow

The current workflow is:

1. Choose target section
2. Upload OSM member export
3. Preview imported rows
4. Match existing people by name within the selected section
5. Apply selected rows

Apply can:

- update matched people
- replace provisional people
- create new people for unmatched rows

Existing non-blank fields should be protected by default.

Manual corrections should not be overwritten unless the organiser explicitly chooses to replace existing data.

---

## OSM Event Attendance Import

OSM event exports are used to update attendance for a camp.

The expected event export structure is simple:

- First Name
- Last Name
- Attending

Attendance values are mapped as follows:

- Yes becomes Attending
- No becomes Not attending
- Invited becomes Invited
- blank becomes No response

This allows a useful camp setup workflow:

1. Import all section members into the camp candidate roster
2. Import the OSM event attendance export later
3. Use attendance status to decide who appears in operational outputs

---

## Candidate Roster

People in a camp are not necessarily final attendees.

The People module should support a candidate roster, where each person may be:

- Provisional
- Invited
- Attending
- Not attending
- No response
- Unknown

Operational outputs should later be able to filter to the correct people, usually Attending only.

---

## Safer Section-Level Imports

The current global import buttons are useful, but they are too easy to misuse.

Future import workflow should move import actions into each section block.

Example:

Cubs:

- Import/update Cubs from OSM member export
- Update Cubs attendance from OSM event export

Scouts:

- Import/update Scouts from OSM member export
- Update Scouts attendance from OSM event export

This avoids accidentally importing a Cubs file into Squirrels or another section.

Preferred future routes:

- /camps/{camp_id}/sections/{section_id}/osm-member-import
- /camps/{camp_id}/sections/{section_id}/osm-attendance-update

The import page should clearly show the target section.

Example:

You are importing into: Cubs

---

## Import Review Requirements

Before Apply is pressed, the importer should show what will happen to each row.

Each row should show one of:

- Update existing person
- Replace provisional person
- Create new person
- Skip
- Needs manual review

Duplicate-name matches should not be guessed.

If more than one person has the same normalised name in the target section, the row should require manual review.

---

## Recovery Tools

The app should provide a simple way to recover from import mistakes.

Needed tool:

- select multiple people
- choose a new section
- move selected people

This is useful if people are imported into the wrong section or if section assignments need correcting.

---

## Current Export Types

Current or near-term printable/exportable outputs include:

- camp overview
- people list
- emergency contacts
- team lists
- task sheets
- team work packs
- programme
- group schedules
- leader schedules
- parent pack
- leader pack
- risk assessment pack
- readiness report later

---

## Deferred Export / Import / Archive System

A future export/import/archive system is planned, but it is not current work.

This belongs later in the roadmap, after the People, Sections and OSM workflows are stable.

Planned future file types:

- .ccctemplate
- .cccarchive
- .cccbackup

---

## Camp Template File

A .ccctemplate file is a reusable camp template.

It may contain:

- activities
- programme structure
- tasks
- task categories
- task phases
- risk assessment templates
- teams / group structures
- settings

It must not contain:

- people
- contact details
- emergency contacts
- medical information
- dietary information
- attendance records

Templates are for reusing planning structure, not personal data.

---

## Camp Archive File

A .cccarchive file is an archived camp record.

An archive may contain by default:

- names
- sections
- teams
- attendance
- activities
- programme
- tasks
- risk assessments

The archive wizard should allow sensitive fields to be included or excluded.

Suggested defaults:

- Names: on
- Attendance: on
- Teams: on
- Programme: on
- Tasks: on
- Activities: on
- Risk assessments: on
- Contact details: off
- Emergency contacts: off
- Medical information: off

Sensitive fields should be off by default.

---

## Full Backup File

A .cccbackup file is a full application backup.

It should contain:

- the full database
- all camps
- all people
- all tasks
- all programme data
- all risk assessment data
- all settings
- everything needed for disaster recovery

This is different from a camp template or archive.

A backup is for restoring the whole application after data loss or moving the application to another computer.

---

## File Format Principles

Normal users should not be given raw JSON exports.

Future Camp Command Centre files should use app-specific formats.

Design principles:

- no user-facing JSON exports
- app-managed encryption
- no user-managed passwords for normal exports
- protection against casual viewing
- protection against accidental editing
- portability between computers

---

## Camp Lifecycle

Future camp states should include:

- Planning
- Active
- Completed
- Archived

Completed camps can later be archived and removed from normal working views.

Archived camps should be restorable if needed.

---

## Current Priority

Do not build the export/import/archive system yet.

Current priorities remain:

1. Safer section-level OSM member imports
2. Safer section-level OSM attendance imports
3. Attendance summaries and filters
4. Import review improvements
5. Bulk move people between sections