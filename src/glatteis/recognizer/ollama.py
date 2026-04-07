from typing import List, Union

from ollama import generate

DEFAULT_PROMPT = "please just repeat the word 'donkey', but misspelled slightly Do not add anything else."


class Ollama:
    def __init__(self, language_model: str, prompt: Union[str, None] = None):
        self.model = language_model
        self.prompt = prompt if prompt is not None else DEFAULT_PROMPT

    @staticmethod
    def _verify_response(response: str) -> List[str]:
        return []

    def __call__(self, text: str) -> List[str]:
        response = generate(
            model=self.model,
            prompt=self.prompt,
            keep_alive=10.0,
        )
        print(response.response)
        verified_response = self._verify_response(response.response)
        return verified_response
