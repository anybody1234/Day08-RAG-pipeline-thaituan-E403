"""
Task 7 — Reranking Module.

Implement RRF (Reciprocal Rank Fusion) — không cần API key, phù hợp cho
merge kết quả từ semantic search + lexical search.

RRF hoạt động thế nào:
    - Công thức: RRF(d) = Σ 1 / (k + rank_r(d))
    - k = 60 (smoothing constant, từ paper Cormack et al. 2009)
    - Gộp kết quả từ nhiều ranker dựa trên thứ hạng, không phải score
    - Ưu điểm: không cần normalize score giữa các ranker khác nhau

Lưu ý quan trọng:
    Điểm RRF CHỈ phụ thuộc thứ hạng — top-1 luôn ≈ 1/(k+1) ≈ 0.0164 (k=60),
    BẤT KỂ nội dung liên quan hay không. ĐỪNG dùng điểm RRF để quyết định fallback.
"""

from typing import Optional

import numpy as np


def rerank_rrf(
    ranked_lists: list[list[dict]], top_k: int = 5, k: int = 60
) -> list[dict]:
    """
    Reciprocal Rank Fusion — gộp kết quả từ nhiều ranker.

    RRF(d) = Σ 1 / (k + rank_r(d))

    Args:
        ranked_lists: List of ranked result lists (mỗi list từ 1 ranker)
        top_k: Số lượng kết quả cuối cùng
        k: Smoothing constant (default=60, từ paper Cormack et al. 2009)

    Returns:
        List of top_k candidates sorted by RRF score descending.
    """
    rrf_scores = {}  # content -> score
    content_map = {}  # content -> full dict (giữ dict đầu tiên gặp)

    for ranked_list in ranked_lists:
        for rank, item in enumerate(ranked_list, 1):
            key = item["content"]
            rrf_scores[key] = rrf_scores.get(key, 0) + 1 / (k + rank)
            # Giữ item đầu tiên (có thể có score cao hơn)
            if key not in content_map:
                content_map[key] = item

    # Sort by RRF score descending
    sorted_items = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)

    results = []
    for content, score in sorted_items[:top_k]:
        item = content_map[content].copy()
        item["rrf_score"] = round(score, 6)  # Giữ RRF score riêng
        item["score"] = round(score, 6)      # Score chính dùng để display
        results.append(item)

    return results


def rerank_cross_encoder(
    query: str, candidates: list[dict], top_k: int = 5
) -> list[dict]:
    """
    Rerank candidates sử dụng cross-encoder model (Jina API).

    Args:
        query: Câu truy vấn
        candidates: List of {'content': str, 'score': float, 'metadata': dict}
        top_k: Số lượng kết quả sau rerank

    Returns:
        List of top_k candidates, re-scored và sorted by rerank_score descending.
    """
    import os
    import requests

    jina_api_key = os.getenv("JINA_API_KEY", "")
    if not jina_api_key:
        print("  ⚠ JINA_API_KEY không có, fallback sang RRF")
        return rerank_rrf([candidates], top_k=top_k)

    try:
        response = requests.post(
            "https://api.jina.ai/v1/rerank",
            headers={
                "Authorization": f"Bearer {jina_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "jina-reranker-v2-base-multilingual",
                "query": query,
                "documents": [c["content"] for c in candidates],
                "top_n": top_k,
            },
            timeout=30,
        )
        response.raise_for_status()
        reranked = response.json()["results"]
        return [
            {**candidates[r["index"]], "score": r["relevance_score"]}
            for r in reranked
        ]
    except Exception as e:
        print(f"  ⚠ Jina reranker failed ({e}), fallback sang RRF")
        return rerank_rrf([candidates], top_k=top_k)


def rerank_mmr(
    query_embedding: list[float],
    candidates: list[dict],
    top_k: int = 5,
    lambda_param: float = 0.7,
) -> list[dict]:
    """
    Maximal Marginal Relevance — chọn candidates vừa relevant vừa diverse.

    MMR = λ * sim(query, doc) - (1-λ) * max(sim(doc, selected_docs))

    Args:
        query_embedding: Vector embedding của query
        candidates: List with 'embedding' key
        top_k: Số lượng kết quả
        lambda_param: Trade-off relevance (1.0) vs diversity (0.0)

    Returns:
        List of top_k candidates selected by MMR.
    """
    if not candidates:
        return []

    def cosine_sim(a, b):
        a = np.array(a)
        b = np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))

    selected = []
    remaining = list(range(len(candidates)))

    for _ in range(min(top_k, len(candidates))):
        best_idx = None
        best_score = float('-inf')

        for idx in remaining:
            # Relevance to query
            if "embedding" in candidates[idx]:
                relevance = cosine_sim(query_embedding, candidates[idx]["embedding"])
            else:
                relevance = candidates[idx].get("score", 0)

            # Max similarity to already selected
            max_sim_to_selected = 0
            for sel_idx in selected:
                if "embedding" in candidates[idx] and "embedding" in candidates[sel_idx]:
                    sim = cosine_sim(candidates[idx]["embedding"], candidates[sel_idx]["embedding"])
                    max_sim_to_selected = max(max_sim_to_selected, sim)

            # MMR score
            mmr_score = lambda_param * relevance - (1 - lambda_param) * max_sim_to_selected

            if mmr_score > best_score:
                best_score = mmr_score
                best_idx = idx

        if best_idx is not None:
            selected.append(best_idx)
            remaining.remove(best_idx)

    return [candidates[i] for i in selected]


# =============================================================================
# Main rerank interface
# =============================================================================

def rerank(
    query: str,
    candidates: list[dict],
    top_k: int = 5,
    method: str = "rrf",  # "cross_encoder" | "mmr" | "rrf"
) -> list[dict]:
    """
    Unified reranking interface.

    Args:
        query: Câu truy vấn
        candidates: Danh sách candidates từ retrieval
        top_k: Số lượng kết quả sau rerank
        method: Phương pháp reranking

    Returns:
        List of top_k reranked candidates.
    """
    if not candidates:
        return []

    if method == "cross_encoder":
        return rerank_cross_encoder(query, candidates, top_k)
    elif method == "rrf":
        # RRF với single list — giữ nguyên thứ tự nhưng gán RRF score
        return rerank_rrf([candidates], top_k=top_k)
    elif method == "mmr":
        # MMR cần query_embedding
        from .task4_chunking_indexing import get_embedding_model
        model = get_embedding_model()
        query_emb = model.encode(query).tolist()
        return rerank_mmr(query_emb, candidates, top_k=top_k)
    else:
        raise ValueError(f"Unknown rerank method: {method}")


if __name__ == "__main__":
    # Test with dummy data
    dummy_candidates = [
        {"content": "IELTS Writing Task 2 Band Descriptors", "score": 0.8, "metadata": {}},
        {"content": "Band 8 Lexical Resource criteria", "score": 0.6, "metadata": {}},
        {"content": "Cohesive devices for Band 8 essays", "score": 0.5, "metadata": {}},
    ]
    results = rerank("IELTS band 8 criteria", dummy_candidates, top_k=2)
    for r in results:
        print(f"[{r['score']:.4f}] {r['content']}")
