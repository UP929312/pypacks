import os
import json

import requests

data = requests.get("https://raw.githubusercontent.com/misode/mcmeta/1.21.4-summary/item_components/data.min.json").json()

output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\scripts\\all_items.py"

BASE = """from typing import Literal

MinecraftItem = Literal"""

with open(output_path, "w") as file:
    combined = sorted(data)+sorted([f"minecraft:{x}" for x in data])
    file.write(BASE+json.dumps(combined, indent=4)+"\n")
