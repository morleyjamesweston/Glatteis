from typing import List

import spacy


class SpacyNLP:
    def __init__(self, model) -> None:

        self.nlp = spacy.load(name=model)

    def __call__(self, text: str) -> List[str]:
        doc = self.nlp(text)
        candidates = []

        for entity in doc.ents:
            if entity.root.ent_type_ in (
                "GPE",
                "NORP",
                "LOC",
                "LC",
            ):
                candidates.append(entity.root.text)

        return candidates
