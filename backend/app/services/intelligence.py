import os
import json
from groq import Groq
from app.config.settings import settings

CATEGORIES = [
    "electricity bill",
    "insurance",
    "subscription",
    "tax document",
    "bank statement",
    "scholarship document",
    "rent receipt",
    "medical document",
    "other"
]

def classify_document(text: str) -> str:
    """Classify the text into one of the predefined categories using Groq."""
    if not text or len(text.strip()) == 0:
        return "other"
        
    try:
        client = Groq(api_key=settings.groq_api_key)
        truncated_text = text[:1500] 
        
        prompt = f"""You are an expert document classifier. Categorize the following document text into EXACTLY ONE of these categories: {', '.join(CATEGORIES)}.
Do not output anything else except the exact category name.

DOCUMENT TEXT:
{truncated_text}
"""
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        
        result = response.choices[0].message.content.strip().lower()
        
        # Verify it's a valid category
        for cat in CATEGORIES:
            if cat in result:
                return cat
                
        return "other"
    except Exception as e:
        print(f"Classification error: {e}")
        return "other"

def extract_entities(text: str, category: str) -> dict:
    """Extract structured JSON entities from the text using Groq."""
    if not text or len(text.strip()) == 0:
        return {}
        
    prompt = f"""
You are an expert data extraction AI. Read the following text extracted from a document categorized as "{category}".
Extract the following information and return it as a pure JSON object:
- due_date
- expiry_date
- payment_amount
- provider_name
- account_identifier
- policy_number

CRITICAL INSTRUCTION FOR DATES: 
You MUST format all dates (due_date and expiry_date) strictly as "YYYY-MM-DD" (e.g. "2026-05-29"). If you see "May 29 2026" or "29 May, 2026", convert it to "2026-05-29".

If a field is not found in the text, set its value to null. 
Do not include any other text, markdown formatting, or explanation. ONLY output the JSON object.

DOCUMENT TEXT:
{text[:2000]}
"""
    
    try:
        # Ask Groq to extract the JSON
        client = Groq(api_key=settings.groq_api_key)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )
        
        raw_output = response.choices[0].message.content.strip()
        parsed_json = json.loads(raw_output)
        return parsed_json
    except Exception as e:
        print(f"Entity extraction error: {e}")
        return {}
