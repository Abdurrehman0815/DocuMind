import logging
from sqlalchemy.orm import Session
from app.models.chunk import DocumentChunk
from fastembed import TextEmbedding

logger = logging.getLogger(__name__)

# Lazy load the local embedding model so it doesn't block startup
_local_model = None

class LocalEmbeddingModel:
    def encode(self, texts):
        global _local_model
        try:
            if _local_model is None:
                # BAAI/bge-small-en-v1.5 generates 384-dimensional embeddings like all-MiniLM-L6-v2
                _local_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
            
            # fastembed returns an iterator of numpy arrays, we convert to list of lists
            embeddings = list(_local_model.embed(texts))
            return [emb.tolist() for emb in embeddings]
        except Exception as e:
            logger.error(f"Local embedding failed: {e}")
            return [[0.0] * 384 for _ in texts]

def get_embedding_model():
    return LocalEmbeddingModel()

def embed_document_text(document_id: int, text: str, db: Session):
    """
    Splits the text into chunks, generates embeddings using HF API, and saves to pgvector.
    """
    if not text or len(text.strip()) == 0:
        return
        
    try:
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
        logger.info(f"Created {len(chunks)} chunks. Generating embeddings via API...")
        
        model = get_embedding_model()
        embeddings = model.encode(chunks)
        
        for i, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
            doc_chunk = DocumentChunk(
                document_id=document_id,
                content=chunk_text,
                embedding=embedding
            )
            db.add(doc_chunk)
            
        db.commit()
        logger.info(f"Saved {len(chunks)} embeddings to pgvector for document {document_id}")
            
    except Exception as e:
        print(f"Embedding error for document {document_id}: {e}")
