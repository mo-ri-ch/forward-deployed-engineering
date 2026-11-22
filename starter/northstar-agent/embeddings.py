"""Turn text into embeddings: lists of numbers that capture meaning.

Uses all-MiniLM-L6-v2, a small free model that runs inside Colab (no key, 384 numbers per text).
If it can't be downloaded, it falls back to a simpler method based on letter patterns, so the
notebook still runs. The fallback is worse at meaning, so your scores will differ.
"""
import numpy as np

_model = None
method = None


def _load():
    global _model, method
    try:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        method = "all-MiniLM-L6-v2"
    except Exception as e:
        from sklearn.feature_extraction.text import HashingVectorizer
        _model = HashingVectorizer(analyzer="char_wb", ngram_range=(3, 5), n_features=4096, alternate_sign=False)
        method = "letter patterns (fallback)"
        print(f"Couldn't load the embeddings model ({type(e).__name__}), so using the simpler fallback.")
    print("Embeddings:", method)


def embed(texts):
    """Return one row of numbers per text, each scaled to length 1."""
    if _model is None:
        _load()
    if method == "all-MiniLM-L6-v2":
        return _model.encode(list(texts), normalize_embeddings=True)
    vectors = _model.transform(list(texts)).toarray()
    return vectors / np.maximum(np.linalg.norm(vectors, axis=1, keepdims=True), 1e-9)
