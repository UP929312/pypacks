from typing import TYPE_CHECKING

from pypacks.resources.custom_mcfunction import MCFunction

if TYPE_CHECKING:
    from pypacks.pack import Pack


# This is a simple raycasting system that can be used to detect blocks in a line of sight.
# It takes 4 inputs, the hit block function, the failed function, the ray transitive blocks,
# and if the we should check if the ray_transitive_blocks is present or absent.
# An example of this is:
# {
#     "hit_block_function": f"{pack_namespace}:raycast/hit_block",
#     "failed_function": f"{pack_namespace}:raycast/failed",
#     "ray_transitive_blocks": "#minecraft:replaceable",
#     "if_or_unless": "unless",
# }
# Which runs the default raycast/hit_block, the default raycast/failed, a list of blocks which can be passed though
# And also that we should end the ray unless we hit one of the blocks.
# If we set it to "if", we will stop the ray "if" we hit a block.


def generate_default_raycasting_functions(pack_namespace: str) -> tuple[MCFunction, ...]:
    DEBUG_RAYCASTING = False
    arguments = {
        "hit_block_function": f"{pack_namespace}:raycast/hit_block",
        "failed_function": f"{pack_namespace}:raycast/failed",
        "ray_transitive_blocks": "#minecraft:replaceable",
        "if_or_unless": "unless",
    }
    formatted_arguments = "{" + ", ".join([f"\"{key}\": \"{value}\"" for key, value in arguments.items()]) + "}"
    arguments_replacements = {key: f"$({key})" for key in arguments}
    formatted_arguments_replacements = "{" + ", ".join([f"\"{key}\": \"{value}\"" for key, value in arguments_replacements.items()]) + "}"

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

    hit_block_default = MCFunction("hit_block", [
        "# Running custom commands since the block was found",
        "setblock ~ ~ ~ minecraft:stone",
        ],
        ["raycast"],
    )

    # This exists as an intermediate to set the scoreboard value *and then* calling the function, otherwise overriding it requires the scoreboard line.
    hit_block_set_score = MCFunction("hit_block_set_score", [
        "# Mark the ray as having found a block",
        "scoreboard players set #hit raycast 1",
        "$function $(hit_block_function)",  # Call the hit block function
        ],
        ["raycast"],
    )

    ray = MCFunction("ray", [
        "# Run a function if a block was detected",
        f"$execute $(if_or_unless) block ~ ~ ~ $(ray_transitive_blocks) run function {hit_block_set_score.get_reference(pack_namespace)} {{\"hit_block_function\": \"$(hit_block_function)\"}}",
        "",
        "# Add one distance to the ray",
        "scoreboard players add #distance raycast 1",
        "",
        "# Added: Particle for debugging",
        f"{'' if DEBUG_RAYCASTING else '# '}particle minecraft:cloud ~ ~ ~",
        "",
        "# If the raycast failed, run the failed function",
        "$execute if score #hit raycast matches 0 if score #distance raycast matches 551.. run function $(failed_function)",
        "",
        "# Advance forward and run the ray again if no block was found",
        f"$execute if score #hit raycast matches 0 if score #distance raycast matches ..550 positioned ^ ^ ^0.01 run function {pack_namespace}:raycast/ray {formatted_arguments_replacements}",
        ],
        ["raycast"],
    )

    # This exists so we don't have to have everything in start_ray duplicated, as an interface, almost.
    populate_start_ray = MCFunction("populate_start_ray", [
        f"function {pack_namespace}:raycast/start_ray {formatted_arguments}",
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
        f"$execute positioned ~ ~1.62 ~ run function {pack_namespace}:raycast/ray {formatted_arguments_replacements}",
        "",
        "# Raycasting finished, removing tag from the raycaster.",
        "tag @s remove is_raycasting",
        ],
        ["raycast"],
    )
    return failed, load_ray, hit_block_default, hit_block_set_score, ray, populate_start_ray, start_ray
