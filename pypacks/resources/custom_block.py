import os
import json
import shutil
from typing import TYPE_CHECKING, Literal
from dataclasses import dataclass, field

from pypacks.resources.custom_advancement import Criteria, CustomAdvancement
from pypacks.resources.mcfunction import MCFunction
from pypacks.resources.custom_loot_table import CustomLootTable, SingleItemPool
from pypacks.resources.constants import DIRECTION_TO_BLOCKS

if TYPE_CHECKING:
    from pypacks.datapack import Datapack
    from pypacks.resources.custom_item import CustomItem

# TODO: Support non cubes? Player heads? Custom models?
# First, rotation

@dataclass
class FacePaths:
    # If a face is None, it will use the front texture
    front: str
    back: str | None
    top: str | None
    bottom: str | None
    left: str | None
    right: str | None

    def __post_init__(self) -> None:
        # We have 3 options, axial (NESW+Up+Down), cardinal (NESW), and on_axis (north-south, east-west, up-down)
        assert self.front is not None
        if [x is None for x in [self.back, self.top, self.bottom, self.left, self.right]]:
            self.direction_type = "symmetric"
            return
        elif self.top is None and self.bottom is None and [x is not None for x in [self.back, self.left, self.right]]:
            self.direction_type = "cardinal"
            return
        elif [x is not None for x in [self.back, self.top, self.bottom, self.left, self.right]]:
            self.direction_type = "axial"
            return
        raise ValueError("Invalid FacePaths object, must have one of:" +
                         "Front | Front, Back, Left, Right | Front, Back, Top, Bottom, Left, Right")  # fmt: skip

    def create_resource_pack_files(self, block: "CustomBlock", datapack: "Datapack") -> None:
        # Requires the following file structure:
        # ├── assets/
        # │   └── <datapack namespace>/
        # │       ├── blockstates/
        # │       │   └── <custom_block>.json
        # │       ├── models/
        # │       │   └── block/
        # │       │       └── <custom_block>.json
        # │       └── textures/
        # │           └── block/
        # │               ├── <custom_block>_top.png
        # │               ├── <custom_block>_bottom.png
        # │               ├── <custom_block>_north.png
        # │               ├── <custom_block>_south.png
        # │               ├── <custom_block>_east.png
        # │               └── <custom_block>_west.png
        os.makedirs(os.path.join(datapack.resource_pack_path, "assets", datapack.namespace, "blockstates"), exist_ok=True)
        os.makedirs(os.path.join(datapack.resource_pack_path, "assets", datapack.namespace, "models", "block"), exist_ok=True)
        os.makedirs(os.path.join(datapack.resource_pack_path, "assets", datapack.namespace, "textures", "block"), exist_ok=True)
        with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/blockstates/{block.internal_name}.json", "w") as file:
            json.dump({
                "variants": {
                    "": {"model": f"{datapack.namespace}:block/{block.internal_name}"},
                }
            }, file, indent=4)

        with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/models/block/{block.internal_name}.json", "w") as file:
            json.dump({
                "parent": "block/cube",
                "textures": {
                    "up": f"{datapack.namespace}:block/{self.top or self.front}",
                    "down": f"{datapack.namespace}:block/{self.bottom or self.front}",
                    "north": f"{datapack.namespace}:block/{self.back or self.front}",
                    "south": f"{datapack.namespace}:block/{self.front}",
                    "east": f"{datapack.namespace}:block/{self.right or self.front}",
                    "west": f"{datapack.namespace}:block/{self.left or self.front}",
                }
            }, file, indent=4)

        for face in [self.front, self.back, self.top, self.bottom, self.left, self.right]:
            if face is not None:
                shutil.copyfile(face, f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/block/{block.internal_name}_{face}.png")


@dataclass
class CustomBlock:
    """Adds a custom block, for the texture, pass in a single 16x16 texture path, or a FacePaths object, which allows multiple paths to be
    passed in (e.g. rotatable logs). Setting drops to "self" will make the block drop itself when broken, 
    and setting it to None will make it drop nothing."""
    internal_name: str
    name: str
    base_block: str
    block_texture: str | FacePaths
    drops: "Literal['self'] | CustomItem | CustomLootTable | str | None" = "self"
    # silk_touch_drops: "Literal['self'] | CustomItem | CustomLootTable | str | None" = "self"
    # on_right_click: str | None = None  # For things like inventories, custom furnaces, etc

    block_item: "CustomItem | None" = field(init=False, repr=False, default=None)  # Used by datapack to create the custom icons

    def __post_init__(self) -> None:
        if isinstance(self.block_texture, str):
            self.block_texture = FacePaths(self.block_texture, None, None, None, None, None)
        if (self.block_texture.direction_type != "symmetric" and
            self.base_block not in DIRECTION_TO_BLOCKS[self.block_texture.direction_type]
           ):
            raise ValueError(f"Block {self.base_block} cannot use this texture face paths! (Base block probably doesn't support these rotations)")

    def set_or_create_loot_table(self) -> None:
        """Takes a CustomItem, item_name, CustomLootTable, or None, and sets the loot_table attribute to a CustomLootTable object."""
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
        """Used to create a new custom block."""
        assert item.custom_name is not None and item.texture_path is not None
        item.is_block = True
        class_ = cls(item.internal_name, item.custom_name, item.base_item, item.texture_path, drops=drops)
        class_.block_item = item
        class_.set_or_create_loot_table()
        return class_

    def create_advancement(self, datapack: "Datapack") -> "CustomAdvancement":
        """Required to detect when the custom block is placed."""
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
        # detect_rotation = MCFunction(f"detect_rotation_{self.internal_name}", [
        #     f"execute if score #rotation {datapack.namespace}.data matches 0 if entity @s[y_rotation=-46..45] run scoreboard players set #rotation {datapack.namespace}.data 1",
        #     f"execute if score #rotation {datapack.namespace}.data matches 0 if entity @s[y_rotation=45..135] run scoreboard players set #rotation {datapack.namespace}.data 2",
        #     f"execute if score #rotation {datapack.namespace}.data matches 0 if entity @s[y_rotation=135..225] run scoreboard players set #rotation {datapack.namespace}.data 3",
        #     f"execute if score #rotation {datapack.namespace}.data matches 0 if entity @s[y_rotation=225..315] run scoreboard players set #rotation {datapack.namespace}.data 4",
        # ], ["custom_blocks"]),
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
            # execute if score #rotation {datapack.namespace}.data matches {i+1} run setblock ~ ~ ~ {block_id}[facing={face}," + ",".join(block_states) + f"]{beautify_name}\n
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
        """Runs every tick, but once per datapack, not per block."""
        return MCFunction(f"all_blocks_tick", [
            # Kill all xp orbs and items, spawn the loot, then kill the item display itself.
            *[f"execute as @e[type=item_display, tag={datapack.namespace}.custom_block.{custom_block.internal_name}] at @s if block ~ ~ ~ minecraft:air run function {datapack.namespace}:custom_blocks/on_destroy/on_destroy_no_silk_touch_{custom_block.internal_name}"
              for custom_block in datapack.custom_blocks],
        ], ["custom_blocks"])

    # def create_resource_pack_files(self, datapack: "Datapack") -> None:
    #     assert isinstance(self.block_texture, FacePaths)
    #     self.block_texture.create_resource_pack_files(self, datapack)