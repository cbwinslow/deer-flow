from src.nlp import LegalNLPProcessor


def test_extract_entities():
    processor = LegalNLPProcessor()
    text = "The President of the United States signed the Act."
    ents = processor.extract_entities(text)
    assert len(ents) > 0
