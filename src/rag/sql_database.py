"""Simple SQLite-based metadata store for RAG documents."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable, Any


class SQLDatabase:
    """Store and query document metadata using SQLite."""

    def __init__(self, path: str | Path = "rag_metadata.db") -> None:
        self.path = Path(path)
        self.conn = sqlite3.connect(self.path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, metadata TEXT)"
        )
        self.conn.commit()

    def add_documents(
        self, texts: Iterable[str], metadatas: Iterable[dict] | None = None
    ) -> None:
        metadatas = metadatas or [{} for _ in texts]
        for text, meta in zip(texts, metadatas):
            self.conn.execute(
                "INSERT INTO documents (text, metadata) VALUES (?, ?)",
                (text, json.dumps(meta, ensure_ascii=False)),
            )
        self.conn.commit()

    def query(self, sql: str) -> list[tuple[Any, ...]]:
        cur = self.conn.execute(sql)
        return cur.fetchall()
