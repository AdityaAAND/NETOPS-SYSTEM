#Create chromaDB ingestion



from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

documents= []
for file in Path("data").rglob("*.txt"):
    loader = TextLoader(str(file))
    documents.extend(loader.load())

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("Knowledge base created.")