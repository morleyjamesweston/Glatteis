from ..configs import Configs, Library
from .ollama import Ollama
from .spacy import SpacyNLP
from .stanza import StanzaNLP


def init_nlp(configs: Configs):
    print(Configs)
    if configs.library == Library.SPACY:
        return SpacyNLP(configs.model)
    elif configs.library == Library.STANZA:
        return StanzaNLP(configs.model)
    elif configs.library == Library.OLLAMA:
        return Ollama(configs.model)
    else:
        raise ValueError("TODO: More")
