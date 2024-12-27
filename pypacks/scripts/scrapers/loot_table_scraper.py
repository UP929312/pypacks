import os
import json

VERSION = "1.21.4"
input_path = f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\.minecraft\\versions\\{VERSION}\\{VERSION}\\data\\minecraft\\loot_table"
output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\scripts\\loot_tables.py"

loot_tables = []

for root, _, files in os.walk(input_path):
    for file in files:
        if file.endswith(".json"):
            relative_path = os.path.relpath(os.path.join(root, file), input_path)
            loot_tables.append(relative_path.replace("\\", "/").removesuffix(".json"))

BASE = """from typing import Literal

LootTables = Literal"""

with open(output_path, "w") as file:
    file.write(BASE+json.dumps(loot_tables, indent=4))
