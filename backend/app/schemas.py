"""
Pydantic schemas = the shape of data going in and out of the API.

These are separate from the DB model on purpose: the API can accept
partial data, and we can validate it before touching the database.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExtractRequest(BaseModel):
    """Body for /extract when the user pastes text instead of a file."""
    text: str


class AskRequest(BaseModel):
    """Body for /ask — a follow-up question about the current complaint."""
    question: str
    context: str  # the extracted complaint details, used to ground the answer


class AskResponse(BaseModel):
    answer: str


class ComplaintFields(BaseModel):
    """
    The full set of form fields. Every field is optional because the
    AI may not find all of them in a given complaint document.
    """
    complaint_source: Optional[str] = None
    customer_name: Optional[str] = None
    product_name: Optional[str] = None
    product_strength: Optional[str] = None
    batch_number: Optional[str] = None
    manufacturing_date: Optional[str] = None
    expiry_date: Optional[str] = None
    quantity_affected: Optional[str] = None
    complaint_type: Optional[str] = None
    complaint_date: Optional[str] = None
    description: Optional[str] = None
    initial_severity: Optional[str] = None
    priority: Optional[str] = None


class ExtractResponse(BaseModel):
    """What /extract returns: the fields plus the bonus AI insights."""
    fields: ComplaintFields
    ai_summary: Optional[str] = None
    ai_risk: Optional[str] = None
    ai_capa: Optional[str] = None
    missing_fields: list[str] = []
    completeness_note: Optional[str] = None


class ComplaintOut(ComplaintFields):
    """A saved complaint as returned from the database."""
    id: int
    ai_summary: Optional[str] = None
    ai_risk: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
