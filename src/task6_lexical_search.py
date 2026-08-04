"""
Task 6 — Lexical Search Module (BM25).

Mặc định sử dụng BM25 (rank-bm25).

BM25 hoạt động thế nào:
    - Term Frequency (TF): từ xuất hiện nhiều trong document → điểm cao
    - Inverse Document Frequency (IDF): từ hiếm → quan trọng hơn
    - Document length normalization: document dài không bị ưu tiên quá mức
    - Formula: score(q,d) = Σ IDF(qi) * (tf(qi,d) * (k1+1)) / (tf(qi,d) + k1*(1-b+b*|d|/avgdl))
    - k1=1.5 (term saturation), b=0.75 (length normalization)

Cài đặt:
    pip install rank-bm25
"""

import re
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi

from .task4_chunking_indexing import get_collection

# =============================================================================
# CORPUS & BM25 INDEX (lazy initialization)
# =============================================================================

_corpus: list[dict] = []  # List of {'content': str, 'metadata': dict}
_bm25_index = None


def _tokenize(text: str) -> list[str]:
    """
    Tokenize text cho BM25.
    Đơn giản: lowercase + split theo whitespace + loại bỏ ký tự đặc biệt.
    """
    text = text.lower()
    # Loại bỏ ký tự đặc biệt, giữ lại chữ và số
    tokens = re.findall(r'\b\w+\b', text)
    return tokens


def _load_corpus_from_chromadb():
    """Load toàn bộ documents từ ChromaDB để build BM25 index."""
    global _corpus

    collection = get_collection()
    count = collection.count()

    if count == 0:
        print("  ⚠ ChromaDB collection rỗng! Chạy Task 4 trước.")
        return

    # Lấy toàn bộ documents từ ChromaDB
    results = collection.get(
        include=["documents", "metadatas"],
        limit=count,
    )

    _corpus = []
    for doc, meta in zip(results["documents"], results["metadatas"]):
        _corpus.append({
            "content": doc,
            "metadata": meta,
        })

    print(f"  ✓ Loaded {len(_corpus)} chunks từ ChromaDB cho BM25 index")


def build_bm25_index(corpus: list[dict] = None) -> BM25Okapi:
    """
    Xây dựng BM25 index từ corpus.

    Args:
        corpus: List of {'content': str, 'metadata': dict}.
                Nếu None, load từ ChromaDB.

    Returns:
        BM25Okapi index object
    """
    global _corpus, _bm25_index

    if corpus is not None:
        _corpus = corpus

    if not _corpus:
        _load_corpus_from_chromadb()

    if not _corpus:
        raise ValueError("Corpus rỗng — không thể build BM25 index")

    # Tokenize corpus
    tokenized_corpus = [_tokenize(doc["content"]) for doc in _corpus]
    _bm25_index = BM25Okapi(tokenized_corpus)

    return _bm25_index


def _ensure_index():
    """Đảm bảo BM25 index đã được build (lazy init)."""
    global _bm25_index
    if _bm25_index is None:
        build_bm25_index()


def lexical_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm từ khóa sử dụng BM25.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {
            'content': str,
            'score': float,      # BM25 score (higher = more relevant)
            'metadata': dict
        }
        Sorted by score descending.
    """
    _ensure_index()

    if not _corpus:
        return []

    # Tokenize query
    tokenized_query = _tokenize(query)

    # Tính BM25 scores
    scores = _bm25_index.get_scores(tokenized_query)

    # Lấy top_k indices (sorted descending)
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []
    for idx in top_indices:
        if scores[idx] > 0:
            results.append({
                "content": _corpus[idx]["content"],
                "score": float(round(scores[idx], 4)),
                "metadata": _corpus[idx]["metadata"],
            })

    return results


if __name__ == "__main__":
    # Test
    test_queries = [
        "lexical resource band 6 band 7 difference",
        "cohesive devices cause effect",
        "tuition fee payment methods",
    ]

    for q in test_queries:
        print(f"\nQuery: {q}")
        print("-" * 50)
        results = lexical_search(q, top_k=3)
        for i, r in enumerate(results, 1):
            print(f"  {i}. [{r['score']:.3f}] {r['content'][:80]}...")
