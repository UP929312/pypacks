import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pypacks.utils import recursively_remove_nones_from_data
from pypacks.resources.base_resource import BaseResource

if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.resources.entities.spawn_conditions import SpawnCondition
    # from pypacks.resources.custom_item import CustomItem


@dataclass
class GenericEntityVariant(BaseResource):
    internal_name: str
    texture_path: str | Path  # A path to the texture for the entity
    spawn_conditions: dict[int, "SpawnCondition | None"] = field(default_factory=dict)  # Mapping of priorty to spawn condition

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="x_variant")
    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="textures/entity/x")
    entity_type: str = field(init=False, repr=False, hash=False, default="x")

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "asset_id": f"{pack_namespace}:entity/{self.entity_type}/{self.internal_name}",
            "spawn_conditions": [{
                "priority": key,
                "condition": value.to_dict(pack_namespace) if value is not None else None,
            } for key, value in self.spawn_conditions.items()] if self.spawn_conditions else [{"priority": 0}],
        })

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "GenericEntityVariant":  # type: ignore[override]
        return cls(
            internal_name=internal_name,
            texture_path=data["asset_id"].split(":")[1]+".png",
            spawn_conditions={condition["priority"]: condition.get("condition") for condition in data["spawn_conditions"]},
        )

    def generate_give_spawn_egg_command(self, pack_namespace: str) -> str:
        return f"/give @s {self.entity_type}_spawn_egg[{self.entity_type}/variant=\"{self.get_reference(pack_namespace)}:\"]"

    def generate_summon_command(self, pack_namespace: str) -> str:
        return f"summon {self.entity_type} ~ ~ ~ {{\"variant\": \"{pack_namespace}:{self.internal_name}\"}}"

    @classmethod
    def from_combined_files(cls, data_path: "Path", assets_path: "Path") -> list["GenericEntityVariant"]:
        entity_variants: list["GenericEntityVariant"] = super().from_datapack_files(data_path)  # pyright: ignore
        for entity_variant in entity_variants:
            entity_variant.texture_path = assets_path/"textures"/entity_variant.texture_path
        return entity_variants

    def create_resource_pack_files(self, pack: "Pack") -> None:
        # Create and move the texture file
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name, exist_ok=True)
        shutil.copyfile(self.texture_path, Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name/f"{self.internal_name}.png")

    # def generate_custom_item(self, pack: "Pack") -> "CustomItem":  # Need to type variants!
    #     from pypacks.resources.custom_item import CustomItem
    #     return CustomItem(
    #         self.internal_name.replace("_", " ").title()+" Spawn Egg",
    #         f"minecraft:{self.entity_type}_spawn_egg",
    #         ###
    #     )
