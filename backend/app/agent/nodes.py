"""
The graph nodes.

Each function is ONE step. It takes the current state, does its job,
and returns only the pieces of state it changed. LangGraph merges those
changes back into the shared state automatically.

Flow:
    check_input -> extract -> classify_risk -> check_completeness
                -> summarize -> recommend_capa
"""
from app.agent.llm import ask_llm, parse_json
from app.agent.prompts import EXTRACT_PROMPT, RISK_PROMPT, SUMMARY_PROMPT, CAPA_PROMPT
from app.agent.state import ComplaintState

# The fields we treat as essential for a usable complaint record.
REQUIRED_FIELDS = ["product_name", "batch_number", "complaint_type"]


def check_input(state: ComplaintState) -> dict:
    """
    First gate: is there any real text to work with?
    If not, we set an error and the graph will skip straight to the end.
    """
    text = (state.get("raw_text") or "").strip()
    if len(text) < 10:
        return {"error": "No readable complaint text was provided."}
    return {"error": None}


def extract(state: ComplaintState) -> dict:
    """Pull the structured form fields out of the raw complaint text."""
    prompt = EXTRACT_PROMPT.format(text=state["raw_text"])
    answer = ask_llm(prompt)
    fields = parse_json(answer)
    return {"fields": fields}


def classify_risk(state: ComplaintState) -> dict:
    """Decide severity, priority and a one-line risk (bonus feature)."""
    prompt = RISK_PROMPT.format(text=state["raw_text"])
    result = parse_json(ask_llm(prompt))

    severity = result.get("severity", "Minor")
    priority = result.get("priority", "Low")

    # Feed severity/priority back into the extracted fields so the form
    # gets pre-filled with them too.
    fields = dict(state.get("fields", {}))
    fields["initial_severity"] = severity
    fields["priority"] = priority

    return {
        "severity": severity,
        "priority": priority,
        "risk": result.get("risk", ""),
        "fields": fields,
    }


def check_completeness(state: ComplaintState) -> dict:
    """
    Completeness checker (bonus feature).
    Flags any essential field the AI could not find, so the reviewer
    knows what to ask the customer for.
    """
    fields = state.get("fields", {})
    missing = [f for f in REQUIRED_FIELDS if not fields.get(f)]

    if missing:
        pretty = ", ".join(m.replace("_", " ") for m in missing)
        note = f"Complaint is missing: {pretty}. Please follow up with the customer."
    else:
        note = "All essential fields were captured."

    return {"missing_fields": missing, "completeness_note": note}


def summarize(state: ComplaintState) -> dict:
    """Write a one-line summary for quick review (bonus feature)."""
    prompt = SUMMARY_PROMPT.format(text=state["raw_text"])
    summary = ask_llm(prompt).strip()
    return {"summary": summary}


def recommend_capa(state: ComplaintState) -> dict:
    """
    CAPA recommendation (bonus feature).
    Suggests a corrective and preventive action for the complaint.
    """
    prompt = CAPA_PROMPT.format(text=state["raw_text"])
    capa = ask_llm(prompt).strip()
    return {"capa": capa}
