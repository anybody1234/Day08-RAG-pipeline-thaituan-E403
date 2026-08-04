"""
RAG Chatbot — IELTS Band Descriptors & Sample Essays
Streamlit app with Retrieval Technique Comparison UI.

Chạy:
    streamlit run app.py
"""

import os
import sys
import time
from pathlib import Path

# Fix Windows encoding — charmap không encode được Unicode (✓, ⚠)
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Thêm project root vào sys.path để import các task từ src/
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="IELTS RAG Pipeline — Technique Comparison",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# CUSTOM CSS
# =============================================================================

st.markdown("""
<style>
    /* Card style for result items */
    .result-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #0f3460;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 10px;
    }
    .score-badge {
        background: linear-gradient(135deg, #e94560 0%, #0f3460 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85em;
        display: inline-block;
    }
    .technique-header {
        font-size: 1.1em;
        font-weight: 600;
        padding: 8px 0;
        border-bottom: 2px solid #0f3460;
        margin-bottom: 12px;
    }
    .metric-highlight {
        font-size: 1.8em;
        font-weight: 700;
        color: #e94560;
    }
    .overlap-tag {
        background: #2d6a4f;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.75em;
    }
    .unique-tag {
        background: #e76f51;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.75em;
    }
    /* Hide streamlit elements */
    .stDeployButton {display:none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SIDEBAR — SETTINGS & INFO
# =============================================================================

with st.sidebar:
    st.title("📝 IELTS RAG Assistant")
    st.caption("So sánh hiệu quả các kỹ thuật Retrieval")

    st.divider()

    st.subheader("💡 Câu hỏi gợi ý")
    suggestions = [
        "Sự khác biệt giữa Band 6 và Band 7 ở Lexical Resource?",
        "Cohesive devices cho Band 8 trong bài Cause-Effect",
        "Band 9 Task Achievement cần những gì?",
        "How to improve grammar for Band 7?",
        "Speaking Band 8 sample answers about music",
    ]
    for s in suggestions:
        if st.button(s, use_container_width=True, key=f"sug_{hash(s)}"):
            st.session_state["pending_query"] = s

    st.divider()

    st.subheader("⚙️ Thiết lập")
    top_k = st.slider("Số chunks retrieval (top_k)", 3, 15, 5)

    st.divider()

    st.subheader("📊 Kiến trúc Pipeline")
    st.markdown("""
    ```
    Query
     ├→ 🔵 Semantic Search (cosine)
     ├→ 🟢 Lexical Search (BM25)
     ├→ 🟡 Hybrid + RRF Rerank
     └→ 🔴 PageIndex (vectorless)
    ```
    """)

    st.divider()
    st.caption("**Dữ liệu:** IELTS Writing & Speaking Band Descriptors + Sample Essays Band 6.0→9.0")


# =============================================================================
# SESSION STATE
# =============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None
if "last_comparison" not in st.session_state:
    st.session_state.last_comparison = None

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def run_technique(name: str, func, query: str, top_k: int) -> dict:
    """Chạy 1 retrieval technique, đo thời gian."""
    start = time.time()
    try:
        results = func(query, top_k=top_k)
    except Exception as e:
        results = []
        st.warning(f"{name} lỗi: {e}")
    elapsed = time.time() - start
    return {
        "name": name,
        "results": results,
        "time_ms": round(elapsed * 1000, 1),
        "count": len(results),
    }


def get_content_set(results: list[dict]) -> set:
    """Lấy set nội dung để so sánh overlap."""
    return {r["content"][:100] for r in results}


def render_results_column(technique_data: dict, all_contents: dict):
    """Render kết quả của 1 technique trong 1 column."""
    name = technique_data["name"]
    results = technique_data["results"]
    time_ms = technique_data["time_ms"]
    count = technique_data["count"]

    # Metrics row
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Chunks", count)
    with col_b:
        st.metric("Thời gian", f"{time_ms}ms")

    if not results:
        st.info("Không có kết quả")
        return

    # Top score
    top_score = results[0]["score"] if results else 0
    st.markdown(f"**Top score:** `{top_score:.4f}`")

    # Results list
    my_contents = get_content_set(results)
    other_techniques = {k: v for k, v in all_contents.items() if k != name}

    for i, r in enumerate(results):
        content_key = r["content"][:100]
        score = r["score"]
        meta = r.get("metadata", {})
        source_file = meta.get("source", "?")
        sub_type = meta.get("sub_type", meta.get("type", ""))

        # Check overlap
        found_in = [t_name for t_name, t_set in other_techniques.items() if content_key in t_set]

        with st.container():
            # Header with score
            score_color = "🟢" if score > 0.5 else "🟡" if score > 0.3 else "🔴"
            st.markdown(f"**{i+1}.** {score_color} `{score:.4f}` — **{source_file}** `{sub_type}`")

            # Overlap tags
            if found_in:
                tags = " ".join([f"✅ {t}" for t in found_in])
                st.caption(f"Overlap: {tags}")
            else:
                st.caption("🔶 Unique — chỉ có ở kỹ thuật này")

            # Content preview
            with st.expander(f"Xem nội dung chunk", expanded=False):
                st.text(r["content"][:400])

            st.divider()


def compute_overlap_matrix(technique_results: dict) -> dict:
    """Tính overlap matrix giữa các techniques."""
    content_sets = {name: get_content_set(data["results"]) for name, data in technique_results.items()}
    matrix = {}
    for name_a, set_a in content_sets.items():
        matrix[name_a] = {}
        for name_b, set_b in content_sets.items():
            if name_a == name_b:
                matrix[name_a][name_b] = len(set_a)
            else:
                matrix[name_a][name_b] = len(set_a & set_b)
    return matrix


# =============================================================================
# MAIN UI
# =============================================================================

st.title("📝 IELTS RAG Pipeline — So Sánh Kỹ Thuật Retrieval")
st.caption("Nhập câu hỏi để xem kết quả từ **Semantic Search**, **BM25 Lexical**, **Hybrid + RRF**, và **PageIndex** cạnh nhau")

# Chat history (compact)
if st.session_state.messages:
    with st.expander(f"📜 Lịch sử chat ({len(st.session_state.messages)} tin nhắn)", expanded=False):
        for msg in st.session_state.messages:
            role_icon = "👤" if msg["role"] == "user" else "🤖"
            st.markdown(f"{role_icon} **{msg['role']}:** {msg['content'][:200]}...")

# =============================================================================
# QUERY INPUT
# =============================================================================

user_input = st.chat_input("Hỏi về IELTS Band Descriptors, Essay mẫu, Speaking samples...")
query = user_input or st.session_state.pending_query

if query:
    st.session_state.pending_query = None
    st.session_state.messages.append({"role": "user", "content": query})

    st.markdown(f"### 🔍 Query: *{query}*")
    st.divider()

    # =========================================================================
    # TAB 1: TECHNIQUE COMPARISON
    # =========================================================================

    tab_compare, tab_answer, tab_analysis = st.tabs([
        "📊 So sánh kỹ thuật",
        "💬 Câu trả lời LLM",
        "📈 Phân tích chi tiết",
    ])

    with tab_compare:
        with st.spinner("Đang chạy 4 kỹ thuật retrieval song song..."):
            # Import modules
            from src.task5_semantic_search import semantic_search
            from src.task6_lexical_search import lexical_search
            from src.task7_reranking import rerank_rrf
            from src.task8_pageindex_vectorless import pageindex_search

            # Run all techniques
            semantic_data = run_technique("🔵 Semantic", semantic_search, query, top_k)

            bm25_data = run_technique("🟢 BM25", lexical_search, query, top_k)

            # Hybrid + RRF
            start = time.time()
            try:
                dense = semantic_search(query, top_k=top_k * 2)
                sparse = lexical_search(query, top_k=top_k * 2)
                hybrid_results = rerank_rrf([dense, sparse], top_k=top_k, k=60)
                for item in hybrid_results:
                    item["source"] = "hybrid"
            except Exception as e:
                hybrid_results = []
                st.warning(f"Hybrid lỗi: {e}")
            hybrid_data = {
                "name": "🟡 Hybrid+RRF",
                "results": hybrid_results,
                "time_ms": round((time.time() - start) * 1000, 1),
                "count": len(hybrid_results),
            }

            pageindex_data = run_technique("🔴 PageIndex", pageindex_search, query, top_k)

            # Collect all results
            all_techniques = {
                "🔵 Semantic": semantic_data,
                "🟢 BM25": bm25_data,
                "🟡 Hybrid+RRF": hybrid_data,
                "🔴 PageIndex": pageindex_data,
            }

            # Save for analysis tab
            st.session_state.last_comparison = all_techniques

        # ----- SUMMARY METRICS -----
        st.subheader("⚡ Tổng quan hiệu suất")
        cols = st.columns(4)
        icons = ["🔵", "🟢", "🟡", "🔴"]
        for col, (name, data) in zip(cols, all_techniques.items()):
            with col:
                top_score = data["results"][0]["score"] if data["results"] else 0
                st.metric(
                    label=name,
                    value=f"{data['count']} chunks",
                    delta=f"{data['time_ms']}ms | top: {top_score:.3f}",
                )

        st.divider()

        # ----- SIDE-BY-SIDE RESULTS -----
        st.subheader("📋 Kết quả chi tiết — So sánh cạnh nhau")

        all_content_sets = {name: get_content_set(data["results"]) for name, data in all_techniques.items()}

        # Show 3 main techniques (PageIndex often empty)
        active_techniques = {k: v for k, v in all_techniques.items() if v["count"] > 0}

        if len(active_techniques) >= 3:
            cols = st.columns(3)
            for col, (name, data) in zip(cols, list(active_techniques.items())[:3]):
                with col:
                    st.markdown(f"#### {name}")
                    render_results_column(data, all_content_sets)
        elif len(active_techniques) >= 2:
            cols = st.columns(2)
            for col, (name, data) in zip(cols, list(active_techniques.items())[:2]):
                with col:
                    st.markdown(f"#### {name}")
                    render_results_column(data, all_content_sets)
        else:
            for name, data in active_techniques.items():
                st.markdown(f"#### {name}")
                render_results_column(data, all_content_sets)

        # PageIndex section (if has results)
        if pageindex_data["count"] > 0:
            st.divider()
            st.markdown("#### 🔴 PageIndex (Vectorless Fallback)")
            render_results_column(pageindex_data, all_content_sets)

    # =========================================================================
    # TAB 2: LLM ANSWER
    # =========================================================================

    with tab_answer:
        st.subheader("💬 Câu trả lời từ RAG Pipeline")

        with st.spinner("Đang tổng hợp câu trả lời từ LLM..."):
            try:
                from src.task10_generation import generate_with_citation
                response = generate_with_citation(query, top_k=top_k)
                answer = response.get("answer", "Chưa thể trả lời.")
                sources = response.get("sources", [])
                retrieval_source = response.get("retrieval_source", "hybrid")

            except Exception as e:
                answer = f"⚠️ Lỗi: {e}"
                sources = []
                retrieval_source = "error"

        st.markdown(answer)

        if sources:
            st.divider()
            st.caption(f"📚 Retrieval source: **{retrieval_source}** | {len(sources)} chunks sử dụng")
            with st.expander("Xem nguồn tham khảo"):
                for i, src in enumerate(sources, 1):
                    meta = src.get("metadata", {})
                    st.markdown(f"**[{i}]** `{meta.get('source', '?')}` — score: `{src.get('score', 0):.4f}`")
                    st.text(src.get("content", "")[:300])
                    st.divider()

    # =========================================================================
    # TAB 3: ANALYSIS
    # =========================================================================

    with tab_analysis:
        st.subheader("📈 Phân tích sâu — So sánh kỹ thuật")

        if st.session_state.last_comparison:
            techniques = st.session_state.last_comparison

            # ----- OVERLAP MATRIX -----
            st.markdown("#### 🔄 Ma trận Overlap (số chunks trùng nhau)")
            overlap = compute_overlap_matrix(techniques)
            import pandas as pd
            overlap_df = pd.DataFrame(overlap)
            st.dataframe(overlap_df, use_container_width=True)

            st.caption("""
            **Cách đọc:** Giá trị ô (A, B) = số chunks xuất hiện ở CẢ kỹ thuật A và B.
            Đường chéo = tổng chunks của kỹ thuật đó.
            Overlap cao → 2 kỹ thuật tìm ra nội dung giống nhau.
            Overlap thấp → kỹ thuật tìm ra nội dung khác biệt → hybrid sẽ hiệu quả hơn.
            """)

            st.divider()

            # ----- SCORE DISTRIBUTION -----
            st.markdown("#### 📊 Phân bố điểm (Score Distribution)")

            score_data = []
            for name, data in techniques.items():
                for r in data["results"]:
                    score_data.append({
                        "Technique": name,
                        "Score": r["score"],
                        "Source": r.get("metadata", {}).get("source", "?"),
                    })

            if score_data:
                score_df = pd.DataFrame(score_data)
                st.bar_chart(score_df, x="Technique", y="Score", color="Technique", horizontal=False)

            st.divider()

            # ----- TIMING COMPARISON -----
            st.markdown("#### ⏱️ Thời gian xử lý")
            timing_data = {name: data["time_ms"] for name, data in techniques.items()}
            timing_df = pd.DataFrame([
                {"Kỹ thuật": name, "Thời gian (ms)": ms}
                for name, ms in timing_data.items()
            ])
            st.bar_chart(timing_df, x="Kỹ thuật", y="Thời gian (ms)")

            st.divider()

            # ----- UNIQUE CHUNKS ANALYSIS -----
            st.markdown("#### 🔶 Chunks độc nhất (chỉ có ở 1 kỹ thuật)")

            all_sets = {name: get_content_set(data["results"]) for name, data in techniques.items()}
            all_union = set()
            for s in all_sets.values():
                all_union |= s

            for name, content_set in all_sets.items():
                other_union = set()
                for other_name, other_set in all_sets.items():
                    if other_name != name:
                        other_union |= other_set
                unique = content_set - other_union
                if unique:
                    st.markdown(f"**{name}:** {len(unique)} chunks độc nhất")
                    for chunk_preview in list(unique)[:3]:
                        st.text(f"  • {chunk_preview}...")

            st.divider()

            # ----- KEY INSIGHTS -----
            st.markdown("#### 💡 Nhận xét tự động")

            # Insight 1: Which technique found most?
            best_count = max(techniques.items(), key=lambda x: x[1]["count"])
            st.success(f"**Nhiều kết quả nhất:** {best_count[0]} ({best_count[1]['count']} chunks)")

            # Insight 2: Which is fastest?
            active = {k: v for k, v in techniques.items() if v["count"] > 0}
            if active:
                fastest = min(active.items(), key=lambda x: x[1]["time_ms"])
                st.info(f"**Nhanh nhất:** {fastest[0]} ({fastest[1]['time_ms']}ms)")

            # Insight 3: Hybrid benefit
            semantic_set = all_sets.get("🔵 Semantic", set())
            bm25_set = all_sets.get("🟢 BM25", set())
            hybrid_set = all_sets.get("🟡 Hybrid+RRF", set())

            if semantic_set and bm25_set:
                overlap_count = len(semantic_set & bm25_set)
                total_unique = len(semantic_set | bm25_set)
                if total_unique > 0:
                    diversity = 1 - (overlap_count / total_unique)
                    st.markdown(f"""
                    **Độ đa dạng Semantic vs BM25:** `{diversity:.0%}`
                    - Overlap: {overlap_count} chunks giống nhau
                    - Tổng unique: {total_unique} chunks khác biệt
                    - {'✅ Hybrid mang lại nhiều giá trị gia tăng!' if diversity > 0.3 else '⚠️ Hai kỹ thuật cho kết quả khá giống nhau.'}
                    """)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer if 'answer' in dir() else "Xem tab So sánh kỹ thuật",
    })
