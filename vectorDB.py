import uuid
import chromadb
import json

client = chromadb.PersistentClient('vectorstore')
collection = client.get_or_create_collection(name="medicines")

with open('modified_indian_meds.json', 'r') as f:
    df = json.load(f)

if not collection.count():
    for item in df:
        # Assuming each item in the JSON contains "description", "links" and "dosage"
        description = item.get("description", "")
        links = item.get("url", "")
        dosage = item.get("Directions for Use")

        # Add data to ChromaDB collection
        collection.add(
            documents=[description],
            metadatas=[{"links": links, "dosage": dosage}],
            ids=[str(uuid.uuid4())]
        )

    print("Data has been added to ChromaDB!")
