# How The App Works

Camp Command Centre is organised around a Camp.

A Camp is the main working object.

Everything else belongs to a Camp or supports planning that Camp.

---

## Core Idea

The app is not just a database of records.

It is intended to become a guided planning and operations tool.

The app should help the organiser understand:

1. Who is involved?
2. Who is attending?
3. What needs doing?
4. Who is responsible?
5. What is planned?
6. What is missing?
7. What needs checking?
8. Are we ready?

---

## Current App Structure

The current early-MVP app includes:

    Camp
     ├── People
     ├── Sections
     ├── Teams
     ├── Tasks
     ├── Activities
     ├── Programme
     ├── Risk Assessments
     ├── Printable Outputs
     └── OSM Imports

Future modules will add more areas later, but these are the current working foundations.

---

## Camp

A Camp represents one camp, sleepover, Nights Away event or similar activity.

A Camp contains:

- basic camp details
- people
- sections
- teams
- tasks
- activities
- programme sessions
- risk assessments
- printable outputs

The app is camp-centred.

This means that when a user is working, they are usually working inside one selected camp.

---

## People

People are stored against a specific camp.

The People module supports:

- young people
- leaders
- helpers
- young leaders
- parents/guardians
- visitors

People can be added manually, created as provisional placeholders, or imported from OSM.

A person can have:

- home section
- section unit
- person type
- attendance status
- information source
- contact details
- emergency contact details
- medical/allergy/dietary notes
- task assignments
- team memberships

---

## Candidate Roster

The People list is not only a final attendee list.

It is a candidate roster for the camp.

A person may be:

- Provisional
- Invited
- Attending
- Not attending
- No response
- Unknown

This allows the organiser to start planning before the final attendee list is confirmed.

It also allows the organiser to import all members from OSM and then use an OSM event export to update who is actually attending.

---

## Provisional People

Provisional people are placeholders.

Example:

- Cubs YP01
- Cubs YP02
- Scouts YP01

They allow planning to begin before names are known.

A provisional person can later be replaced with a real person while keeping existing links to teams, tasks and future planning structures.

---

## Sections

Sections group people by their Scout section or similar organisational group.

Default sections include:

- Squirrels
- Beavers
- Cubs
- Scouts
- Explorers
- Young Leaders
- Leaders / Adults
- Other

The People page is grouped by section.

Future OSM imports should be launched from inside the relevant section block so the target section is clear.

---

## Section Units

Different sections use different names for smaller units.

Examples:

- Cubs may use Sixes
- Scouts may use Patrols
- Young Leaders may appear as Young Leaders / YLs
- Leaders may appear as Leaders

The app stores this as a neutral section unit field.

The section unit is useful reference information.

It does not automatically create Teams yet.

---

## Teams

Teams are camp-specific working groups.

Examples:

- tent groups
- patrols/sixes
- duty teams
- activity groups
- transport groups
- leader teams
- helper teams

A person can belong to multiple teams.

Sections and Teams are different:

- Section says where someone belongs generally.
- Team says how someone is being used or grouped for this camp.

---

## Tasks

Tasks are used to plan and track work.

Tasks can be assigned to:

- people
- teams

Tasks can be organised by:

- status
- phase
- category
- priority
- due date

The app can produce task sheets and work packs.

This helps turn planning information into practical jobs for people to do.

---

## Activities

Activities describe things that may happen during the camp.

An activity can include:

- description
- default duration
- location
- activity lead
- supporting adults notes
- equipment notes
- risk notes
- wet weather alternative
- badge notes

Activities can be linked to programme sessions.

---

## Programme

Programme sessions create the camp timetable.

A programme session can include:

- date
- start time
- end time
- title
- session type
- linked activity
- participant group
- lead person
- supporting staff
- location
- notes

Programme outputs can show:

- full programme
- group schedules
- leader schedules
- activity leader schedules
- leader board

---

## Risk Assessments

Risk assessments are included as a safety backbone.

The app supports:

- camp-level risk assessment
- activity-level risk assessment
- risk controls
- printable risk assessment views
- risk assessment pack

Important note:

The app helps organise risk assessment information.

It does not replace official Scouts approval processes.

---

## OSM Imports

The app now has early OSM import support.

There are two main types of OSM import:

1. OSM member export
2. OSM event attendance export

---

## OSM Member Export

The OSM member export can be used to create or update people.

It can import useful fields such as:

- names
- phone/email
- primary contact
- emergency contact
- allergies
- medication
- medical notes
- dietary requirements
- section unit

The importer can:

- update existing people
- replace provisional people
- create new people

Existing non-blank manual data should be protected unless the organiser chooses to overwrite it.

---

## OSM Event Attendance Export

The OSM event attendance export can be used to update attendance status.

Typical values map as:

- Yes becomes Attending
- No becomes Not attending
- Invited becomes Invited
- blank becomes No response

This allows a useful workflow:

1. Import the whole section roster.
2. Import event attendance.
3. Use attendance status to decide who appears in operational outputs.

---

## Current Core Flow

The current working flow is:

    Create Camp
    Add or import People
    Organise People by Section
    Create Teams
    Create Tasks
    Assign Tasks
    Create Activities
    Build Programme
    Add Risk Assessments
    Generate Printable Outputs

---

## Near-Term Improved Flow

The next improved flow should be:

    Create Camp
    Open People
    Open a Section block
    Import/update that section from OSM
    Update that section attendance from OSM
    Review attendance and missing profile fields
    Create Teams
    Assign Tasks
    Build Programme
    Print outputs

This will reduce mistakes because imports will happen inside the section they belong to.

---

## Outputs

The app should turn planning information into practical outputs.

Current or near-term outputs include:

- people lists
- team lists
- task sheets
- team work packs
- programme printouts
- risk assessment pack
- leader pack later
- parent pack later
- readiness report later

---

## Readiness

The long-term aim is for the app to answer:

Are we ready?

Readiness should come from the data already in the app.

Examples:

- missing emergency contacts
- missing medical information
- incomplete tasks
- missing risk assessments
- programme gaps
- staffing gaps
- unresolved warnings

Readiness should not be built as a separate checklist until the underlying data is reliable.

---

## Deferred Areas

The app should not build everything at once.

Deferred areas include:

- accommodation
- site planning
- equipment
- food and catering
- transport and logistics
- finance
- forms
- communications
- documents
- compliance
- incident and welfare logging
- lessons learned
- online multi-user deployment
- export/import/archive implementation

These should come later.

---

## Current Priority

The current priority is to make the People, Sections and OSM workflow safe enough to trust with real camp data.

Next priorities:

1. Safer section-level OSM member imports
2. Safer section-level OSM attendance imports
3. Attendance summaries and filters
4. Import review improvements
5. Bulk move people between sections