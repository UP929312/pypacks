from dataclasses import dataclass, field
from typing import Any


@dataclass
class NumberProvider:
    # https://minecraft.wiki/w/Loot_table#Number_provider
    ...


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
    n: float | int
    p: float

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