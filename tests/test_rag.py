from app import chunk_text, find_relevant_chunks, build_embedding


def test_chunk_text_splits_long_content():
    text = "This is a long note about machine learning and neural networks for students studying AI fundamentals. " * 3
    chunks = chunk_text(text, max_chars=120, overlap=20)
    assert len(chunks) >= 2
    assert all(chunk.strip() for chunk in chunks)


def test_find_relevant_chunks_prioritizes_matches():
    chunks = [
        "The theory of relativity explains time and space.",
        "Photosynthesis converts sunlight into chemical energy.",
        "Machine learning models improve with examples.",
    ]
    vocabulary = sorted({token for text in chunks for token in text.lower().split()})
    query = "What is relativity?"
    ranked = find_relevant_chunks(query, chunks, vocabulary)
    assert ranked[0]["text"] == chunks[0]
