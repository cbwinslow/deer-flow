"""spaCy-powered legal document processing utilities."""

from __future__ import annotations

from typing import List, Dict

import spacy


class LegalNLPProcessor:
    """Extract information from legal documents using spaCy."""

    def __init__(self, model: str = "en_core_web_sm") -> None:
        self.nlp = spacy.load(model)

    def extract_entities(self, text: str) -> List[Dict[str, str]]:
        """Return named entities found in ``text``."""
        doc = self.nlp(text)
        return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

    def chunk_text(self, text: str, max_chars: int = 1000) -> List[str]:
        """Split text into roughly ``max_chars`` chunks respecting sentences."""
        doc = self.nlp(text)
        chunks: List[str] = []
        current = ""
        for sent in doc.sents:
            if len(current) + len(sent.text) > max_chars and current:
                chunks.append(current.strip())
                current = sent.text
            else:
                current += " " + sent.text
        if current.strip():
            chunks.append(current.strip())
        return chunks
