"""
The 'state' is a shared box of data that travels through the graph.

Every node reads what it needs from the state and writes its result
back into it. By the time we reach the end, the state holds the full
extracted complaint plus all the AI insights.
"""
from typing import Optional, TypedDict


class ComplaintState(TypedDict, total=False):
    # input
    raw_text: str

    # filled by the extract node
    fields: dict

    # filled by the risk node
    severity: str
    priority: str
    risk: str

    # filled by the completeness node
    missing_fields: list
    completeness_note: str

    # filled by the summary node
    summary: str

    # filled by the capa node
    capa: str

    # set if the input was empty / unusable
    error: Optional[str]
