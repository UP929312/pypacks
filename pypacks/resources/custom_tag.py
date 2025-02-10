import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from pypacks.pack import Pack


# TODO: https://minecraft.wiki/w/Resource_location#Registries_and_registry_objects
# Type hint that ^

# Block tags, Item Tags, Entity Type Tags, Function Tags

@dataclass
class CustomTag:
    """A tag containing a list of values"""
    # Block tags can be called when testing for block arguments in commands with #<resource location>, which succeeds if the block matches any of the blocks specified in the tag.
    # Item tags can be called when testing for item arguments in commands with #<resource location> or in recipes and advancements using "tag": "<resource location>", which succeeds if the item matches any of the items specified in the tag.
    # Entity type tags can be called in type target selector argument and loot table conditions with #<resource location>, which checks if the entity's type matches any of the entity types specified in the tag.
    # Function tags can be called in the /function command with #<resource location>, which runs all the functions specified in the tag in the order of their first appearance in a tag. If a function is referenced multiple times in a tag and its sub-tags, it is run once.
    internal_name: str
    values: list[str]
    tag_type: Literal["banner_pattern", "block", "cat_variant", "damage_type", "enchantment", "entity_type", "fluid", "game_event", "instrument", "item", "painting_variant", "point_of_interest_type", "worldgen"]
    sub_directories: list[str] = field(default_factory=list)
    replace: bool = False

    datapack_subdirectory_name: str = field(init=False, repr=False, default="tags")

    def get_reference(self, pack_namespace: str) -> str:
        return f"#{pack_namespace}:{'/'.join(self.sub_directories)}{self.internal_name}"

    def to_dict(self, pack_namespace: str) -> dict[str, bool | list[str]]:
        return {
            "replace": self.replace,
            "values": self.values
        }

    def create_datapack_files(self, pack: "Pack") -> None:
        # path = Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/Path(self.sub_directories)/self.tag_type/f"{self.internal_name}.json"
        path = Path(pack.datapack_output_path, "data", pack.namespace, self.__class__.datapack_subdirectory_name, *self.sub_directories, self.tag_type, f"{self.internal_name}.json")
        os.makedirs(path.parent, exist_ok=True)
        with open(path, "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)
