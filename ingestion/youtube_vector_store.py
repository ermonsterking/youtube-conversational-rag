from langchain_chroma import Chroma

from utils.youtube_transcript import get_transcript
from utils.youtube_documents import transcript_to_documents
from ingestion.youtube_splitter import split_youtube_documents
from ingestion.embeddings import HuggingFaceAPIEmbeddings


COLLECTION_NAME = "youtube_videos"
PERSIST_DIRECTORY = "./chroma_db"


def get_vector_store():

    embeddings = HuggingFaceAPIEmbeddings()

    vector_store = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings
    )

    return vector_store


def video_exists(video_id):

    vector_store = get_vector_store()

    results = vector_store.get(
        where={
            "video_id": video_id
        },
        limit=1
    )

    return len(results["ids"]) > 0


def create_youtube_vector_store(video_id):

    # -----------------------------------------
    # Check if video already exists
    # -----------------------------------------

    if video_exists(video_id):

        print(f"Video {video_id} already exists in ChromaDB.")

        return get_vector_store()


    # -----------------------------------------
    # New video → get transcript
    # -----------------------------------------

    print(f"New video detected: {video_id}")
    print("Downloading transcript...")

    transcript = get_transcript(video_id)


    # -----------------------------------------
    # Convert transcript to Documents
    # -----------------------------------------

    documents = transcript_to_documents(
        transcript,
        video_id
    )

    print(
        f"Transcript snippets: {len(documents)}"
    )


    # -----------------------------------------
    # Create timestamp-aware chunks
    # -----------------------------------------

    chunks = split_youtube_documents(
        documents
    )

    print(
        f"Final chunks: {len(chunks)}"
    )


    # -----------------------------------------
    # Create embeddings
    # -----------------------------------------

    embeddings = HuggingFaceAPIEmbeddings()


    # -----------------------------------------
    # Store in ChromaDB
    # -----------------------------------------

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY,
        collection_name=COLLECTION_NAME
    )

    print(
        f"Video {video_id} successfully stored in ChromaDB."
    )

    return vector_store