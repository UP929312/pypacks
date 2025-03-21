from dataclasses import dataclass, field
from typing import Any, Literal


VerticalAnchor = Literal["absolute", "above_bottom", "below_top"]
# absolute: An absolute height as seen on the F3 screen.
# above_bottom: A relative height starting at the bottom of the world.
# below_top: A relative height starting at the top of the world. Higher values move the height down.

# https://minecraft.wiki/w/Custom_world_generation/height_provider


@dataclass(frozen=True)
class HeightProvider:
    """Used to specify a height."""
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HeightProvider":
        cls_ = HEIGHT_PROVIDER_NAME_TO_CLASSES[data["type"]]
        return cls_.from_dict(data)


@dataclass(frozen=True)
class ConstantHeightProvider(HeightProvider):
    """Used to specify a constant height."""
    value: int
    vertical_anchor: VerticalAnchor = "absolute"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "constant",
            "value": {self.vertical_anchor: self.value},
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConstantHeightProvider":
        key, value = list(data["value"].items())[0]
        return cls(
            value=key,
            vertical_anchor=value,
        )


@dataclass(frozen=True)
class UniformHeightProvider(HeightProvider):
    """Used to specify a random value in a uniform distribution"""
    min_inclusive: int = 64
    min_inclusive_anchor: VerticalAnchor = "absolute"
    max_inclusive: int = 128
    max_inclusive_anchor: VerticalAnchor = "absolute"

    def __post_init__(self) -> None:
        assert self.min_inclusive <= self.max_inclusive, "max_inclusive cannot be less than min_inclusive"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "uniform",
            "min_inclusive": {self.min_inclusive_anchor: self.min_inclusive},
            "max_inclusive": {self.max_inclusive_anchor: self.max_inclusive},
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UniformHeightProvider":
        min_key, min_value = list(data["min_inclusive"].items())[0]
        max_key, max_value = list(data["max_inclusive"].items())[0]
        return cls(
            min_inclusive=min_key,
            min_inclusive_anchor=min_value,
            max_inclusive=max_key,
            max_inclusive_anchor=max_value,
        )


@dataclass(frozen=True)
class BiasedToBottomHeightProvider(HeightProvider):
    """Used to specify a random value, biased towards the bottom"""
    min_inclusive: int = 64
    min_inclusive_anchor: VerticalAnchor = "absolute"
    max_inclusive: int = 128
    max_inclusive_anchor: VerticalAnchor = "absolute"
    inner: int = 1  # The inner value. Must be at least 1.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "biased_to_bottom",
            "min_inclusive": {self.min_inclusive_anchor: self.min_inclusive},
            "max_inclusive": {self.max_inclusive_anchor: self.max_inclusive},
            "inner": self.inner,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BiasedToBottomHeightProvider":
        min_key, min_value = list(data["min_inclusive"].items())[0]
        max_key, max_value = list(data["max_inclusive"].items())[0]
        return cls(
            min_inclusive=min_key,
            min_inclusive_anchor=min_value,
            max_inclusive=max_key,
            max_inclusive_anchor=max_value,
            inner=data["inner"],
        )


@dataclass(frozen=True)
class VeryBiasedToBottomHeightProvider(HeightProvider):
    """Used to specify a random value, biased towards the bottom"""
    min_inclusive: int = 64
    min_inclusive_anchor: VerticalAnchor = "absolute"
    max_inclusive: int = 128
    max_inclusive_anchor: VerticalAnchor = "absolute"
    inner: int = 1  # The inner value. Must be at least 1.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "very_biased_to_bottom",
            "min_inclusive": {self.min_inclusive_anchor: self.min_inclusive},
            "max_inclusive": {self.max_inclusive_anchor: self.max_inclusive},
            "inner": self.inner,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VeryBiasedToBottomHeightProvider":
        min_key, min_value = list(data["min_inclusive"].items())[0]
        max_key, max_value = list(data["max_inclusive"].items())[0]
        return cls(
            min_inclusive=min_key,
            min_inclusive_anchor=min_value,
            max_inclusive=max_key,
            max_inclusive_anchor=max_value,
            inner=data["inner"],
        )


@dataclass(frozen=True)
class TrapezoidHeightProvider(HeightProvider):
    """Used to specify a random value, isosceles trapezoidal distribution"""
    min_inclusive: int = 64
    min_inclusive_anchor: VerticalAnchor = "absolute"
    max_inclusive: int = 128
    max_inclusive_anchor: VerticalAnchor = "absolute"
    plateau: int = 0  # The length of the range in the middle of the trapezoid distribution that has a uniform distribution.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "trapezoid",
            "min_inclusive": {self.min_inclusive_anchor: self.min_inclusive},
            "max_inclusive": {self.max_inclusive_anchor: self.max_inclusive},
            "plateau": self.plateau,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TrapezoidHeightProvider":
        min_key, min_value = list(data["min_inclusive"].items())[0]
        max_key, max_value = list(data["max_inclusive"].items())[0]
        return cls(
            min_inclusive=min_key,
            min_inclusive_anchor=min_value,
            max_inclusive=max_key,
            max_inclusive_anchor=max_value,
            plateau=data["plateau"],
        )


@dataclass(frozen=True)
class WeightedListHeightProvider(HeightProvider):
    """Used to specify a random value from a weighted list"""
    distributions: dict["HeightProvider", int] = field(default_factory=lambda: {ConstantHeightProvider(0): 1})

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "weighted_list",
            "distribution": [
                {"data": height_provider.to_dict(pack_namespace), "weight": weight}
                for height_provider, weight in self.distributions.items()
            ],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WeightedListHeightProvider":
        return cls(
            distributions={
                HeightProvider.from_dict(d["data"]): d["weight"]
                for d in data["distribution"]
            }
        )


HEIGHT_PROVIDER_NAME_TO_CLASSES = {
    "constant": ConstantHeightProvider,
    "uniform": UniformHeightProvider,
    "biased_to_bottom": BiasedToBottomHeightProvider,
    "very_biased_to_bottom": VeryBiasedToBottomHeightProvider,
    "trapezoid": TrapezoidHeightProvider,
    "weighted_list": WeightedListHeightProvider,
}
