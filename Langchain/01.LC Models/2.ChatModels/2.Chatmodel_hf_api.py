from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()

llm = HuggingFaceEndpoint(
                        repo_id="deepseek-ai/DeepSeek-R1",
                        # repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                        # huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN"),
                        task="text-generation")


model = ChatHuggingFace(llm = llm)

response = model.invoke("What is the capital of India?")

print(response.content)