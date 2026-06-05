from datetime import date
from pathlib import Path

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Camp, Person, Team, TeamMembership, Task, TaskAssignment

app = FastAPI(title="Camp Command Centre")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


def get_latest_camp(db: Session):
    return db.query(Camp).order_by(Camp.start_date.desc()).first()


def parse_optional_date(value: str):
    value = (value or "").strip()
    if not value:
        return None
    return date.fromisoformat(value)


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    current_camp = get_latest_camp(db)

    people_count = 0
    task_count = 0
    if current_camp:
        people_count = db.query(Person).filter(Person.camp_id == current_camp.id).count()
        task_count = db.query(Task).filter(Task.camp_id == current_camp.id).count()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "camp": current_camp,
            "people_count": people_count,
            "task_count": task_count,
            "programme_sessions": 0,
            "readiness": 0,
        },
    )


@app.get("/camps", response_class=HTMLResponse)
async def camp_list(request: Request, db: Session = Depends(get_db)):
    camps = db.query(Camp).order_by(Camp.start_date.desc()).all()

    return templates.TemplateResponse(
        "camps/list.html",
        {
            "request": request,
            "camps": camps,
        },
    )


@app.get("/camps/new", response_class=HTMLResponse)
async def new_camp_form(request: Request):
    return templates.TemplateResponse(
        "camps/new.html",
        {
            "request": request,
            "error": None,
        },
    )


@app.post("/camps/new")
async def create_camp(
    request: Request,
    name: str = Form(...),
    camp_type: str = Form("Campsite Camp"),
    start_date: date = Form(...),
    end_date: date = Form(...),
    venue_name: str = Form(""),
    camp_leader: str = Form(""),
    permit_holder: str = Form(""),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    if end_date < start_date:
        return templates.TemplateResponse(
            "camps/new.html",
            {
                "request": request,
                "error": "The end date cannot be before the start date.",
            },
            status_code=400,
        )

    camp = Camp(
        name=name.strip(),
        camp_type=camp_type,
        start_date=start_date,
        end_date=end_date,
        venue_name=venue_name.strip() or None,
        camp_leader=camp_leader.strip() or None,
        permit_holder=permit_holder.strip() or None,
        status="Planning",
        notes=notes.strip() or None,
    )

    db.add(camp)
    db.commit()
    db.refresh(camp)

    return RedirectResponse(url=f"/camps/{camp.id}", status_code=303)


@app.get("/camps/{camp_id}/edit", response_class=HTMLResponse)
async def edit_camp_form(request: Request, camp_id: int, db: Session = Depends(get_db)):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Camp not found.",
            },
            status_code=404,
        )

    return templates.TemplateResponse(
        "camps/edit.html",
        {
            "request": request,
            "camp": camp,
            "error": None,
        },
    )


@app.post("/camps/{camp_id}/edit")
async def update_camp(
    request: Request,
    camp_id: int,
    name: str = Form(...),
    camp_type: str = Form("Campsite Camp"),
    start_date: date = Form(...),
    end_date: date = Form(...),
    venue_name: str = Form(""),
    camp_leader: str = Form(""),
    permit_holder: str = Form(""),
    status: str = Form("Planning"),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Camp not found.",
            },
            status_code=404,
        )

    if end_date < start_date:
        return templates.TemplateResponse(
            "camps/edit.html",
            {
                "request": request,
                "camp": camp,
                "error": "The end date cannot be before the start date.",
            },
            status_code=400,
        )

    camp.name = name.strip()
    camp.camp_type = camp_type
    camp.start_date = start_date
    camp.end_date = end_date
    camp.venue_name = venue_name.strip() or None
    camp.camp_leader = camp_leader.strip() or None
    camp.permit_holder = permit_holder.strip() or None
    camp.status = status
    camp.notes = notes.strip() or None

    db.commit()

    return RedirectResponse(url=f"/camps/{camp.id}", status_code=303)


@app.get("/camps/{camp_id}", response_class=HTMLResponse)
async def camp_detail(request: Request, camp_id: int, db: Session = Depends(get_db)):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Camp not found.",
            },
            status_code=404,
        )

    people_count = db.query(Person).filter(Person.camp_id == camp.id).count()
    team_count = db.query(Team).filter(Team.camp_id == camp.id).count()
    task_count = db.query(Task).filter(Task.camp_id == camp.id).count()

    return templates.TemplateResponse(
        "camps/detail.html",
        {
            "request": request,
            "camp": camp,
            "people_count": people_count,
            "team_count": team_count,
            "task_count": task_count,
            "programme_sessions": 0,
            "readiness": 0,
        },
    )


@app.get("/people", response_class=HTMLResponse)
async def people_page(request: Request, db: Session = Depends(get_db)):
    camp = get_latest_camp(db)

    if camp is None:
        return templates.TemplateResponse("people.html", {"request": request})

    return RedirectResponse(url=f"/camps/{camp.id}/people", status_code=303)


@app.get("/camps/{camp_id}/people", response_class=HTMLResponse)
async def camp_people_list(request: Request, camp_id: int, db: Session = Depends(get_db)):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Camp not found.",
            },
            status_code=404,
        )

    people = (
        db.query(Person)
        .filter(Person.camp_id == camp.id)
        .order_by(Person.person_type, Person.last_name, Person.first_name)
        .all()
    )

    return templates.TemplateResponse(
        "people/list.html",
        {
            "request": request,
            "camp": camp,
            "people": people,
        },
    )


@app.get("/camps/{camp_id}/people/new", response_class=HTMLResponse)
async def new_person_form(request: Request, camp_id: int, db: Session = Depends(get_db)):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Camp not found.",
            },
            status_code=404,
        )

    return templates.TemplateResponse(
        "people/new.html",
        {
            "request": request,
            "camp": camp,
            "error": None,
        },
    )


@app.post("/camps/{camp_id}/people/new")
async def create_person(
    request: Request,
    camp_id: int,
    first_name: str = Form(...),
    last_name: str = Form(...),
    person_type: str = Form(...),
    email: str = Form(""),
    phone: str = Form(""),
    role_notes: str = Form(""),
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Camp not found.",
            },
            status_code=404,
        )

    if not first_name.strip() or not last_name.strip():
        return templates.TemplateResponse(
            "people/new.html",
            {
                "request": request,
                "camp": camp,
                "error": "First name and last name are required.",
            },
            status_code=400,
        )

    person = Person(
        camp_id=camp.id,
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        person_type=person_type,
        email=email.strip() or None,
        phone=phone.strip() or None,
        role_notes=role_notes.strip() or None,
    )

    db.add(person)
    db.commit()
    db.refresh(person)

    return RedirectResponse(url=f"/camps/{camp.id}/people/{person.id}", status_code=303)




@app.get("/camps/{camp_id}/people/{person_id}/edit", response_class=HTMLResponse)
async def edit_person_form(
    request: Request,
    camp_id: int,
    person_id: int,
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Camp not found.",
            },
            status_code=404,
        )

    person = (
        db.query(Person)
        .filter(Person.id == person_id, Person.camp_id == camp.id)
        .first()
    )

    if person is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Person not found.",
            },
            status_code=404,
        )

    return templates.TemplateResponse(
        "people/edit.html",
        {
            "request": request,
            "camp": camp,
            "person": person,
            "error": None,
        },
    )


@app.post("/camps/{camp_id}/people/{person_id}/edit")
async def update_person(
    request: Request,
    camp_id: int,
    person_id: int,
    first_name: str = Form(...),
    last_name: str = Form(...),
    person_type: str = Form(...),
    email: str = Form(""),
    phone: str = Form(""),
    role_notes: str = Form(""),
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Camp not found.",
            },
            status_code=404,
        )

    person = (
        db.query(Person)
        .filter(Person.id == person_id, Person.camp_id == camp.id)
        .first()
    )

    if person is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Person not found.",
            },
            status_code=404,
        )

    if not first_name.strip() or not last_name.strip():
        return templates.TemplateResponse(
            "people/edit.html",
            {
                "request": request,
                "camp": camp,
                "person": person,
                "error": "First name and last name are required.",
            },
            status_code=400,
        )

    person.first_name = first_name.strip()
    person.last_name = last_name.strip()
    person.person_type = person_type
    person.email = email.strip() or None
    person.phone = phone.strip() or None
    person.role_notes = role_notes.strip() or None

    db.commit()

    return RedirectResponse(url=f"/camps/{camp.id}/people/{person.id}", status_code=303)


@app.get("/camps/{camp_id}/people/{person_id}", response_class=HTMLResponse)
async def person_detail(
    request: Request,
    camp_id: int,
    person_id: int,
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Camp not found.",
            },
            status_code=404,
        )

    person = (
        db.query(Person)
        .filter(Person.id == person_id, Person.camp_id == camp.id)
        .first()
    )

    if person is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Person not found.",
            },
            status_code=404,
        )

    return templates.TemplateResponse(
        "people/detail.html",
        {
            "request": request,
            "camp": camp,
            "person": person,
        },
    )




@app.get("/teams", response_class=HTMLResponse)
async def teams_page(request: Request, db: Session = Depends(get_db)):
    camp = get_latest_camp(db)

    if camp is None:
        return templates.TemplateResponse("teams/no_camp.html", {"request": request})

    return RedirectResponse(url=f"/camps/{camp.id}/teams", status_code=303)


@app.get("/camps/{camp_id}/teams", response_class=HTMLResponse)
async def camp_team_list(request: Request, camp_id: int, db: Session = Depends(get_db)):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Camp not found.",
            },
            status_code=404,
        )

    teams = (
        db.query(Team)
        .filter(Team.camp_id == camp.id)
        .order_by(Team.team_type, Team.name)
        .all()
    )

    team_member_counts = {}
    for team in teams:
        team_member_counts[team.id] = (
            db.query(TeamMembership)
            .filter(TeamMembership.team_id == team.id, TeamMembership.camp_id == camp.id)
            .count()
        )

    return templates.TemplateResponse(
        "teams/list.html",
        {
            "request": request,
            "camp": camp,
            "teams": teams,
            "team_member_counts": team_member_counts,
        },
    )


@app.get("/camps/{camp_id}/teams/new", response_class=HTMLResponse)
async def new_team_form(request: Request, camp_id: int, db: Session = Depends(get_db)):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Camp not found.",
            },
            status_code=404,
        )

    return templates.TemplateResponse(
        "teams/new.html",
        {
            "request": request,
            "camp": camp,
            "error": None,
        },
    )


@app.post("/camps/{camp_id}/teams/new")
async def create_team(
    request: Request,
    camp_id: int,
    name: str = Form(...),
    team_type: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Camp not found.",
            },
            status_code=404,
        )

    if not name.strip():
        return templates.TemplateResponse(
            "teams/new.html",
            {
                "request": request,
                "camp": camp,
                "error": "Team name is required.",
            },
            status_code=400,
        )

    team = Team(
        camp_id=camp.id,
        name=name.strip(),
        team_type=team_type,
        description=description.strip() or None,
    )

    db.add(team)
    db.commit()
    db.refresh(team)

    return RedirectResponse(url=f"/camps/{camp.id}/teams/{team.id}", status_code=303)




@app.get("/camps/{camp_id}/teams/{team_id}/edit", response_class=HTMLResponse)
async def edit_team_form(
    request: Request,
    camp_id: int,
    team_id: int,
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Camp not found.",
            },
            status_code=404,
        )

    team = (
        db.query(Team)
        .filter(Team.id == team_id, Team.camp_id == camp.id)
        .first()
    )

    if team is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Team not found.",
            },
            status_code=404,
        )

    return templates.TemplateResponse(
        "teams/edit.html",
        {
            "request": request,
            "camp": camp,
            "team": team,
            "error": None,
        },
    )


@app.post("/camps/{camp_id}/teams/{team_id}/edit")
async def update_team(
    request: Request,
    camp_id: int,
    team_id: int,
    name: str = Form(...),
    team_type: str = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Camp not found.",
            },
            status_code=404,
        )

    team = (
        db.query(Team)
        .filter(Team.id == team_id, Team.camp_id == camp.id)
        .first()
    )

    if team is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Team not found.",
            },
            status_code=404,
        )

    if not name.strip():
        return templates.TemplateResponse(
            "teams/edit.html",
            {
                "request": request,
                "camp": camp,
                "team": team,
                "error": "Team name is required.",
            },
            status_code=400,
        )

    team.name = name.strip()
    team.team_type = team_type
    team.description = description.strip() or None

    db.commit()

    return RedirectResponse(url=f"/camps/{camp.id}/teams/{team.id}", status_code=303)


@app.get("/camps/{camp_id}/teams/{team_id}", response_class=HTMLResponse)
async def team_detail(
    request: Request,
    camp_id: int,
    team_id: int,
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Camp not found.",
            },
            status_code=404,
        )

    team = (
        db.query(Team)
        .filter(Team.id == team_id, Team.camp_id == camp.id)
        .first()
    )

    if team is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Team not found.",
            },
            status_code=404,
        )

    memberships = (
        db.query(TeamMembership, Person)
        .join(Person, Person.id == TeamMembership.person_id)
        .filter(TeamMembership.team_id == team.id, TeamMembership.camp_id == camp.id)
        .order_by(Person.last_name, Person.first_name)
        .all()
    )

    return templates.TemplateResponse(
        "teams/detail.html",
        {
            "request": request,
            "camp": camp,
            "team": team,
            "memberships": memberships,
        },
    )


@app.get("/camps/{camp_id}/teams/{team_id}/members/new", response_class=HTMLResponse)
async def add_team_member_form(
    request: Request,
    camp_id: int,
    team_id: int,
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Camp not found.",
            },
            status_code=404,
        )

    team = (
        db.query(Team)
        .filter(Team.id == team_id, Team.camp_id == camp.id)
        .first()
    )

    if team is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Team not found.",
            },
            status_code=404,
        )

    existing_person_ids = [
        row.person_id
        for row in db.query(TeamMembership)
        .filter(TeamMembership.team_id == team.id, TeamMembership.camp_id == camp.id)
        .all()
    ]

    people_query = db.query(Person).filter(Person.camp_id == camp.id)

    if existing_person_ids:
        people_query = people_query.filter(Person.id.notin_(existing_person_ids))

    available_people = people_query.order_by(Person.person_type, Person.last_name, Person.first_name).all()

    return templates.TemplateResponse(
        "teams/add_member.html",
        {
            "request": request,
            "camp": camp,
            "team": team,
            "available_people": available_people,
            "error": None,
        },
    )


@app.post("/camps/{camp_id}/teams/{team_id}/members/new")
async def add_team_member(
    request: Request,
    camp_id: int,
    team_id: int,
    person_id: int = Form(...),
    role_in_team: str = Form(""),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Camp not found.",
            },
            status_code=404,
        )

    team = (
        db.query(Team)
        .filter(Team.id == team_id, Team.camp_id == camp.id)
        .first()
    )

    person = (
        db.query(Person)
        .filter(Person.id == person_id, Person.camp_id == camp.id)
        .first()
    )

    if team is None or person is None:
        return templates.TemplateResponse(
            "not_found.html",
            {
                "request": request,
                "message": "Team or person not found.",
            },
            status_code=404,
        )

    existing = (
        db.query(TeamMembership)
        .filter(
            TeamMembership.team_id == team.id,
            TeamMembership.person_id == person.id,
            TeamMembership.camp_id == camp.id,
        )
        .first()
    )

    if existing is None:
        membership = TeamMembership(
            camp_id=camp.id,
            team_id=team.id,
            person_id=person.id,
            role_in_team=role_in_team.strip() or None,
            notes=notes.strip() or None,
        )
        db.add(membership)
        db.commit()

    return RedirectResponse(url=f"/camps/{camp.id}/teams/{team.id}", status_code=303)


@app.post("/camps/{camp_id}/teams/{team_id}/members/{membership_id}/remove")
async def remove_team_member(
    camp_id: int,
    team_id: int,
    membership_id: int,
    db: Session = Depends(get_db),
):
    membership = (
        db.query(TeamMembership)
        .filter(
            TeamMembership.id == membership_id,
            TeamMembership.camp_id == camp_id,
            TeamMembership.team_id == team_id,
        )
        .first()
    )

    if membership is not None:
        db.delete(membership)
        db.commit()

    return RedirectResponse(url=f"/camps/{camp_id}/teams/{team_id}", status_code=303)


@app.get("/programme", response_class=HTMLResponse)
async def programme_page(request: Request):
    return templates.TemplateResponse("programme.html", {"request": request})


@app.get("/tasks", response_class=HTMLResponse)
async def tasks_page(request: Request, db: Session = Depends(get_db)):
    camp = get_latest_camp(db)

    if camp is None:
        return templates.TemplateResponse("tasks/no_camp.html", {"request": request})

    return RedirectResponse(url=f"/camps/{camp.id}/tasks", status_code=303)


@app.get("/camps/{camp_id}/tasks", response_class=HTMLResponse)
async def camp_task_list(request: Request, camp_id: int, db: Session = Depends(get_db)):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Camp not found."},
            status_code=404,
        )

    tasks = (
        db.query(Task)
        .filter(Task.camp_id == camp.id)
        .order_by(Task.status, Task.priority, Task.due_date, Task.title)
        .all()
    )

    assignment_counts = {}
    for task in tasks:
        assignment_counts[task.id] = (
            db.query(TaskAssignment)
            .filter(TaskAssignment.task_id == task.id, TaskAssignment.camp_id == camp.id)
            .count()
        )

    return templates.TemplateResponse(
        "tasks/list.html",
        {
            "request": request,
            "camp": camp,
            "tasks": tasks,
            "assignment_counts": assignment_counts,
        },
    )


@app.get("/camps/{camp_id}/tasks/new", response_class=HTMLResponse)
async def new_task_form(request: Request, camp_id: int, db: Session = Depends(get_db)):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Camp not found."},
            status_code=404,
        )

    return templates.TemplateResponse(
        "tasks/new.html",
        {
            "request": request,
            "camp": camp,
            "error": None,
        },
    )


@app.post("/camps/{camp_id}/tasks/new")
async def create_task(
    request: Request,
    camp_id: int,
    title: str = Form(...),
    description: str = Form(""),
    category: str = Form(""),
    phase: str = Form(""),
    priority: str = Form("Normal"),
    status: str = Form("Planned"),
    due_date: str = Form(""),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Camp not found."},
            status_code=404,
        )

    if not title.strip():
        return templates.TemplateResponse(
            "tasks/new.html",
            {
                "request": request,
                "camp": camp,
                "error": "Task title is required.",
            },
            status_code=400,
        )

    task = Task(
        camp_id=camp.id,
        title=title.strip(),
        description=description.strip() or None,
        category=category.strip() or None,
        phase=phase.strip() or None,
        priority=priority,
        status=status,
        due_date=parse_optional_date(due_date),
        notes=notes.strip() or None,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return RedirectResponse(url=f"/camps/{camp.id}/tasks/{task.id}", status_code=303)


@app.get("/camps/{camp_id}/tasks/{task_id}", response_class=HTMLResponse)
async def task_detail(
    request: Request,
    camp_id: int,
    task_id: int,
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Camp not found."},
            status_code=404,
        )

    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.camp_id == camp.id)
        .first()
    )

    if task is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Task not found."},
            status_code=404,
        )

    assignments = (
        db.query(TaskAssignment)
        .filter(TaskAssignment.task_id == task.id, TaskAssignment.camp_id == camp.id)
        .order_by(TaskAssignment.id)
        .all()
    )

    assignment_rows = []
    for assignment in assignments:
        assignee_label = "Unknown"
        assignee_type = ""

        if assignment.assigned_person_id:
            person = db.get(Person, assignment.assigned_person_id)
            if person:
                assignee_label = f"{person.first_name} {person.last_name}"
                assignee_type = person.person_type

        if assignment.assigned_team_id:
            team = db.get(Team, assignment.assigned_team_id)
            if team:
                assignee_label = team.name
                assignee_type = team.team_type

        assignment_rows.append(
            {
                "assignment": assignment,
                "assignee_label": assignee_label,
                "assignee_type": assignee_type,
            }
        )

    return templates.TemplateResponse(
        "tasks/detail.html",
        {
            "request": request,
            "camp": camp,
            "task": task,
            "assignment_rows": assignment_rows,
        },
    )


@app.get("/camps/{camp_id}/tasks/{task_id}/assignments/new", response_class=HTMLResponse)
async def new_task_assignment_form(
    request: Request,
    camp_id: int,
    task_id: int,
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Camp not found."},
            status_code=404,
        )

    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.camp_id == camp.id)
        .first()
    )

    if task is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Task not found."},
            status_code=404,
        )

    people = (
        db.query(Person)
        .filter(Person.camp_id == camp.id)
        .order_by(Person.person_type, Person.last_name, Person.first_name)
        .all()
    )

    teams = (
        db.query(Team)
        .filter(Team.camp_id == camp.id)
        .order_by(Team.team_type, Team.name)
        .all()
    )

    return templates.TemplateResponse(
        "tasks/add_assignment.html",
        {
            "request": request,
            "camp": camp,
            "task": task,
            "people": people,
            "teams": teams,
            "error": None,
        },
    )


@app.post("/camps/{camp_id}/tasks/{task_id}/assignments/new")
async def create_task_assignment(
    request: Request,
    camp_id: int,
    task_id: int,
    assignee: str = Form(...),
    status_override: str = Form(""),
    assignment_notes: str = Form(""),
    db: Session = Depends(get_db),
):
    camp = db.get(Camp, camp_id)

    if camp is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Camp not found."},
            status_code=404,
        )

    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.camp_id == camp.id)
        .first()
    )

    if task is None:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Task not found."},
            status_code=404,
        )

    kind, raw_id = assignee.split(":", 1)
    target_id = int(raw_id)

    assigned_person_id = None
    assigned_team_id = None

    if kind == "person":
        person = (
            db.query(Person)
            .filter(Person.id == target_id, Person.camp_id == camp.id)
            .first()
        )
        if person is None:
            return templates.TemplateResponse(
                "not_found.html",
                {"request": request, "message": "Person not found."},
                status_code=404,
            )
        assigned_person_id = person.id

    elif kind == "team":
        team = (
            db.query(Team)
            .filter(Team.id == target_id, Team.camp_id == camp.id)
            .first()
        )
        if team is None:
            return templates.TemplateResponse(
                "not_found.html",
                {"request": request, "message": "Team not found."},
                status_code=404,
            )
        assigned_team_id = team.id

    assignment = TaskAssignment(
        camp_id=camp.id,
        task_id=task.id,
        assigned_person_id=assigned_person_id,
        assigned_team_id=assigned_team_id,
        status_override=status_override.strip() or None,
        assignment_notes=assignment_notes.strip() or None,
    )

    db.add(assignment)
    db.commit()

    return RedirectResponse(url=f"/camps/{camp.id}/tasks/{task.id}", status_code=303)


@app.post("/camps/{camp_id}/tasks/{task_id}/assignments/{assignment_id}/remove")
async def remove_task_assignment(
    camp_id: int,
    task_id: int,
    assignment_id: int,
    db: Session = Depends(get_db),
):
    assignment = (
        db.query(TaskAssignment)
        .filter(
            TaskAssignment.id == assignment_id,
            TaskAssignment.camp_id == camp_id,
            TaskAssignment.task_id == task_id,
        )
        .first()
    )

    if assignment is not None:
        db.delete(assignment)
        db.commit()

    return RedirectResponse(url=f"/camps/{camp_id}/tasks/{task_id}", status_code=303)


@app.get("/readiness", response_class=HTMLResponse)
async def readiness_page(request: Request):
    return templates.TemplateResponse("readiness.html", {"request": request})


@app.get("/outputs", response_class=HTMLResponse)
async def outputs_page(request: Request):
    return templates.TemplateResponse("outputs.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok"}
