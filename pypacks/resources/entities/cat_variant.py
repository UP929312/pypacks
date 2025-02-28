from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pypacks.resources.entities.entity_variant import GenericEntityVariant


if TYPE_CHECKING:
    from pypacks.resources.entities.spawn_conditions import SpawnConditionType


@dataclass
class CatVariant(GenericEntityVariant):
    internal_name: str
    texture_path: str | Path  # A path to the texture for the entity
    spawn_conditions: dict[int, "SpawnConditionType"] = field(default_factory=dict)  # Mapping of priorty to spawn condition

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="cat_variant")
    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="entity/cat")
    entity_type: str = field(init=False, repr=False, hash=False, default="cat")
