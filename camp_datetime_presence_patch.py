from pathlib import Path

# ---------------------------------------------------------------------
# Camp model: add start_time / end_time
# ---------------------------------------------------------------------
path = Path("app/models/camp.py")
text = path.read_text(encoding="utf-8")

text = text.replace(
    "from datetime import date, datetime\n",
    "from datetime import date, datetime, time\n",
)

text = text.replace(
    "from sqlalchemy import Date, DateTime, Integer, String, Text\n",
    "from sqlalchemy import Date, DateTime, Integer, String, Text, Time\n",
)

old = '''    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
'''

new = '''    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    start_time: Mapped[time] = mapped_column(Time, nullable=False, default=time(18, 0))

    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False, default=time(14, 0))
'''

if "start_time" not in text:
    if old not in text:
        raise SystemExit("Could not find Camp start/end date fields.")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------
# Main app: import time/datetime, PresenceWindow, schema columns, camp default rule
# ---------------------------------------------------------------------
path = Path("app/main.py")
text = path.read_text(encoding="utf-8")

text = text.replace(
    "from datetime import date\n",
    "from datetime import date, datetime, time\n",
)

if "PresenceWindow" not in text:
    text = text.replace(
        "ActivityRiskAssessment, ActivityRiskControl",
        "ActivityRiskAssessment, ActivityRiskControl, PresenceWindow",
        1,
    )

old_schema = '''            ("section", "participating_group_id", "INTEGER"),
            ("activity", "badge_notes", "TEXT"),
'''

new_schema = '''            ("camp", "start_time", "TIME DEFAULT '18:00:00'"),
            ("camp", "end_time", "TIME DEFAULT '14:00:00'"),
            ("section", "participating_group_id", "INTEGER"),
            ("activity", "badge_notes", "TEXT"),
'''

if '("camp", "start_time"' not in text:
    if old_schema not in text:
        raise SystemExit("Could not find optional schema column list anchor.")
    text = text.replace(old_schema, new_schema, 1)

helper_anchor = '''def get_latest_camp(db: Session):
    return db.query(Camp).order_by(Camp.start_date.desc()).first()


def parse_optional_date(value: str):
'''

helper = '''def get_latest_camp(db: Session):
    return db.query(Camp).order_by(Camp.start_date.desc()).first()


def camp_start_datetime(camp: Camp):
    return datetime.combine(camp.start_date, camp.start_time or time(18, 0))


def camp_end_datetime(camp: Camp):
    return datetime.combine(camp.end_date, camp.end_time or time(14, 0))


def ensure_camp_default_presence_window(db: Session, camp: Camp):
    # Keep the camp-level default presence rule aligned with camp setup times.
    start_at = camp_start_datetime(camp)
    end_at = camp_end_datetime(camp)

    if end_at <= start_at:
        return None

    default_rule = (
        db.query(PresenceWindow)
        .filter(
            PresenceWindow.camp_id == camp.id,
            PresenceWindow.scope_type == "camp",
            PresenceWindow.scope_id.is_(None),
        )
        .order_by(PresenceWindow.id)
        .first()
    )

    if default_rule is None:
        default_rule = PresenceWindow(
            camp_id=camp.id,
            scope_type="camp",
            scope_id=None,
            starts_at=start_at,
            ends_at=end_at,
            status="Expected",
            notes="Camp default presence window from camp setup.",
        )
        db.add(default_rule)
    else:
        default_rule.starts_at = start_at
        default_rule.ends_at = end_at

        if not default_rule.status:
            default_rule.status = "Expected"

        if not default_rule.notes:
            default_rule.notes = "Camp default presence window from camp setup."

    db.commit()
    return default_rule


def parse_optional_date(value: str):
'''

if "def ensure_camp_default_presence_window" not in text:
    if helper_anchor not in text:
        raise SystemExit("Could not find helper insertion anchor.")
    text = text.replace(helper_anchor, helper, 1)

old_startup = '''            apply_default_task_phase_descriptions(db, camp)
            apply_default_task_category_descriptions(db, camp)
'''

new_startup = '''            apply_default_task_phase_descriptions(db, camp)
            apply_default_task_category_descriptions(db, camp)
            ensure_camp_default_presence_window(db, camp)
'''

startup_block = text.split("def on_startup", 1)[1].split("def get_latest_camp", 1)[0]
if "ensure_camp_default_presence_window(db, camp)" not in startup_block:
    text = text.replace(old_startup, new_startup, 1)

# create_camp signature
old_create_sig = '''    start_date: date = Form(...),
    end_date: date = Form(...),
    venue_name: str = Form(""),
'''

new_create_sig = '''    start_date: date = Form(...),
    start_time: time = Form(time(18, 0)),
    end_date: date = Form(...),
    end_time: time = Form(time(14, 0)),
    venue_name: str = Form(""),
'''

if old_create_sig in text:
    text = text.replace(old_create_sig, new_create_sig, 1)

# create validation
old_create_validation = '''    if end_date < start_date:
        return templates.TemplateResponse(
            "camps/new.html",
            {
                "request": request,
                "error": "The end date cannot be before the start date.",
            },
            status_code=400,
        )
'''

new_create_validation = '''    if datetime.combine(end_date, end_time) <= datetime.combine(start_date, start_time):
        return templates.TemplateResponse(
            "camps/new.html",
            {
                "request": request,
                "error": "The camp end date/time must be after the start date/time.",
            },
            status_code=400,
        )
'''

if old_create_validation in text:
    text = text.replace(old_create_validation, new_create_validation, 1)

# create model values - first occurrence only
old_create_values = '''        start_date=start_date,
        end_date=end_date,
'''

new_create_values = '''        start_date=start_date,
        start_time=start_time,
        end_date=end_date,
        end_time=end_time,
'''

if old_create_values in text:
    text = text.replace(old_create_values, new_create_values, 1)

old_create_after_defaults = '''    apply_default_task_phase_descriptions(db, camp)
    apply_default_task_category_descriptions(db, camp)

    return RedirectResponse(url=f"/camps/{camp.id}", status_code=303)
'''

new_create_after_defaults = '''    apply_default_task_phase_descriptions(db, camp)
    apply_default_task_category_descriptions(db, camp)
    ensure_camp_default_presence_window(db, camp)

    return RedirectResponse(url=f"/camps/{camp.id}", status_code=303)
'''

if old_create_after_defaults in text:
    text = text.replace(old_create_after_defaults, new_create_after_defaults, 1)

# update_camp signature
old_update_sig = '''    start_date: date = Form(...),
    end_date: date = Form(...),
    venue_name: str = Form(""),
'''

new_update_sig = '''    start_date: date = Form(...),
    start_time: time = Form(time(18, 0)),
    end_date: date = Form(...),
    end_time: time = Form(time(14, 0)),
    venue_name: str = Form(""),
'''

if old_update_sig in text:
    text = text.replace(old_update_sig, new_update_sig, 1)

# update validation
old_update_validation = '''    if end_date < start_date:
        return templates.TemplateResponse(
            "camps/edit.html",
            {
                "request": request,
                "camp": camp,
                "error": "The end date cannot be before the start date.",
            },
            status_code=400,
        )
'''

new_update_validation = '''    if datetime.combine(end_date, end_time) <= datetime.combine(start_date, start_time):
        return templates.TemplateResponse(
            "camps/edit.html",
            {
                "request": request,
                "camp": camp,
                "error": "The camp end date/time must be after the start date/time.",
            },
            status_code=400,
        )
'''

if old_update_validation in text:
    text = text.replace(old_update_validation, new_update_validation, 1)

old_update_values = '''    camp.start_date = start_date
    camp.end_date = end_date
'''

new_update_values = '''    camp.start_date = start_date
    camp.start_time = start_time
    camp.end_date = end_date
    camp.end_time = end_time
'''

if old_update_values in text:
    text = text.replace(old_update_values, new_update_values, 1)

old_update_commit = '''    db.commit()

    return RedirectResponse(url=f"/camps/{camp.id}", status_code=303)
'''

new_update_commit = '''    db.commit()
    ensure_camp_default_presence_window(db, camp)

    return RedirectResponse(url=f"/camps/{camp.id}", status_code=303)
'''

# Replace the update route commit block after "camp.notes =" to avoid touching create route.
update_route_start = text.find('@app.post("/camps/{camp_id}/edit")')
if update_route_start != -1:
    before = text[:update_route_start]
    after = text[update_route_start:]
    if "ensure_camp_default_presence_window(db, camp)" not in after.split("@app.get", 1)[0]:
        after = after.replace(old_update_commit, new_update_commit, 1)
    text = before + after

path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------
# Camp templates
# ---------------------------------------------------------------------
# New camp form
path = Path("app/templates/camps/new.html")
text = path.read_text(encoding="utf-8")

old = '''    <label for="start_date">Start Date</label>
    <input id="start_date" name="start_date" type="date" required>

    <label for="end_date">End Date</label>
    <input id="end_date" name="end_date" type="date" required>
'''

new = '''    <div class="grid">
      <div>
        <label for="start_date">Start Date</label>
        <input id="start_date" name="start_date" type="date" required>
      </div>

      <div>
        <label for="start_time">Start Time</label>
        <input id="start_time" name="start_time" type="time" required value="18:00">
      </div>

      <div>
        <label for="end_date">End Date</label>
        <input id="end_date" name="end_date" type="date" required>
      </div>

      <div>
        <label for="end_time">End Time</label>
        <input id="end_time" name="end_time" type="time" required value="14:00">
      </div>
    </div>
'''

if "start_time" not in text:
    if old not in text:
        raise SystemExit("Could not find new camp date inputs.")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")


# Edit camp form
path = Path("app/templates/camps/edit.html")
text = path.read_text(encoding="utf-8")

old = '''    <label for="start_date">Start Date</label>
    <input id="start_date" name="start_date" type="date" required value="{{ camp.start_date }}">

    <label for="end_date">End Date</label>
    <input id="end_date" name="end_date" type="date" required value="{{ camp.end_date }}">
'''

new = '''    <div class="grid">
      <div>
        <label for="start_date">Start Date</label>
        <input id="start_date" name="start_date" type="date" required value="{{ camp.start_date }}">
      </div>

      <div>
        <label for="start_time">Start Time</label>
        <input id="start_time" name="start_time" type="time" required value="{{ camp.start_time.strftime('%H:%M') if camp.start_time else '18:00' }}">
      </div>

      <div>
        <label for="end_date">End Date</label>
        <input id="end_date" name="end_date" type="date" required value="{{ camp.end_date }}">
      </div>

      <div>
        <label for="end_time">End Time</label>
        <input id="end_time" name="end_time" type="time" required value="{{ camp.end_time.strftime('%H:%M') if camp.end_time else '14:00' }}">
      </div>
    </div>
'''

if "start_time" not in text:
    if old not in text:
        raise SystemExit("Could not find edit camp date inputs.")
    text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")


# Detail page display + Presence button
path = Path("app/templates/camps/detail.html")
text = path.read_text(encoding="utf-8")

text = text.replace(
    '''    {{ camp.start_date }} to {{ camp.end_date }}
''',
    '''    {{ camp.start_date }} {{ camp.start_time.strftime("%H:%M") if camp.start_time else "" }} to {{ camp.end_date }} {{ camp.end_time.strftime("%H:%M") if camp.end_time else "" }}
''',
)

if 'href="/camps/{{ camp.id }}/presence"' not in text:
    text = text.replace(
        '''  <a class="button secondary" href="/camps/{{ camp.id }}/people">People</a>
''',
        '''  <a class="button secondary" href="/camps/{{ camp.id }}/people">People</a>
  <a class="button secondary" href="/camps/{{ camp.id }}/presence">Presence</a>
''',
        1,
    )

path.write_text(text, encoding="utf-8")


# Camps list display
path = Path("app/templates/camps/list.html")
text = path.read_text(encoding="utf-8")

text = text.replace(
    '''            <td>{{ camp.start_date }} to {{ camp.end_date }}</td>
''',
    '''            <td>{{ camp.start_date }} {{ camp.start_time.strftime("%H:%M") if camp.start_time else "" }} to {{ camp.end_date }} {{ camp.end_time.strftime("%H:%M") if camp.end_time else "" }}</td>
''',
)

path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------
# Presence seed: use camp setup times for camp default
# ---------------------------------------------------------------------
path = Path("scripts/seed_presence_windows.py")
if path.exists():
    text = path.read_text(encoding="utf-8")

    text = text.replace(
        '''        add_window(
            "camp",
            None,
            combine(day0, 18, 0),
            combine(day2, 14, 0),
            notes="Default camp presence window.",
        )
''',
        '''        add_window(
            "camp",
            None,
            datetime.combine(camp.start_date, camp.start_time or time(18, 0)),
            datetime.combine(camp.end_date, camp.end_time or time(14, 0)),
            notes="Default camp presence window from camp setup.",
        )
''',
    )

    path.write_text(text, encoding="utf-8")

print("Added camp start/end times and camp default presence sync.")
