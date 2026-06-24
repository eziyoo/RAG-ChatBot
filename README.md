# 🏥 RAG Clinic Assistant

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about clinic documents using LlamaIndex, ChromaDB, and OpenAI. Includes both a terminal interface and a Gradio web UI.

---

## 📸 Demo

> Ask questions like *"How do I prepare for a colonoscopy?"* or *"What are my rights as a patient?"* and get accurate, document-grounded answers instantly.

---

## 🧠 How It Works

This project uses the RAG (Retrieval-Augmented Generation) pattern:

1. **Ingest** — Documents in the `docs/` folder are loaded, split into chunks, and embedded using OpenAI's embedding model. Vectors are stored in a local ChromaDB database.
2. **Retrieve** — When a question is asked, the top 3 most semantically similar chunks are retrieved from ChromaDB.
3. **Generate** — The retrieved chunks are passed to `gpt-4o-mini` as context, which generates a grounded, accurate answer.

```
docs/ (your documents)
    │
    ▼
[ingest.py] → chunks → embeddings → chroma_db/
                                          │
                    User question ────────┘
                          │
                    [similarity search]
                          │
                    [gpt-4o-mini generates answer]
                          │
                    🤖 Response
```

---

## 📁 Project Structure

```
RAG-ChatBot/
├── docs/                        # Source documents (clinic knowledge base)
│   ├── blood_tests_reference.txt
│   ├── clinic_faq.txt
│   ├── colonoscopy_prep.txt
│   ├── emergency_escalation_rules.txt
│   ├── insurance_guide.txt
│   ├── patient_rights.txt
│   ├── prescription_refill_policy.txt
│   └── telehealth_guide.txt
├── chroma_db/                   # Auto-generated vector database (git-ignored)
├── ingest.py                    # Step 1: Load, chunk, embed, and store documents
├── query.py                     # Step 2: Terminal-based Q&A interface
├── app.py                       # Step 3: Gradio web UI
├── .env                         # API keys (git-ignored)
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
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Your API Key

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key_here
```

> Get your API key from [platform.openai.com](https://platform.openai.com/api-keys)

---

## 🚀 Usage

### Step 1 — Ingest Documents

Run this **once** to embed your documents and build the vector database:

```bash
python ingest.py
```

This reads all files from `docs/`, chunks them into 512-token pieces, sends them to OpenAI for embedding, and stores everything in `./chroma_db`. You only need to re-run this if you add or change documents.

### Step 2A — Terminal Interface

Ask questions directly in your terminal:

```bash
python query.py
```

```
🙋 Your question: Do I need someone to drive me home after a colonoscopy?
🤖 Answer: Yes, you must arrange for a responsible adult to drive you home...
```

Type `exit` or `quit` to stop.

### Step 2B — Web UI (Gradio)

Launch the browser-based chat interface:

```bash
python app.py
```

Then open your browser at `http://localhost:7860`.

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| RAG Framework | [LlamaIndex](https://www.llamaindex.ai/) |
| Vector Database | [ChromaDB](https://www.trychroma.com/) |
| Embedding Model | OpenAI `text-embedding-ada-002` |
| LLM | OpenAI `gpt-4o-mini` |
| Web UI | [Gradio](https://gradio.app/) |
| Language | Python 3.10+ |

---

## 📦 Requirements

Generate with:

```bash
pip freeze > requirements.txt
```

Key dependencies:
- `llama-index`
- `llama-index-vector-stores-chroma`
- `llama-index-llms-openai`
- `chromadb`
- `gradio`
- `openai`
- `python-dotenv`

---

## 🔒 Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key |

Never commit your `.env` file. It is listed in `.gitignore`.

---

## 📄 Adding New Documents

1. Add your `.txt`, `.pdf`, or `.docx` files to the `docs/` folder
2. Delete the existing `chroma_db/` folder (or it will merge with old data)
3. Re-run `python ingest.py`

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📝 License

This project is licensed under the MIT License.
