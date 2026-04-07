from typing import Union

import pandas as pd
from geopandas import GeoDataFrame
from ollama import generate

DEFAULT_PROMPT = """
In the following text, there is the place named
"""


class OllamaResolver:
    def __init__(self, model: str, prompt: Union[str, None] = None):
        self.model = model
        self.prompt = prompt if prompt is not None else DEFAULT_PROMPT

    def _create_prompt(self, text: str, candidates: GeoDataFrame):
        original_name = candidates["original_names"].iloc[0]

        formatted_candidates = candidates.filter(
            [
                "original_index",
                "original_names",
                "admin_rank",
                "gazetteer_name",
                "population_column",
            ],
            axis=1,
        )

        formatted_candidates.rename(
            columns={
                "original_index": "index",
                "original_names": "name",
                "admin_rank": "admin_rank",
                "gazetteer_name": "gazetteer",
                "population_column": "population",
            },
            inplace=True,
        )

        formatted_candidates = formatted_candidates.to_json(
            orient="records", lines=True
        )

        prompt = f"""
In the following text, there is the place named {original_name}, but which {original_name}
it refers to is uncertain. The choices are:

{formatted_candidates}


More specific candidates are preferred, specifically those with a lower admin rank. Candidates with a higher population are also preferred. However, these heuristics should only be used if the text does not provide any other clues. If the text provides clues that contradict these heuristics, then those clues should be followed instead.

Please choose the most appropriate one, and return the index of the chosen place in the original candidates dataframe. Do not add any other text.
{text}
"""
        return prompt

    @staticmethod
    def _parse_response(response: str, text: str) -> GeoDataFrame:
        return GeoDataFrame()

    def _resolve_place_name(self, text: str, candidates: GeoDataFrame):
        pass

    def __call__(self, text: str, candidates: GeoDataFrame) -> GeoDataFrame:
        # Split candidates into different dataframes by standardized_names column
        candidate_frames = [
            GeoDataFrame(candidates[candidates["standardized_names"] == name])
            for name in candidates["standardized_names"].unique()
        ]

        out_frame = GeoDataFrame()
        for candidate_frame in candidate_frames:
            if len(candidate_frame) == 1:
                out_frame = pd.concat([out_frame, candidate_frame])
            else:
                response = generate(
                    model=self.model,
                    prompt=self._create_prompt(text, candidate_frame),
                    keep_alive=10.0,
                )
                index = response.response.strip()
                candidate_frame = candidate_frame[
                    candidate_frame["original_index"] == int(index)
                ]
                out_frame = pd.concat([out_frame, candidate_frame])

        print(out_frame)
        return GeoDataFrame()
