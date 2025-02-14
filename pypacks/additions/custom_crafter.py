import json
from dataclasses import dataclass

from pypacks.additions.item_components import Components, EntityData
from pypacks.resources.custom_item import CustomItem
from pypacks.resources.custom_mcfunction import MCFunction
from pypacks.resources.custom_recipe import CustomCrafterRecipe, ShapedCraftingRecipe
from pypacks.resources.custom_sound import CustomSound
from pypacks.resources.custom_tag import CustomTag

from pypacks.utils import to_component_string

# TODO: Add a way to customize the custom crafter object, currently it's a spawn egg with no lore or whatever. Merge with custom item?
# TODO: Give the custom crafter a custom model (optional).
# TODO: Make the Bat egg have custom formatting, i.e. rather than doing \"{crafter_name}\", do the json way, like we do with custom items, {"text": custom_crafter}
# Potentially, add a delay, so things aren't crafted instantly.


# To allow a custom crafter object, we need a few things:
# To override the entity data of the item, that's it?
# I suppose we also need to ensure it's a spawn egg of some kind.

@dataclass
class CustomCrafter:
    """Allows for more indepth crafting with ingredients that have custom components.
    This is achieved by using droppers"""
    internal_name: str
    crafter_name: str
    crafter_block_crafting_recipe: "ShapedCraftingRecipe | None"  # Output is ignored...
    recipes: list["CustomCrafterRecipe"]
    on_craft_sound: "str | CustomSound" = "minecraft:block.amethyst_block.chime"

    def __post_init__(self) -> None:
        if self.crafter_block_crafting_recipe is not None:
            self.crafter_block_crafting_recipe.result = self.generate_custom_item()

    def generate_custom_item(self) -> "CustomItem":
        entity_data = {
            "id": "minecraft:item_display", "Tags": [f"{self.internal_name}_custom_crafter", "placing"],
            "item": {"id": "minecraft:crafting_table", "count": 1},
            "brightness": {"sky": 10, "block": 10}, "Rotation": [0.0, 0.0],
            "transformation": {"left_rotation": [0.0, 0.0, 0.0, 1.0], "right_rotation": [0.0, 0.0, 0.0, 1.0], "translation": [0.0, 0.5, 0.0], "scale": [1.01, 1.01, 1.01]},
        }
        return CustomItem(
            self.internal_name+"_custom_crafter", "minecraft:bat_spawn_egg", self.crafter_name,
            components=Components(entity_data=EntityData(entity_data)),
        )

    def _deal_with_item_components(self, ingredient: "str | CustomItem | CustomTag", pack_namespace: str) -> str:
        if isinstance(ingredient, CustomTag):
            return ingredient.get_reference(pack_namespace)
        if isinstance(ingredient, CustomItem):
            return f"{ingredient.base_item}[{to_component_string(ingredient.to_dict(pack_namespace))}]"
        return ingredient

    def on_tick(self, pack_namespace: str) -> MCFunction:
        # We need to place an item display at every "custom dropper".
        # Droppers have slots 0-8, with 4 being the center slot.
        # We need to not only check for the presence of the right ingredients,
        # but also the absence of any items in empty slots.
        # We first need to allow the placing of custom crafters.
        # We do this by giving a spawn egg which spawns the item display, it also sets the block.
        # Then, every tick, we check if something's been crafted, or if the block has been broken.
        # If it has, remove the item display and give them the spawn egg back.
        # ========================================================================================
        tag_name = f"{self.internal_name}_custom_crafter"
        on_tick_block_management = [
            # Manages placing and breaking of the block (we use double because Python/JSON convert Python floats to Java doubles in Custom item, so won't make the same item)
            "# Custom crafter block management (placing/breaking of the block):",
            f"execute at @e[type=item_display, tag={tag_name}, tag=placing] run setblock ~ ~ ~ dropper[facing=up]{{CustomName:'\"{self.crafter_name}\"'}}",
            f"tag @e[type=item_display, tag={tag_name}, tag=placing] remove placing",
            f"execute as @e[type=item_display, tag={tag_name}] at @s unless block ~ ~ ~ dropper[facing=up] run data modify entity @e[type=item,distance=..1,nbt={{Item:{{id:\"minecraft:dropper\"}}}},limit=1] Item set value {{id:\"minecraft:bat_spawn_egg\",count:1,components:{{\"custom_name\":'\"{self.crafter_name}\"',\"minecraft:entity_data\":{{id:\"minecraft:item_display\",Tags:[\"{tag_name}\",\"placing\"],Rotation:[0d,0d],brightness:{{sky:10,block:10}},transformation:{{left_rotation:[0d,0d,0d,1d],right_rotation:[0d,0d,0d,1d],translation:[0d,0.5d,0d],scale:[1.01d,1.01d,1.01d]}},item:{{id:\"minecraft:crafting_table\",count:1}}}}}}}}",
            f"execute as @e[type=item_display, tag={tag_name}] at @s unless block ~ ~ ~ dropper[facing=up] run kill @s",
        ]
        # ========================================================================================
        on_success_commands = []
        for recipe in self.recipes:
            execute_at_command = f"execute at @e[type=item_display, tag={tag_name}] "
            #
            item_checks = [
                f"if items block ~ ~ ~ container.{index} {self._deal_with_item_components(ingredient, pack_namespace)} " if ingredient not in ["minecraft:air", "air", ""]
                else f"unless data block ~ ~ ~ Items[{{Slot: {index}b}}] "
                for index, ingredient in enumerate(recipe.ingredients)
            ]
            #
            item_display_name = recipe.result.custom_name or recipe.result.base_item if isinstance(recipe.result, CustomItem) else recipe.result
            play_sound = f"run playsound {self.on_craft_sound.get_reference(pack_namespace) if isinstance(self.on_craft_sound, CustomSound) else self.on_craft_sound} master @a[distance=..10] ~ ~ ~ 1 1"
            play_sound_command = f"# {item_display_name} crafting command:\n" + execute_at_command + "".join(item_checks) + play_sound
            on_success_commands.append(play_sound_command)
            #
            result_component = json.dumps(recipe.result.to_dict(pack_namespace)) if isinstance(recipe.result, CustomItem) else "{}"
            set_slot_command = f"run data modify block ~ ~ ~ Items set value [{{Slot: 4b, id: \"{str(recipe.result)}\", count: 1b, components: {result_component}}}]"
            recipe_command = execute_at_command + "".join(item_checks) + set_slot_command
            on_success_commands.append(recipe_command)

        return MCFunction(f"on_tick_custom_crafter_{self.internal_name}", [
            *on_tick_block_management,
            "",
            "# And for custom crafting:",
            "\n\n".join(on_success_commands)
            ], ["custom_crafting"],
        )
