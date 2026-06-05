from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Camp Command Centre")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# Temporary in-memory camp data.
# This will be replaced with SQLite/SQLAlchemy later.
CAMPS = [
    {
        "id": 1,
        "name": "Spring Cub Camp 2027",
        "camp_type": "Campsite Camp",
        "start_date": "2027-05-15",
        "end_date": "2027-05-17",
        "venue_name": "Green Wood Campsite",
        "camp_leader": "Bogdan Alecsa",
        "permit_holder": "Ed Smith",
        "status": "Planning",
        "notes": "Prototype camp used for early UI testing.",
    }
]


def get_camp_or_none(camp_id: int) -> Optional[dict]:
    for camp in CAMPS:
        if camp["id"] == camp_id:
            return camp
    return None


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    current_camp = CAMPS[0] if CAMPS else None

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "camp": current_camp,
            "people_count": 42,
            "task_count": 58,
            "programme_sessions": 18,
            "readiness": 78,
        },
    )


@app.get("/camps", response_class=HTMLResponse)
async def camp_list(request: Request):
    return templates.TemplateResponse(
        "camps/list.html",
        {
            "request": request,
            "camps": CAMPS,
        },
    )


@app.get("/camps/new", response_class=HTMLResponse)
async def new_camp_form(request: Request):
    return templates.TemplateResponse(
        "camps/new.html",
        {
            "request": request,
        },
    )


@app.post("/camps/new")
async def create_camp(
    name: str = Form(...),
    camp_type: str = Form("Campsite Camp"),
    start_date: str = Form(...),
    end_date: str = Form(...),
    venue_name: str = Form(""),
    camp_leader: str = Form(""),
    permit_holder: str = Form(""),
    notes: str = Form(""),
):
    new_id = max([camp["id"] for camp in CAMPS], default=0) + 1

    camp = {
        "id": new_id,
        "name": name,
        "camp_type": camp_type,
        "start_date": start_date,
        "end_date": end_date,
        "venue_name": venue_name,
        "camp_leader": camp_leader,
        "permit_holder": permit_holder,
        "status": "Planning",
        "notes": notes,
    }

    CAMPS.append(camp)

    return RedirectResponse(url=f"/camps/{new_id}", status_code=303)


@app.get("/camps/{camp_id}", response_class=HTMLResponse)
async def camp_detail(request: Request, camp_id: int):
    camp = get_camp_or_none(camp_id)

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
            "people_count": 42,
            "team_count": 6,
            "task_count": 58,
            "programme_sessions": 18,
            "readiness": 78,
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
