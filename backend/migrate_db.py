from app.config.database import engine
from sqlalchemy import text

def add_extracted_text_column():
    print("Migrating Database: adding 'extracted_text' column to 'documents' table...")
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE documents ADD COLUMN extracted_text TEXT;"))
            conn.commit()
            print("Successfully added 'extracted_text' column!")
        except Exception as e:
            if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
                print("Column 'extracted_text' already exists. Skipping.")
            else:
                print(f"Error migrating: {e}")

if __name__ == "__main__":
    add_extracted_text_column()
