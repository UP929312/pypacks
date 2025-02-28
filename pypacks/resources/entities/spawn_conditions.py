from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeAlias, Any


if TYPE_CHECKING:
    from pypacks.resources.world_gen.structure import CustomStructure
    from pypacks.resources.world_gen.biome import CustomBiome


@dataclass
class BiomeSpawnCondition:
    biomes: list["str | CustomBiome"]

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        from pypacks.resources.world_gen.biome import CustomBiome
        return {
            "type": "biome",
            "biomes": [biome.get_reference(pack_namespace) if isinstance(biome, CustomBiome) else biome for biome in self.biomes],
        }


@dataclass
class StructureSpawnCondition:
    structures: list["str | CustomStructure"]

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        from pypacks.resources.world_gen.structure import CustomStructure
        return {
            "type": "structure",
            "structures": [structure.get_reference(pack_namespace) if isinstance(structure, CustomStructure) else structure for structure in self.structures],
        }


@dataclass
class MoonBrightnessSpawnCondition:
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


SpawnConditionType: TypeAlias = BiomeSpawnCondition | StructureSpawnCondition | MoonBrightnessSpawnCondition
