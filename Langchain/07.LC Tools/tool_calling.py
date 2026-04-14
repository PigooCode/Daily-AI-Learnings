from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
import requests
from dotenv import load_dotenv

load_dotenv()

@tool
def multiply(a:int , b:int) -> int:
    """Given two numbers , return their product."""
    return a * b
 
# print(multiply.invoke({'a': 5, 'b': 3}))

llm = ChatOpenAI()

llm_2 = llm.bind_tools([multiply])

result = llm_2.invoke("What is the product of 5 and 3?")

print(result.tool_calls)