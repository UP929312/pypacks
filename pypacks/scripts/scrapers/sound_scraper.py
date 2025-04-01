import os
import json

import requests

data = requests.get("https://raw.githubusercontent.com/misode/mcmeta/1.21.5-summary/sounds/data.min.json").json()

ENABLED = False
output_path = f"C:/Users/{os.environ['USERNAME']}/Desktop/pypacks/pypacks/scripts/repos/sounds.py"

BASE = """from typing import Literal

MinecraftSound = Literal"""

all_sounds = sorted([f"minecraft:{x}" for x in data])

with open(output_path, "w", encoding="utf-8") as file:
    if ENABLED:
        file.write(BASE+json.dumps(all_sounds, indent=4)+"\n")
    else:
        file.write("MinecraftSound = str\n\n"+'"""'+BASE+json.dumps(all_sounds, indent=4)+"\n"+'"""')
