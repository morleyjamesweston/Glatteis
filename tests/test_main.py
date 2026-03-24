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


def test_multi_gaz():
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


    cantons = gpd.read_file("./tests/test_data/swiss_govt_data/cantons.geojson")
    cantons = cantons.to_crs("EPSG:4326")

    geoparser.add_gazetteer(
        gdf=cantons,
        gazetteer_name="swissCantons",
        index_col="KANTONSNUM",
        names_col="NAME",
        population_column="EINWOHNERZ",
        admin_rank=3,
        is_contextual=True,
    )

    districts = gpd.read_file("./tests/test_data/swiss_govt_data/districts.geojson")
    districts = districts.to_crs("EPSG:4326")
    geoparser.add_gazetteer(
        gdf=districts,
        gazetteer_name="swissDistricts",
        index_col="BEZIRKSNUM",
        names_col="NAME",
        population_column="EINWOHNERZ",
        admin_rank=2,
        is_contextual=False,
    )


    munis = gpd.read_file("./tests/test_data/swiss_govt_data/municipalities.geojson")
    munis = munis.to_crs("EPSG:4326")
    geoparser.add_gazetteer(
        gdf=munis,
        gazetteer_name="swissMunicipalities",
        index_col="BFS_NUMMER",
        names_col="NAME",
        population_column="EINWOHNERZ",
        admin_rank=1,
        is_contextual=False,
    )

    populated_places = gpd.read_file("./tests/test_data/ne_110m_populated_places.zip")

    geoparser.add_gazetteer(
        gdf=populated_places,
        gazetteer_name="naturalEarthPopulatedPlaces",
        index_col="WOF_ID",
        names_col="NAME_DE",
        population_column="POP_MIN",
        admin_rank=4,
        is_contextual=False,
    )

    text = """
Terminus Olten schliesst Instagram statt Tanzfläche: Clubsterben in der Schweiz
Der Club Terminus in Olten schliesst. Es ist ein Symptom einer Branche in der Krise: Die Jungen bleiben fern.
Olten ist in Kanton Solothurn.
Laute Musik, tanzende Menschen und Drinks an der Bar: Noch wird im Terminus in Olten gefeiert. Bald macht der Club aber dicht. Trotz treuer Ü40-Fangemeinde findet an Ostern die letzte Party statt. Nach 31 Jahren ist Schluss.
DJ-Mischpult und tanzende Menschen in grün beleuchtetem Club.
Legende: Farbige Lichter, laute Musik vom DJ: Immer mehr Clubs wie das Terminus verschwinden. SRF
Das Problem: Die Jungen fehlen. Anstatt in der Disco verbringen viele junge Menschen ihre Wochenenden lieber daheim oder im Fitnesscenter. Wer im Club feiert, ist heute nicht mehr 20, sondern eher 50.
Schild des Terminus Clubs.
Legende: Nach gut 30 Jahren schliesst das Terminus in Olten nach Ostern seine Türen. SRF
Für viele Besucherinnen und Besucher ist das Terminus aber ein Teil ihres Lebens. «Das ist meine Stube. Seit 25 Jahren komme ich alle zwei bis drei Monate her – früher ein bisschen mehr», sagt Andrea Hochuli. Und Hanspeter Zeller ergänzt: «Ich habe hier sehr viel Zeit verbracht und viele gute Leute kennengelernt.» Heute zählt das Terminus noch einen Drittel der Besuchenden von früher.
Anlass als Fotokulisse
Das fehlende Publikum schlägt sich in der Anzahl Clubs und Discos nieder. Zwischen 2013 und 2023 verschwand schweizweit rund die Hälfte. Die Zahl ging von 466 auf 249 zurück, zeigt die Statistik des Bundes.
Mann sitzt auf schwarzem Sofa vor Musikposter.
Legende: Clubs in Kleinstädten wie Olten werden es künftig noch schwerer haben, glaubt Terminus-Betreiber Dušan Nedeljković. SRF
Für Terminus-Mitinhaber Dušan Nedeljković ist klar: «Das Konzept Club ist aus der Zeit gefallen.» Der Grund sei Social Media. Ein Club am immer gleichen Ort mit den oft gleichen Leuten sei keine Kulisse für eine Story, die man auf Instagram postet. Viel weniger Leute würden heute im Moment leben und den Augenblick geniessen.
Hand hält Smartphone mit Kamera-App bei Nachtparty.
Legende: Club-Killer Social Media? Für den Terminus-Mitbesitzer ist das Konzept der Disco aus der Zeit gefallen. SRF
«An einen Anlass geht man nicht mehr, um Spass zu haben. Es ist mittlerweile eine Kulisse, um den Anlass auf dem Handy zu dokumentieren.» In einer Kleinstadt wie Olten sieht der Clubbetreiber keine Zukunft für das Konzept.
Terminus-Aus sinnbildlich für Szene
Was Nedeljković in Olten merkt, bestätigt Alexander Bücheli für andere Orte. Die besten Zeiten der Clubs seien lange vorbei, so der Sprecher der Schweizer Bar- und Club-Kommission. Überspitzt meint er: «In den 90er-Jahren konnte man vier Boxen reinstellen und Techno an die Türen schreiben – und der Betrieb lief.»
Mann mit Brille auf Stadtstrasse.
Legende: Das Terminus sei keine Ausnahme, sagt Alexander Bücheli, sondern sinnbildlich für die Szene. SRF
Seit rund 15 Jahren seien die Herausforderungen grösser. Das Verschwinden des Terminus sei ein Verlust fürs Mittelland – aber sinnbildlich für den aktuellen Zustand der Schweizer Club-Kultur, so Bücheli.
Gründe gebe es mehrere. Einer: Die gesündere Lebensweise der jüngeren Generation. Sie trinkt weniger Alkohol – wenn sie denn in einen Club geht. «Das hat einen direkten Einfluss auf den Pro-Kopf-Umsatz. Man kann es auch nicht mit alkoholfreien Alternativen ersetzen.»
Person an der Bar, die Drinks vorbereitet.
Legende: Wer Alkohol trinkt, bestellt mehr Getränke. Bei kleinen Margen merken das die Clubs. SRF
Mit Alkohol würden die Gäste eher noch ein Getränk mehr bestellen. «Bei einer kleinen Marge macht es am Schluss die Masse aus, ob etwas finanzierbar ist.» Als Beispiel erwähnt Bücheli die Stadt Zürich. In den dortigen Clubs sei der Umsatz innerhalb von fünf Jahren um 40 Prozent gesunken.
Mit der Pandemie hätten viele Junge Alternativen zu den Clubs entdeckt: sich daheim treffen, in der Nacht ins Gym, wandern oder ein Brunch am Sonntag. Sport und Party geht schlecht zusammen.
«Tanzen ist ein urmenschliches Bedürfnis»
Trotzdem ist Club-Kenner Alexander Bücheli optimistisch für die Branche. «Das analoge Erlebnis eines Club-Besuchs in einer zunehmend digitalisierten Gesellschaft ist eine attraktive Alternative.»
DJ mischt Musik an einem Mischpult.
Legende: Club-Kenner und -betreiber sind sich einig: Ganz verschwinden werden Clubs mit Musik und tanzenden Menschen nicht. SRF
Weniger zuversichtlich ist Dušan Nedeljković vom Terminus. Die Schweizer Club-Szene stehe weiterhin vor schwierigen Zeiten. «Es wird sich auf die Grossstädte konzentrieren.» Doch auch er ist überzeugt: Ganz verschwinden werden Clubs nicht. «Tanzen ist ein urmenschliches Bedürfnis.»
"""

    result = geoparser.parse(text)
    print(result)
