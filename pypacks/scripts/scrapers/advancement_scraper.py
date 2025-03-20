import os
import json

VERSION = "1.21.4"
ENABLED = False
input_path = f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\.minecraft\\versions\\{VERSION}\\{VERSION}\\data\\minecraft\\advancement"
output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\scripts\\repos\\advancements.py"

advancements = []

for *_, files in os.walk(input_path):
    for file_name in files:
        advancements.append(file_name.removesuffix(".json"))

BASE = """from typing import Literal

AdvancementsType = Literal"""

with open(output_path, "w", encoding="utf-8") as file:
    if ENABLED:
        file.write(BASE+json.dumps(sorted(advancements), indent=4)+"\n")
    else:
        file.write("AdvancementsType = str\n")
