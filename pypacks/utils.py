import json
import os
from pathlib import Path
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from pypacks.additions.text import Text

PYPACKS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/pypacks"
IMAGES_PATH = Path(PYPACKS_ROOT)/"assets"/"images"


def recursively_remove_nones_from_data(obj: Any) -> Any:
    if isinstance(obj, list):
        return [recursively_remove_nones_from_data(x) for x in obj if x is not None]
    if isinstance(obj, dict):
        return {key: recursively_remove_nones_from_data(value) for key, value in obj.items() if value is not None}
    return obj


def to_component_string(obj: dict[str, Any]) -> str:
    # TODO: Move the recursively remove nones from data to the obj itself, then remove the if val is not None
    # TODO: Also remove this whole "surrounding quotes" thing, it's not needed when we upgrade to 1.21.5
    surrounding_quotes = {key: "'" if key in ["custom_name", "bundle_contents"] else "" for key in obj.keys()}
    return ", ".join([f'{key}={surrounding_quotes[key]}{json.dumps(recursively_remove_nones_from_data(val))}{surrounding_quotes[key]}' for key, val in obj.items() if val is not None])


def remove_colour_codes(text: "str | Text") -> list[dict[str, str | bool]]:
    """Removes colour codes from a string"""
    from pypacks.additions.text import Text
    if isinstance(text, Text):
        return text.to_dict()
    return [{"text": text}]


def chunk_list(lst: list[Any], size: int) -> list[list[Any]]:
    return [lst[i:i + size] for i in range(0, len(lst), size)]
