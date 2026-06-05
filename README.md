# Camp Command Centre

Camp Command Centre is a local-first, browser-based camp planning and operations tool for Scout camps, sleepovers and other Nights Away events.

It helps organisers answer five practical questions:

1. What are we doing?
2. Who is involved?
3. Who is responsible?
4. What have we forgotten?
5. Are we ready?

## Project Status

Current phase: **Milestone 0 – repository setup and clickable prototype**

This starter pack includes:

- FastAPI skeleton
- basic dashboard page
- Codespaces configuration
- project documentation folder
- sample data folder
- tests folder
- scripts folder

## Running Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

On Mac/Linux use:

```bash
source .venv/bin/activate
```

## Running in GitHub Codespaces

Open the repository in Codespaces, then run:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Codespaces should offer to open the forwarded port.

## Development Philosophy

Camp Command Centre is not a spreadsheet and not just a database frontend.

It is a guided camp planning tool.
