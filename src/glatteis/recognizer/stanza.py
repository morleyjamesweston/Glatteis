from typing import List


class StanzaNLP:
    def __init__(self, model) -> None:
        import stanza

        self.nlp = stanza.Pipeline(model, processors="tokenize, ner", use_gpu=False)

    def __call__(self, text: str) -> List[str]:
        candidates = []
        doc = self.nlp(text)
        for token in doc.entities:  # pyright: ignore
            if token.type in ("GPE", "LOC"):
                candidates.append(token.text)
        return candidates
