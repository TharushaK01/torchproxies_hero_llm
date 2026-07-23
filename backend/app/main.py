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





import base64
import json
import os
import re
import shutil
import time
from typing import Any, Dict, List
from urllib.parse import urlparse
from contextlib import asynccontextmanager

from bs4 import BeautifulSoup
import chromadb
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from google.oauth2.service_account import Credentials
import gspread
import httpx
from openai import AsyncOpenAI
from supabase import Client, create_client

# Load environment variables
load_dotenv()

# Initialize Supabase Client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
print(f"DEBUG -> Loaded SUPABASE_URL: '{SUPABASE_URL}'")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# Google Sheets & Data Ingestion / Caching
# ==========================================
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
SPREADSHEET_ID = "1uyuGN3rwojkGPjzKrGr3CBCM4IAs2zwPExqEkfB7bMY"
CACHE_TTL_SECONDS = 600  # 10 minutes cache TTL

# In-Memory Cache Store
sheet1_cache = {
    "raw_records": [],
    "formatted_rules": "",
    "last_fetched": 0
}

def get_sheets_client():
    """Authenticates using service_account.json with guaranteed absolute path resolution."""
    # 1. Locate the 'backend' directory dynamically relative to this main.py file
    base_backend_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
    
    # 2. Target exact location: backend/service_account.json
    creds_path = os.path.join(base_backend_dir, "service_account.json")

    # 3. Validation check
    if not os.path.exists(creds_path):
        raise FileNotFoundError(
            f"Service account file not found at absolute path: {creds_path}"
        )

    # 4. Authorize using the guaranteed absolute path
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    return gspread.authorize(creds)




def clean_and_parse_sheet_data(records: List[Dict[str, Any]]) -> str:
    """Sanitizes raw sheet rows and creates clean, structured LLM prompt rules."""
    formatted_rules = []
    
    for row in records:
        # Standardize and sanitize key/value strings
        cat = str(row.get("category") or row.get("Category") or "").strip()
        uc = str(row.get("use case") or row.get("Use Case") or "").strip()
        rec = str(row.get("proxy type recomended") or row.get("Proxy Type Recommended") or "").strip()
        prod = str(row.get("specific product") or row.get("Specific Product") or "").strip()
        prompt_guide = str(row.get("prompt for llm") or row.get("Prompt for LLM") or "").strip()

        # Filter out empty rows
        if not cat and not uc and not prod:
            continue

        rule_entry = (
            f"- Category: {cat} | Use Case: {uc} | "
            f"Recommended Proxy: {rec} | Product: {prod} | Guidance: {prompt_guide}"
        )
        formatted_rules.append(rule_entry)

    return "\n".join(formatted_rules)

def fetch_and_cache_sheet1(force_refresh: bool = False) -> str:
    """Ingests Sheet1 data, cleans it, and updates the in-memory cache if expired."""
    current_time = time.time()
    
    # Check if cache is still valid
    if not force_refresh and (current_time - sheet1_cache["last_fetched"] < CACHE_TTL_SECONDS) and sheet1_cache["formatted_rules"]:
        return sheet1_cache["formatted_rules"]

    try:
        print("🔄 [Data Ingestion] Fetching fresh data from Google Sheets API...")
        gc = get_sheets_client()
        sh = gc.open_by_key(SPREADSHEET_ID)
        sheet1 = sh.worksheet("Sheet1")
        records = sheet1.get_all_records()

        # Clean and cache
        cleaned_rules = clean_and_parse_sheet_data(records)
        sheet1_cache["raw_records"] = records
        sheet1_cache["formatted_rules"] = cleaned_rules
        sheet1_cache["last_fetched"] = current_time

        print(f"✅ [Data Ingestion] Successfully cached {len(records)} rows from Sheet1.")
        return cleaned_rules

    except Exception as e:
        print(f"⚠️ [Data Ingestion] Failed to refresh Sheet1 cache: {e}")
        # Fallback to existing stale cache if available
        return sheet1_cache["formatted_rules"]

def log_unmapped_usecase_to_sheet2(
    category: str,
    usecase: str,
    proxy_type: str = "Pending Review",
    product: str = "Pending Review",
):
    """Appends new/unmapped user queries directly to Sheet2."""
    try:
        gc = get_sheets_client()
        sh = gc.open_by_key(SPREADSHEET_ID)
        sheet2 = sh.worksheet("Sheet2")

        new_row = [category, usecase, proxy_type, product]
        sheet2.append_row(new_row)
        print(f"✅ Successfully logged new use case to Sheet2: {usecase}")
    except Exception as e:
        print(f"⚠️ Failed to write to Sheet2: {e}")

# ==========================================
# FastAPI Application Lifespan & Config
# ==========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # App Startup: Pre-warm Google Sheets cache
    fetch_and_cache_sheet1(force_refresh=True)
    yield

app = FastAPI(title="TorchProxies Enterprise AI Production Engine", lifespan=lifespan)

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

openrouter_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY")
)

chroma_client = chromadb.PersistentClient(path=DB_PATH)
collection = chroma_client.get_or_create_collection(name="proxy_knowledge")

def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def extract_url_from_text(text: str) -> str | None:
    url_pattern = r"(https?://[^\s]+|(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})"
    match = re.search(url_pattern, text)
    if match:
        return match.group(0)
    return None

async def analyze_target_url(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    domain = urlparse(url).netloc.replace("www.", "")
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=5.0) as client:
            res = await client.get(url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")

            title = soup.title.string.strip() if soup.title and soup.title.string else ""
            meta_desc = ""
            desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
            if desc_tag:
                meta_desc = desc_tag.get("content", "")

            og_site_name = ""
            og_tag = soup.find("meta", attrs={"property": "og:site_name"})
            if og_tag:
                og_site_name = og_tag.get("content", "")

            headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2"])[:5]]

            return json.dumps({
                "domain": domain,
                "title": title,
                "site_name": og_site_name,
                "meta_description": meta_desc,
                "key_headings": headings,
                "http_status": res.status_code,
            })
    except Exception as err:
        return json.dumps({"domain": domain, "error": f"Could not scrape live content: {str(err)}"})

def save_message_to_supabase(session_id: str, role: str, content: str):
    try:
        supabase.table("messages").insert(
            {"session_id": session_id, "role": role, "content": content}
        ).execute()
    except Exception as err:
        print(f"⚠️ Failed to save message to Supabase: {err}")

async def check_and_log_unmapped_usecase(query: str, sheet1_rules: str):
    """Background task: Uses LLM to evaluate if the query was present in Sheet1 context."""
    try:
        analysis_prompt = f"""
You are an auditor analyzing whether a user request matches known spreadsheet rules.

--- SHEET1 RULES ---
{sheet1_rules}

--- USER REQUEST ---
{query}

Task:
1. Determine if the user's scenario/use case is explicitly covered in the SHEET1 RULES above.
2. Output ONLY a valid JSON object with:
   - "is_mapped": true or false
   - "category": "General domain string"
   - "usecase": "Brief summary of query"

Respond ONLY with valid JSON.
"""
        response = await openrouter_client.chat.completions.create(
            model="google/gemma-4-26b-a4b-it:free",
            messages=[{"role": "user", "content": analysis_prompt}],
            temperature=0.0,
        )

        raw_json = response.choices[0].message.content.strip()
        raw_json = re.sub(r"^```json\s*|\s*```$", "", raw_json, flags=re.MULTILINE)
        data = json.loads(raw_json)

        if not data.get("is_mapped", True):
            category = data.get("category", "Uncategorized")
            usecase = data.get("usecase", query)
            log_unmapped_usecase_to_sheet2(
                category=category,
                usecase=usecase,
                proxy_type="Pending Review",
                product="Pending Review",
            )
    except Exception as e:
        print(f"⚠️ Background Sheet2 check failed: {e}")

@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "cache_last_fetched": sheet1_cache["last_fetched"],
        "cached_rules_count": len(sheet1_cache["raw_records"]),
    }

@app.post("/v1/admin/refresh-cache")
async def manual_cache_refresh():
    """Admin endpoint to force refresh the Google Sheets rules cache on demand."""
    rules = fetch_and_cache_sheet1(force_refresh=True)
    return {"status": "success", "cached_rules": rules}

@app.post("/v1/chat")
async def chat_endpoint(
    background_tasks: BackgroundTasks,
    history: str = Form(...),
    session_id: str = Form("default_session"),
    file: UploadFile = File(None),
):
    try:
        # 1. Parse incoming user query from request history
        chat_history = json.loads(history)
        user_messages = [m for m in chat_history if m["role"] == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="No valid input query found.")
        latest_query = user_messages[-1]["content"]

        # 2. Save incoming user message to Supabase
        background_tasks.add_task(save_message_to_supabase, session_id, "user", latest_query)

        # 3. Off-Topic Keyword Guardrail Check
        HARD_OFF_TOPIC = ["recipe", "cooking", "food", "sports", "football", "movie", "gossip", "politics"]
        if any(word in latest_query.lower() for word in HARD_OFF_TOPIC):
            def instant_fallback():
                fallback_msg = (
                    "I apologize, but as the Torch Proxies assistant, I can only help you with our proxy services. "
                    "If you need general assistance, please [Chat with a Live Agent](https://torchproxies.com/chatwoot)."
                )
                yield f"data: {json.dumps({'response': fallback_msg})}\n\n"

            return StreamingResponse(instant_fallback(), media_type="text/event-stream")

        # 4. Handle file/image uploads
        saved_file_path = None
        base64_image = None
        if file is not None and file.filename:
            saved_file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(saved_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            base64_image = encode_image_to_base64(saved_file_path)

        # 5. Extract URL & analyze target website metadata
        detected_url = extract_url_from_text(latest_query)
        site_json = "{}"
        if detected_url:
            site_json = await analyze_target_url(detected_url)

        # 6. Retrieve rules from In-Memory Caching Layer (Zero network delay)
        sheet1_rules = fetch_and_cache_sheet1()

        # Schedule background check to log unmapped queries to Sheet2
        background_tasks.add_task(check_and_log_unmapped_usecase, latest_query, sheet1_rules)

        # 7. RAG Context Extraction (ChromaDB)
        retrieved_context = ""
        try:
            existing_collections = [c.name for c in chroma_client.list_collections()]
            if "proxy_knowledge" in existing_collections and collection.count() > 0:
                embed_response = openrouter_client.embeddings.create(
                    model="nvidia/llama-nemotron-embed-vl-1b-v2:free",
                    input=latest_query,
                )
                query_embedding = embed_response.data[0].embedding
                results = collection.query(query_embeddings=[query_embedding], n_results=2)
                if results and results.get("documents") and results["documents"][0]:
                    retrieved_context = "\n---\n".join(results["documents"][0])
        except Exception as db_err:
            print(f"⚠️ Vector lookup bypassed: {str(db_err)}")

        # 8. System Prompt Assembly
        system_instruction = f"""
You are the official technical proxy recommendation agent for TorchProxies.

--- CRITICAL RULE: BREVITY & CONCISENESS ---
Keep all responses extremely brief, direct, and to-the-point. Limit your answers to 1-3 short sentences maximum.

--- SPREADSHEET (SHEET1) RECOMMENDED PRODUCT RULES ---
Use these exact spreadsheet rules as your primary source for recommending products:
{sheet1_rules}

--- DETECTED TARGET WEBSITE METADATA (JSON) ---
<site_context>
{site_json}
</site_context>

--- PRODUCT RULE: LIVE AGENT ESCALATION ---
For custom bulk pricing, billing issues, bugs, or unhandled requests, direct customers to: [Chat with a Live Agent](https://torchproxies.com/chatwoot).

--- VECTOR KNOWLEDGE BASE CONTEXT ---
{retrieved_context}
--------------------------------------
"""

        # 9. Format Payload Messages
        formatted_messages = [{"role": "system", "content": system_instruction}]

        for msg in chat_history[-4:]:
            formatted_messages.append({"role": msg["role"], "content": msg["content"]})

        if base64_image:
            formatted_messages[-1]["content"] = [
                {"type": "text", "text": latest_query},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
            ]

        # 10. Asynchronous Streaming Response Pipeline
        async def event_generator():
            full_ai_response = ""
            try:
                response_stream = await openrouter_client.chat.completions.create(
                    model="google/gemma-4-26b-a4b-it:free",
                    messages=formatted_messages,
                    temperature=0.2,
                    stream=True,
                    extra_body={"reasoning": {"enabled": False}},
                )

                async for chunk in response_stream:
                    if chunk.choices and len(chunk.choices) > 0:
                        content = chunk.choices[0].delta.content
                        if content:
                            full_ai_response += content
                            yield f"data: {json.dumps({'response': content})}\n\n"

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