from utils.youtube_transcript import get_transcript
from utils.youtube_documents import transcript_to_documents


video_id = "kFHSf2oS5l0"

transcript = get_transcript(video_id)

documents = transcript_to_documents(
    transcript,
    video_id
)

print("Number of documents:", len(documents))

print("\nFirst document:")
print(documents[0].page_content)

print("\nMetadata:")
print(documents[0].metadata)