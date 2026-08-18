from ingestion.youtube_vector_store import create_youtube_vector_store


video_id = "kFHSf2oS5l0"

print("\n--- FIRST CALL ---")

create_youtube_vector_store(video_id)


print("\n--- SECOND CALL ---")

create_youtube_vector_store(video_id)