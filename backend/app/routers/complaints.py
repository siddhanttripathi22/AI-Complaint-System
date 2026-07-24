
import io

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app import models, schemas
from app.agent.graph import run_agent
from app.agent.llm import ask_llm
from app.agent.prompts import CHAT_PROMPT
from app.database import get_db

router = APIRouter(prefix="/api/complaints", tags=["complaints"])


def _read_file(file: UploadFile) -> str:
    """
    Turn an uploaded file into plain text.
    Supports PDF, DOCX, and plain text / email files.
    (Production-grade OCR is not required for this assignment.)
    """
    data = file.file.read()
    name = (file.filename or "").lower()

    if name.endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(data))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if name.endswith(".docx"):
        from docx import Document
        doc = Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)

    # .txt, .eml or anything else: just decode as text.
    return data.decode("utf-8", errors="ignore")


def _to_response(result: dict) -> schemas.ExtractResponse:
    """Shape the agent's raw state into our API response."""
    if result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])

    return schemas.ExtractResponse(
        fields=schemas.ComplaintFields(**result.get("fields", {})),
        ai_summary=result.get("summary"),
        ai_risk=result.get("risk"),
        missing_fields=result.get("missing_fields", []),
        completeness_note=result.get("completeness_note"),
    )


@router.post("/extract", response_model=schemas.ExtractResponse)
def extract_from_text(body: schemas.ExtractRequest):
    """User pasted complaint text -> run the LangGraph agent on it."""
    result = run_agent(body.text)
    return _to_response(result)


@router.post("/extract-file", response_model=schemas.ExtractResponse)
def extract_from_file(file: UploadFile = File(...)):
    """User uploaded a complaint document -> read it, then run the agent."""
    text = _read_file(file)
    result = run_agent(text)
    return _to_response(result)


@router.post("", response_model=schemas.ComplaintOut)
def save_complaint(body: schemas.ComplaintFields, db: Session = Depends(get_db)):
    """Save the (possibly reviewer-edited) complaint into the database."""
    complaint = models.Complaint(**body.model_dump())
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint


@router.post("/ask", response_model=schemas.AskResponse)
def ask_about_complaint(body: schemas.AskRequest):
    """
    Answer a follow-up question about the current complaint.
    This powers the 'Ask me anything about this complaint' chat box.
    """
    prompt = CHAT_PROMPT.format(context=body.context, question=body.question)
    answer = ask_llm(prompt).strip()
    return schemas.AskResponse(answer=answer)


@router.get("", response_model=list[schemas.ComplaintOut])
def list_complaints(db: Session = Depends(get_db)):
    """Show all saved complaints, newest first."""
    return (
        db.query(models.Complaint)
        .order_by(models.Complaint.created_at.desc())
        .all()
    )
