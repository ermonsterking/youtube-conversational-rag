# 🎥 YouTube Conversational RAG Chatbot

A conversational AI chatbot that allows users to paste a YouTube video URL and ask questions about the video's content.

The application retrieves the video's transcript, converts it into timestamp-aware chunks, generates semantic embeddings using BGE-M3, stores them in ChromaDB, retrieves relevant transcript sections, and uses a Groq-hosted LLM to generate grounded answers.

## 🚀 Features

- Paste a YouTube video URL
- Automatic YouTube video ID extraction
- Automatic transcript retrieval
- Supports automatically generated transcripts
- Timestamp-aware transcript documents
- Semantic chunking
- BGE-M3 embeddings through Hugging Face
- ChromaDB vector database
- Video-specific retrieval
- Conversational follow-up questions
- Query contextualization using chat history
- Groq LLM for answer generation
- Answers grounded only in the video transcript
- Clickable YouTube timestamp sources
- Video caching to avoid unnecessary reprocessing
- Streamlit web interface
- Basic error handling
- New Video / Clear Chat functionality

## 🏗️ Architecture

```text
                YouTube URL
                     │
                     ▼
              Video ID Extraction
                     │
                     ▼
             YouTube Transcript
                     │
                     ▼
          Timestamp-aware Documents
                     │
                     ▼
               Text Chunking
                     │
                     ▼
                BGE-M3
              Embeddings
                     │
                     ▼
                 ChromaDB
                     │
                     │
User Question ───────┤
                     │
Chat History ────────┤
                     ▼
             Query Contextualization
                     │
                     ▼
              Semantic Retrieval
                     │
                     ▼
          Relevant Transcript Chunks
                     │
                     ▼
                 Groq LLM
                     │
                     ▼
            Grounded Answer
                     │
                     ▼
          Answer + Video Sources
