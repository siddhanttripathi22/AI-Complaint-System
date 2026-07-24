
import json
import re

from langchain_groq import ChatGroq

from app.config import settings


llm = ChatGroq(
    api_key=settings.groq_api_key,
    model=settings.groq_model,
    temperature=0,
)


def ask_llm(prompt: str) -> str:
    """Send one prompt, get the text answer back."""
    response = llm.invoke(prompt)
    return response.content


def parse_json(text: str) -> dict:
    """
    LLMs sometimes wrap JSON in ```json fences or add a stray sentence.
    This grabs the first {...} block and parses it. Returns {} on failure
    so one bad response never crashes the whole pipeline.
    """
    if not text:
        return {}
    # find the outermost JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return {}
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return {}
