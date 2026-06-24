# 🏥 RAG Clinic Assistant

A production-style Retrieval-Augmented Generation (RAG) chatbot that answers questions about clinic documents. Built with **LlamaIndex**, **ChromaDB**, **OpenAI**, and served via a **FastAPI** backend with a clean, framework-free HTML/CSS/JS frontend.

---

## ✨ Features

- 💬 ChatGPT-style dark web UI — no React, no Vue, pure HTML/CSS/JS
- 🔍 Semantic search over clinic documents using vector embeddings
- 🤖 Answers grounded in your documents via `gpt-4o-mini`
- 💾 Automatic per-session chat backup to `chatBackup/` as JSON
- ⚡ FastAPI backend with instant startup — index loaded once at boot
- 📱 Responsive layout — works on mobile and desktop
- 🗂️ Sidebar with document list and "New Chat" button

---

## 🧠 How It Works

This project implements the standard RAG pipeline in two phases:

### Offline — Indexing (run once)

```
docs/ (your .txt / .pdf files)
       │
       ▼
[ingest.py]
  → split into 512-token chunks
  → embed with OpenAI text-embedding-ada-002
  → store vectors in ./chroma_db
```

### Online — Query (every request)

```
User question
      │
      ▼
[Embed question] → vector
      │
      ▼
[ChromaDB] → top 3 semantically similar chunks
      │
      ▼
[gpt-4o-mini] ← chunks + question as context
      │
      ▼
  🤖 Grounded answer
```

---

## 📁 Project Structure

```
RAG-ChatBot/
├── docs/                              # Source documents (clinic knowledge base)
│   ├── blood_tests_reference.txt
│   ├── clinic_faq.txt
│   ├── colonoscopy_prep.txt
│   ├── emergency_escalation_rules.txt
│   ├── insurance_guide.txt
│   ├── patient_rights.txt
│   ├── prescription_refill_policy.txt
│   └── telehealth_guide.txt
├── static/
│   └── index.html                     # Full chat UI (single file, no frameworks)
├── chroma_db/                         # Auto-generated vector DB (git-ignored)
├── chatBackup/                        # Per-session chat logs as JSON (git-ignored)
├── ingest.py                          # Step 1: Chunk, embed, and index documents
├── query.py                           # Step 2: Terminal Q&A interface
├── api.py                             # Step 3: FastAPI backend
├── .env                               # API keys (git-ignored)
├── .gitignore
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/eziyoo/RAG-ChatBot.git
cd RAG-ChatBot
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Your API Key

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

> Get your key from [platform.openai.com/api-keys](https://platform.openai.com/api-keys). Make sure billing is enabled — costs are minimal (fractions of a cent per query).

---

## 🚀 Usage

### Step 1 — Ingest Documents

Run **once** to build the vector database from your documents:

```bash
python ingest.py
```

This reads all files from `docs/`, chunks them into 512-token pieces, embeds them with OpenAI, and stores everything in `./chroma_db`.

> Re-run this any time you add, remove, or update documents.

### Step 2 — Start the Web App

```bash
uvicorn api:app --reload
```

Open your browser at **[http://localhost:8000](http://localhost:8000)**.

### Optional — Terminal Interface

For quick testing without the web UI:

```bash
python query.py
```

```
🙋 Your question: Do I need someone to drive me home after a colonoscopy?
🤖 Answer: Yes, you must arrange for a responsible adult to drive you home...
```

Type `exit` or `quit` to stop.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| RAG Framework | [LlamaIndex](https://www.llamaindex.ai/) |
| Vector Database | [ChromaDB](https://www.trychroma.com/) — local, no cloud needed |
| Embedding Model | OpenAI `text-embedding-ada-002` |
| LLM | OpenAI `gpt-4o-mini` |
| Backend | [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn |
| Frontend | Vanilla HTML / CSS / JavaScript (no frameworks) |
| Environment | Python 3.10+ |

---

## 📦 Dependencies

Install all at once:

```bash
pip install -r requirements.txt
```

Key packages:

```
llama-index
llama-index-vector-stores-chroma
llama-index-llms-openai
chromadb
fastapi
uvicorn
python-multipart
openai
python-dotenv
```

Generate a fresh lockfile after adding packages:

```bash
pip freeze > requirements.txt
```

---

## 💾 Chat Backup

Every conversation is automatically saved to `chatBackup/` as a JSON file. One file is created per session — it is overwritten on each message (not duplicated).

```
chatBackup/
├── chat_2026-06-24_18-42-00.json   ← Session 1
├── chat_2026-06-24_20-15-00.json   ← Session 2 (New Chat clicked)
└── ...
```

Each file contains the full message history:

```json
{
  "saved_at": "2026-06-24_18-43-15",
  "session_id": "2026-06-24_18-42-00",
  "messages": [
    { "role": "user",      "content": "What are my rights as a patient?" },
    { "role": "assistant", "content": "As a patient, you have the right to..." }
  ]
}
```

---

## 📄 Adding New Documents

1. Add `.txt`, `.pdf`, or `.docx` files to the `docs/` folder
2. Delete the existing `chroma_db/` folder to avoid stale data:
   ```bash
   rm -rf chroma_db/
   ```
3. Re-run the ingestion pipeline:
   ```bash
   python ingest.py
   ```

---

## 🔒 Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key |

The `.env` file is listed in `.gitignore` and will never be committed to version control.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).