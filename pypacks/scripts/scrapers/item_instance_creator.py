import os
from dataclasses import dataclass
from typing import Any

import requests

# from pypacks.resources.custom_item import CustomItem
from pypacks.resources.base_resource import overridden_repr
from pypacks.resources.custom_painting import CustomPainting
from pypacks.additions.item_components import (
    AttributeModifier, Components, Cooldown, Consumable, DeathProtection, EntityData, Equippable,
    Food, Instrument, JukeboxPlayable, PotionEffect, Tool, ToolRule, UseRemainder,
)
from pypacks.resources.custom_painting import ALL_DEFAULT_PAINTINGS


@dataclass
class FakePack:
    namespace: str = "minecraft"


for cls in [AttributeModifier, Cooldown, Components, Consumable, CustomPainting, DeathProtection, EntityData, Equippable,
            Food, Instrument, JukeboxPlayable, PotionEffect, Tool, ToolRule, UseRemainder]:  # CustomItem
    cls.__repr__ = overridden_repr  # type: ignore[assignment]


def is_not_normal_item(data: dict[str, Any]) -> bool:
    """Filters out items that aren't interesting, like stone blocks, interesting items have one or more of these attributes."""
    special_attributes = [
        "minecraft:damage_resistant", "minecraft:jukebox_playable", "minecraft:consumable", "minecraft:food", "minecraft:use_cooldown",
        "minecraft:use_remainder", "minecraft:death_protection", "minecraft:damage", "minecraft:max_damage", "minecraft:glider",
        "minecraft:tool", "minecraft:equippable", "minecraft:repairable",
    ]
    return bool(
        data.get("minecraft:attribute_modifiers", {}).get("modifiers") or
        data.get("minecraft:enchantments", {}).get("levels") or
        any(data.get(attr) for attr in special_attributes)
    )


def format_custom_item_name(item: str, base_item: str, components: Components, max_stack: int, rarity: str) -> str:
    """Converts a custom item to a string that can be used to create the item in the all_item_instances.py file."""
    max_stack_arg = (f"max_stack_size={max_stack}, ") if max_stack != 64 else ""
    rarity_arg = f"rarity=\"{rarity}\", " if (rarity != "common") else ""
    return (
        f"""{item.upper()} = CustomItem(internal_name="minecraft:{item.removeprefix("minecraft:").lower()}", base_item="{base_item}", """ +
        f"components={components}, {max_stack_arg}{rarity_arg})"""
    ).replace(", )", ")")


all_item_data: dict[str, Any] = requests.get("https://raw.githubusercontent.com/misode/mcmeta/1.21.4-summary/item_components/data.min.json").json()

lines = [
    "from pypacks.resources.custom_item import CustomItem",
    "from pypacks.additions.item_components import (",
    "    AttributeModifier, Components, Cooldown, Consumable, DeathProtection, EntityData, Equippable,",
    "    Food, Instrument, JukeboxPlayable, PotionEffect, Tool, ToolRule, UseRemainder,",
    ")",
    "",
]
items = []
for item, data in all_item_data.items():
    if is_not_normal_item(data):
        attribute_modifiers = [AttributeModifier.from_dict(modifier) for modifier in data.get("minecraft:attribute_modifiers", {}).get("modifiers")]
        tool = Tool.from_dict(data["minecraft:tool"]) if data.get("minecraft:tool") else None
        equippable = Equippable.from_dict(data["minecraft:equippable"]) if data.get("minecraft:equippable") else None
        damage_resistance = data["minecraft:damage_resistant"]["types"] if data.get("minecraft:damage_resistant") else None
        enchantable = data["minecraft:enchantable"]["value"] if data.get("minecraft:enchantable", {}).get("value") else None
        jukebox_playable = JukeboxPlayable.from_dict(data["minecraft:jukebox_playable"]) if data.get("minecraft:jukebox_playable") else None
        use_cooldown = Cooldown.from_dict(data["minecraft:use_cooldown"]) if data.get("minecraft:use_cooldown") else None
        use_remainder = UseRemainder.from_dict(data["minecraft:use_remainder"]) if data.get("minecraft:use_remainder") else None
        consumable = Consumable.from_dict(data["minecraft:consumable"]) if data.get("minecraft:consumable") else None
        food = Food.from_dict(data["minecraft:food"]) if data.get("minecraft:food") else None
        death_protection = DeathProtection.from_dict(data["minecraft:death_protection"]) if data.get("minecraft:death_protection") else None
        durability = data["minecraft:max_damage"] if data.get("minecraft:max_damage") else None
        lost_durability = data["minecraft:damage"] if data.get("minecraft:damage") else None
        glider = data["minecraft:glider"] == {} if data.get("minecraft:glider") else False

        repaired_by: list[str] = [data["minecraft:repairable"]["items"]] if data.get("minecraft:repairable") else []

        components = Components(
            attribute_modifiers=attribute_modifiers, tool=tool, equippable=equippable, damage_resistant_to=damage_resistance,
            repaired_by=repaired_by, enchantable_at_level=enchantable, jukebox_playable=jukebox_playable,
            cooldown=use_cooldown, use_remainder=use_remainder, food=food, death_protection=death_protection, consumable=consumable,
            durability=durability, lost_durability=lost_durability, glider=glider,
        )
        line = format_custom_item_name(item, item, components, data["minecraft:max_stack_size"], data.get("minecraft:rarity"))
        # custom_item = CustomItem(internal_name=f"minecraft:{item.removeprefix('minecraft:')}", base_item=item, components=components, max_stack_size=data["minecraft:max_stack_size"], rarity=data.get("minecraft:rarity"))
        items.append(item.upper())
        lines.append(line)

lines.append("\n# Manually added:")

# ====================================================================================================================
GOAT_HORN_NAMES = ["Ponder", "Sing", "Seek", "Feel", "Admire", "Call", "Yearn", "Dream"]
for goat_horn_sound_index, name in enumerate(GOAT_HORN_NAMES):
    components = Components(instrument=Instrument(f"minecraft:item.goat_horn.sound.{goat_horn_sound_index}"))
    items.append(f"GOAT_HORN_{name.upper()}")
    lines.append(format_custom_item_name(f"GOAT_HORN_{name.upper()}", "minecraft:goat_horn", components, 1, 'common'))
# ====================================================================================================================
for painting in ALL_DEFAULT_PAINTINGS:
    painting_item = painting.generate_custom_item(FakePack())  # type: ignore[arg-type]
    items.append(painting_item.internal_name.upper()+"_PAINTING")
    lines.append(format_custom_item_name(painting_item.internal_name+"_PAINTING", "minecraft:painting", painting_item.components, 1, 'common'))
# ====================================================================================================================
output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\minecraft\\items.py"
with open(output_path, "w", encoding="utf-8") as file:
    file.write("\n".join(lines)+"\n\n")
    file.write(
        "DEFAULT_ITEMS = {\n" +
        "".join([f"    \"{x}\": {x},\n" for x in items]) +
        "}\n"
    )
