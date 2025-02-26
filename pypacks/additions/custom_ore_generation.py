from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pypacks.resources.custom_mcfunction import MCFunction
from pypacks.additions.custom_chunk_scanner import CustomChunkScanner
from pypacks.providers.int_provider import IntRange

if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.additions.custom_block import CustomBlock


RELATIVE_ORE_PLACEMENTS = [
    # First we construct a 2x2 cube
    "~ ~ ~",  "~1 ~ ~",  "~ ~ ~1",  "~1 ~ ~1",
    "~ ~1 ~", "~1 ~1 ~", "~ ~1 ~1", "~1 ~1 ~1",
    # Then we start sprawling out, from 9 blocks - 27 blocks (3x3)
    "~ ~ ~2",  "~1 ~ ~2",  "~2 ~ ~",  "~2 ~ ~1", "~2 ~ ~2",
    "~ ~1 ~2", "~1 ~1 ~2", "~2 ~1 ~", "~2 ~1 ~1","~2 ~1 ~2",
    # The third layer, 3x3
    "~ ~2 ~", "~ ~2 ~1", "~ ~2 ~2", "~1 ~2 ~","~1 ~2 ~1", "~1 ~2 ~1", "~2 ~2 ~", "~2 ~2 ~1","~2 ~2 ~2",
]



@dataclass
class CustomOreGeneration:
    """Generates custom ores in the world.
    The chance is 1/chance_of_spawning_in_a_chunk, so entering 2 = 50% chance (1/2),
    entering 5 = 20% chance (1/5), entering 10 = 10% chance (1/10), etc"""
    internal_name: str
    block: "CustomBlock"
    chance_of_spawning_in_a_chunk: int = 16   # 1 in 16 chance
    # depth
    ore_vein_size: "IntRange" = field(default_factory=lambda: IntRange(1, 7))

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default=None)  # type: ignore[assignment]

    # We take a chunk scanner, and when it does new generation, we do our ore bits.
    # We do this by calling "place_ore" many times, and with random deviation

    def create_datapack_files(self, pack: "Pack") -> None:
        ...  # self.create_chunk_scanner(pack.namespace).create_datapack_files(pack)

    def create_chunk_scanner(self, pack_namespace: str) -> "CustomChunkScanner":
        return CustomChunkScanner(
            f"{self.internal_name}_ore_generation_chunk_scanner",
            self.create_generate_ore_function(pack_namespace),
        )

    @staticmethod
    def create_ore_vein_function(pack_namespace: str) -> tuple["MCFunction", "MCFunction"]:
        # We need to run the ore spreader *at* a certain location.
        # spread_vein = MCFunction("spread_vein", [
        #     f"$say Spreading! $(place_ore_function)",
        #     "# Check if we've reached the ore vein size",
        #     f"execute if score ore_vein_size inputs matches 0 run say Ore Vein Size Finished",
        #     f"execute if score ore_vein_size inputs matches 0 run return fail",
        #     "",
        #     "# Reduce the vein size counter",
        #     f"scoreboard players remove ore_vein_size inputs 1",
        #     "",
        #     "# Place an ore block by calling a separate function",
        #     f"say About to run the place function",
        #     "$execute positioned ~ ~ ~ run function $(place_ore_function)",
        #     "",
        #     "# Generate a random direction to grow into",
        #     f"# About to pick a random direction",
        #     f"execute store result score random_direction inputs run random value 1..6",
        #     f"# Spreading into",
        #     "# Randomly spread in different directions (6 possible faces, forward, back, left, right, up, down)",
        #     f"$execute if score random_direction inputs matches 1 run execute positioned ~1 ~ ~ run function {pack_namespace}:custom_ore_generation/spread_vein {{\"place_ore_function\": \"$(place_ore_function)\"}}",
        #     f"$execute if score random_direction inputs matches 2 run execute positioned ~-1 ~ ~ run function {pack_namespace}:custom_ore_generation/spread_vein {{\"place_ore_function\": \"$(place_ore_function)\"}}",
        #     f"$execute if score random_direction inputs matches 3 run execute positioned ~ ~1 ~ run function {pack_namespace}:custom_ore_generation/spread_vein {{\"place_ore_function\": \"$(place_ore_function)\"}}",
        #     f"$execute if score random_direction inputs matches 4 run execute positioned ~ ~-1 ~ run function {pack_namespace}:custom_ore_generation/spread_vein {{\"place_ore_function\": \"$(place_ore_function)\"}}",
        #     f"$execute if score random_direction inputs matches 5 run execute positioned ~ ~ ~1 run function {pack_namespace}:custom_ore_generation/spread_vein {{\"place_ore_function\": \"$(place_ore_function)\"}}",
        #     f"$execute if score random_direction inputs matches 6 run execute positioned ~ ~ ~-1 run function {pack_namespace}:custom_ore_generation/spread_vein {{\"place_ore_function\": \"$(place_ore_function)\"}}",
        # ], ["custom_ore_generation"])
        spread_vein = MCFunction("spread_vein", [
            f"$say Spreading! $(place_ore_function) ($(vein_min_size)-$(vein_max_size))",
            f"$execute store result score vein_size inputs run random value $(vein_min_size)..$(vein_max_size)",
            'tellraw @a [{"text": "Randomly generated number: "}, {"score":{"name":"vein_size","objective":"inputs"}}]',
            *[
                f"execute if score vein_size inputs matches {i}.. run say Number was bigger than {i}, so running at {relative_coords}"
                for i, relative_coords in enumerate(RELATIVE_ORE_PLACEMENTS, 1)
            ],  
            *[
                f"$execute if score vein_size inputs matches {i}.. run execute positioned {relative_coords} run function $(place_ore_function)"
                for i, relative_coords in enumerate(RELATIVE_ORE_PLACEMENTS, 1)
            ],
        ], ["custom_ore_generation"])

        intermediate = MCFunction("intermediate", [
                f"say In the intermediate function!",
                f"$execute positioned $(x) $(y) $(z) run function {spread_vein.get_reference(pack_namespace)} {{\"place_ore_function\": \"$(place_ore_function)\", \"vein_min_size\": \"$(vein_min_size)\", \"vein_max_size\": \"$(vein_max_size)\"}}",
            ], ["custom_ore_generation"]
        )
        return spread_vein, intermediate

    def create_generate_ore_function(self, pack_namespace: str) -> "MCFunction":
        """The function which has x, y, and z macros of the chunk corner"""
        place_function = self.block.generate_place_function(pack_namespace).get_reference(pack_namespace)
        spread_ore_function = self.create_ore_vein_function(pack_namespace)[1].get_reference(pack_namespace)
        return MCFunction(f"{self.internal_name}_generate_ore", [
            f"execute store result score random_chance coords run random value 1..{self.chance_of_spawning_in_a_chunk}",
            "execute unless score random_chance coords matches 1 run return fail",
            "# Then, generate a random x and z (we exclude the edged lazily because it means we don't get mega clusters and generally stay within chunks.)",
            "execute store result score random_x_offset coords run random value 1..14",
            "execute store result score random_y_offset coords run random value 1..14",
            "execute store result score random_z_offset coords run random value 1..14",
            "# Increase the x, y and z component by the random offsets",
            "$scoreboard players set ore_origin_x coords $(x)",
            "$scoreboard players set ore_origin_y coords $(y)",
            "$scoreboard players set ore_origin_z coords $(z)",
            "scoreboard players operation ore_origin_x coords += random_x_offset coords",
            "scoreboard players operation ore_origin_y coords += random_y_offset coords",
            "scoreboard players operation ore_origin_z coords += random_z_offset coords",
            f"# Then compile them into a object and run all the create ore functions",
            f"execute store result storage {pack_namespace}:ore_generation_macros data.x int 1 run scoreboard players get ore_origin_x coords",
            f"execute store result storage {pack_namespace}:ore_generation_macros data.y int 1 run scoreboard players get ore_origin_y coords",
            f"execute store result storage {pack_namespace}:ore_generation_macros data.z int 1 run scoreboard players get ore_origin_z coords",
            f"data modify storage {pack_namespace}:ore_generation_macros data.vein_min_size set value {self.ore_vein_size.min}",
            f"data modify storage {pack_namespace}:ore_generation_macros data.vein_max_size set value {self.ore_vein_size.max}",
            f"data modify storage {pack_namespace}:ore_generation_macros data.place_ore_function set value \"{place_function}\"",
            "say About to run ore generation!",
            # f"function {spread_ore_function} with storage {pack_namespace}:ore_generation_macros data",  # Passes in the function, and x, y, z
        ], ["custom_ore_generation"])
