# Technical Architecture

Camp Command Centre is a local-first Python web application.

The current architecture is designed to run locally or in GitHub Codespaces, while keeping open the possibility of future online deployment.

---

## Current Status

The app is now a working early MVP.

It is no longer just a starter FastAPI skeleton.

Current implemented areas include:

- camps
- people
- sections
- teams
- tasks
- activities
- programme
- risk assessments
- OSM member import
- OSM attendance import groundwork
- printable outputs

The architecture is still simple, which is appropriate for the current stage.

---

## Current Technology Stack

Current stack:

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Jinja2 templates
- plain CSS
- simple JavaScript where useful
- GitHub Codespaces for development

This is suitable for a local-first MVP.

---

## Local-First Principle

The MVP should run on a personal computer without needing a hosted server.

The user should be able to run:

    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Then open the app in a browser.

Local-first is important because:

- it avoids early hosting complexity
- it supports offline/local use
- it keeps development simple
- it avoids premature multi-user design
- it allows fast iteration

---

## Codespaces Development

The app must work in GitHub Codespaces.

This allows development from a locked-down work laptop without installing software locally.

Codespaces should support:

- running the FastAPI app
- previewing the browser UI
- editing code
- committing changes
- testing migrations/schema updates
- using SQLite locally in the workspace

---

## Application Structure

The current broad structure is:

    app/
      main.py
      database.py
      models/
      routes/
      services/
      templates/
      static/

    docs/
    tests/
    requirements.txt
    README.md

The app currently still has a lot of route logic in `main.py`.

That has been acceptable for rapid MVP development, but some areas should be split into route/service modules as the app grows.

---

## Current Models

Current model areas include:

- Camp
- Person
- Section
- Team
- Team Membership
- Task
- Task Assignment
- Task Phase
- Task Category
- Activity
- Programme Session
- Programme Session Staff
- Camp Risk Assessment
- Camp Risk Control
- Activity Risk Assessment
- Activity Risk Control

The model structure is now strong enough to support the Phase 1 MVP.

---

## Database

The current database is SQLite.

SQLite is suitable for the local-first MVP because:

- it is simple
- it needs no separate database server
- it works in Codespaces
- it works locally
- it is easy to back up as a single file

Future online deployment may require PostgreSQL.

Do not move to PostgreSQL until there is a real need.

---

## Schema Updates

During MVP development, schema changes are currently handled with a lightweight SQLite-safe schema patching approach.

The app uses `create_all()` for missing tables and a small helper to add optional columns where needed.

This is acceptable for the current early MVP.

Future improvement:

- introduce Alembic migrations
- create formal migration history
- make upgrades safer for real user data

Alembic should be added before the app is used heavily with important long-term data.

---

## Routes

Routes currently cover:

- camps
- people
- sections
- teams
- tasks
- activities
- programme
- risk assessments
- OSM imports
- print views

The Programme module has already been moved into a separate route module.

Future route cleanup should move more large areas out of `main.py`.

Suggested future route modules:

- `routes/camps.py`
- `routes/people.py`
- `routes/sections.py`
- `routes/teams.py`
- `routes/tasks.py`
- `routes/activities.py`
- `routes/risk_assessments.py`
- `routes/imports.py`
- `routes/exports.py`

Do this gradually, not as a disruptive rewrite.

---

## Services

Service modules should contain reusable business logic.

Current/future services may include:

- OSM member import service
- OSM attendance import service
- task service
- programme service
- risk assessment service
- export service
- template service
- readiness service later

The OSM event attendance parser has already started moving in this direction.

More import parsing logic should move out of `main.py` over time.

---

## Templates

The app uses Jinja2 templates.

Templates currently support:

- normal HTML screens
- forms
- list/detail/edit pages
- import preview pages
- printable outputs

Template design should stay simple and readable.

Avoid introducing a heavy frontend framework too early.

The current app does not need React/Vue/etc.

---

## Static Files

Static files include:

- CSS
- small JavaScript
- images if needed later

JavaScript should be used where it improves usability, such as:

- showing selected upload file names
- enabling/disabling preview buttons
- simple UI toggles
- collapsible sections

Do not move core app logic into JavaScript.

---

## Import Architecture

Imports are becoming an important part of the app.

Current import types:

- OSM member export
- OSM event attendance export

Import principles:

- upload file
- parse file
- preview results
- show matching/action information
- apply selected rows
- protect existing manual data by default
- show result summary

Future import architecture should be section-aware.

The safest normal workflow is:

- open section block
- choose import action for that section
- upload file
- preview
- apply

This avoids accidental imports into the wrong section.

---

## OSM Member Import

OSM member import currently supports:

- person-level update
- bulk preview
- bulk apply
- updating existing people
- replacing provisional people
- creating new people
- importing contact and health-related fields
- storing section unit
- suggesting person type from unit names

Future technical improvements:

- move parser fully into service module
- improve row action calculation
- improve duplicate-name handling
- improve result summaries
- add stronger tests around sample OSM files

---

## OSM Event Attendance Import

OSM event attendance import currently has groundwork.

It maps:

- Yes to Attending
- No to Not attending
- Invited to Invited
- blank to No response

Future technical improvements:

- finish section-level routes
- improve preview/apply workflow
- test with real OSM event exports
- add attendance summaries by section
- ensure it only updates attendance fields

---

## Print Architecture

Print outputs currently use HTML print views.

This is suitable for the MVP.

Current print outputs include:

- task sheets
- team work packs
- programme outputs
- risk assessment outputs

Future improvements:

- joined-up camp file
- parent pack
- leader pack
- emergency/contact list
- print styling improvements
- possibly PDF export later

Do not introduce complex PDF tooling until the HTML print views are stable.

---

## Security and Sensitive Data

The app may store sensitive information, including:

- contact details
- emergency contacts
- allergies
- medication
- medical notes
- dietary requirements

Current MVP is local-first, so the immediate security model is simple.

Future work should consider:

- database location
- backup safety
- export safety
- user permissions
- audit trails
- encryption for archive/backup files
- sensitive fields excluded from templates

Sensitive data should not be included in reusable templates.

Sensitive archive fields should be off by default.

---

## Authentication and Permissions

Full authentication and permissions are deferred.

Current MVP assumes a trusted local organiser.

Future versions may include:

- login
- camp-specific access
- role-based permissions
- read-only access
- helper access
- parent/carer form links

Do not build this yet.

It should wait until the local-first MVP is stable.

---

## Future Online Deployment

The architecture should not block future online deployment.

Possible future deployment options:

- local PC
- Raspberry Pi
- hosted cloud app
- VPS
- PostgreSQL-backed deployment

Online deployment will require more work around:

- authentication
- permissions
- database migrations
- backups
- security
- data protection
- multi-user concurrency

This is deferred.

---

## Testing

Testing should grow as the MVP stabilises.

Useful test areas:

- route smoke tests
- model creation tests
- OSM member parser tests
- OSM attendance parser tests
- import apply behaviour
- task assignment behaviour
- programme route tests
- risk assessment route tests

OSM import tests are especially important because imports can change many records at once.

---

## Code Organisation Priorities

Near-term technical priorities:

1. Keep current app working
2. Avoid regressions
3. Move OSM import actions into section-specific workflows
4. Improve import review/action logic
5. Add tests for import parsing and apply behaviour
6. Gradually move large route blocks out of `main.py`
7. Add formal migrations later

Do not do a large architecture rewrite now.

---

## Deferred Export / Import / Archive System

A future export/import/archive system is planned.

Future file types may include:

- .ccctemplate
- .cccarchive
- .cccbackup

Design principles:

- no user-facing JSON exports
- app-managed encryption
- sensitive fields off by default in archives
- templates exclude personal data
- backups support disaster recovery

This is not current build work.

---

## Current Technical Risk

The main current technical risks are:

- too much logic still in `main.py`
- import workflow needs better safety
- SQLite schema patching is temporary
- limited automated tests
- no formal migrations yet
- no backup/restore yet

These are manageable at this stage.

Do not overcorrect too early.

---

## Current Build Priority

The technical priority remains aligned with the product priority:

1. Safer section-level OSM member imports
2. Safer section-level OSM attendance imports
3. Attendance summaries and filters
4. Import review improvements
5. Bulk move people between sections

These improve real-world safety and usability without derailing the MVP.

---

## Summary

The current architecture is appropriate for an early local-first MVP.

The app has grown beyond the starter skeleton and now has real camp planning functionality.

The next technical work should harden the current workflows, especially People, Sections and OSM imports, before adding large new modules or doing major architecture rewrites.