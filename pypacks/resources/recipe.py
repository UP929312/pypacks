import json
from dataclasses import dataclass
from typing import TypeVar


# https://minecraft.wiki/w/Recipe


@dataclass
class ShapelessCraftingRecipe:
    name: str
    ingredients: list[list[str] | str]
    # Ingredients can either be a list of Items (i.e. a flint and iron ingot makes a flint and steel), or a list of lists,
    # which allows you to put multiple items in, e.g. making a chest from all the types of wood.
    result: str
    amount: int = 1

    def to_file_contents(self) -> str:
        return json.dumps({
            "type": "minecraft:crafting_shapeless",
            "ingredients": self.ingredients,
            "result": {
                "id": self.result,
                "count": self.amount,
            }
        }, indent=4)


@dataclass
class ShapedCraftingRecipe:
    name: str
    rows: list[str]
    keys: dict[str, list[str] | str]
    result: str
    amount: int = 1

    def __post_init__(self):
        assert 0 < len(self.rows) <= 3, "Rows must be a list of 1-3 strings"
        row_1 = self.rows[0]
        row_2 = self.rows[1] if len(self.rows) >= 2 else None
        row_3 = self.rows[2] if len(self.rows) == 3 else None
        self.removed_nones_rows = [x for x in [row_1, row_2, row_3] if x is not None]

    def to_file_contents(self) -> str:
        return json.dumps({
            "type": "minecraft:crafting_shaped",
            "pattern": self.removed_nones_rows,
            "key": self.keys,
            "result": {
                "id": self.result,
                "count": self.amount,
            },
            "show_notification": True,
        }, indent=4)


@dataclass
class CraftingTransmuteRecipe:
    name: str
    input_item: str
    material_item: str
    result: str

    def to_file_contents(self) -> str:
        return json.dumps({
            "type": "minecraft:crafting_shapeless",
            "input": self.input_item,
            "material": self.material_item,
            "result": self.result,
        }, indent=4)


@dataclass
class FurnaceRecipe:
    name: str
    ingredient: str
    result: str
    experience: int | None = 1
    cooking_time_ticks: int = 200

    def to_file_contents(self) -> str:
        return json.dumps({
            "type": "minecraft:smelting",
            "ingredient": self.ingredient,
            "result": {
                "id": self.result,
            },
            "experience": self.experience,
            "cookingtime": self.cooking_time_ticks,
        }, indent=4)


@dataclass
class BlastFurnaceRecipe:
    name: str
    ingredient: str
    result: str
    experience: int | None = 1
    cooking_time_ticks: int = 200

    def to_file_contents(self) -> str:
        return json.dumps({
            "type": "minecraft:blasting",
            "ingredient": self.ingredient,
            "result": {
                "id": self.result,
            },
            "experience": self.experience,
            "cookingtime": self.cooking_time_ticks
        }, indent=4)


@dataclass
class CampfireRecipe:
    name: str
    ingredient: str
    result: str
    experience: int | None = 1
    cooking_time_ticks: int = 200

    def to_file_contents(self) -> str:
        return json.dumps({
            "type": "minecraft:campfire_cooking",
            "ingredient": self.ingredient,
            "result": {
                "id": self.result,
            },
            "experience": self.experience,
            "cookingtime": self.cooking_time_ticks,
        }, indent=4)

@dataclass
class SmithingTransformRecipe:
    name: str
    template_item: str
    base_item: str
    addition_item: str
    result: str

    def to_file_contents(self) -> str:
        return json.dumps({
            "type": "minecraft:smithing_transform",
            "template": {
                "item": self.template_item,
            },
            "base": {
                "item": self.base_item,
            },
            "addition": {
                "item": self.addition_item,
            },
            "result": {
                "item": self.result,
            }
        }, indent=4)


@dataclass
class SmithingTrimRecipe:
    name: str
    template_item: str
    base_item: str
    addition_item: str

    def to_file_contents(self) -> str:
        return json.dumps({
            "type": "minecraft:smithing_trim",
            "template": {
                "item": self.template_item,
            },
            "base": {
                "item": self.base_item,
            },
            "addition": {
                "item": self.addition_item,
            },
        }, indent=4)


@dataclass
class SmokerRecipe:
    name: str
    ingredient: str
    result: str
    experience: int | None = 1
    cooking_time_ticks: int = 200

    def to_file_contents(self) -> str:
        return json.dumps({
            "type": "minecraft:smoking",
            "ingredient": self.ingredient,
            "result": {
                "id": self.result,
            },
            "experience": self.experience,
            "cookingtime": self.cooking_time_ticks,
        }, indent=4)


@dataclass
class StonecutterRecipe:
    name: str
    ingredient: str
    result: str
    count: int = 1

    def to_file_contents(self) -> str:
        return json.dumps({
            "type": "minecraft:stonecutting",
            "ingredient": self.ingredient,
            "result": {
                "id": self.result,
                "count": self.count,
            }
        }, indent=4)


# This is a type hint for a recipe, it can be any of the recipe types
Recipe = TypeVar(
    "Recipe", ShapelessCraftingRecipe, ShapedCraftingRecipe, CraftingTransmuteRecipe, FurnaceRecipe, BlastFurnaceRecipe,
    CampfireRecipe, SmithingTransformRecipe, SmithingTrimRecipe, SmokerRecipe, StonecutterRecipe
)
