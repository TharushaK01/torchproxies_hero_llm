from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import os
import shutil
from pydantic import BaseModel
from typing import List, Dict, Any
import ollama
import chromadb
import json

app = FastAPI(title="Proxy Support AI Local Core Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.abspath("./chroma_db")
chroma_client = chromadb.PersistentClient(path=DB_PATH)

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Connect to the persistent ChromaDB database folder
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="proxy_knowledge")


# class ChatRequest(BaseModel):
#     # message: str
#     history: List[Dict[str, str]]


@app.get("/health")
async def health_check():
    return {"status": "online", "engine": "ollama-local"}


@app.post("/v1/ingest")
async def trigger_ingest():
    try:
        from backend.app.ingest import run_ingestion
        run_ingestion()

        return {
            "status": "success", 
            "message": "Vector database updated successfully", 
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@app.post("/v1/chat")
async def chat_endpoint(
    history: str = Form(...),
    file: UploadFile = File(None)  # Optional file upload
):
    try:
        chat_history = json.loads(history)
        user_messages =  [m for m in chat_history if m["role"] == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="No user message found in the request history.")
        latest_query = user_messages[-1]["content"]

        saved_file_path = None
        if file is not None and file.filename:
            saved_file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(saved_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        OFF_TOPIC_KEYWORDS = [
            "recipe", "cooking", "food", "dish", "meal", "ingredients", "chocolate chips", "pasta", "soup", "dessert", "bake", "grill", "fry", "boil", "roast", "saute", "stir-fry", "simmer",
            "sports", "game", "team", "player", "score", "sports", "football", "basketball", "soccer", "tennis", "baseball", "hockey",
            "entertainment", "movie", "film", "music", "concert", "song", "album", "artist", "celebrity", "show", "TV", "theater",
            "politics", "election", "government", "policy", "weather", "law", "president", "senator", "congress", "political party", "campaign", "vote", "legislation",
            "general", "news", "gossip", "trivia", "fun", "joke", "meme", "viral", "trend", "fashion", "lifestyle", "travel", "vacation", "holiday", "festival", "event"
        ]
        
        query_lower = latest_query.lower()

        is_generic_code = ("write a script" in query_lower or "how to scrape" in query_lower or "beautifulsoup" in query_lower or "selenium" in query_lower or "python code" in query_lower or "javascript code" in query_lower)
        has_proxy_context = ("proxy" in query_lower or "proxies" in query_lower or "network" in query_lower or "vpn" in query_lower or "tor" in query_lower)


        # If it's a completely off-topic keyword, or generic scraping code without proxy usage:
        if any(keyword in query_lower for keyword in OFF_TOPIC_KEYWORDS) or (is_generic_code and not has_proxy_context):
            def guardrail_fallback():
                yield f"data: {json.dumps({'response': 'I apologize, but as the Torch Proxies assistant, I can only help you with our proxy services, service pricing plans, and technical proxy configuration adjustments.'})}\n\n"
            return StreamingResponse(guardrail_fallback(), media_type="text/event-stream")


        # FIX: Generate embedding using nomic-embed-text and the correct .embed() syntax
        query_embedding_resp = ollama.embed(model="nomic-embed-text", input=latest_query)
        query_embedding = query_embedding_resp["embeddings"][0]
        
        
        # Search ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=2
        )
        
        # Combine the retrieved document matches into a single text block
        retrieved_context = ""
        if results and results['documents'] and results['documents'][0]:
            retrieved_context = "\n".join(results['documents'][0]) if results['documents'] else ""
        
        # 3. Create a dynamic system prompt with the loaded documentation context
        system_instruction = (
            "You are the official Torch Proxies support assistant.\n"
            "Your task is to answer user inquiries accurately using the documentation below. "
            "CRITICAL: Whenever you mention or recommend a proxy package, you MUST provide its exact "
            "Markdown format checkout link found inside the documentation context (e.g., [Purchase Plan X Hybrid](https://torchproxies.com/...)). "
            "Never hallucinate or invent a URL that does not exist in the text context.\n\n"
            f"--- TORCH PROXIES DOCUMENTATION REFERENCE ---\n{retrieved_context}\n--------------------------------------"
        )

        formatted_messages = [{'role': 'system', 'content': system_instruction}]
        for msg in chat_history[-5:]:
            formatted_messages.append({'role': msg['role'], 'content': msg['content']})

            if saved_file_path:
                formatted_messages[-1]['images'] = [saved_file_path]

        def event_generator():
            response_stream = ollama.chat(
                model='qwen2.5vl:7b',
                messages=formatted_messages,
                options={
                    'temperature': 0.3,
                    'repeat_penalty': 1.2,
                    'frequency_penalty': 0.5,
                    'top_k': 20,
                    'top_p': 0.85
                }, # Lower temperature keeps answers tied accurately to context
                stream=True
            )
            
            for chunk in response_stream:
                content = chunk.message.content
                if content:
                    yield f"data: {json.dumps({'response': content})}\n\n"
            
            if saved_file_path and os.path.exists(saved_file_path):
                os.remove(saved_file_path)
                print(f"🗑️ Cleaned up temporary image asset at: {saved_file_path}")

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except Exception as e:
        print(f"Internal Backend Crash Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ollama Memory Error: {str(e)}")