"""
Task 9 — Retrieval Pipeline Hoàn Chỉnh.

Kết hợp semantic search + lexical search + reranking + PageIndex fallback
thành một pipeline thống nhất.

Logic:
    1. Chạy semantic_search + lexical_search
    2. Merge kết quả bằng RRF (Reciprocal Rank Fusion)
    3. Rerank (optional)
    4. Nếu top result cosine score gốc < threshold → fallback sang PageIndex
    5. Return top_k results

⚠️ QUAN TRỌNG: So threshold với điểm cosine gốc từ semantic_search,
   KHÔNG phải điểm RRF (xem README.md cho giải thích chi tiết).
"""

from .task5_semantic_search import semantic_search
from .task6_lexical_search import lexical_search
from .task7_reranking import rerank_rrf
from .task8_pageindex_vectorless import pageindex_search

# =============================================================================
# CONFIGURATION
# =============================================================================

# Threshold dựa trên cosine similarity gốc từ semantic_search (thang [0,1]).
# Calibrate bằng cách chạy query liên quan (score ~0.5-0.8) vs query lạc đề (score ~0.2-0.3).
# 0.3 là ngưỡng hợp lý: dưới 0.3 → nội dung rất ít liên quan.
SCORE_THRESHOLD = 0.48
DEFAULT_TOP_K = 5
RERANK_METHOD = "rrf"  # "cross_encoder" | "mmr" | "rrf"


def retrieve(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    score_threshold: float = SCORE_THRESHOLD,
    use_reranking: bool = True,
) -> list[dict]:
    """
    Retrieval pipeline hoàn chỉnh với fallback logic.

    Pipeline:
        Query
          ├→ Semantic Search → dense_results (giữ điểm cosine gốc)
          ├→ Lexical Search  → sparse_results
          │
          ├→ Merge (RRF) → merged_results
          │
          └→ If dense_results[0]["score"] < threshold:
                └→ PageIndex Vectorless → fallback_results

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả cuối cùng
        score_threshold: Ngưỡng điểm cosine gốc tối thiểu (KHÔNG phải điểm RRF)
        use_reranking: Có áp dụng RRF merge hay không

    Returns:
        List of {
            'content': str,
            'score': float,
            'metadata': dict,
            'source': str  # 'hybrid' hoặc 'pageindex'
        }
    """
    # Step 1: Chạy semantic search + lexical search
    dense_results = semantic_search(query, top_k=top_k * 2)
    sparse_results = lexical_search(query, top_k=top_k * 2)

    # Step 2: Merge bằng RRF
    if use_reranking and dense_results and sparse_results:
        merged = rerank_rrf(
            [dense_results, sparse_results],
            top_k=top_k * 2,
            k=60,
        )
    elif dense_results:
        merged = dense_results[:top_k * 2]
    elif sparse_results:
        merged = sparse_results[:top_k * 2]
    else:
        merged = []

    # Gắn source marker
    for item in merged:
        item["source"] = "hybrid"

    # Step 3: Lấy top_k kết quả
    final_results = merged[:top_k]

    # Step 4: Check threshold DÙNG ĐIỂM COSINE GỐC (dense_results), KHÔNG PHẢI RRF
    # Điểm RRF chỉ phụ thuộc thứ hạng, không phản ánh độ liên quan thực sự.
    best_cosine_score = dense_results[0]["score"] if dense_results else 0.0

    if best_cosine_score < score_threshold:
        print(f"  ⚠ Semantic best score ({best_cosine_score:.3f}) < threshold ({score_threshold})")
        print(f"    → Triggering PageIndex fallback...")
        fallback = pageindex_search(query, top_k=top_k)
        if fallback:
            return fallback
        else:
            print(f"    → PageIndex cũng không có kết quả. Trả về hybrid results.")

    return final_results


if __name__ == "__main__":
    test_queries = [
        "What is the difference between Band 6 and Band 7 in Lexical Resource?",
        "How to use cohesive devices for Band 8 in cause and effect essay?",
        "Band 9 task achievement criteria for IELTS Writing Task 2",
        "xyzabc123nonsense",  # Query vô nghĩa → test fallback
    ]

    for q in test_queries:
        print(f"\nQuery: {q}")
        print("-" * 60)
        results = retrieve(q, top_k=3)
        for i, r in enumerate(results, 1):
            src = r.get("source", "unknown")
            print(f"  {i}. [{r['score']:.4f}] [{src}] {r['content'][:80]}...")
