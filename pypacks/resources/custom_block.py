from typing import TYPE_CHECKING, Literal
from dataclasses import dataclass, field

from pypacks.resources.custom_advancement import Criteria, CustomAdvancement
from pypacks.resources.mcfunction import MCFunction
from pypacks.resources.custom_loot_table import CustomLootTable, SingleItemPool

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
# Implement destroying them :) - Done, but needs drops, probably loot tables?


@dataclass
class CustomBlock:
    """Adds a custom block, for the texture, pass in a single 16x16 texture path, or a FacePaths object, which allows multiple paths to be
    passed in. Setting drops to "self" will make the block drop itself when broken, and setting it to None will make it drop `nothing`."""
    # When they destroy it, we need to replace the dropped item with our custom one.
    internal_name: str
    name: str
    base_block: str = "minecraft:stone"
    block_texture: str = "new_example_block"  #  | FacePaths
    drops: "Literal['self'] | CustomItem | CustomLootTable | str | None" = "self"
    silk_touch_drops: "Literal['self'] | CustomItem | CustomLootTable | str | None" = "self"
    # on_right_click: str | None = None  # For things like inventories, custom furnaces, etc

    block_item: "CustomItem | None" = field(init=False, repr=False, default=None)  # Used by datapack to create the custom icons

    def set_or_create_loot_table(self) -> None:

        from pypacks.resources.custom_item import CustomItem
        self.loot_table = None
        if self.drops == "self":
            if self.block_item is not None:
                self.loot_table = CustomLootTable(f"{self.internal_name}_block_drop_loot_table", [SingleItemPool(self.block_item)])
            else:
                raise ValueError("If drops is set to 'self', then block_item must be set.")
        elif isinstance(self.drops, (CustomItem, str)):
            self.loot_table = CustomLootTable(f"{self.internal_name}_block_drop_loot_table", [SingleItemPool(self.drops)])
        elif isinstance(self.drops, CustomLootTable):
            self.loot_table = self.drops

    @classmethod
    def from_item(cls, item: "CustomItem", drops: "Literal['self'] | CustomItem | CustomLootTable | None" = "self") -> "CustomBlock":
        assert item.custom_name is not None
        assert item.texture_path is not None
        item.is_block = True
        class_ = cls(item.internal_name, item.custom_name, item.base_item, item.texture_path, drops=drops)
        class_.block_item = item
        class_.set_or_create_loot_table()
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
        rewarded_function = f"{datapack.namespace}:custom_blocks/revoke_and_run/revoke_and_run_{self.internal_name}"
        advancement = CustomAdvancement(f"placed_{self.internal_name}", criteria=[criteria], rewarded_function=rewarded_function, hidden=True)
        return advancement

    def generate_functions(self, datapack: "Datapack") -> tuple["MCFunction", ...]:
        # These are in reverse order (pretty much), so we can reference them in the next function.
        # ============================================================================================================
        # Has to be secondary so we have @s set correctly.
        execute_as_item_display = MCFunction(f"execute_on_item_display_{self.internal_name}", [
            f"tag @s add {datapack.namespace}.custom_block",
            f"tag @s add {datapack.namespace}.custom_block.{self.internal_name}",

            # Make it _slightly_ bigger than the block, so it hides the original (only a tiny bit bigger), to stop z-fighting too.
            "data modify entity @s transformation.scale set value [1.002f, 1.002f, 1.002f]",
            "data modify entity @s brightness set value {block: 15, sky: 15}",

            # For item displays, container.0 is just the item it is displaying.
            f"item replace entity @s container.0 with minecraft:sponge[minecraft:item_model='{datapack.namespace}:{self.internal_name}']",
            ],
            ["custom_blocks", "execute_on_item_display"],
        )
        # Spawn the item display, then call the setup on it directly.
        spawn_item_display = MCFunction(f"setup_item_display_{self.internal_name}", [
            f"execute align xyz positioned ~.5 ~.5 ~.5 summon item_display at @s run function {execute_as_item_display.get_reference(datapack)}",
            ],
            ["custom_blocks", "setup_item_display"],
        )
        # ============================================================================================================
        arguments = {
            "hit_block_function": f"{spawn_item_display.get_reference(datapack)}",
            "failed_function": f"{datapack.namespace}:raycast/failed",
            "ray_transitive_blocks": f"{self.base_block}",
            "if_or_unless": "if",
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
        on_destroy_no_silk_touch_function = MCFunction(f"on_destroy_no_silk_touch_{self.internal_name}", [
                f"kill @e[type=experience_orb, distance=..0.5]",  # Kill all xp orbs dropped
                f"kill @e[type=item, distance=..0.5]",  # Kill all naturally dropped items
                f"loot spawn ~ ~ ~ loot {self.loot_table.get_reference(datapack)}" if self.loot_table is not None else "# Doesn't drop loot",  # Spawn the loot
                f"kill @s"  # Kill the item display
            ],
            ["custom_blocks", "on_destroy"],
        )
        # ============================================================================================================
        return execute_as_item_display, spawn_item_display, populate_start_ray, revoke_and_run_mcfunction, on_destroy_no_silk_touch_function

    @staticmethod
    def on_tick_function(datapack: "Datapack") -> "MCFunction":
        return MCFunction(f"all_blocks_tick", [
            # Kill all xp orbs and items, spawn the loot, then kill the item display itself.
            *[f"execute as @e[type=item_display, tag={datapack.namespace}.custom_block.{custom_block.internal_name}] at @s if block ~ ~ ~ minecraft:air run function {datapack.namespace}:custom_blocks/on_destroy/on_destroy_no_silk_touch_{custom_block.internal_name}"
              for custom_block in datapack.custom_blocks],
        ], ["custom_blocks"])