import pytest
from glatteis import GeoParser, Configs
from glatteis.configs import Library, Language



def test_configs():
    assert GeoParser(language_code="de")

    conf = Configs(language=Language.DE, library=Library.SPACY, model="de_core_news_lg")
    with pytest.raises(ValueError):
        GeoParser(language_code="fr", configs=conf)

    assert GeoParser(language_code="de", configs=conf)

    with pytest.raises(ValueError):
        GeoParser(language_code="NON_EXISTANT_LANGUAGE")

    conf = Configs(language=Language.DE, library=Library.OLLAMA, model="de")
    with pytest.raises(ValueError):
        GeoParser(language_code="de", configs=conf)


    conf = Configs(language=Language.DE, library="NON_EXISTANT_LIB", model="de_core_news_lg") #pyright: ignore
    with pytest.raises(ValueError):
        GeoParser(language_code="de", configs=conf)
