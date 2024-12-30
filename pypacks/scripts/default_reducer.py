from typing import Any

from pypacks.scripts.default_dictionary import DEFAULT_OBJECT_JSON
from pypacks.resources.custom_item import CustomItem
from pypacks.resources.item_components import AttributeModifier, Components, Tool, ToolRule


# "acacia_boat": {
#         "minecraft:attribute_modifiers": {
#             "modifiers": []
#         },
#         "minecraft:enchantments": {
#             "levels": {}
#         },
#         "minecraft:item_model": "minecraft:acacia_boat",
#         "minecraft:item_name": "{\"translate\":\"item.minecraft.acacia_boat\"}",
#         "minecraft:lore": [],
#         "minecraft:max_stack_size": 1,
#         "minecraft:rarity": "common",
#         "minecraft:repair_cost": 0
#     },

def is_normal_item(data: dict[str, Any]) -> bool:
    return (
        not data.get("minecraft:attribute_modifiers", {}).get("modifiers") and
        not data.get("minecraft:enchantments", {}).get("levels") and
        not data.get("minecraft:lore")
    )

lines = []
for item, data in DEFAULT_OBJECT_JSON.items():
    if not is_normal_item(data):
        print(item, data)
        a = CustomItem(
            internal_name=item.removeprefix("minecraft:"),
            base_item=item,  # type: ignore[abc]
            # custom_name=data.get("minecraft:item_name", {}),
            lore=data.get("minecraft:lore", []),
            max_stack_size=data.get("minecraft:max_stack_size", 64),
            rarity=data.get("minecraft:rarity"),
            # custom_data=data,
        )
        attribute_modifiers = [AttributeModifier.from_dict(modifier) for modifier in data.get("minecraft:attribute_modifiers", {}).get("modifiers")]
        tool = Tool(
                rules=[
                    ToolRule(
                        tool_rule.get("blocks", {}),
                        tool_rule.get("speed", 1.0),
                        tool_rule.get("correct_for_drops", False)
                    )
                    for tool_rule in data.get("minecraft:tool", {}).get("rules", {})
                ],
        ) if data.get("minecraft:tool") else None
        components_string = Components(attribute_modifiers=attribute_modifiers, tool=tool)
        lines.append(f"""
{item} = CustomItem(base_item="{item}", internal_name="minecraft:{item.removeprefix("minecraft:")}", components_string={components_string}, max_stack_size={data.get("minecraft:max_stack_size", 64)}, rarity="{data.get("minecraft:rarity")}")
""".strip("\n"))

# print("\n\n".join(lines))
