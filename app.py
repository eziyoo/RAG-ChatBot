import os
import json
import gradio as gr
from datetime import datetime
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.openai import OpenAI
import chromadb

# Load API key
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Set LLM explicitly
Settings.llm = OpenAI(model="gpt-4o-mini")

# Load index once at startup
print("🗄️  Connecting to ChromaDB...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = chroma_client.get_or_create_collection("rag_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_vector_store(
    vector_store,
    storage_context=storage_context
)
query_engine = index.as_query_engine(similarity_top_k=3)
print("✅ Index loaded. Starting app...")

# ── Chat backup ───────────────────────────────────────────────
BACKUP_DIR = "chatBackup"
os.makedirs(BACKUP_DIR, exist_ok=True)

def save_chat(history):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(BACKUP_DIR, f"chat_{timestamp}.json")
    messages = []
    for msg in history:
        # Gradio 6.x passes history as list of dicts: {"role": ..., "content": ...}
        if isinstance(msg, dict):
            messages.append({"role": msg["role"], "content": msg["content"]})
        # Fallback for older tuple format: (user_msg, bot_msg)
        elif isinstance(msg, (list, tuple)):
            user_msg, bot_msg = msg[0], msg[1]
            if user_msg:
                messages.append({"role": "user",      "content": user_msg})
            if bot_msg:
                messages.append({"role": "assistant", "content": bot_msg})
    payload = {"saved_at": timestamp, "messages": messages}
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"💾 Chat saved → {filename}")
# ─────────────────────────────────────────────────────────────

# Chat function
def chat(message, history):
    try:
        response = query_engine.query(message)
        answer = str(response)
    except Exception as e:
        answer = f"⚠️ Something went wrong: {str(e)}"

    # Gradio 6.x history is list of dicts — append new exchange
    updated_history = list(history) + [
        {"role": "user",      "content": message},
        {"role": "assistant", "content": answer}
    ]
    save_chat(updated_history)
    return answer

# ✅ Gradio 6.x — theme goes in launch(), NOT in gr.Blocks()
with gr.Blocks() as demo:
    gr.ChatInterface(
        fn=chat,
        title="🏥 Clinic Assistant",
        description="Ask me anything about clinic policies, patient rights, prescriptions, telehealth, and more.",
        examples=[
            "What are my rights as a patient?",
            "How do I prepare for a colonoscopy?",
            "How do I request a prescription refill?",
            "What should I do in a medical emergency?",
            "Does the clinic accept my insurance?",
        ],
        chatbot=gr.Chatbot(height=500),  # ✅ removed type="messages"
    )

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())  # ✅ theme moved here