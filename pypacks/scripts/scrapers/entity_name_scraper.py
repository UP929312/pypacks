import os
import json

VERSION = "1.21.5"
input_path = f"C:/Users/{os.environ['USERNAME']}/AppData/Roaming/.minecraft/versions/{VERSION}/{VERSION}/data/minecraft\\tags\\entity_type"
output_path = f"C:/Users/{os.environ['USERNAME']}/Desktop/pypacks/pypacks/scripts/repos/all_entity_names.py"

all_entity_names = []
for tag in os.listdir(input_path):
    with open(input_path+f"\\{tag}", encoding="utf-8") as file:
        data = json.load(file)
    all_entity_names.extend([x for x in data["values"] if not x.startswith("#")])  # Remove all references to other tags

all_entity_names.extend([
    # From folders:
    "minecraft:cow", "minecraft:creaking", "minecraft:creeper", "minecraft:enderdragon", "minecraft:enderman", "minecraft:goat",
    "minecraft:hoglin", "minecraft:illager", "minecraft:panda", "minecraft:piglin", "minecraft:sheep", "minecraft:sniffer",
    "minecraft:villager", "minecraft:warden", "minecraft:wolf",
    # From files:
    "minecraft:armadillo", "minecraft:guardian", "minecraft:wandering_trader",
])

BASE = """from typing import Literal

MinecraftEntity = Literal"""

with open(output_path, "w", encoding="utf-8") as file:
    file.write(BASE+json.dumps(list(sorted(set(all_entity_names))), indent=4)+"\n")
