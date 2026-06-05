from datetime import date
from pathlib import Path

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Camp, Person

app = FastAPI(title="Camp Command Centre")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


def get_latest_camp(db: Session):
    return db.query(Camp).order_by(Camp.start_date.desc()).first()


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    current_camp = get_latest_camp(db)

    people_count = 0
    if current_camp:
        people_count = db.query(Person).filter(Person.camp_id == current_camp.id).count()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "camp": current_camp,
            "people_count": people_count,
            "task_count": 0,
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

    return templates.TemplateResponse(
        "camps/detail.html",
        {
            "request": request,
            "camp": camp,
            "people_count": people_count,
            "team_count": 0,
            "task_count": 0,
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


@app.get("/programme", response_class=HTMLResponse)
async def programme_page(request: Request):
    return templates.TemplateResponse("programme.html", {"request": request})


@app.get("/tasks", response_class=HTMLResponse)
async def tasks_page(request: Request):
    return templates.TemplateResponse("tasks.html", {"request": request})


@app.get("/readiness", response_class=HTMLResponse)
async def readiness_page(request: Request):
    return templates.TemplateResponse("readiness.html", {"request": request})


@app.get("/outputs", response_class=HTMLResponse)
async def outputs_page(request: Request):
    return templates.TemplateResponse("outputs.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok"}
