from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Any

from pypacks.resources.entities.entity_variant import GenericEntityVariant


if TYPE_CHECKING:
    from pypacks.resources.entities.spawn_conditions import SpawnCondition


@dataclass
class ChickenVariant(GenericEntityVariant):
    internal_name: str
    texture_path: str | Path  # A path to the texture for the entity
    model: Literal["normal", "cold"] = "normal"  # Normal or cold model
    spawn_conditions: dict[int, "SpawnCondition | None"] = field(default_factory=dict)  # Mapping of priorty to spawn condition

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="chicken_variant")
    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="entity/chicken")
    entity_type: str = field(init=False, repr=False, hash=False, default="chicken")

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return super().to_dict(pack_namespace) | (
            {"model": self.model} if self.model != "normal" else {}
        )

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "ChickenVariant":  # type: ignore[override]
        return cls(
            internal_name=internal_name,
            texture_path=data["asset_id"].split(":")[1]+".png",
            model=data.get("model", "normal"),  # pyright: ignore (This keeps erroring for no reason, pyright is bad)
            spawn_conditions={condition["priority"]: condition.get("condition") for condition in data["spawn_conditions"]},
        )
