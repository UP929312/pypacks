import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Generic, Literal, Any

from pypacks.resources.entities.entity_variant import GenericEntityVariant


if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.resources.entities.spawn_conditions import SpawnConditionType


@dataclass
class WolfVariant:
    internal_name: str
    angry_texture_path: str | Path = ""  # A path to the texture for the angry wolf
    wild_texture_path: str | Path = ""  # A path to the texture for the angry wolf
    tame_texture_path: str | Path = ""  # A path to the texture for the angry wolf
    spawn_conditions: dict[int, "SpawnConditionType"] = field(default_factory=dict)  # Mapping of priorty to spawn condition

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="wolf_variant")
    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="entity/wolf")
    entity_type: str = field(init=False, repr=False, hash=False, default="wolf")

    def __post_init__(self) -> None:
        self.internal_generic_entity_variant = GenericEntityVariant(
            internal_name=self.internal_name, texture_path=self.angry_texture_path, spawn_conditions=self.spawn_conditions
        )

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "assets": {
                "angry":  f"{pack_namespace}:entity/{self.entity_type}/{self.internal_name}_angry",
                "wild": f"{pack_namespace}:entity/{self.entity_type}/{self.internal_name}_wild",
                "tame": f"{pack_namespace}:entity/{self.entity_type}/{self.internal_name}_tame",
            },
            "spawn_conditions": [{
                "priority": key,
                "condition": value.to_dict(pack_namespace),
            } for key, value in self.spawn_conditions.items()] if self.spawn_conditions else [{"priority": 0}],
        }

    generate_spawn_command = GenericEntityVariant.generate_spawn_command 
    create_datapack_files = GenericEntityVariant.create_datapack_files

    def create_resource_pack_files(self, pack: "Pack") -> None:
        # Create and move the texture file
        entity_wolf_subdir = Path(pack.resource_pack_path)/"assets"/pack.namespace/"textures"/self.__class__.resource_pack_subdirectory_name
        os.makedirs(entity_wolf_subdir, exist_ok=True)
        for texture_path, state in zip([self.angry_texture_path, self.wild_texture_path, self.tame_texture_path], ["angry", "wild", "tame"]):
            shutil.copyfile(texture_path, entity_wolf_subdir/f"{self.internal_name}_{state}.png")
