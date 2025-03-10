from dataclasses import dataclass
from typing import Any


@dataclass
class EnchantmentLevelBasedProvider:
    # https://minecraft.wiki/w/Enchantment_definition#Level-based_value

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplementedError("This method must be implemented by the subclass")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EnchantmentLevelBasedProvider":
        cls_ = ENCHANTMENT_LEVEL_BASED_PROVIDER_TO_CLASSES[data["type"]]
        return cls_.from_dict(data)


@dataclass
class LinearEnchantmentLevelBasedProvider(EnchantmentLevelBasedProvider):
    """The value is linearly increased (or decreased) per level. The final value is base + per_level_above_first * (level - 1)."""
    base: float  # Value to use for a level I enchantment
    per_level_above_first: float  # Amount added to the value for each level above the first.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:linear",
            "base": self.base,
            "per_level_above_first": self.per_level_above_first,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LinearEnchantmentLevelBasedProvider":
        return LinearEnchantmentLevelBasedProvider(
            base=data["base"],
            per_level_above_first=data["per_level_above_first"],
        )


@dataclass
class LevelsSquaredEnchantmentLevelBasedProvider(EnchantmentLevelBasedProvider):
    """The value is based on the square of the level. The final value is level ^ 2 + added"""
    added: float  # Value to add to the squared level

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:levels_squared",
            "added": self.added,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LevelsSquaredEnchantmentLevelBasedProvider":
        return cls(
            added=data["added"],
        )


@dataclass
class ClampedEnchantmentLevelBasedProvider(EnchantmentLevelBasedProvider):
    """Uses another level-based value and clamps the resulting value to the range [min, max]."""
    value: "EnchantmentLevelBasedProvider | float"  # Level-based value — input
    min: float  # The minimum value of the output
    max: float  # The maximum value of the output

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:clamped",
            "value": self.value.to_dict(pack_namespace) if isinstance(self.value, EnchantmentLevelBasedProvider) else self.value,
            "min": self.min,
            "max": self.max,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ClampedEnchantmentLevelBasedProvider":
        return cls(
            value=EnchantmentLevelBasedProvider.from_dict(data["value"]),
            min=data["min"],
            max=data["max"],
        )


@dataclass
class FractionEnchantmentLevelBasedProvider(EnchantmentLevelBasedProvider):
    """Calculates a fraction of 2 level-based values: numerator/denominator"""
    numerator: "EnchantmentLevelBasedProvider | float"  # Numerator of the fraction
    denominator: "EnchantmentLevelBasedProvider | float"  # Denominator of the fraction

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:fraction",
            "numerator": self.numerator.to_dict(pack_namespace) if isinstance(self.numerator, EnchantmentLevelBasedProvider) else self.numerator,
            "denominator": self.denominator.to_dict(pack_namespace) if isinstance(self.denominator, EnchantmentLevelBasedProvider) else self.denominator,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FractionEnchantmentLevelBasedProvider":
        return cls(
            numerator=data["numerator"] if isinstance(data["numerator"], float) else EnchantmentLevelBasedProvider.from_dict(data["numerator"]),
            denominator=data["denominator"] if isinstance(data["denominator"], float) else EnchantmentLevelBasedProvider.from_dict(data["denominator"]),
        )


@dataclass
class LookupEnchantmentLevelBasedProvider(EnchantmentLevelBasedProvider):
    """Directly defines the value for each level, with a fallback for levels that aren't directly defined"""
    values: list[float]  # List of values to use for each level, indexed by level - 1
    fallback: "EnchantmentLevelBasedProvider | float"  # Value to use when `values` doesn't define a value for the given level.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:lookup",
            "values": self.values,
            "fallback": self.fallback.to_dict(pack_namespace) if isinstance(self.fallback, EnchantmentLevelBasedProvider) else self.fallback,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LookupEnchantmentLevelBasedProvider":
        return cls(
            values=data["values"],
            fallback=data["fallback"] if isinstance(data["fallback"], float) else EnchantmentLevelBasedProvider.from_dict(data["fallback"]),
        )


ENCHANTMENT_LEVEL_BASED_PROVIDER_TO_CLASSES: dict[str, type["EnchantmentLevelBasedProvider"]] = {
    "minecraft:linear": LinearEnchantmentLevelBasedProvider,
    "minecraft:levels_squared": LevelsSquaredEnchantmentLevelBasedProvider,
    "minecraft:clamped": ClampedEnchantmentLevelBasedProvider,
    "minecraft:fraction": FractionEnchantmentLevelBasedProvider,
    "minecraft:lookup": LookupEnchantmentLevelBasedProvider,
}
