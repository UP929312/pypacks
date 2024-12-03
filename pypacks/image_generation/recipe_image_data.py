from PIL import Image
from typing import TYPE_CHECKING

from pypacks.utils import PYPACKS_ROOT

if TYPE_CHECKING:
    from pypacks.resources.custom_recipe import *

shapeless_crafting_recipe = {
    0: (5, 5),
    1: (20, 5),
    2: (35, 5),
    3: (5, 50),
    4: (20, 50),
    5: (35, 50),
    "result": (20, 20),
}

def generate_crafting_image(recipe: "ShapedCraftingRecipe | ShapelessCraftingRecipe") -> bytes:
    # Load the image from /assets/images/recipes/crafting_3_x_3.png
    image = Image.open(f"{PYPACKS_ROOT}/assets/images/recipes/crafting_3_x_3.png").convert("RGBA")
    # Load the item images
    return b""