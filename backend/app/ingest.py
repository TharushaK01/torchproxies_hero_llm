import ollama
import chromadb

# Connect to your persistent database store
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="proxy_knowledge")

def instant_vector_upsert(doc_id: str, text: str, category: str):
    """Generates an embedding and instantly updates/inserts into ChromaDB."""
    try:
        response = ollama.embed(model="nomic-embed-text", input=text)
        embedding = response["embeddings"][0]
        
        collection.upsert(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[{"category": category}]
        )
        print(f"✅ Instant Sync Success: '{doc_id}' is live in the Vector DB.")
    except Exception as e:
        print(f"❌ Ingestion failed: {str(e)}")

if __name__ == "__main__":
    # Add your real, custom proxy documentation right here whenever needed!
    print("Ready to ingest real data. Call instant_vector_upsert() below.")
    
    # Example of adding a real documentation item:
    instant_vector_upsert(
        doc_id="doc_real_01",
        text="Our server location infrastructure is hosted in Ashburn (US-East), Frankfurt (EU-Central), and Singapore (AP-Southeast).",
        category="infrastructure"
    )