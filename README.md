# AI-Powered Customer Complaint Management System

An AI intake assistant for pharmaceutical (API & FDF) customer complaints.
You upload or paste a complaint document, and a **LangGraph** agent reads it,
extracts the key details, assesses risk, and auto-fills a Quality Management
System (QMS) complaint form. The reviewer can edit anything and save it.

Built for the AIVOA Round 1 Full Stack assessment.

---

## Tech Stack

| Layer     | Technology                                  |
|-----------|---------------------------------------------|
| Frontend  | React + Redux Toolkit (Vite), Inter font    |
| Backend   | Python + FastAPI                            |
| AI Agent  | LangGraph                                    |
| LLM       | Groq — `openai/gpt-oss-20b`                        |
| Database  | Postgres                          |

---

## How It Works

```
                 ┌─────────────── Frontend (React + Redux) ───────────────┐
   User ─────►   │  AI Assistant panel  ──►  form auto-fills on the left  │
                 └───────────────┬────────────────────────────────────────┘
                                 │  POST /api/complaints/extract
                                 ▼
                 ┌─────────────── Backend (FastAPI) ──────────────────────┐
                 │                run_agent(text)                         │
                 │                     │                                   │
                 │   LangGraph:  check_input ─► extract ─► classify_risk   │
                 │                    ─► check_completeness ─► summarize    │
                 └───────────────┬────────────────────────────────────────┘
                                 │  extracted fields + AI insights
                                 ▼
                          Reviewer edits → Save → MySQL
```

The LangGraph agent has five nodes, each doing one job:

1. **check_input** – makes sure there is real text (else stops early).
2. **extract** – pulls out the form fields as JSON.
3. **classify_risk** – decides severity, priority and a risk note *(bonus)*.
4. **check_completeness** – flags any missing essential field *(bonus)*.
5. **summarize** – writes a one-line summary *(bonus)*.

---

## Setup

### 1. Backend

```bash
cd backend
python -m venv venv
Windows: venv\Scripts\activate
pip install -r requirements.txt



uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000` — API docs at `/docs`.

### 2. Database

Make sure Postgres is running and a database exists. The app
creates the table automatically on startup. To create it manually instead:



### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

---

## Try It

1. Open the app.
2. In the AI Assistant panel, paste the text from
   `sample-data/sample_complaint_email.txt` (or upload it as a file).
3. Click **Extract Details** — the form fills in, and you'll see the
   summary, risk and completeness insights.
4. Edit if needed, then **Save Complaint**.

---

## API Endpoints

| Method | Path                            | Purpose                          |
|--------|---------------------------------|----------------------------------|
| POST   | `/api/complaints/extract`       | Extract fields from pasted text  |
| POST   | `/api/complaints/extract-file`  | Extract fields from a file       |
| POST   | `/api/complaints`               | Save a complaint                 |
| GET    | `/api/complaints`               | List saved complaints            |

---

## Project Structure

```
complaint-system/
├── backend/
│   └── app/
│       ├── main.py              # FastAPI app
│       ├── config.py            # env settings
│       ├── database.py          # DB connection
│       ├── models.py            # complaints table
│       ├── schemas.py           # request/response shapes
│       ├── routers/complaints.py# API endpoints
│       └── agent/               # LangGraph agent
│           ├── state.py         # shared data
│           ├── prompts.py       # LLM instructions
│           ├── llm.py           # Groq setup + JSON parsing
│           ├── nodes.py         # the five steps
│           └── graph.py         # wiring
├── frontend/
│   └── src/
│       ├── store/               # Redux store + slice
│       ├── api/client.js        # axios
│       └── components/          # form + AI assistant
├── database/init.sql
└── sample-data/
```

---

## Bonus Features Implemented

- **AI Risk Classification** – severity + priority + risk note.
- **Complaint Completeness Checker** – flags missing essential fields.
- **Complaint Summary** – one-line summary for quick triage.

## Notes

- Production-grade OCR is not implemented (not required). File reading
  handles selectable-text PDF, DOCX, TXT and EML.
- `openai/gpt-oss-20b` is used as required; switch `GROQ_MODEL` in `.env` to
  `llama-3.3-70b-versatile` to compare stronger extraction.
```
