"""Simple RAG database implementation using ChromaDB."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

from .sql_database import SQLDatabase


class RAGDatabase:
    """Vector store wrapper for Retrieval-Augmented Generation."""

    def __init__(
        self,
        persist_directory: str | Path = "rag_db",
        embedding_model: str = "all-MiniLM-L6-v2",
        embeddings: HuggingFaceEmbeddings | None = None,
        sql_db_path: str | Path = "rag_metadata.db",
    ) -> None:
        """Create a new RAG database.

        Parameters
        ----------
        persist_directory : str | Path
            Location to store the Chroma database.
        embedding_model : str
            Name of the HuggingFace embedding model to use if ``embeddings`` is not provided.
        embeddings : HuggingFaceEmbeddings | None
            Optional pre-built embeddings instance for testing or custom setups.
        """

        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.embeddings = embeddings or HuggingFaceEmbeddings(
            model_name=embedding_model
        )
        self.db = Chroma(
            persist_directory=str(self.persist_directory),
            embedding_function=self.embeddings,
        )
        self.sql_db = SQLDatabase(sql_db_path)
        self.splitter = RecursiveCharacterTextSplitter()

    def add_texts(
        self, texts: Iterable[str], metadatas: Iterable[dict] | None = None
    ) -> None:
        """Add texts to the vector store."""
        docs = self.splitter.create_documents(list(texts), metadatas=metadatas)
        self.db.add_documents(docs)
        self.sql_db.add_documents(
            [d.page_content for d in docs],
            [d.metadata for d in docs],
        )

    def add_report(self, report: str, metadata: dict | None = None) -> None:
        """Convenience wrapper to store a generated report."""
        self.add_texts([report], [metadata] if metadata else None)

    def query_sql(self, sql: str):
        """Execute an arbitrary SQL query against stored metadata."""
        return self.sql_db.query(sql)

    def query(self, query_text: str, k: int = 3) -> List:
        """Return top ``k`` relevant documents for ``query_text``."""
        return self.db.similarity_search(query_text, k=k)
