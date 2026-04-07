from dataclasses import dataclass
from typing import Union

from .ollama import OllamaRecognizer
from .spacy import SpacyNLP
from .stanza import StanzaNLP


@dataclass
class Configs:
    library: str
    model: str


MULTILINGUAL_CONFIG = Configs(library="spacy", model="xx_ent_wiki_sm")

DEFAULT_CONFIGS = {
    "de": Configs(library="spacy", model="de_core_news_lg"),
    "fr": Configs(library="spacy", model="fr_core_news_lg"),
}


class Recognizer:
    def __init__(
        self,
        language: str,
        library: Union[str, None],
        model: Union[str, None],
    ):

        if library is None:
            library = DEFAULT_CONFIGS.get(language, MULTILINGUAL_CONFIG).library
        if model is None:
            model = DEFAULT_CONFIGS.get(language, MULTILINGUAL_CONFIG).model

        if library.lower() == "spacy":
            self.nlp = SpacyNLP(model)
        elif library.lower() == "stanza":
            self.nlp = StanzaNLP(model)
        elif library.lower() == "ollama":
            self.nlp = OllamaRecognizer(model)
        else:
            raise ValueError("TODO: More")

    def __call__(self, text):
        return self.nlp(text)
