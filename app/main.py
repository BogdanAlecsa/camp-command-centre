from datetime import date
from pathlib import Path

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Camp

app = FastAPI(title="Camp Command Centre")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    current_camp = db.query(Camp).order_by(Camp.start_date.desc()).first()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "camp": current_camp,
            "people_count": 0,
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


@app.get("/camps/{camp_id}", response_class=HTMLResponse)
async def camp_detail(request: Request, camp_id: int, db: Session = Depends(get_db)):
    camp = db.query(Camp).filter(Camp.id == camp_id).first()

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
        "camps/detail.html",
        {
            "request": request,
            "camp": camp,
            "people_count": 0,
            "team_count": 0,
            "task_count": 0,
            "programme_sessions": 0,
            "readiness": 0,
        },
    )


@app.get("/people", response_class=HTMLResponse)
async def people_page(request: Request):
    return templates.TemplateResponse("people.html", {"request": request})


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
