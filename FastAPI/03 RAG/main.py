# rag_pipeline.py

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────
# STEP 1 — RAW DOCUMENTS
# ─────────────────────────────────────────
documents = [
    "Project AMIGO Q3 for client Belden is currently At Risk. Risk R1: Budget overrun with severity High.",
    "Project AMIGO Q2 for client Belden is On Track. All milestones completed on time.",
    "Risk R2 in project AMIGO Q3: Resource shortage with severity Medium. Mitigation: hiring in progress.",
    "Client Belden has 3 active projects. Overall portfolio health is Yellow.",
    "Project Phoenix for client Acme is Completed. Final delivery was on 1st March 2025.",
]

# ─────────────────────────────────────────
# STEP 2 — CHUNK
# ─────────────────────────────────────────
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30)
chunks = splitter.create_documents(documents)

print(f"✅ Total chunks created: {len(chunks)}")

# ─────────────────────────────────────────
# STEP 3 — EMBED + STORE
# ─────────────────────────────────────────
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("✅ Embeddings stored in ChromaDB")

# ─────────────────────────────────────────
# STEP 4 — RETRIEVE
# ─────────────────────────────────────────
query = "What are the risks in project AMIGO Q3?"

retrieved_chunks = vectorstore.similarity_search(query, k=3)
context = "\n\n".join([doc.page_content for doc in retrieved_chunks])

print(f"\n== Retrieved Context for: '{query}' ==")
print(context)

# ─────────────────────────────────────────
# STEP 5 — GENERATE
# ─────────────────────────────────────────
llm = ChatOpenAI(model="gpt-4o-mini")

messages = [
    SystemMessage(content="You are a helpful assistant. Answer only using the context provided. If the answer isn't in the context, say you don't know."),
    HumanMessage(content=f"Context:\n{context}\n\nQuestion: {query}")
]

response = llm.invoke(messages)

print("\n== LLM Answer ==")
print(response.content)