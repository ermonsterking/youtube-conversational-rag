from utils.youtube_transcript import get_transcript
from utils.youtube_documents import transcript_to_documents
from ingestion.youtube_splitter import split_youtube_documents


video_id = "kFHSf2oS5l0"

transcript = get_transcript(video_id)

documents = transcript_to_documents(
    transcript,
    video_id
)

chunks = split_youtube_documents(documents)

print("Original documents:", len(documents))
print("Final chunks:", len(chunks))

print("\nFirst chunk:")
print(chunks[0].page_content)

print("\nMetadata:")
print(chunks[0].metadata)