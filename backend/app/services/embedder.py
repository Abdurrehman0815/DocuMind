import os
import logging
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"

from sqlalchemy.orm import Session
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.models.chunk import DocumentChunk

logger = logging.getLogger(__name__)

# Lazy load the embedding model
_embedding_model_instance = None

def get_embedding_model():
    global _embedding_model_instance
    if _embedding_model_instance is None:
        from sentence_transformers import SentenceTransformer
        logger.info("Loading HuggingFace multilingual embedding model...")
        _embedding_model_instance = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        logger.info("Model loaded successfully.")
    return _embedding_model_instance

def embed_document_text(document_id: int, text: str, db: Session):
    """
    Chunks the document text, generates vector embeddings, 
    and saves them to the pgvector database.
    """
    if not text or len(text.strip()) == 0:
        return
        
    try:
        # 1. Chunk the text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = text_splitter.split_text(text)
        
        if not chunks:
            return
            
        # 2. Generate embeddings
        model = get_embedding_model()
        # encode() returns a list of numpy arrays (or tensors). We convert to list of floats for pgvector.
        embeddings = model.encode(chunks)
        
        # 3. Save to database
        for i, chunk_text in enumerate(chunks):
            embedding_vector = embeddings[i].tolist()
            
            new_chunk = DocumentChunk(
                document_id=document_id,
                content=chunk_text,
                embedding=embedding_vector
            )
            db.add(new_chunk)
            
        db.commit()
        print(f"Successfully embedded {len(chunks)} chunks for document {document_id}")
        
    except Exception as e:
        print(f"Embedding error for document {document_id}: {e}")
