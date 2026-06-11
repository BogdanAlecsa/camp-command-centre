# Tests

Initial test priorities:

1. Programme rotation engine
2. Universal import wizard
3. Readiness engine
4. Work pack generation
5. Export generation

## Programme print route smoke test

Programme print routes are high-risk because template/context mistakes can produce 500 errors.

Use this smoke test before and after any programme printable change.

Terminal 1:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Terminal 2:

```bash
python scripts/smoke_programme_print_routes.py
```

Optional:

```bash
python scripts/smoke_programme_print_routes.py --camp-id 3
```

The script checks:

- full programme
- group programmes
- activity leader schedules
- leader programme
- leader location board
- session roll call, when a session exists

It fails if any route returns a non-200 response or does not render HTML.
