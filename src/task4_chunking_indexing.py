"""
Task 4 — Chunking & Indexing vào Vector Store.

Hướng dẫn:
    1. Đọc toàn bộ markdown files từ data/standardized/
    2. Chunking strategy: RecursiveCharacterTextSplitter
    3. Embedding model: sentence-transformers/all-MiniLM-L6-v2 (384 dim)
    4. Vector store: ChromaDB (local persistent)

Lựa chọn:
    - Chunking: RecursiveCharacterTextSplitter vì an toàn, phổ biến, xử lý tốt
      cả heading lẫn paragraph. chunk_size=500 để mỗi chunk đủ ngữ cảnh cho
      1 band descriptor hoặc 1 đoạn essay. overlap=50 để giữ liên tục giữa chunks.
    - Embedding: all-MiniLM-L6-v2 (384 dim) vì nhẹ, nhanh, phù hợp corpus
      tiếng Anh (IELTS). Không cần bge-m3 vì dữ liệu chủ yếu English.
    - Vector store: ChromaDB vì đơn giản, local, không cần Docker.

Cài đặt:
    pip install langchain-text-splitters sentence-transformers chromadb
"""

from pathlib import Path

import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"
CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"

# =============================================================================
# CONFIGURATION — Giải thích lựa chọn
# =============================================================================

# Chunking: RecursiveCharacterTextSplitter
# chunk_size=500: Đủ chứa 1 band descriptor hoặc 1 đoạn essay + examiner comment.
# Không quá dài để gây noise trong retrieval, không quá ngắn để mất ngữ cảnh.
CHUNK_SIZE = 500
# chunk_overlap=50: ~10% overlap để giữ liên tục context giữa các chunks liền kề.
CHUNK_OVERLAP = 50
CHUNKING_METHOD = "recursive"  # "recursive" | "markdown_header" | "semantic"

# Embedding: all-MiniLM-L6-v2
# - 384 dimensions, ~22M params, rất nhanh
# - Phù hợp cho corpus tiếng Anh (IELTS content)
# - Nhẹ hơn nhiều so với bge-m3 (1024 dim), giảm RAM và thời gian index
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

# Vector store: ChromaDB
VECTOR_STORE = "chromadb"
COLLECTION_NAME = "ielts_band_descriptors"


# =============================================================================
# SINGLETON INSTANCES (lazy initialization)
# =============================================================================

_embedding_model = None
_chroma_collection = None


def get_embedding_model() -> SentenceTransformer:
    """Lấy embedding model (singleton để tránh load lại nhiều lần)."""
    global _embedding_model
    if _embedding_model is None:
        print(f"  Loading embedding model: {EMBEDDING_MODEL}...")
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    return _embedding_model


def get_collection():
    """Lấy ChromaDB collection (singleton)."""
    global _chroma_collection
    if _chroma_collection is None:
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        _chroma_collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},  # Cosine similarity
        )
    return _chroma_collection


# =============================================================================
# IMPLEMENTATION
# =============================================================================

def load_documents() -> list[dict]:
    """
    Đọc toàn bộ markdown files từ data/standardized/.

    Returns:
        List of {'content': str, 'metadata': {'source': str, 'type': str}}
    """
    documents = []
    if not STANDARDIZED_DIR.exists():
        print(f"  ⚠ Thư mục {STANDARDIZED_DIR} chưa tồn tại. Chạy Task 3 trước.")
        return documents

    for md_file in sorted(STANDARDIZED_DIR.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        if not content.strip():
            continue

        # Xác định loại tài liệu: legal (band descriptors) hoặc news (essays)
        rel_path = str(md_file.relative_to(STANDARDIZED_DIR))
        doc_type = "legal" if "legal" in rel_path else "news"

        # Sub-type: speaking, writing, hoặc band_descriptors
        if "speaking" in rel_path:
            sub_type = "speaking"
        elif "writing" in rel_path:
            sub_type = "writing"
        else:
            sub_type = "band_descriptors" if doc_type == "legal" else "essay"

        documents.append({
            "content": content,
            "metadata": {
                "source": md_file.name,
                "type": doc_type,
                "sub_type": sub_type,
            }
        })

    return documents


def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Chunk documents theo RecursiveCharacterTextSplitter.

    Returns:
        List of {'content': str, 'metadata': dict} — mỗi item là 1 chunk
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    chunks = []
    for doc in documents:
        splits = splitter.split_text(doc["content"])
        for i, chunk_text in enumerate(splits):
            chunks.append({
                "content": chunk_text,
                "metadata": {
                    **doc["metadata"],
                    "chunk_index": i,
                }
            })

    return chunks


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Embed toàn bộ chunks bằng all-MiniLM-L6-v2.

    Returns:
        Mỗi chunk dict được thêm key 'embedding': list[float]
    """
    model = get_embedding_model()
    texts = [c["content"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)

    for chunk, emb in zip(chunks, embeddings):
        chunk["embedding"] = emb.tolist()

    return chunks


def index_to_vectorstore(chunks: list[dict]):
    """
    Lưu chunks vào ChromaDB vector store.
    """
    collection = get_collection()

    # Tạo unique IDs cho mỗi chunk
    ids = [
        f"{c['metadata']['source']}_chunk_{c['metadata']['chunk_index']}"
        for c in chunks
    ]

    # Upsert vào ChromaDB
    # ChromaDB có batch size limit, chia thành batches nếu cần
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        batch_ids = ids[i:i + batch_size]

        collection.upsert(
            ids=batch_ids,
            documents=[c["content"] for c in batch],
            embeddings=[c["embedding"] for c in batch],
            metadatas=[c["metadata"] for c in batch],
        )

    print(f"  ✓ Indexed {len(chunks)} chunks vào ChromaDB collection '{COLLECTION_NAME}'")
    print(f"    Collection size: {collection.count()}")


def run_pipeline():
    """Chạy toàn bộ pipeline: load → chunk → embed → index."""
    print("=" * 50)
    print("Task 4: Chunking & Indexing")
    print(f"  Chunking: {CHUNKING_METHOD} (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    print(f"  Embedding: {EMBEDDING_MODEL} (dim={EMBEDDING_DIM})")
    print(f"  Vector Store: {VECTOR_STORE}")
    print("=" * 50)

    docs = load_documents()
    print(f"\n✓ Loaded {len(docs)} documents")

    if not docs:
        print("⚠ Không có documents! Chạy Task 1, 2, 3 trước.")
        return

    chunks = chunk_documents(docs)
    print(f"✓ Created {len(chunks)} chunks")

    chunks = embed_chunks(chunks)
    print(f"✓ Embedded {len(chunks)} chunks")

    index_to_vectorstore(chunks)
    print("✓ Indexed to vector store")


if __name__ == "__main__":
    run_pipeline()
