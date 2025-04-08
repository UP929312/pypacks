import os
from typing import Any

import requests

from pypacks.resources.custom_advancement import CustomAdvancement


all_data: dict[str, Any] = requests.get("https://raw.githubusercontent.com/misode/mcmeta/refs/heads/summary/data/advancement/data.min.json").json()
output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\minecraft\\advancements.py"

lines = [
    "from pypacks.resources.custom_advancement import CustomAdvancement, Criteria",
    "",
    "",
]

instances = [CustomAdvancement.from_dict(item_name.split("/")[-1], data, item_name.split("/")[:-1]) for item_name, data in all_data.items()]
lines += [f"{x.internal_name.upper().replace('/', '_')} = {repr(x)}" for x in instances]

with open(output_path, "w", encoding="utf-8") as file:
    file.write("\n".join(lines)+"\n")
