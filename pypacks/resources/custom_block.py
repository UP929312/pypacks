import json
from typing import TYPE_CHECKING, Literal
from dataclasses import dataclass, field

from pypacks.resources.custom_advancement import Criteria, CustomAdvancement
from pypacks.resources.mcfunction import MCFunction

if TYPE_CHECKING:
    from pypacks.datapack import Datapack
    from pypacks.resources.custom_item import CustomItem

@dataclass
class FacePaths:
    # If a face is None, it will use the front texture
    front: str
    back: str | None
    top: str | None
    bottom: str | None
    left: str | None
    right: str | None

# TODO: Support non cubes? Player heads? Custom models?

# TODO:
# Implement destroying them :)


@dataclass
class CustomBlock:
    """Adds a custom block, for the texture, pass in a single 16x16 texture path, or a FacePaths object, which allows multiple paths to be
    passed in. Setting drops to "self" will make the block drop itself when broken, and setting it to None will make it drop `nothing`."""
    # When they destroy it, we need to replace the dropped item with our custom one.
    internal_name: str
    name: str
    base_block: str = "minecraft:stone"
    block_texture: str = "new_example_block"  #  | FacePaths
    drops: "CustomItem | None | Literal['self']" = "self"
    # on_right_click: str | None = None  # For things like inventories, custom furnaces, etc
    # silk_touch_drops: "CustomItem | str | None | Literal['self']" = "self"

    block_item: "CustomItem" = field(init=False, default=None)  # type: ignore[abc]

    @classmethod
    def from_item(cls, item: "CustomItem", drops: "CustomItem | None | Literal['self']" = "self") -> "CustomBlock":
        assert item.custom_name is not None
        assert item.texture_path is not None
        item.is_block = True
        class_ = cls(item.internal_name, item.custom_name, item.base_item, item.texture_path, drops=drops)
        class_.block_item = item
        return class_

    def create_advancement(self, datapack: "Datapack") -> "CustomAdvancement":
        condition = {
            "location": [
                {
                    "condition": "minecraft:match_tool",
                    "predicate": {
                        "predicates": {
                            "minecraft:custom_data": "{%s:'%s'}" % ("pypacks_custom_item", self.internal_name),
                        }
                    }
                }
            ]
        }
        criteria = Criteria(f"placed_{self.internal_name}", "minecraft:placed_block", conditions=condition)
        rewarded_function = f"{datapack.namespace}:custom_blocks/revoke_and_run/revoke_and_run_{self.block_item.internal_name}"
        advancement = CustomAdvancement(f"placed_{self.internal_name}", criteria=[criteria], rewarded_function=rewarded_function, hidden=True)
        return advancement

    def generate_functions(self, datapack: "Datapack") -> tuple["MCFunction", ...]:
        # These are in reverse order (pretty much), so we can reference them in the next function.
        # ============================================================================================================
        # Has to be secondary so we have @s set correctly.
        execute_as_item_display = MCFunction(f"execute_on_item_display_{self.internal_name}", [
            # f"tag @s add {datapack.namespace}.block_display.{self.internal_name}",
            # f"tag @s add global.ignore",
            # f"tag @s add global.ignore.kill",
            # f"tag @s add smithed.entity",
            # f"tag @s add smithed.block",
            # f"tag @s add {datapack.namespace}.custom_block",
            # f"tag @s add {datapack.namespace}.{self.internal_name}",
            # f"tag @s add {datapack.namespace}.vanilla.{self.base_block}",

            # Make it _slightly_ bigger than the block, so it hides the original (only a tiny bit bigger), to stop z-fighting too.
            f"data modify entity @s transformation.scale set value [1.002f, 1.002f, 1.002f]",
            "data modify entity @s brightness set value {block: 15, sky: 15}",

            # For item displays, container.0 is just the item it is displaying.
            f"item replace entity @s container.0 with minecraft:sponge[minecraft:item_model='{datapack.namespace}:{self.internal_name}']",
            ],
            ["custom_blocks", "execute_on_item_display"],
        )
        # Spawn the item display, then call the setup on it directly.
        spawn_item_display = MCFunction(f"setup_item_display_{self.block_item.internal_name}", [
            f"execute align xyz positioned ~.5 ~.5 ~.5 summon item_display at @s run function {execute_as_item_display.get_reference(datapack)}",
            ],
            ["custom_blocks", "setup_item_display"],
        )
        # ============================================================================================================
        hit_block = MCFunction(f"hit_block_{self.internal_name}", [
            "# Mark the ray as having found a block",
            "scoreboard players set #hit raycast 1",  # TODO: Set this in raycasting instead...
            "",
            "# Running custom commands since the block was found",
            f"function {spawn_item_display.get_reference(datapack)}",
            ],
            ["custom_blocks", "hit_block"],
        )
        arguments = {
            "hit_block_function": f"{hit_block.get_reference(datapack)}",
            "failed_function": f"{datapack.namespace}:raycast/failed",
            "ray_transitive_blocks": f"#{datapack.namespace}:ray_transitive_blocks",
        }
        formatted_arguments = "{" +", ".join([f"\"{key}\": \"{value}\"" for key, value in arguments.items()]) + "}"
        populate_start_ray = MCFunction(f"populate_start_ray_{self.internal_name}", [
                f"function {datapack.namespace}:raycast/start_ray {formatted_arguments}",
            ],
            ["custom_blocks", "populate_start_ray"],
        )
        # ============================================================================================================
        revoke_and_run_mcfunction = MCFunction(f"revoke_and_run_{self.internal_name}", [
                f"advancement revoke @s only {datapack.namespace}:placed_{self.internal_name}",
                f"function {populate_start_ray.get_reference(datapack)}",
            ],
            ["custom_blocks", "revoke_and_run"],
        )
        # ============================================================================================================
        return execute_as_item_display, spawn_item_display, hit_block, populate_start_ray, revoke_and_run_mcfunction
