from dataclasses import dataclass
from enum import StrEnum


class Language(StrEnum):
    DE = "de"
    FR = "fr"


class Library(StrEnum):
    SPACY = "spacy"
    STANZA = "stanza"
    OLLAMA = "ollama"


@dataclass
class Configs:
    language: Language
    library: Library
    model: str


DEFAULT_CONFIGS = {
    "de": Configs(language=Language.DE, library=Library.SPACY, model="de_core_news_lg"),
    "fr": Configs(language=Language.FR, library=Library.SPACY, model="fr_core_news_lg"),
}


def init_configs(language_code: str, configs: Configs | None):
    if configs:
        if language_code != str(configs.language):
            raise ValueError("Language code does not equal config language")
        return configs
    else:
        configs = DEFAULT_CONFIGS.get(language_code)
        if configs is None:
            raise ValueError()
        else:
            return configs
