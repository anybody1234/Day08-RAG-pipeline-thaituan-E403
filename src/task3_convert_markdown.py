"""
Task 3 — Convert toàn bộ file trong data/landing/ thành Markdown.

Sử dụng MarkItDown của Microsoft cho PDF:
    https://github.com/microsoft/markitdown

Cài đặt:
    pip install "markitdown[pdf]"

Hướng dẫn:
    1. Scan toàn bộ file trong data/landing/ (PDF, JSON)
    2. Convert sang Markdown
    3. Lưu vào data/standardized/ giữ nguyên cấu trúc thư mục
"""

import json
from pathlib import Path

LANDING_DIR = Path(__file__).parent.parent / "data" / "landing"
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "standardized"


def convert_legal_docs():
    """Convert PDF/DOCX files trong data/landing/legal/ sang markdown."""
    legal_dir = LANDING_DIR / "legal"
    output_dir = OUTPUT_DIR / "legal"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not legal_dir.exists():
        print("  ⚠ Thư mục data/landing/legal/ chưa tồn tại. Chạy Task 1 trước.")
        return

    # Thử dùng MarkItDown, nếu không có thì fallback sang đọc text trực tiếp
    try:
        from markitdown import MarkItDown
        md_converter = MarkItDown()
        use_markitdown = True
    except ImportError:
        print("  ⚠ MarkItDown chưa cài. Dùng fallback text extraction.")
        use_markitdown = False

    for filepath in sorted(legal_dir.iterdir()):
        if filepath.suffix.lower() in (".pdf", ".docx", ".doc"):
            print(f"  Converting: {filepath.name}")
            output_path = output_dir / f"{filepath.stem}.md"

            if use_markitdown:
                try:
                    result = md_converter.convert(str(filepath))
                    output_path.write_text(result.text_content, encoding="utf-8")
                except Exception as e:
                    print(f"    ⚠ MarkItDown failed ({e}), using fallback")
                    # Fallback: đọc PDF text đơn giản
                    _fallback_pdf_to_md(filepath, output_path)
            else:
                _fallback_pdf_to_md(filepath, output_path)

            print(f"    ✓ Saved: {output_path.name}")


def _fallback_pdf_to_md(filepath: Path, output_path: Path):
    """Fallback: extract text từ PDF bằng pdfminer hoặc đọc raw."""
    try:
        # Thử pdfminer
        from pdfminer.high_level import extract_text
        text = extract_text(str(filepath))
        output_path.write_text(text, encoding="utf-8")
    except ImportError:
        try:
            # Thử PyPDF2
            import PyPDF2
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = "\n".join(page.extract_text() or "" for page in reader.pages)
            output_path.write_text(text, encoding="utf-8")
        except ImportError:
            # Cuối cùng: tạo md file với thông tin cơ bản
            output_path.write_text(
                f"# {filepath.stem}\n\n"
                f"*Source: {filepath.name}*\n\n"
                f"[PDF file — cần markitdown[pdf] để convert]\n",
                encoding="utf-8",
            )


def convert_news_articles():
    """Convert JSON crawled articles trong data/landing/news/ sang markdown.

    Hỗ trợ cấu trúc thư mục mới từ team:
        news/speaking/*.json
        news/writing/*.json
    """
    news_dir = LANDING_DIR / "news"
    output_dir = OUTPUT_DIR / "news"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not news_dir.exists():
        print("  ⚠ Thư mục data/landing/news/ chưa tồn tại. Chạy Task 2 trước.")
        return

    # Dùng rglob để tìm JSON trong cả subdirectories (speaking/, writing/)
    json_files = sorted(news_dir.rglob("*.json"))

    if not json_files:
        print("  ⚠ Không tìm thấy file JSON nào.")
        return

    for filepath in json_files:
        # Giữ lại tên subfolder (speaking/writing) trong output
        relative = filepath.relative_to(news_dir)
        sub_output_dir = output_dir / relative.parent
        sub_output_dir.mkdir(parents=True, exist_ok=True)

        print(f"  Converting: {relative}")
        data = json.loads(filepath.read_text(encoding="utf-8"))
        output_path = sub_output_dir / f"{filepath.stem}.md"

        # Thêm metadata header — hỗ trợ cả field cũ (essay_type, question) và mới (task_type, prompt)
        title = data.get("title", "Unknown")
        header = f"# {title}\n\n"
        header += f"**Source:** {data.get('source_name', data.get('url', 'N/A'))}\n"
        header += f"**URL:** {data.get('url', 'N/A')}\n"
        header += f"**Crawled:** {data.get('date_crawled', 'N/A')}\n"

        # IELTS-specific metadata
        task_type = data.get("task_type") or data.get("essay_type")
        if task_type:
            header += f"**Task Type:** {task_type}\n"

        band_score = data.get("band_score")
        if band_score:
            header += f"**Band Score:** {band_score}\n"

        test_type = data.get("test_type")
        if test_type:
            header += f"**Test Type:** {test_type}\n"

        prompt = data.get("prompt") or data.get("question")
        if prompt:
            header += f"\n**Prompt/Question:**\n> {prompt}\n"

        header += "\n---\n\n"

        # Content body
        body = data.get("content_markdown", "")

        # Examiner comment (nếu có)
        examiner = data.get("examiner_comment")
        if examiner:
            body += f"\n\n---\n\n## Examiner's Comment\n\n{examiner}\n"

        content = header + body
        output_path.write_text(content, encoding="utf-8")
        print(f"    ✓ Saved: {output_path.name}")


def convert_all():
    """Convert toàn bộ files."""
    print("=" * 50)
    print("Task 3: Convert to Markdown")
    print("=" * 50)

    print("\n--- Legal Documents (Band Descriptors) ---")
    convert_legal_docs()

    print("\n--- News Articles (Sample Essays) ---")
    convert_news_articles()

    print(f"\n✓ Done! Output tại: {OUTPUT_DIR}")


if __name__ == "__main__":
    convert_all()
