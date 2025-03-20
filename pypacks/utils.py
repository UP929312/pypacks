import os
import json
from pathlib import Path
from typing import Any

PYPACKS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/pypacks"
IMAGES_PATH = Path(PYPACKS_ROOT)/"assets"/"images"


def recursively_remove_nones_from_data(obj: Any) -> Any:
    if isinstance(obj, list):
        return [recursively_remove_nones_from_data(x) for x in obj if x is not None]
    if isinstance(obj, dict):
        return {key: recursively_remove_nones_from_data(value) for key, value in obj.items() if value is not None}
    return obj


def chunk_list(lst: list[Any], size: int) -> list[list[Any]]:
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def format_written_book(string: str) -> str:
    # Extract the JSON part (inside `written_book_content=...`)
    prefix = 'written_book_content='
    start = string.index(prefix) + len(prefix)
    json_str = string[start:].rstrip(']')  # Remove trailing `]` if needed

    # Parse JSON and pretty-print it
    parsed_json = json.loads(json_str)
    return string[:start]+json.dumps(parsed_json, indent=4).replace("\n", " \\\n")+"]"
