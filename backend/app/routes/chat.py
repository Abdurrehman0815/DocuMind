from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.middleware.auth import get_current_user
from app.services.rag import generate_chat_response

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    query: str
    document_id: Optional[int] = None
    language: str = "English"

@router.post("")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    answer = generate_chat_response(
        query=request.query,
        user_id=current_user.id,
        db=db,
        document_id=request.document_id,
        language=request.language
    )
    
    return {"answer": answer}
