from dataclasses import dataclass
from typing import Any


class IntProvider:
    """A class that represents a provider of an integer value."""
    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "IntProvider":
        cls_: type["IntProvider"] = INT_PROVIDER_NAME_TO_CLASS[data["type"].removeprefix("minecraft:")]
        return cls_.from_dict(data)


@dataclass
class ConstantIntProvider(IntProvider):
    value: int  # The constant value to use.

    def to_dict(self) -> dict[str, Any]:
        return {"type": "constant", "value": self.value}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConstantIntProvider":
        return cls(value=data["value"])


@dataclass
class IntRange:
    """Not used in the actual game, but used for defining ranges of integers in, say, custom ore generation."""
    min: int  # The minimum possible value.
    max: int  # The maximum possible value. Cannot be less than min.

    def __post_init__(self) -> None:
        assert self.min <= self.max, "max cannot be less than min"

    def to_dict(self) -> dict[str, Any]:
        return {"min": self.min, "max": self.max}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "IntRange":
        return cls(min=data["min"], max=data["max"])


@dataclass
class UniformIntProvider(IntProvider):
    min_inclusive: int  # The minimum possible value.
    max_inclusive: int  # The maximum possible value. Cannot be less than min_inclusive.

    def __post_init__(self) -> None:
        assert self.min_inclusive <= self.max_inclusive, "max_inclusive cannot be less than min_inclusive"

    def to_dict(self) -> dict[str, Any]:
        return {"type": "uniform", "min_inclusive": self.min_inclusive, "max_inclusive": self.max_inclusive}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UniformIntProvider":
        return cls(min_inclusive=data["min_inclusive"], max_inclusive=data["max_inclusive"])


@dataclass
class BiasedToBottomIntProvider(IntProvider):
    min_inclusive: int  # The minimum possible value.
    max_inclusive: int  # The maximum possible value. Cannot be less than min_inclusive.

    def __post_init__(self) -> None:
        assert self.min_inclusive <= self.max_inclusive, "max_inclusive cannot be less than min_inclusive"

    def to_dict(self) -> dict[str, Any]:
        return {"type": "biased_to_bottom", "min_inclusive": self.min_inclusive, "max_inclusive": self.max_inclusive}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BiasedToBottomIntProvider":
        return cls(min_inclusive=data["min_inclusive"], max_inclusive=data["max_inclusive"])


@dataclass
class ClampedIntProvider(IntProvider):
    min_inclusive: int  # The minimum allowed value that the number will be.
    max_inclusive: int  # The maximum allowed value that the number will be. Cannot be less than min_inclusive.
    source: "IntProvider | int"

    def __post_init__(self) -> None:
        assert self.min_inclusive <= self.max_inclusive, "max_inclusive cannot be less than min_inclusive"

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "clamped",
            "min_inclusive": self.min_inclusive,
            "max_inclusive": self.max_inclusive,
            "source": self.source.to_dict() if isinstance(self.source, IntProvider) else self.source
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ClampedIntProvider":
        return cls(min_inclusive=data["min_inclusive"], max_inclusive=data["max_inclusive"], source=IntProvider.from_dict(data["source"]))


@dataclass
class ClampedNormalIntProvider(IntProvider):
    mean: float | int  # The mean value of the normal distribution.
    deviation: float | int  # The deviation of the normal distribution.
    min_inclusive: int  # The minimum allowed value that the number will be.
    max_inclusive: int  # The maximum allowed value that the number will be.

    def __post_init__(self) -> None:
        assert self.min_inclusive <= self.max_inclusive, "max_inclusive cannot be less than min_inclusive"

    def to_dict(self) -> dict[str, Any]:
        return {"type": "clamped_normal", "mean": self.mean, "deviation": self.deviation, "min_inclusive": self.min_inclusive, "max_inclusive": self.max_inclusive}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ClampedNormalIntProvider":
        return cls(mean=data["mean"], deviation=data["deviation"], min_inclusive=data["min_inclusive"], max_inclusive=data["max_inclusive"])


@dataclass
class WeightedListIntProvider(IntProvider):
    providers: dict["IntProvider | int", int]  # A random pool of int providers and their weights.

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "weighted_list",
            "providers": [
                {"data": provider.to_dict() if isinstance(provider, IntProvider) else provider, "weight": weight}
                for provider, weight in self.providers.items()
            ]
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "WeightedListIntProvider":
        return cls(providers={
            IntProvider.from_dict(provider["data"]) if isinstance(provider["data"], dict) else provider["data"]: provider["weight"]
            for provider in data["providers"]
            }
        )


INT_PROVIDER_NAME_TO_CLASS = {
    "constant": ConstantIntProvider,
    "uniform": UniformIntProvider,
    "biased_to_bottom": BiasedToBottomIntProvider,
    "clamped": ClampedIntProvider,
    "clamped_normal": ClampedNormalIntProvider,
    "weighted_list": WeightedListIntProvider,
}
