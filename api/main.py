from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ingestion.youtube_vector_store import create_youtube_vector_store
from chains.rag_chain import generate_answer


app = FastAPI(
    title="YouTube Conversational RAG API",
    description="Backend API for the YouTube Conversational RAG chatbot",
    version="1.0.0"
)


# --------------------------------------------------
# Request Models
# --------------------------------------------------

class LoadVideoRequest(BaseModel):
    video_id: str


class AskRequest(BaseModel):
    video_id: str
    question: str


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "ok",
        "service": "YouTube Conversational RAG API"
    }


# --------------------------------------------------
# Load Video
# --------------------------------------------------

@app.post("/load-video")
def load_video(request: LoadVideoRequest):

    try:

        create_youtube_vector_store(
            request.video_id
        )

        return {
            "success": True,
            "video_id": request.video_id,
            "message": "Video loaded successfully."
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not load video: {str(e)}"
        )


# --------------------------------------------------
# Ask Question
# --------------------------------------------------

@app.post("/ask")
def ask_question(request: AskRequest):

    try:

        result = generate_answer(
            query=request.question,
            video_id=request.video_id
        )

        return {
            "success": True,
            "video_id": request.video_id,
            "question": request.question,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not generate answer: {str(e)}"
        )
# --------------------------------------------------
# Root Endpoint
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "YouTube Conversational RAG API is running",
        "docs": "/docs",
        "health": "/health"
    }