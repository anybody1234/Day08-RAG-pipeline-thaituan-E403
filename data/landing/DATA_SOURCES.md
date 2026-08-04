# Nguồn Dữ Liệu — IELTS Writing Band Descriptors & Sample Essays

Chủ đề dữ liệu của nhóm: **Tra cứu tiêu chí chấm điểm IELTS Writing (Band Descriptors) và phân tích essay mẫu theo band**.
Tài liệu này ghi lại nguồn gốc từng file trong `data/landing/` để phục vụ Task 3+ (convert/chunking) và để nhóm có thể trích dẫn nguồn khi báo cáo.

Cấu trúc thư mục được giữ nguyên theo template gốc:
- `data/landing/legal/` → dùng cho **Band Descriptors** (văn bản tiêu chí chính thức, tương đương "văn bản chính sách/quy định" trong đề bài gốc).
- `data/landing/news/` → dùng cho **Sample essays theo band** (tương đương "bài viết/thông báo" trong đề bài gốc, ở đây là các bài luận mẫu).

---

## 1. Band Descriptors (`data/landing/legal/`)

| File | Nguồn | Ghi chú |
|---|---|---|
| `ielts-writing-band-descriptors-official-ielts.org-2023.pdf` | [ielts.org/cdn/Guides/ielts-writing-band-descriptors.pdf](https://ielts.org/cdn/Guides/ielts-writing-band-descriptors.pdf) | Tài liệu **chính thức**, đồng sở hữu bởi British Council, IDP IELTS, Cambridge Assessment English. Cập nhật 05/2023. Bao gồm đầy đủ Task 1 và Task 2, 4 tiêu chí (Task Achievement/Response, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy), band 1–9. |

### ⚠️ Lưu ý quan trọng về "band lẻ" (6.5, 7.5, 8.5...)

IELTS **chỉ công bố band descriptor ở các mốc nguyên (1–9)**. Không tồn tại một bảng tiêu chí riêng biệt cho band 6.5 hay 7.5. Band lẻ của **điểm Writing tổng** (overall) là kết quả **lấy trung bình cộng 4 tiêu chí rồi làm tròn lên đến 0.5 gần nhất** — ví dụ 6, 6, 7, 7 → trung bình 6.5.
→ Khi trả lời câu hỏi kiểu *"khác biệt giữa band 6.0 và 7.0 ở Lexical Resource"*, RAG có thể trích trực tiếp từ file band descriptor gốc. Khi trả lời câu hỏi liên quan band lẻ (6.5, 7.5, 8.5), nên diễn giải là **mức trung gian giữa hai band nguyên liền kề**, không trích dẫn như thể có mô tả riêng.

---

## 2. Sample Essays theo Band (`data/landing/news/`)

21 file JSON (`essay_band{X.X}_{NN}.json`), 3 bài / band, band 6.0 → 9.0 (gồm cả band lẻ). Schema mỗi file:

```json
{
  "url": "nguồn gốc thật",
  "title": "chủ đề Task 1/2",
  "date_crawled": "ngày thu thập",
  "band_score": "điểm band",
  "task_type": "Task 1 | Task 2",
  "test_type": "Academic | General Training",
  "source_name": "tên site/tác giả",
  "source_reputation": "xem phân loại bên dưới",
  "prompt": "đề bài gốc",
  "content_markdown": "toàn văn bài luận",
  "examiner_comment": "nhận xét (nếu có)"
}
```

### Phân loại độ tin cậy nguồn (`source_reputation`)

1. **`official`** — Bài thi thật của thí sinh, được giám khảo IELTS chính thức chấm điểm và viết nhận xét, công bố bởi ielts.org. Chỉ có 2 bài: `essay_band6.0_01.json` (Task 1, Band 6.0) và `essay_band7.5_01.json` (Task 2, Band 7.5) — trích từ tài liệu ["Sample Candidate Writing Responses and Examiner Comments"](https://ielts.org/cdn/computer-delivered-sample-tests-academic-writing/ielts-academic-writing-example-responses-to-parts-1-and-2-with-band-scores-and-examiner-comments.pdf). Đây là nguồn đáng tin cậy nhất trong bộ dữ liệu.
2. **`expert model answer`** — Bài mẫu do giáo viên/cựu giám khảo IELTS có tên tuổi tự viết làm chuẩn tham chiếu cho một band mục tiêu (vd. IELTS Liz — cựu giám khảo; Simone Braverman — tác giả bộ sách *High Scorer's Choice*). Không phải bài thi thật của thí sinh, band do chính tác giả tự gán.
3. **`established prep site sample`** — Bài mẫu/bài phân tích từ các trang luyện thi IELTS uy tín, có quy trình biên tập rõ ràng (IELTS Buddy, IELTS Blog, IELTS Podcast, IELTS Juice, IELTS Ladder...), band do site tự chấm/tự gán, **chưa được Cambridge/IDP/British Council xác minh độc lập**.

Band 8.5–9.0 hầu như không có bài thi thật công khai (IELTS không công bố script band cao để tránh học vẹt) nên các band này chủ yếu dùng nguồn loại 2. Band 6.0–8.0 chủ yếu dùng nguồn loại 3, xen giữa 2 bài loại 1 (official).

### Danh sách nguồn đã dùng

- ielts.org (official)
- ieltsbuddy.com
- ielts-blog.com
- ieltsliz.com
- ieltspodcast.com
- ieltsjuice.com
- ieltsladder.com
- ieltskaro.com

**Lưu ý khi trình bày:** khi RAG trả lời câu hỏi có trích dẫn essay mẫu, nên hiển thị kèm `source_reputation` để người dùng biết đây là band "chính thức" hay band "tự gán bởi site luyện thi" — tránh gây hiểu nhầm là điểm số được Cambridge xác nhận.
