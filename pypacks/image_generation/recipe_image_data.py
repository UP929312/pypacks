import io
from PIL import Image
from typing import TYPE_CHECKING

from pypacks.utils import PYPACKS_ROOT, resolve_default_item_image

if TYPE_CHECKING:
    from pypacks.resources.custom_recipe import *

crafting_recipe = {
    0: (2, 2),
    1: (2+16+3, 2),
    2: (2+16+3+16+2, 2),
    3: (2, 2+16+2),
    4: (2+16+3, 2+16+2),
    5: (2+16+3+16+2, 2+16+2),
    6: (2, 2+16+2+16+2),
    7: (2+16+3, 2+16+2+16+2),
    8: (2+16+3+16+2, 2+16+2+16+2),
    "result": (97, 19),
}

def generate_crafting_image(recipe: "ShapedCraftingRecipe | ShapelessCraftingRecipe") -> bytes:
    from pypacks.resources.custom_recipe import ShapedCraftingRecipe, ShapelessCraftingRecipe
    from pypacks.resources.custom_item import CustomItem
    # BASE
    base_image = Image.open(f"{PYPACKS_ROOT}/assets/images/recipes/crafting_3_x_3.png").convert("RGBA")
    # RESULT
    result_texture_path = (
        resolve_default_item_image(recipe.result) if not isinstance(recipe.result, CustomItem) else (
        recipe.result.texture_path if recipe.result.texture_path is not None
        else resolve_default_item_image(recipe.result.base_item))  # type: ignore
    )
    with Image.open(result_texture_path) as result_image:  # type: ignore[abc]
        result_image = result_image.convert("RGBA")
        base_image.paste(result_image, crafting_recipe["result"], result_image)
    # recipe.ingredients = [recipe.ingredients[1]]*9
    # INGREDIENTS
    if isinstance(recipe, ShapelessCraftingRecipe):
        first_ingredients = [ingredient[0] if isinstance(ingredient, list) else ingredient for ingredient in recipe.ingredients]
        for i, ingredient in enumerate(first_ingredients):
            with Image.open(resolve_default_item_image(ingredient)) as ingredient_image:
                ingredient_image = ingredient_image.convert("RGBA")
                base_image.paste(ingredient_image, crafting_recipe[i], ingredient_image)
    # RETURN (CONVERT TO BYTES)
    # base_image.show()
    img_byte_arr = io.BytesIO()
    base_image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr
