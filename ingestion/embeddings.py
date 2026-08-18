import os
from typing import List

from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from langchain_core.embeddings import Embeddings


load_dotenv()


class HuggingFaceAPIEmbeddings(Embeddings):

    def __init__(self, model="BAAI/bge-m3"):

        self.model = model

        self.client = InferenceClient(
            api_key=os.getenv("HF_TOKEN")
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:

        embeddings = []

        for text in texts:

            embedding = self.client.feature_extraction(
                text,
                model=self.model
            )

            embeddings.append(embedding.tolist())

        return embeddings

    def embed_query(self, text: str) -> List[float]:

        embedding = self.client.feature_extraction(
            text,
            model=self.model
        )

        return embedding.tolist()

if __name__ == "__main__":

    embeddings = HuggingFaceAPIEmbeddings()

    documents = embeddings.embed_documents([
        "A neural network is a mathematical model inspired by the brain.",
        "Gradient descent is an optimization algorithm."
    ])

    query = embeddings.embed_query(
        "What is a neural network?"
    )

    print("Number of document embeddings:", len(documents))
    print("Document vector dimension:", len(documents[0]))

    print("Query vector dimension:", len(query))