# Technical Architecture

## Stack

Recommended MVP stack:

- Python
- FastAPI
- SQLAlchemy
- Alembic
- SQLite
- Jinja2
- Bootstrap
- HTMX later

## Architecture

```text
Browser
    ↓
FastAPI Routes
    ↓
Services
    ↓
Repositories
    ↓
SQLAlchemy
    ↓
SQLite / PostgreSQL
```

## Critical Rules

- routes stay thin
- business logic lives in services
- reports are HTML-first
- templates are copied, never live-linked
- workflow drives UI
- every major feature should work offline
