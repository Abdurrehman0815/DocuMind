from app.config.database import engine
from sqlalchemy import text

def add_intelligence_columns():
    print("Migrating Database: adding 'category' and 'extracted_entities' columns to 'documents' table...")
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE documents ADD COLUMN category VARCHAR(50);"))
            print("Successfully added 'category' column!")
        except Exception as e:
            print("Column 'category' may already exist.")
            
        try:
            conn.execute(text("ALTER TABLE documents ADD COLUMN extracted_entities JSON;"))
            print("Successfully added 'extracted_entities' column!")
        except Exception as e:
            print("Column 'extracted_entities' may already exist.")
            
        conn.commit()

if __name__ == "__main__":
    add_intelligence_columns()
