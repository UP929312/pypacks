from pypacks.resources import *  # noqa: F403
from pypacks.additions.item_components import *  # noqa: F403
# from pypacks.additions import *

# ============================================================================================================

crafting_environment = AllOfEnvironment(
    "crafting_environment",
    definitions=[
        FunctionEnvironment("iron_block_crafting_recipe_environment"),
    ],
)
custom_test_environments: list[CustomTestEnvironment] = [crafting_environment]

# ============================================================================================================

iron_block_crafting_recipe = CustomGameTest(
    "iron_block_crafting_recipe", crafting_environment, GameTestStructure("iron_block_crafting_structure", "structures/iron_block_crafting_recipe.nbt"),
    max_ticks=20, setup_ticks=20,
)
# ======
custom_item = CustomItem("custom_item", "minecraft:emerald")
custom_item_recipe = ShapedCraftingRecipe(
    "custom_item_recipe",
    rows=[
        "ggg",
        "ggg",
        "ggg",
    ],
    keys={"g": "minecraft:green_dye"},
    result=custom_item,
)
custom_item_shaped_crafting_recipe = CustomGameTest(
    "custom_item_shaped_crafting_recipe", crafting_environment, GameTestStructure("custom_item_shaped", "structures/custom_item_shaped.nbt"),
    max_ticks=20, setup_ticks=20,
)
# ======

custom_items = [custom_item]
custom_recipes = [custom_item_recipe]
custom_game_tests = [iron_block_crafting_recipe, custom_item_shaped_crafting_recipe]

# ============================================================================================================
