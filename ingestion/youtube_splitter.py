from langchain_core.documents import Document


def split_youtube_documents(
    documents,
    chunk_size=1000,
    chunk_overlap=150
):
    chunks = []

    current_text = []
    current_length = 0
    current_start = None

    for document in documents:

        text = document.page_content.strip()

        if not text:
            continue

        start = document.metadata["start"]
        duration = document.metadata["duration"]
        end = start + duration

        # Start a new chunk
        if current_start is None:
            current_start = start

        current_text.append(text)
        current_length += len(text) + 1

        # Chunk is large enough
        if current_length >= chunk_size:

            chunk_text = " ".join(current_text)

            chunks.append(
                Document(
                    page_content=chunk_text,
                    metadata={
                        "video_id": document.metadata["video_id"],
                        "start": current_start,
                        "end": end
                    }
                )
            )

            # Keep last portion for overlap
            overlap_text = chunk_text[-chunk_overlap:]

            current_text = [overlap_text]
            current_length = len(overlap_text)
            current_start = start

    # Add remaining text
    if current_text:

        chunk_text = " ".join(current_text)

        last_document = documents[-1]

        chunks.append(
            Document(
                page_content=chunk_text,
                metadata={
                    "video_id": last_document.metadata["video_id"],
                    "start": current_start,
                    "end": (
                        last_document.metadata["start"]
                        + last_document.metadata["duration"]
                    )
                }
            )
        )

    return chunks