import os
import gradio as gr
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

# Chat function
def chat(message, history):
    try:
        response = query_engine.query(message)
        return str(response)
    except Exception as e:
        return f"⚠️ Something went wrong: {str(e)}"

# ✅ Gradio 6.x — theme goes on gr.Blocks, not ChatInterface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
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
        chatbot=gr.Chatbot(height=500),
    )

if __name__ == "__main__":
    demo.launch()