# Bài Tập Nhóm — IELTS RAG Chatbot & Evaluation Pipeline

## Thành viên nhóm

| STT | Họ và tên | Mã học viên | Nhiệm vụ | Trạng thái |
|-----|-----------|-------------|----------|------------|
| 1 | Lục Minh Đức | 2A202601918 | Team Leader & RAG Architect — Điều phối, ghép pipeline Task 9, kiểm tra tổng thể | Hoàn thành |
| 2 | Phan Hoàng Long | 2A202601565 | Data & Pipeline Specialist — Task 1-4 (thu thập dữ liệu, chunking, indexing) | Hoàn thành |
| 3 | Phạm Nguyên Việt | 2A202601547 | Frontend & Chatbot Dev — app.py (Streamlit UI), Task 10 (Generation) | Hoàn thành |
| 4 | Phạm Bá Thượng Hải | 2A202601797 | Evaluation & QA Engineer — golden_dataset.json, eval_pipeline.py, results.md | Hoàn thành |

---

## Chủ đề dữ liệu

**IELTS Band Descriptors & Sample Essays** — Tiêu chí chấm điểm IELTS Writing & Speaking (Band 6.0-9.0) kèm bài mẫu từ nguồn chính thức (ielts.org, British Council/IDP).

---

## Kiến Trúc Hệ Thống

```
                         +------------------+
                         |   Streamlit UI   |
                         |    (app.py)      |
                         +--------+---------+
                                  |
                                  v
                    +-------------+-------------+
                    |  generate_with_citation()  |
                    |       (Task 10)            |
                    |  - Reorder lost-in-middle  |
                    |  - Format context + cite   |
                    |  - LLM (OpenRouter)        |
                    +-------------+-------------+
                                  |
                                  v
                    +-------------+-------------+
                    |     retrieve() — Task 9    |
                    |    Retrieval Pipeline       |
                    +-------------+-------------+
                                  |
              +-------------------+-------------------+
              |                                       |
              v                                       v
   +----------+----------+                 +----------+----------+
   | Semantic Search      |                 | Lexical Search      |
   | (Task 5)             |                 | (Task 6 — BM25)     |
   | cosine similarity    |                 | keyword matching     |
   +----------+----------+                 +----------+----------+
              |                                       |
              v                                       v
   +----------+----------+              +-------------+----------+
   | ChromaDB (Task 4)   |              | BM25 Index (rank-bm25) |
   | 481 chunks           |              | 481 documents          |
   | all-MiniLM-L6-v2     |              +------------------------+
   +---------------------+
              |
              +-----> RRF Reranking (Task 7, k=60)
              |
              +-----> Score < 0.48? ---> PageIndex Fallback (Task 8)

   Dữ liệu:
   PDF (ielts.org) ---> MarkItDown ---> Markdown ---> Chunking ---> Embedding ---> ChromaDB
   JSON (essays)   --->            ---> Markdown ---> Chunking ---> Embedding ---> ChromaDB
```

---

## Sản phẩm nhóm

### 1. RAG Chatbot (app.py)

- **Giao diện:** Streamlit với 3 tabs (So sánh kỹ thuật | Câu trả lời LLM | Phân tích chi tiết)
- **So sánh 4 kỹ thuật retrieval:** Semantic, BM25, Hybrid+RRF, PageIndex — hiển thị cạnh nhau
- **Tính năng:** câu hỏi gợi ý, slider top_k, overlap matrix, score distribution, timing chart
- **Generation:** LLM (gpt-4o-mini qua OpenRouter) với citation và trích dẫn nguồn

### 2. Evaluation Pipeline (group_project/evaluation/)

- **Framework:** Lightweight RAGAS-style metrics (keyword overlap + token matching)
- **Golden dataset:** 18 bộ đề (9 Speaking + 9 Writing), tổng 21 câu hỏi đánh giá
- **4 metrics:** Faithfulness, Answer Relevance, Context Recall, Context Precision
- **A/B testing:** Config A (Hybrid+RRF) vs Config B (Semantic-only)
- **Báo cáo:** results.md đầy đủ bảng điểm, phân tích worst performers, 4 đề xuất cải tiến

---

## Hướng Dẫn Chạy

```bash
# Cài đặt dependencies
pip install -r requirements.txt

# Chạy chatbot
streamlit run app.py

# Chạy evaluation pipeline
python -m group_project.evaluation.eval_pipeline

# Chạy tests (35/35 passed)
pytest tests/test_individual.py -v
```

---

## Cấu hình

| Tham số | Giá trị |
|---------|---------|
| Embedding model | sentence-transformers/all-MiniLM-L6-v2 (384 dim) |
| Chunking | RecursiveCharacterTextSplitter (size=500, overlap=50) |
| Vector store | ChromaDB (481 chunks, cosine similarity) |
| Reranking | RRF (k=60) |
| Fallback threshold | Cosine score < 0.48 |
| LLM | gpt-4o-mini (OpenRouter) |
| Temperature | 0.3 |
