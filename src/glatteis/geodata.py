from itertools import permutations
from typing import Dict, List, Union
import flashtext
import geopandas as gpd
import pandas as pd
import re
from typing import Iterable, Set


GEO_STOPWORD_PRESETS = [
    "CANTONE ",
    "CANTON ",
    "CANTONS ",
    "CANTONES ",
    "CANTONI ",
    "CANTONS ",
    "KANTON ",
    "DES ",
    "DI ",
    "DELLA ",
    "DELLI ",
    "DELL'",
    "DEL ",
    "DEI ",
    "DEGLI ",
    "DE ",
    "ST. ",
    "D'",
]

class GeoData:
    def __init__(self) -> None:
        self.gazetteers: Dict[str, gpd.GeoDataFrame] = {}
        self.slim_gazetteer = gpd.GeoDataFrame()
        self.keywords = flashtext.KeywordProcessor()
        self.stopwords: Set[str] = set()
        self.add_stopwords(GEO_STOPWORD_PRESETS)

    def _add_keywords(self, keywords: Iterable[str]) -> None:
        for keyword in keywords:
            self.keywords.add_keyword(keyword)

    def add_stopwords(self, stopwords: Iterable[str]) -> None:
        for word in stopwords:
            self.stopwords.add(word)

    def _candidate_exists(self, candidate: str) -> bool:
        cands = self.keywords.extract_keywords(candidate)
        return len(cands) > 0

    def _standardize_name(self, name: str, geographical_stopwords: Set[str]) -> str:
        name = name.casefold()
        name = name.upper()
        for n in geographical_stopwords:
            name = name.removeprefix(n)
            name = name.strip()
        name = re.sub(r"(\(.*\))", "", name)
        name = re.sub(r"\s+", " ", name)
        name = name.strip()
        return name

    def add_gazetteer(
        self,
        gdf: gpd.GeoDataFrame,
        gazetteer_name: str,
        index_col: str,
        names_col: str,
        admin_rank: Union[str, int],
        population_column: str | None = None,
        is_contextual: bool = False,
    ) -> None:
        if index_col not in gdf.columns:
            raise ValueError("Index column not in GeoDataFrame")
        if names_col not in gdf.columns:
            raise ValueError("Names column not in GeoDataFrame")
        if type(admin_rank) is str and admin_rank not in gdf.columns:
            raise ValueError("Admin rank column not in GeoDataFrame")
        if population_column and population_column not in gdf.columns:
            raise ValueError("Population column not in GeoDataFrame")

        simplified_gdf = gdf.copy(deep=True)

        # removes null name rows
        simplified_gdf= simplified_gdf[simplified_gdf[names_col].notnull()]
        if type(simplified_gdf) is not gpd.GeoDataFrame:
            raise ValueError('')

        simplified_gdf = simplified_gdf.to_crs("EPSG:4326")

        # sets administrative rank to int for whole gazetteer,
        # or sets administrative rank column name
        if isinstance(admin_rank, str):
            pass
        elif isinstance(admin_rank, int):
            simplified_gdf["gaz_admin_rank"] = admin_rank
            admin_rank = "gaz_admin_rank"
        else:
            raise TypeError("Admin rank must be str or int")

        # sets population column to int for whole gazetteer,
        # or sets population column name
        if population_column is None:
            simplified_gdf["gaz_population"] = 0
            population_column = "gaz_population"
        elif isinstance(population_column, str):
            pass

        # sets standardized name column
        simplified_gdf["standardized_names"] = [
            self._standardize_name(n, self.stopwords) for n in simplified_gdf[names_col]
        ]

        # # only gets needed columns for slim gazetteer
        simplified_gdf = simplified_gdf[
            [
                index_col,
                names_col,
                admin_rank,
                population_column,
                "standardized_names",
                "geometry",
            ]
        ]

        # This is to keep type checker happy
        simplified_gdf = gpd.GeoDataFrame(simplified_gdf)

        # Inplace to keep typing happy
        simplified_gdf.rename(
            columns={
                index_col: "original_index",
                names_col: "original_names",
                admin_rank: "admin_rank",
                population_column: "population_column",
            },
            inplace=True
        )

        simplified_gdf["gazetteer_name"] = gazetteer_name
        simplified_gdf["is_contextual"] = is_contextual

        self.gazetteers[gazetteer_name] = gdf

        self.slim_gazetteer = pd.concat(
            [self.slim_gazetteer, simplified_gdf], ignore_index=True
        )

        self._add_keywords(simplified_gdf["original_names"].tolist())
        self._add_keywords(simplified_gdf["standardized_names"].tolist())

    def __repr__(self) -> str:
        return f"GeoData( gazetteers: {len(self.gazetteers)}, locations: {len(self.keywords)})"
