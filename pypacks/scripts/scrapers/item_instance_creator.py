import os
from dataclasses import dataclass, fields, MISSING
from typing import Any

import requests

# from pypacks.resources.custom_item import CustomItem
from pypacks.resources.custom_painting import CustomPainting
from pypacks.additions.item_components import AttributeModifier, Components, Equippable, Tool, Instrument, JukeboxPlayable
from pypacks.resources.custom_painting import ALL_DEFAULT_PAINTINGS


@dataclass
class FakePack:
    namespace: str = "minecraft"


def overriden_repr(self) -> str:
    # Retrieve the default values, handling both `default` and `default_factory`
    default_values = {}
    excluded_fields = set()

    for f in fields(self):
        if not f.init or not f.repr:  # Ignore fields with `init=False` or `repr=False`
            excluded_fields.add(f.name)
        
        # Handle both default values and default factories
        if f.default is not MISSING:
            default_values[f.name] = f.default
        elif f.default_factory is not MISSING:  # Handle default factories
            default_values[f.name] = f.default_factory()

    # Filter out attributes that:
    # 1. Are equal to their default value (including default_factory values)
    # 2. Are marked with `init=False` or `repr=False`
    non_default_attrs = {
        name: value for name, value in self.__dict__.items()
        if name not in excluded_fields and (name not in default_values or default_values[name] != value)
    }

    # If no non-default values exist, return just the class name
    if not non_default_attrs:
        return f"{self.__class__.__name__}()"

    # Format and return the non-default arguments
    return f"{self.__class__.__name__}(" + ", ".join(f"{k}={repr(v)}" for k, v in non_default_attrs.items()) + ")"


# CustomItem.__repr__ = overriden_repr
CustomPainting.__repr__ = overriden_repr
Instrument.__repr__ = overriden_repr
AttributeModifier.__repr__ = overriden_repr
Components.__repr__ = overriden_repr
Equippable.__repr__ = overriden_repr
Tool.__repr__ = overriden_repr
JukeboxPlayable.__repr__ = overriden_repr


def is_not_normal_item(data: dict[str, Any]) -> bool:
    return bool(
        data.get("minecraft:attribute_modifiers", {}).get("modifiers") or
        data.get("minecraft:enchantments", {}).get("levels") or
        data.get("minecraft:damage_resistant") or
        data.get("minecraft:jukebox_playable")
        # data.get("minecraft:enchantment_glint_override")  # Glistening melons
    )


def format_custom_item_name(item: str, base_item: str, components: Components, max_stack: int, rarity: str) -> str:
    max_stack_arg = (f"max_stack_size={max_stack}, ") if max_stack != 64 else ""
    rarity_arg = f"rarity=\"{rarity}\", " if (rarity != "common") else ""
    return (
        f"""{item.upper()} = CustomItem(internal_name="minecraft:{item.removeprefix("minecraft:").lower()}", base_item="{base_item}", """ +
        f"components={components}, {max_stack_arg}{rarity_arg})"""
    ).replace(", )", ")")


all_item_data: dict[str, Any] = requests.get("https://raw.githubusercontent.com/misode/mcmeta/1.21.4-summary/item_components/data.min.json").json()

lines = [
    "from pypacks.resources.custom_item import CustomItem",
    "from pypacks.additions.item_components import AttributeModifier, Components, EntityData, Equippable, Tool, ToolRule, Instrument, JukeboxPlayable",
    "",
]
items = []
for item, data in all_item_data.items():
    if is_not_normal_item(data):
        # rint(item, data)
        attribute_modifiers = [AttributeModifier.from_dict(modifier) for modifier in data.get("minecraft:attribute_modifiers", {}).get("modifiers")]
        tool = Tool.from_dict(data["minecraft:tool"]) if data.get("minecraft:tool") else None
        equippable = Equippable.from_dict(data["minecraft:equippable"]) if data.get("minecraft:equippable") else None
        damage_resistance = data["minecraft:damage_resistant"]["types"] if data.get("minecraft:damage_resistant") else None
        enchantable = data["minecraft:enchantable"]["value"] if data.get("minecraft:enchantable", {}).get("value") else None
        jukebox_playable = JukeboxPlayable.from_dict(data["minecraft:jukebox_playable"]) if data.get("minecraft:jukebox_playable") else None

        repaired_by: list[str] = [data["minecraft:repairable"]["items"]] if data.get("minecraft:repairable") else []

        components = Components(
            attribute_modifiers=attribute_modifiers, tool=tool, equippable=equippable, damage_resistant_to=damage_resistance,
            repaired_by=repaired_by, enchantable_at_level=enchantable, jukebox_playable=jukebox_playable,
        )
        line = format_custom_item_name(item, item, components, data["minecraft:max_stack_size"], data.get("minecraft:rarity"))
        # custom_item = CustomItem(internal_name=f"minecraft:{item.removeprefix('minecraft:')}", base_item=item, components=components, max_stack_size=data["minecraft:max_stack_size"], rarity=data.get("minecraft:rarity"))
        items.append(item.upper())
        lines.append(line)


# TODO: Consumable/Food
# use_cooldown, use_remainder, `damage`, death_protection, max_damage

# {'minecraft:item_model', 'minecraft:use_cooldown', 'minecraft:ominous_bottle_amplifier', 'minecraft:container', 'minecraft:repairable',
# 'minecraft:map_color', 'minecraft:map_decorations', 'minecraft:enchantment_glint_override', 'minecraft:block_state', 'minecraft:bundle_contents',
# 'minecraft:debug_stick_state', 'minecraft:enchantable', 'minecraft:glider', 'minecraft:use_remainder', 'minecraft:bees', 'minecraft:item_name',
# 'minecraft:potion_contents', 'minecraft:food', 'minecraft:stored_enchantments', 'minecraft:bucket_entity_data', 'minecraft:charged_projectiles',
# 'minecraft:equippable', 'minecraft:suspicious_stew_effects', 'minecraft:max_stack_size', 'minecraft:damage', 'minecraft:rarity', 'minecraft:recipes',
# 'minecraft:attribute_modifiers', 'minecraft:death_protection', 'minecraft:banner_patterns', 'minecraft:tool', 'minecraft:pot_decorations',
# 'minecraft:max_damage', 'minecraft:lore', 'minecraft:repair_cost', 'minecraft:jukebox_playable', 'minecraft:writable_book_content'
#  'minecraft:damage_resistant', 'minecraft:consumable', 'minecraft:enchantments', 'minecraft:fireworks'}

# ====================================================================================================================
GOAT_HORN_NAMES = ["Ponder", "Sing", "Seek", "Feel", "Admire", "Call", "Yearn", "Dream"]
for goat_horn_sound_index, name in enumerate(GOAT_HORN_NAMES):
    components = Components(instrument=Instrument(f"minecraft:item.goat_horn.sound.{goat_horn_sound_index}"))
    items.append(f"GOAT_HORN_{name.upper()}")
    lines.append(format_custom_item_name(f"GOAT_HORN_{name.upper()}", "minecraft:goat_horn", components, 1, 'common'))
# ====================================================================================================================
# Paintings
for painting in ALL_DEFAULT_PAINTINGS:
    painting_item = painting.generate_custom_item(FakePack())  # type: ignore[abc]
    items.append(painting_item.internal_name.upper()+"_PAINTING")
    lines.append(format_custom_item_name(painting_item.internal_name+"_PAINTING", "minecraft:painting", painting_item.components, 1, 'common'))

output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\scripts\\repos\\all_item_instances.py"
with open(output_path, "w") as file:
    file.write("\n".join(lines)+"\n\n")
    file.write("DEFAULT_ITEMS = {\n" +
               "".join([f"    \"{x}\": {x},\n" for x in items]) +
               "}\n")
