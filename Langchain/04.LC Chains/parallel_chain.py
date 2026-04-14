from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

load_dotenv()

model1 = ChatOpenAI(model="gpt-3.5-turbo")
model2 = ChatOpenAI(model="gpt-4")  

prompt1 = PromptTemplate(
    template="Generate short and simple notes about {topic}",
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template = "Generate 5 short questions answers about the following text {topic}",
    input_variables=['topic']
)

prompt3 = PromptTemplate(
    template="Merge the provided notes and quiz into a single document . notes: {notes} quiz: {quiz}",
    input_variables=['notes', 'quiz']   
)

parser = StrOutputParser()

parallel_chain = RunnableParallel(
    {
    "notes": prompt1 | model1 | parser,
    "quiz": prompt2 | model2 | parser
    }
)

merge_chain = prompt3 | model1 | parser

chain = parallel_chain | merge_chain

response = chain.invoke({"topic": "space exploration"})

# print(response)

chain.get_graph().print_ascii()

