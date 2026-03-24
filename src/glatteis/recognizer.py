from typing import List
from .configs import Configs, Library


def init_nlp(configs: Configs):
    if configs.library == Library.SPACY:
        return SpacyNLP(configs.model)
    elif configs.library == Library.STANZA:
        return StanzaNLP(configs.model)
    elif configs.library == Library.OLLAMA:
        raise ValueError("TODO: OLLAMA")
        # return Ollama()
    else:
        raise ValueError("TODO: More")


# class Ollama:
#     def __init__(self):
#         from ollama import chat

#     def __call__(self, text: str) -> None:
#         from ollama import ChatResponse
#         response: ChatResponse = chat(
#             model="gemma3",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": "Why is the sky blue?",
#                 },
#             ],
#         )
#         print(response["message"]["content"])
#         # or access fields directly from the response object
#         print(response.message.content)
#         pass


class StanzaNLP:
    def __init__(self, stanza_language_model) -> None:
        import stanza

        self.nlp = stanza.Pipeline(
            stanza_language_model, processors="tokenize, ner", use_gpu=False
        )

    def __call__(self, text: str) -> list:
        candidates: List[str] = []
        doc = self.nlp(text)
        for token in doc.entities:  # pyright: ignore
            if token.type in ("GPE", "LOC"):
                candidates.append(token.text)
        return candidates


class SpacyNLP:
    def __init__(self, spacy_language_model) -> None:
        import spacy

        self.nlp = spacy.load(name=spacy_language_model)

    def __call__(self, text: str) -> list:
        doc = self.nlp(text)
        candidates: List[str] = []

        for entity in doc.ents:
            if entity.root.ent_type_ in (
                "GPE",
                "NORP",
                "LOC",
                "LC",
            ):
                candidates.append(entity.root.text)

        return candidates
