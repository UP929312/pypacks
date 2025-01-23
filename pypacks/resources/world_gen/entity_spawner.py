from dataclasses import dataclass
from typing import Any, Literal

from pypacks.additions.constants import MOB_TO_CATEGORY


@dataclass
class SpawnOverride:
    entity_name: str = "minecraft:cow"
    bounding_box: Literal["piece", "full"] = "full"  # If full, overrides spawn setting inside the full bounding box of the structure. If piece, only the bounding boxs of all structure pieces.
    min_count: int = 1
    max_count: int = 1
    weight: int = 1

    @staticmethod
    def combine_spawn_overrides(spawn_overrides: list["SpawnOverride | DisableSpawnOverrideCategory"]) -> dict[str, Any]:
        spawn_overrides_dict = {}
        # By group
        for group in ["monster", "creature", "ambient", "water_creature", "underground_water_creature", "water_ambient", "misc", "axolotls"]:
            relevant_spawns = [spawn for spawn in spawn_overrides
                               if isinstance(spawn, SpawnOverride)
                               and MOB_TO_CATEGORY[spawn.entity_name.removeprefix("minecraft:")] == group
            ]
            if relevant_spawns:
                if any(x for x in spawn_overrides if isinstance(x, DisableSpawnOverrideCategory) and x.mob_category == group):
                    raise ValueError("Cannot have both a spawn override and a disable spawn override in the same group")
                if not all(spawn.bounding_box == relevant_spawns[0].bounding_box for spawn in relevant_spawns):
                    raise ValueError("All spawn overrides in a group must have the same bounding box type")
                if group not in spawn_overrides_dict:
                    spawn_overrides_dict[group] = {"bounding_box": relevant_spawns[0].bounding_box, "spawns": []}
                spawn_overrides_dict[group]["spawns"].extend([spawn.to_dict() for spawn in relevant_spawns])
        for disable_spawn in [spawn for spawn in spawn_overrides if isinstance(spawn, DisableSpawnOverrideCategory)]:
            spawn_overrides_dict[disable_spawn.mob_category] = disable_spawn.to_dict()
        return spawn_overrides_dict

    def to_dict(self) -> dict[str, Any]:
        if self.max_count < self.min_count:
            raise ValueError("max_count must be greater than or equal to min_count")
        if self.min_count < 1:
            raise ValueError("min_count must be greater than 0")
        if self.max_count < 1:
            raise ValueError("max_count must be greater than 0")
        return {
            "type": self.entity_name,
            "minCount": self.min_count,
            "maxCount": self.max_count,
            "weight": self.weight,
        }


@dataclass
class DisableSpawnOverrideCategory:
    mob_category: Literal["monster", "creature", "ambient", "water_creature", "underground_water_creature", "water_ambient", "misc", "axolotls"]
    bounding_box: Literal["piece", "full"] = "full"  # If full, overrides spawn setting inside the full bounding box of the structure. If piece, only the bounding boxs of all structure pieces.

    def to_dict(self) -> dict[str, Any]:
        return {
            "bounding_box": self.bounding_box,
            "spawns": []
        }
