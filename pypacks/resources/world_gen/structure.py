
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
from typing import Any, Literal, TYPE_CHECKING

from pypacks.resources.world_gen.entity_spawner import SpawnOverride, DisableSpawnOverrideCategory
from pypacks.utils import recursively_remove_nones_from_data

if TYPE_CHECKING:
    from pypacks.resources.world_gen.biome import CustomBiome
    from pypacks.pack import Pack

# TODO: I need to properly implement Structure type, so I can give the arguments for jigsaws and such.
# Also, need to take the nbt and put it in /structure in the datapack (apart from for simple structures)


@dataclass(frozen=True)
class CustomStructure:
    """A structure is a large decoration, covering an area up to 256x256x256 block centered on the structure start.
    Structures often consist of multiple pieces that are fit together to form the overall structure. 
    N.b. To generate in a world, a structure needs to be part of at least one structure set."""
    # https://minecraft.wiki/w/Structure_definition
    internal_name: str
    structure_type: "JigsawStructureType"
    biomes_to_spawn_in: list[str] | str  # One or more biome(s) (an  ID, #tag, or a list containing  IDs) - Biomes that this structure is allowed to generate in.
    generation_step: Literal[
        "raw_generation", "lakes", "local_modifications", "underground_structures", "surface_structures", "strongholds", "underground_ores", "underground_decoration", "fluid_springs", "vegetal_decoration", "top_layer_modification"
    ] = "surface_structures"  # The step where the structure generates.  See also the features field in custom biome. Structure features are generated prior to features in the same step
    terrain_adaptation: Literal["none", "beard_thin", "beard_box", "bury", "encapsulate"] = "none"  # The type of terrain adaptation used for the structure. none for no adaptation, beard_thin is used by pillager outposts and villages, beard_box is used by ancient cities, bury is used by strongholds, and encapsulate is used by Trial Chambers.
    entity_spawn_overrides: list["SpawnOverride | DisableSpawnOverrideCategory"] = field(default_factory=list)  # Overrides the mobs that can spawn in this structure. Used for things like blaze and wither skeleton spawning in nether fortresses, and can also be used to block mobs from spawning like in ancient cities. Empty means no overrides.

    datapack_subdirectory_name: str = field(init=False, repr=False, default="worldgen/structure")

    def get_reference(self, pack_namespace: str) -> str:
        return f"{pack_namespace}:{self.internal_name}"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            **self.structure_type.to_dict(),
            "biomes": self.biomes_to_spawn_in,
            "step": self.generation_step,
            "terrain_adaptation": self.terrain_adaptation if self.terrain_adaptation != "none" else None,
            "spawn_overrides": SpawnOverride.combine_spawn_overrides(self.entity_spawn_overrides),
        })

    def create_datapack_files(self, pack: "Pack") -> None:
        # If created via the CustomStructureSet, the subdirs might not exist
        os.makedirs(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name, exist_ok=True)

        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)


@dataclass
class SingleCustomStructure:
    """A single structure, most of the work is done for you."""
    internal_name: str
    biomes_to_spawn_in: "list[str | CustomBiome] | str"  # One or more biome(s) (an  ID, #tag, or a list containing  IDs) - Biomes that this structure is allowed to generate in.
    path_to_nbt_file: Path | str

    datapack_subdirectory_name: str = field(init=False, repr=False, default="worldgen/structure")

    def get_reference(self, pack_namespace: str) -> str:
        return f"{pack_namespace}:{self.internal_name}"

    def create_datapack_files(self, pack: "Pack") -> None:
        from pypacks.resources.world_gen.biome import CustomBiome
        from pypacks.resources.world_gen.structure_set import CustomStructureSet
        biomes = self.biomes_to_spawn_in if isinstance(self.biomes_to_spawn_in, list) else [self.biomes_to_spawn_in]
        custom_structure = CustomStructure(
            self.internal_name,
            structure_type=JigsawStructureType(
                self.get_reference(pack.namespace),
                size=1,
                start_height=0,
                project_start_to_heightmap="WORLD_SURFACE_WG",
            ),
            biomes_to_spawn_in=[biome.get_reference(pack.namespace) if isinstance(biome, CustomBiome) else biome for biome in biomes],
            generation_step="surface_structures",
            terrain_adaptation="beard_thin",
        )
        custom_structure.create_datapack_files(pack)
        CustomStructureSet(self.internal_name, {custom_structure.get_reference(pack.namespace): 1}).create_datapack_files(pack)
        SingleItemTemplatePool(self.internal_name, self.get_reference(pack.namespace)).create_datapack_files(pack)

        os.makedirs(Path(pack.datapack_output_path)/"data"/pack.namespace/"structure", exist_ok=True)
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/"structure"/f"{self.internal_name}", "wb") as file:
            file.write(Path(self.path_to_nbt_file).read_bytes())


@dataclass
class JigsawStructureType:
    start_pool: str
    size: int = 1  # The depth of jigsaw structures to generate.
    start_height: int = 0
    project_start_to_heightmap: Literal["WORLD_SURFACE_WG", "WORLD_SURFACE", "OCEAN_FLOOR_WG", "OCEAN_FLOOR", "WORLD_SURFACE_WG", "WORLD_SURFACE", "OCEAN_FLOOR_WG", "OCEAN_FLOOR"] = "WORLD_SURFACE_WG"  # WG = Exclusively during World Gen
    max_distance_from_center: int = 80

    def to_dict(self) -> dict[str, Any]:
        assert self.size <= 20, "Size must be between 0 and 20"
        return {
            "type": "minecraft:jigsaw",
            "start_pool": self.start_pool,
            "size": self.size,
            "start_height": {"absolute": self.start_height},
            "project_start_to_heightmap": self.project_start_to_heightmap,
            "max_distance_from_center": self.max_distance_from_center,
            "use_expansion_hack": False,
        }


@dataclass
class SingleItemTemplatePool:
    internal_name: str
    element_type: str

    def to_dict(self) -> dict[str, Any]:
        assert ":" in self.element_type, "Element type must be in the format 'namespace:element'"
        return {
            "fallback": "minecraft:empty",
            "elements": [
                {
                    "weight": 1,  # 1-150
                    "element": {
                        "element_type": "minecraft:single_pool_element",
                        "location": self.element_type,
                        "projection": "rigid",
                        "processors": {"processors": []},
                    }
                }
            ]
        }

    def create_datapack_files(self, pack: "Pack") -> None:
        os.makedirs(Path(pack.datapack_output_path)/"data"/pack.namespace/"worldgen/template_pool", exist_ok=True)
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/"worldgen/template_pool"/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(), file, indent=4)
