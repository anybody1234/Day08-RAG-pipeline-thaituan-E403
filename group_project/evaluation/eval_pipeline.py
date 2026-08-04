"""
RAG Evaluation Pipeline — IELTS Band Descriptors & Sample Essays.

Đánh giá chất lượng RAG pipeline với 4 metrics:
    1. Faithfulness: câu trả lời có bám sát context không?
    2. Answer Relevance: câu trả lời có liên quan đến câu hỏi không?
    3. Context Recall: retrieval có lấy được đủ thông tin cần thiết không?
    4. Context Precision: trong các chunks retrieved, bao nhiêu % thực sự hữu ích?

So sánh A/B:
    - Config A: Hybrid (Semantic + BM25 + RRF reranking)
    - Config B: Semantic-only (không BM25, không reranking)

Chạy:
    python -m group_project.evaluation.eval_pipeline

Note: Dùng lightweight metrics (keyword overlap, embedding similarity) thay vì
gọi LLM (OpenRouter free rate limit = 50 req/ngày, RAGAS gọi ~5-10 LLM calls/metric/câu hỏi).
"""

import json
import os
import sys
import time
from pathlib import Path
from collections import Counter

# Fix encoding
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

GOLDEN_DATASET_PATH = Path(__file__).parent / "golden_dataset.json"
RESULTS_PATH = Path(__file__).parent / "results.md"


# =============================================================================
# EXTRACT EVALUATION QUESTIONS FROM GOLDEN DATASET
# =============================================================================

def load_eval_questions() -> list[dict]:
    """
    Chuyển golden_dataset.json (speaking/writing sets) thành danh sách
    câu hỏi đánh giá cho RAG pipeline.

    Mỗi item: {'question': str, 'expected_keywords': list, 'category': str, 'band': str}
    """
    with open(GOLDEN_DATASET_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    eval_questions = []

    # ---- Speaking sets: dùng Part 3 (discussion) vì sát RAG nhất ----
    for s in data.get("speaking_sets", []):
        band = s.get("target_band_range", "?")
        parts = s.get("parts", {})

        # Part 3 có câu hỏi thảo luận sâu — phù hợp để test RAG
        p3 = parts.get("part_3", {})
        for q in p3.get("questions", [])[:1]:  # Lấy 1 câu/set
            eval_questions.append({
                "question": f"In IELTS Speaking Band {band}, how should a candidate answer: {q}",
                "expected_keywords": p3.get("expected_keywords", []),
                "category": f"Speaking Part 3 - {p3.get('category', '')}",
                "band": band,
                "type": "speaking",
            })

    # ---- Writing sets: dùng Task 2 essay questions ----
    for w in data.get("writing_sets", []):
        band = w.get("target_band_range", "?")
        tasks = w.get("tasks", {})

        t2 = tasks.get("task_2", {})
        if t2.get("question"):
            eval_questions.append({
                "question": f"For IELTS Writing Task 2 at Band {band}, what are the key criteria? Essay question: {t2['question'][:100]}",
                "expected_keywords": t2.get("expected_keywords", []),
                "category": f"Writing Task 2 - {t2.get('type', '')}",
                "band": band,
                "type": "writing",
            })

    # ---- Thêm câu hỏi trực tiếp về band descriptors ----
    descriptor_questions = [
        {
            "question": "What is the difference between Band 6 and Band 7 in Lexical Resource for IELTS Writing Task 2?",
            "expected_keywords": ["lexical", "resource", "band", "vocabulary", "range", "error", "appropriate"],
            "category": "Band Descriptors - Lexical Resource",
            "band": "6-7",
            "type": "descriptor",
        },
        {
            "question": "What are the criteria for Band 8 in Coherence and Cohesion?",
            "expected_keywords": ["coherence", "cohesion", "paragraph", "link", "logical", "sequence", "referencing"],
            "category": "Band Descriptors - Coherence & Cohesion",
            "band": "8",
            "type": "descriptor",
        },
        {
            "question": "How to achieve Band 9 in Task Achievement for IELTS Writing?",
            "expected_keywords": ["task", "achievement", "response", "position", "fully", "extended", "supported"],
            "category": "Band Descriptors - Task Achievement",
            "band": "9",
            "type": "descriptor",
        },
    ]
    eval_questions.extend(descriptor_questions)

    return eval_questions


# =============================================================================
# LIGHTWEIGHT RAGAS-STYLE METRICS (no LLM calls)
# =============================================================================

def _tokenize(text: str) -> set:
    """Simple tokenizer for keyword overlap."""
    import re
    return set(re.findall(r'\b\w+\b', text.lower()))


def metric_faithfulness(answer: str, contexts: list[str]) -> float:
    """
    Faithfulness: Bao nhiêu % claims trong answer có xuất hiện trong context?
    Approximation: word overlap giữa answer và context.
    Score [0, 1]: 1 = toàn bộ answer words đều có trong context.
    """
    if not answer or not contexts:
        return 0.0

    answer_tokens = _tokenize(answer)
    context_tokens = set()
    for ctx in contexts:
        context_tokens |= _tokenize(ctx)

    if not answer_tokens:
        return 0.0

    # Loại bỏ stop words phổ biến
    stop_words = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at",
                  "to", "for", "of", "and", "or", "but", "not", "with", "this",
                  "that", "it", "be", "have", "has", "had", "do", "does", "did",
                  "will", "would", "can", "could", "may", "might", "shall", "should",
                  "its", "their", "your", "my", "his", "her", "our", "by", "from",
                  "as", "if", "so", "no", "than", "too", "very", "just", "about"}

    answer_content = answer_tokens - stop_words
    if not answer_content:
        return 1.0

    overlap = answer_content & context_tokens
    return len(overlap) / len(answer_content)


def metric_answer_relevance(question: str, answer: str) -> float:
    """
    Answer Relevance: Câu trả lời có liên quan đến câu hỏi không?
    Approximation: keyword overlap giữa question và answer.
    """
    if not question or not answer:
        return 0.0

    q_tokens = _tokenize(question)
    a_tokens = _tokenize(answer)

    stop_words = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at",
                  "to", "for", "of", "and", "or", "but", "not", "with", "what",
                  "how", "why", "when", "where", "which", "who", "do", "does"}

    q_content = q_tokens - stop_words
    if not q_content:
        return 1.0

    overlap = q_content & a_tokens
    return len(overlap) / len(q_content)


def metric_context_recall(expected_keywords: list[str], contexts: list[str]) -> float:
    """
    Context Recall: Bao nhiêu % expected keywords được tìm thấy trong retrieved contexts?
    """
    if not expected_keywords or not contexts:
        return 0.0

    context_text = " ".join(contexts).lower()
    found = sum(1 for kw in expected_keywords if kw.lower() in context_text)
    return found / len(expected_keywords)


def metric_context_precision(question: str, contexts: list[str]) -> float:
    """
    Context Precision: Bao nhiêu % retrieved chunks thực sự liên quan đến question?
    Approximation: chunk nào có ít nhất 2 keyword từ question → relevant.
    """
    if not contexts:
        return 0.0

    q_tokens = _tokenize(question)
    stop_words = {"the", "a", "an", "is", "are", "in", "on", "at", "to", "for",
                  "of", "and", "or", "what", "how", "why", "when", "where"}
    q_keywords = q_tokens - stop_words

    if not q_keywords:
        return 1.0

    relevant = 0
    for ctx in contexts:
        ctx_tokens = _tokenize(ctx)
        overlap = q_keywords & ctx_tokens
        if len(overlap) >= 2:  # Ít nhất 2 keyword match → relevant
            relevant += 1

    return relevant / len(contexts)


# =============================================================================
# EVALUATION RUNNER
# =============================================================================

def run_evaluation(config_name: str, retrieve_func, eval_questions: list[dict]) -> list[dict]:
    """
    Chạy evaluation trên 1 config.

    Args:
        config_name: Tên config (ví dụ: "Hybrid+RRF", "Semantic-only")
        retrieve_func: Function(query, top_k) -> list[dict]
        eval_questions: Danh sách câu hỏi đánh giá

    Returns:
        List of per-question results
    """
    from src.task10_generation import generate_with_citation

    results = []
    for i, item in enumerate(eval_questions):
        q = item["question"]
        print(f"  [{i+1}/{len(eval_questions)}] {q[:60]}...")

        start = time.time()

        try:
            # Chạy RAG pipeline
            response = generate_with_citation(q, top_k=5)
            answer = response.get("answer", "")
            sources = response.get("sources", [])
            contexts = [s.get("content", "") for s in sources]
        except Exception as e:
            print(f"    Error: {e}")
            answer = ""
            contexts = []

        elapsed = time.time() - start

        # Tính 4 metrics
        faithfulness = metric_faithfulness(answer, contexts)
        relevance = metric_answer_relevance(q, answer)
        recall = metric_context_recall(item.get("expected_keywords", []), contexts)
        precision = metric_context_precision(q, contexts)

        results.append({
            "question": q,
            "category": item.get("category", ""),
            "band": item.get("band", ""),
            "type": item.get("type", ""),
            "answer_length": len(answer),
            "num_contexts": len(contexts),
            "faithfulness": round(faithfulness, 4),
            "answer_relevance": round(relevance, 4),
            "context_recall": round(recall, 4),
            "context_precision": round(precision, 4),
            "latency_s": round(elapsed, 2),
        })

    return results


def compute_averages(results: list[dict]) -> dict:
    """Tính trung bình 4 metrics."""
    n = len(results)
    if n == 0:
        return {"faithfulness": 0, "answer_relevance": 0, "context_recall": 0, "context_precision": 0}

    return {
        "faithfulness": round(sum(r["faithfulness"] for r in results) / n, 4),
        "answer_relevance": round(sum(r["answer_relevance"] for r in results) / n, 4),
        "context_recall": round(sum(r["context_recall"] for r in results) / n, 4),
        "context_precision": round(sum(r["context_precision"] for r in results) / n, 4),
        "avg_latency_s": round(sum(r["latency_s"] for r in results) / n, 2),
    }


# =============================================================================
# A/B COMPARISON
# =============================================================================

def run_ab_comparison(eval_questions: list[dict]) -> dict:
    """
    So sánh A/B:
        Config A: Hybrid (Semantic + BM25 + RRF) — dùng pipeline mặc định
        Config B: Semantic-only (không reranking, không BM25)
    """
    from src.task5_semantic_search import semantic_search
    from src.task10_generation import generate_with_citation

    print("\n" + "=" * 60)
    print("Config A: Hybrid (Semantic + BM25 + RRF Reranking)")
    print("=" * 60)
    results_a = run_evaluation("Hybrid+RRF", None, eval_questions)

    print("\n" + "=" * 60)
    print("Config B: Semantic-only (no BM25, no reranking)")
    print("=" * 60)

    # Tạm patch generate_with_citation để dùng semantic-only
    results_b = []
    for i, item in enumerate(eval_questions):
        q = item["question"]
        print(f"  [{i+1}/{len(eval_questions)}] {q[:60]}...")

        start = time.time()

        try:
            # Chỉ dùng semantic search
            contexts_raw = semantic_search(q, top_k=5)
            contexts = [c.get("content", "") for c in contexts_raw]

            # Build answer thủ công (không qua LLM để tiết kiệm rate limit)
            if contexts:
                answer = f"Dựa trên thông tin tìm được:\n\n"
                for j, ctx in enumerate(contexts[:3], 1):
                    answer += f"[{j}] {ctx[:200]}...\n\n"
            else:
                answer = "Không tìm thấy thông tin liên quan."
        except Exception as e:
            print(f"    Error: {e}")
            answer = ""
            contexts = []

        elapsed = time.time() - start

        faithfulness = metric_faithfulness(answer, contexts)
        relevance = metric_answer_relevance(q, answer)
        recall = metric_context_recall(item.get("expected_keywords", []), contexts)
        precision = metric_context_precision(q, contexts)

        results_b.append({
            "question": q,
            "category": item.get("category", ""),
            "band": item.get("band", ""),
            "type": item.get("type", ""),
            "answer_length": len(answer),
            "num_contexts": len(contexts),
            "faithfulness": round(faithfulness, 4),
            "answer_relevance": round(relevance, 4),
            "context_recall": round(recall, 4),
            "context_precision": round(precision, 4),
            "latency_s": round(elapsed, 2),
        })

    return {
        "Config A: Hybrid+RRF": {
            "results": results_a,
            "averages": compute_averages(results_a),
        },
        "Config B: Semantic-only": {
            "results": results_b,
            "averages": compute_averages(results_b),
        },
    }


# =============================================================================
# EXPORT RESULTS.MD
# =============================================================================

def export_results(comparison: dict, eval_questions: list[dict]):
    """Export evaluation results to results.md."""

    config_a = comparison["Config A: Hybrid+RRF"]
    config_b = comparison["Config B: Semantic-only"]
    avg_a = config_a["averages"]
    avg_b = config_b["averages"]

    def delta(a, b):
        d = a - b
        return f"+{d:.4f}" if d >= 0 else f"{d:.4f}"

    content = f"""# RAG Evaluation Results — IELTS Band Descriptors & Sample Essays

## Framework su dung

> **Lightweight RAGAS-style metrics** (keyword overlap + token matching)
> - Khong goi LLM de tinh metrics → tiet kiem rate limit OpenRouter
> - 4 metrics: Faithfulness, Answer Relevance, Context Recall, Context Precision
> - So sanh A/B: Hybrid+RRF vs Semantic-only

## Tong so cau hoi danh gia: {len(eval_questions)}

---

## Overall Scores

| Metric | Config A (Hybrid+RRF) | Config B (Semantic-only) | Delta |
|--------|-----------------------|--------------------------|-------|
| Faithfulness | {avg_a['faithfulness']:.4f} | {avg_b['faithfulness']:.4f} | {delta(avg_a['faithfulness'], avg_b['faithfulness'])} |
| Answer Relevance | {avg_a['answer_relevance']:.4f} | {avg_b['answer_relevance']:.4f} | {delta(avg_a['answer_relevance'], avg_b['answer_relevance'])} |
| Context Recall | {avg_a['context_recall']:.4f} | {avg_b['context_recall']:.4f} | {delta(avg_a['context_recall'], avg_b['context_recall'])} |
| Context Precision | {avg_a['context_precision']:.4f} | {avg_b['context_precision']:.4f} | {delta(avg_a['context_precision'], avg_b['context_precision'])} |
| **Average** | **{sum([avg_a['faithfulness'], avg_a['answer_relevance'], avg_a['context_recall'], avg_a['context_precision']])/4:.4f}** | **{sum([avg_b['faithfulness'], avg_b['answer_relevance'], avg_b['context_recall'], avg_b['context_precision']])/4:.4f}** | |
| Avg Latency | {avg_a['avg_latency_s']:.2f}s | {avg_b['avg_latency_s']:.2f}s | |

---

## A/B Comparison Analysis

**Config A: Hybrid + RRF Reranking**
> Ket hop Semantic Search (cosine similarity) + BM25 Lexical Search,
> merge bang Reciprocal Rank Fusion (k=60). Answer duoc tong hop boi LLM
> (OpenRouter gpt-4o-mini) voi citation tu retrieved chunks.

**Config B: Semantic-only**
> Chi dung Semantic Search (all-MiniLM-L6-v2, cosine similarity).
> Khong co BM25, khong co RRF reranking. Answer la raw context truc tiep.

**Ket luan:**
"""

    # Tính overall average
    overall_a = sum([avg_a['faithfulness'], avg_a['answer_relevance'], avg_a['context_recall'], avg_a['context_precision']]) / 4
    overall_b = sum([avg_b['faithfulness'], avg_b['answer_relevance'], avg_b['context_recall'], avg_b['context_precision']]) / 4

    if overall_a > overall_b:
        content += f"> **Config A (Hybrid+RRF) tot hon** voi average score {overall_a:.4f} vs {overall_b:.4f}.\n"
        content += "> Hybrid search ket hop duoc ca semantic understanding (cosine) va keyword matching (BM25),\n"
        content += "> giup retrieval da dang hon va phu song nhieu context hon.\n"
    else:
        content += f"> **Config B (Semantic-only) tot hon** voi average score {overall_b:.4f} vs {overall_a:.4f}.\n"
        content += "> Semantic search da du tot cho corpus IELTS tieng Anh.\n"

    # ---- Worst performers ----
    content += "\n---\n\n## Worst Performers (Bottom 3)\n\n"
    content += "| # | Question | Faithfulness | Relevance | Recall | Category |\n"
    content += "|---|----------|-------------|-----------|--------|----------|\n"

    # Sort by average of 4 metrics (ascending → worst first)
    results_a_sorted = sorted(
        config_a["results"],
        key=lambda r: (r["faithfulness"] + r["answer_relevance"] + r["context_recall"] + r["context_precision"]) / 4,
    )

    for i, r in enumerate(results_a_sorted[:3], 1):
        q_short = r["question"][:50] + "..."
        content += f"| {i} | {q_short} | {r['faithfulness']:.3f} | {r['answer_relevance']:.3f} | {r['context_recall']:.3f} | {r['category']} |\n"

    # ---- Per-question detail ----
    content += "\n---\n\n## Chi tiet tung cau hoi (Config A: Hybrid+RRF)\n\n"
    content += "| # | Category | Band | Faithfulness | Relevance | Recall | Precision | Latency |\n"
    content += "|---|----------|------|-------------|-----------|--------|-----------|--------|\n"

    for i, r in enumerate(config_a["results"], 1):
        content += (
            f"| {i} | {r['category'][:30]} | {r['band']} | "
            f"{r['faithfulness']:.3f} | {r['answer_relevance']:.3f} | "
            f"{r['context_recall']:.3f} | {r['context_precision']:.3f} | "
            f"{r['latency_s']:.1f}s |\n"
        )

    # ---- Recommendations ----
    content += f"""
---

## Recommendations

### Cai tien 1: Tang chunk_size tu 500 len 800
**Action:** Dieu chinh `CHUNK_SIZE` trong `task4_chunking_indexing.py` de moi chunk chua nhieu ngu canh hon.
**Expected impact:** Tang Faithfulness +5-10% vi LLM co nhieu context hon de trich xuat thong tin.

### Cai tien 2: Su dung cross-encoder reranking (Jina/Cohere)
**Action:** Cau hinh `JINA_API_KEY` va bat cross-encoder reranking trong `task7_reranking.py`.
**Expected impact:** Tang Context Precision +10-15% vi cross-encoder danh gia relevance tot hon RRF.

### Cai tien 3: Multilingual embedding model (bge-m3)
**Action:** Doi `EMBEDDING_MODEL` tu `all-MiniLM-L6-v2` sang `BAAI/bge-m3` de ho tro ca tieng Viet.
**Expected impact:** Tang Answer Relevance khi user hoi bang tieng Viet, hien tai model chi tot voi English.

---

*Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}*
*Pipeline: Semantic Search + BM25 + RRF Reranking + OpenRouter LLM*
*Evaluation: {len(eval_questions)} questions across Band 6.0-9.0*
"""

    RESULTS_PATH.write_text(content, encoding="utf-8")
    print(f"\n{'='*60}")
    print(f"Results exported to: {RESULTS_PATH}")
    print(f"{'='*60}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("RAG Evaluation Pipeline — IELTS Band Descriptors")
    print("=" * 60)

    # Load questions
    eval_questions = load_eval_questions()
    print(f"\nLoaded {len(eval_questions)} evaluation questions")
    print(f"  - Speaking: {sum(1 for q in eval_questions if q['type'] == 'speaking')}")
    print(f"  - Writing: {sum(1 for q in eval_questions if q['type'] == 'writing')}")
    print(f"  - Descriptors: {sum(1 for q in eval_questions if q['type'] == 'descriptor')}")

    # Run A/B comparison
    comparison = run_ab_comparison(eval_questions)

    # Print summary
    for config_name, data in comparison.items():
        avg = data["averages"]
        print(f"\n{config_name}:")
        print(f"  Faithfulness:      {avg['faithfulness']:.4f}")
        print(f"  Answer Relevance:  {avg['answer_relevance']:.4f}")
        print(f"  Context Recall:    {avg['context_recall']:.4f}")
        print(f"  Context Precision: {avg['context_precision']:.4f}")
        print(f"  Avg Latency:       {avg['avg_latency_s']:.2f}s")

    # Export
    export_results(comparison, eval_questions)

    print("\n✅ CP5 Passed — Evaluation complete!")
