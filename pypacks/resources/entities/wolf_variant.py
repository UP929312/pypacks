import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pypacks.utils import recursively_remove_nones_from_data
from pypacks.resources.base_resource import BaseResource
from pypacks.resources.entities.entity_variant import GenericEntityVariant


if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.resources.entities.spawn_conditions import SpawnCondition


@dataclass
class WolfVariant(BaseResource):
    internal_name: str
    angry_texture_path: str | Path  # A path to the texture for the angry wolf
    wild_texture_path: str | Path  # A path to the texture for the angry wolf
    tame_texture_path: str | Path  # A path to the texture for the angry wolf
    spawn_conditions: dict[int, "SpawnCondition | None"] = field(default_factory=dict)  # Mapping of priorty to spawn condition

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="wolf_variant")
    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="entity/wolf")
    entity_type: str = field(init=False, repr=False, hash=False, default="wolf")

    def __post_init__(self) -> None:
        self.internal_generic_entity_variant = GenericEntityVariant(
            internal_name=self.internal_name, texture_path=self.wild_texture_path, spawn_conditions=self.spawn_conditions
        )

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "assets": {
                "angry":  f"{pack_namespace}:entity/{self.entity_type}/{self.internal_name}_angry",
                "wild": f"{pack_namespace}:entity/{self.entity_type}/{self.internal_name}_wild",
                "tame": f"{pack_namespace}:entity/{self.entity_type}/{self.internal_name}_tame",
            },
            "spawn_conditions": [{
                "priority": key,
                "condition": value.to_dict(pack_namespace) if value is not None else None,
            } for key, value in self.spawn_conditions.items()] if self.spawn_conditions else [{"priority": 0}],
        })

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "WolfVariant":
        return cls(
            internal_name=internal_name,
            angry_texture_path=data["assets"]["angry"].split(":")[1],
            wild_texture_path=data["assets"]["wild"].split(":")[1],
            tame_texture_path=data["assets"]["tame"].split(":")[1],
            spawn_conditions={condition["priority"]: condition.get("condition") for condition in data["spawn_conditions"]},
        )

    generate_give_spawn_egg_command = GenericEntityVariant.generate_give_spawn_egg_command
    generate_summon_command = GenericEntityVariant.generate_summon_command
    create_datapack_files = GenericEntityVariant.create_datapack_files

    def create_resource_pack_files(self, pack: "Pack") -> None:
        # Create and move the texture file
        entity_wolf_subdir = Path(pack.resource_pack_path)/"assets"/pack.namespace/"textures"/self.__class__.resource_pack_subdirectory_name
        os.makedirs(entity_wolf_subdir, exist_ok=True)
        for texture_path, state in zip([self.angry_texture_path, self.wild_texture_path, self.tame_texture_path], ["angry", "wild", "tame"]):
            shutil.copyfile(texture_path, entity_wolf_subdir/f"{self.internal_name}_{state}.png")
