import json
import os
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


def to_component_string(obj: dict[str, Any]) -> str:
    replacee, replacer = "\\\\", "\\"
    return ", ".join([f"{key}={json.dumps(recursively_remove_nones_from_data(val)).replace(replacee, replacer)}" for key, val in obj.items() if val is not None])


def make_white_and_remove_italics(text: str | dict[str, Any]) -> str | dict[str, Any]:
    if isinstance(text, str):
        return {"text": text, "color": "white", "italic": False}
    if text.get("italic") is False:
        return text
    return {**text, "color": "white", "italic": False}


def remove_italics(text: str | dict[str, Any]) -> str | dict[str, Any]:
    if isinstance(text, str):
        return text
    if text.get("italic") is False:
        return text
    return {**text, "italic": False}


def chunk_list(lst: list[Any], size: int) -> list[list[Any]]:
    return [lst[i:i + size] for i in range(0, len(lst), size)]
