import os
from typing import Any

import requests

from pypacks.resources.custom_painting import CustomPainting


all_data: dict[str, Any] = requests.get("https://raw.githubusercontent.com/misode/mcmeta/refs/heads/summary/data/painting_variant/data.min.json").json()
output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\minecraft\\paintings.py"

lines = [
    "from pypacks.resources.custom_painting import CustomPainting",
    "",
    "",
]

instances = [CustomPainting.from_dict(item_name.split("/")[0], data, item_name.split("/")[1:]) for item_name, data in all_data.items()]
lines += [f"{x.internal_name.upper()} = {repr(x)}" for x in instances]
lines += [""]
lines += ["ALL_PAINTINGS = ["]
lines += ["    "+", ".join([x.internal_name.upper() for x in instances])]
lines += ["]"]

with open(output_path, "w", encoding="utf-8") as file:
    file.write("\n".join(lines)+"\n")
