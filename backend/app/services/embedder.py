import logging
import httpx
from sqlalchemy.orm import Session
from app.models.chunk import DocumentChunk

logger = logging.getLogger(__name__)

# HuggingFace Free Inference API for embeddings (No API key needed for basic usage, rate limited)
HF_API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

class APIEmbeddingModel:
    def encode(self, texts):
        try:
            # We must pass strings as a list to the API
            response = httpx.post(HF_API_URL, json={"inputs": texts}, timeout=10.0)
            if response.status_code == 200:
                # The API returns a list of embeddings
                return response.json()
            else:
                logger.error(f"HF API Error: {response.text}")
                # Fallback zero embedding if API fails
                return [[0.0] * 384 for _ in texts]
        except Exception as e:
            logger.error(f"Embedding request failed: {e}")
            return [[0.0] * 384 for _ in texts]

def get_embedding_model():
    return APIEmbeddingModel()

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
