import os
from typing import Any

import requests

from pypacks.resources.custom_dimension import CustomDimensionType

all_data: dict[str, Any] = requests.get("https://raw.githubusercontent.com/misode/mcmeta/refs/heads/summary/data/dimension_type/data.min.json").json()

lines = [
    "from pypacks.providers.int_provider import UniformIntProvider",
    "from pypacks.resources.custom_dimension import CustomDimensionType",
    "",
]

names = []
instances: list["CustomDimensionType"] = []
for item_name, data in all_data.items():
    dimension = CustomDimensionType.from_dict(item_name, data, [])
    names.append(dimension.internal_name)
    instances.append(dimension)

lines += [f"{x.internal_name.upper()} = {repr(x)}" for x in instances]

output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\minecraft\\dimension_types.py"
with open(output_path, "w", encoding="utf-8") as file:
    file.write("\n".join(lines)+"\n")
