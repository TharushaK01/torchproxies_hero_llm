import os
import json
import chromadb
import re
from openai import OpenAI
from dotenv import load_dotenv

# Initialize Environment Variable Engine Configurations
load_dotenv()

# Path to your knowledge documents directory
KNOWLEDGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../knowledge"))

# Initialize OpenRouter Client wrapper mapped against native OpenRouter targets
openrouter_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

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
            
            print(f"🧠 Generating vector embeddings via OpenRouter for: {file_name}...")
            embed_response = openrouter_client.embeddings.create(
                model="nvidia/llama-nemotron-embed-vl-1b-v2:free",
                input=content
            )
            embedding = embed_response.data[0].embedding
            
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


def chunk_markdown(text, max_chars=1000):
    """Splits markdown text into logical chunks based on sections and paragraphs."""
    sections = re.split(r'(?=\n###? )', text)
    chunks = []
    for section in sections:
        section = section.strip()
        if not section:
            continue
        if len(section) > max_chars:
            paragraphs = section.split("\n\n")
            current_chunk = ""
            for para in paragraphs:
                if len(current_chunk) + len(para) < max_chars:
                    current_chunk += para + "\n\n"
                else:
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())
                    current_chunk = para + "\n\n"
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
        else:
            chunks.append(section)
    return chunks

def run_ingestion():
    print("🚀 Starting Smart Vector Embedding Ingestion Pipeline...")
    
    DB_PATH = os.path.abspath("./chroma_db")
    client = chromadb.PersistentClient(path=DB_PATH)
    
    try:
        client.delete_collection(name="proxy_knowledge")
    except Exception:
        pass
        
    collection = client.get_or_create_collection(name="proxy_knowledge")
    TARGET_KNOWLEDGE_DIR = os.path.abspath("./knowledge")
    
    total_chunks_created = 0
    
    if not os.path.exists(TARGET_KNOWLEDGE_DIR):
        os.makedirs(TARGET_KNOWLEDGE_DIR)
        return {"chunks_processed": 0, "status": "knowledge_dir_created"}
    
    for filename in os.listdir(TARGET_KNOWLEDGE_DIR):
        if filename.endswith(".md"):
            file_path = os.path.join(TARGET_KNOWLEDGE_DIR, filename)
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
                
                chunks = chunk_markdown(file_content)
                print(f"✂️ Split {filename} into {len(chunks)} fragments.")
                
                for idx, chunk_text in enumerate(chunks):
                    chunk_id = f"chunk_{filename.replace('.', '_')}_{idx}"
                    
                    # Request embedding vectors via OpenRouter cloud infrastructure
                    embed_response = openrouter_client.embeddings.create(
                        model="nvidia/llama-nemotron-embed-vl-1b-v2:free",
                        input=chunk_text
                    )
                    embedding_vector = embed_response.data[0].embedding
                    
                    # Upsert vector array into local Chroma collection
                    collection.upsert(
                        ids=[chunk_id],
                        embeddings=[embedding_vector],
                        documents=[chunk_text],
                        metadatas=[{
                            "source": filename, 
                            "chunk_index": idx,
                            "type": "documentation"
                        }]
                    )
                    total_chunks_created += 1
                    
            except Exception as e:
                print(f"❌ Failed to process vector matrix for {filename}: {str(e)}")
                continue

    print(f"🏁 Vector Database update complete! Generated {total_chunks_created} embeddings.")
    return {
        "chunks_processed": total_chunks_created,
        "status": "completed_successfully"
    }

if __name__ == "__main__":
    run_ingestion()