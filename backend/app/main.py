from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import ollama
import json

# 1. Initialize FastAPI Core Engine
app = FastAPI(title="Proxy Support AI Local Core Engine")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Define Request Structure
class ChatRequest(BaseModel):
    message: str


@app.post("/v1/chat")
async def chat_endpoint(payload: ChatRequest):
    try:
        system_instruction = (
            "You are an elite network infrastructure assistant. Expertly troubleshoot "
            "residential, datacenter, and mobile proxies, rotation configs, sticky sessions, "
            "IP whitelisting, user-pass authentication, and network protocols."
        )
        
        # Request generation from local Ollama
        # response = ollama.chat(
        #     model='gemma', 
        #     messages=[
        #         {'role': 'system', 'content': system_instruction},
        #         {'role': 'user', 'content': payload.message}
        #     ],
        #     options={'temperature': 0.3}
        # )
        
        # # FIX: Access fields using dot notation (.message.content) instead of brackets (['message']['content'])
        # return {"response": response.message.content}

        # We call the generator inside a helper function to stream chunks out
        def event_generator():
            response_stream = ollama.chat(
                model='gemma',
                messages=[
                    {'role': 'system', 'content': system_instruction},
                    {'role': 'user', 'content': payload.message}
                ],
                options={'temperature': 0.3},
                stream=True # <-- Enables chunk-by-chunk delivery
            )
            
            for chunk in response_stream:
                content = chunk.message.content
                if content:
                    # Send text chunk as a standard server event layout
                    yield f"data: {json.dumps({'response': content})}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")


        
    except Exception as e:
        # This will now print the true error to your Python terminal if anything else drops out
        print(f"Internal Backend Crash Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ollama Error: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "online", "engine": "ollama-local"}