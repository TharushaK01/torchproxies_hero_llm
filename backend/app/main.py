import os
import httpx  # type: ignore[import]
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

OLLAMA_BASE_URL = "http://127.0.0.1:11434"
CHAT_MODEL = "gemma3:4b"

app = FastAPI(title="Proxy AI Chatbot Backend")

# Enable Cross-Origin Resource Sharing (CORS) for local frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "model": CHAT_MODEL}

@app.post("/v1/chat")
async def handle_chat(payload: ChatRequest):
    ollama_chat_url = f"{OLLAMA_BASE_URL}/api/chat"
    
    system_instructions = (
        "You are an expert, safe customer support AI agent for a static proxy company. "
        "You must answer user questions helpfully using only our brand products. "
        "Do not hallucinate links or provide general advice outside of server/proxy management."
    )
    
    messages = [
        {"role": "system", "content": system_instructions},
        {"role": "user", "content": payload.message}
    ]
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                ollama_chat_url,
                json={
                    "model": CHAT_MODEL,
                    "messages": messages,
                    "stream": False
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Ollama error status: {response.status_code}")
                
            result = response.json()
            assistant_response = result["message"]["content"]
            return {"response": assistant_response}
            
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Cannot reach local Ollama engine: {exc}") 
