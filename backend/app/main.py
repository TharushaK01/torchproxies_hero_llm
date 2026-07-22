# from fastapi import FastAPI, HTTPException, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import StreamingResponse
# import os
# import shutil
# from pydantic import BaseModel
# from typing import List, Dict, Any
# import chromadb
# import json
# import base64
# from openai import OpenAI
# from dotenv import load_dotenv


# load_dotenv()



# app = FastAPI(title="Proxy Support AI Cloud Core Engine")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# DB_PATH = os.path.abspath("./chroma_db")
# UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../uploads"))
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# # Initialize OpenRouter Client wrapper mapped against native OpenRouter targets
# openrouter_client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key=os.getenv("OPENROUTER_API_KEY")
# )

# # Connect to the persistent ChromaDB database folder
# chroma_client = chromadb.PersistentClient(path=DB_PATH)
# collection = chroma_client.get_or_create_collection(name="proxy_knowledge")

# def encode_image_to_base64(image_path: str) -> str:
#     """Encodes temporary local visual assets into base64 strings for OpenRouter submission."""
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode("utf-8")


# @app.get("/health")
# async def health_check():
#    return {"status": "online", "pipeline": "openrouter-cloud-integrated"}


# @app.post("/v1/ingest")
# async def trigger_ingest():
#     try:
#         from backend.app.ingest import run_ingestion
#         run_ingestion()
#         return {
#             "status": "success", 
#             "message": "Vector database updated successfully", 
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


# @app.post("/v1/chat")
# async def chat_endpoint(
#     history: str = Form(...),
#     file: UploadFile = File(None)  # Optional file upload
# ):
#     # try:
#     #     # 1. Parse incoming request parameters
#     #     chat_history = json.loads(history)
#     #     user_messages = [m for m in chat_history if m["role"] == "user"]
#     #     if not user_messages:
#     #         raise HTTPException(status_code=400, detail="No user message found in the request history.")
#     #     latest_query = user_messages[-1]["content"]

#     #     # 2. Extract and handle temporary local storage assets
#     #     saved_file_path = None
#     #     if file is not None and file.filename:
#     #         saved_file_path = os.path.join(UPLOAD_DIR, file.filename)
#     #         with open(saved_file_path, "wb") as buffer:
#     #             shutil.copyfileobj(file.file, buffer)

#     #     # 3. Guardrail analysis execution engine
#     #     OFF_TOPIC_KEYWORDS = [
#     #         "recipe", "cooking", "food", "dish", "meal", "ingredients", "chocolate chips", "pasta", "soup", "dessert", "bake", "grill", "fry", "boil", "roast", "saute", "stir-fry", "simmer",
#     #         "sports", "game", "team", "player", "score", "sports", "football", "basketball", "soccer", "tennis", "baseball", "hockey",
#     #         "entertainment", "movie", "film", "music", "concert", "song", "album", "artist", "celebrity", "show", "TV", "theater",
#     #         "politics", "election", "government", "policy", "weather", "law", "president", "senator", "congress", "political party", "campaign", "vote", "legislation",
#     #         "general", "news", "gossip", "trivia", "fun", "joke", "meme", "viral", "trend", "fashion", "lifestyle", "travel", "vacation", "holiday", "festival", "event"
#     #     ]
        
#     #     query_lower = latest_query.lower()
#     #     is_generic_code = ("write a script" in query_lower or "how to scrape" in query_lower or "beautifulsoup" in query_lower or "selenium" in query_lower or "python code" in query_lower or "javascript code" in query_lower)
#     #     has_proxy_context = ("proxy" in query_lower or "proxies" in query_lower or "network" in query_lower or "vpn" in query_lower or "tor" in query_lower)

#     #     if any(keyword in query_lower for keyword in OFF_TOPIC_KEYWORDS) or (is_generic_code and not has_proxy_context):
#     #         def guardrail_fallback():
#     #             yield f"data: {json.dumps({'response': 'I apologize, but as the Torch Proxies assistant, I can only help you with our proxy services, service pricing plans, and technical proxy configuration adjustments.'})}\n\n"
#     #         return StreamingResponse(guardrail_fallback(), media_type="text/event-stream")

#     #     # 4. Vector DB contextual retrieval via OpenRouter cloud embedding endpoints
#     #     retrieved_context = ""
#     #     try:
#     #         existing_collections = [c.name for c in chroma_client.list_collections()]

#     #         if "proxy_knowledge" in existing_collections:
#     #             active_collection = chroma_client.get_collection(name="proxy_knowledge")

#     #             if active_collection.count() > 0:
#     #                 # Cloud request replacing local Ollama implementation
#     #                 embed_response = openrouter_client.embeddings.create(
#     #                     model="nvidia/llama-nemotron-embed-vl-1b-v2:free",
#     #                     input=latest_query
#     #                 )
#     #                 query_embedding = embed_response.data[0].embedding

#     #                 results = active_collection.query(
#     #                     query_embeddings=[query_embedding],
#     #                     n_results=2
#     #                 )

#     #                 if results and results.get('documents') and results['documents'][0]:
#     #                     retrieved_context = "\n---\n".join(results['documents'][0])
#     #                     print("🔍 Context successfully pulled via Cloud Embeddings.")
#     #             else:
#     #                 print("⚠️ ChromaDB collection 'proxy_knowledge' is currently empty.")
#     #         else:
#     #             print("⚠️ ChromaDB collection 'proxy_knowledge' does not exist yet.")
#     #     except Exception as db_err:
#     #         print(f"🚨 Critical Vector DB lookup error shielded gracefully: {str(db_err)}")





#     try:
#         # 1. Parse incoming UI historical data map
#         chat_history = json.loads(history)
#         user_messages = [m for m in chat_history if m["role"] == "user"]
#         if not user_messages:
#             raise HTTPException(status_code=400, detail="No valid input query found.")
#         latest_query = user_messages[-1]["content"]

#         # 2. Process physical file assets submitted by front-end client interface
#         saved_file_path = None
#         base64_image = None
#         if file is not None and file.filename:
#             saved_file_path = os.path.join(UPLOAD_DIR, file.filename)
#             with open(saved_file_path, "wb") as buffer:
#                 shutil.copyfileobj(file.file, buffer)
#             # Standardize format profile maps for multi-modal parsing channels
#             base64_image = encode_image_to_base64(saved_file_path)

#         # 3. Fast Static Off-Topic Keyword Guardrail Check
#         HARD_OFF_TOPIC = ["recipe", "cooking", "food", "sports", "football", "movie", "gossip", "politics"]
#         if any(word in latest_query.lower() for word in HARD_OFF_TOPIC):
#             def instant_fallback():
#                 yield f"data: {json.dumps({'response': 'I apologize, but as the Torch Proxies assistant, I can only help you with our proxy services. If you need general assistance, please [Chat with a Live Agent](https://torchproxies.com/chatwoot).'})}\n\n"
#             return StreamingResponse(instant_fallback(), media_type="text/event-stream")

#         # 4. Context Extraction (via Cloud Embedding Engine)
#         retrieved_context = ""
#         try:
#             existing_collections = [c.name for c in chroma_client.list_collections()]
#             if "proxy_knowledge" in existing_collections and collection.count() > 0:
#                 embed_response = openrouter_client.embeddings.create(
#                     model="nvidia/llama-nemotron-embed-vl-1b-v2:free",
#                     input=latest_query
#                 )
#                 query_embedding = embed_response.data[0].embedding
                
#                 results = collection.query(
#                     query_embeddings=[query_embedding],
#                     n_results=2
#                 )
#                 if results and results.get('documents') and results['documents'][0]:
#                     retrieved_context = "\n---\n".join(results['documents'][0])
#         except Exception as db_err:
#             print(f"⚠️ Context lookup bypassed: {str(db_err)}")

#         # # 5. Build prompt contextual alignment maps
#         # system_instruction = (
#         #     "You are the official Torch Proxies support assistant.\n"
#         #     "Your task is to answer user inquiries accurately using the documentation below. "
#         #     "CRITICAL: Whenever you mention or recommend a proxy package, you MUST provide its exact "
#         #     "Markdown format checkout link found inside the documentation context (e.g., [Purchase Plan X Hybrid](https://torchproxies.com/...)). "
#         #     "Never hallucinate or invent a URL that does not exist in the text context.\n\n"
#         #     f"--- TORCH PROXIES DOCUMENTATION REFERENCE ---\n{retrieved_context}\n--------------------------------------"
#         # )


# # # 5. Build prompt contextual alignment maps (Updated with Phase 2 Product Rules & Guardrails)
# #         system_instruction = (
# #             "You are the official Torch Proxies support assistant. Guard closely your core knowledge mapping rules:\n\n"
            
# #             "--- RULE 1: RESIDENTIAL PROXY INTENT ---\n"
# #             "If the user asks about Residential Proxies, you must prioritize and suggest the 'PlanX' package "
# #             "as our recommended best-fit option. Explicitly clarify to the user that our Residential packages "
# #             "(Standard, Premium, and PlanX) provide bandwidth measured in GB and function via allocated Credits.\n\n"
            
# #             "--- RULE 2: ISP PROXY INTENT ---\n"
# #             "If the user asks about proxy solutions for any of these 4 specific target scenarios:\n"
# #             "1. Sneakers\n"
# #             "2. Tickets\n"
# #             "3. Social Media\n"
# #             "4. Web Scraping\n"
# #             "You must explicitly recommend our 'ISP Proxy' product. State clearly that our ISP Proxies fully support "
# #             "these use cases and operate on a monthly renewal model.\n\n"
            
# #             "--- RULE 3: ESCALATION & GENERAL SUPPORT ---\n"
# #             "If the user asks questions outside of these specific product options, requests pricing adjustments, "
# #             "experiences system trouble, or asks to speak with a human agent, you must direct them to a live support representative. "
# #             "Provide this exact markdown link formatted exactly like this: [Chat with a Live Agent](https://torchproxies.com/chatwoot).\n\n"
            
# #             f"--- TORCH PROXIES DOCUMENTATION REFERENCE ---\n{retrieved_context}\n--------------------------------------"
# #         )




# # 5. Injection of Core Product Knowledge Engine Guardrails
#         system_instruction = (
#             "You are the official Torch Proxies support assistant. You must enforce these explicit system guardrails:\n\n"
            
#             "--- PRODUCT RULE 1: RESIDENTIAL PROXIES ---\n"
#             "If the user asks about Residential Proxies, you must prioritize and explicitly recommend the 'PlanX' package "
#             "as the ideal, best-fit tier. Explicitly state that our Residential packages (Standard, Premium, PlanX) "
#             "provide data volume in GB and run on a Credits allotment system.\n\n"
            
#             "--- PRODUCT RULE 2: ISP PROXIES ---\n"
#             "If the user is inquiring about proxies for any of the following 4 specific use cases:\n"
#             "1. Sneakers\n"
#             "2. Tickets\n"
#             "3. Social Media\n"
#             "4. Web Scraping\n"
#             "You must recommend our dedicated 'ISP Proxy' product. Inform the user that we offer custom ISP proxy profiles "
#             "supporting all 4 categories, operating on a transparent monthly renewal system.\n\n"
            
#             "--- PRODUCT RULE 3: LIVE AGENT ESCALATION ---\n"
#             "If the customer inquires about custom bulk pricing, billing issues, complex configuration bugs, asks questions "
#             "unrelated to our Residential/ISP inventory, or explicitly requests human intervention, you must politely direct them to a human agent. "
#             "You must output this exact Markdown link: [Chat with a Live Agent](https://torchproxies.com/chatwoot).\n\n"
            
#             f"--- LOCAL PRODUCT REFERENCE MATRIX ---\n{retrieved_context}\n--------------------------------------"
#         )



#         formatted_messages = [{'role': 'system', 'content': system_instruction}]
#         for msg in chat_history[-4:]:
#             formatted_messages.append({'role': msg['role'], 'content': msg['content']})


#             # Inject Vision parameters into the final prompt index if a base64 image asset is ready
#         if base64_image:
#             # Overwrite the latest user content block into an OpenAI/OpenRouter compatible multimodal array format
#             formatted_messages[-1]['content'] = [
#                 {"type": "text", "text": latest_query},
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": f"data:image/jpeg;base64,{base64_image}"
#                     }
#                 }
#             ]

#         # 6. Stream Engine generation targeting OpenRouter Cloud nodes
#         def event_generator():
#             try:
#                 response_stream = openrouter_client.chat.completions.create(
#                     model="nvidia/nemotron-3-ultra-550b-a55b:free",
#                     messages=formatted_messages,
#                     temperature=0.3,
#                     stream=True,
#                     extra_body={
#                         "reasoning": {"enabled": True}
#                     }
#                 )
                
#                 for chunk in response_stream:
#                     if chunk.choices and len(chunk.choices) > 0:
#                         content = chunk.choices[0].delta.content
#                         if content:
#                             yield f"data: {json.dumps({'response': content})}\n\n"
#             except Exception as stream_err:
#                 yield f"data: {json.dumps({'response': f'🚨 OpenRouter Pipeline Error: {str(stream_err)}'})}\n\n"
#             finally:
#                 if saved_file_path and os.path.exists(saved_file_path):
#                     os.remove(saved_file_path)
#                     print(f"🗑️ Cleaned up temporary image asset at: {saved_file_path}")

#         return StreamingResponse(event_generator(), media_type="text/event-stream")

#     except Exception as e:
#         print(f"🚨 Main endpoint error caught: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))






from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import os
import shutil
import json
import base64
from typing import List, Dict, Any
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from urllib.parse import urlparse
import httpx
import re
from supabase import create_client, Client
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks # Added BackgroundTasks
from openai import AsyncOpenAI # Switched from OpenAI to AsyncOpenAI

# Load environment variables
load_dotenv()

# Initialize Supabase Client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
print(f"DEBUG -> Loaded SUPABASE_URL: '{SUPABASE_URL}'")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="TorchProxies Enterprise AI Production Engine")

# CORS middleware alignment for the frontend dashboard interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.abspath("./chroma_db")
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Centralized OpenRouter Cloud Client
openrouter_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Active connection array mapped to the cloud-embedded local Vector DB
chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(name="proxy_knowledge")


def encode_image_to_base64(image_path: str) -> str:
    """Encodes temporary local visual assets into base64 strings for OpenRouter submission."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def analyze_target_url(url: str) -> str:
    """Scrapes site metadata and maps it to the target use case."""
    try:
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
            
        domain = urlparse(url).netloc.replace("www.", "")
        
        async with httpx.AsyncClient(follow_redirects=True, timeout=3.0) as client:
            res = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(res.text, "html.parser")
            title = soup.title.string.strip() if soup.title and soup.title.string else ""
            
            meta_desc = ""
            desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
            if desc_tag:
                meta_desc = desc_tag.get("content", "")

        combined_text = f"Domain: {domain} | Title: {title} | Description: {meta_desc}".lower()
        
        # Sneaker & E-commerce sites
        if any(k in combined_text for k in ["nike", "adidas", "yeezy", "footlocker", "supreme", "sneakers", "shoes", "kicks"]):
            return f"The target URL is '{domain}' (Sneakers/Footwear). Recommend our dedicated ISP Proxies for Sneakers."
            
        # Ticketing platforms
        elif any(k in combined_text for k in ["ticketmaster", "axs", "stubhub", "tickets", "concert", "event"]):
            return f"The target URL is '{domain}' (Ticketing). Recommend our dedicated ISP Proxies for Tickets."
            
        # Social Media platforms
        elif any(k in combined_text for k in ["instagram", "tiktok", "twitter", "x.com", "facebook", "social media"]):
            return f"The target URL is '{domain}' (Social Media). Recommend our dedicated ISP Proxies for Social Media."
            
        # General Web Scraping / E-commerce targets
        else:
            return f"The target URL is '{domain}'. If scraping data from this site, recommend our ISP Proxies for Web Scraping or Residential Proxies (PlanX)."
            
    except Exception as err:
        return ""


# def save_message_to_supabase(session_id: str, role: str, content: str):
    # """Inserts a single message row into the Supabase 'messages' table."""
    # try:
    #     supabase.table("messages").insert({
    #         "session_id": session_id,
    #         "role": role,
    #         "content": content
    #     }).execute()
    # except Exception as err:
    #     print(f"⚠️ Failed to save message to Supabase: {err}")

def save_message_to_supabase(session_id: str, role: str, content: str):
    try:
        supabase.table("messages").insert({
            "session_id": session_id,
            "role": role,
            "content": content
        }).execute()
    except Exception as err:  # <--- Aligned with 'try:' (4 spaces)
        print(f"⚠️ Failed to save message to Supabase: {err}")



def get_session_history_from_supabase(session_id: str):
    """Retrieves all past messages for a given session sorted chronologically."""
    try:
        res = supabase.table("messages") \
            .select("role, content") \
            .eq("session_id", session_id) \
            .order("created_at", desc=False) \
            .execute()
        return res.data
    except Exception as err:
        print(f"⚠️ Failed to fetch history from Supabase: {err}")
        return []


@app.get("/health")
async def health_check():
    return {"status": "online", "pipeline": "openrouter-cloud-integrated"}


@app.post("/v1/chat")
async def chat_endpoint(
    background_tasks: BackgroundTasks,
    history: str = Form(...),
    session_id: str = Form("default_session"),
    file: UploadFile = File(None)
):
    # 1. Parse incoming UI historical data map
    chat_history = json.loads(history)
    user_messages = [m for m in chat_history if m["role"] == "user"]
    if not user_messages:
        raise HTTPException(status_code=400, detail="No valid input query found.")
    latest_query = user_messages[-1]["content"]

    # 2. Save incoming message to Supabase
    background_tasks.add_task(save_message_to_supabase, session_id, "user", latest_query)

    try:
        # 3. Process physical file assets
        saved_file_path = None
        base64_image = None
        if file is not None and file.filename:
            saved_file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(saved_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            base64_image = encode_image_to_base64(saved_file_path)

        # 4. Fast Static Off-Topic Keyword Guardrail Check
        HARD_OFF_TOPIC = ["recipe", "cooking", "food", "sports", "football", "movie", "gossip", "politics"]
        if any(word in latest_query.lower() for word in HARD_OFF_TOPIC):
            def instant_fallback():
                yield f"data: {json.dumps({'response': 'I apologize, but as the Torch Proxies assistant, I can only help you with our proxy services. If you need general assistance, please [Chat with a Live Agent](https://torchproxies.com/chatwoot).'})}\n\n"
            return StreamingResponse(instant_fallback(), media_type="text/event-stream")

        # 5. URL Extraction & Analysis Pass
        url_match = re.search(r'(https?://[^\s]+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}[^\s]*)', latest_query)
        detected_url_context = ""
        if url_match:
            extracted_url = url_match.group(0)
            detected_url_context = await analyze_target_url(extracted_url)

        # 6. Context Extraction (via Cloud Embedding Engine)
        retrieved_context = ""
        try:
            existing_collections = [c.name for c in chroma_client.list_collections()]
            if "proxy_knowledge" in existing_collections and collection.count() > 0:
                embed_response = openrouter_client.embeddings.create(
                    model="nvidia/llama-nemotron-embed-vl-1b-v2:free",
                    input=latest_query
                )
                query_embedding = embed_response.data[0].embedding
                
                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=2
                )
                if results and results.get('documents') and results['documents'][0]:
                    retrieved_context = "\n---\n".join(results['documents'][0])
        except Exception as db_err:
            print(f"⚠️ Context lookup bypassed: {str(db_err)}")

        # 7. System Instruction Setup
        system_instruction = (
            "You are the official Torch Proxies support assistant. You must enforce these explicit system guardrails:\n\n"
            
            "--- CRITICAL RULE: BREVITY & CONCISENESS ---\n"
            "Keep all responses extremely brief, direct, and to-the-point. Limit your answers to 1-3 short sentences maximum.\n\n"
            
            f"--- DETECTED TARGET WEBSITE ANALYSIS ---\n{detected_url_context}\n\n"

            "--- PRODUCT RULE 1: RESIDENTIAL PROXIES ---\n"
            "If the user asks about Residential Proxies, recommend 'PlanX'. Mention they use GB and Credits. Keep it to one sentence.\n\n"
            
            "--- PRODUCT RULE 2: ISP PROXIES ---\n"
            "If inquiring about Sneakers, Tickets, Social Media, or Web Scraping (or a website in those categories), recommend 'ISP Proxy' on a monthly renewal. Keep it to one sentence.\n\n"
            
            "--- PRODUCT RULE 3: LIVE AGENT ESCALATION ---\n"
            "For custom bulk pricing, billing, bugs, or off-topic chats, immediately direct them to: [Chat with a Live Agent](https://torchproxies.com/chatwoot).\n\n"
            
            f"--- LOCAL PRODUCT REFERENCE MATRIX ---\n{retrieved_context}\n--------------------------------------"
        )

        # 8. Structuring Payload Messages
        formatted_messages = [{'role': 'system', 'content': system_instruction}]
        
        for msg in chat_history[-4:]:
            formatted_messages.append({'role': msg['role'], 'content': msg['content']})

        if base64_image:
            formatted_messages[-1]['content'] = [
                {"type": "text", "text": latest_query},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]

        # 9. Asynchronous Streaming Response Pipeline Execution
        async def event_generator():
            full_ai_response = ""
            try:
                response_stream = await openrouter_client.chat.completions.create(
                    model= "google/gemma-4-26b-a4b-it:free",
                    messages=formatted_messages,
                    temperature=0.2,
                    stream=True,
                    extra_body={
                        "reasoning": {"enabled": True}  #True change to False
                    }
                )
                
                async for chunk in response_stream:
                    if chunk.choices and len(chunk.choices) > 0:
                        content = chunk.choices[0].delta.content
                        if content:
                            full_ai_response += content
                            yield f"data: {json.dumps({'response': content})}\n\n"

                # Save AI response to Supabase once streaming completes
                if full_ai_response:
                    background_tasks.add_task(
                        save_message_to_supabase, session_id, "assistant", full_ai_response
                    )

            except Exception as stream_err:
                yield f"data: {json.dumps({'response': f'🚨 Engine Connection Interrupted: {str(stream_err)}'})}\n\n"
            finally:
                if saved_file_path and os.path.exists(saved_file_path):
                    os.remove(saved_file_path)

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))