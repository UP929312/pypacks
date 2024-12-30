import os
import json

from pypacks.scripts.default_dictionary import DEFAULT_OBJECT_JSON

output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\scripts\\all_items.py"

BASE = """from typing import Literal

MinecraftItem = Literal"""

with open(output_path, "w") as file:
    combined = sorted(DEFAULT_OBJECT_JSON)+sorted([f"minecraft:{x}" for x in DEFAULT_OBJECT_JSON])
    file.write(BASE+json.dumps(combined, indent=4))
