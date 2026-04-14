from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatOpenAI(model="gpt-4")

result = model.invoke("What is the capital of India?")

print(model.invoke("what was my previous question?"))
