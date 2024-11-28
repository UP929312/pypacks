import json
import shutil
from typing import TYPE_CHECKING, Literal
from dataclasses import dataclass, field

from pypacks.resources.custom_predicate import Predicate
from pypacks.resources.custom_advancement import Criteria, CustomAdvancement

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

# TODO MASTER:
# 1. Setup custom items for the custom blocks, perhaps it takes an item field, and you just pass in a custom item?
# 2. Tag all custom items (for blocks) with some tag, so when we're writing the predicate, we can check if it's a custom block.
# 3. Write predicates which check if the block is a custom block, and if it is, we can run the custom block function.

# ORRR, do we do it the other way around? Add the custom block data to the item?

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
    # silk_touch_drops: "CustomItem | str | None | Literal['self']" = "self"

    block_item: "CustomItem | None" = field(init=False, default=None)

    @classmethod
    def from_item(cls, item: "CustomItem", drops: "CustomItem | None | Literal['self']" = "self") -> "CustomBlock":
        assert item.custom_name is not None
        assert item.texture_path is not None
        item.is_block = True
        # item.custom_data |= {"pypacks_custom_block": item.internal_name}
        class_ = cls(item.internal_name, item.custom_name, item.base_item, item.texture_path, drops=drops)
        class_.block_item = item
        return class_

    def create_resource_pack_files(self, datapack: "Datapack") -> None:
        pass

    def create_datapack_files(self, datapack: "Datapack") -> None:
        # initial_place_function_content, execute_as_file_content = self.generate_place_function(datapack)
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
        # advancement = CustomAdvancement(f"placed_{self.internal_name}", criteria=[criteria], rewarded_function=f"{datapack.namespace}:custom_blocks/{self.internal_name}/place", hidden=True)
        advancement = CustomAdvancement(f"placed_{self.internal_name}", criteria=[criteria], rewarded_function=f"{datapack.namespace}:give/musical_horn", hidden=True)
        advancement.create_datapack_files(datapack)

    def generate_place_function(self, datapack: "Datapack") -> tuple[str, str]:
        # We need to generate a 3d cube texture for the block.
        # We use item models because we can't give the block_display custom textures.
        # summon minecraft:item_display ~ ~ ~ {"item": {"id": "sponge", "components": {"item_model": "pypacks_testing:item/ruby_ore"}}}
        # item replace entity @e[type=minecraft:block_display] container.0 with minecraft:sponge[minecraft:item_model="pypacks_testing:item/ruby_ore"]
        initial_place_function_content = [
            f"tag @s add {datapack.namespace}.placer",
            f"setblock ~ ~ ~ air",
            f"setblock ~ ~ ~ {self.base_block}",
            f"execute align xyz positioned ~.5 ~.5 ~.5 summon item_display at @s run function {datapack.namespace}:custom_blocks/{self.internal_name}/place_secondary",
            f"tag @s remove {datapack.namespace}.placer",
        ]
        # Has to be secondary so we have @s set correctly.
        execute_as_file_content = [
            f"tag @s add {datapack.namespace}.block_display.{self.internal_name}",
            # f"tag @s add global.ignore",
            # f"tag @s add global.ignore.kill",
            # f"tag @s add smithed.entity",
            # f"tag @s add smithed.block",
            # f"tag @s add {datapack.namespace}.custom_block",
            # f"tag @s add {datapack.namespace}.{self.internal_name}",
            # f"tag @s add {datapack.namespace}.vanilla.{self.base_block}",

            # Make it _slightly_ bigger than the block, so it hides the original (only a tiny bit bigger), to stop z-fighting too.
            f"data modify entity @s transformation.scale set value [1.002f,1.002f,1.002f]",
            f"data modify entity @s brightness set value {{block:15,sky:15}}",

            # For item displays, container.0 is just the item it is displaying.
            f"item replace entity @s container.0 with minecraft:sponge[minecraft:item_model='{datapack.namespace}:item/{self.internal_name}']"
        ]
        return "\n".join(initial_place_function_content), "\n".join(execute_as_file_content)
