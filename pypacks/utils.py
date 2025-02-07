import json
import os
from pathlib import Path
from typing import Any

from pypacks.additions.constants import COLOUR_CODE_MAPPINGS

PYPACKS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/pypacks"
IMAGES_PATH = Path(PYPACKS_ROOT)/"assets"/"images"


def recursively_remove_nones_from_data(obj: Any) -> Any:
    if isinstance(obj, list):
        return [recursively_remove_nones_from_data(x) for x in obj if x is not None]
    if isinstance(obj, dict):
        return {key: recursively_remove_nones_from_data(value) for key, value in obj.items() if value is not None}
    return obj


def to_component_string(obj: dict[str, Any]) -> str:
    return ", ".join([f"{key}={json.dumps(recursively_remove_nones_from_data(val))}" for key, val in obj.items() if val is not None])


def colour_codes_to_json_format(text: str, auto_unitalicise: bool = False, make_white: bool = True) -> str:
    """Converts a string like '&6Hello &cworld' to a JSON string like '[{"text":"Hello ","color":"gold"},{"text":"world","color":"red"}]'
    DOES NOT WORK FOR FORMATTING (YET)"""
    if not text:
        return '[]'
    if "&" not in text:
        # return f"\"{text}\""
        return json.dumps([{"text": text, "color": "white", "italic": False} if make_white else {"text": text, "italic": False}])
    # Split on colour codes, but keep the original colour codes
    split_text = [x for x in text.split("&") if x]
    # Split on the first character of each colour code
    colour_code_and_text = [(x[0], x[1:]) if f"&{x[0]}" in COLOUR_CODE_MAPPINGS else ("&f", x) for x in split_text]
    # Convert the colour codes to JSON format
    json_data = [{"text": x[1], "color": COLOUR_CODE_MAPPINGS.get("&" + x[0], "white")} for x in colour_code_and_text]
    # To auto untalicise, add {"italics": False} to each dictionary
    italics_removed = [x | ({"italic": False} if auto_unitalicise else {}) for x in json_data]
    return json.dumps(italics_removed)


def remove_colour_codes(text: str) -> str:
    """Removes Minecraft colour codes from a string"""
    string = text[:]
    for code in COLOUR_CODE_MAPPINGS:
        string = string.replace(code, "")
    return string


def chunk_list(lst: list[Any], size: int) -> list[list[Any]]:
    return [lst[i:i + size] for i in range(0, len(lst), size)]
