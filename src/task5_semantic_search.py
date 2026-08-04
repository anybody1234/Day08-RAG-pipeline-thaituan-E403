"""
Task 5 — Semantic Search Module.

Viết module tìm kiếm ngữ nghĩa (dense retrieval) trên vector store (ChromaDB).

Yêu cầu:
    - Input: query string + top_k
    - Output: danh sách chunks có score, sorted descending
    - Tương thích với embedding model (all-MiniLM-L6-v2) và vector store (ChromaDB) ở Task 4
"""

from .task4_chunking_indexing import get_collection, get_embedding_model


def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm ngữ nghĩa sử dụng vector similarity (cosine).

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {
            'content': str,      # Nội dung chunk
            'score': float,      # Cosine similarity score (0-1, higher = more similar)
            'metadata': dict     # source, type, chunk_index
        }
        Sorted by score descending.
    """
    # Bước 1: Embed query bằng cùng model ở Task 4
    model = get_embedding_model()
    query_vector = model.encode(query).tolist()

    # Bước 2: Query ChromaDB (cosine distance)
    collection = get_collection()

    # Đảm bảo top_k không vượt quá số documents trong collection
    count = collection.count()
    if count == 0:
        return []
    actual_top_k = min(top_k, count)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=actual_top_k,
        include=["documents", "metadatas", "distances"],
    )

    # Bước 3: Convert cosine distance → cosine similarity score
    # ChromaDB trả về cosine distance (0 = identical, 2 = opposite)
    # Similarity = 1 - distance (for cosine space)
    output = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        # Cosine distance → similarity: score = max(0, 1 - dist)
        score = max(0.0, 1.0 - dist)
        output.append({
            "content": doc,
            "score": round(score, 4),
            "metadata": meta,
        })

    # Sort descending by score
    output.sort(key=lambda x: x["score"], reverse=True)
    return output[:top_k]


if __name__ == "__main__":
    # Test
    test_queries = [
        "what is the difference between band 6 and band 7 lexical resource",
        "cohesive devices for band 8 cause and effect essay",
        "task achievement band 9 criteria",
    ]

    for q in test_queries:
        print(f"\nQuery: {q}")
        print("-" * 50)
        results = semantic_search(q, top_k=3)
        for i, r in enumerate(results, 1):
            print(f"  {i}. [{r['score']:.3f}] {r['content'][:80]}...")
