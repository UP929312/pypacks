from dataclasses import dataclass
from typing import Any, TypeAlias


@dataclass
class ConstantIntProvider:
    value: int  # The constant value to use.

    def to_dict(self) -> dict[str, Any]:
        return {"type": "constant", "value": self.value}


@dataclass
class UniformIntProvider:
    min_inclusive: int  # The minimum possible value.
    max_inclusive: int  # The maximum possible value. Cannot be less than min_inclusive.

    def to_dict(self) -> dict[str, Any]:
        assert self.min_inclusive <= self.max_inclusive, "max_inclusive cannot be less than min_inclusive"
        return {"type": "uniform", "min_inclusive": self.min_inclusive, "max_inclusive": self.max_inclusive}


@dataclass
class BiasedToBottomIntProvider:
    min_inclusive: int  # The minimum possible value.
    max_inclusive: int  # The maximum possible value. Cannot be less than min_inclusive.

    def to_dict(self) -> dict[str, Any]:
        assert self.min_inclusive <= self.max_inclusive, "max_inclusive cannot be less than min_inclusive"
        return {"type": "biased_to_bottom", "min_inclusive": self.min_inclusive, "max_inclusive": self.max_inclusive}


@dataclass
class ClampedIntProvider:
    min_inclusive: int  # The minimum allowed value that the number will be.
    max_inclusive: int  # The maximum allowed value that the number will be. Cannot be less than min_inclusive.
    source: "IntProvider | int"

    def to_dict(self) -> dict[str, Any]:
        assert self.min_inclusive <= self.max_inclusive, "max_inclusive cannot be less than min_inclusive"
        return {
            "type": "clamped",
            "min_inclusive": self.min_inclusive,
            "max_inclusive": self.max_inclusive,
            "source": self.source.to_dict() if isinstance(self.source, IntProvider) else self.source
        }


@dataclass
class ClampedNormalIntProvider:
    mean: float | int  # The mean value of the normal distribution.
    deviation: float | int  # The deviation of the normal distribution.
    min_inclusive: int  # The minimum allowed value that the number will be.
    max_inclusive: int  # The maximum allowed value that the number will be.

    def to_dict(self) -> dict[str, Any]:
        assert self.min_inclusive <= self.max_inclusive, "max_inclusive cannot be less than min_inclusive"
        return {"type": "clamped_normal", "mean": self.mean, "deviation": self.deviation, "min_inclusive": self.min_inclusive, "max_inclusive": self.max_inclusive}


@dataclass
class WeightedListIntProvider:
    providers: dict["IntProvider | int", int]  # A random pool of int providers and their weights.

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "weighted_list",
            "providers": [
                {"data": provider.to_dict() if isinstance(provider, IntProvider) else provider, "weight": weight}
                for provider, weight in self.providers.items()
            ]
        }



IntProvider: TypeAlias = ConstantIntProvider | UniformIntProvider | BiasedToBottomIntProvider | ClampedIntProvider | ClampedNormalIntProvider | WeightedListIntProvider

# If type is constant, additional fields are as follows:
#  value: The constant value to use.

# If type is uniform or biased_to_bottom, additional fields are as follows:
#  min_inclusive: The minimum possible value.
#  max_inclusive: The maximum possible value. Cannot be less than  min_inclusive.

# If type is clamped, additional fields are as follows:
#  min_inclusive: The minimum allowed value that the number will be.
#  max_inclusive: The maximum allowed value that the number will be. Cannot be less than  min_inclusive.
#  source: The source int provider
# Int provider[]

# If type is clamped_normal, additional fields are as follows:
#  mean: The mean value of the normal distribution.
#  deviation: The deviation of the normal distribution.
#  min_inclusive: The minimum allowed value that the number will be.
#  max_inclusive: The maximum allowed value that the number will be.

# If type is weighted_list, additional fields are as follows:
#  distribution: A random pool of int providers.
# : One entry in the random pool.
#  data: An int.
# Int provider[]
#  weight: The weight of this entry.