import sys
import logging
from sqlalchemy.orm import Session
from fastembed import TextEmbedding
from app.config.database import SessionLocal
from app.models.document import Document
from app.models.chunk import DocumentChunk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def embed_document_text(document_id: int):
    """
    Splits the text into chunks, generates embeddings using fastembed, and saves to pgvector.
    Runs in a standalone process to guarantee memory is freed by the OS upon exit.
    """
    db = SessionLocal()
    try:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc or not doc.extracted_text:
            return
            
        text = doc.extracted_text
        if not text or len(text.strip()) == 0:
            return
            
        logger.info(f"Chunking document {document_id}")
        
        # We use a simple manual text splitter instead of langchain to save memory
        def simple_chunker(text, chunk_size=500, overlap=50):
            words = text.split()
            chunks = []
            i = 0
            while i < len(words):
                chunk = " ".join(words[i:i+chunk_size])
                chunks.append(chunk)
                i += chunk_size - overlap
            return chunks
            
        chunks = simple_chunker(text)
        logger.info(f"Created {len(chunks)} chunks. Loading model...")
        
        # Load model (uses ~90MB RAM)
        model = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
        
        logger.info("Generating embeddings...")
        embeddings = list(model.embed(chunks))
        
        # Delete existing chunks if any
        db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).delete()
        
        for i, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
            doc_chunk = DocumentChunk(
                document_id=document_id,
                content=chunk_text,
                embedding=embedding.tolist()
            )
            db.add(doc_chunk)
            
        db.commit()
        logger.info(f"Saved {len(chunks)} embeddings to pgvector for document {document_id}")
            
    except Exception as e:
        logger.error(f"Embedding error for document {document_id}: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        doc_id = int(sys.argv[1])
        embed_document_text(doc_id)
