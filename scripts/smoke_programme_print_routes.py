#!/usr/bin/env python3
"""Smoke-check programme print routes against a running local server.

This is deliberately lightweight:
- no pytest required
- no httpx required
- uses urllib and sqlite3 from the standard library
- reads the current local SQLite database to find a camp/session
- calls the running FastAPI server and fails if any print route returns 500

Usage:

    # Terminal 1
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

    # Terminal 2
    python scripts/smoke_programme_print_routes.py

Optional:

    python scripts/smoke_programme_print_routes.py --camp-id 3
    python scripts/smoke_programme_print_routes.py --base-url http://127.0.0.1:8000
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_DB_PATH = Path("data/camp_command_centre.sqlite")
DEFAULT_BASE_URL = "http://127.0.0.1:8000"


def normalise_base_url(value: str) -> str:
    return (value or DEFAULT_BASE_URL).rstrip("/")


def fetch_latest_camp_id(db_path: Path) -> int:
    if not db_path.exists():
        raise SystemExit(f"Database not found: {db_path}")

    with sqlite3.connect(db_path) as con:
        row = con.execute(
            """
            SELECT id
            FROM camp
            ORDER BY start_date DESC, id DESC
            LIMIT 1
            """
        ).fetchone()

    if row is None:
        raise SystemExit("No camp found in the database. Seed or create a camp first.")

    return int(row[0])


def fetch_first_session_id(db_path: Path, camp_id: int) -> int | None:
    with sqlite3.connect(db_path) as con:
        row = con.execute(
            """
            SELECT id
            FROM programme_session
            WHERE camp_id = ?
            ORDER BY session_date, start_time, id
            LIMIT 1
            """,
            (camp_id,),
        ).fetchone()

    if row is None:
        return None

    return int(row[0])


def check_route(base_url: str, route: str, timeout: float = 10.0) -> tuple[bool, str]:
    url = base_url + route
    request = Request(url, headers={"User-Agent": "camp-command-centre-smoke-test"})

    try:
        with urlopen(request, timeout=timeout) as response:
            status = response.status
            body = response.read(800).decode("utf-8", errors="replace")

    except HTTPError as exc:
        body = exc.read(1200).decode("utf-8", errors="replace")
        return False, f"{route} -> HTTP {exc.code}\n{body[:1200]}"

    except URLError as exc:
        return False, (
            f"{route} -> connection failed: {exc}\n"
            "Is the dev server running? Start it with:\n"
            "  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
        )

    except Exception as exc:
        return False, f"{route} -> unexpected error: {exc!r}"

    if status != 200:
        return False, f"{route} -> HTTP {status}"

    lowered = body.lower()

    if "<html" not in lowered and "<!doctype html" not in lowered:
        return False, f"{route} -> HTTP 200 but response did not look like HTML"

    return True, f"{route} -> OK"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH))
    parser.add_argument("--camp-id", type=int, default=None)
    parser.add_argument("--session-id", type=int, default=None)
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()

    base_url = normalise_base_url(args.base_url)
    db_path = Path(args.db)

    camp_id = args.camp_id if args.camp_id is not None else fetch_latest_camp_id(db_path)
    session_id = args.session_id if args.session_id is not None else fetch_first_session_id(db_path, camp_id)

    routes = [
        f"/camps/{camp_id}/programme/print/full",
        f"/camps/{camp_id}/programme/print/groups",
        f"/camps/{camp_id}/programme/print/activity-leaders",
        f"/camps/{camp_id}/programme/print/leader",
        f"/camps/{camp_id}/programme/print/leader-board",
    ]

    if session_id is not None:
        routes.append(f"/camps/{camp_id}/programme/{session_id}/print/roll-call")
    else:
        print("No programme session found; skipping session roll-call route.")

    print("Programme print smoke test")
    print(f"Base URL: {base_url}")
    print(f"Camp ID: {camp_id}")
    print(f"Session ID: {session_id if session_id is not None else 'none'}")
    print("")

    failures: list[str] = []

    for route in routes:
        ok, message = check_route(base_url, route, timeout=args.timeout)
        print(message)

        if not ok:
            failures.append(message)

    print("")

    if failures:
        print("FAILED programme print smoke test")
        print("")
        for failure in failures:
            print(failure)
            print("")
        return 1

    print("PASSED programme print smoke test")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
