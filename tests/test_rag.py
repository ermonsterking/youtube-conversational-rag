from chains.rag_chain import generate_answer


video_id = "kFHSf2oS5l0"

query = "What is an aircraft carrier?"

result = generate_answer(
    query=query,
    video_id=video_id
)

print("\nQUESTION:")
print(query)

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES:")

for source in result["sources"]:

    print(
        f"{source['start']:.2f}s - "
        f"{source['end']:.2f}s"
    )