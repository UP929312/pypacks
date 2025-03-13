import os
import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pypacks.resources.base_resource import BaseResource

if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.resources.entities.spawn_conditions import SpawnCondition


@dataclass
class GenericEntityVariant(BaseResource):
    internal_name: str
    texture_path: str | Path  # A path to the texture for the entity
    spawn_conditions: dict[int, "SpawnCondition | None"] = field(default_factory=dict)  # Mapping of priorty to spawn condition

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="x_variant")
    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="entity/x")
    entity_type: str = field(init=False, repr=False, hash=False, default="x")

    def get_reference(self, pack_namespace: str) -> str:
        return f"{pack_namespace}:{self.internal_name}"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "asset_id": f"{pack_namespace}:entity/{self.entity_type}/{self.internal_name}",
            "spawn_conditions": [{
                "priority": key,
                "condition": value.to_dict(pack_namespace) if value else None,
            } for key, value in self.spawn_conditions.items()] if self.spawn_conditions else [{"priority": 0}],
        }

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "GenericEntityVariant":
        # {'asset_id': 'pypacks_testing:entity/cat/sand_cat', 'spawn_conditions': [{'priority': 0}] }
        return cls(
            internal_name=internal_name,
            texture_path="", # data["texture_path"],  # TODO: Have no path, can maybe find it out later? By crawling through the resource pack?
            spawn_conditions={condition["priority"]: condition.get("condition") for condition in data["spawn_conditions"]},
        )

    def generate_give_spawn_egg_command(self, pack_namespace: str) -> str:
        return f"/give @s {self.entity_type}_spawn_egg[{self.entity_type}/variant=\"{self.get_reference(pack_namespace)}:\"]"

    def generate_summon_command(self, pack_namespace: str) -> str:
        return f"summon {self.entity_type} ~ ~ ~ {{\"variant\": \"{pack_namespace}:{self.internal_name}\"}}"

    def create_datapack_files(self, pack: "Pack") -> None:
        os.makedirs(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name, exist_ok=True)
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)

    def create_resource_pack_files(self, pack: "Pack") -> None:
        # Create and move the texture file
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/"textures"/self.__class__.resource_pack_subdirectory_name, exist_ok=True)
        shutil.copyfile(self.texture_path, Path(pack.resource_pack_path)/"assets"/pack.namespace/"textures"/self.__class__.resource_pack_subdirectory_name/f"{self.internal_name}.png")
