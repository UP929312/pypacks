import os
import re
from typing import Any

from pypacks.scripts.default_dictionary import DEFAULT_OBJECT_JSON
from pypacks.resources.custom_item import CustomItem
from pypacks.resources.item_components import AttributeModifier, Components, Equippable, Tool

EMPTY_PATTERN = re.compile(r"[A-Za-z_]*=(None|{}|\[]|False), ")

def is_not_normal_item(data: dict[str, Any]) -> bool:
    return bool(
        data.get("minecraft:attribute_modifiers", {}).get("modifiers") or
        data.get("minecraft:enchantments", {}).get("levels") or
        data.get("minecraft:damage_resistant")
        # data.get("minecraft:enchantment_glint_override")
    )

def is_tool_item(data: dict[str, Any]) -> bool:
    return bool(data.get("minecraft:enchantable"))



lines = [
    "from pypacks.resources.custom_item import CustomItem",
    "from pypacks.resources.item_components import AttributeModifier, Components, Equippable, Tool, ToolRule",
    ""
]
items = []
for item, data in DEFAULT_OBJECT_JSON.items():
    if is_not_normal_item(data):
        # print(item, data)
        attribute_modifiers = [AttributeModifier.from_dict(modifier) for modifier in data.get("minecraft:attribute_modifiers", {}).get("modifiers")]
        tool = Tool.from_dict(data["minecraft:tool"]) if data.get("minecraft:tool") else None
        equippable = Equippable.from_dict(data["minecraft:equippable"]) if data.get("minecraft:equippable") else None
        damage_resistance = data["minecraft:damage_resistant"]["types"] if data.get("minecraft:damage_resistant") else None
        enchantable = data["minecraft:enchantable"]["value"] if data.get("minecraft:enchantable", {}).get("value") else None
        repaired_by: list[str] | None = [data["minecraft:repairable"]["items"]] if data.get("minecraft:repairable") else []
        components = Components(
            attribute_modifiers=attribute_modifiers, tool=tool, equippable=equippable, damage_resistant_to=damage_resistance,
            repaired_by=repaired_by, enchantable_at_level=enchantable,
        )
        # ====
        components_string = re.sub(EMPTY_PATTERN, "", str(components)).replace(", writable_book_content=None", "")
        components_arg = f"components={components_string}, " if components_string else ""
        max_stack_arg = (f"max_stack_size={data['minecraft:max_stack_size']}, ") if data["minecraft:max_stack_size"] != 64 else ""
        rarity_arg = f"rarity=\"{data.get('minecraft:rarity')}\", " if (data.get("minecraft:rarity") != "common") else ""
        # ====
        line = (
            f"""{item.upper()} = CustomItem(internal_name="minecraft:{item.removeprefix("minecraft:")}", base_item="{item}", """+
            f"{components_arg}{max_stack_arg}{rarity_arg})"""
        ).replace(", )", ")")
        items.append(item.upper())
        lines.append(line)

output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\scripts\\all_item_instances.py"
with open(output_path, "w") as file:
    file.write("\n".join(lines)+"\n\n")
    file.write("DEFAULT_ITEMS = {\n" +
               "".join([f"    \"{x}\": {x},\n" for x in items]) +
               "}\n")
