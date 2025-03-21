from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pypacks.resources.world_gen.biome import CustomBiome
    from pypacks.resources.world_gen.structure import CustomStructure, SingleCustomStructure
    from pypacks.resources.world_gen.structure_set import CustomStructureSet


@dataclass
class WorldGenResources:
    custom_biomes: list["CustomBiome"] = field(default_factory=list)
    custom_structures: list["CustomStructure | SingleCustomStructure"] = field(default_factory=list)
    custom_structure_sets: list["CustomStructureSet"] = field(default_factory=list)

    datapack_subdirectory_name: str = field(init=False, repr=False, default="worldgen")

    @classmethod
    def from_datapack_files(cls, root_path: "Path") -> "WorldGenResources":
        from pypacks.resources.world_gen.biome import CustomBiome
        from pypacks.resources.world_gen.structure import CustomStructure, SingleCustomStructure
        from pypacks.resources.world_gen.structure_set import CustomStructureSet
        return cls(
            custom_biomes=CustomBiome.from_datapack_files(root_path),
            custom_structures=CustomStructure.from_datapack_files(root_path),  # type: ignore[arg-type]
            custom_structure_sets=CustomStructureSet.from_datapack_files(root_path),
        )
