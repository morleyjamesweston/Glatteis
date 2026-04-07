from typing import Union

import geopandas as gpd

from .geodata import GeoData
from .recognizer import Recognizer
from .resolver import Resolver
from .utils import standardize_name


class GeoParser:
    def __init__(
        self,
        language: str,
        recognition_library: Union[str, None] = None,
        recognition_model: Union[str, None] = None,
        resolution_library: Union[str, None] = None,
        resolution_model: Union[str, None] = None,
    ) -> None:
        self.geodata = GeoData()

        self.recognizer = Recognizer(
            language=language, library=recognition_library, model=recognition_model
        )
        self.resolver = Resolver(
            language=language, library=resolution_library, model=resolution_model
        )

    # Passthrough for add_gazetteer
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
        self.geodata.add_gazetteer(
            gdf,
            gazetteer_name,
            index_col,
            names_col,
            admin_rank,
            population_column,
            is_contextual,
        )

    def parse(self, text: str) -> gpd.GeoDataFrame | None:
        if not self.geodata.gazetteers:
            raise Exception("No gazetteers loaded")

        candidates = self.recognizer(text)
        candidates = [standardize_name(c, self.geodata.stopwords) for c in candidates]
        candidates = self.geodata.get_candidates(candidates)
        if candidates is None:
            return None
        else:
            candidates = self.resolver(text, candidates)
            return candidates
