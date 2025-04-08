from dataclasses import dataclass, field
from typing import Any

from pypacks.resources.base_resource import BaseResource
from pypacks.providers.int_provider import IntProvider
from pypacks.resources.custom_enchantment import CustomEnchantment

# TODO: These never get passed in anywhere/create_datapack_files ever ran...
# They live in their own folder, enchantment_provider, but I want a better way to create them I suppose
# than just a new Pack input.


@dataclass
class EnchantmentProvider(BaseResource):
    internal_name: str
    """BASE CLASS FOR ENCHANTMENT PROVIDERS, DON'T USE DIRECTLY"""
    # https://minecraft.wiki/w/Enchantment_provider
    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="enchantment_provider")

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplementedError("This method must be implemented by the subclass")

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "EnchantmentProvider":  # type: ignore[override]
        cls_ = ENCHANTMENT_PROVIDER_NAME_TO_CLASSES[data["type"]]
        return cls_(internal_name=internal_name, **data)


@dataclass
class SingleEnchantmentProvider(EnchantmentProvider):
    """Always returns the same enchantment"""
    enchantment: "str | CustomEnchantment"  # One enchantment (a string ID) - the enchantment to return
    level: "int | IntProvider"  # The level of the enchantment

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:single",
            "enchantment": self.enchantment.get_reference(pack_namespace) if isinstance(self.enchantment, CustomEnchantment) else self.enchantment,
            "level": self.level.to_dict() if isinstance(self.level, IntProvider) else self.level,
        }


@dataclass
class EnchantmentsByCostProvider(EnchantmentProvider):
    """Returns random enchantments from a list of possible enchantments, using a configured cost. Similar to the cost of an enchanting table."""
    # https://minecraft.wiki/w/Enchantment_provider
    enchantments: list["str | CustomEnchantment"]  # List of all possible enchantments
    cost: "int | IntProvider"  # The cost to use to determine the enchantments

    def to_dict(self,  pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:enchantments_by_cost",
            "enchantments": [x.get_reference(pack_namespace) if isinstance(x, CustomEnchantment) else x for x in self.enchantments],
            "cost": self.cost.to_dict() if isinstance(self.cost, IntProvider) else self.cost,
        }


@dataclass
class EnchantmentsByCostWithDifficultyProvider(EnchantmentProvider):
    """Works the same way as enchantments_by_cost but the cost is determined using the local difficulty of the area.
    The effective cost is calculated by min_cost + rand(0, local_difficulty_factor * max_cost_span). Where:
    - rand(a,b) refers to a random number between a and b.
    - local_difficulty_factor is: local_difficulty/2 - 1 clamped to a value between 0 and 1."""
    # https://minecraft.wiki/w/Enchantment_provider
    enchantments: list["str | CustomEnchantment"]  # List of all possible enchantments
    min_cost: int  # Minimum 1 - The base cost at local difficulty below 2.
    max_cost_span: int  # Minimum 0 - Factor of the uniform randomization range for local difficulty.

    def __post_init__(self) -> None:
        assert self.max_cost_span >= 0, "max_cost_span must be at least 0"
        assert self.min_cost >= 1, "min_cost must be at least 1"

    def to_dict(self,  pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:enchantments_by_cost_with_difficulty",
            "enchantments": [x.get_reference(pack_namespace) if isinstance(x, CustomEnchantment) else x for x in self.enchantments],
            "min_cost": self.min_cost,
            "max_cost_span": self.max_cost_span,
        }


ENCHANTMENT_PROVIDER_NAME_TO_CLASSES: dict[str, type["EnchantmentProvider"]] = {
    "single": SingleEnchantmentProvider,
    "enchantments_by_cost": EnchantmentsByCostProvider,
    "enchantments_by_cost_with_difficulty": EnchantmentsByCostWithDifficultyProvider,
}
