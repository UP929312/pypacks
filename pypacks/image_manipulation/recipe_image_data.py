import io
from PIL import Image
from typing import TYPE_CHECKING

from pypacks.utils import IMAGES_PATH
from pypacks.image_manipulation.built_in_resolving import resolve_default_item_image

if TYPE_CHECKING:
    from PIL.Image import Image as ImageType
    from pypacks.resources.custom_item import CustomItem
    from pypacks.resources.custom_recipe import *  # noqa: F403

CoordMappingType = dict[int | str, tuple[int, int]]

crafting_recipe_coords: CoordMappingType = {
    0: (6, 6),
    1: (6+16+3, 6),
    2: (6+16+3+16+2, 6),
    3: (6, 6+16+2),
    4: (6+16+3, 6+16+2),
    5: (6+16+3+16+2, 6+16+2),
    6: (6, 6+16+2+16+2),
    7: (6+16+3, 6+16+2+16+2),
    8: (6+16+3+16+2, 6+16+2+16+2),
    "result": (101, 23),
}

furnace_recipe_coords: CoordMappingType = {
    0: (6, 6),  # Ingredient to smelt
    "result": (65, 23),
}

stonecutter_recipe_coords: CoordMappingType = {
    0: (6, 23),  # Input
    1: (38, 6),  # Result (again)
    "result": (128, 23),
}

campfire_recipe_coords: CoordMappingType = {
    0: (8, 7),
    "result": (67, 25),
}

smithing_recipe_coords: CoordMappingType = {
    0: (8, 40),
    1: (26, 40),
    2: (44, 40),
    "result": (97, 40),
}

# =================================================================================================###################


def place_ingredients_on_image(
    recipe: "Recipe", ingredients: list["str | CustomItem"], coord_mapping: dict[int | str, tuple[int, int]]
) -> "ImageType":
    from pypacks.resources.custom_item import CustomItem
    from pypacks.resources.custom_recipe import SmithingTrimRecipe

    # BASE IMAGE ========================================================
    base_image = Image.open(IMAGES_PATH/"recipe_bases"/f"{recipe.recipe_block_name}.png").convert("RGBA")
    # INGREDIENTS =======================================================
    for i, ingredient in enumerate(ingredients):
        if isinstance(ingredient, CustomItem) or ingredient.removeprefix("minecraft:") not in [" ", "", "air"]:  # For shaped recipes, the " " is a placeholder for nothing, just ignore it
            with Image.open(resolve_default_item_image(ingredient) if not isinstance(ingredient, CustomItem) else ingredient.texture_path) as ingredient_image:  # type: ignore
                ingredient_image = ingredient_image.convert("RGBA").resize((16, 16), resample=Image.NEAREST)
                base_image.paste(ingredient_image, coord_mapping[i], ingredient_image)
    # RESULT ============================================================
    result: "str | CustomItem" = recipe.result if not isinstance(recipe, SmithingTrimRecipe) else recipe.resolve_ingredient_type(recipe.base_item)
    result_texture_path = (
        resolve_default_item_image(result) if not isinstance(result, CustomItem) else (
            result.texture_path if result.texture_path is not None
            else resolve_default_item_image(result.base_item)
        )
    )
    with Image.open(result_texture_path) as result_image:
        result_image = result_image.convert("RGBA").resize((16, 16), resample=Image.NEAREST)
        base_image.paste(result_image, coord_mapping["result"], result_image)
    # ===================================================================
    # Extend bottom bar by 50 additional pixels and fill it in with 0D020F without resizing the image
    # with_text = Image.new("RGBA", (base_image.width, base_image.height+50), color="#0D020F")
    # with_text.paste(base_image, (0, 0))
    # ImageDraw.Draw(with_text).rectangle(xy=(0, with_text.height-50, with_text.width, with_text.height), fill="#0D020F")
    # with_text.show()
    # RETURN
    return base_image


def generate_custom_crafter_recipe_image(recipe: "CustomCrafterRecipe") -> "ImageType":
    return place_ingredients_on_image(
        recipe,
        [recipe.resolve_ingredient_type(ingredient) for ingredient in recipe.ingredients],
        crafting_recipe_coords,
    )


def generate_shapeless_crafting_image(recipe: "ShapelessCraftingRecipe") -> "ImageType":
    return place_ingredients_on_image(
        recipe,
        [recipe.resolve_ingredient_type(ingredient) for ingredient in recipe.ingredients],
        crafting_recipe_coords,
    )


def generate_shaped_crafting_image(recipe: "ShapedCraftingRecipe") -> "ImageType":
    # Need to create a list from the keys and rows, turning "iii", "   "iii" into ["i", "i", "i", " ", " ", "i", "i", "i"]
    ingredients_combined = [ingredient for row in recipe.rows for ingredient in row]
    # Then get all the keys, replacing the ingredients with the keys, and flattening the list
    ingredients_replaced = [recipe.keys.get(ingredient, ingredient) for ingredient in ingredients_combined]
    # The keys sometimes return multiple items, get the first item if it's a list
    return place_ingredients_on_image(
        recipe,
        [recipe.resolve_ingredient_type(x) for x in ingredients_replaced],
        crafting_recipe_coords,
    )


def generate_crafting_transmute_crafting_image(recipe: "CraftingTransmuteRecipe") -> "ImageType":
    return place_ingredients_on_image(
        recipe,
        [recipe.resolve_ingredient_type(recipe.input_item)],
        crafting_recipe_coords,
    )


def generate_furnace_recipe_image(recipe: "FurnaceRecipe | BlastFurnaceRecipe | SmokerRecipe") -> "ImageType":
    return place_ingredients_on_image(
        recipe,
        [recipe.resolve_ingredient_type(recipe.ingredient)],
        furnace_recipe_coords,
    )


def generate_stonecutter_recipe_image(recipe: "StonecutterRecipe") -> "ImageType":
    return place_ingredients_on_image(
        recipe,
        [recipe.resolve_ingredient_type(recipe.ingredient), recipe.resolve_ingredient_type(recipe.result)],
        stonecutter_recipe_coords,
    )


def generate_campfire_recipe_image(recipe: "CampfireRecipe") -> "ImageType":
    return place_ingredients_on_image(
        recipe,
        [recipe.resolve_ingredient_type(recipe.ingredient)],
        campfire_recipe_coords,
    )


def generate_smithing_trim_recipe_image(recipe: "SmithingTrimRecipe") -> "ImageType":
    return place_ingredients_on_image(
        recipe,
        [
            recipe.resolve_ingredient_type(recipe.base_item),
            recipe.resolve_ingredient_type(recipe.addition_item),
            recipe.resolve_ingredient_type(recipe.template_item)
        ],
        smithing_recipe_coords,
    )


def generate_smithing_transform_recipe_image(recipe: "SmithingTransformRecipe") -> "ImageType":
    return place_ingredients_on_image(
        recipe,
        [
            recipe.resolve_ingredient_type(recipe.base_item),
            recipe.resolve_ingredient_type(recipe.addition_item),
            recipe.resolve_ingredient_type(recipe.template_item),
        ],
        smithing_recipe_coords,
    )

# =================================================================================================###################


def generate_recipe_image(recipe: "Recipe") -> bytes:
    from pypacks.resources.custom_recipe import (
        CustomCrafterRecipe, ShapelessCraftingRecipe, ShapedCraftingRecipe, CraftingTransmuteRecipe, FurnaceRecipe, StonecutterRecipe,
        SmokerRecipe, BlastFurnaceRecipe, CampfireRecipe, SmithingTrimRecipe, SmithingTransformRecipe
    )

    class_to_function = {
        CustomCrafterRecipe: generate_custom_crafter_recipe_image,
        ShapedCraftingRecipe: generate_shaped_crafting_image,
        ShapelessCraftingRecipe: generate_shapeless_crafting_image,
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
