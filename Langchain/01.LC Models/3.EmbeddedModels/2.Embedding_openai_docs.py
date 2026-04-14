from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embedding = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=32)

documents = [
    "What is the capital of India?",
    "What is the capital of France?",
    "What is the capital of Germany?"
]

response = embedding.embed_documents(documents)

print(str(response))