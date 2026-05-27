import logging
from sqlalchemy.orm import Session
from app.models.chunk import DocumentChunk
from fastembed import TextEmbedding

logger = logging.getLogger(__name__)

class LocalEmbeddingModel:
    def encode(self, texts):
        import gc
        try:
            # We explicitly DO NOT cache this globally to save RAM.
            # We load the model, generate embeddings, and instantly delete it from memory.
            # all-MiniLM-L6-v2 uses ~90MB RAM compared to BAAI's ~130MB, both are 384-dimensional
            model = TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
            
            # fastembed returns an iterator of numpy arrays, we convert to list of lists
            embeddings = list(model.embed(texts))
            result = [emb.tolist() for emb in embeddings]
            
            # Explicitly free memory to prevent Render 512MB OOM crash
            del model
            gc.collect()
            
            return result
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
