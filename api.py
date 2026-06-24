import os
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load .env FIRST before anything else
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# ── LlamaIndex / ChromaDB setup (loaded once at startup) ─────
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.openai import OpenAI
import chromadb

Settings.llm = OpenAI(model="gpt-4o-mini")

print("🗄️  Connecting to ChromaDB...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection("rag_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(
    vector_store,
    storage_context=storage_context,
)
query_engine = index.as_query_engine(similarity_top_k=3)
print("✅ Index loaded. API ready.")

# ── Chat backup ───────────────────────────────────────────────
BACKUP_DIR = "chatBackup"
os.makedirs(BACKUP_DIR, exist_ok=True)

# One filename per server session — created once at startup
session_start = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
SESSION_FILE = os.path.join(BACKUP_DIR, f"chat_{session_start}.json")

def save_chat(history: list):
    payload = {
        "saved_at":   datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        "session_id": session_start,
        "messages":   history
    }
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

# ── FastAPI app ───────────────────────────────────────────────
app = FastAPI(title="Clinic Assistant API")

# Serve static/ folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# ── Request / Response models ─────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    history: list = []

class ChatResponse(BaseModel):
    answer: str

# ── Routes ────────────────────────────────────────────────────
@app.get("/")
async def serve_index():
    return FileResponse("static/index.html")

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        response = query_engine.query(req.message)
        answer = str(response)
    except Exception as e:
        answer = f"⚠️ Something went wrong: {str(e)}"

    # Save backup
    updated = list(req.history) + [
        {"role": "user",      "content": req.message},
        {"role": "assistant", "content": answer},
    ]
    save_chat(updated)

    return ChatResponse(answer=answer)