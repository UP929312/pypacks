import json
from dataclasses import dataclass
from typing import TypeVar, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from pypacks.datapack import Datapack

from pypacks.resources.custom_item import CustomItem

StringOrItemOrTag = TypeVar("StringOrItemOrTag", str, CustomItem)

# https://minecraft.wiki/w/Recipe

@dataclass
class GenericRecipe:
    name: str

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        raise NotImplementedError
    
    def format_item_or_string(self, item_or_string: str | CustomItem) -> str:
        if isinstance(item_or_string, CustomItem):
            return item_or_string.base_item
        return item_or_string

    def create_json_file(self, datapack: "Datapack") -> None:
        with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/recipe/{self.name}.json", "w") as f:
            json.dump(self.to_dict(datapack), f, indent=4)

@dataclass
class ShapelessCraftingRecipe(GenericRecipe):
    name: str
    ingredients: list[list[str] | str]
    # Ingredients can either be a list of Items (i.e. a flint and iron ingot makes a flint and steel), or a list of lists,
    # which allows you to put multiple items in, e.g. making a chest from all the types of wood.
    result: StringOrItemOrTag  # type: ignore
    amount: int = 1

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        data = {
            "type": "minecraft:crafting_shapeless",
            "ingredients": self.ingredients,
            "result": {
                "id": self.format_item_or_string(self.result),
                "count": self.amount,
            }
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_components_dict(datapack)
        return data


@dataclass
class ShapedCraftingRecipe(GenericRecipe):
    name: str
    rows: list[str]
    keys: dict[str, list[str] | str]
    result: StringOrItemOrTag  # type: ignore[abc]
    amount: int = 1

    def __post_init__(self) -> None:
        assert 0 < len(self.rows) <= 3, "Rows must be a list of 1-3 strings"
        row_1 = self.rows[0]
        row_2 = self.rows[1] if len(self.rows) >= 2 else None
        row_3 = self.rows[2] if len(self.rows) == 3 else None
        self.removed_nones_rows = [x for x in [row_1, row_2, row_3] if x is not None]

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        data = {
            "type": "minecraft:crafting_shaped",
            "pattern": self.removed_nones_rows,
            "key": self.keys,
            "result": {
                "id": self.format_item_or_string(self.result),
                "count": self.amount,
            },
            "show_notification": True,
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_components_dict(datapack)
        return data


@dataclass
class CraftingTransmuteRecipe(GenericRecipe):
    name: str
    input_item: str
    material_item: str
    result: str

    def to_dict(self, datapack: "Datapack") -> dict[str, str]:
        return {
            "type": "minecraft:crafting_shapeless",
            "input": self.input_item,
            "material": self.material_item,
            "result": self.result,
        }


@dataclass
class FurnaceRecipe(GenericRecipe):
    name: str
    ingredient: str
    result: StringOrItemOrTag  # type: ignore
    experience: int | None = 1
    cooking_time_ticks: int = 200

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        data = {
            "type": "minecraft:smelting",
            "ingredient": self.ingredient,
            "result": {
                "id": self.format_item_or_string(self.result),
            },
            "experience": self.experience,
            "cookingtime": self.cooking_time_ticks,
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_components_dict(datapack)
        return data


@dataclass
class BlastFurnaceRecipe(GenericRecipe):
    name: str
    ingredient: str
    result: StringOrItemOrTag  # type: ignore
    experience: int | None = 1
    cooking_time_ticks: int = 200

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        data = {
            "type": "minecraft:blasting",
            "ingredient": self.ingredient,
            "result": {
                "id": self.format_item_or_string(self.result),
            },
            "experience": self.experience,
            "cookingtime": self.cooking_time_ticks
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_components_dict(datapack)
        return data


@dataclass
class CampfireRecipe(GenericRecipe):
    name: str
    ingredient: str
    result: StringOrItemOrTag  # type: ignore
    experience: int | None = 1
    cooking_time_ticks: int = 200

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        data = {
            "type": "minecraft:campfire_cooking",
            "ingredient": self.ingredient,
            "result": {
                "id": self.format_item_or_string(self.result),
            },
            "experience": self.experience,
            "cookingtime": self.cooking_time_ticks,
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_components_dict(datapack)
        return data

@dataclass
class SmithingTransformRecipe(GenericRecipe):
    name: str
    template_item: str
    base_item: str
    addition_item: str
    result: StringOrItemOrTag  # type: ignore

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        data = {
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
                "item": self.format_item_or_string(self.result),
            }
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_components_dict(datapack)
        return data


@dataclass
class SmithingTrimRecipe(GenericRecipe):
    name: str
    template_item: str
    base_item: str
    addition_item: str

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        return {
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
        }


@dataclass
class SmokerRecipe(GenericRecipe):
    name: str
    ingredient: str
    result: StringOrItemOrTag  # type: ignore
    experience: int | None = 1
    cooking_time_ticks: int = 200

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        data = {
            "type": "minecraft:smoking",
            "ingredient": self.ingredient,
            "result": {
                "id": self.format_item_or_string(self.result),
            },
            "experience": self.experience,
            "cookingtime": self.cooking_time_ticks,
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_components_dict(datapack)
        return data


@dataclass
class StonecutterRecipe(GenericRecipe):
    name: str
    ingredient: str
    result: StringOrItemOrTag  # type: ignore
    count: int = 1

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        data = {
            "type": "minecraft:stonecutting",
            "ingredient": self.ingredient,
            "result": {
                "id": self.format_item_or_string(self.result),
                "count": self.count,
            }
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_components_dict(datapack)
        return data


# This is a type hint for a recipe, it can be any of the recipe types
Recipe = TypeVar(
    "Recipe", ShapelessCraftingRecipe, ShapedCraftingRecipe, CraftingTransmuteRecipe, FurnaceRecipe, BlastFurnaceRecipe,
    CampfireRecipe, SmithingTransformRecipe, SmithingTrimRecipe, SmokerRecipe, StonecutterRecipe
)
