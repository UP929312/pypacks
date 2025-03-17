from pypacks import Pack, Config
from examples.tests.tests import custom_test_environments, custom_game_tests, custom_items, custom_recipes

import os
os.chdir(os.path.dirname(__file__))


# ============================================================================================================
datapack = Pack(
    name="PyPacks Test Suite",
    description="A datapack holding many tests",
    namespace="pypacks_test_suite",
    world_name="PyPacksWorld",
    custom_items=custom_items,
    custom_recipes=custom_recipes,  # type: ignore
    custom_test_environments=custom_test_environments,
    custom_game_tests=custom_game_tests,
    config=Config(generate_create_wall_command=False, generate_reference_book=False),
)
