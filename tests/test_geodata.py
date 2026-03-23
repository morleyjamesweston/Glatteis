import pytest
import geopandas as gpd
import pandas as pd

from glatteis.geodata import GeoData


def test_init():
    assert GeoData()

def test_add_gaz():
    geodata = GeoData()

    ne_countries = gpd.read_file("./tests/test_data/ne_10m_admin_0_countries.zip")

    # Must be geodataframe
    with pytest.raises(ValueError):
        geodata.add_gazetteer(
            gdf=pd.DataFrame(ne_countries), # pyright: ignore
            gazetteer_name="natural_earth_countries",
            index_col="ADM0_A3",
            names_col="NAME_DE",
            population_column="POP_EST",
            admin_rank=3,
            is_contextual=False,
        )

    # Columns aren't in dataframe
    with pytest.raises(ValueError):
        geodata.add_gazetteer(
            gdf=ne_countries,
            gazetteer_name="natural_earth_countries",
            index_col="NON_EXTANT_COLUMN",
            names_col="NAME_DE",
            population_column="POP_EST",
            admin_rank=3,
            is_contextual=False,
        )

    with pytest.raises(ValueError):
        geodata.add_gazetteer(
            gdf=ne_countries,
            gazetteer_name="natural_earth_countries",
            index_col="ADM0_A3",
            names_col="NON_EXTANT_COLUMN",
            population_column="POP_EST",
            admin_rank=3,
            is_contextual=False,
        )

    with pytest.raises(ValueError):
        geodata.add_gazetteer(
            gdf=ne_countries,
            gazetteer_name="natural_earth_countries",
            index_col="ADM0_A3",
            names_col="NAME_DE",
            population_column="NON_EXTANT_COLUMN",
            admin_rank=3,
            is_contextual=False,
        )

    with pytest.raises(ValueError):
        geodata.add_gazetteer(
            gdf=ne_countries,
            gazetteer_name="natural_earth_countries",
            index_col="ADM0_A3",
            names_col="NAME_DE",
            population_column="POP_EST",
            admin_rank="NON_EXTANT_COLUMN",
            is_contextual=False,
        )

    # Must be int or string
    with pytest.raises(TypeError):
        geodata.add_gazetteer(
            gdf=ne_countries,
            gazetteer_name="natural_earth_countries",
            index_col="ADM0_A3",
            names_col="NAME_DE",
            population_column="POP_EST",
            admin_rank=1.5, # pyright: ignore
            is_contextual=False,
        )

    geodata.add_gazetteer(
        gdf=ne_countries,
        gazetteer_name="natural_earth_countries",
        index_col="ADM0_A3",
        names_col="NAME_DE",
        population_column="POP_EST",
        admin_rank=0,
        is_contextual=True,
    )

    # Tests both admin rank and missing pop column
    ne_countries['ADMIN_RANK'] = 4
    geodata.add_gazetteer(
        gdf=ne_countries,
        gazetteer_name="natural_earth_countries_2",
        index_col="ADM0_A3",
        names_col="NAME_DE",
        admin_rank="ADMIN_RANK",
        is_contextual=True,
    )

    assert(geodata)

    assert(geodata._candidate_exists("DUMMY_PLACE_NAME") == 0)

    # tests __repr__
    assert(print(geodata) is None)
