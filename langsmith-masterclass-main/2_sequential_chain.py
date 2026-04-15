from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

os.environ['langchain_project'] = 'llm deq app'

load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model = ChatOpenAI( temperature=0.9, model='gpt-3.5-turbo' )

model2 = ChatOpenAI( temperature=0.5, model='gpt-4o' )

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model2 | parser

config = {
    'tags': ['sequential chain', 'demo', 'Nikhil'],
    'metadata': {
        'model1': 'gpt-3.5',
        'author': 'Nikhil',
    }
}

result = chain.invoke({'topic': 'Unemployment in India'},config=config)

print(result)
