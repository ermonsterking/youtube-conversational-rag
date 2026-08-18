from retrieval.retriever import retrieve_documents


video_id = "kFHSf2oS5l0"

query = "What is an aircraft carrier?"

documents = retrieve_documents(
    query=query,
    video_id=video_id,
    k=4
)

print(f"\nRetrieved {len(documents)} documents\n")

for i, document in enumerate(documents, start=1):

    print("=" * 80)
    print(f"RESULT {i}")
    print("=" * 80)

    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)