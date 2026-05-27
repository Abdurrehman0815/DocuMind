# DocuMind - AI Life Admin

DocuMind is an intelligent, full-stack AI Document Manager that acts as your personal life admin. It automatically processes your uploaded documents (bills, receipts, insurance policies, etc.), categorizes them, extracts important entities, and sends automated WhatsApp reminders before deadlines.

## Key Features
- **Computer Vision OCR**: Automatically extracts raw text from uploaded images (JPG, PNG) and PDFs.
- **AI Classification & Entity Extraction**: Uses `Groq (Llama 3.1 8B)` to categorize documents and cleanly extract due dates, amounts, and account numbers.
- **Semantic Math Search**: Queries documents using a `paraphrase-multilingual-MiniLM` vector embedding engine powered by PostgreSQL `pgvector`.
- **Multilingual AI Assistant**: Chat with your documents in English, Hindi, or Tamil using Local RAG.
- **Smart WhatsApp Reminders**: Runs a background cron job using `apscheduler` and Twilio to ping your phone when a deadline approaches with urgency scoring (CRITICAL, HIGH, MEDIUM).
- **Glassmorphism UI**: Beautiful, fully responsive frontend built with React, TailwindCSS, and Lucide Icons.

## Tech Stack
- **Frontend**: React, Vite, TailwindCSS, React Router
- **Backend**: FastAPI, SQLAlchemy, APScheduler
- **AI/ML**: Groq API (Llama 3.1), HuggingFace Transformers, EasyOCR, PyMuPDF
- **Database & Storage**: Supabase (PostgreSQL with `pgvector`), Supabase Storage
- **Notifications**: Twilio API

## How to Run

### Backend
1. Navigate to the `backend` folder.
2. Install dependencies: `pip install -r requirements.txt`
3. Fill out the `.env` file with your Supabase and Twilio credentials.
4. Run the server: `python -m uvicorn app.main:app --reload`

### Frontend
1. Navigate to the `frontend` folder.
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`


