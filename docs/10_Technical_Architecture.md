# Technical Architecture

Camp Command Centre is a local-first Python web application.

The current architecture is designed to run locally or in GitHub Codespaces, while keeping open the possibility of future online deployment.

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

## Run Command

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Application Structure

Current broad structure:

```text
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
```

Some route logic remains in `main.py`.

Programme-specific work is now in `app/routes/programme.py`.

As the app grows, more route/service separation will be needed.

---

## Current Models

Current model areas include:

- Camp
- Person
- Section
- Participating Group
- Presence Window
- Team
- Team Membership
- Task
- Task Assignment
- Task Phase
- Task Category
- Activity
- Programme Session
- Programme Session Staff
- Programme Session Backup
- Camp Risk Assessment
- Camp Risk Control
- Activity Risk Assessment
- Activity Risk Control

---

## Programme Route

`app/routes/programme.py` currently handles:

- programme list
- session detail
- session create/edit/delete
- rotations
- print routes
- session staff
- session backup plans
- session roll call
- presence-aware staff availability
- programme warnings

This route is becoming large.

Future refactor candidates:

- programme services
- presence services
- print context builders
- session staff service
- backup plan service
- warning/readiness service

---

## Templates

Templates are in:

```text
app/templates/
```

Programme templates are in:

```text
app/templates/programme/
```

Important programme templates include:

- list.html
- detail.html
- new.html
- edit.html
- print_full.html
- print_groups.html
- print_leader.html
- print_activity_leaders.html
- print_leader_board.html
- print_session_roll_call.html

Print templates should be changed carefully.

---

## Static Files and CSS

Most styling currently lives in templates/base CSS.

Some static CSS may also exist in:

```text
app/static/css/
```

Do not assume a named `static` route exists unless the app defines one.

Use existing static path conventions already present in the app.

---

## SQLite and Schema Changes

The app currently uses SQLite.

Some schema changes are handled through `Base.metadata.create_all()` and pragmatic schema helpers.

This is acceptable for early local MVP development, but it is not a long-term migration strategy.

Future recommendation:

- introduce Alembic, or
- create a small controlled migration layer

Before broader use, schema changes should become repeatable and testable.

---

## Testing

Testing is currently light.

Immediate technical need:

- route/template smoke tests
- print route smoke tests
- compile checks
- basic database setup tests
- import parser tests

The minimum pre-commit check is:

```bash
python -m compileall app scripts
```

But compile checks are not enough.

The print route regressions show that render tests are needed.

---

## Print Route Risk

Programme print routes are high-risk because a small template/context mismatch can break the whole page.

Future print changes should follow this process:

1. change one print route/template at a time
2. run compile check
3. open the route in browser
4. check server log for 500 errors
5. commit only after all print outputs load

---

## Future Online Deployment

Future online deployment is possible, but deferred.

Potential future changes:

- PostgreSQL
- user accounts
- role-based access
- hosted deployment
- backups
- audit trail
- concurrent editing
- better migration system

The MVP should not be forced into online complexity too early.
