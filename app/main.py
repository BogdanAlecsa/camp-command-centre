from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Camp Command Centre")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "camp_name": "Spring Cub Camp 2027",
            "camp_status": "Prototype",
            "people_count": 42,
            "task_count": 58,
            "programme_sessions": 18,
            "readiness": 78,
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
