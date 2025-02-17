from dataclasses import dataclass
from typing import Any, TypeAlias


@dataclass
class ConstantFloatProvider:
    value: float  # The constant value to use.

    def to_dict(self) -> dict[str, Any]:
        return {"type": "constant", "value": self.value}


@dataclass
class UniformFloatProvider:
    min_inclusive: float  # The minimum possible value.
    max_exclusive: float  # The maximum possible value. Cannot be less than min_inclusive.

    def __post_init__(self) -> None:
        assert self.min_inclusive <= self.max_exclusive, "max_inclusive cannot be less than min_inclusive"

    def to_dict(self) -> dict[str, Any]:
        return {"type": "uniform", "min_inclusive": self.min_inclusive, "max_exclusive": self.max_exclusive}


@dataclass
class ClampedNormalFloatProvider:
    mean: float | int  # The mean value of the normal distribution.
    deviation: float | int  # The deviation of the normal distribution.
    min_inclusive: int  # The minimum allowed value that the number will be.
    max_inclusive: int  # The maximum allowed value that the number will be.

    def __post_init__(self) -> None:
        assert self.min_inclusive <= self.max_inclusive, "max_inclusive cannot be less than min_inclusive"

    def to_dict(self) -> dict[str, Any]:
        return {"type": "clamped_normal", "mean": self.mean, "deviation": self.deviation, "min": self.min_inclusive, "max": self.max_inclusive}


@dataclass
class TrapezoidFloatProvider:
    min_inclusive: float
    max_inclusive: float
    plateau: float  # The range in the middle of the trapezoid distribution that has a uniform distribution. Must be less than or equal to max - min

    def __post_init__(self) -> None:
        assert self.min_inclusive <= self.max_inclusive, "max_inclusive cannot be less than min_inclusive"
        assert self.plateau <= self.max_inclusive - self.min_inclusive, "plateau cannot be greater than max - min"

    def to_dict(self) -> dict[str, Any]:
        return {"type": "trapezoid", "min": self.min_inclusive, "max": self.max_inclusive, "plateau": self.plateau}


FloatProvider: TypeAlias = ConstantFloatProvider | UniformFloatProvider | ClampedNormalFloatProvider | TrapezoidFloatProvider
