from retrieval.retriever import retrieve_documents
from llm.groq_model import get_llm


def generate_answer(query, video_id, chat_history=None):

    if chat_history is None:
        chat_history = []

    llm = get_llm()

    # -----------------------------------------
    # Step 1: Build conversation history
    # -----------------------------------------

    history_text = ""

    for message in chat_history:

        role = message["role"]
        content = message["content"]

        history_text += f"{role}: {content}\n"


    # -----------------------------------------
    # Step 2: Create standalone retrieval query
    # -----------------------------------------

    if history_text:

        rewrite_prompt = f"""
You are a query rewriting assistant.

The user is asking questions about a YouTube video.

Rewrite the user's latest question into a standalone
question that can be understood without the previous
conversation.

Do NOT answer the question.

Preserve the user's meaning.

Conversation history:
-------------------

{history_text}

Latest question:
----------------

{query}

Standalone question:
"""

        rewrite_response = llm.invoke(rewrite_prompt)

        retrieval_query = rewrite_response.content.strip()

    else:

        retrieval_query = query


    # -----------------------------------------
    # Step 3: Retrieve relevant documents
    # -----------------------------------------

    documents = retrieve_documents(
        query=retrieval_query,
        video_id=video_id,
        k=4
    )


    if not documents:

        return {
            "answer": "I couldn't find relevant information in this video.",
            "sources": []
        }


    # -----------------------------------------
    # Step 4: Build transcript context
    # -----------------------------------------

    context = "\n\n".join(
        document.page_content
        for document in documents
    )


    # -----------------------------------------
    # Step 5: Generate final answer
    # -----------------------------------------

    prompt = f"""
You are a YouTube video assistant.

Answer the user's question using ONLY the provided
transcript context.

IMPORTANT RULES:

1. Do not use outside knowledge.
2. Do not invent facts.
3. Preserve the meaning of the transcript.
4. Answer clearly and naturally.
5. If the answer is not available in the transcript,
   say:

"I couldn't find the answer in the provided video."

Transcript context:
-------------------

{context}

-------------------

Conversation history:
-------------------

{history_text}

-------------------

User's question:
{query}

Answer:
"""

    response = llm.invoke(prompt)


    # -----------------------------------------
    # Step 6: Build unique sources
    # -----------------------------------------

    sources = []
    seen = set()

    for document in documents:

        start = document.metadata["start"]
        end = document.metadata["end"]
        video_id = document.metadata["video_id"]

        key = (
            video_id,
            round(start, 2),
            round(end, 2)
        )

        if key in seen:
            continue

        seen.add(key)

        sources.append({
            "start": start,
            "end": end,
            "video_id": video_id
        })


    return {
        "answer": response.content,
        "sources": sources
    }