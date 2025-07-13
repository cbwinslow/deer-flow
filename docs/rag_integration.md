# RAG Integration

This project now includes a simple Retrieval-Augmented Generation (RAG) database built with **ChromaDB**. It allows you to store documents and retrieve relevant passages for prompts.

## Usage

```python
from src.rag import RAGDatabase

db = RAGDatabase()
# Add your texts or documents
texts = ["Paris is the capital of France."]
db.add_texts(texts)
# Query for similar documents
results = db.query("capital of France")
for doc in results:
    print(doc.page_content)
```

The RAG database persists by default in the `rag_db` directory. You can specify another path when creating the `RAGDatabase` instance.

## Saving Reports

Use `add_report` to store generated research reports along with optional metadata:

```python
report = "Summary of legal findings"
db.add_report(report, {"case": "freedom act"})
```

## SQL Queries

All added documents are also indexed in a SQLite database. You can run SQL queries:

```python
rows = db.query_sql("SELECT id, metadata FROM documents WHERE metadata LIKE '%freedom%'")
```
