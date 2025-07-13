# Legal NLP Features

DeerFlow now includes basic natural language processing tools powered by
[spaCy](https://spacy.io). The `LegalNLPProcessor` can extract entities from
legal documents and split long texts into chunks suitable for embedding and
storage in the RAG database.

Example usage:

```python
from src.nlp import LegalNLPProcessor
from src.rag import RAGDatabase

processor = LegalNLPProcessor()
db = RAGDatabase()

text = "The Parliament of Wonderland enacted the Freedom Act."
entities = processor.extract_entities(text)
chunks = processor.chunk_text(text)
db.add_texts(chunks, [{"entities": entities} for _ in chunks])
```

The associated metadata is stored in a SQLite database so you can run SQL queries
against processed documents.
