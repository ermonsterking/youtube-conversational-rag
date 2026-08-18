# 🎥 YouTube Conversational RAG

> A conversational AI assistant that lets users chat with any supported YouTube video using its transcript as the knowledge source.

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-green)](https://www.langchain.com/)
[![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-orange)](https://www.trychroma.com/)
[![Groq](https://img.shields.io/badge/LLM-Groq-red)](https://groq.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b?logo=streamlit)](https://streamlit.io/)
[![Hugging Face](https://img.shields.io/badge/Embeddings-Hugging%20Face-yellow?logo=huggingface)](https://huggingface.co/)

---

## 📌 Overview

**YouTube Conversational RAG** is a Retrieval-Augmented Generation application that allows users to interact with the content of a YouTube video through natural-language questions.

Instead of sending the entire transcript directly to an LLM, the application:

1. Extracts the YouTube video ID.
2. Retrieves the available transcript.
3. Converts transcript segments into timestamp-aware documents.
4. Splits the transcript into semantic chunks.
5. Generates embeddings using **BAAI/bge-m3**.
6. Stores the embeddings in **ChromaDB**.
7. Retrieves only the most relevant transcript chunks for a question.
8. Uses conversation history to understand follow-up questions.
9. Sends the retrieved context to a **Groq-hosted LLM**.
10. Generates a grounded answer with clickable YouTube timestamps.

The goal is to demonstrate a practical, end-to-end **Conversational RAG architecture** using modern GenAI tooling.

---

## ✨ Features

- 🎥 Accepts YouTube video URLs
- 🔗 Automatic YouTube video ID extraction
- 📝 Automatic transcript retrieval
- 🌐 Supports available automatically generated transcripts
- ⏱️ Timestamp-aware transcript processing
- ✂️ Transcript chunking
- 🧠 BGE-M3 semantic embeddings
- 🗄️ ChromaDB vector storage
- 🔎 Semantic similarity retrieval
- 🎯 Video-specific retrieval
- 💬 Conversational follow-up questions
- 🧩 Query contextualization using chat history
- ⚡ Groq LLM inference
- 📚 Clickable timestamp-based sources
- ♻️ Video caching to avoid unnecessary reprocessing
- 🆕 New Video / Clear Chat functionality
- 🖥️ Streamlit interface
- 🛡️ Basic error handling

---

# 🏗️ System Architecture

```text
                         YouTube URL
                              │
                              ▼
                    ┌──────────────────┐
                    │ Video ID Extract │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ YouTube Transcript│
                    └────────┬─────────┘
                             │
                             ▼
                  ┌───────────────────────┐
                  │ Timestamped Documents│
                  └───────────┬───────────┘
                              │
                              ▼
                       Text Chunking
                              │
                              ▼
                       BGE-M3 Embeddings
                              │
                              ▼
                         ChromaDB
                              │
                              │
                              │
          ┌───────────────────┴──────────────────┐
          │                                      │
          ▼                                      ▼
     User Question                         Chat History
          │                                      │
          └───────────────────┬──────────────────┘
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
                    Grounded Final Answer
                              │
                              ▼
                  Answer + Timestamp Sources
