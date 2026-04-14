from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence, RunnableParallel

load_dotenv()

prompt1 = PromptTemplate(
    template="Write a tweet about {topic}",
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template="Write a linkedin Post about {topic}",  
    input_variables=['topic']
)

model = ChatOpenAI(model="gpt-3.5-turbo")

parser = StrOutputParser()

parallel_chain = RunnableParallel(
    { 'tweet': prompt1 | model | parser,
      'linkedin_post': prompt2 | model | parser
    }
)

response = parallel_chain.invoke({"topic": "AI in healthcare"})

print(response)