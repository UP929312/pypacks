from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.resources.custom_mcfunction import MCFunction

# This is a simple raycasting system that can be used to detect blocks in a line of sight.
# It takes 4 inputs, the hit block commaand, the failed command (no blocks in the limit), the ray traversable blocks,
# and if the we should check if the ray_traversable_blocks is present or absent (end if we find a block, or if we don't).
# An example of this is:
# raycast = RayCast(
#     on_block_hit_command="setblock ~ ~ ~ minecraft:stone",
#     no_blocks_hit_command="say No blocks hit!",
#     blocks_to_detect="#minecraft:replaceable",
#     if_or_unless="unless",
# )
# (This will set a stone block where the ray hits, and say "No blocks hit!" if the ray doesn't hit anything)



@dataclass
class BlockRaycast:
    internal_name: str
    on_block_hit_command: str = "setblock ~ ~ ~ minecraft:gold_block"
    no_blocks_hit_command: str = "say No blocks hit!"
    blocks_to_detect: str = "#minecraft:replaceable"  # Blocks the ray can pass through, e.g. #minecraft:replaceable (air, short grass, etc)
    if_or_unless: str = "unless"  # If set to "if", the ray will stop if it hits a block, if set to "unless", the ray will stop if it doesn't hit a block
    # particle_at_ray: bool = False
    # space_between_iterations: float = 0.01  # The space between each ray iteration
    # max_distance: int = 550  # The maximum distance the ray can travel

    datapack_subdirectory_name: str = field(default="function/raycast", init=False, repr=False, hash=False)

    @staticmethod
    def generate_default_raycast_functions(pack_namespace: str) -> tuple["MCFunction", ...]:
        from pypacks.resources.custom_mcfunction import MCFunction  # Avoid circular import

        arguments = ["hit_block_command", "failed_command", "ray_traversable_blocks", "if_or_unless"]
        arguments_replacements = {key: f"$({key})" for key in arguments}
        formatted_arguments_replacements = "{" + ", ".join([f"\"{key}\": \"{value}\"" for key, value in arguments_replacements.items()]) + "}"
        # DEBUG_RAYCASTING = False

        load_ray = MCFunction("load", [
            "scoreboard objectives add raycast dummy",
            ],
            ["raycast"],
        )

        # This exists as an intermediate to set the scoreboard value *and then* calling the function, otherwise overriding it requires the scoreboard line.
        hit_block_set_score = MCFunction("hit_block_set_score", [
            "# Mark the ray as having found a block/entity",
            "scoreboard players set #hit raycast 1",
            "$$(hit_block_command)",  # Call the hit block function
            ],
            ["raycast"],
        )

        # Each Ray iteration
        ray = MCFunction("block_ray", [
            "# Requires the following macros when calling: hit_block_command, failed_command, ray_traversable_blocks, if_or_unless",
            "",
            "# Run a function if a block was detected:",
            f"$execute $(if_or_unless) block ~ ~ ~ $(ray_traversable_blocks) run function {hit_block_set_score.get_reference(pack_namespace)} {{\"hit_block_command\": \"$(hit_block_command)\"}}",
            "",
            "# Add one distance to the ray",
            "scoreboard players add #distance raycast 1",
            "",
            # "# Added: Particle for debugging",
            # f"{'' if DEBUG_RAYCASTING else '# '}particle minecraft:cloud ~ ~ ~",
            # "",
            "# If the raycast failed, run the failed function",
            "$execute if score #hit raycast matches 0 if score #distance raycast matches 551.. run $(failed_command)",
            "",
            "# Advance forward and run the ray again if no block was found",
            f"$execute if score #hit raycast matches 0 if score #distance raycast matches ..550 positioned ^ ^ ^0.01 run function {pack_namespace}:raycast/block_ray {formatted_arguments_replacements}",
            ],
            ["raycast"],
        )

        start_ray = MCFunction("start_block_ray", [
            "# Setting up the raycasting data.",
            "tag @s add is_raycasting",
            "scoreboard players set #hit raycast 0",
            "scoreboard players set #distance raycast 0",
            "",
            "# Play a debug sound:",
            "playsound minecraft:ui.button.click block @s ~ ~ ~",
            "",
            "# Activating the raycast. This function will call itself until it is done (at height of player - 1.62 blocks high)",
            f"$execute positioned ~ ~1.62 ~ run function {ray.get_reference(pack_namespace)} {formatted_arguments_replacements}",
            "",
            "# Raycasting finished, removing tag from the raycaster.",
            "tag @s remove is_raycasting",
            ],
            ["raycast"],
        )
        return load_ray, hit_block_set_score, start_ray, ray

    def create_deploy_function(self, pack_namespace: str) -> "MCFunction":
        from pypacks.resources.custom_mcfunction import MCFunction  # Avoid circular import

        # This exists so we don't have to have everything in start_ray duplicated, as an interface, almost.
        arguments = {
            "hit_block_command": self.on_block_hit_command,
            "failed_command": self.no_blocks_hit_command,
            "ray_traversable_blocks": self.blocks_to_detect,
            "if_or_unless": self.if_or_unless,
        }
        formatted_arguments = "{" + ", ".join([f"\"{key}\": \"{value}\"" for key, value in arguments.items()]) + "}"
        populate_start_ray = MCFunction(f"populate_start_block_ray_for_{self.internal_name}", [
            f"function {pack_namespace}:raycast/start_block_ray {formatted_arguments}",
            ],
            ["raycast", "populate_start_ray"],
        )
        # ========================================
        return populate_start_ray

    def create_datapack_files(self, pack: "Pack") -> None:
        # Makedirs in case it's an inline call, e.g. on_right_click or whatever.
        os.makedirs(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name, exist_ok=True)
        os.makedirs(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/"populate_start_ray", exist_ok=True)
        self.create_deploy_function(pack.namespace).create_datapack_files(pack)


# ====================================================================================================================


@dataclass
class EntityRaycast:
    internal_name: str
    on_entity_hit_command: str = "say Hit an entity!"
    no_entities_hit_command: str = "say No entities hit!"
    entity_to_detect: str = "minecraft:cow"

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="function/raycast")

    @staticmethod
    def generate_default_raycast_functions(pack_namespace: str) -> tuple["MCFunction", ...]:
        from pypacks.resources.custom_mcfunction import MCFunction  # Avoid circular import

        arguments = ["hit_entity_command", "failed_command", "entity_to_detect"]
        arguments_replacements = {key: f"$({key})" for key in arguments}
        formatted_arguments_replacements = "{" + ", ".join([f"\"{key}\": \"{value}\"" for key, value in arguments_replacements.items()]) + "}"

        load_ray = MCFunction("load", [
            "scoreboard objectives add raycast dummy",
            ],
            ["raycast"],
        )

        # This exists as an intermediate to set the scoreboard value *and then* calling the function, otherwise overriding it requires the scoreboard line.
        hit_entity_set_score = MCFunction("hit_entity_set_score", [
            "# Mark the ray as having found a block/entity",
            "scoreboard players set #hit raycast 1",
            "$$(hit_entity_command)",  # Call the hit entity function
            ],
            ["raycast"],
        )

        # Each Ray iteration
        ray = MCFunction("entity_ray", [
            "# Requires the following macros when calling: hit_entity_command, failed_command, entity_to_detect",
            "",
            "# Run a function if an entity was detected:",
            f"$execute if entity @e[distance=..1, type=$(entity_to_detect)] run function {hit_entity_set_score.get_reference(pack_namespace)} {{\"hit_entity_command\": \"$(hit_entity_command)\"}}",
            "",
            "# Add one distance to the ray",
            "scoreboard players add #distance raycast 1",
            "",
            "# If the raycast failed, run the failed function",
            "$execute if score #hit raycast matches 0 if score #distance raycast matches 551.. run $(failed_command)",
            "",
            "# Advance forward and run the ray again if no block was found",
            f"$execute if score #hit raycast matches 0 if score #distance raycast matches ..550 positioned ^ ^ ^0.01 run function {pack_namespace}:raycast/entity_ray {formatted_arguments_replacements}",
            ],
            ["raycast"],
        )

        start_ray = MCFunction("start_entity_ray", [
            "# Setting up the raycasting data.",
            "tag @s add is_raycasting",
            "scoreboard players set #hit raycast 0",
            "scoreboard players set #distance raycast 0",
            "",
            "# Play a debug sound:",
            "playsound minecraft:ui.button.click block @s ~ ~ ~",
            "",
            "# Activating the raycast. This function will call itself until it is done (at height of player - 1.62 blocks high)",
            f"$execute positioned ~ ~1.62 ~ run function {ray.get_reference(pack_namespace)} {formatted_arguments_replacements}",
            "",
            "# Raycasting finished, removing tag from the raycaster.",
            "tag @s remove is_raycasting",
            ],
            ["raycast"],
        )
        return load_ray, hit_entity_set_score, start_ray, ray

    def create_deploy_function(self, pack_namespace: str) -> "MCFunction":
        from pypacks.resources.custom_mcfunction import MCFunction  # Avoid circular import

        # This exists so we don't have to have everything in start_ray duplicated, as an interface, almost.
        arguments = {
            "hit_entity_command": self.on_entity_hit_command,
            "failed_command": self.no_entities_hit_command,
            "entity_to_detect": self.entity_to_detect,
        }
        formatted_arguments = "{" + ", ".join([f"\"{key}\": \"{value}\"" for key, value in arguments.items()]) + "}"
        populate_start_ray = MCFunction(f"populate_start_entity_ray_for_{self.internal_name}", [
            f"function {pack_namespace}:raycast/start_entity_ray {formatted_arguments}",
            ],
            ["raycast", "populate_start_ray"],
        )
        # ========================================
        return populate_start_ray

    def create_datapack_files(self, pack: "Pack") -> None:
        # Makedirs in case it's an inline call, e.g. on_right_click or whatever.
        os.makedirs(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name, exist_ok=True)
        os.makedirs(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/"populate_start_ray", exist_ok=True)
        self.create_deploy_function(pack.namespace).create_datapack_files(pack)