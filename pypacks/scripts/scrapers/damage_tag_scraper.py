import os
import json

VERSION = "1.21.5"
input_path = f"C:/Users/{os.environ['USERNAME']}/AppData/Roaming/.minecraft/versions/{VERSION}/{VERSION}/data/minecraft\\tags\\damage_type"
output_path = f"C:/Users/{os.environ['USERNAME']}/Desktop/pypacks/pypacks/scripts/repos/damage_tags.py"

damage_tags = [x.removesuffix(".json") for x in os.listdir(input_path)]

BASE = """from typing import Literal

DamageTagsType = Literal"""

with open(output_path, "w", encoding="utf-8") as file:
    file.write(BASE+json.dumps(sorted(damage_tags), indent=4)+"\n")
