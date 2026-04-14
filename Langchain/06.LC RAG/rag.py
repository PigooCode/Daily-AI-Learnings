from youtube_transcript_api import YouTubeTranscriptApi , TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv

load_dotenv()

# indexing 

video_id = "zwUSZD3t_BU"  # replace with your YouTube video ID

try:
    transcript_data = YouTubeTranscriptApi().fetch(video_id, languages=['en'])
    transcript = " ".join(chunk.text for chunk in transcript_data)
    # print(transcript_data) 

except TranscriptsDisabled:
    print("Transcripts are disabled for this video.")

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks= splitter.split_text(transcript)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = FAISS.from_texts(chunks, embeddings) 

# retrieval

retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

model = ChatOpenAI(model="gpt-3.5-turbo")

prompt = PromptTemplate(
    template="""
        You are a helpful assistant.
        Answer ONLY from the provided transcript context.
        If the context is insufficient, just say you don't know.
        Context: {context}
        Question: {question}
    """,
    input_variables=['context', 'question']
)

question = "is the topic of AI discussed im the video?"
context = retriever.invoke(question)

final_prompt = prompt.invoke({"context": context, "question": question})

ans = model.invoke(final_prompt)
print(ans.content)
