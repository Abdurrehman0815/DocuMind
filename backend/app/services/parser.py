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

import requests

def parse_image_with_ocrspace(file_bytes: bytes, filename: str) -> str:
    """Extract text from an image using the free OCR.Space API to save RAM."""
    try:
        url = "https://api.ocr.space/parse/image"
        payload = {
            'apikey': 'helloworld',
            'language': 'eng',
            'scale': True,
            'OCREngine': 2 # Engine 2 is better for receipts/documents
        }
        files = {
            'file': (filename, file_bytes)
        }
        
        response = requests.post(url, data=payload, files=files, timeout=30)
        result = response.json()
        
        if result.get("ParsedResults") and not result.get("IsErroredOnProcessing"):
            text = result["ParsedResults"][0].get("ParsedText", "")
            return text.strip()
        else:
            print(f"OCR.Space Error: {result.get('ErrorMessage')}")
            return ""
    except Exception as e:
        print(f"OCR.Space request failed: {e}")
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
            extracted_text = parse_image_with_ocrspace(file_bytes, doc.filename)
            
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
            db.commit()
            
            # 3. Vector Embeddings (RAG Memory)
            # Run in a separate process to guarantee the OS reclaims the memory instantly!
            import subprocess
            import sys
            print(f"Spawning separate process for embeddings for doc {doc.id}...")
            # Use the same python executable running the current process
            subprocess.run([sys.executable, "-m", "app.services.run_embeddings", str(doc.id)])
            
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
