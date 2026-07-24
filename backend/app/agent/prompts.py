EXTRACT_PROMPT = """You are a pharmaceutical Quality Assurance assistant.
You read a customer complaint (for an API or finished drug product) and
pull out the key details to fill a complaint intake form.

Return ONLY a JSON object with exactly these keys. Use null if a value
is not mentioned. Do not invent values.

{{
  "complaint_source": "how the complaint arrived, e.g. Email, Phone, Distributor",
  "customer_name": "the customer or company that raised it",
  "product_name": "name of the drug / product",
  "product_strength": "strength or grade, e.g. 500mg, USP",
  "batch_number": "batch or lot number",
  "manufacturing_date": "as written in the text",
  "expiry_date": "as written in the text",
  "quantity_affected": "amount affected, with unit",
  "complaint_type": "short category, e.g. Contamination, Packaging Defect, Discoloration, Efficacy",
  "complaint_date": "date the complaint was made",
  "description": "a clear 1-2 sentence description of the problem"
}}

Complaint document:
---
{text}
---
JSON:"""



RISK_PROMPT = """You are a pharmaceutical QA risk assessor.
Given the complaint below, decide:

- severity: one of "Critical", "Major", "Minor"
- priority: one of "High", "Medium", "Low"
- risk: one short phrase explaining the main patient/quality risk

Rules of thumb:
- Anything about contamination, wrong product, or a health hazard is Critical / High.
- Packaging or labelling defects that could cause a mix-up are Major.
- Cosmetic issues with no safety impact are Minor / Low.

Return ONLY JSON: {{"severity": "...", "priority": "...", "risk": "..."}}

Complaint:
---
{text}
---
JSON:"""



SUMMARY_PROMPT = """Summarise this pharmaceutical complaint in ONE short
sentence a QA reviewer can read at a glance. No preamble, just the sentence.

Complaint:
---
{text}
---
Summary:"""



CHAT_PROMPT = """You are a pharmaceutical QA assistant. Answer the user's
question about the complaint below. Be concise, factual and helpful. If the
answer is not present in the complaint, say you don't have that information.

Complaint details:
---
{context}
---
Question: {question}
Answer:"""
