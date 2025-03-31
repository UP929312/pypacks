import os
import json
import shutil
from pathlib import Path
from typing import Any

PYPACKS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/pypacks"
IMAGES_PATH = Path(PYPACKS_ROOT)/"assets"/"images"

MAX_INT = 2_147_483_648
MAX_FLOAT = 3.402823466E+38


def recursively_remove_nones_from_data(obj: Any) -> Any:
    """Recursively goes through dicts and lists and removes keys/values which are None."""
    if isinstance(obj, list):
        return [recursively_remove_nones_from_data(x) for x in obj if x is not None]
    if isinstance(obj, dict):
        return {key: recursively_remove_nones_from_data(value) for key, value in obj.items() if value is not None}
    return obj


def chunk_list(lst: list[Any], size: int) -> list[list[Any]]:
    """Chunks a list into smaller lists of size `size`."""
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def format_written_book(string: str) -> str:
    # Extract the JSON part (inside `written_book_content=...`)
    prefix = 'written_book_content='
    start = string.index(prefix) + len(prefix)
    json_str = string[start:].rstrip(']')  # Remove trailing `]` if needed

    # Parse JSON and pretty-print it
    parsed_json = json.loads(json_str)
    return string[:start]+json.dumps(parsed_json, indent=4).replace("\n", " \\\n")+"]"


def cleanup_experimental_warning(save_path: "str | Path") -> None:
    """Removes the experimental warning from a save file that is caused by level.dat & experimental features.
    WARNING: This alters the save file and removes multiple folders and files!"""
    save_path = Path(save_path)
    # Delete the level.dat references to custom dimensions
    from pypacks.additions.nbt_parser import NBTParser
    parser = NBTParser.from_file(save_path/"level.dat")
    data = parser.output
    non_default_dimensions = [x for x in data[""]["Data"]["WorldGenSettings"]["dimensions"] if x not in ["minecraft:overworld", "minecraft:the_nether", "minecraft:the_end"]]
    for dimension in non_default_dimensions:
        print(f"Contains custom dimension: {dimension}, needs to be removed!")
        del data[""]["Data"]["WorldGenSettings"]["dimensions"][dimension]
    # Make sure the player's dimension is set to the overworld
    data[""]["Data"]["Player"]["Dimension"] = "minecraft:overworld"
    parser.to_file(save_path/"level.dat")
    # Delete the custom dimensions and dimension types folder (and worldgen folder)
    from pypacks.additions.constants import EXPERIMENTAL_FEATURES
    for datapack in os.listdir(save_path/"datapacks"):
        for namespace in os.listdir(save_path/"datapacks"/datapack/"data"):
            # print(save_path/"datapacks"/datapack/"data"/namespace/"dimension")
            for directory in EXPERIMENTAL_FEATURES:
                shutil.rmtree(save_path/"datapacks"/datapack/"data"/namespace/directory, ignore_errors=True)
