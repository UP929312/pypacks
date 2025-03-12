from dataclasses import dataclass, field

from pypacks.resources.world_gen.biome import CustomBiome
from pypacks.resources.world_gen.structure import CustomStructure, SingleCustomStructure
from pypacks.resources.world_gen.structure_set import CustomStructureSet

@dataclass
class WorldGenResources:
    custom_biomes: list["CustomBiome"] = field(default_factory=list)
    custom_structures: list["CustomStructure | SingleCustomStructure"] = field(default_factory=list)
    custom_structure_sets: list["CustomStructureSet"] = field(default_factory=list)
