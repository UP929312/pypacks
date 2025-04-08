import os
from typing import Any

import requests

from pypacks.resources.custom_damage_type import CustomDamageType


all_data: dict[str, Any] = requests.get("https://raw.githubusercontent.com/misode/mcmeta/refs/heads/summary/data/damage_type/data.min.json").json()
output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\minecraft\\damage_types.py"

lines = [
    "from pypacks.resources.custom_damage_type import CustomDamageType",
    "",
    "",
]

instances = [CustomDamageType.from_dict(data["message_id"].replace(".", "_"), data, []) for item_name, data in all_data.items()]
lines += [f"{x.internal_name.upper().replace('/', '_')} = {repr(x)}" for x in instances]

with open(output_path, "w", encoding="utf-8") as file:
    file.write("\n".join(lines)+"\n")
