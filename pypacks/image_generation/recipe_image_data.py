import io
from PIL import Image
from typing import TYPE_CHECKING

from pypacks.utils import IMAGES_PATH, resolve_default_item_image

if TYPE_CHECKING:
    from PIL.Image import Image as ImageType
    from pypacks.resources.custom_item import CustomItem
    from pypacks.resources.custom_recipe import *

CoordMappingType = dict[int | str, tuple[int, int]]

crafting_recipe_coords: CoordMappingType = {
    0: (2, 2),
    1: (2+16+3, 2),
    2: (2+16+3+16+2, 2),
    3: (2, 2+16+2),
    4: (2+16+3, 2+16+2),
    5: (2+16+3+16+2, 2+16+2),
    6: (2, 2+16+2+16+2),
    7: (2+16+3, 2+16+2+16+2),
    8: (2+16+3+16+2, 2+16+2+16+2),
    "result": (96, 19),
}

furnace_recipe_coords: CoordMappingType = {
    0: (3, 3),
    1: (3, 3),
    "result": (62, 20),
}

stonecutter_recipe_coords: CoordMappingType = {
    0: (3, 21),
    1: (35, 4),
    "result": (125, 20),
}

campfire_recipe_coords: CoordMappingType = {
    0: (3, 3),
    "result": (62, 20),
}

smithing_recipe_coords: CoordMappingType = {
    0: (8, 48),
    1: (26, 48),
    2: (44, 48),
    "result": (97, 48),
}

# =================================================================================================###################

def place_ingredients_on_image(
    recipe: "Recipe", ingredients: list[str], result: "str | CustomItem", coord_mapping: dict[int | str, tuple[int, int]]
) -> "ImageType":
    from pypacks.resources.custom_item import CustomItem

    # BASE
    base_image = Image.open(f"{IMAGES_PATH}/recipe_bases/{recipe.recipe_block_name}.png").convert("RGBA")
    # INGREDIENTS
    for i, ingredient in enumerate(ingredients):
        with Image.open(resolve_default_item_image(ingredient) if not isinstance(ingredient, CustomItem) else ingredient.texture_path) as ingredient_image:  # type: ignore
            ingredient_image = ingredient_image.convert("RGBA")
            base_image.paste(ingredient_image, coord_mapping[i], ingredient_image)
    # RESULT
    result_texture_path = (
        resolve_default_item_image(result) if not isinstance(result, CustomItem) else (
        result.texture_path if result.texture_path is not None
        else resolve_default_item_image(result.base_item))
    )
    with Image.open(result_texture_path) as result_image:
        result_image = result_image.convert("RGBA")
        base_image.paste(result_image, coord_mapping["result"], result_image)
    # RETURN
    return base_image


def generate_shapeless_crafting_image(recipe: "ShapelessCraftingRecipe") -> "ImageType":
    return place_ingredients_on_image(
        recipe,
        [ingredient[0] if isinstance(ingredient, list) else ingredient for ingredient in recipe.ingredients],
        recipe.result,
        crafting_recipe_coords,
    )

def generate_shaped_crafting_image(recipe: "ShapedCraftingRecipe") -> "ImageType":
    # Need to create a list from the keys and rows, turning "iii", "   "iii" into ["i", "i", "i", " ", " ", "i", "i", "i"]
    ingredients_combined = [ingredient for row in recipe.rows for ingredient in row]
    # Then get all the keys, replacing the ingredients with the keys, and flattening the list
    ingredients_replaced = [recipe.keys.get(ingredient, ingredient) for ingredient in ingredients_combined]
    # The keys sometimes return multiple items, get the first item if it's a list
    ingredients_flattened = [x[0] if isinstance(x, list) else x for x in ingredients_replaced]
    return place_ingredients_on_image(
        recipe,
        ingredients_flattened,
        recipe.result,
        crafting_recipe_coords,
    )

def generate_crafting_transmute_crafting_image(recipe: "CraftingTransmuteRecipe") -> "ImageType":
    return place_ingredients_on_image(
        recipe,
        [recipe.input_item[0] if isinstance(recipe.input_item, list) else recipe.input_item, recipe.material_item],
        recipe.result,
        crafting_recipe_coords,
    )

def generate_furnace_recipe_image(recipe: "FurnaceRecipe | BlastFurnaceRecipe | SmokerRecipe") -> "ImageType":
    return place_ingredients_on_image(
        recipe,
        [recipe.ingredient],
        recipe.result,
        furnace_recipe_coords,
    )

def generate_stonecutter_recipe_image(recipe: "StonecutterRecipe") -> "ImageType":
    return place_ingredients_on_image(
        recipe,
        [recipe.ingredient, recipe.result],  #type: ignore
        recipe.result,
        stonecutter_recipe_coords,
    )

def generate_campfire_recipe_image(recipe: "CampfireRecipe") -> "ImageType":
    return place_ingredients_on_image(
        recipe,
        [recipe.ingredient],
        recipe.result,
        campfire_recipe_coords,
    )

def generate_smithing_trim_recipe_image(recipe: "SmithingTrimRecipe") -> "ImageType":
    return place_ingredients_on_image(
        recipe,
        [recipe.base_item, recipe.addition_item, recipe.template_item],
        recipe.base_item,
        smithing_recipe_coords,
    )

def generate_smithing_transform_recipe_image(recipe: "SmithingTransformRecipe") -> "ImageType":
    return place_ingredients_on_image(
        recipe,
        [recipe.base_item, recipe.addition_item, recipe.template_item],
        recipe.result,
        smithing_recipe_coords,
    )

# =================================================================================================###################


def generate_recipe_image(recipe: "Recipe") -> bytes:
    from pypacks.resources.custom_recipe import (
        ShapedCraftingRecipe, ShapelessCraftingRecipe, CraftingTransmuteRecipe, FurnaceRecipe, StonecutterRecipe,
        SmokerRecipe, BlastFurnaceRecipe, CampfireRecipe, SmithingTrimRecipe, SmithingTransformRecipe
    )

    class_to_function = {
        ShapelessCraftingRecipe: generate_shapeless_crafting_image,
        ShapedCraftingRecipe: generate_shaped_crafting_image,
        CraftingTransmuteRecipe: generate_crafting_transmute_crafting_image,

        FurnaceRecipe: generate_furnace_recipe_image,
        SmokerRecipe: generate_furnace_recipe_image,
        BlastFurnaceRecipe: generate_furnace_recipe_image,

        StonecutterRecipe: generate_stonecutter_recipe_image,
        CampfireRecipe: generate_campfire_recipe_image,

        SmithingTrimRecipe: generate_smithing_trim_recipe_image,
        SmithingTransformRecipe: generate_smithing_transform_recipe_image,
    }
    function = class_to_function[type(recipe)]
    image = function(recipe)  # type: ignore[operator]

    # RETURN (CONVERT TO BYTES)
    # image.show()
    img_bytes_io_arr = io.BytesIO()
    image.save(img_bytes_io_arr, format='PNG')
    img_byte_arr = img_bytes_io_arr.getvalue()
    return img_byte_arr
