from typing import List, Union

from ollama import generate

DEFAULT_PROMPT = """
The following is an excerpt from a news article.
Please identify the place names in the text, and return them as a list of names, one per line. Do not add numbers, or anything besides names separated by a newline. Do not change the names of the places, and add no other text.
"""


class OllamaRecognizer:
    def __init__(self, model: str, prompt: Union[str, None] = None):
        self.model = model
        self.prompt = prompt if prompt is not None else DEFAULT_PROMPT

    def _create_prompt(self, text: str):
        prompt = "\n\n".join([self.prompt, text])
        return prompt

    @staticmethod
    def _parse_response(response: str, text: str) -> List[str]:
        locations = response.splitlines()
        locations = [loc.strip() for loc in locations]
        locations = [loc for loc in locations if loc in text]
        return locations

    def __call__(self, text: str) -> List[str]:
        response = generate(
            model=self.model,
            prompt=self._create_prompt(text),
            keep_alive=10.0,
        )
        verified_response = self._parse_response(response.response, text)
        return verified_response
