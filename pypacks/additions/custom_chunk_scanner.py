from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pypacks.resources.custom_mcfunction import MCFunction
from pypacks.resources.custom_tag import CustomTag
from pypacks.additions.custom_loop import CustomLoop

if TYPE_CHECKING:
    from pypacks.pack import Pack


@dataclass
class CustomChunkScanner:
    """A Custom Chunk Scanner.
    This allows you to run functions once per chunk (i.e. on generation), useful for ore generation, custom structures, block replacements, etc.
    The function is ran with three macros, `x`, `y`, and `z`, which are the chunk corner coordinates (smallest x and z). y is set to -64."""
    internal_name: str
    function_to_run: "MCFunction"

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default=None)  # type: ignore[assignment]

    def create_datapack_files(self, pack: "Pack") -> None:
        return CustomTag(
            "chunk_scanner_functions",
            [
                chunk_scanner.function_to_run.get_reference(pack.namespace)
                for chunk_scanner in pack.custom_chunk_scanners
            ],
            "function",
        ).create_datapack_files(pack)

    @staticmethod
    def generate_check_chunk_loop(pack_namespace: str) -> "CustomLoop":
        """Generates a function that checks all the chunks around the player."""
        checked_function = CustomChunkScanner.generate_mark_and_call_function(pack_namespace).get_reference(pack_namespace)

        check_chunks = MCFunction("check_chunks_loop", [
            # First, we get the players position:
            "execute as @a run execute store result score x_coord coords run data get entity @s Pos[0] 1",  # Stores their x into obj "coords" | player "x_coord"
            "execute as @a run execute store result score z_coord coords run data get entity @s Pos[2] 1",  # Stores their z into obj "coords" | player "z_coord"
            # Secondly, get the relative 0, 0 chunk coordinates (this can be compacted, but I like the clarity):
            "scoreboard players operation chunk_offset_x coords = x_coord coords",
            "scoreboard players operation chunk_offset_x coords %= 16 constants",
            "scoreboard players operation chunk_edge_x coords = x_coord coords",
            "scoreboard players operation chunk_edge_x coords -= chunk_offset_x coords",  # This is the x coord of the corner of their chunk
            "scoreboard players operation chunk_offset_z coords = z_coord coords",
            "scoreboard players operation chunk_offset_z coords %= 16 constants",
            "scoreboard players operation chunk_edge_z coords = z_coord coords",
            "scoreboard players operation chunk_edge_z coords -= chunk_offset_z coords",  # This is the z coord of the corner of their chunk
            "",
            "scoreboard players set y inputs 100",  # TODO: change to -64 or 0 or something
            "",
            *[
                # Thirdly, with the chunk corner, we want to try in the 8 adjacent chunk corners
                "\n" +
                "scoreboard players operation x inputs = chunk_edge_x coords\n" +
                "scoreboard players operation z inputs = chunk_edge_z coords\n" +
                (f"scoreboard players {'add' if x >= 0 else 'remove'} x inputs {abs(x)}\n" if x != 0 else "") +
                (f"scoreboard players {'add' if z >= 0 else 'remove'} z inputs {abs(z)}\n" if z != 0 else "") +
                f"execute store result storage {pack_namespace}:chunk_scanner_macros pos.x int 1 run scoreboard players get x inputs\n" +
                f"execute store result storage {pack_namespace}:chunk_scanner_macros pos.y int 1 run scoreboard players get y inputs\n" +
                f"execute store result storage {pack_namespace}:chunk_scanner_macros pos.z int 1 run scoreboard players get z inputs\n" +
                f"function {checked_function} with storage {pack_namespace}:chunk_scanner_macros pos\n"
                for x in [-16, 0, 16] for z in [-16, 0, 16] if (x, z) != (0, 0)
            ],
        ], ["custom_chunk_scanning"])
        return CustomLoop("check_chunks_loop", 1 * 20, check_chunks)

    @staticmethod
    def generate_mark_and_call_function(pack_namespace: str) -> MCFunction:
        return MCFunction("mark_and_call", [
            # Firstly, check if the chunk has already been processed, if so, skip it
            "$execute positioned $(x) $(y) $(z) if entity @e[type=item_display, tag=world_marker, distance=..0.5] run return fail",  # unless loaded ~ ~ ~
            # Secondly, spawn the marker, so we know that chunk has been processed.
            "$summon item_display $(x) $(y) $(z) {Tags:[\"world_marker\"]}",
            "$summon pig $(x) $(y) $(z) {NoAI:1b, NoGravity: 1b, Silent: 1b, Tags:[\"world_marker\"]}",
            # Thirdly, call all the functions with the args
            f"$function #{pack_namespace}:chunk_scanner_functions {{\"x\": $(x), \"y\": $(y), \"z\": $(z)}}",
        ], ["custom_chunk_scanning"])
