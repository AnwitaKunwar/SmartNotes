import io
import os
import re
from collections import Counter
from typing import List, Dict, Tuple

import numpy as np
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency path
    OpenAI = None

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY and OpenAI else None

st.set_page_config(page_title="College Notes AI", page_icon="📚", layout="wide")


def normalize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "")
    text = re.sub(r"[^\w\s.-]", " ", text)
    return text.strip()


def chunk_text(text: str, max_chars: int = 800, overlap: int = 120) -> List[str]:
    cleaned = normalize_text(text)
    if not cleaned:
        return []

    chunks: List[str] = []
    start = 0
    while start < len(cleaned):
        end = min(len(cleaned), start + max_chars)
        segment = cleaned[start:end].strip()
        if not segment:
            break

        if end < len(cleaned):
            last_space = segment.rfind(" ")
            if last_space > max_chars // 2:
                end = start + last_space
                segment = cleaned[start:end].strip()

        if segment:
            chunks.append(segment)

        if end >= len(cleaned):
            break
        start = max(start + 1, end - overlap)

    return [chunk for chunk in chunks if chunk]


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


def build_embedding(text: str, vocabulary: List[str]) -> np.ndarray:
    counts = Counter(tokenize(text))
    vector = np.zeros(len(vocabulary), dtype=float)
    for idx, term in enumerate(vocabulary):
        vector[idx] = counts.get(term, 0)
    return vector


def cosine_similarity(left: np.ndarray, right: np.ndarray) -> float:
    left_norm = np.linalg.norm(left)
    right_norm = np.linalg.norm(right)
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return float(np.dot(left, right) / (left_norm * right_norm))


def find_relevant_chunks(query: str, chunks: List[str], vocabulary: List[str]) -> List[Dict[str, object]]:
    if not chunks:
        return []

    query_vector = build_embedding(query, vocabulary)
    scored: List[Dict[str, object]] = []
    for chunk in chunks:
        chunk_vector = build_embedding(chunk, vocabulary)
        score = cosine_similarity(query_vector, chunk_vector)
        scored.append({"text": chunk, "score": score})

    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored


def extract_pdf_text(uploaded_file) -> str:
    bytes_content = uploaded_file.getvalue()
    reader = PdfReader(io.BytesIO(bytes_content))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def build_knowledge_base(uploaded_files) -> Tuple[List[Dict[str, object]], List[Dict[str, object]], List[str]]:
    documents: List[Dict[str, object]] = []
    chunks: List[Dict[str, object]] = []

    for uploaded_file in uploaded_files:
        raw_text = extract_pdf_text(uploaded_file)
        cleaned_text = normalize_text(raw_text)
        if not cleaned_text:
            continue

        page_chunks = chunk_text(cleaned_text)
        for index, chunk in enumerate(page_chunks):
            chunks.append(
                {
                    "source": uploaded_file.name,
                    "chunk_index": index,
                    "text": chunk,
                }
            )

        documents.append({"name": uploaded_file.name, "text": cleaned_text, "chunk_count": len(page_chunks)})

    vocabulary = sorted({token for chunk in chunks for token in tokenize(chunk["text"])})
    return documents, chunks, vocabulary


def answer_question(query: str, retrieved_chunks: List[Dict[str, object]]) -> str:
    if client and retrieved_chunks:
        context = "\n\n".join(f"- {chunk['text']}" for chunk in retrieved_chunks[:4])
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful study assistant. Answer using only the retrieved notes. If the evidence is weak, mention that.",
                },
                {
                    "role": "user",
                    "content": f"Question: {query}\n\nRetrieved notes:\n{context}",
                },
            ],
        )
        return response.choices[0].message.content.strip()

    if not retrieved_chunks:
        return "Upload notes and ask a question to begin the RAG workflow."

    top_chunk = retrieved_chunks[0]["text"]
    return f"Based on the uploaded notes, the closest match is: {top_chunk[:600]}"


def main() -> None:
    st.title("College Notes AI")
    st.caption("Upload PDF notes, build a retrieval layer, and ask questions in natural language.")

    if "documents" not in st.session_state:
        st.session_state.documents = []
    if "chunks" not in st.session_state:
        st.session_state.chunks = []
    if "vocabulary" not in st.session_state:
        st.session_state.vocabulary = []

    with st.sidebar:
        st.subheader("Knowledge base")
        uploaded_files = st.file_uploader("Upload PDF notes", type=["pdf"], accept_multiple_files=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Build knowledge base"):
                if not uploaded_files:
                    st.warning("Please upload at least one PDF first.")
                else:
                    documents, chunks, vocabulary = build_knowledge_base(uploaded_files)
                    st.session_state.documents = documents
                    st.session_state.chunks = chunks
                    st.session_state.vocabulary = vocabulary
                    st.success(f"Indexed {len(documents)} document(s) and {len(chunks)} chunk(s).")
        with col2:
            if st.button("Clear"):
                st.session_state.documents = []
                st.session_state.chunks = []
                st.session_state.vocabulary = []
                st.success("Knowledge base cleared.")

        if st.session_state.documents:
            st.metric("Documents", len(st.session_state.documents))
            st.metric("Chunks", len(st.session_state.chunks))
        else:
            st.info("No notes indexed yet.")

    if st.session_state.documents:
        st.success("Knowledge base ready. Ask a question about the uploaded material.")
    else:
        st.info("Upload one or more PDFs and click Build knowledge base to start.")

    query = st.text_input("Ask a question about your notes", placeholder="Summarize the core ideas from these notes")
    if st.button("Ask") and query:
        if not st.session_state.chunks:
            st.warning("Build a knowledge base before asking questions.")
        else:
            ranked_chunks = find_relevant_chunks(query, [chunk["text"] for chunk in st.session_state.chunks], st.session_state.vocabulary)
            answer = answer_question(query, ranked_chunks[:4])
            st.subheader("Answer")
            st.write(answer)

            st.subheader("Most relevant snippets")
            for item in ranked_chunks[:4]:
                score = item["score"]
                st.caption(f"Similarity score: {score:.2f}")
                st.write(item["text"])
                st.divider()


if __name__ == "__main__":
    main()
