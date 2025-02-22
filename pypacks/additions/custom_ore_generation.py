from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pypacks.resources.custom_mcfunction import MCFunction
from pypacks.additions.custom_chunk_scanner import CustomChunkScanner

if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.additions.custom_block import CustomBlock


@dataclass
class CustomOreGeneration:
    """Generates custom ores in the world.
    The chance is 1/chance_of_spawning_in_a_chunk, so entering 2 = 50% chance (1/2),
    entering 5 = 20% chance (1/5), entering 10 = 10% chance (1/10), etc"""
    internal_name: str
    block: "str | CustomBlock"
    chance_of_spawning_in_a_chunk: int = 10

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default=None)  # type: ignore[abc]
    
    # We take a chunk scanner, and when it does new generation, we do our ore bits.
    # We do this by calling "place_ore" many times, and with random deviation

    def create_datapack_files(self, pack: "Pack") -> None:
        self.create_chunk_scanner(pack.namespace).create_datapack_files(pack)

    def create_chunk_scanner(self, pack_namespace: str) -> "CustomChunkScanner":
        return CustomChunkScanner(
            f"{self.internal_name}_ore_generation_chunk_scanner",
            self.create_generate_ore_function(pack_namespace),
        )

    def create_generate_ore_function(self, pack_namespace: str) -> "MCFunction":
        return MCFunction(f"{self.internal_name}_generate_ore", [
            # Only run sometimes
            f"execute store result score random_chance coords run random value 1..{self.chance_of_spawning_in_a_chunk}",
            "execute unless score random_chance coords matches 1 run return fail",
            # Then, generate a random x and z (we exclude the edged lazily because it means we don't get mega clusters and generally stay within chunks.)
            "execute store result score random_x_offset coords run random value 1..14",
            "execute store result score random_y_offset coords run random value 1..14",
            "execute store result score random_z_offset coords run random value 1..14",
            "say Hi"  # Only runs 1/10 of the time!
            # <Spawn all the ore>
        ], ["custom_ore_generation"])
