from ingestion.youtube_vector_store import create_youtube_vector_store


video_id = "kFHSf2oS5l0"

vector_store = create_youtube_vector_store(
    video_id
)

print("\nYouTube video successfully stored in ChromaDB!")