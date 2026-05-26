from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.config.database import get_db
from app.middleware.auth import get_current_user
from app.models.chunk import DocumentChunk
from app.models.document import Document
from app.services.embedder import get_embedding_model

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("")
def search_documents(q: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if not q or not q.strip():
        return []
        
    model = get_embedding_model()
    query_embedding = model.encode([q])[0].tolist()
    
    # We find the chunks that match, and then group by document to return unique documents
    # The documents are returned ordered by the best matching chunk
    base_query = db.query(DocumentChunk, Document).join(Document).filter(Document.user_id == current_user.id)
    
    results = base_query.order_by(
        DocumentChunk.embedding.cosine_distance(query_embedding)
    ).limit(20).all()
    
    # Deduplicate documents while preserving the order of the best match
    seen_doc_ids = set()
    matched_docs = []
    
    for chunk, doc in results:
        if doc.id not in seen_doc_ids:
            seen_doc_ids.add(doc.id)
            matched_docs.append({
                "id": doc.id,
                "filename": doc.filename,
                "file_path": doc.file_path,
                "content_type": doc.content_type,
                "status": doc.status,
                "category": doc.category,
                "created_at": doc.created_at,
                "matching_chunk": chunk.content
            })
            
    return matched_docs
