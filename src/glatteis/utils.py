import re
from typing import Set


def standardize_name(name: str, geographical_stopwords: Set[str]) -> str:
    name = name.casefold()
    name = name.upper()
    for n in geographical_stopwords:
        name = name.removeprefix(n)
        name = name.strip()
    name = re.sub(r"(\(.*\))", "", name)
    name = re.sub(r"\s+", " ", name)
    name = name.strip()
    return name
