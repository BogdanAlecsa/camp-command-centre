# Templates

Templates reduce repeated work between camps.

Many camps share the same planning structure, even when the people attending are different.

Templates should help the organiser reuse good planning without copying personal data by mistake.

---

## Core Rule

Templates are copied into camps.

They are never live-linked.

    Template
        ↓ copy
    Camp record

After a template is copied into a camp, the camp has its own independent copy.

Changing the template later should not unexpectedly change an existing camp.

Changing an existing camp should not unexpectedly change the original template.

---

## Current Status

Template support is mostly deferred.

The current app already has reusable-looking structures, but not a full template system yet.

Current reusable foundations include:

- task phases
- task categories
- activities
- programme structure
- teams
- risk assessment structures
- printable outputs

The next priority is still the People, Sections and OSM workflow.

Templates should not be built until the current MVP core is safer.

---

## Template Types

Future template types may include:

- Task Templates
- Activity Templates
- Programme Templates
- Risk Assessment Templates
- Team Templates
- Camp Templates
- Form Templates later
- Communication Templates later
- Readiness Templates later

---

## Camp Templates

A Camp Template is a reusable structure for a future camp.

A camp template may include:

- activities
- programme structure
- tasks
- task categories
- task phases
- risk assessment templates
- teams / group structures
- settings

A camp template should help create a new camp quickly.

Example uses:

- indoor sleepover template
- campsite camp template
- family camp template
- group camp template
- expedition template
- weekend camp template

---

## What Camp Templates Must Exclude

Camp templates must not contain personal data.

A camp template must exclude:

- people
- contact details
- emergency contacts
- medical information
- allergy information
- medication information
- dietary information
- attendance records
- welfare or incident notes

Templates are for planning structure, not for copying personal information.

---

## Task Templates

Task templates should allow common task sets to be reused.

Examples:

- book venue
- confirm permit holder
- prepare programme
- send joining instructions
- check medical information
- prepare risk assessments
- print leader packs
- pack equipment
- return equipment
- close down camp

Task templates may include:

- title
- description
- category
- phase
- priority
- suggested due timing
- checklist items later

When copied into a camp, task templates become normal camp tasks.

---

## Task Phase and Category Templates

The app already uses task phases and task categories.

These are useful template-like structures.

Default phases may include:

- Early Planning
- Preparation
- Final Week
- Camp Setup
- During Camp
- Pack Down
- After Camp

Default categories may include:

- Venue
- People & Forms
- Programme
- Equipment
- Food
- Transport
- Documents
- Safety / Risk
- Communications
- Finance
- General

Future camp templates should be able to include customised phases and categories.

---

## Activity Templates

Activity templates should allow common activities to be reused.

An activity template may include:

- activity name
- description
- default duration
- default location type
- equipment notes
- risk notes
- wet weather alternative
- badge links
- suggested staffing

When copied into a camp, the activity becomes a normal camp activity and can be edited.

---

## Programme Templates

Programme templates should allow reusable programme structures.

Examples:

- Friday evening arrival pattern
- Saturday rotation day
- Sunday pack-down pattern
- indoor sleepover programme
- Cub camp programme
- Scout camp programme
- family camp programme

Programme templates may include:

- programme sessions
- relative day/time structure
- session types
- activity slots
- meal slots
- setup/pack-down slots
- rotation blocks
- leader/admin slots

Programme templates should not include real people as leads.

They may include placeholder roles such as:

- Activity Lead
- Camp Leader
- First Aider
- Kitchen Team
- Duty Team

---

## Risk Assessment Templates

Risk assessment templates should help reuse common risk structures.

Examples:

- campfire
- cooking
- wide game
- hike
- water activity
- tool use
- campsite hazards
- indoor sleepover risks

Risk assessment templates may include:

- hazards
- who is at risk
- control measures
- review notes
- suggested residual risk notes

When copied into a camp or activity, the risk assessment must be reviewed for that specific context.

Important note:

The app helps organise risk assessment information.

It does not replace official Scouts approval processes.

---

## Team Templates

Team templates should help create common camp groups.

Examples:

- leader team
- kitchen team
- first aid team
- setup team
- pack-down team
- activity groups
- duty teams
- tent groups later

Team templates should define structure only.

They should not include real people unless copied inside a specific camp.

---

## Form Templates

Form templates are deferred.

Future form templates may include:

- medical update form
- consent form
- emergency contact confirmation
- travel permission form
- activity permission form
- dietary update form

Important principle:

Form responses should become structured database records.

They should not just be uploaded PDFs.

---

## Communication Templates

Communication templates are deferred.

Future communication templates may include:

- invitation
- joining instructions
- payment reminder
- missing information reminder
- leader briefing
- helper task message
- final information email

Communication templates should support merge fields later, such as camp name, dates, venue and response deadlines.

---

## Readiness Templates

Readiness templates are deferred.

A readiness template may define checks appropriate for a camp type.

Examples:

- indoor sleepover readiness
- greenfield camp readiness
- campsite camp readiness
- expedition readiness

Readiness templates should build on real app data.

They should not become separate manual checklists unless needed.

---

## Template Export

Future template export belongs to the deferred Export / Import / Archive system.

Possible future file type:

- .ccctemplate

A .ccctemplate file should contain reusable planning structure only.

It must not include personal data.

---

## Template Import

Future template import should allow a user to bring a reusable camp template into another installation.

Import should show a preview before applying.

Template import should explain what will be created, such as:

- tasks
- phases
- categories
- activities
- programme sessions
- risk templates
- team structures

It should not create people.

---

## Relationship to Archives and Backups

Templates are different from archives and backups.

## Template

Reusable planning structure.

No personal data.

## Archive

A completed camp record for reference.

May include some personal data depending on archive options.

## Backup

Full application backup for disaster recovery.

May include everything.

These must not be confused.

---

## Current Priority

Do not build the template system yet.

Current priorities remain:

1. Safer section-level OSM member imports
2. Safer section-level OSM attendance imports
3. Attendance summaries and filters
4. Import review improvements
5. Bulk move people between sections

Templates become more valuable after the core MVP workflow is stable.

---

## First Template Features to Build Later

When template work begins, start simple.

Suggested order:

1. Task template sets
2. Activity templates
3. Programme templates
4. Risk assessment templates
5. Full camp templates
6. Template export/import

Avoid starting with the full template/archive/backup system.

Build from practical repeated camp planning needs.

---

## Summary

Templates should reduce repeated work between camps.

They should copy useful planning structure.

They must not accidentally copy personal or sensitive data.

The template system is important, but it is not the next build priority.