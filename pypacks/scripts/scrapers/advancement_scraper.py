import os
import json

VERSION = "1.21.5"
ENABLED = True
input_path = f"C:/Users/{os.environ['USERNAME']}/AppData/Roaming/.minecraft/versions/{VERSION}/{VERSION}/data/minecraft/advancement/"
output_path = f"C:/Users/{os.environ['USERNAME']}/Desktop/pypacks/pypacks/scripts/repos/advancements.py"

advancements = []

for root, _, files in os.walk(input_path):
    if "recipes" in root:
        continue
    for file_name in files:
        advancements.append(root.removeprefix(input_path).removeprefix("\\")+"/"+file_name.removesuffix(".json"))

BASE = """from typing import Literal

AdvancementsType = Literal"""

with open(output_path, "w", encoding="utf-8") as file:
    if ENABLED:
        file.write(BASE+json.dumps(sorted(advancements), indent=4)+"\n")
    else:
        file.write("AdvancementsType = str\n\n"+'"""'+BASE+json.dumps(sorted(advancements), indent=4)+"\n"+'"""\n')
