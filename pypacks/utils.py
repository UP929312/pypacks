import json
import io
import os
import pathlib
from typing import Any

from .scripts.texture_mapping import ITEM_TO_SPECIAL_TEXTURE_MAPPING

PYPACKS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/pypacks"

colour_code_mappings = {
    "&0": "black",
    "&1": "dark_blue",
    "&2": "dark_green",
    "&3": "dark_aqua",
    "&4": "dark_red",
    "&5": "dark_purple",
    "&6": "gold",
    "&7": "gray",
    "&8": "dark_gray",
    "&9": "blue",
    "&a": "green",
    "&b": "aqua",
    "&c": "red",
    "&d": "light_purple",
    "&e": "yellow",
    "&f": "white",
    # "&l": "bold",
    # "&m": "strikethrough",
    # "&n": "underline",
    # "&o": "italic",
    # "&r": "reset",
    # obfuscated?
}


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


def colour_codes_to_json_format(text: str, auto_unitalicise: bool = False) -> str:
    """Converts a string like '&6Hello &cworld' to a JSON string like '[{"text":"Hello ","color":"gold"},{"text":"world","color":"red"}]'
    DOES NOT WORK FOR FORMATTING (YET)"""
    if not text:
        return '[]'
    if "&" not in text:
        return json.dumps([{"text": text, "color": "white", "italic": False}])
    # Split on colour codes, but keep the original colour codes
    split_text = [x for x in text.split("&") if x]
    # Split on the first character of each colour code
    colour_code_and_text = [(x[0], x[1:]) if f"&{x[0]}" in colour_code_mappings else ("&f", x) for x in split_text]
    # Convert the colour codes to JSON format
    json_data = [{"text": x[1], "color": colour_code_mappings.get("&" + x[0], "white")} for x in colour_code_and_text]
    # To auto untalicise, add {"italics": False} to each dictionary
    italics_removed = [x | ({"italic": False} if auto_unitalicise else {}) for x in json_data]
    return json.dumps(italics_removed)


def remove_colour_codes(text: str) -> str:
    """Removes Minecraft colour codes from a string"""
    string = text[:]
    for code in colour_code_mappings:
        string = string.replace(code, "")
    return string


def get_png_dimensions(file_path: str | None = None, image_bytes: bytes | None = None) -> tuple[int, int]:
    """Returns width, height of the image"""
    if file_path is not None:
        with open(file_path, 'rb') as file:
            file.seek(16)  # Width and height start at byte 16
            width = int.from_bytes(file.read(4), 'big')
            height = int.from_bytes(file.read(4), 'big')
    else:
        # TODO: The same, one with a context manager, one without...
        assert image_bytes is not None, "Must provide image bytes if not providing file_path"
        file_io = io.BytesIO(image_bytes)
        file_io.seek(16)  # Width and height start at byte 16
        width = int.from_bytes(file_io.read(4), 'big')
        height = int.from_bytes(file_io.read(4), 'big')
    assert width == height, "Image must be square"
    assert width == 1 or width % 2 == 0, "Image width must be divisible by 16"
    assert height == 1 or height % 2 == 0, "Image height must be divisible by 16"
    assert 1 <= width <= 512, "Image width must be between 1 and 512"
    assert 1 <= height <= 512, "Image height must be between 1 and 512"
    # rint(file_path, width, height)
    return width, height

def get_png_height(file_path: str | None = None, image_bytes: bytes | None = None) -> int:
    """Returns the height of the image"""
    if file_path is not None:
        return get_png_dimensions(file_path=file_path)[1]
    else:
        return get_png_dimensions(image_bytes=image_bytes)[1]


def inline_open(file_path: str, mode: str = "rb") -> Any:
    with open(file_path, mode) as file:
        return file.read()

def resolve_default_item_image(base_item: str) -> str:
    no_minecraft = base_item.removeprefix('minecraft:')
    path = pathlib.Path(f"{PYPACKS_ROOT}/assets/minecraft/item/{no_minecraft}.png")
    if no_minecraft in ITEM_TO_SPECIAL_TEXTURE_MAPPING:
        path = pathlib.Path(f"{PYPACKS_ROOT}/assets/minecraft/item/{ITEM_TO_SPECIAL_TEXTURE_MAPPING[no_minecraft]}.png")
    if no_minecraft in ["player_head", "zombie_head", "creeper_head", "skeleton_skull", "wither_skeleton_skull", "dragon_head"]:
        path = pathlib.Path(f"{PYPACKS_ROOT}/assets/images/reference_book_icons/player_head.png")
    if no_minecraft.endswith("spawn_egg"):
        path = pathlib.Path(f"{PYPACKS_ROOT}/assets/images/reference_book_icons/spawn_egg.png")
    if not path.exists():
        path = pathlib.Path(f"{PYPACKS_ROOT}/assets/images/reference_book_icons/unknown.png")  # Others, player head
    return str(path)


def pascal_to_snake(name: str) -> str:
    return ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')

# def get_ogg_duration(audio_bytes: bytes) -> float:
#     f = io.BytesIO(audio_bytes)
#     sample_rate = None
#     last_granule_pos = None
    
#     while True:
#         # Read OGG page header (27 bytes minimum)
#         header = file.read(27)
#         if len(header) < 27:
#             break

#         if header[:4] != b'OggS':
#             raise ValueError("Not a valid OGG file")

#         # Number of segments in the page
#         segment_count = header[26]
#         segment_table = file.read(segment_count)

#         # Calculate total size of this page's payload
#         segment_size = sum(segment_table)
#         payload_data = file.read(segment_size)

#         # Extract granule position (bytes 6-13 of the header)
#         granule_pos = int.from_bytes(header[6:14], 'little')
#         if last_granule_pos is None or granule_pos > last_granule_pos:
#             last_granule_pos = granule_pos

#         # Find the sample rate in the Vorbis Identification Header
#         if sample_rate is None:
#             index = payload_data.find(b'\x01vorbis')
#             if index != -1:
#                 # Vorbis header found
#                 sample_rate = int.from_bytes(payload_data[index + 11:index + 15], 'little')

#     # Debugging: Log values to validate correctness
#     rint(f"Last granule position: {last_granule_pos}")
#     rint(f"Sample rate: {sample_rate}")

#     if sample_rate and last_granule_pos:
#         duration = last_granule_pos / sample_rate
#         rint(f"Calculated duration: {duration} seconds")
#         return duration
#     else:
#         raise ValueError("Could not determine file duration")
