from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.resources.custom_mcfunction import MCFunction
    from pypacks.resources.custom_tag import CustomTag
    from pypacks.scripts.repos.all_entity_names import MinecraftEntity

# TODO: entity raycasts can be changed to accept lists of entity (or do the whole tag situation?).
# Also, the entity one should have a "stop for blocks" option, we can just extend the condition.


@dataclass
class Raycast:
    internal_name: str

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="function/raycast")

    @staticmethod
    def generate_default_raycast_functions(pack_namespace: str) -> tuple["MCFunction", ...]:
        from pypacks.resources.custom_mcfunction import MCFunction  # Avoid circular import

        # DEBUG_RAYCASTING = False
        arguments = ["condition", "on_successful_hit", "on_failure",
                     "distance_between_iterations", "max_iterations", "max_iterations_plus_one"]
        arguments_replacements = {key: f"$({key})" for key in arguments}  # This is different to the one in _create_prepare_ray_command
        formatted_arguments_replacements = "{" + ", ".join([f"\"{key}\": \"{value}\"" for key, value in arguments_replacements.items()]) + "}"

        # This exists as an intermediate to set the scoreboard value *and then* calling the function, otherwise overriding it requires the scoreboard line.
        on_success_set_score = MCFunction("on_success_set_score", [
            "# Mark the ray as having found a block/entity",
            "scoreboard players set #hit raycast 1",
            "$$(on_successful_hit)",  # Run the on_successful_hit command
            ],
            ["raycast"],
        )

        # Each Ray iteration
        ray = MCFunction("ray", [
            # "say Running the ray!",
            "",
            "# Run a function if a block was detected:",
            # $(if_or_unless) block ~ ~ ~ $(ray_traversable_blocks)
            f"$execute $(condition) run function {on_success_set_score.get_reference(pack_namespace)} {{\"on_successful_hit\": \"$(on_successful_hit)\"}}",
            "",
            "# Add one distance to the ray",
            "scoreboard players add #distance raycast 1",
            "",
            # "# Added: Particle for debugging",
            # f"{'' if DEBUG_RAYCASTING else '# '}particle minecraft:cloud ~ ~ ~",
            # "",
            "# If the raycast failed, run the failed function",
            # "$execute if score #hit raycast matches 0 if score #distance raycast matches 501.. run $(on_failure)",
            "$execute if score #hit raycast matches 0 if score #distance raycast matches $(max_iterations_plus_one).. run $(on_failure)",
            "",
            "# Advance forward and run the ray again if no successful hit occured",
            # f"$execute if score #hit raycast matches 0 if score #distance raycast matches ..500 positioned ^ ^ ^$(distance_between_iterations) run function {pack_namespace}:raycast/ray {formatted_arguments_replacements}",
            f"$execute if score #hit raycast matches 0 if score #distance raycast matches ..$(max_iterations) positioned ^ ^ ^$(distance_between_iterations) run function {pack_namespace}:raycast/ray {formatted_arguments_replacements}",
            ],
            ["raycast"],
        )

        setup_ray = MCFunction("setup_ray", [
            "# Setting up the raycasting data.",
            "tag @s add is_raycasting",
            "scoreboard players set #hit raycast 0",
            "scoreboard players set #distance raycast 0",
            "",
            "# Play a debug sound:",
            "playsound minecraft:ui.button.click block @s ~ ~ ~",
            # "say Starting the ray!",
            "",
            "# Activating the raycast. This function will call itself until it is done (at height of player - 1.62 blocks high)",
            f"$execute positioned ~ ~1.62 ~ run function {ray.get_reference(pack_namespace)} {formatted_arguments_replacements}",
            "",
            "# Raycasting finished, removing tag from the raycaster.",
            "tag @s remove is_raycasting",
            ],
            ["raycast"],
        )
        return on_success_set_score, setup_ray, ray

    def create_deploy_function(self, pack_namespace: str) -> "MCFunction":
        raise NotImplementedError

    def get_run_command(self, pack_namespace: str) -> str:
        return self.create_deploy_function(pack_namespace).get_run_command(pack_namespace)

    def create_datapack_files(self, pack: "Pack") -> None:
        # Makedirs in case it's an inline call, e.g. on_right_click or whatever.
        os.makedirs(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name, exist_ok=True)
        prepare_ray_subdirectory = self._create_prepare_ray_command("", "", "", 1, 1, "").sub_directories[-1]
        os.makedirs(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/prepare_ray_subdirectory, exist_ok=True)
        self.create_deploy_function(pack.namespace).create_datapack_files(pack)

    def _create_prepare_ray_command(
            self, condition: str, on_successful_hit: str, on_failure: str, distance_between_iterations: float, max_distance_in_blocks: int, pack_namespace: str
        ) -> "MCFunction":
        from pypacks.resources.custom_mcfunction import MCFunction
        arguments = {
            "condition": condition,
            "on_successful_hit": on_successful_hit,
            "on_failure": on_failure,
            "distance_between_iterations": distance_between_iterations,
            "max_iterations": int(max_distance_in_blocks // distance_between_iterations),
            "max_iterations_plus_one": int((max_distance_in_blocks // distance_between_iterations) + 1),
        }
        formatted_arguments = "{" + ", ".join([f"\"{key}\": \"{value}\"" for key, value in arguments.items()]) + "}"
        # This exists so we don't have to have everything in start_ray duplicated, as an interface, almost.
        prepare_ray = MCFunction(f"prepare_ray_for_{self.internal_name}", [
            f"function {pack_namespace}:raycast/setup_ray {formatted_arguments}",
            ],
            ["raycast", "prepare_ray"],
        )
        return prepare_ray


# ====================================================================================================================
# This is a simple raycasting system that can be used to detect blocks in a line of sight.
# It takes 4 inputs, the hit block commaand, the failed command (no blocks in the limit), the ray traversable blocks,
# and if the we should check if the ray_traversable_blocks is present or absent (end if we find a block, or if we don't).
# An example of this is:
# raycast = BlockRaycast(
#     on_block_hit_command="setblock ~ ~ ~ minecraft:stone",
#     no_blocks_hit_command="say No blocks hit!",
#     blocks_to_detect="#minecraft:replaceable",
#     if_or_unless="unless",
# )
# (This will set a stone block where the ray hits, and say "No blocks hit!" if the ray doesn't hit anything)


@dataclass
class BlockRaycast(Raycast):
    internal_name: str
    on_block_hit_command: str = "setblock ~ ~ ~ minecraft:gold_block"
    no_blocks_hit_command: str = "say No blocks hit!"
    blocks_to_detect: "str | CustomTag" = "#minecraft:replaceable"  # Blocks the ray can pass through (if blocks to detect is set to unless), e.g. #minecraft:replaceable (air, short grass, etc)
    if_or_unless: Literal["if", "unless"] = "unless"  # If set to "if", the ray will stop if it hits a block, if set to "unless", the ray will stop if it doesn't hit the block(s)
    # command_ran_each_iteration: str = "particle minecraft:cloud ~ ~ ~"  # The command to run each iteration of the ray TODO: Implement
    distance_between_iterations: float = 0.01  # The space between each ray iteration
    max_distance_in_blocks: int = 6  # The maximum distance the ray can travel (this can be liberal, even numbers as big as 50-100 is fine!)

    def create_deploy_function(self, pack_namespace: str) -> "MCFunction":
        from pypacks.resources.custom_tag import CustomTag
        assert self.if_or_unless in ("if", "unless"), "if_or_unless must be either 'if' or 'unless'"
        block_or_block_tag = self.blocks_to_detect.get_reference(pack_namespace) if isinstance(self.blocks_to_detect, CustomTag) else self.blocks_to_detect
        return self._create_prepare_ray_command(
            condition=f"{self.if_or_unless} block ~ ~ ~ {block_or_block_tag}",
            on_successful_hit=self.on_block_hit_command,
            on_failure=self.no_blocks_hit_command,
            distance_between_iterations=self.distance_between_iterations,
            max_distance_in_blocks=self.max_distance_in_blocks,
            pack_namespace=pack_namespace,
        )


# ====================================================================================================================


@dataclass
class EntityRaycast(Raycast):
    internal_name: str
    on_entity_hit_command: str = "say Hit an entity!"
    no_entities_hit_command: str = "say No entities hit!"
    entity_to_detect: "MinecraftEntity | None" = "minecraft:cow"
    # command_ran_each_iteration: str = "particle minecraft:cloud ~ ~ ~"  # The command to run each iteration of the ray TODO: Implement
    distance_between_iterations: float = 0.01  # The space between each ray iteration
    max_distance_in_blocks: int = 6  # The maximum distance the ray can travel (this can be liberal, even numbers as big as 50-100 is fine!)

    def create_deploy_function(self, pack_namespace: str) -> "MCFunction":
        return self._create_prepare_ray_command(
            condition=(
                f"if entity @e[distance=..1, type={self.entity_to_detect}]"
                if self.entity_to_detect is not None else
                "if entity @e[distance=..1]"
            ),
            on_successful_hit=self.on_entity_hit_command,
            on_failure=self.no_entities_hit_command,
            distance_between_iterations=self.distance_between_iterations,
            max_distance_in_blocks=self.max_distance_in_blocks,
            pack_namespace=pack_namespace,
        )
