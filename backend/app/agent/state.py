
from typing import Optional, TypedDict


class ComplaintState(TypedDict, total=False):
   
    raw_text: str

 
    fields: dict

    
    severity: str
    priority: str
    risk: str

   
    missing_fields: list
    completeness_note: str

   
    summary: str

   
    error: Optional[str]
