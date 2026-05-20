# 🏥 Medical Assistant AI

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://medical-assistant-ai-ml-engineer.streamlit.app)
[![Backend](https://img.shields.io/badge/Backend-Render-46E3B7?style=for-the-badge&logo=render)](https://render.com)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python)](https://python.org)

An intelligent, RAG-based medical assistant that lets you upload medical PDFs and ask questions against them in natural language. Built with **Streamlit**, **FastAPI**, **OpenAI Embeddings**, and **Pinecone** vector database — no fine-tuning required.

> 🔗 **Try it live:** [https://medical-assistant-ai-ml-engineer.streamlit.app](https://medical-assistant-ai-ml-engineer.streamlit.app)

---

## ✨ Features

- 📄 **PDF Ingestion** — Upload one or more medical documents (reports, research papers, drug references, clinical guidelines) directly through the UI
- 🔍 **Semantic Search** — Documents are chunked, embedded using OpenAI's embedding models, and stored in Pinecone for fast vector similarity retrieval
- 🤖 **Conversational Q&A** — Ask natural language questions and get contextually grounded answers sourced from your uploaded PDFs
- ⚡ **Groq-Powered Inference** — Low-latency LLM responses via the Groq API
- 🚀 **FastAPI Backend** — RESTful API layer handling PDF ingestion, embedding pipeline, and query endpoints
- ☁️ **Deployed on Render** — Backend hosted as a scalable web service on Render
- 🖥️ **Streamlit Frontend** — Clean, interactive UI deployed on Streamlit Cloud with zero config for end users

---

## 🧱 Architecture

```
┌──────────────────────────────────────────────────────┐
│            FRONTEND  (Streamlit Cloud)                │
│                                                      │
│   User uploads PDF  ──►  User types question         │
└───────────────┬──────────────────┬───────────────────┘
                │  HTTP POST       │  HTTP POST
                ▼                  ▼
┌──────────────────────────────────────────────────────┐
│              BACKEND  (FastAPI on Render)             │
│                                                      │
│  /upload                        /query               │
│    │                              │                  │
│    ▼                              ▼                  │
│  PDF Parsing &            Embed user query           │
│  Text Chunking               (OpenAI)                │
│    │                              │                  │
│    ▼                              ▼                  │
│  OpenAI Embeddings  ──►  Pinecone Similarity Search  │
│  (text-embedding-ada-002)    (Top-K chunks)          │
│                                   │                  │
│                                   ▼                  │
│                            Groq LLM API              │
│                        (context-augmented prompt)    │
└───────────────────────────────────┬─────────────────┘
                                    │
                                    ▼
                          Answer returned to
                          Streamlit frontend
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (Streamlit Cloud) |
| Backend API | FastAPI |
| Backend Hosting | Render |
| Embeddings | OpenAI (`text-embedding-ada-002`) |
| Vector Store | Pinecone |
| LLM Inference | Groq API |
| PDF Parsing | PyPDF / pdfplumber |
| Language | Python 3.12+ |
| Package Manager | uv / pip |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- [OpenAI API Key](https://platform.openai.com/account/api-keys)
- [Pinecone API Key](https://app.pinecone.io/)
- [Groq API Key](https://console.groq.com/)

### 1. Clone the repository

```bash
git clone https://github.com/saurabh2836/medical-assistant-ai-ml-engineer.git
cd medical-assistant-ai-ml-engineer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or if using `uv`:

```bash
uv sync
```

### 3. Set up environment variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=medical-assistant
GROQ_API_KEY=your_groq_api_key
```

### 4. Create a Pinecone index

In your [Pinecone console](https://app.pinecone.io/), create an index with:
- **Dimensions:** `1536` (for `text-embedding-ada-002`)
- **Metric:** `cosine`

### 5. Run locally

**Backend (FastAPI):**
```bash
uvicorn server.main:app --reload --port 8000
```

**Frontend (Streamlit):**
```bash
streamlit run client/app.py
```

Open your browser at `http://localhost:8501`. Make sure the `API_BASE_URL` in your Streamlit config points to `http://localhost:8000`.

---

## ☁️ Deployment

### Backend — Render

1. Push your repo to GitHub
2. Go to [render.com](https://render.com) → **New Web Service** → connect your repo
3. Set **Build Command:** `pip install -r requirements.txt`
4. Set **Start Command:** `uvicorn server.main:app --host 0.0.0.0 --port $PORT`
5. Add all environment variables (`OPENAI_API_KEY`, `PINECONE_API_KEY`, `GROQ_API_KEY`, etc.) under **Environment**
6. Deploy — Render will provide a public URL for your backend

### Frontend — Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) → **New app** → connect your repo
2. Set **Main file path** to `client/app.py`
3. Add secrets under **Advanced settings → Secrets** (including your Render backend URL as `API_BASE_URL`)
4. Deploy

🔗 **Live App:** [https://medical-assistant-ai-ml-engineer.streamlit.app](https://medical-assistant-ai-ml-engineer.streamlit.app)

---

## 📋 How to Use

1. **Upload a PDF** — Use the file uploader in the sidebar to upload any medical document
2. **Wait for processing** — The app will parse, chunk, embed, and store the document in Pinecone
3. **Ask questions** — Type your question in the chat input (e.g., *"What are the side effects of ibuprofen?"*)
4. **Get answers** — The assistant retrieves relevant chunks from your document and generates a grounded response

---

## 📁 Project Structure

```
medical-assistant-ai-ml-engineer/
├── client/                  # Streamlit frontend
│   ├── app.py               # Main Streamlit UI
│   └── components/          # UI components
├── server/                  # FastAPI backend
│   ├── main.py              # FastAPI app & route definitions
│   ├── embeddings.py        # OpenAI embedding logic
│   ├── pinecone_client.py   # Pinecone upsert & query
│   ├── pdf_parser.py        # PDF text extraction & chunking
│   └── llm.py               # Groq LLM integration
├── main.py                  # Root entry point
├── pyproject.toml           # Project metadata and dependencies
├── .python-version          # Python version pin (3.12)
├── .gitignore
└── README.md
```

---

## ⚙️ Configuration

| Variable | Description | Default |
|---|---|---|
| `OPENAI_API_KEY` | OpenAI API key for embeddings | Required |
| `PINECONE_API_KEY` | Pinecone API key | Required |
| `PINECONE_INDEX_NAME` | Name of your Pinecone index | `medical-assistant` |
| `GROQ_API_KEY` | Groq API key for LLM inference | Required |
| `API_BASE_URL` | FastAPI backend URL (Render) | `http://localhost:8000` |
| `CHUNK_SIZE` | Token size per text chunk | `500` |
| `CHUNK_OVERLAP` | Overlap between chunks | `50` |
| `TOP_K` | Number of similar chunks to retrieve | `5` |

---

## 🔒 Disclaimer

> This tool is intended for **informational and research purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical decisions.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Saurabh** — Senior Full Stack Developer & AI/ML Enthusiast
- GitHub: [@saurabh2836](https://github.com/saurabh2836)
