from app.config.database import engine, Base
from sqlalchemy import text

# Import models so Base knows about them
import app.models.document
import app.models.chunk

def setup_vector_db():
    print("Enabling pgvector extension on Supabase...")
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.commit()
        print("pgvector extension enabled!")
        
    print("Creating vector tables...")
    Base.metadata.create_all(bind=engine)
    print("Vector tables created successfully!")

if __name__ == "__main__":
    setup_vector_db()
