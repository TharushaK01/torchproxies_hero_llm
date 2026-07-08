from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
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

# Connect to the persistent ChromaDB database folder
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="proxy_knowledge")

class ChatRequest(BaseModel):
    # message: str
    history: List[Dict[str, str]]

@app.post("/v1/chat")
async def chat_endpoint(payload: ChatRequest):
    try:

        user_messages =  [m for m in payload.history if m["role"] == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="No user message found in the request history.")
        latest_query = user_messages[-1]["content"]
        
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
            retrieved_context = "\n".join(results['documents'][0])
        
        # 3. Create a dynamic system prompt with the loaded documentation context
        system_instruction = (
            "You are an elite network infrastructure assistant. Expertly troubleshoot "
            "residential, datacenter, and mobile proxies, rotation configs, sticky sessions, "
            "IP whitelisting, user-pass authentication, and network protocols.\n\n"
            "Use the following custom reference documentation to answer the user's question. "
            "If the answer cannot be found in the documentation, use your broad technical knowledge.\n\n"
            f"--- CUSTOM DOCUMENTATION REFERENCE ---\n{retrieved_context}\n--------------------------------------"
        )

        formatted_messages = payload.history

        def event_generator():
            response_stream = ollama.chat(
                model='qwen2.5-coder:7b',
                messages=formatted_messages,
                options={'temperature': 0.2}, # Lower temperature keeps answers tied accurately to context
                stream=True
            )
            
            for chunk in response_stream:
                content = chunk.message.content
                if content:
                    yield f"data: {json.dumps({'response': content})}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except Exception as e:
        print(f"Internal Backend Crash Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ollama Memory Error: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "online", "engine": "ollama-local"}