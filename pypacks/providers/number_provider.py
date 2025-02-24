from dataclasses import dataclass
from typing import Any


@dataclass
class NumberProvider:
    # https://minecraft.wiki/w/Loot_table#Number_provider
    ...

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError


@dataclass
class ConstantNumberProvider(NumberProvider):
    value: float | int

    def to_dict(self) -> dict[str, Any]:
        return {"type": "minecraft:constant", "value": self.value}


@dataclass
class UniformNumberProvider(NumberProvider):
    min: float | int
    max: float | int

    def to_dict(self) -> dict[str, Any]:
        return {"type": "minecraft:uniform", "min": self.min, "max": self.max}


@dataclass
class BinomialNumberProvider(NumberProvider):
    """A random number following a binomial distribution."""
    n: int  # Number provider. The amount of trials.
    p: float  # Number provider. The probability of success on an individual trial.

    def to_dict(self) -> dict[str, Any]:
        return {"type": "minecraft:binomial", "n": self.n, "p": self.p}


@dataclass
class ScoreboardNumberProvider(NumberProvider):
    target: str
    score: str
    scale: float | int = 1.0

    def to_dict(self) -> dict[str, Any]:
        return {"type": "minecraft:scoreboard", "target": {"target": self.target}, "score": self.score, "scale": self.scale}


@dataclass
class StorageNumberProvider(NumberProvider):
    storage: str
    path: str

    def to_dict(self) -> dict[str, Any]:
        return {"type": "minecraft:storage", "storage": self.storage, "path": self.path}
