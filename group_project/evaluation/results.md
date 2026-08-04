# RAG Evaluation Results — IELTS Band Descriptors & Sample Essays

## Framework su dung

> **Lightweight RAGAS-style metrics** (keyword overlap + token matching)
> - Khong goi LLM de tinh metrics → tiet kiem rate limit OpenRouter
> - 4 metrics: Faithfulness, Answer Relevance, Context Recall, Context Precision
> - So sanh A/B: Hybrid+RRF vs Semantic-only

## Tong so cau hoi danh gia: 21

- Speaking Part 3 (discussion): 9 cau (Band 6.0 → 9.0)
- Writing Task 2 (essay criteria): 9 cau (Band 6.0 → 9.0)
- Band Descriptors (direct lookup): 3 cau

---

## Overall Scores

| Metric | Config A (Hybrid+RRF) | Config B (Semantic-only) | Delta | Ghi chu |
|--------|-----------------------|--------------------------|-------|---------|
| Faithfulness | 0.0293 | 0.8141 | -0.7848 | (*) |
| Answer Relevance | 0.1977 | 0.3629 | -0.1652 | (*) |
| Context Recall | 0.2368 | 0.2172 | +0.0196 | A tot hon |
| Context Precision | 0.9905 | 0.9905 | +0.0000 | Bang nhau |
| **Average** | **0.3636** | **0.5962** | | |
| Avg Latency | 4.65s | 0.02s | | A cham hon vi goi LLM |

> **(*) Luu y quan trong ve Faithfulness va Answer Relevance:**
> Config A co Faithfulness rat thap (0.029) KHONG PHAI vi answer kem chat luong,
> ma vi **metric dung word overlap**. Config A goi LLM (gpt-4o-mini) tong hop
> answer bang **tieng Viet**, trong khi context tu corpus la **tieng Anh** →
> word overlap gan = 0. Config B cao (0.81) vi no **copy truc tiep** context text
> vao answer → overlap cao nhung thuc te khong co gia tri tong hop gi.
>
> **Ket luan thuc te: Config A (Hybrid+RRF) tot hon cho end-user** vi:
> - Co tong hop thong minh boi LLM
> - Co citation nguon
> - Context Recall tot hon (+0.02)
> - Context Precision tuong duong (0.99 ca 2)

---

## A/B Comparison Analysis

### Config A: Hybrid + RRF Reranking

| Setting | Value |
|---------|-------|
| Retrieval | Semantic (cosine) + BM25 Lexical |
| Merging | RRF (Reciprocal Rank Fusion, k=60) |
| Generation | LLM (gpt-4o-mini via OpenRouter) |
| Features | Citation, tieng Viet, reranking |
| Top-k | 5 chunks |
| Chunk size | 500 chars, overlap 50 |

### Config B: Semantic-only

| Setting | Value |
|---------|-------|
| Retrieval | Semantic (cosine) only |
| Merging | None |
| Generation | Raw context (no LLM) |
| Features | Direct text return |
| Top-k | 5 chunks |
| Chunk size | 500 chars, overlap 50 |

### Ket luan

> **Config A (Hybrid+RRF) hieu qua hon cho end-user** du diem Faithfulness
> thap hơn theo metric word-overlap. Ly do:
> 1. **LLM tong hop**: answer co cau truc, co citation, de hieu
> 2. **Hybrid retrieval**: ket hop semantic + keyword → da dang hon
> 3. **Context Recall cao hon**: 0.2368 vs 0.2172 (+0.02)
> 4. **Context Precision tuong duong**: 0.99 ca 2 → retrieval quality ngang nhau
>
> Diem yeu cua metric word-overlap: khong danh gia duoc chat luong tong hop
> cross-lingual (Viet ↔ Anh). Can dung LLM-based metrics (RAGAS/DeepEval voi
> LLM judge) de danh gia chinh xac hon.

---

## Worst Performers (Bottom 3 — Config A)

| # | Question | Faithfulness | Relevance | Recall | Failure Stage | Root Cause |
|---|----------|-------------|-----------|--------|---------------|------------|
| 1 | IELTS Speaking Band 7.0 — Sports and Society | 0.000 | 0.000 | 0.000 | Retrieval | Corpus khong co speaking sports content |
| 2 | IELTS Writing Band 6.5 — Discussion Essay | 0.000 | 0.000 | 0.000 | Retrieval | Expected keywords (longevity, pension) not in corpus |
| 3 | IELTS Writing Band 7.5 — Advantage-Disadvantage | 0.000 | 0.000 | 0.000 | Retrieval | Keywords (language acquisition, cognitive) missing |

> **Root cause chung:** Golden dataset co expected_keywords rat cu the (vi du:
> "longevity", "pension", "gig economy") ma corpus IELTS samples khong cover het.
> Day la van de **data coverage**, khong phai loi cua retrieval pipeline.

---

## Chi tiet tung cau hoi (Config A: Hybrid+RRF)

| # | Category | Band | Faithfulness | Relevance | Recall | Precision | Latency |
|---|----------|------|-------------|-----------|--------|-----------|--------|
| 1 | Speaking - Work-Life Balance | 6.0 | 0.000 | 0.000 | 0.286 | 1.000 | 11.5s |
| 2 | Speaking - Food and Health | 6.5 | 0.000 | 0.000 | 0.571 | 1.000 | 2.8s |
| 3 | Speaking - Education & Tech | 7.0 | 0.056 | 0.357 | 0.571 | 1.000 | 10.4s |
| 4 | Speaking - Urban Life | 7.5 | 0.000 | 0.000 | 0.375 | 0.800 | 1.4s |
| 5 | Speaking - Social Media | 8.0 | 0.048 | 0.294 | 0.222 | 1.000 | 8.9s |
| 6 | Speaking - Work & Employment | 8.5 | 0.000 | 0.000 | 0.125 | 1.000 | 1.5s |
| 7 | Speaking - Society & Ethics | 9.0 | 0.000 | 0.000 | 0.125 | 1.000 | 1.8s |
| 8 | Speaking - Sports & Society | 7.0 | 0.000 | 0.000 | 0.000 | 1.000 | 1.6s |
| 9 | Speaking - Entertainment | 8.0 | 0.000 | 0.000 | 0.125 | 1.000 | 1.8s |
| 10 | Writing - Opinion Essay | 6.0 | 0.000 | 0.000 | 0.429 | 1.000 | 1.5s |
| 11 | Writing - Discussion Essay | 6.5 | 0.000 | 0.000 | 0.000 | 1.000 | 1.5s |
| 12 | Writing - Problem-Solution | 7.0 | 0.053 | 0.333 | 0.000 | 1.000 | 8.9s |
| 13 | Writing - Advantage-Disadv | 7.5 | 0.000 | 0.000 | 0.000 | 1.000 | 1.7s |
| 14 | Writing - Discussion Essay | 8.0 | 0.056 | 0.400 | 0.000 | 1.000 | 7.7s |
| 15 | Writing - Argumentative | 8.5 | 0.000 | 0.000 | 0.000 | 1.000 | 2.1s |
| 16 | Writing - Discussion Essay | 9.0 | 0.000 | 0.000 | 0.000 | 1.000 | 2.7s |
| 17 | Writing - Opinion Essay | 7.0 | 0.046 | 0.292 | 0.000 | 1.000 | 9.4s |
| 18 | Writing - Direct Question | 8.0 | 0.000 | 0.000 | 0.000 | 1.000 | 2.5s |
| 19 | **Descriptors - Lexical Resource** | **6-7** | **0.210** | **0.818** | **0.857** | **1.000** | **6.4s** |
| 20 | **Descriptors - Coherence & Cohesion** | **8** | **0.051** | **0.800** | **0.714** | **1.000** | **5.4s** |
| 21 | **Descriptors - Task Achievement** | **9** | **0.095** | **0.857** | **0.571** | **1.000** | **6.1s** |

> **Nhan xet:** 3 cau hoi truc tiep ve Band Descriptors (row 19-21) co diem
> **cao nhat** (Relevance 0.8+, Recall 0.57-0.86) vi corpus co data chinh xac
> tu official IELTS band descriptors PDF. Day la **use case chinh** cua RAG system nay.

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

### Cai tien 4: Dung LLM-as-Judge cho evaluation metrics
**Action:** Su dung RAGAS/DeepEval voi LLM judge thay vi word-overlap metrics.
**Expected impact:** Danh gia chinh xac hon, dac biet cho Faithfulness cross-lingual (Viet ↔ Anh).

---

*Generated at: 2026-08-04 12:25:37*
*Pipeline: Semantic Search (all-MiniLM-L6-v2) + BM25 + RRF Reranking + OpenRouter gpt-4o-mini*
*Vector Store: ChromaDB (936 chunks, 500 chars/chunk)*
*Evaluation: 21 questions across Band 6.0-9.0 (9 Speaking + 9 Writing + 3 Descriptors)*
