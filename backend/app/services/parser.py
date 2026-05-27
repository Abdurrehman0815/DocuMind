import os
import io
import httpx
import base64
from sqlalchemy.orm import Session
from groq import Groq

from app.config.database import SessionLocal
from app.models.document import Document
from app.services.intelligence import classify_document, extract_entities
from app.services.embedder import embed_document_text
from app.config.settings import settings

def download_file_bytes(url: str) -> bytes:
    """Download the public file URL from Supabase to process it."""
    response = httpx.get(url)
    response.raise_for_status()
    return response.content

def parse_pdf(file_bytes: bytes) -> str:
    """Extract text from a digital PDF using PyMuPDF (fitz)."""
    import fitz  # PyMuPDF
    
    text = ""
    # Open the PDF from memory
    with fitz.open("pdf", file_bytes) as doc:
        for page in doc:
            text += page.get_text() + "\n"
            
    return text.strip()

def parse_image_with_groq(file_bytes: bytes, mime_type: str) -> str:
    """Extract text from an image using Groq Vision API."""
    try:
        base64_image = base64.b64encode(file_bytes).decode('utf-8')
        client = Groq(api_key=settings.groq_api_key)
        
        response = client.chat.completions.create(
            model="llama-3.2-90b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all the text from this image exactly as it appears. Do not add any extra commentary, just return the text."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq Vision error: {e}")
        return ""

def process_document_background(document_id: int):
    """
    Background task to download the file, parse the text based on its content_type,
    and update the database.
    """
    db = SessionLocal()
    try:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            return
            
        # Update status to parsing
        doc.status = "parsing"
        db.commit()

        # Download file from Supabase public URL
        file_bytes = download_file_bytes(doc.file_path)
        
        # 1. OCR Extraction
        extracted_text = ""
        
        if doc.content_type == "application/pdf":
            extracted_text = parse_pdf(file_bytes)
        elif doc.content_type in ["image/png", "image/jpeg", "image/jpg"]:
            extracted_text = parse_image_with_groq(file_bytes, doc.content_type)
            
        doc.extracted_text = extracted_text
        
        # 2. AI Intelligence (Classification & Extraction)
        # Skip if there's no text to analyze
        if extracted_text and extracted_text.strip():
            doc.status = "analyzing"
            db.commit()
            
            category = classify_document(extracted_text)
            doc.category = category
            
            # Using Groq to extract entities
            entities = extract_entities(extracted_text, category)
            doc.extracted_entities = entities
            
            # 3. Vector Embeddings (RAG Memory)
            embed_document_text(doc.id, extracted_text, db)
            
        # Update database with final status
        doc.status = "processed"
        db.commit()
        
    except Exception as e:
        print(f"Error parsing document {document_id}: {e}")
        if doc:
            doc.status = "error"
            db.commit()
    finally:
        db.close()
