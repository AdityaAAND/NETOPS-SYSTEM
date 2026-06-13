# Import Chroma vector database
from langchain_chroma import Chroma

# Import embedding model wrapper
from langchain_huggingface import HuggingFaceEmbeddings


# ---------------------------------------------------
# STEP 1: Load embedding model
# ---------------------------------------------------
# This converts text into vectors (numerical representations)
# Similar meanings → similar vectors
#
# Example:
# "OSPF neighbor reset"
# and
# "OSPF adjacency instability"
#
# will have similar embeddings.
#
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ---------------------------------------------------
# STEP 2: Connect to existing ChromaDB
# ---------------------------------------------------
# We are NOT creating a database here.
#
# We are loading the one we created earlier
# inside the chroma_db folder.
#
db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)


# ---------------------------------------------------
# STEP 3: Create search query
# ---------------------------------------------------
# This simulates an alert coming from Prometheus
# or Alertmanager.
#
query = """
CPU utilization 98%
OSPF neighbor resets
Packet loss
"""


# ---------------------------------------------------
# STEP 4: Search ChromaDB
# ---------------------------------------------------
# similarity_search()
#
# Converts query → embedding
# Compares against all document embeddings
# Returns the most relevant documents.
#
# k=5 means:
# return top 5 matching documents.
#
results = db.similarity_search(
    query,
    k=5
)


# ---------------------------------------------------
# STEP 5: Display results
# ---------------------------------------------------
#
# enumerate() gives:
#
# Result 1
# Result 2
# Result 3
#
for i, doc in enumerate(results, start=1):

    print(f"\nResult {i}")

    print("=" * 60)

    # Show file source
    print("Source:", doc.metadata.get("source"))

    print("\n")

    # Show first 300 characters
    print(doc.page_content[:300])

    print("\n")