from llm.groq_model import get_llm


llm = get_llm()

response = llm.invoke(
    "What is a neural network? Explain briefly."
)

print(response.content)