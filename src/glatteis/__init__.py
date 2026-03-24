from typing import Union
from .configs import Configs, init_configs
from .recognizer import init_nlp
from .geodata import GeoData
from .resolver import resolve
from .utils import standardize_name
import geopandas as gpd


class GeoParser:
    def __init__(self, language_code: str, configs: Configs | None = None) -> None:
        self.geodata = GeoData()
        self.configs = init_configs(language_code, configs)
        self.nlp = init_nlp(self.configs)

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

        candidates = self.nlp(text)
        candidates = [standardize_name(c, self.geodata.stopwords) for c in candidates]
        candidates = self.geodata.get_candidates(candidates)
        if candidates is None:
            return None
        else:
            candidates = resolve(candidates)
            return candidates
