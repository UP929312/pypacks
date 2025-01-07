import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Any, TYPE_CHECKING, TypeAlias

from pypacks.utils import recursively_remove_nones_from_data

if TYPE_CHECKING:
    from pypacks.pack import Pack
    # from pypacks.resources.custom_item import CustomItem
    from pypacks.resources.custom_predicate import Predicate


@dataclass
class CustomEnchantment:
    # https://minecraft.wiki/w/Enchantment_definition
    internal_name: str
    description: dict[str, Any] | str  # A JSON text component - The description of the enchantment.
    exclusive_set: str | list[str] = field(repr=False, default_factory=list)  # One or more enchantments (an ID, a #tag, or an array containing IDs) - Enchantments that are incompatible with this enchantment
    supported_items: str | list[str] = field(repr=False, default_factory=list)  # One or more items (an ID, a #tag, or an array containing IDs) - Items on which this enchantment can be applied using an anvil or using the /enchant command.
    primary_items: str | list[str] = field(repr=False, default_factory=list)  # One or more items (an ID, a #tag, or an array containing IDs) - `MUST be a subset of supported_items` - Items for which this enchantment appears in an enchanting table. If empty, defaults to being the same as supported_items.
    weight: int = field(repr=False, default=1024)  # 1-1024 | Controls the probability of this enchantment when enchanting. The probability is determined weight/total weight * 100%, where total_weight is the sum of the weights of all available enchantments.
    max_level: int = field(repr=False, default=1)  # 1-255 | The maximum level of this enchantment.
    min_cost_base: int = field(repr=False, default=1)  # 1-100 | The minimum base cost of this enchantment in levels. The base cost range will be modified before use.
    per_level_increase_min: int = field(repr=False, default=1)  # 0-100 | The amount of levels added to the minimum for each level above level I.
    max_cost_base: int = field(repr=False, default=1)  # 1-100 | The maximum base cost of this enchantment in levels. The base cost range will be modified before use.
    per_level_increase_max: int = field(repr=False, default=1)  # 0-100 | The amount of levels added to the maximum for each level above level I.
    anvil_cost: int = field(repr=False, default=1)  # 0-100 |  The base cost when applying this enchantment to another item using an anvil. Halved when adding using a book, multiplied by the level of the enchantment.
    slots: list[Literal["any", "hand", "mainhand", "offhand", "armor", "feet", "legs", "chest", "head", "body"]] = field(default_factory=lambda: ["any"])  # List of equipment slots that this enchantment works in.
    effects: list["EnchantEffect"] = field(repr=False, default_factory=list)  #  Effect components - Controls the effect of the enchantment.

    datapack_subdirectory_name: str = field(init=False, repr=False, default="enchantment")

    def __post_init__(self) -> None:
        assert 0 < self.weight <= 1024, "Weight must be between 1 and 1024"
        assert 0 < self.max_level <= 255, "Max level must be between 1 and 255"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "description": self.description if isinstance(self.description, dict) else {"text": self.description},
            "exclusive_set": self.exclusive_set,
            "supported_items": self.supported_items,
            "primary_items": self.primary_items if self.primary_items else None,
            "weight": self.weight,
            "max_level": self.max_level,
            "min_cost": {
                "base": self.min_cost_base,
                "per_level_above_first": self.per_level_increase_min,
            },
            "max_cost": {
                "base": self.max_cost_base,
                "per_level_above_first": self.per_level_increase_max,
            },
            "anvil_cost": self.anvil_cost,
            "slots": self.slots,
            "effects": [effect.to_dict() for effect in self.effects],
        })

    def create_datapack_files(self, pack: "Pack") -> None:
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)


# ====================================================================================================================
# Enchantment effects
# ====================================================================================================================

ValueEffectComponentIdType = Literal[
    "minecraft:armor_effectiveness", "minecraft:damage", "minecraft:damage_protection", "minecraft:smash_damage_per_fallen_block",
    "minecraft:knockback", "minecraft:equipment_drops", "minecraft:ammo_use", "minecraft:projectile_piercing", "minecraft:block_experience",
    "minecraft:repair_with_xp", "minecraft:item_damage", "minecraft:projectile_count", "minecraft:trident_return_acceleration",
    "minecraft:projectile_spread", "minecraft:fishing_time_reduction", "minecraft:fishing_luck_bonus", "minecraft:mob_experience",
]

EntityEffectComponentIdType = Literal[
    "minecraft:hit_block", "minecraft:tick", "minecraft:projectile_spawned", "minecraft:post_attack",
]

@dataclass
class EnchantEffect:
    component_id: "ValueEffectComponentIdType"
    value_effect: "ValueEffect"  #  Determines how to modify the value.
    requirements: "Predicate | None" = None  # Determines when the effect is active. Cannot be of type `minecraft:reference` - all predicates must be in-lined
    enchanted: Literal["attacker", "victim"] = "victim"  # Which entity has to have the enchantment

    def to_dict(self) -> dict[str, Any]:
        return {
            self.component_id: {
                "effect": self.value_effect,
                "requirements": self.requirements.to_dict() if self.requirements else None,
                "enchanted": self.enchanted,
            }
        }


@dataclass
class SetEffect:
    """Sets the value to the specified value."""
    value: int | float  # Level based value determining the new value. - https://minecraft.wiki/w/Enchantment_definition#Level-based_value

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:set",
            "value": float(self.value),
        }


@dataclass
class AddEffect:
    """Adds the specified value to the old value."""
    value: int | float  # Level based value determining the value to add. - https://minecraft.wiki/w/Enchantment_definition#Level-based_value

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:add",
            "value": float(self.value),
        }


@dataclass
class MultiplyEffect:
    """Multiplies the old value with the specified factor."""
    factor: int | float  # Level based value determining the factor to multiply. - https://minecraft.wiki/w/Enchantment_definition#Level-based_value

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:multiply",
            "factor": float(self.factor),
        }


@dataclass
class RemoveBinomialEffect:
    """Runs multiple checks, each time reducing the value by 1 with the specified chance."""
    chance: float  # The chance to remove the value. - https://minecraft.wiki/w/Enchantment_definition#Level-based_value

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:remove_binomial",
            "chance": self.chance,
        }


@dataclass
class AnyOfEffect:
    """Runs multiple value effects in series."""
    effects: list["ValueEffect"]

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:any_of",
            "effects": [effect.to_dict() for effect in self.effects],
        }


ValueEffect: TypeAlias = SetEffect | AddEffect | MultiplyEffect | RemoveBinomialEffect | AnyOfEffect
