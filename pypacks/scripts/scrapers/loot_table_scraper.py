import os
import json

VERSION = "1.21.5"
ENABLED = False
input_path = f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\.minecraft\\versions\\{VERSION}\\{VERSION}\\data\\minecraft\\loot_table"
output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\scripts\\repos\\loot_tables.py"

loot_tables = []

for root, _, files in os.walk(input_path):
    for file_name in files:
        if file_name.endswith(".json"):
            relative_path = os.path.relpath(os.path.join(root, file_name), input_path)
            loot_tables.append(relative_path.replace("\\", "/").removesuffix(".json"))

BASE = """from typing import Literal

LootTables = Literal"""

with open(output_path, "w", encoding="utf-8") as file:
    if ENABLED:
        file.write(BASE+json.dumps(sorted(loot_tables), indent=4)+"\n")
    else:
        file.write("LootTables = str\n")
