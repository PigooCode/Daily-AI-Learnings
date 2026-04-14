from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline
from dotenv import load_dotenv
import os

load_dotenv()

llm = HuggingFacePipeline.from_model_id(
                        model_id="deepseek-ai/DeepSeek-R1",
                        # repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                        task="text-generation",
                        kwargs={"max_new_tokens": 100, "temperature": 0.7})


model = ChatHuggingFace(llm = llm)

response = model.invoke("What is the capital of India?")

print(response.content)