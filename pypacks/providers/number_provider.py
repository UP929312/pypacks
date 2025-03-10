from dataclasses import dataclass
from typing import Any


@dataclass
class NumberProvider:
    # https://minecraft.wiki/w/Loot_table#Number_provider

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "NumberProvider":
        cls_ = NUMBER_PROVIDER_NAME_TO_CLASS[data["type"]]
        return cls_.from_dict(data)


@dataclass
class ConstantNumberProvider(NumberProvider):
    value: float | int

    def to_dict(self) -> dict[str, Any]:
        return {"type": "minecraft:constant", "value": self.value}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConstantNumberProvider":
        return cls(value=data["value"])


@dataclass
class UniformNumberProvider(NumberProvider):
    min: float | int
    max: float | int

    def to_dict(self) -> dict[str, Any]:
        return {"type": "minecraft:uniform", "min": self.min, "max": self.max}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UniformNumberProvider":
        return cls(min=data["min"], max=data["max"])


@dataclass
class BinomialNumberProvider(NumberProvider):
    """A random number following a binomial distribution."""
    n: int  # Number provider. The amount of trials.
    p: float  # Number provider. The probability of success on an individual trial.

    def to_dict(self) -> dict[str, Any]:
        return {"type": "minecraft:binomial", "n": self.n, "p": self.p}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BinomialNumberProvider":
        return cls(n=data["n"], p=data["p"])


@dataclass
class ScoreboardNumberProvider(NumberProvider):
    target: str
    score: str
    scale: float | int = 1.0

    def to_dict(self) -> dict[str, Any]:
        return {"type": "minecraft:scoreboard", "target": {"target": self.target}, "score": self.score, "scale": self.scale}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ScoreboardNumberProvider":
        return cls(target=data["target"]["target"], score=data["score"], scale=data.get("scale", 1.0))


@dataclass
class StorageNumberProvider(NumberProvider):
    storage: str
    path: str

    def to_dict(self) -> dict[str, Any]:
        return {"type": "minecraft:storage", "storage": self.storage, "path": self.path}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StorageNumberProvider":
        return cls(storage=data["storage"], path=data["path"])


NUMBER_PROVIDER_NAME_TO_CLASS: dict[str, type[NumberProvider]] = {
    "minecraft:constant": ConstantNumberProvider,
    "minecraft:uniform": UniformNumberProvider,
    "minecraft:binomial": BinomialNumberProvider,
    "minecraft:scoreboard": ScoreboardNumberProvider,
    "minecraft:storage": StorageNumberProvider,
}
