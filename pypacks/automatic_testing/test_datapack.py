from pypacks import Datapack  # type: ignore[attr-defined]
from pypacks.resources.custom_recipe import FurnaceRecipe
# ============================================================================================================
# Custom recipes
feather_to_string_recipe = FurnaceRecipe("feather_to_string_recipe", "minecraft:feather", "minecraft:string", 1, 20)
recipes = [feather_to_string_recipe]

world_name = "PyPacksWorld"
datapack_name = "PyPacks Tests"
namespace = "pypacks_tests"

datapack = Datapack(
    datapack_name, "The testing framework datapack", namespace, world_name=world_name,
    custom_recipes=recipes,  # type: ignore[arg-type]
)
