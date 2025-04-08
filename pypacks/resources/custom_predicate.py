from dataclasses import dataclass, field
from typing import Any

from pypacks.resources.base_resource import BaseResource


@dataclass
class Predicate(BaseResource):
    """Parent Predicate, do not use directly. Used one from resources/predicate/predicates.py"""
    # https://minecraft.wiki/w/Predicate
    internal_name: str

    # sub_directories: list[str] = field(init=False, repr=False, hash=False, default_factory=list)  # Used to nest and organise items nicely
    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="predicate")

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "Predicate":  # type: ignore[override]  # , sub_directories: list[str]
        from pypacks.resources.predicate.predicates import PREDICATE_NAME_TO_CLASS, AllOfPredicate
        if isinstance(data, list):
            # This is a list of conditions, so it's an AllOfPredicate
            return AllOfPredicate.from_dict(internal_name, {"terms": data})
        cls_ = PREDICATE_NAME_TO_CLASS[data["condition"].removeprefix("minecraft:")]
        return cls_.from_dict(internal_name, data)
