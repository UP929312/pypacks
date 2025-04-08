from dataclasses import dataclass, field
from typing import TypeAlias, Any, TYPE_CHECKING, Literal


if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.scripts.repos.all_items import MinecraftItem
    MinecraftOrCustomItem: TypeAlias = "MinecraftItem | CustomItem"

from pypacks.image_manipulation.recipe_image_data import generate_recipe_image
from pypacks.resources.base_resource import BaseResource
from pypacks.resources.custom_item import CustomItem
from pypacks.resources.custom_tag import CustomTag


@dataclass
class Recipe(BaseResource):
    # https://minecraft.wiki/w/Recipe
    internal_name: str
    result: "MinecraftOrCustomItem"

    used_ingredients: list["str | CustomItem"] = field(init=False, repr=False, default_factory=list)  # Used for recipe generation, set by __post_init__
    recipe_block_name: str = field(init=False, repr=False)
    datapack_subdirectory_name: str = field(init=False, repr=False, default="recipe")

    def generate_recipe_image(self) -> bytes:
        return generate_recipe_image(self)

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "Recipe":  # type: ignore[override]
        cls_ = RECIPE_TYPE_TO_CLASSES[data["type"]]
        return cls_.from_dict(internal_name, data)

    @staticmethod
    def result_from_dict(internal_name: str, data: dict[str, Any]) -> "MinecraftOrCustomItem":
        if "components" in data["result"]:
            return CustomItem.from_dict(internal_name+"_item", data["result"]["id"], data["result"]["components"])
        return data["result"]["id"]  # type: ignore[no-any-return]

    @staticmethod
    def resolve_ingredient_type(data: "MinecraftItem | CustomTag | list[MinecraftItem] | CustomItem") -> "str | CustomItem":
        """Takes a MinecraftItem, list of MinecraftItems, CustomTag, or CustomItem and returns the first item,
        For CustomItem/MinecraftItem, just return it, for lists, return the first value,
        for Tags, return the first item in the tag (if it's not also a tag, if it is, search in that one too)"""
        if isinstance(data, CustomTag):
            return data.get_first_non_tag_item()
        if isinstance(data, list):
            return data[0]
        return data  # For strings and CustomItems


@dataclass
class CustomCrafterRecipe(Recipe):
    ingredients: list["MinecraftOrCustomItem | Literal['minecraft:air', 'air', ''] | CustomTag"]

    recipe_block_name: str = field(init=False, repr=False, default="custom_crafter")  # "dispenser"

    def __post_init__(self) -> None:
        self.used_ingredients = [self.resolve_ingredient_type(x) for x in self.ingredients]
        assert 0 < len(self.ingredients) <= 9, "Ingredients must be a list of 1-9 items"

    def create_datapack_files(self, pack: "Pack") -> None:
        # No .json file with the recipe for CustomCrafterRecipes
        return


@dataclass
class ShapedCraftingRecipe(Recipe):
    rows: list[str] = field(default_factory=lambda: ["III", " S ", "III"])
    keys: dict[str, "MinecraftItem | CustomTag | list[MinecraftItem]"] = field(default_factory=lambda: {"I": "minecraft:iron_ingot", "S": "minecraft:stick"})
    amount: int = 1
    recipe_category: Literal["equipment", "building", "misc", "redstone"] = "misc"

    recipe_block_name: str = field(init=False, repr=False, default="crafting_table")

    def __post_init__(self) -> None:
        assert 0 < len(self.rows) <= 3, "Rows must be a list of 1-3 strings"
        row_1 = self.rows[0]  # Now row is a 3 length string
        row_2 = self.rows[1] if len(self.rows) >= 2 else None
        row_3 = self.rows[2] if len(self.rows) == 3 else None
        self.removed_nones_rows: list[str] = [x for x in [row_1, row_2, row_3] if x is not None]
        self.enumeratable_list = [
            *[self.keys.get(x, "minecraft:air") for x in row_1],
            *[self.keys.get(x, "minecraft:air") for x in (list(row_2) if row_2 is not None else ["", "", ""])],
            *[self.keys.get(x, "minecraft:air") for x in (list(row_3) if row_3 is not None else ["", "", ""])],
        ]
        self.used_ingredients = [self.resolve_ingredient_type(x) for x in self.enumeratable_list]

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        data = {
            "type": "minecraft:crafting_shaped",
            "category": self.recipe_category,
            "pattern": self.removed_nones_rows,
            "key": {key: (value.get_reference(pack_namespace) if isinstance(value, CustomTag) else value) for key, value in self.keys.items()},
            "result": {
                "id": str(self.result),
                "count": self.amount,
            },
            "show_notification": True,
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_dict(pack_namespace)  # type: ignore[index, call-overload, assignment]
        return data

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "ShapedCraftingRecipe":  # type: ignore[override]
        rows = [data["pattern"][0]]
        if len(data["pattern"]) > 1:
            rows.append(data["pattern"][1])
        if len(data["pattern"]) > 2:
            rows.append(data["pattern"][2])
        return cls(
            internal_name,
            rows=rows,
            keys=data["key"],
            result=cls.result_from_dict(f"{internal_name}_item", data),
            amount=data["result"].get("count", 1),
            recipe_category=data.get("recipe_category", "misc"),
        )


@dataclass
class ShapelessCraftingRecipe(Recipe):
    ingredients: list["MinecraftItem | CustomTag | list[MinecraftItem]"]
    # Ingredients can either be a list of Items (i.e. a flint and iron ingot makes a flint and steel), or a list of lists,
    # which allows you to put multiple items in, e.g. making a chest from all the types of wood.
    amount: int = 1
    recipe_category: Literal["equipment", "building", "misc", "redstone"] = "misc"

    recipe_block_name: str = field(init=False, repr=False, default="crafting_table")

    def __post_init__(self) -> None:
        assert 0 < len(self.ingredients) <= 9, "Ingredients must be a list of 1-9 items"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        data = {
            "type": "minecraft:crafting_shapeless",
            "category": self.recipe_category,
            "ingredients": [(x.get_reference(pack_namespace) if isinstance(x, CustomTag) else x) for x in self.ingredients],
            "result": {
                "id": str(self.result),
                "count": self.amount,
            }
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_dict(pack_namespace)  # type: ignore[index, call-overload]
        return data

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "ShapelessCraftingRecipe":  # type: ignore[override]
        return cls(
            internal_name,
            ingredients=data["ingredients"],
            result=cls.result_from_dict(f"{internal_name}_item", data),
            amount=data["result"].get("count", 1),
            recipe_category=data.get("recipe_category", "misc"),
        )


@dataclass
class CraftingTransmuteRecipe(Recipe):
    result: "MinecraftItem"
    input_item: "MinecraftItem | CustomTag | list[MinecraftItem]"
    material_item: "MinecraftItem | CustomTag | list[MinecraftItem]"
    recipe_category: Literal["equipment", "building", "misc", "redstone"] = "misc"

    recipe_block_name: str = field(init=False, repr=False, default="crafting_table_transmute")

    def __post_init__(self) -> None:
        self.used_ingredients = [self.resolve_ingredient_type(x) for x in [self.input_item, self.material_item]]

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:crafting_transmute",
            "category": self.recipe_category,
            "input": self.input_item.get_reference(pack_namespace) if isinstance(self.input_item, CustomTag) else self.input_item,
            "material": self.material_item.get_reference(pack_namespace) if isinstance(self.material_item, CustomTag) else self.material_item,
            "result": {"id": self.result},
        }

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "CraftingTransmuteRecipe":  # type: ignore[override]
        return cls(
            internal_name,
            result=data["result"].get("id") or data["result"],
            input_item=data["input"],
            material_item=data["material"],
            recipe_category=data.get("recipe_category", "misc"),
        )


@dataclass
class BlastFurnaceRecipe(Recipe):
    ingredient: "MinecraftItem | CustomTag | list[MinecraftItem]"
    experience: int = 1
    cooking_time_ticks: int = 200
    recipe_category: Literal["blocks", "misc"] = "misc"

    recipe_block_name: str = field(init=False, repr=False, default="blast_furnace")

    def __post_init__(self) -> None:
        self.used_ingredients = [self.resolve_ingredient_type(self.ingredient)]

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        data = {
            "type": "minecraft:blasting",
            "ingredient": self.ingredient.get_reference(pack_namespace) if isinstance(self.ingredient, CustomTag) else self.ingredient,
            "result": {
                "id": str(self.result),
            },
            "experience": self.experience,
            "cookingtime": self.cooking_time_ticks,
            "category": self.recipe_category,
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_dict(pack_namespace)  # type: ignore[index, assignment, call-overload]
        return data

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "BlastFurnaceRecipe":  # type: ignore[override]
        return cls(
            internal_name,
            ingredient=data["ingredient"],
            result=cls.result_from_dict(f"{internal_name}_item", data),
            experience=int(data["experience"]),
            cooking_time_ticks=data["cookingtime"],
            recipe_category=data.get("recipe_category", "misc"),
        )


@dataclass
class CampfireRecipe(Recipe):
    ingredient: "MinecraftItem | CustomTag | list[MinecraftItem]"
    experience: int = 1
    cooking_time_ticks: int = 200

    recipe_block_name: str = field(init=False, repr=False, default="campfire")

    def __post_init__(self) -> None:
        self.used_ingredients = [self.resolve_ingredient_type(self.ingredient)]

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        data = {
            "type": "minecraft:campfire_cooking",
            "ingredient": self.ingredient.get_reference(pack_namespace) if isinstance(self.ingredient, CustomTag) else self.ingredient,
            "result": {
                "id": str(self.result),
            },
            "experience": self.experience,
            "cookingtime": self.cooking_time_ticks,
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_dict(pack_namespace)  # type: ignore[index, assignment, call-overload]
        return data

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "CampfireRecipe":  # type: ignore[override]
        return cls(
            internal_name,
            ingredient=data["ingredient"],
            result=cls.result_from_dict(f"{internal_name}_item", data),
            experience=int(data["experience"]),
            cooking_time_ticks=data["cookingtime"],
        )


@dataclass
class FurnaceRecipe(Recipe):
    ingredient: "MinecraftItem | CustomTag | list[MinecraftItem]"
    experience: int = 1
    cooking_time_ticks: int = 200
    recipe_category: Literal["food", "blocks", "misc"] = "misc"

    recipe_block_name: str = field(init=False, repr=False, default="furnace")

    def __post_init__(self) -> None:
        self.used_ingredients = [self.resolve_ingredient_type(self.ingredient)]

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        data = {
            "type": "minecraft:smelting",
            "category": self.recipe_category,
            "ingredient": self.ingredient.get_reference(pack_namespace) if isinstance(self.ingredient, CustomTag) else self.ingredient,
            "result": {
                "id": str(self.result),
            },
            "experience": self.experience,
            "cookingtime": self.cooking_time_ticks,
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_dict(pack_namespace)  # type: ignore[index, assignment, call-overload]
        return data

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "FurnaceRecipe":  # type: ignore[override]
        return cls(
            internal_name,
            ingredient=data["ingredient"],
            result=cls.result_from_dict(f"{internal_name}_item", data),
            experience=int(data["experience"]),
            cooking_time_ticks=data["cookingtime"],
            recipe_category=data.get("recipe_category", "misc"),
        )


@dataclass
class SmithingTransformRecipe(Recipe):
    template_item: "MinecraftItem | CustomTag | list[MinecraftItem]"
    base_item: "MinecraftItem | CustomTag | list[MinecraftItem]"
    addition_item: "MinecraftItem | CustomTag | list[MinecraftItem]"

    recipe_block_name: str = field(init=False, repr=False, default="smithing_table")

    def __post_init__(self) -> None:
        self.used_ingredients = [self.resolve_ingredient_type(x) for x in [self.template_item, self.base_item, self.addition_item]]

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        data = {
            "type": "minecraft:smithing_transform",
            "template": self.template_item.get_reference(pack_namespace) if isinstance(self.template_item, CustomTag) else self.template_item,
            "base":     self.base_item.get_reference(pack_namespace) if isinstance(self.base_item, CustomTag) else self.base_item,  # fmt: skip
            "addition": self.addition_item.get_reference(pack_namespace) if isinstance(self.addition_item, CustomTag) else self.addition_item,
            "result": {
                "id": str(self.result)
            },
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_dict(pack_namespace)  # type: ignore[index, assignment, call-overload]
        return data

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "SmithingTransformRecipe":  # type: ignore[override]
        return cls(
            internal_name,
            template_item=data["template"],
            base_item=data["base"],
            addition_item=data["addition"],
            result=cls.result_from_dict(f"{internal_name}_item", data),
        )


@dataclass
class SmithingTrimRecipe(Recipe):
    template_item: "MinecraftItem | CustomTag | list[MinecraftItem]"
    base_item: "MinecraftItem | CustomTag | list[MinecraftItem]"
    addition_item: "MinecraftItem | CustomTag | list[MinecraftItem]"

    result: "MinecraftItem | CustomTag | list[MinecraftItem]" = field(init=False, repr=False)  # type: ignore[assignment]
    recipe_block_name: str = field(init=False, repr=False, default="smithing_table")

    def __post_init__(self) -> None:
        self.result = self.base_item
        self.used_ingredients = [self.resolve_ingredient_type(x) for x in [self.template_item, self.base_item, self.addition_item]]

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:smithing_trim",
            "template": self.template_item.get_reference(pack_namespace) if isinstance(self.template_item, CustomTag) else self.template_item,
            "base": self.base_item.get_reference(pack_namespace) if isinstance(self.base_item, CustomTag) else self.base_item,
            "addition": self.addition_item.get_reference(pack_namespace) if isinstance(self.addition_item, CustomTag) else self.addition_item,
        }

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "SmithingTrimRecipe":  # type: ignore[override]
        return cls(
            internal_name,
            template_item=data["template"],
            base_item=data["base"],
            addition_item=data["addition"],
        )


@dataclass
class SmokerRecipe(Recipe):
    ingredient: "MinecraftItem | CustomTag | list[MinecraftItem]"
    experience: int = 1
    cooking_time_ticks: int = 200

    recipe_block_name: str = field(init=False, repr=False, default="smoker")

    def __post_init__(self) -> None:
        self.used_ingredients = [self.resolve_ingredient_type(self.ingredient)]

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        data = {
            "type": "minecraft:smoking",
            "category": "food",
            "ingredient": self.ingredient.get_reference(pack_namespace) if isinstance(self.ingredient, CustomTag) else self.ingredient,
            "result": {
                "id": str(self.result),
            },
            "experience": self.experience,
            "cookingtime": self.cooking_time_ticks,
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_dict(pack_namespace)  # type: ignore[index, assignment, call-overload]
        return data

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "SmokerRecipe":  # type: ignore[override]
        return cls(
            internal_name,
            ingredient=data["ingredient"],
            result=cls.result_from_dict(f"{internal_name}_item", data),
            experience=int(data["experience"]),
            cooking_time_ticks=data["cookingtime"],
        )


@dataclass
class StonecutterRecipe(Recipe):
    ingredient: "MinecraftItem | CustomTag | list[MinecraftItem]"
    count: int = 1

    recipe_block_name: str = field(init=False, repr=False, default="stonecutter")

    def __post_init__(self) -> None:
        self.used_ingredients = [self.resolve_ingredient_type(self.ingredient)]

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        data = {
            "type": "minecraft:stonecutting",
            "ingredient": self.ingredient.get_reference(pack_namespace) if isinstance(self.ingredient, CustomTag) else self.ingredient,
            "result": {
                "id": str(self.result),
                "count": self.count,
            }
        }
        if isinstance(self.result, CustomItem):
            data["result"]["components"] = self.result.to_dict(pack_namespace)  # type: ignore[index, call-overload]
        return data

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "StonecutterRecipe":  # type: ignore[override]
        return cls(
            internal_name,
            ingredient=data["ingredient"],
            result=cls.result_from_dict(f"{internal_name}_item", data),
            count=data["result"].get("count", 1),
        )


RECIPE_TYPE_TO_CLASSES: dict[str, type["Recipe"]] = {
    "minecraft:crafting_shaped": ShapedCraftingRecipe,
    "minecraft:crafting_shapeless": ShapelessCraftingRecipe,
    "minecraft:crafting_transmute": CraftingTransmuteRecipe,
    "minecraft:blasting": BlastFurnaceRecipe,
    "minecraft:campfire_cooking": CampfireRecipe,
    "minecraft:smelting": FurnaceRecipe,
    "minecraft:smithing_transform": SmithingTransformRecipe,
    "minecraft:smithing_trim": SmithingTrimRecipe,
    "minecraft:smoking": SmokerRecipe,
    "minecraft:stonecutting": StonecutterRecipe,
}

ALL_RECIPES_TYPES: list[Recipe] = [
    CustomCrafterRecipe, ShapedCraftingRecipe, ShapelessCraftingRecipe, CraftingTransmuteRecipe, FurnaceRecipe, BlastFurnaceRecipe,  # type: ignore[list-item]
    CampfireRecipe, SmithingTransformRecipe, SmithingTrimRecipe, SmokerRecipe, StonecutterRecipe,  # type: ignore[list-item]
]
