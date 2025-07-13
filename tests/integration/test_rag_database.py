from langchain_community.embeddings import FakeEmbeddings
import pytest

try:
    import chromadb  # noqa: F401
except Exception:  # pragma: no cover - skip if chromadb fails to import
    pytest.skip("chromadb not available", allow_module_level=True)
from src.rag import RAGDatabase


def test_rag_add_and_query(tmp_path):
    fake = FakeEmbeddings(size=8)
    db = RAGDatabase(persist_directory=tmp_path, embeddings=fake)
    texts = ["Paris is the capital of France.", "Berlin is the capital of Germany."]
    db.add_texts(texts)
    results = db.query("capital of Germany", k=1)
    assert len(results) == 1
    assert "Germany" in results[0].page_content


def test_sql_query(tmp_path):
    from langchain_community.embeddings import FakeEmbeddings

    db = RAGDatabase(
        persist_directory=tmp_path / "vec",
        sql_db_path=tmp_path / "meta.db",
        embeddings=FakeEmbeddings(size=8),
    )
    db.add_report("Law A states B", {"title": "Law A"})
    rows = db.query_sql("SELECT COUNT(*) FROM documents")
    assert rows[0][0] == 1
