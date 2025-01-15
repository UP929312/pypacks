import os
import json

VERSION = "1.21.4"
input_path = f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\.minecraft\\versions\\{VERSION}\\{VERSION}\\data\\minecraft\\damage_type"
output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\scripts\\repos\\damage_types.py"

damage_types = [x.removesuffix(".json") for x in os.listdir(input_path)]

# {
#   "exhaustion": 0.0,
#   "message_id": "magic",
#   "scaling": "when_caused_by_living_non_player"
# }

BASE = """from typing import Literal

DamageTypesType = Literal"""

with open(output_path, "w") as file:
    file.write(BASE+json.dumps(sorted(damage_types), indent=4)+"\n")
