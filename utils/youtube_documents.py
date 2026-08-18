from langchain_core.documents import Document


def transcript_to_documents(transcript, video_id):

    documents = []

    for snippet in transcript:

        document = Document(
            page_content=snippet.text,
            metadata={
                "video_id": video_id,
                "start": snippet.start,
                "duration": snippet.duration
            }
        )

        documents.append(document)

    return documents