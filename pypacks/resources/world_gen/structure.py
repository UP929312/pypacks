
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
from typing import Any, Literal, TYPE_CHECKING

from pypacks.resources.world_gen.entity_spawner import SpawnOverride
from pypacks.utils import recursively_remove_nones_from_data

if TYPE_CHECKING:
    from pypacks.resources.world_gen.biome import CustomBiome
    from pypacks.resources.world_gen.structure_set import CustomStructureSet
    from pypacks.resources.custom_item import CustomItem
    from pypacks.resources.world_gen.entity_spawner import DisableSpawnOverrideCategory
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
    path_to_nbt_file: Path | str
    biomes_to_spawn_in: "list[str | CustomBiome]" = field(default_factory=list)  # Biomes that this structure is allowed to generate in.

    datapack_subdirectory_name: str = field(init=False, repr=False, default="worldgen/structure")

    def get_reference(self, pack_namespace: str) -> str:
        return f"{pack_namespace}:{self.internal_name}"

    def create_children(self, pack_namespace: str) -> tuple["CustomStructure", "CustomStructureSet", "SingleItemTemplatePool"]:
        from pypacks.resources.world_gen.biome import CustomBiome
        from pypacks.resources.world_gen.structure_set import CustomStructureSet
        custom_structure = CustomStructure(
            self.internal_name,
            structure_type=JigsawStructureType(
                self.get_reference(pack_namespace),
                size=1,
                start_height=0,
                project_start_to_heightmap="WORLD_SURFACE_WG",
            ),
            biomes_to_spawn_in=[biome.get_reference(pack_namespace) if isinstance(biome, CustomBiome) else biome for biome in self.biomes_to_spawn_in],
            generation_step="surface_structures",
            terrain_adaptation="beard_thin",
        )
        custom_structure_set = CustomStructureSet(self.internal_name, {custom_structure.get_reference(pack_namespace): 1})
        single_item_template_pool = SingleItemTemplatePool(self.internal_name, self.get_reference(pack_namespace))
        return custom_structure, custom_structure_set, single_item_template_pool

    def create_datapack_files(self, pack: "Pack") -> None:
        custom_structure, custom_structure_set, single_item_template_pool = self.create_children(pack.namespace)
        custom_structure.create_datapack_files(pack)
        custom_structure_set.create_datapack_files(pack)
        single_item_template_pool.create_datapack_files(pack)

        os.makedirs(Path(pack.datapack_output_path)/"data"/pack.namespace/"structure", exist_ok=True)
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/"structure"/f"{self.internal_name}.nbt", "wb") as file:
            file.write(Path(self.path_to_nbt_file).read_bytes())

    def generate_custom_item(self, pack_namespace: str) -> "CustomItem":
        from pypacks.additions.raycasting import BlockRaycast
        from pypacks.resources.custom_item import CustomItem
        from pypacks.additions.item_components import Components, Cooldown
        from pypacks.additions.reference_book_config import DEV_ITEMS_REF_BOOK_CONFIG
        block_raycast = BlockRaycast(
            self.internal_name+"_structure_placer_raycast",
            on_block_hit_command=f"place template {self.get_reference(pack_namespace)} ~ ~1 ~",
            no_blocks_hit_command="say Oops, something went wrong!",
            max_distance_in_blocks=20,
        )
        return CustomItem(
            self.internal_name+"_structure_placer", "minecraft:stick", f"Structure Placer ({self.internal_name})",
            on_right_click=block_raycast, components=Components(cooldown=Cooldown(0.3)),
            ref_book_config=DEV_ITEMS_REF_BOOK_CONFIG,
        )


@dataclass
class JigsawStructureType:
    start_pool: str
    size: int = 1  # The depth of jigsaw structures to generate.
    start_height: int = 0
    project_start_to_heightmap: Literal["WORLD_SURFACE_WG", "WORLD_SURFACE", "OCEAN_FLOOR_WG", "OCEAN_FLOOR", "WORLD_SURFACE_WG", "WORLD_SURFACE", "OCEAN_FLOOR_WG", "OCEAN_FLOOR"] = "WORLD_SURFACE_WG"  # WG = Exclusively during World Gen
    max_distance_from_center: int = 80
    apply_waterlogging: bool = True

    def to_dict(self) -> dict[str, Any]:
        assert 0 <= self.size <= 20, "Size must be between 0 and 20"
        assert 1 <= self.max_distance_from_center <= 128, "Max distance from center must be between 1 and 128"
        return {
            "type": "minecraft:jigsaw",
            "start_pool": self.start_pool,
            "size": self.size,
            "start_height": {"absolute": self.start_height},  # TODO: Height provider
            "project_start_to_heightmap": self.project_start_to_heightmap,
            "max_distance_from_center": self.max_distance_from_center,
            "use_expansion_hack": False,
            "liquid_settings": "apply_waterlogging" if self.apply_waterlogging else "ignore_waterlogging",
        }


@dataclass
class SingleItemTemplatePool:
    internal_name: str
    element_type: str

    def to_dict(self) -> dict[str, Any]:
        assert ":" in self.element_type, "Element type must be in the format 'namespace:element'"
        self.weight = 1
        assert 1 <= self.weight <= 150, "Weight must be between 1 and 150"
        return {
            "fallback": "minecraft:empty",
            "elements": [
                {
                    "weight": self.weight,
                    "element": {
                        "element_type": "minecraft:single_pool_element",
                        "location": self.element_type,
                        "projection": "rigid",
                        # "processors": {"processors": []},  # TODO: Look into this
                        "processors": "minecraft:empty",
                    }
                }
            ]
        }

    def create_datapack_files(self, pack: "Pack") -> None:
        os.makedirs(Path(pack.datapack_output_path)/"data"/pack.namespace/"worldgen/template_pool", exist_ok=True)
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/"worldgen/template_pool"/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(), file, indent=4)

# ============================================================================================================


@dataclass
class GameTestStructure:
    internal_name: str
    path_to_structure_nbt: Path | str

    datapack_subdirectory_name: str = field(init=False, repr=False, default="worldgen/structure")

    def create_datapack_files(self, pack: "Pack") -> None:
        structure = SingleCustomStructure(self.internal_name, self.path_to_structure_nbt)
        structure.create_datapack_files(pack)
        # os.makedirs(Path(pack.datapack_output_path)/"data"/pack.namespace/"structure", exist_ok=True)
        # with open(Path(pack.datapack_output_path)/"data"/pack.namespace/"structure"/f"{self.internal_name}.nbt", "wb") as file:
        #     file.write(Path(self.path_to_structure_nbt).read_bytes())

    @classmethod
    def from_single_custom_structure(cls, single_custom_structure: SingleCustomStructure) -> "GameTestStructure":
        return cls(single_custom_structure.internal_name, single_custom_structure.path_to_nbt_file)

    def get_reference(self, pack_namespace: str) -> str:
        return f"{pack_namespace}:{self.internal_name}"
