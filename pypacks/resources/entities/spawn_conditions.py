from dataclasses import dataclass
from typing import TYPE_CHECKING, Any


if TYPE_CHECKING:
    from pypacks.resources.world_gen.structure import CustomStructure
    from pypacks.resources.world_gen.biome import CustomBiome


class SpawnCondition:
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SpawnCondition":
        cls_ = SPAWN_CONDITION_TO_CLASSES[data["type"]]
        return cls_.from_dict(data)


@dataclass
class BiomeSpawnCondition(SpawnCondition):
    biomes: list["str | CustomBiome"]

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        from pypacks.resources.world_gen.biome import CustomBiome
        return {
            "type": "biome",
            "biomes": [biome.get_reference(pack_namespace) if isinstance(biome, CustomBiome) else biome for biome in self.biomes],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BiomeSpawnCondition":
        return cls(
            biomes=data["biomes"],
        )


@dataclass
class StructureSpawnCondition(SpawnCondition):
    structures: list["str | CustomStructure"]

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        from pypacks.resources.world_gen.structure import CustomStructure
        return {
            "type": "structure",
            "structures": [structure.get_reference(pack_namespace) if isinstance(structure, CustomStructure) else structure for structure in self.structures],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StructureSpawnCondition":
        return cls(
            structures=data["structures"],
        )


@dataclass
class MoonBrightnessSpawnCondition(SpawnCondition):
    min_brightness: float
    max_brightness: float

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "moon_brightness",
            "range": {
                "min": self.min_brightness,
                "max": self.max_brightness
            }
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MoonBrightnessSpawnCondition":
        return cls(
            min_brightness=data["range"]["min"],
            max_brightness=data["range"]["max"],
        )


SPAWN_CONDITION_TO_CLASSES: dict[str, type[SpawnCondition]] = {
    "biome": BiomeSpawnCondition,
    "structure": StructureSpawnCondition,
    "moon_brightness": MoonBrightnessSpawnCondition,
}
