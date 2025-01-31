import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pypacks.pack import Pack
from pypacks.providers.int_provider import IntProvider
from pypacks.resources.custom_enchantment import CustomEnchantment

# TODO: These never get passed in anywhere/create_datapack_files ever ran...


@dataclass
class EnchantmentProvider:
    internal_name: str
    """BASE CLASS FOR ENCHANTMENT PROVIDERS, DON'T USE DIRECTLY"""
    # https://minecraft.wiki/w/Enchantment_provider
    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="enchantment_provider")

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplementedError("This method must be implemented by the subclass")
    
    def create_datapack_files(self, pack: "Pack") -> None:
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)


@dataclass
class SingleEnchantmentProvider(EnchantmentProvider):
    """Always returns the same enchantment"""
    internal_name: str
    enchantment: "str | CustomEnchantment"  # One enchantment (a string ID) - the enchantment to return
    level: "int | IntProvider"  #  The level of the enchantment

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
    internal_name: str
    enchantments: list["str | CustomEnchantment"]  # List of all possible enchantments
    cost: "int | IntProvider"  #  The cost to use to determine the enchantments

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
    internal_name: str
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
