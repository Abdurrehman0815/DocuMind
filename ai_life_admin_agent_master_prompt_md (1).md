# AI Life Admin Agent — MASTER PROJECT PROMPT

## Overview

Build a production-ready AI-powered Life Administration Assistant using modern AI engineering practices.

The system should help users manage:

- bills
- insurance documents
- personal files
- deadlines
- subscriptions
- reminders
- forms
- financial documents
- important dates

The project must focus on:

- RAG architecture
- intelligent document understanding
- semantic memory
- open-source LLMs
- vector databases
- agentic workflows
- scalable backend systems

DO NOT include browser automation or Selenium/Playwright automation features.

---

# PROJECT GOAL

The application acts as an AI-powered personal life management assistant.

Users can:

- upload documents
- ask questions about uploaded files
- retrieve important dates
- receive smart reminders
- search semantically
- organize personal information intelligently

The AI system should:

- understand uploaded documents
- extract important information
- create embeddings
- store contextual memory
- answer contextual questions using RAG
- prioritize deadlines intelligently

---

# CORE FEATURES

## 1. Authentication System

Implement:

- secure JWT authentication
- signup/login
- password hashing
- protected APIs
- session handling

Preferred stack:

- FastAPI auth
- Supabase auth OR JWT-based auth

---

## 2. Document Upload System

Users should upload:

- PDFs
- images
- screenshots
- scanned documents

Supported formats:

- pdf
- png
- jpg
- jpeg

Features:

- drag-and-drop upload
- upload progress
- document previews

---

## 3. OCR + Document Parsing

Implement OCR pipeline using:

- PaddleOCR OR Tesseract OCR

Extract:

- raw text
- tables
- dates
- names
- amounts
- addresses
- identifiers

The parser should support:

- invoices
- bills
- insurance documents
- receipts
- ID proofs
- forms

---

## 4. AI Document Classification

Automatically classify uploaded files into categories:

- electricity bill
- insurance
- subscription
- tax document
- bank statement
- scholarship document
- rent receipt
- medical document

Use:

- HuggingFace transformers
- DistilBERT OR MiniLM

Store classification metadata in database.

---

## 5. Information Extraction Engine

Extract important entities:

- due dates
- expiry dates
- payment amounts
- provider names
- account identifiers
- policy numbers

Store structured JSON output.

Example:

```json
{
  "document_type": "Insurance",
  "expiry_date": "2026-09-10",
  "provider": "HDFC ERGO",
  "policy_number": "XXXXXX"
}
```

---

## 6. RAG Architecture

Implement complete Retrieval-Augmented Generation pipeline.

### RAG Flow

1. Extract text
2. Chunk documents
3. Generate embeddings
4. Store vectors
5. Retrieve relevant chunks
6. Send retrieved context to LLM
7. Generate grounded answers

---

## 7. Embedding System

Use HuggingFace embedding models.

Recommended:

- BAAI/bge-small-en
- all-MiniLM-L6-v2

Requirements:

- semantic similarity search
- optimized chunking
- metadata-aware retrieval

---

## 8. Vector Database

Use one:

- ChromaDB
- Qdrant
- FAISS

Store:

- embeddings
- metadata
- chunk references
- timestamps

Support:

- semantic search
- contextual retrieval
- filtering

---

## 9. Open Source LLM Integration

Use Ollama for local LLM inference.

Supported models:

- Llama 3
- Mistral
- DeepSeek
- Phi-3

The system should:

- answer questions contextually
- summarize documents
- explain documents simply
- retrieve important details accurately

---

## 10. AI Reminder Engine

Create intelligent reminder system.

The AI should:

- detect deadlines automatically
- identify urgency
- prioritize reminders

Reminder categories:

- bill due dates
- insurance renewals
- subscription expiry
- scholarship deadlines
- document expiry

Features:

- dashboard reminders
- email notifications
- in-app alerts

---

## 11. Semantic Search System

Users should search naturally.

Examples:

- "Show unpaid bills"
- "Find insurance documents"
- "Which documents expire next month?"
- "Show all electricity bills"

Use:

- vector similarity search
- metadata filtering
- semantic retrieval

---

## 12. AI Chat Assistant

Create conversational assistant connected to RAG pipeline.

Features:

- memory-aware conversation
- contextual responses
- document-grounded answers
- follow-up understanding

Example:

**User:**

“When does my insurance expire?”

**Assistant:**

“Your HDFC ERGO insurance expires on September 10, 2026.”

---

## 13. Dashboard UI

Frontend should include:

- document overview
- upload center
- reminders section
- AI assistant
- semantic search
- categorized documents

Use:

- React.js
- Tailwind CSS
- ShadCN UI

Design goals:

- modern
- minimal
- responsive
- professional
- AI-product style UI

---

# ADVANCED FEATURES

## 14. Smart Summarization

Generate:

- short summaries
- bullet summaries
- action items

Example:

“This bill is due in 3 days.”

---

## 15. Deadline Priority Scoring

Implement AI-based urgency scoring.

Example:

- overdue → critical
- due tomorrow → high
- due next month → medium

---

## 16. Multi-Language Support

Support:

- English
- Tamil
- Hindi

Use multilingual embeddings where needed.

---

# SYSTEM ARCHITECTURE

## Frontend

- React.js
- Tailwind CSS
- ShadCN UI

## Backend

- FastAPI

## AI Layer

- LangChain
- LangGraph

## LLM Layer

- Ollama

## Embedding Layer

- HuggingFace embeddings

## Vector DB

- ChromaDB OR Qdrant

## Database

- PostgreSQL OR Supabase

## Storage

- Supabase Storage OR local object storage

---

# DATABASE DESIGN

Create tables for:

- users
- documents
- embeddings
- reminders
- chats
- extracted_entities

Relationships should be normalized.

---

# API REQUIREMENTS

Create APIs for:

- authentication
- upload
- OCR processing
- embeddings generation
- RAG querying
- reminders
- semantic search
- AI chat

Use:

- async FastAPI
- modular architecture
- proper validation

---

# PROJECT STRUCTURE

```txt
backend/
│
├── app/
├── routes/
├── services/
├── rag/
├── embeddings/
├── ocr/
├── llm/
├── vector_db/
├── models/
├── utils/
├── middleware/
└── config/

frontend/
│
├── components/
├── pages/
├── hooks/
├── services/
├── layouts/
├── store/
└── utils/
```

---

# DEVELOPMENT PHASES

# PHASE 1 — Project Setup

## Tasks

- initialize frontend/backend
- setup FastAPI
- setup React
- configure Tailwind
- configure database
- setup environment variables

## Testing

- verify frontend/backend communication
- verify database connection

---

# PHASE 2 — Authentication

## Tasks

- signup/login
- JWT handling
- protected routes

## Testing

- successful auth flow
- token validation

---

# PHASE 3 — File Upload System

## Tasks

- upload APIs
- frontend uploader
- file storage

## Testing

- upload validation
- preview testing

---

# PHASE 4 — OCR Pipeline

## Tasks

- OCR extraction
- text cleaning
- parser pipeline

## Testing

- extraction accuracy
- multilingual OCR

---

# PHASE 5 — Embedding + Vector DB

## Tasks

- chunking
- embedding generation
- vector storage

## Testing

- semantic retrieval accuracy

---

# PHASE 6 — RAG System

## Tasks

- retriever pipeline
- contextual prompts
- grounded generation

## Testing

- question-answer correctness

---

# PHASE 7 — AI Chat Assistant

## Tasks

- chat UI
- memory handling
- conversational flow

## Testing

- contextual continuity

---

# PHASE 8 — Reminder Engine

## Tasks

- deadline detection
- reminders
- urgency scoring

## Testing

- reminder accuracy

---

# PHASE 9 — Dashboard UI

## Tasks

- analytics
- categorized docs
- reminders page
- AI assistant interface

## Testing

- responsive UI
- UX improvements

---

# PHASE 10 — Optimization + Deployment

## Tasks

- Dockerization
- caching
- API optimization
- deployment

## Deployment

- frontend → Vercel
- backend → Render/Railway
- vector DB → Qdrant Cloud

---

# CODING STANDARDS

Requirements:

- modular code
- reusable components
- clean architecture
- proper comments
- type safety
- environment configs
- scalable structure

---

# SECURITY REQUIREMENTS

Implement:

- JWT validation
- rate limiting
- secure uploads
- file validation
- API protection
- encrypted secrets

---

# UI/UX REQUIREMENTS

Design style:

- modern AI SaaS
- glassmorphism optional
- clean spacing
- responsive
- dashboard-centric

Use:

- cards
- charts
- AI-style chat interface

---

# FINAL GOAL

The final application should feel like:

- a real AI product
- production-ready SaaS
- intelligent personal assistant
- scalable AI platform

The system must demonstrate:

- RAG engineering
- vector databases
- open-source LLM integration
- document intelligence
- semantic retrieval
- AI memory systems
- full-stack AI engineering

---

# IMPLEMENTATION INSTRUCTIONS FOR AI CODING AGENT

Build the project step-by-step phase-wise.

After completing each phase:

1. Explain completed work
2. Provide testing steps
3. Verify functionality
4. Only then move to next phase

Do not skip phases.

Maintain production-grade architecture throughout the project.

Ensure all APIs are modular, scalable, and secure.

Prioritize clean code, maintainability, and extensibility.

The final output should be deployable and portfolio-ready.

