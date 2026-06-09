from pathlib import Path

# Patch app/routes/presence.py
route_path = Path("app/routes/presence.py")
text = route_path.read_text(encoding="utf-8")

text = text.replace(
    "from datetime import datetime, time\nfrom pathlib import Path\n",
    "from datetime import datetime, time\nfrom pathlib import Path\nfrom urllib.parse import urlencode\n",
)

text = text.replace(
    "from fastapi import APIRouter, Depends, Request\n",
    "from fastapi import APIRouter, Depends, Form, Request\n",
)

text = text.replace(
    "from fastapi.responses import HTMLResponse\n",
    "from fastapi.responses import HTMLResponse, RedirectResponse\n",
)

helper = '''
def presence_redirect_url(camp_id: int, at_time: str | None = None):
    if at_time:
        return f"/camps/{camp_id}/presence?" + urlencode({"at_time": at_time})
    return f"/camps/{camp_id}/presence"


def parse_scope_ref(scope_ref: str):
    scope_type, _, raw_scope_id = (scope_ref or "").partition(":")
    scope_id = int(raw_scope_id) if raw_scope_id else None
    return scope_type, scope_id


def validate_presence_scope(db: Session, camp: Camp, scope_type: str, scope_id: int | None):
    if scope_type == SCOPE_CAMP:
        return None

    if scope_type == SCOPE_GROUP:
        return (
            db.query(ParticipatingGroup)
            .filter(ParticipatingGroup.id == scope_id, ParticipatingGroup.camp_id == camp.id)
            .first()
        )

    if scope_type == SCOPE_SECTION:
        return (
            db.query(Section)
            .filter(Section.id == scope_id, Section.camp_id == camp.id)
            .first()
        )

    if scope_type == SCOPE_PERSON:
        return (
            db.query(Person)
            .filter(Person.id == scope_id, Person.camp_id == camp.id)
            .first()
        )

    return None


@router.post("/camps/{camp_id}/presence/rules/add")
async def add_presence_rule(
    camp_id: int,
    scope_ref: str = Form(...),
    starts_at: str = Form(...),
    ends_at: str = Form(...),
    status: str = Form("Expected"),
    notes: str = Form(""),
    return_at_time: str = Form(""),
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return RedirectResponse(url="/camps", status_code=303)

    try:
        scope_type, scope_id = parse_scope_ref(scope_ref)
        clean_starts_at = datetime.fromisoformat(starts_at)
        clean_ends_at = datetime.fromisoformat(ends_at)
    except ValueError:
        return RedirectResponse(url=presence_redirect_url(camp.id, return_at_time), status_code=303)

    allowed_statuses = {"Expected", "Partial", "Not Attending", "Unknown"}
    clean_status = status if status in allowed_statuses else "Expected"

    if clean_starts_at >= clean_ends_at:
        return RedirectResponse(url=presence_redirect_url(camp.id, return_at_time), status_code=303)

    if scope_type != SCOPE_CAMP and validate_presence_scope(db, camp, scope_type, scope_id) is None:
        return RedirectResponse(url=presence_redirect_url(camp.id, return_at_time), status_code=303)

    db.add(
        PresenceWindow(
            camp_id=camp.id,
            scope_type=scope_type,
            scope_id=scope_id,
            starts_at=clean_starts_at,
            ends_at=clean_ends_at,
            status=clean_status,
            notes=notes.strip() or None,
        )
    )
    db.commit()

    return RedirectResponse(url=presence_redirect_url(camp.id, return_at_time), status_code=303)


@router.post("/camps/{camp_id}/presence/rules/{rule_id}/delete")
async def delete_presence_rule(
    camp_id: int,
    rule_id: int,
    return_at_time: str = Form(""),
    db: Session = Depends(get_db),
):
    rule = (
        db.query(PresenceWindow)
        .filter(PresenceWindow.id == rule_id, PresenceWindow.camp_id == camp_id)
        .first()
    )

    if rule:
        db.delete(rule)
        db.commit()

    return RedirectResponse(url=presence_redirect_url(camp_id, return_at_time), status_code=303)

'''

if "def presence_redirect_url" not in text:
    anchor = '@router.get("/camps/{camp_id}/presence", response_class=HTMLResponse)\n'
    if anchor not in text:
        raise SystemExit("Could not find presence route anchor.")
    text = text.replace(anchor, helper + "\n" + anchor, 1)

old_context = '''            "summary_types": summary_types,
            "present_responsible_adult_count": present_responsible_adult_count,
            "present_young_leader_count": present_young_leader_count,
            "present_young_person_count": present_young_person_count,
            "rule_rows": rule_rows,
            "format_dt": format_dt,
'''

new_context = '''            "summary_types": summary_types,
            "present_responsible_adult_count": present_responsible_adult_count,
            "present_young_leader_count": present_young_leader_count,
            "present_young_person_count": present_young_person_count,
            "rule_rows": rule_rows,
            "groups": groups,
            "sections": sections,
            "people": people,
            "group_lookup": group_lookup,
            "presence_statuses": ["Expected", "Partial", "Not Attending", "Unknown"],
            "rule_default_start_input": datetime.combine(camp.start_date, time(18, 0)).strftime("%Y-%m-%dT%H:%M"),
            "rule_default_end_input": datetime.combine(camp.end_date, time(14, 0)).strftime("%Y-%m-%dT%H:%M"),
            "format_dt": format_dt,
'''

if old_context not in text:
    raise SystemExit("Could not find presence template context block.")

text = text.replace(old_context, new_context, 1)

old_rule_append = '''        rule_rows.append(
            {
                "scope_label": scope_label,
                "window": format_window(window),
            }
        )
'''

new_rule_append = '''        rule_rows.append(
            {
                "rule_id": window.id,
                "scope_label": scope_label,
                "window": format_window(window),
            }
        )
'''

if old_rule_append not in text:
    raise SystemExit("Could not find rule_rows append block.")

text = text.replace(old_rule_append, new_rule_append, 1)

route_path.write_text(text, encoding="utf-8")


# Patch app/templates/presence/dashboard.html
template_path = Path("app/templates/presence/dashboard.html")
text = template_path.read_text(encoding="utf-8")

if ".presence-rule-grid" not in text:
    text = text.replace(
        "</style>",
        '''  .presence-rule-grid {
    display: grid;
    grid-template-columns: minmax(260px, 1.5fr) minmax(190px, 1fr) minmax(190px, 1fr) minmax(150px, .8fr);
    gap: .65rem;
    align-items: end;
  }

  .presence-rule-notes-row {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: .65rem;
    align-items: end;
    margin-top: .65rem;
  }

  .presence-rule-grid label,
  .presence-rule-notes-row label {
    margin: 0;
  }

  .presence-rule-grid input,
  .presence-rule-grid select,
  .presence-rule-notes-row input {
    margin: .25rem 0 0;
  }

  .presence-rule-actions {
    display: flex;
    gap: .4rem;
    flex-wrap: wrap;
  }
</style>''',
        1,
    )

start = text.find('<section class="card">\n  <h3>Presence rules</h3>')
if start == -1:
    raise SystemExit("Could not find Presence rules section.")

end = text.rfind("{% endblock %}")
if end == -1:
    raise SystemExit("Could not find endblock.")

new_rules_section = '''<section class="card">
  <h3>Presence rules</h3>
  <p class="muted">
    Rules cascade from camp → group → section → person. More specific rules override broader ones.
    Multiple rules at the same level allow split attendance windows.
  </p>

  <form method="post" action="/camps/{{ camp.id }}/presence/rules/add">
    <input type="hidden" name="return_at_time" value="{{ selected_at_input }}">

    <div class="presence-rule-grid">
      <div>
        <label for="scope_ref"><strong>Rule applies to</strong></label>
        <select id="scope_ref" name="scope_ref" required>
          <option value="camp:">Whole camp default</option>

          <optgroup label="Participating groups">
            {% for group in groups %}
              <option value="participating_group:{{ group.id }}">Group — {{ group.name }}</option>
            {% endfor %}
          </optgroup>

          <optgroup label="Sections">
            {% for section in sections %}
              {% set group = group_lookup.get(section.participating_group_id) if group_lookup is defined else None %}
              <option value="section:{{ section.id }}">Section — {{ group.name ~ " → " if group else "" }}{{ section.name }}</option>
            {% endfor %}
          </optgroup>

          <optgroup label="People">
            {% for person in people %}
              <option value="person:{{ person.id }}">Person — {{ person.first_name }} {{ person.last_name }} ({{ person.person_type }})</option>
            {% endfor %}
          </optgroup>
        </select>
      </div>

      <div>
        <label for="starts_at"><strong>Starts</strong></label>
        <input id="starts_at" name="starts_at" type="datetime-local" value="{{ rule_default_start_input }}" required>
      </div>

      <div>
        <label for="ends_at"><strong>Ends</strong></label>
        <input id="ends_at" name="ends_at" type="datetime-local" value="{{ rule_default_end_input }}" required>
      </div>

      <div>
        <label for="status"><strong>Status</strong></label>
        <select id="status" name="status">
          {% for status in presence_statuses %}
            <option value="{{ status }}">{{ status }}</option>
          {% endfor %}
        </select>
      </div>
    </div>

    <div class="presence-rule-notes-row">
      <div>
        <label for="notes"><strong>Notes</strong></label>
        <input id="notes" name="notes" placeholder="Late arrival, early departure, day helper, etc.">
      </div>
      <button type="submit">Add presence rule</button>
    </div>
  </form>

  {% if rule_rows %}
    <table>
      <thead>
        <tr>
          <th>Scope</th>
          <th>Status</th>
          <th>Window</th>
          <th>Notes</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {% for row in rule_rows %}
          <tr>
            <td><strong>{{ row.scope_label }}</strong></td>
            <td>{{ row.window.status }}</td>
            <td>{{ format_dt(row.window.starts_at) }} → {{ format_dt(row.window.ends_at) }}</td>
            <td>{{ row.window.notes or "" }}</td>
            <td>
              <form method="post" action="/camps/{{ camp.id }}/presence/rules/{{ row.rule_id }}/delete" onsubmit="return confirm('Delete this presence rule?');">
                <input type="hidden" name="return_at_time" value="{{ selected_at_input }}">
                <button class="secondary small" type="submit">Delete</button>
              </form>
            </td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
  {% else %}
    <p>No presence rules have been added yet. The page is using the camp date fallback.</p>
  {% endif %}
</section>

'''

text = text[:start] + new_rules_section + text[end:]

template_path.write_text(text, encoding="utf-8")

print("Added Presence rules editor.")
