from pathlib import Path

#load the 37 documents


documents = []


for file in Path("data").rglob("*.txt"):
    with open(file ,"r", encoding="utf-8") as f:
        documents.append(
            {
            "source": str(file),
            "content": f.read()
            }
        
        )

print(f"Loaded {len(documents)} documents")

for doc in documents[:3]:
    print(doc["source"])