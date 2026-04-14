from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence

load_dotenv()

prompt = PromptTemplate(
    template="Write a joke about {topic}",
    input_variables=['topic']
)

model = ChatOpenAI(model="gpt-3.5-turbo")

parser = StrOutputParser()


prompt2 = PromptTemplate(
    template="first state and then Explain the following joke: {joke}",
    input_variables=['joke']
)


chain = RunnableSequence(
    prompt , model , parser ,prompt2 , model , parser
)
response = chain.invoke({"topic": "programming"})
print(response)
