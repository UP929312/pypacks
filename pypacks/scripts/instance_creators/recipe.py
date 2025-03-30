import os
from typing import Any

import requests

from pypacks.resources.custom_recipe import Recipe


all_data: dict[str, Any] = requests.get("https://raw.githubusercontent.com/misode/mcmeta/refs/heads/summary/data/recipe/data.min.json").json()
output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\minecraft\\recipes.py"

lines = [
    "from pypacks.resources.custom_recipe import ShapedCraftingRecipe, ShapelessCraftingRecipe, FurnaceRecipe, CampfireRecipe, SmokerRecipe, StonecutterRecipe, CraftingTransmuteRecipe, BlastFurnaceRecipe, SmithingTrimRecipe, SmithingTransformRecipe",
    "from pypacks.resources.custom_item import CustomItem",
    "",
    "",
]

def parse_recipe_data(item_name: str, data: dict[str, Any]) -> "Recipe | None":
    try:
        return Recipe.from_dict(item_name, data)
    except KeyError:
        return None

instances = [parse_recipe_data(item_name, data) for item_name, data in all_data.items()]
lines += [f"{x.internal_name.upper()} = {repr(x)}" for x in instances if x is not None]

with open(output_path, "w", encoding="utf-8") as file:
    file.write("\n".join(lines)+"\n")
