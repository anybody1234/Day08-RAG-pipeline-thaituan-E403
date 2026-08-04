"""
Task 8 — PageIndex Vectorless RAG.

Đăng ký tài khoản tại: https://pageindex.ai/
SDK & sample code: https://github.com/VectifyAI/PageIndex

PageIndex cho phép RAG mà không cần vector store — sử dụng
structural understanding của document thay vì embedding.

Cài đặt:
    pip install pageindex

Lưu ý:
    - Nếu không có PAGEINDEX_API_KEY → graceful fallback return []
    - API /retrieval đã deprecated nhưng vẫn hoạt động
    - Response có "retrieved_nodes" → parse "relevant_contents"
"""

import os
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"


def upload_documents():
    """
    Upload toàn bộ markdown documents lên PageIndex.
    """
    if not PAGEINDEX_API_KEY:
        print("  ⚠ PAGEINDEX_API_KEY chưa set. Bỏ qua upload.")
        return

    try:
        from pageindex.client import PageIndexClient

        client = PageIndexClient(api_key=PAGEINDEX_API_KEY)

        for md_file in sorted(STANDARDIZED_DIR.rglob("*.md")):
            print(f"  Uploading: {md_file.name}")
            try:
                # PageIndex nhận PDF — convert md → temporary text file
                resp = client.submit_document(str(md_file))
                doc_id = resp.get("doc_id") or resp.get("id")
                print(f"    ✓ Uploaded: {md_file.name} → {doc_id}")
            except Exception as e:
                print(f"    ⚠ Upload failed for {md_file.name}: {e}")

    except ImportError:
        print("  ⚠ pageindex package chưa cài. pip install pageindex")
    except Exception as e:
        print(f"  ⚠ PageIndex upload error: {e}")


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Vectorless retrieval sử dụng PageIndex.
    Dùng làm fallback khi hybrid search không có kết quả tốt.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {
            'content': str,
            'score': float,
            'metadata': dict,
            'source': 'pageindex'   # Đánh dấu nguồn retrieval
        }
    """
    if not PAGEINDEX_API_KEY:
        print("  ⚠ PAGEINDEX_API_KEY chưa set. Trả về danh sách rỗng.")
        return []

    try:
        from pageindex.client import PageIndexClient

        client = PageIndexClient(api_key=PAGEINDEX_API_KEY)

        # Lấy danh sách documents đã upload
        docs = client.list_documents()
        if not docs:
            print("  ⚠ Chưa upload documents lên PageIndex")
            return []

        results = []

        # Query mỗi document
        for doc_info in docs[:3]:  # Giới hạn 3 documents để tránh chậm
            doc_id = doc_info.get("doc_id") or doc_info.get("id")
            if not doc_id:
                continue

            try:
                # Submit query
                resp = client.submit_query(doc_id=doc_id, query=query)
                retrieval_id = resp.get("retrieval_id") or resp.get("id")

                if not retrieval_id:
                    continue

                # Poll cho đến khi status == "completed" (tối đa 30s)
                for _ in range(30):
                    retrieval = client.get_retrieval(retrieval_id)
                    status = retrieval.get("status", "")
                    if status == "completed":
                        break
                    time.sleep(1)

                # Parse results
                for node in retrieval.get("retrieved_nodes", [])[:2]:
                    for group in node.get("relevant_contents", []):
                        for item in group if isinstance(group, list) else [group]:
                            content = item.get("relevant_content", "")
                            if content:
                                results.append({
                                    "content": content,
                                    "score": round(1.0 / (len(results) + 1), 4),
                                    "metadata": {
                                        "section": item.get("section_title", ""),
                                        "doc_id": doc_id,
                                    },
                                    "source": "pageindex",
                                })

            except Exception as e:
                print(f"    ⚠ Query failed for doc {doc_id}: {e}")

        return results[:top_k]

    except ImportError:
        print("  ⚠ pageindex package chưa cài")
        return []
    except Exception as e:
        print(f"  ⚠ PageIndex search error: {e}")
        return []


if __name__ == "__main__":
    if not PAGEINDEX_API_KEY:
        print("⚠ Hãy set PAGEINDEX_API_KEY trong file .env")
        print("  Đăng ký tại: https://pageindex.ai/")
    else:
        print("Uploading documents...")
        upload_documents()

        print("\nTest query:")
        results = pageindex_search("IELTS band 8 lexical resource criteria", top_k=3)
        for r in results:
            print(f"[{r['score']:.3f}] {r['content'][:100]}...")
