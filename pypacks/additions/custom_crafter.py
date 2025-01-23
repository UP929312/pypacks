from dataclasses import dataclass
from typing import TYPE_CHECKING

from pypacks.additions.item_components import Components, EntityData
from pypacks.resources.custom_item import CustomItem
from pypacks.resources.custom_mcfunction import MCFunction
from pypacks.resources.custom_recipe import CustomCrafterRecipe, ShapedCraftingRecipe

if TYPE_CHECKING:
    from pypacks.pack import Pack
    # from pypacks.resources.custom_item import CustomItem


@dataclass
class CustomCrafter:
    """Allows for more indepth crafting with ingredients that have custom components.
    This is achieved by using droppers"""
    internal_name: str
    crafter_name: str
    block_crafting_recipe: ShapedCraftingRecipe  # Output is ignore...

    datapack_subdirectory_name: str = None  # type: ignore[abc]

    def generate_give_command(self, pack_namespace: str) -> "CustomItem":
        entity_data = {"id": "minecraft:item_display", "Tags": [f"{self.internal_name}_custom_crafter", "placing"], "Rotation": [0.0, 0.0], "brightness": {"sky": 10, "block": 10}, "transformation": {"left_rotation": [0.0, 0.0, 0.0, 1.0], "right_rotation": [0.0, 0.0, 0.0, 1.0], "translation": [0.0, 0.5, 0.0], "scale": [1.01, 1.01, 1.01]}, "item" : {"id": "minecraft:crafting_table", "count": 1}}
        return CustomItem(
            self.internal_name+"_custom_crafter", "minecraft:bat_spawn_egg", self.crafter_name,
            components=Components(entity_data=EntityData(entity_data)),
        )

    def create_datapack_files(self, pack: "Pack") -> None:
        pass

    def on_tick(self, pack_namespace: str) -> MCFunction:
        # We need to place an item display at every "custom dropper".
        # Droppers have slots 0-8, with 4 being the center slot.
        # We need to not only check for the presence of the right ingredients,
        # but also the absence of any items in empty slots.
        # We first need to allow the placing of custom crafters.
        # We do this by giving a spawn egg which spawns the item display, it also sets the block.
        # Then, every tick, we check if something's been crafted, or if the block has been broken.
        # If it has, remove the item display and give them the spawn egg back.

        # Temp recipe for testing
        recipe = CustomCrafterRecipe(
            "custom_test_recipe", [
                "minecraft:stone", "minecraft:air", "minecraft:stone",
                "minecraft:stone", "minecraft:air", "minecraft:stone",
                "minecraft:stone", "minecraft:stone", "minecraft:stone",
            ],
            "minecraft:coal",
        )
        # ========================================================================================
        custom_crafter_name = f"{self.crafter_name}"
        tag_name = f"{self.internal_name}_custom_crafter"
        on_tick_block_management = [
            # Manages placing and breaking of the block
            f"execute at @e[type=item_display, tag={tag_name}, tag=placing] run setblock ~ ~ ~ dropper[facing=up]{{CustomName:'\"{custom_crafter_name}\"'}}",
            f"tag @e[type=item_display, tag={tag_name}, tag=placing] remove placing",
            f"execute as @e[type=item_display, tag={tag_name}] at @s unless block ~ ~ ~ dropper[facing=up] run data modify entity @e[type=item,distance=..1,nbt={{Item:{{id:\"minecraft:dropper\"}}}},limit=1] Item set value {{id:\"minecraft:bat_spawn_egg\",count:1,components:{{\"item_name\":'\"{custom_crafter_name}\"',\"minecraft:entity_data\":{{id:\"minecraft:item_display\",Tags:[\"{tag_name}\",\"placing\"],Rotation:[0f,0f],brightness:{{sky:10,block:10}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.5f,0f],scale:[1.01f,1.01f,1.01f]}},item:{{id:\"minecraft:crafting_table\",count:1}}}}}}}}",
            f"execute as @e[type=item_display, tag={tag_name}] at @s unless block ~ ~ ~ dropper[facing=up] run kill @s",
        ]
        # ========================================================================================
        execute_at_command = f"execute at @e[type=item_display, tag={tag_name}] "
        item_checks = [
            f"if items block ~ ~ ~ container.{index} {ingredient} " if ingredient != "minecraft:air"
            # f"if items block ~ ~ ~ container.{index} {ingredient}[custom_data~{{some:true}}] " if ingredient != "minecraft:air"
            else f"unless data block ~ ~ ~ Items[{{Slot:{index}b}}] "
            for index, ingredient in enumerate(recipe.ingredients)
        ]
        set_slot_command = "run data modify block ~ ~ ~ Items set value [{Slot:4b,id:\"minecraft:ender_eye\",count:1b,components:{\"minecraft:custom_data\":{custom_result:true},\"minecraft:item_name\":'\"Some Custom Result\"'}}]"
        # print("\n".join(item_checks))
        return MCFunction(f"on_tick_custom_crafter_{self.internal_name}", [
            *on_tick_block_management,
            "",
            "# And for custom crafting:",
            execute_at_command + "".join(item_checks) + set_slot_command
            ], ["custom_crafting"],
        )
