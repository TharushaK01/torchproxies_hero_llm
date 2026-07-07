import os
import ollama
import chromadb

# Path to your knowledge documents directory
KNOWLEDGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../knowledge"))

# Connect to the persistent ChromaDB database folder
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="proxy_knowledge")

def batch_import_knowledge():
    """Scans the knowledge directory and syncs text/markdown files to ChromaDB."""
    if not os.path.exists(KNOWLEDGE_DIR):
        print(f"❌ Error: Knowledge folder not found at {KNOWLEDGE_DIR}")
        return

    print(f"📂 Scanning knowledge folder: {KNOWLEDGE_DIR}\n" + "-"*50)
    
    # Get all text and markdown files in the folder
    files = [f for f in os.listdir(KNOWLEDGE_DIR) if f.endswith(('.txt', '.md'))]
    
    if not files:
        print("⚠️ No .txt or .md files found in the knowledge directory.")
        return

    for file_name in files:
        file_path = os.path.join(KNOWLEDGE_DIR, file_name)
        
        # Use the filename (without extension) as the unique doc_id
        doc_id = os.path.splitext(file_name)[0]
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if not content:
                print(f"⏩ Skipping empty file: {file_name}")
                continue
                
            # Determine a simple category based on the file name
            category = "faq" if "faq" in file_name.lower() else "general"
            
            print(f"🧠 Generating vector embeddings for: {file_name}...")
            response = ollama.embed(model="nomic-embed-text", input=content)
            embedding = response["embeddings"][0]
            
            # Instantly insert or update the file contents inside ChromaDB
            collection.upsert(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[content],
                metadatas=[{"category": category, "source": file_name}]
            )
            print(f"✅ Successfully synced: '{doc_id}' into Vector DB.")
            
        except Exception as e:
            print(f"❌ Failed to process {file_name}: {str(e)}")
            
    print("-"*50 + "\n🎉 Batch import complete! Your custom database is updated.")

if __name__ == "__main__":
    batch_import_knowledge()