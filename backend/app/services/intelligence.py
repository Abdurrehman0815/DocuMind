import os
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"

import json
from groq import Groq
from app.config.settings import settings

# Lazy load classifier so it doesn't block startup
_classifier = None

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

def get_classifier():
    global _classifier
    if _classifier is None:
        from transformers import pipeline
        # Using a fast, lightweight DistilBERT zero-shot classification model
        # This fixes the tokenizer Enum parsing error on Windows
        _classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")
    return _classifier

def classify_document(text: str) -> str:
    """Classify the text into one of the predefined categories using HuggingFace."""
    if not text or len(text.strip()) == 0:
        return "other"
        
    try:
        classifier = get_classifier()
        # Truncate text for classification to avoid token limits
        truncated_text = text[:1500] 
        result = classifier(truncated_text, CATEGORIES)
        
        # result['labels'][0] contains the highest scoring category
        best_category = result['labels'][0]
        return best_category
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
