from dataclasses import dataclass

from pypacks.templates.recipe_templates import (
    furnace_recipe_template, shapeless_recipe_template, shaped_recipe_template, smoker_recipe_template,
)


@dataclass
class ShapelessCraftingRecipe:
    name: str
    ingredients: list[list[str] | str]
    # Ingredients can either be a list of Items (i.e. a flint and iron ingot makes a flint and steel), or a list of lists,
    # which allows you to put multiple items in, e.g. making a chest from all the types of wood.
    result: str
    amount: int = 1

    def to_file_contents(self) -> str:
        return shapeless_recipe_template(self.ingredients, self.result, self.amount)


@dataclass
class ShapedCraftingRecipe:
    name: str
    rows: list[str]
    keys: dict[str, list[str] | str]
    result: str
    amount: int = 1

    def to_file_contents(self) -> str:
        assert 0 < len(self.rows) <= 3, "Rows must be a list of 1-3 strings"
        row_1 = self.rows[0]
        row_2 = self.rows[1] if len(self.rows) >= 2 else None
        row_3 = self.rows[2] if len(self.rows) == 3 else None
        removed_nones = [x for x in [row_1, row_2, row_3] if x is not None]
        return shaped_recipe_template(removed_nones, self.keys, self.result, self.amount)


@dataclass
class StoneCutterRecipe:
    pass


@dataclass
class FurnaceRecipe:
    name: str
    ingredient: str
    result: str
    experience: int | None = 1
    cooking_time_ticks: int = 200

    def to_file_contents(self) -> str:
        return furnace_recipe_template(self.ingredient, self.result, self.experience, self.cooking_time_ticks)


@dataclass
class SmokerRecipe:
    name: str
    ingredient: str
    result: str
    experience: int | None = 1
    cooking_time_ticks: int = 200

    def to_file_contents(self) -> str:
        return smoker_recipe_template(self.ingredient, self.result, self.experience, self.cooking_time_ticks)