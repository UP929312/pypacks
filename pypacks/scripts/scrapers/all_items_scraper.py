import os
import json

import requests

data = requests.get("https://raw.githubusercontent.com/misode/mcmeta/1.21.5-summary/item_components/data.min.json").json()

ENABLED = False
output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\scripts\\repos\\all_items.py"

BASE = """from typing import Literal

MinecraftItem = Literal"""

with open(output_path, "w", encoding="utf-8") as file:
    if ENABLED:
        combined = sorted([f"minecraft:{x}" for x in data])  # +sorted(data)
        file.write(BASE+json.dumps(combined, indent=4)+"\n")
    else:
        file.write("MinecraftItem = str\n")
