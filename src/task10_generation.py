"""
Task 10 — Generation Có Citation.

Hướng dẫn:
    1. Sắp xếp lại chunks sau reranking để tránh "lost in the middle"
    2. Format context với source labels cho citation
    3. Inject vào prompt và gọi LLM
    4. Return answer có citation + sources

LLM: OpenRouter API (OpenAI-compatible interface)
    - Base URL: https://openrouter.ai/api/v1
    - Dùng model ":free" nếu chưa có credit
    - Xem models: https://openrouter.ai/models?max_price=0
"""

import os

from dotenv import load_dotenv

load_dotenv()

from .task9_retrieval_pipeline import retrieve

# =============================================================================
# CONFIGURATION — Giải thích lựa chọn
# =============================================================================

# top_k: Số chunks đưa vào context
# Chọn 5 vì: đủ evidence cho IELTS band descriptors mà không quá dài
# (mỗi chunk ~500 chars → 5 chunks ≈ 2500 chars context, nằm gọn trong window)
TOP_K = 5

# top_p (nucleus sampling): Xác suất tích luỹ cho token generation
# Chọn 0.9 vì: đủ diverse cho câu trả lời tự nhiên nhưng không quá random
TOP_P = 0.9

# temperature: Độ ngẫu nhiên của output
# Chọn 0.3 vì: RAG cần factual accuracy, ít sáng tạo
# IELTS band descriptors cần trích dẫn chính xác, không cần paraphrase nhiều
TEMPERATURE = 0.3

# LLM model — OpenRouter model ID
# openai/gpt-4o-mini: cân bằng chất lượng vs chi phí
# Nếu chưa có credit → đổi sang model ":free"
LLM_MODEL = "openai/gpt-4o-mini"


# =============================================================================
# SYSTEM PROMPT
# =============================================================================

SYSTEM_PROMPT = """Bạn là trợ lý tra cứu tiêu chí chấm điểm IELTS (Band Descriptors)
và phân tích bài essay mẫu Band 8.0+.

Quy tắc bắt buộc:
1. Chỉ sử dụng thông tin từ context được cung cấp — KHÔNG bịa đặt
2. Mỗi khẳng định phải có trích dẫn ngay sau, ví dụ: [IELTS Writing Task 2 Band Descriptors, 2026]
3. Nếu context không đủ thông tin → trả lời: "Tôi không thể xác minh thông tin này từ nguồn hiện có"
4. Trả lời bằng tiếng Việt, có cấu trúc rõ ràng
5. Khi so sánh band scores, trình bày dạng bảng hoặc điểm nổi bật rõ ràng
6. Khi phân tích essay mẫu, chỉ ra cụ thể từ/cụm từ minh họa"""


# =============================================================================
# DOCUMENT REORDERING (tránh lost in the middle)
# =============================================================================

def reorder_for_llm(chunks: list[dict]) -> list[dict]:
    """
    Sắp xếp chunks để tránh "lost in the middle" effect.

    LLM nhớ tốt thông tin ở ĐẦU và CUỐI prompt, quên thông tin ở GIỮA.
    Strategy: đặt chunks quan trọng nhất ở đầu và cuối, kém quan trọng ở giữa.

    Input order (by score):  [1, 2, 3, 4, 5]
    Output order:            [1, 3, 5, 4, 2]
    (best first, worst in middle, second-best last)

    Reference: Liu et al. (2023), "Lost in the Middle: How Language Models Use Long Contexts"

    Args:
        chunks: List sorted by score descending (from retrieval)

    Returns:
        List reordered để maximize LLM attention.
    """
    if len(chunks) <= 2:
        return chunks

    # Indices chẵn (0, 2, 4, ...) → đặt ở đầu (most important first)
    front = chunks[::2]
    # Indices lẻ (1, 3, ...) → đặt ở cuối, reversed (second-best last)
    back = chunks[1::2]

    return front + back[::-1]


# =============================================================================
# CONTEXT FORMATTING
# =============================================================================

def format_context(chunks: list[dict]) -> str:
    """
    Format chunks thành context string cho prompt.
    Mỗi chunk có label source để LLM có thể cite.

    Args:
        chunks: List of {'content': str, 'metadata': dict, 'score': float}

    Returns:
        Formatted context string.
    """
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source = chunk.get("metadata", {}).get("source", f"Source {i}")
        doc_type = chunk.get("metadata", {}).get("type", "unknown")
        score = chunk.get("score", 0)

        context_parts.append(
            f"[Document {i} | Source: {source} | Type: {doc_type} | Relevance: {score:.3f}]\n"
            f"{chunk['content']}\n"
        )

    return "\n---\n".join(context_parts)


# =============================================================================
# GENERATION
# =============================================================================

def generate_with_citation(query: str, top_k: int = TOP_K) -> dict:
    """
    End-to-end RAG generation có citation.

    Pipeline:
        1. Retrieve relevant chunks (Task 9)
        2. Reorder để tránh lost in the middle
        3. Format context với source labels
        4. Build prompt (system + context + query)
        5. Call LLM (OpenRouter API — OpenAI-compatible)
        6. Return answer + sources

    Args:
        query: Câu hỏi của user

    Returns:
        {
            'answer': str,           # Câu trả lời có citation
            'sources': list[dict],   # Các chunks đã dùng
            'retrieval_source': str  # 'hybrid' hoặc 'pageindex'
        }
    """
    # Step 1: Retrieve
    chunks = retrieve(query, top_k=top_k)

    if not chunks:
        return {
            "answer": "Tôi không tìm thấy thông tin liên quan trong cơ sở dữ liệu. "
                      "Vui lòng thử câu hỏi khác về tiêu chí chấm điểm IELTS hoặc bài essay mẫu.",
            "sources": [],
            "retrieval_source": "none",
        }

    # Step 2: Reorder để tránh lost in the middle
    reordered = reorder_for_llm(chunks)

    # Step 3: Format context
    context = format_context(reordered)

    # Step 4: Build prompt
    user_message = f"""Context:\n{context}\n\n---\n\nQuestion: {query}"""

    # Step 5: Call LLM
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        # Nếu không có API key → trả lời dựa trên context trực tiếp (no LLM)
        return {
            "answer": _generate_without_llm(query, reordered),
            "sources": chunks,
            "retrieval_source": chunks[0].get("source", "hybrid") if chunks else "none",
        }

    try:
        from openai import OpenAI

        # Xác định base_url dựa trên API key
        if os.getenv("OPENROUTER_API_KEY"):
            base_url = "https://openrouter.ai/api/v1"
            model = LLM_MODEL
        elif os.getenv("OPENAI_API_KEY"):
            base_url = "https://api.openai.com/v1"
            model = "gpt-4o-mini"
        else:
            base_url = "https://openrouter.ai/api/v1"
            model = LLM_MODEL

        client = OpenAI(api_key=api_key, base_url=base_url)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=TEMPERATURE,
            top_p=TOP_P,
            max_tokens=1024,
        )

        answer = response.choices[0].message.content

    except Exception as e:
        print(f"  ⚠ LLM call failed ({e}), using fallback generation")
        answer = _generate_without_llm(query, reordered)

    # Step 6: Return
    return {
        "answer": answer,
        "sources": chunks,
        "retrieval_source": chunks[0].get("source", "hybrid") if chunks else "none",
    }


def _generate_without_llm(query: str, chunks: list[dict]) -> str:
    """
    Fallback generation khi không có LLM API key.
    Trả về context trực tiếp với format đẹp.
    """
    parts = [
        f"**Câu hỏi:** {query}\n",
        "**Thông tin tìm được từ cơ sở dữ liệu IELTS:**\n",
    ]

    for i, chunk in enumerate(chunks[:3], 1):
        source = chunk.get("metadata", {}).get("source", f"Source {i}")
        parts.append(f"\n**[{i}] Nguồn: {source}**\n")
        # Lấy 500 ký tự đầu tiên
        content = chunk["content"][:500]
        parts.append(f"{content}\n")

    parts.append(
        "\n---\n"
        "*Lưu ý: Đây là kết quả retrieval trực tiếp (không qua LLM). "
        "Để có câu trả lời tổng hợp, hãy cấu hình OPENROUTER_API_KEY trong file .env*"
    )

    return "\n".join(parts)


if __name__ == "__main__":
    test_queries = [
        "Sự khác biệt giữa Band 6 và Band 7 ở tiêu chí Lexical Resource trong Task 2 là gì?",
        "Cho tôi ví dụ cách dùng cohesive devices đạt Band 8 trong bài luận Cause and Effect.",
        "Band 9 Task Achievement cần những gì?",
    ]

    for q in test_queries:
        print(f"\n{'='*70}")
        print(f"Q: {q}")
        print("=" * 70)
        result = generate_with_citation(q)
        print(f"\nA: {result['answer']}")
        print(f"\n[Sources: {len(result['sources'])} chunks | via {result['retrieval_source']}]")
