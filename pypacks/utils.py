import json
import os
from pathlib import Path
from typing import Any, TYPE_CHECKING

from .scripts.texture_mapping import ITEM_TO_SPECIAL_TEXTURE_MAPPING
from pypacks.resources.constants import COLOUR_CODE_MAPPINGS

if TYPE_CHECKING:
    from pypacks.datapack import Datapack
    from pypacks.resources.custom_item import CustomItem

PYPACKS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/pypacks"
IMAGES_PATH = Path(PYPACKS_ROOT)/"assets"/"images"


def extract_item_components(item: "str | CustomItem", datapack: "Datapack") -> dict[str, Any]:
    """Returns the item's components (fixed)"""
    from pypacks.resources.custom_item import CustomItem
    regular_data = item.to_dict(datapack.namespace) if isinstance(item, CustomItem) else {}
    components = item.additional_item_data.to_dict(datapack) if isinstance(item, CustomItem) and item.additional_item_data is not None else {}
    combined = recusively_remove_nones_from_data(regular_data | components)
    return combined


def recusively_remove_nones_from_data(obj: Any) -> Any:
    if isinstance(obj, list):
        return [recusively_remove_nones_from_data(x) for x in obj if x is not None]
    if isinstance(obj, dict):
        return {key: recusively_remove_nones_from_data(value) for key, value in obj.items() if value is not None}
    return obj


def _to_snbt(obj: dict[str, Any]) -> str:
    return json.dumps(recusively_remove_nones_from_data(obj)).replace("\"'", "'").replace("'\"", "'")


def to_component_string(obj: dict[str, Any]) -> str:
    return ", ".join([f"{key}={_to_snbt(val)}" for key, val in obj.items() if val is not None])


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


def resolve_default_item_image(base_item: str) -> Path:
    no_minecraft = base_item.removeprefix('minecraft:')
    path = Path(PYPACKS_ROOT)/"assets"/"minecraft"/"item"/f"{no_minecraft}.png"
    if no_minecraft in ITEM_TO_SPECIAL_TEXTURE_MAPPING:
        path = Path(PYPACKS_ROOT)/"assets"/"minecraft"/"item"/f"{ITEM_TO_SPECIAL_TEXTURE_MAPPING[no_minecraft]}.png"
    if no_minecraft in ["player_head", "zombie_head", "creeper_head", "skeleton_skull", "wither_skeleton_skull", "dragon_head"]:
        path = Path(PYPACKS_ROOT)/"assets"/"images"/"reference_book_icons"/"player_head.png"
    if no_minecraft in ["white_banner", "orange_banner", "magenta_banner", "light_blue_banner", "yellow_banner", "lime_banner", "pink_banner", "gray_banner", "light_gray_banner", "cyan_banner", "purple_banner", "blue_banner", "brown_banner", "green_banner", "red_banner", "black_banner"]:
        path = Path(PYPACKS_ROOT)/"assets"/"images"/"reference_book_icons"/"banner.png"
    if no_minecraft.endswith("spawn_egg"):
        path = Path(PYPACKS_ROOT)/"assets"/"images"/"reference_book_icons"/"spawn_egg.png"
    if not path.exists():
        path = Path(PYPACKS_ROOT)/"assets"/"images"/"reference_book_icons"/"unknown.png"  # Others, player head
    return path


def chunk_list(lst: list[Any], size: int) -> list[list[Any]]:
    return [lst[i:i + size] for i in range(0, len(lst), size)]


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
