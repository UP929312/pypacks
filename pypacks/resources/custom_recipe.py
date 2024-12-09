import json
from dataclasses import dataclass, field
from typing import TypeAlias, Any, TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from pypacks.datapack import Datapack

from pypacks.image_generation.recipe_image_data import generate_recipe_image
from pypacks.resources.custom_item import CustomItem

StringOrItemOrTag: TypeAlias = str | CustomItem
StringOrCustomItem: TypeAlias = str | CustomItem
RecipeCategory = Literal["blocks", "building", "equipment", "food", "misc", "redstone"]

# https://minecraft.wiki/w/Recipe


@dataclass
class GenericRecipe:
    internal_name: str

    datapack_subdirectory_name: str = field(init=False, repr=False, default="recipe")

    def __post_init__(self) -> None:
        self.recipe_image_bytes = generate_recipe_image(self)  # type: ignore

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        raise NotImplementedError
    
    def format_item_or_string(self, item_or_string: "str | CustomItem") -> str:
        if isinstance(item_or_string, CustomItem):
            return item_or_string.base_item
        return item_or_string

    def create_datapack_files(self, datapack: "Datapack") -> None:
        with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/{self.__class__.datapack_subdirectory_name}/{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(datapack), file, indent=4)


@dataclass
class ShapelessCraftingRecipe(GenericRecipe):
    internal_name: str
    ingredients: list[list[str] | str]
    # Ingredients can either be a list of Items (i.e. a flint and iron ingot makes a flint and steel), or a list of lists,
    # which allows you to put multiple items in, e.g. making a chest from all the types of wood.
    result: StringOrCustomItem
    amount: int = 1
    recipe_category: RecipeCategory = "misc"

    recipe_block_name: str = field(init=False, repr=False, default="crafting_table")

    def __post_init__(self) -> None:
        assert 0 < len(self.ingredients) <= 9, "Ingredients must be a list of 1-9 items"

        self.recipe_image_bytes = generate_recipe_image(self)

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        data = {
            "type": "minecraft:crafting_shapeless",
            "category": self.recipe_category,
            "ingredients": self.ingredients,
            "result": {
                "id": self.format_item_or_string(self.result),
                "count": self.amount,
            }
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_dict(datapack.namespace)  # type: ignore[index, call-overload]
        return data


@dataclass
class ShapedCraftingRecipe(GenericRecipe):
    internal_name: str
    rows: list[str]
    keys: dict[str, list[str] | str]
    result: StringOrCustomItem
    amount: int = 1
    recipe_category: RecipeCategory = "misc"

    recipe_block_name: str = field(init=False, repr=False, default="crafting_table")

    def __post_init__(self) -> None:
        super().__post_init__()
        assert 0 < len(self.rows) <= 3, "Rows must be a list of 1-3 strings"
        row_1 = self.rows[0]
        row_2 = self.rows[1] if len(self.rows) >= 2 else None
        row_3 = self.rows[2] if len(self.rows) == 3 else None
        self.removed_nones_rows = [x for x in [row_1, row_2, row_3] if x is not None]

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        data = {
            "type": "minecraft:crafting_shaped",
            "category": self.recipe_category,
            "pattern": self.removed_nones_rows,
            "key": self.keys,
            "result": {
                "id": self.format_item_or_string(self.result),
                "count": self.amount,
            },
            "show_notification": True,
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_dict(datapack.namespace)  # type: ignore[index, call-overload, assignment]
        return data


@dataclass
class CraftingTransmuteRecipe(GenericRecipe):
    internal_name: str
    input_item: str
    material_item: str
    result: str
    recipe_category: RecipeCategory = "misc"

    recipe_block_name: str = field(init=False, repr=False, default="crafting_table_transmute")

    def to_dict(self, datapack: "Datapack") -> dict[str, str]:
        return {
            "type": "minecraft:crafting_shapeless",
            "category": self.recipe_category,
            "input": self.input_item,
            "material": self.material_item,
            "result": self.result,
        }


@dataclass
class FurnaceRecipe(GenericRecipe):
    internal_name: str
    ingredient: str
    result: StringOrCustomItem
    experience: int | None = 1
    cooking_time_ticks: int = 200
    recipe_category: RecipeCategory = "misc"

    recipe_block_name: str = field(init=False, repr=False, default="furnace")

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        data = {
            "type": "minecraft:smelting",
            "category": self.recipe_category,
            "ingredient": self.ingredient,
            "result": {
                "id": self.format_item_or_string(self.result),
            },
            "experience": self.experience,
            "cookingtime": self.cooking_time_ticks,
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_dict(datapack.namespace)  # type: ignore[index, assignment]
        return data


@dataclass
class BlastFurnaceRecipe(GenericRecipe):
    internal_name: str
    ingredient: str
    result: StringOrCustomItem
    experience: int | None = 1
    cooking_time_ticks: int = 200
    recipe_category: RecipeCategory = "misc"

    recipe_block_name: str = field(init=False, repr=False, default="blast_furnace")

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        data = {
            "type": "minecraft:blasting",
            "category": self.recipe_category,
            "ingredient": self.ingredient,
            "result": {
                "id": self.format_item_or_string(self.result),
            },
            "experience": self.experience,
            "cookingtime": self.cooking_time_ticks
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_dict(datapack.namespace)  # type: ignore[index, assignment]
        return data


@dataclass
class CampfireRecipe(GenericRecipe):
    internal_name: str
    ingredient: str
    result: StringOrCustomItem
    experience: int | None = 1
    cooking_time_ticks: int = 200
    recipe_category: RecipeCategory = "misc"

    recipe_block_name: str = field(init=False, repr=False, default="campfire")

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        data = {
            "type": "minecraft:campfire_cooking",
            "category": self.recipe_category,
            "ingredient": self.ingredient,
            "result": {
                "id": self.format_item_or_string(self.result),
            },
            "experience": self.experience,
            "cookingtime": self.cooking_time_ticks,
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_dict(datapack.namespace)  # type: ignore[index, assignment]
        return data


@dataclass
class SmithingTransformRecipe(GenericRecipe):
    internal_name: str
    template_item: str
    base_item: str
    addition_item: str
    result: StringOrCustomItem
    recipe_category: RecipeCategory = "misc"

    recipe_block_name: str = field(init=False, repr=False, default="smithing_table")

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        data = {
            "type": "minecraft:smithing_transform",
            "category": self.recipe_category,
            "template": self.template_item,
            "base": self.base_item,
            "addition": self.addition_item,
            "result": {"id": self.format_item_or_string(self.result)},
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_dict(datapack.namespace)  # type: ignore[index, assignment]
        return data


@dataclass
class SmithingTrimRecipe(GenericRecipe):
    internal_name: str
    template_item: str
    base_item: str
    addition_item: str

    recipe_block_name: str = field(init=False, repr=False, default="smithing_table")

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        return {
            "type": "minecraft:smithing_trim",
            "template": {"item": self.template_item},
            "base": {"item": self.base_item},
            "addition": {"item": self.addition_item},
        }


@dataclass
class SmokerRecipe(GenericRecipe):
    internal_name: str
    ingredient: str
    result: StringOrCustomItem
    experience: int | None = 1
    cooking_time_ticks: int = 200
    recipe_category: RecipeCategory = "misc"

    recipe_block_name: str = field(init=False, repr=False, default="smoker")

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        data = {
            "type": "minecraft:smoking",
            "category": self.recipe_category,
            "ingredient": self.ingredient,
            "result": {
                "id": self.format_item_or_string(self.result),
            },
            "experience": self.experience,
            "cookingtime": self.cooking_time_ticks,
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_dict(datapack.namespace)  # type: ignore[index, assignment]
        return data


@dataclass
class StonecutterRecipe(GenericRecipe):
    internal_name: str
    ingredient: str
    result: StringOrCustomItem
    count: int = 1
    recipe_category: RecipeCategory = "misc"

    recipe_block_name: str = field(init=False, repr=False, default="stonecutter")

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        data = {
            "type": "minecraft:stonecutting",
            "category": self.recipe_category,
            "ingredient": self.ingredient,
            "result": {
                "id": self.format_item_or_string(self.result),
                "count": self.count,
            }
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_dict(datapack.namespace)  # type: ignore[index]
        return data

# This is a type hint for a recipe, it can be any of the recipe types
Recipe: TypeAlias = (
    ShapelessCraftingRecipe | ShapedCraftingRecipe | CraftingTransmuteRecipe | FurnaceRecipe | BlastFurnaceRecipe |
    CampfireRecipe | SmithingTransformRecipe | SmithingTrimRecipe | SmokerRecipe | StonecutterRecipe
)

ALL_RECIPES: list[Recipe] = [
    ShapelessCraftingRecipe, ShapedCraftingRecipe, CraftingTransmuteRecipe, FurnaceRecipe, BlastFurnaceRecipe,  # type: ignore[list-item]
    CampfireRecipe, SmithingTransformRecipe, SmithingTrimRecipe, SmokerRecipe, StonecutterRecipe,  # type: ignore[list-item]
]

