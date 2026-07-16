# 🧠 SmartNotesAI

**SmartNotesAI** is an AI-powered note assistant that enables students to interact with their study material using **Retrieval-Augmented Generation (RAG)**. Upload your lecture notes or PDFs, ask questions in natural language, and receive context-aware answers grounded in your own documents.

Designed as a beginner-friendly GenAI project, SmartNotesAI demonstrates the core concepts behind modern AI applications, including document ingestion, text chunking, semantic retrieval, and LLM-powered question answering.

---

## ✨ Features

* 📄 Upload one or multiple PDF notes
* 📝 Automatic text extraction and preprocessing
* ✂️ Intelligent text chunking for efficient retrieval
* 🔍 Semantic document search using vector embeddings
* 🤖 AI-generated answers based on retrieved context
* 🎨 Simple and interactive Streamlit interface

---

## 🛠️ Tech Stack

| Category        | Technologies            |
| --------------- | ----------------------- |
| Language        | Python                  |
| Frontend        | Streamlit               |
| PDF Processing  | PyPDF2                  |
| Embeddings      | Sentence Transformers   |
| Vector Search   | FAISS                   |
| LLM             | OpenAI API *(optional)* |
| Version Control | Git & GitHub            |

---

## 📂 Project Structure

```text
SmartNotesAI/
│
├── app.py                  # Streamlit application
├── requirements.txt        # Project dependencies
├── README.md
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI
├── tests/                  # Basic unit tests
└── assets/                 # Screenshots and images (optional)
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/AnwitaKunwar/SmartNotes.git
cd SmartNotes
```

### 2. Create a Virtual Environment

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the Application

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

## ⚙️ How It Works

1. Upload one or more PDF study notes.
2. Extract text from each document.
3. Split the text into meaningful chunks.
4. Convert chunks into vector embeddings.
5. Store embeddings in a FAISS vector database.
6. Retrieve the most relevant passages for a user query.
7. Generate an answer using the retrieved context.

This workflow follows the **Retrieval-Augmented Generation (RAG)** architecture used in many production AI assistants.

---

## 💡 Future Improvements

* Multi-document conversations
* Chat history and memory
* OCR support for scanned PDFs
* Hybrid keyword + semantic search
* Citation highlighting
* Support for DOCX, PPTX, and Markdown
* User authentication
* Cloud deployment

---

## 🌐 Deployment

SmartNotesAI is deployment-ready for platforms such as:

* Streamlit Community Cloud
* Render
* Hugging Face Spaces
