import os
import json

VERSION = "1.21.5"
ENABLED = False
input_path = f"C:/Users/{os.environ['USERNAME']}/AppData/Roaming/.minecraft/versions/{VERSION}/{VERSION}/assets/minecraft/models"
output_path = f"C:/Users/{os.environ['USERNAME']}/Desktop/pypacks/pypacks/scripts/repos/models.py"

block_models = []
for prefix in ["", "minecraft"]:
    for item_type in ["block", "item"]:
        block_models.extend([f"{prefix}{item_type}/{x.removesuffix('.json')}" for x in os.listdir(input_path+f"/{item_type}")])

BASE = """from typing import Literal

MinecraftModels = Literal"""

with open(output_path, "w", encoding="utf-8") as file:
    if ENABLED:
        file.write(BASE+json.dumps(sorted(block_models), indent=4)+"\n")
    else:
        file.write("MinecraftModels = str\n\n"+'"""'+BASE+json.dumps(sorted(block_models), indent=4)+"\n"+'"""')
