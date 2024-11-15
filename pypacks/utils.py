from typing import Any
import json

import os
PYPACKS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/pypacks"


def recusively_remove_nones_from_dict(obj: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(obj, dict):
        return obj
    return {key: (recusively_remove_nones_from_dict(val) if isinstance(val, dict) else val) for key, val in obj.items() if val is not None}


def to_snbt(obj: dict[str, Any]) -> str:
    return json.dumps(recusively_remove_nones_from_dict(obj)).replace("\"'", "'").replace("'\"", "'")


def to_component_string(obj: dict[str, Any]) -> str:
    return ", ".join([f"{key}={to_snbt(val)}" for key, val in obj.items() if val is not None])


def chunk_list(lst: list[Any], size: int) -> list[list[Any]]:
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def get_png_dimensions(file_path: str) -> tuple[int, int]:
    """Returns width, height of the image"""
    with open(file_path, 'rb') as f:
        f.seek(16)  # Width and height start at byte 16
        width = int.from_bytes(f.read(4), 'big')
        height = int.from_bytes(f.read(4), 'big')
    assert width == height, "Image must be square"
    assert width == 1 or width % 2 == 0, "Image width must be divisible by 16"
    assert height == 1 or height % 2 == 0, "Image height must be divisible by 16"
    assert 1 <= width <= 512, "Image width must be between 1 and 512"
    assert 1 <= height <= 512, "Image height must be between 1 and 512"
    return width, height
