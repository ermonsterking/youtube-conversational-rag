from langchain_chroma import Chroma

from ingestion.embeddings import HuggingFaceAPIEmbeddings


def get_youtube_vector_store():

    embeddings = HuggingFaceAPIEmbeddings()

    vector_store = Chroma(
        persist_directory="./chroma_db",
        collection_name="youtube_videos",
        embedding_function=embeddings
    )

    return vector_store


def retrieve_documents(query, video_id, k=4):

    vector_store = get_youtube_vector_store()

    documents = vector_store.similarity_search(
        query,
        k=k,
        filter={
            "video_id": video_id
        }
    )

    return documents