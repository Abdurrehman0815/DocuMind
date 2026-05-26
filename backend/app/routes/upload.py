import os
import uuid
from typing import Annotated
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from supabase import create_client, Client

from app.services.parser import process_document_background

from app.config.database import get_db
from app.config.settings import settings
from app.middleware.auth import get_current_user
from app.models.document import Document

router = APIRouter(prefix="/upload", tags=["Upload"])

# Initialize Supabase client
supabase: Client = create_client(settings.supabase_url, settings.supabase_key)

ALLOWED_TYPES = ["application/pdf", "image/png", "image/jpeg", "image/jpg"]
MAX_SIZE = 10 * 1024 * 1024  # 10 MB

@router.post("")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type"
        )
    
    content = await file.read()
    
    if len(content) > MAX_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 10MB limit"
        )

    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{current_user.id}/{uuid.uuid4()}{file_ext}"
    
    # Upload to Supabase Storage
    try:
        res = supabase.storage.from_('documents').upload(
            path=unique_filename,
            file=content,
            file_options={"content-type": file.content_type}
        )
        
        # Get public URL
        public_url = supabase.storage.from_('documents').get_public_url(unique_filename)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload to cloud storage: {str(e)}")

    new_doc = Document(
        user_id=current_user.id,
        filename=file.filename,
        file_path=public_url,
        content_type=file.content_type,
        status="uploaded"
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # Launch OCR parsing in the background
    background_tasks.add_task(process_document_background, new_doc.id)

    return {"message": "File uploaded successfully", "document_id": new_doc.id, "filename": new_doc.filename, "url": public_url}

@router.get("")
def get_documents(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    docs = db.query(Document).filter(Document.user_id == current_user.id).order_by(Document.created_at.desc()).all()
    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "file_path": doc.file_path,
            "content_type": doc.content_type,
            "status": doc.status,
            "category": doc.category,
            "created_at": doc.created_at
        }
        for doc in docs
    ]

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    doc = db.query(Document).filter(Document.id == document_id, Document.user_id == current_user.id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    # Extract path from URL (Assuming URL ends with /documents/{path})
    try:
        path = doc.file_path.split("/documents/")[-1]
        supabase.storage.from_('documents').remove([path])
    except Exception as e:
        print(f"Failed to delete from Supabase: {e}")
        # Continue to delete from DB anyway

    db.delete(doc)
    db.commit()
    return {"message": "Document deleted successfully"}

@router.post("/{document_id}/summarize")
def summarize_document(
    document_id: int, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    doc = db.query(Document).filter(Document.id == document_id, Document.user_id == current_user.id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    if not doc.extracted_text:
        raise HTTPException(status_code=400, detail="Document has no extracted text to summarize. Please wait for OCR to finish.")
        
    import ollama
    
    prompt = f"""You are an expert at summarizing documents. Please read the following document and provide:
1. A very short 1-2 sentence overview.
2. 3-4 bullet points of the most critical information.
3. Any immediate Action Items (like paying a bill, renewing a policy, etc). If none, say "None".

DOCUMENT:
{doc.extracted_text}

SUMMARY:
"""
    
    try:
        response = ollama.chat(model='llama3.2:3b', messages=[
            {'role': 'user', 'content': prompt}
        ])
        return {"summary": response['message']['content'].strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate summary: {str(e)}")
