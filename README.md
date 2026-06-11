# Camp Command Centre

Camp Command Centre is a local-first, browser-based camp planning and operations tool for Scout camps, sleepovers, residential events and other Nights Away activities.

It is designed to help Scout leaders answer five practical questions:

1. What are we doing?
2. Who is involved?
3. Who is responsible?
4. What have we forgotten?
5. Are we ready?

The app is currently being built as a Python/FastAPI MVP that can run locally or inside GitHub Codespaces.

---

## Current Project Status

Current phase:

**Phase 1 MVP — Core Camp Planning**

Current active area:

**Programme, people, presence-aware staffing and operational outputs**

The project has moved beyond the original clickable prototype. It now has working early-MVP functionality for:

- Camps
- People
- Sections
- Participating groups
- Teams
- Tasks and assignments
- Activities
- Programme sessions
- Presence windows
- Session staff
- Programme session backup plans
- Session headcounts and roll-call printables
- Risk assessments
- Printable task, programme and risk outputs
- OSM member import
- OSM event attendance import groundwork

The current priority is not to start large new modules. The current priority is to make the core camp workflow trustworthy enough for real camp planning.

---

## How To Run Locally / Codespaces

From the repository root:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Then open the forwarded browser URL.

Before committing changes, run:

```bash
python -m compileall app scripts
git status
```

---

## Current MVP Principle

The app should remain local-first and practical.

Short-term development should focus on:

- safer people and attendance data
- cleaner programme planning
- reliable print packs
- clear warnings and readiness signals
- avoiding duplicate hidden sources of truth

Large modules such as Food, Transport, Finance, Communications and full Compliance should remain deferred until the core data model is stable.

---

## Important Current Design Rules

### People and Attendance

People are camp-specific records.

People may be real attendees or provisional placeholders.

Attendance status is part of the planning workflow. A person can be:

- Provisional
- Invited
- Attending
- Not attending
- No response
- Unknown

Operational outputs should increasingly distinguish between candidate roster and confirmed attendance.

### Session Staff

Programme sessions use **Session Staff** for operational staffing.

Session Staff can include:

- Leaders
- Helpers
- Young Leaders
- Parent Helpers
- Visitors / observers

The old single **Lead Person** field is being retired. The source of truth for leads is now:

```text
ProgrammeSessionStaff.role == "Lead"
```

### Young Leaders

Young Leaders may help run sessions operationally.

For mandatory adult ratios, they must still be treated as young people and must not count as adult cover.

### Backup Activities

Backup plans are attached to programme sessions.

They can be linked to existing Activities or entered as a lightweight custom fallback.

They do not change the main timetable.

They should appear quietly in leader/internal outputs, not as main programme items.

### Ratios

Mandatory ratios should only apply to Nights Away / residential events.

The most useful check is usually at the separated supervision group/session level, not only campwide.

Ratio work is not yet implemented and needs a careful design pass.

---

## Documentation

Main documentation lives in:

```text
docs/
```

Start with:

```text
docs/00_Philosophy.md
docs/01_How_The_App_Works.md
docs/04_Programme_Planner.md
docs/12_Build_Roadmap.md
docs/13_Next_Steps.md
```
