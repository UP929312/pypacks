import os
import json

VERSION = "1.21.4"
input_path = f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\.minecraft\\versions\\{VERSION}\\{VERSION}\\data\\minecraft\\advancement"
output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\scripts\\advancements.py"

advancements = []

for _, _, files in os.walk(input_path):
    for file in files:
        advancements.append(file.removesuffix(".json"))

BASE = """from typing import Literal

AdvancementsType = Literal"""

with open(output_path, "w") as file:
    file.write(BASE+json.dumps(sorted(advancements), indent=4))
