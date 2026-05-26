import ollama
from sqlalchemy.orm import Session
from sqlalchemy import asc

from app.models.chunk import DocumentChunk
from app.models.document import Document
from app.services.embedder import get_embedding_model

def generate_chat_response(query: str, user_id: str, db: Session, document_id: int = None, language: str = "English") -> str:
    """
    RAG Engine:
    1. Embeds the user query
    2. Searches the pgvector database for similar chunks
    3. Feeds context + query to Ollama
    4. Returns the AI response
    """
    
    # 1. Generate embedding for the query
    model = get_embedding_model()
    query_embedding = model.encode([query])[0].tolist()
    
    # 2. Search for top 3 similar chunks
    base_query = db.query(DocumentChunk).join(Document).filter(Document.user_id == user_id)
    
    if document_id:
        base_query = base_query.filter(DocumentChunk.document_id == document_id)
        
    # Order by cosine distance (most similar first)
    top_chunks = base_query.order_by(
        DocumentChunk.embedding.cosine_distance(query_embedding)
    ).limit(3).all()
    
    if not top_chunks:
        return "I couldn't find any relevant documents to answer your question. Please upload some documents first!"
        
    # 3. Build the Context
    context_texts = []
    for i, chunk in enumerate(top_chunks):
        context_texts.append(f"--- Document Excerpt {i+1} ---\n{chunk.content}")
        
    full_context = "\n\n".join(context_texts)
    
    prompt = f"""You are a helpful AI Life Admin Assistant. 
Answer the user's question based strictly on the following document context.
If the answer cannot be found in the context, tell the user you don't know based on the provided documents.
Do not make up facts. Keep the answer clear and concise.
IMPORTANT: You MUST answer strictly in the following language: {language}.

CONTEXT:
{full_context}

USER QUESTION:
{query}

ANSWER in {language}:
"""

    # 4. Generate response with Ollama
    try:
        response = ollama.chat(model='llama3.2:3b', messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        return response['message']['content'].strip()
        
    except Exception as e:
        print(f"Ollama chat error: {e}")
        return "I'm sorry, my AI brain (Ollama) encountered an error while trying to generate a response. Make sure it is running!"
