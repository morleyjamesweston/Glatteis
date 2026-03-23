from itertools import permutations
from typing import Union
import flashtext
import geopandas as gpd
import pandas as pd
import re

class GeoData:
    def __init__(self) -> None:
        self.gazetteers = {}
        self.slim_gazetteer = gpd.GeoDataFrame()
        self.keywords = flashtext.KeywordProcessor()
        self.stopwords = list()
        # self.add_stopwords(GEO_STOPWORD_PRESETS)
    def _add_keywords(self, keywords: list) -> None:
        for keyword in keywords:
            self.keywords.add_keyword(keyword)
