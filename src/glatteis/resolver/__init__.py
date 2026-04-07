from typing import Union

from geopandas import GeoDataFrame

from .ollama import OllamaResolver


class Resolver:
    def __init__(
        self,
        language: str,
        library: Union[str, None],
        model: Union[str, None],
    ) -> None:
        if model is None:
            raise NotImplementedError(
                "No default model for resolution yet, please specify one"
            )
        self.resolver = OllamaResolver(model)

    def __call__(self, text: str, candidates: GeoDataFrame):
        # print(f"{candidates=}")
        result = self.resolver(text, candidates)
        # print(f"{result=}")
        dummy = GeoDataFrame()
        return dummy
