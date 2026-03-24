import pytest
import geopandas as gpd

from glatteis import GeoParser, Configs
from glatteis.configs import Library, Language


def test_de_defaults():
    geoparser = GeoParser(language_code="de")
    ne_countries = gpd.read_file("./tests/test_data/ne_10m_admin_0_countries.zip")


    geoparser.add_gazetteer(
        gdf=ne_countries,
        gazetteer_name="natural_earth_countries",
        index_col="ADM0_A3",
        names_col="NAME_DE",
        population_column="POP_EST",
        admin_rank=0,
        is_contextual=True,
    )
    text = """
    Inhalt
    4000 Kilometer Flugdistanz Paris und Bern in Reichweite iranischer Raketen – theoretisch
    Der Iran hat zwei Raketen auf einen US-Stützpunkt im Indischen Ozean gefeuert. Die Raketen flogen so weit wie noch nie.
    Teilen
    Darum geht es: Der Iran hat am Wochenende zwei Raketen auf den US‑britischen Stützpunkt Diego Garcia im Indischen Ozean abgefeuert. Dieser liegt rund 4000 Kilometer vom Iran entfernt. Beide Geschosse verfehlten zwar ihr Ziel, dennoch handelt es sich um den bislang weitesten Raketenangriff der islamischen Republik. Das würde bedeuten, dass auch europäische Städte wie Paris, London oder Bern theoretisch in Reichweite solcher Systeme liegen könnten.
    Irans Raketenentwicklung: Das iranische Raketenprogramm entstand als Reaktion auf irakische Raketen im Iran‑Irak‑Krieg und wurde seither unter den Revolutionsgarden massiv ausgebaut. Anfangs reichten die Systeme nur rund 300 Kilometer weit. Später wurden sie zum Kern der iranischen Abschreckung. Moderne Modelle können Gefechtsköpfe von bis zu zwei Tonnen tragen. Offiziell lag ihre Reichweite bislang bei maximal 2000 Kilometern.
    Verschiedene Raketen mit Berglandschaft im Hintergrund.
    Legende: Iranische Langstreckenraketen und Raketenfahrzeuge an einer Rüstungsmesse in Teheran. (24.2.2023) Keystone / ABEDIN TAHERKENARE
    Das Ziel: Der Stützpunkt Diego Garcia liegt im Indischen Ozean und wird gemeinsam von Grossbritannien und den USA betrieben. Er ist für schwere strategische Bomber ausgelegt. Der Hafen der Basis kann grosse Flugzeugträgergruppen und Versorgungsschiffe aufnehmen, die sich im Krisenfall rasch in den Persischen Golf verlegen lassen. Die Basis befindet sich rund 4000 Kilometer südöstlich der iranischen Küste. Laut dem Critical Threats Project ist unklar, welches Raketensystem der Iran eingesetzt hat. Möglich sei eine Weiterentwicklung bekannter Modelle oder eine bisher unbekannte Waffe.
    Luftbild einer tropischen Insel mit Lagune.
    Legende: Der US-Stützpunkt Diego Garcia befindet sich im Nordwesten der gleichnamigen Insel im indischen Ozean. Keystone / U.S. Navy
    Europa in Reichweite: Während Israel und die USA nach eigenen Angaben mehrere Raketensilos und Abschussrampen im Westen des Irans zerstört haben, feuern die Streitkräfte immer noch aus dem Kernland auf Ziele in der Region. Eine Reichweite von rund 4000 Kilometern würde auch europäische Städte wie Berlin, Rom, Warschau oder Bern in den potenziellen Zielkorridor rücken. Die genauen militärischen Fähigkeiten bleiben jedoch unklar.
    Sie haben jetzt die Kapazität, tief nach Europa vorzudringen.
    Angriff bleibt unwahrscheinlich: Israels Ministerpräsident Benjamin Netanjahu forderte, dass sich weitere Länder dem Krieg gegen den Iran anschliessen. «Sie haben jetzt die Kapazität, tief nach Europa vorzudringen», sagte Netanjahu nach dem iranischen Angriff auf Diego Garcia. Der Iran habe bereits europäische Länder wie Zypern angegriffen. Die politische Führung des Irans hat die Angriffe jedoch entschieden zurückgewiesen. Beobachtern zufolge gelten iranische Angriffe auf Ziele in Europa als äusserst unwahrscheinlich, solange die Staaten nicht aktiv am Krieg beteiligt sind. Der Iran verfolgt vielmehr eine Militärdoktrin der äquivalenten Vergeltung nach dem Motto «Auge um Auge, Zahn um Zahn».
    """

    result = geoparser.parse(text)

    assert result is not None
    if result is not None:
        names = result['original_names'].to_list()
        assert "Iran" in names

    text = ""
    result = geoparser.parse(text)
    assert result is None

def test_empty():
    geoparser = GeoParser(language_code="de")
    text = "Berlin"
    with pytest.raises(Exception):
        geoparser.parse(text)


def test_de_stanza():
    conf = Configs(language=Language.DE, library=Library.STANZA, model="de")
    geoparser = GeoParser(language_code="de", configs=conf)

    ne_countries = gpd.read_file("./tests/test_data/ne_10m_admin_0_countries.zip")



    geoparser.add_gazetteer(
        gdf=ne_countries,
        gazetteer_name="natural_earth_countries",
        index_col="ADM0_A3",
        names_col="NAME_DE",
        population_column="POP_EST",
        admin_rank=0,
        is_contextual=True,
    )
    text = """
    Inhalt
    4000 Kilometer Flugdistanz Paris und Bern in Reichweite iranischer Raketen – theoretisch
    Der Iran hat zwei Raketen auf einen US-Stützpunkt im Indischen Ozean gefeuert. Die Raketen flogen so weit wie noch nie.
    Teilen
    Darum geht es: Der Iran hat am Wochenende zwei Raketen auf den US‑britischen Stützpunkt Diego Garcia im Indischen Ozean abgefeuert. Dieser liegt rund 4000 Kilometer vom Iran entfernt. Beide Geschosse verfehlten zwar ihr Ziel, dennoch handelt es sich um den bislang weitesten Raketenangriff der islamischen Republik. Das würde bedeuten, dass auch europäische Städte wie Paris, London oder Bern theoretisch in Reichweite solcher Systeme liegen könnten.
    Irans Raketenentwicklung: Das iranische Raketenprogramm entstand als Reaktion auf irakische Raketen im Iran‑Irak‑Krieg und wurde seither unter den Revolutionsgarden massiv ausgebaut. Anfangs reichten die Systeme nur rund 300 Kilometer weit. Später wurden sie zum Kern der iranischen Abschreckung. Moderne Modelle können Gefechtsköpfe von bis zu zwei Tonnen tragen. Offiziell lag ihre Reichweite bislang bei maximal 2000 Kilometern.
    Verschiedene Raketen mit Berglandschaft im Hintergrund.
    Legende: Iranische Langstreckenraketen und Raketenfahrzeuge an einer Rüstungsmesse in Teheran. (24.2.2023) Keystone / ABEDIN TAHERKENARE
    Das Ziel: Der Stützpunkt Diego Garcia liegt im Indischen Ozean und wird gemeinsam von Grossbritannien und den USA betrieben. Er ist für schwere strategische Bomber ausgelegt. Der Hafen der Basis kann grosse Flugzeugträgergruppen und Versorgungsschiffe aufnehmen, die sich im Krisenfall rasch in den Persischen Golf verlegen lassen. Die Basis befindet sich rund 4000 Kilometer südöstlich der iranischen Küste. Laut dem Critical Threats Project ist unklar, welches Raketensystem der Iran eingesetzt hat. Möglich sei eine Weiterentwicklung bekannter Modelle oder eine bisher unbekannte Waffe.
    Luftbild einer tropischen Insel mit Lagune.
    Legende: Der US-Stützpunkt Diego Garcia befindet sich im Nordwesten der gleichnamigen Insel im indischen Ozean. Keystone / U.S. Navy
    Europa in Reichweite: Während Israel und die USA nach eigenen Angaben mehrere Raketensilos und Abschussrampen im Westen des Irans zerstört haben, feuern die Streitkräfte immer noch aus dem Kernland auf Ziele in der Region. Eine Reichweite von rund 4000 Kilometern würde auch europäische Städte wie Berlin, Rom, Warschau oder Bern in den potenziellen Zielkorridor rücken. Die genauen militärischen Fähigkeiten bleiben jedoch unklar.
    Sie haben jetzt die Kapazität, tief nach Europa vorzudringen.
    Angriff bleibt unwahrscheinlich: Israels Ministerpräsident Benjamin Netanjahu forderte, dass sich weitere Länder dem Krieg gegen den Iran anschliessen. «Sie haben jetzt die Kapazität, tief nach Europa vorzudringen», sagte Netanjahu nach dem iranischen Angriff auf Diego Garcia. Der Iran habe bereits europäische Länder wie Zypern angegriffen. Die politische Führung des Irans hat die Angriffe jedoch entschieden zurückgewiesen. Beobachtern zufolge gelten iranische Angriffe auf Ziele in Europa als äusserst unwahrscheinlich, solange die Staaten nicht aktiv am Krieg beteiligt sind. Der Iran verfolgt vielmehr eine Militärdoktrin der äquivalenten Vergeltung nach dem Motto «Auge um Auge, Zahn um Zahn».
    """

    result = geoparser.parse(text)

    assert result is not None
    if result is not None:
        names = result['original_names'].to_list()
        assert "Iran" in names

    text = ""
    result = geoparser.parse(text)
    assert result is None
