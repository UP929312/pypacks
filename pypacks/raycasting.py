from typing import TYPE_CHECKING

from pypacks.resources.mcfunction import MCFunction
from pypacks.resources.custom_tag import CustomTag

if TYPE_CHECKING:
    from pypacks.datapack import Datapack

def generate_raycasting_functions(datapack: "Datapack") -> tuple[MCFunction, ...]:
    arguments = {
        "hit_block_function": f"{datapack.namespace}:raycast/hit_block",
        "failed_function": f"{datapack.namespace}:raycast/failed",
        "ray_transitive_blocks": f"#{datapack.namespace}:ray_transitive_blocks",
    }
    formatted_arguments = "{" +", ".join([f"\"{key}\": \"{value}\"" for key, value in arguments.items()]) + "}"
    arguments_replacements = {
        "hit_block_function": f"$(hit_block_function)",
        "failed_function": f"$(failed_function)",
        "ray_transitive_blocks": f"$(ray_transitive_blocks)",
    }
    formatted_arguments_replacements = "{" +", ".join([f"\"{key}\": \"{value}\"" for key, value in arguments_replacements.items()]) + "}"

    failed = MCFunction("failed", [
        "# Commands to run when the raycast has failed to detect a block",
        "say Ray casting failed, oops!",
        ],
        ["raycast"],
    )

    load_ray = MCFunction("load", [
        "scoreboard objectives add raycast dummy",
        ],
        ["raycast"],
    )

    hit_block = MCFunction("hit_block", [
        "# Mark the ray as having found a block",
        "scoreboard players set #hit raycast 1",
        "",
        "# Running custom commands since the block was found",
        "setblock ~ ~ ~ minecraft:stone",
        ],
        ["raycast"],
    )

    ray = MCFunction("ray", [
        "# Run a function if a block was detected",
        f"$execute unless block ~ ~ ~ $(ray_transitive_blocks) run function $(hit_block_function)",
        "",
        "# Add one distance to the ray",
        "scoreboard players add #distance raycast 1",
        "",
        "# Added: Particle for debugging",
        "# particle minecraft:cloud ~ ~ ~",
        "",
        "# If the raycast failed, run the failed function",
        f"$execute if score #hit raycast matches 0 if score #distance raycast matches 551.. run function $(failed_function)",
        "",
        "# Advance forward and run the ray again if no block was found",
        f"$execute if score #hit raycast matches 0 if score #distance raycast matches ..550 positioned ^ ^ ^0.01 run function {datapack.namespace}:raycast/ray {formatted_arguments_replacements}",
        ],
        ["raycast"],
    )

    # Change start ray to take an input too, so we don't have to pass it *all* in everytime.
    populate_start_ray = MCFunction("populate_start_ray", [
        f"function {datapack.namespace}:raycast/start_ray {formatted_arguments}",
        ],
        ["raycast"],
    )

    start_ray = MCFunction("start_ray", [
        "# Setting up the raycasting data.",
        "tag @s add is_raycasting",
        "scoreboard players set #hit raycast 0",
        "scoreboard players set #distance raycast 0",
        "",
        "# Play a debug sound:",
        "playsound minecraft:ui.button.click block @s ~ ~ ~",
        "",
        "# Activating the raycast. This function will call itself until it is done (at height of player - 1.62 blocks high)",
        f"$execute positioned ~ ~1.62 ~ run function {datapack.namespace}:raycast/ray {formatted_arguments_replacements}",
        "",
        "# Raycasting finished, removing tag from the raycaster.",
        "tag @s remove is_raycasting",
        ],
        ["raycast"],
    )
    return failed, hit_block, load_ray, ray, populate_start_ray, start_ray

def generate_place_functions(datapack: "Datapack") -> tuple[MCFunction, ...]:
    return ()

raycast_transitive_blocks = [
    "minecraft:air",
    "minecraft:water",
    "minecraft:lava",
    "minecraft:short_grass",
    "minecraft:fern",
    "minecraft:dead_bush",
    "minecraft:seagrass",
    "minecraft:tall_seagrass",
    "minecraft:fire",
    "minecraft:soul_fire",
    "minecraft:snow",
    "minecraft:vine",
    "minecraft:glow_lichen",
    "minecraft:resin_clump",
    "minecraft:light",
    "minecraft:tall_grass",
    "minecraft:large_fern",
    "minecraft:structure_void",
    "minecraft:void_air",
    "minecraft:cave_air",
    "minecraft:bubble_column",
    "minecraft:warped_roots",
    "minecraft:nether_sprouts",
    "minecraft:crimson_roots",
    "minecraft:hanging_roots",
]

ray_transitive_blocks_tag = CustomTag("ray_transitive_blocks", ["block"], raycast_transitive_blocks)
