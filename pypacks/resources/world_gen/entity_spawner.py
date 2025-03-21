from dataclasses import dataclass
from typing import Any, Literal

from pypacks.additions.constants import MOB_TO_CATEGORY

SpawnGroup = Literal["monster", "creature", "ambient", "water_creature", "underground_water_creature", "water_ambient", "misc", "axolotls"]


@dataclass
class SpawnOverride:
    entity_name: str = "minecraft:cow"
    bounding_box: Literal["piece", "full"] = "full"  # If full, overrides spawn setting inside the full bounding box of the structure. If piece, only the bounding boxs of all structure pieces.
    min_count: int = 1
    max_count: int = 1
    weight: int = 1

    @staticmethod
    def combine_spawn_overrides(spawn_overrides: list["SpawnOverride | DisableSpawnOverrideCategory"]) -> dict[SpawnGroup, Any]:
        spawn_overrides_dict: dict[SpawnGroup, Any] = {}
        # By group
        for group in ["monster", "creature", "ambient", "water_creature", "underground_water_creature", "water_ambient", "misc", "axolotls"]:
            relevant_spawns = [
                spawn for spawn in spawn_overrides
                if isinstance(spawn, SpawnOverride)
                and MOB_TO_CATEGORY[spawn.entity_name.removeprefix("minecraft:")] == group
            ]
            if relevant_spawns:
                if any(x for x in spawn_overrides if isinstance(x, DisableSpawnOverrideCategory) and x.mob_category == group):
                    raise ValueError("Cannot have both a spawn override and a disable spawn override in the same group")
                if not all(spawn.bounding_box == relevant_spawns[0].bounding_box for spawn in relevant_spawns):
                    raise ValueError("All spawn overrides in a group must have the same bounding box type")
                if group not in spawn_overrides_dict:
                    spawn_overrides_dict[group] = {"bounding_box": relevant_spawns[0].bounding_box, "spawns": []}  # type: ignore[index]
                spawn_overrides_dict[group]["spawns"].extend([spawn.to_dict() for spawn in relevant_spawns])  # type: ignore[index]
        for disable_spawn in [spawn for spawn in spawn_overrides if isinstance(spawn, DisableSpawnOverrideCategory)]:
            spawn_overrides_dict[disable_spawn.mob_category] = disable_spawn.to_dict()
        return spawn_overrides_dict

    def __post_init__(self) -> None:
        if self.max_count < self.min_count:
            raise ValueError("max_count must be greater than or equal to min_count")
        if self.min_count < 1:
            raise ValueError("min_count must be greater than 0")
        if self.max_count < 1:
            raise ValueError("max_count must be greater than 0")

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.entity_name,
            "minCount": self.min_count,
            "maxCount": self.max_count,
            "weight": self.weight,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SpawnOverride":
        return cls(
            entity_name=data["type"],
            min_count=data["minCount"],
            max_count=data["maxCount"],
            weight=data["weight"]
        )


@dataclass
class DisableSpawnOverrideCategory:
    mob_category: SpawnGroup
    bounding_box: Literal["piece", "full"] = "full"  # If full, overrides spawn setting inside the full bounding box of the structure. If piece, only the bounding boxs of all structure pieces.

    def to_dict(self) -> dict[str, Any]:
        return {
            "bounding_box": self.bounding_box,
            "spawns": []
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DisableSpawnOverrideCategory":
        raise NotImplementedError("Cannot create a DisableSpawnOverrideCategory from a dict (for now)")
        # return cls(
        #     mob_category=data["mob_category"],
        #     bounding_box=data["bounding_box"]
        # )
