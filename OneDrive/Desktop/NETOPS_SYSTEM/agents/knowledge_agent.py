from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

class KnowledgeAgent():
    """Responsible for retrieving incidents,
    playbooks and network docs."""

    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name = "sentence-transformers/all-MiniLM-L6-v2"


        )
        #connect to chromadb
        self.db = Chroma(
            persist_directory = "./chroma_db",
            embedding_function = self.embeddings
        )
    def retrieve_context(self, alert, k=5):
        """
        Retrieve top-k relevant documents.
        """

        results = self.db.similarity_search(
            alert,
            k=k
        )

        return results