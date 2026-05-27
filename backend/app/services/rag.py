import json
from groq import Groq
from sqlalchemy.orm import Session
from app.models.chunk import DocumentChunk
from app.models.document import Document
from app.services.embedder import get_embedding_model
from app.config.settings import settings

def generate_chat_response(query: str, user_id: int, db: Session, document_id: int = None, language: str = "English") -> str:
    """
    RAG Implementation:
    1. Embeds the user query
    2. Searches pgvector for top 3 similar chunks
    3. Feeds context + query to Groq
    4. Returns answer in the requested language
    """
    
    # 1. Embed query
    try:
        model = get_embedding_model()
        query_embedding = model.encode([query])[0].tolist()
    except Exception as e:
        print(f"Embedding error: {e}")
        return "I'm having trouble understanding your query right now."

    # 2. Vector Search (pgvector cosine distance)
    embedding_str = f"[{','.join(map(str, query_embedding))}]"
    
    try:
        base_query = db.query(DocumentChunk, Document).join(Document, DocumentChunk.document_id == Document.id).filter(Document.user_id == user_id)
        if document_id:
            base_query = base_query.filter(DocumentChunk.document_id == document_id)
            
        results = base_query.order_by(DocumentChunk.embedding.cosine_distance(embedding_str)).limit(5).all()
            
        if not results:
            return "You haven't uploaded any documents yet, or I couldn't find any relevant information."
            
        # 3. Build context
        context_parts = []
        for chunk, doc in results:
            context_parts.append(f"--- Document: {doc.filename} ---\n{chunk.content}")
            
        context_str = "\n\n".join(context_parts)
        
        system_prompt = f"""You are a helpful AI Life Admin named DocuMind. 
Answer the user's question using ONLY the provided document context below.
If the answer is not contained in the context, say "I cannot find the answer in your documents."
Always reply in the following language: {language}.

CONTEXT:
{context_str}
"""
        
        # 4. Generate response with Groq
        try:
            client = Groq(api_key=settings.groq_api_key)
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query}
                ],
                temperature=0.2
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Groq chat error: {e}")
            return "I'm sorry, my AI brain (Groq) encountered an error while trying to generate a response."
            
    except Exception as e:
        print(f"Vector search error: {e}")
        return "Error searching your documents."
