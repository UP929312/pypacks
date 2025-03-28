
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from pypacks.utils import recursively_remove_nones_from_data
from pypacks.providers.int_provider import IntRange

if TYPE_CHECKING:
    from pypacks.additions.item_components import EnchantmentType


@dataclass
class DataComponentPredicate:
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplemented
     
    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "DataComponentPredicate":
        key = list(data.keys())[0]
        cls = DATA_COMPONENT_PREDICATE_NAME_TO_CLASSES[key]
        return cls.from_dict(internal_name, data[key])


# @dataclass
# class AttributeModifierPredicate(DataComponentPredicate):
#     attribute: str
#     operation: Literal["=", "<", "<=", ">", ">="]
#     amount: float
#     slot: Literal["mainhand", "offhand", "head", "chest", "legs", "feet", "any"] = "any"
#     id: str = None
#     name: str

#     def to_dict(self) -> dict[str, Any]:
#         return recursively_remove_nones_from_data({
#             "minecraft:attribute_modifiers": {
#                 "modifiers": {
#                     "contains": Attribute
#                     "attribute": self.attribute,
#                     "operation": self.operation,
#                     "amount": self.amount,
#                     "slot": self.slot,
#                     "id": self.id,
#                     "name": self.name
#                 }
#             }
            
#         })



@dataclass
class EnchantmentComponentPredicate(DataComponentPredicate):
    # TODO: Support custom tag here
    enchantments: list["EnchantmentType | str"] | None = None  # Any number of enchantments (or tag with #), If more than one enchantment is specified, succeeds when any one of them is present.
    levels: "IntRange | int | None" = None

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return recursively_remove_nones_from_data({
            "minecraft:enchantments": [
                {
                    "enchantments": self.enchantments,
                    "levels": self.levels.to_dict() if isinstance(self.levels, IntRange) else self.levels
                }
            ],
        })

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "EnchantmentComponentPredicate":
        return cls(
            enchantments=data["enchantments"],
            levels=IntRange.from_dict(data["levels"]) if "min" in data.get("levels", {})  else data.get("levels")
        )


DATA_COMPONENT_PREDICATE_NAME_TO_CLASSES = {
    "minecraft:enchantments": EnchantmentComponentPredicate
}
