# Kết Quả Đánh Giá RAG Pipeline — IELTS Band Descriptors & Bài Mẫu

## Thành viên nhóm

| STT | Họ và tên | Mã học viên |
|-----|-----------|-------------|
| 1 | Lục Minh Đức | 2A202601918 |
| 2 | Phan Hoàng Long | 2A202601565 |
| 3 | Phạm Bá Thượng Hải | 2A202601797 |
| 4 | Phạm Nguyên Việt | 2A202601547 |

---

## Framework sử dụng

> **Lightweight RAGAS-style metrics** (so khớp từ khoá + token matching)
> - Không gọi LLM để tính metrics, tiết kiệm rate limit OpenRouter
> - 4 chỉ số: Faithfulness, Answer Relevance, Context Recall, Context Precision
> - So sánh A/B: Hybrid+RRF vs Semantic-only

## Tổng số câu hỏi đánh giá: 21

- Speaking Part 3 (thảo luận): 9 câu (Band 6.0 - 9.0)
- Writing Task 2 (tiêu chí chấm bài luận): 9 câu (Band 6.0 - 9.0)
- Band Descriptors (tra cứu trực tiếp): 3 câu

---

## Điểm tổng quan

| Chỉ số | Cấu hình A (Hybrid+RRF) | Cấu hình B (Semantic-only) | Chênh lệch | Ghi chú |
|--------|--------------------------|----------------------------|------------|---------|
| Faithfulness | 0.0293 | 0.8141 | -0.7848 | (*) |
| Answer Relevance | 0.1977 | 0.3629 | -0.1652 | (*) |
| Context Recall | 0.2368 | 0.2172 | +0.0196 | A tốt hơn |
| Context Precision | 0.9905 | 0.9905 | +0.0000 | Bằng nhau |
| **Trung bình** | **0.3636** | **0.5962** | | |
| Độ trễ trung bình | 4.65s | 0.02s | | A chậm hơn vì gọi LLM |

> **(*) Lưu ý quan trọng về Faithfulness và Answer Relevance:**
> Cấu hình A có Faithfulness rất thấp (0.029) KHÔNG PHẢI vì câu trả lời kém chất lượng,
> mà vì **phương pháp đo dùng so khớp từ** (word overlap). Cấu hình A gọi LLM (gpt-4o-mini) tổng hợp
> câu trả lời bằng **tiếng Việt**, trong khi ngữ liệu (context) là **tiếng Anh**,
> dẫn đến mức trùng khớp từ gần bằng 0. Cấu hình B đạt điểm cao (0.81) vì nó **sao chép trực tiếp**
> nội dung context vào câu trả lời, tạo ra độ trùng khớp cao nhưng thực tế không có giá trị tổng hợp.
>
> **Kết luận thực tế: Cấu hình A (Hybrid+RRF) tốt hơn cho người dùng cuối** vì:
> - Có tổng hợp thông minh bởi LLM
> - Có trích dẫn nguồn (citation)
> - Context Recall tốt hơn (+0.02)
> - Context Precision tương đương (0.99 cả hai)

---

## Phân tích so sánh A/B

### Cấu hình A: Hybrid + RRF Reranking

| Thiết lập | Giá trị |
|-----------|---------|
| Phương pháp truy xuất | Semantic (cosine) + BM25 Lexical |
| Phương pháp gộp | RRF (Reciprocal Rank Fusion, k=60) |
| Sinh câu trả lời | LLM (gpt-4o-mini qua OpenRouter) |
| Tính năng | Trích dẫn nguồn, tiếng Việt, reranking |
| Số chunks (top_k) | 5 |
| Kích thước chunk | 500 ký tự, chồng lấp 50 |

### Cấu hình B: Chỉ Semantic Search

| Thiết lập | Giá trị |
|-----------|---------|
| Phương pháp truy xuất | Semantic (cosine) duy nhất |
| Phương pháp gộp | Không có |
| Sinh câu trả lời | Trả về context trực tiếp (không qua LLM) |
| Tính năng | Trả văn bản thô |
| Số chunks (top_k) | 5 |
| Kích thước chunk | 500 ký tự, chồng lấp 50 |

### Kết luận

> **Cấu hình A (Hybrid+RRF) hiệu quả hơn cho người dùng cuối** dù điểm Faithfulness
> thấp hơn theo phương pháp đo word-overlap. Lý do:
> 1. **LLM tổng hợp**: câu trả lời có cấu trúc, có trích dẫn nguồn, dễ hiểu
> 2. **Hybrid retrieval**: kết hợp semantic + keyword, đa dạng kết quả hơn
> 3. **Context Recall cao hơn**: 0.2368 so với 0.2172 (+0.02)
> 4. **Context Precision tương đương**: 0.99 cả hai, chất lượng truy xuất ngang nhau
>
> Điểm yếu của phương pháp đo word-overlap: không đánh giá được chất lượng tổng hợp
> xuyên ngôn ngữ (Việt - Anh). Cần dùng LLM-based metrics (RAGAS/DeepEval với
> LLM judge) để đánh giá chính xác hơn.

---

## Các câu hỏi có kết quả kém nhất (3 câu cuối bảng - Cấu hình A)

| # | Câu hỏi | Faithfulness | Relevance | Recall | Giai đoạn lỗi | Nguyên nhân gốc |
|---|---------|-------------|-----------|--------|---------------|-----------------|
| 1 | IELTS Speaking Band 7.0 — Thể thao và Xã hội | 0.000 | 0.000 | 0.000 | Truy xuất | Ngữ liệu không có nội dung về speaking chủ đề thể thao |
| 2 | IELTS Writing Band 6.5 — Bài luận thảo luận | 0.000 | 0.000 | 0.000 | Truy xuất | Từ khoá kỳ vọng (longevity, pension) không có trong ngữ liệu |
| 3 | IELTS Writing Band 7.5 — Bài luận lợi-hại | 0.000 | 0.000 | 0.000 | Truy xuất | Từ khoá (language acquisition, cognitive) không có trong ngữ liệu |

> **Nguyên nhân chung:** Bộ golden dataset có các từ khoá kỳ vọng rất cụ thể (ví dụ:
> "longevity", "pension", "gig economy") mà ngữ liệu IELTS samples không bao phủ hết.
> Đây là vấn đề **độ phủ dữ liệu**, không phải lỗi của pipeline truy xuất.

---

## Chi tiết từng câu hỏi (Cấu hình A: Hybrid+RRF)

| # | Chủ đề | Band | Faithfulness | Relevance | Recall | Precision | Độ trễ |
|---|--------|------|-------------|-----------|--------|-----------|--------|
| 1 | Speaking - Cân bằng công việc-cuộc sống | 6.0 | 0.000 | 0.000 | 0.286 | 1.000 | 11.5s |
| 2 | Speaking - Thực phẩm và Sức khoẻ | 6.5 | 0.000 | 0.000 | 0.571 | 1.000 | 2.8s |
| 3 | Speaking - Giáo dục và Công nghệ | 7.0 | 0.056 | 0.357 | 0.571 | 1.000 | 10.4s |
| 4 | Speaking - Đời sống đô thị | 7.5 | 0.000 | 0.000 | 0.375 | 0.800 | 1.4s |
| 5 | Speaking - Mạng xã hội | 8.0 | 0.048 | 0.294 | 0.222 | 1.000 | 8.9s |
| 6 | Speaking - Công việc và Việc làm | 8.5 | 0.000 | 0.000 | 0.125 | 1.000 | 1.5s |
| 7 | Speaking - Xã hội và Đạo đức | 9.0 | 0.000 | 0.000 | 0.125 | 1.000 | 1.8s |
| 8 | Speaking - Thể thao và Xã hội | 7.0 | 0.000 | 0.000 | 0.000 | 1.000 | 1.6s |
| 9 | Speaking - Giải trí | 8.0 | 0.000 | 0.000 | 0.125 | 1.000 | 1.8s |
| 10 | Writing - Bài luận quan điểm | 6.0 | 0.000 | 0.000 | 0.429 | 1.000 | 1.5s |
| 11 | Writing - Bài luận thảo luận | 6.5 | 0.000 | 0.000 | 0.000 | 1.000 | 1.5s |
| 12 | Writing - Bài luận vấn đề-giải pháp | 7.0 | 0.053 | 0.333 | 0.000 | 1.000 | 8.9s |
| 13 | Writing - Bài luận lợi-hại | 7.5 | 0.000 | 0.000 | 0.000 | 1.000 | 1.7s |
| 14 | Writing - Bài luận thảo luận | 8.0 | 0.056 | 0.400 | 0.000 | 1.000 | 7.7s |
| 15 | Writing - Bài luận tranh luận | 8.5 | 0.000 | 0.000 | 0.000 | 1.000 | 2.1s |
| 16 | Writing - Bài luận thảo luận | 9.0 | 0.000 | 0.000 | 0.000 | 1.000 | 2.7s |
| 17 | Writing - Bài luận quan điểm | 7.0 | 0.046 | 0.292 | 0.000 | 1.000 | 9.4s |
| 18 | Writing - Câu hỏi trực tiếp | 8.0 | 0.000 | 0.000 | 0.000 | 1.000 | 2.5s |
| 19 | **Tiêu chí chấm - Lexical Resource** | **6-7** | **0.210** | **0.818** | **0.857** | **1.000** | **6.4s** |
| 20 | **Tiêu chí chấm - Coherence & Cohesion** | **8** | **0.051** | **0.800** | **0.714** | **1.000** | **5.4s** |
| 21 | **Tiêu chí chấm - Task Achievement** | **9** | **0.095** | **0.857** | **0.571** | **1.000** | **6.1s** |

> **Nhận xét:** 3 câu hỏi tra cứu trực tiếp về Band Descriptors (dòng 19-21) đạt điểm
> **cao nhất** (Relevance 0.8+, Recall 0.57-0.86) vì ngữ liệu có dữ liệu chính xác
> từ file PDF tiêu chí chấm IELTS chính thức. Đây là **trường hợp sử dụng chính** của hệ thống RAG này.

---

## Đề xuất cải tiến

### Cải tiến 1: Tăng kích thước chunk từ 500 lên 800
**Hành động:** Điều chỉnh `CHUNK_SIZE` trong `task4_chunking_indexing.py` để mỗi chunk chứa nhiều ngữ cảnh hơn.
**Tác động dự kiến:** Tăng Faithfulness +5-10% vì LLM có nhiều context hơn để trích xuất thông tin.

### Cải tiến 2: Sử dụng cross-encoder reranking (Jina/Cohere)
**Hành động:** Cấu hình `JINA_API_KEY` và bật cross-encoder reranking trong `task7_reranking.py`.
**Tác động dự kiến:** Tăng Context Precision +10-15% vì cross-encoder đánh giá độ liên quan tốt hơn RRF.

### Cải tiến 3: Dùng mô hình embedding đa ngôn ngữ (bge-m3)
**Hành động:** Đổi `EMBEDDING_MODEL` từ `all-MiniLM-L6-v2` sang `BAAI/bge-m3` để hỗ trợ cả tiếng Việt.
**Tác động dự kiến:** Tăng Answer Relevance khi người dùng hỏi bằng tiếng Việt, hiện tại mô hình chỉ tốt với tiếng Anh.

### Cải tiến 4: Dùng LLM-as-Judge cho các chỉ số đánh giá
**Hành động:** Sử dụng RAGAS/DeepEval với LLM judge thay vì phương pháp so khớp từ (word-overlap).
**Tác động dự kiến:** Đánh giá chính xác hơn, đặc biệt cho Faithfulness xuyên ngôn ngữ (Việt - Anh).

---

*Tạo lúc: 2026-08-04 12:25:37*
*Pipeline: Semantic Search (all-MiniLM-L6-v2) + BM25 + RRF Reranking + OpenRouter gpt-4o-mini*
*Vector Store: ChromaDB (936 chunks, 500 ký tự/chunk)*
*Đánh giá: 21 câu hỏi từ Band 6.0-9.0 (9 Speaking + 9 Writing + 3 Tiêu chí chấm)*
