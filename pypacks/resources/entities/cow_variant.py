from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Any

from pypacks.resources.entities.entity_variant import GenericEntityVariant


if TYPE_CHECKING:
    from pypacks.resources.entities.spawn_conditions import SpawnConditionType


@dataclass
class CowVariant(GenericEntityVariant):
    internal_name: str
    texture_path: str | Path  # A path to the texture for the entity
    model: Literal["normal", "cold", "warm"] = "normal"  # Normal, cold or warm model
    spawn_conditions: dict[int, "SpawnConditionType"] = field(default_factory=dict)  # Mapping of priorty to spawn condition

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="cow_variant")
    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="entity/cow")
    entity_type: str = field(init=False, repr=False, hash=False, default="cow")

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return super().to_dict(pack_namespace) | (
            {"model": self.model} if self.model != "normal" else {}
        )
