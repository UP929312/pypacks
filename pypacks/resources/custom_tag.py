import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from pypacks.resources.base_resource import BaseResource

if TYPE_CHECKING:
    from pypacks.resources.custom_item import CustomItem
    from pypacks.pack import Pack
    TagType = Literal["banner_pattern", "block", "cat_variant", "damage_type", "enchantment", "entity_type", "fluid", "function", "game_event", "instrument", "item", "painting_variant", "point_of_interest_type", "worldgen"]

# https://minecraft.wiki/w/Resource_location#Registries_and_registry_objects
# Type hint that ^?

# Block tags, Item Tags, Entity Type Tags, Function Tags


@dataclass
class CustomTag(BaseResource):
    """A tag containing a list of values
    # WARNING, passing in custom items to this will convert them to their base item, and won't include any components."""
    # Block tags can be called when testing for block arguments in commands with #<resource location>, which succeeds if the block matches any of the blocks specified in the tag.
    # Item tags can be called when testing for item arguments in commands with #<resource location> or in recipes and advancements using "tag": "<resource location>", which succeeds if the item matches any of the items specified in the tag.
    # Entity type tags can be called in type target selector argument and loot table conditions with #<resource location>, which checks if the entity's type matches any of the entity types specified in the tag.
    # Function tags can be called in the /function command with #<resource location>, which runs all the functions specified in the tag in the order of their first appearance in a tag. If a function is referenced multiple times in a tag and its sub-tags, it is run once.
    internal_name: str
    values: list["str | CustomTag | CustomItem"]
    tag_type: Literal["banner_pattern", "block", "cat_variant", "damage_type", "enchantment", "entity_type", "fluid", "function", "game_event", "instrument", "item", "painting_variant", "point_of_interest_type", "worldgen"]
    sub_directories: list[str] = field(default_factory=list)
    replace: bool = False
    create_if_empty: bool = False

    datapack_subdirectory_name: str = field(init=False, repr=False, default="tags")

    def get_reference(self, pack_namespace: str) -> str:
        return "#"+super().get_reference(pack_namespace)  # Cannot be removed, is prefix with "#"!

    def to_dict(self, pack_namespace: str) -> dict[str, bool | list[str]]:
        from pypacks.resources.custom_item import CustomItem
        from pypacks.utils import recursively_remove_nones_from_data
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "replace": self.replace,
            "values": [
                (x.get_reference(pack_namespace) if isinstance(x, CustomTag) else (x.base_item if isinstance(x, CustomItem) else x))
                for x in self.values],
        })

    @classmethod
    def from_dict(cls, internal_name: str, tag_type: "TagType", data: dict[str, bool | list[str]]) -> "CustomTag":  # type: ignore[override]  # TODO: This has another parameter
        return cls(
            internal_name,
            data["values"],  # type: ignore[arg-type]
            tag_type,  # TODO Somehow not require this?
            replace=data.get("replace", False),  # type: ignore[arg-type]
        )

    def create_datapack_files(self, pack: "Pack") -> None:
        from pypacks.resources.custom_item import CustomItem
        if not self.create_if_empty and not self.values:
            return
        if any(isinstance(x, CustomItem) for x in self.values) and pack.config.warn_about_tags_with_custom_items:
            print(f"Warning: Tag {self.internal_name} contains custom items. Custom items will be converted to their base item and will not include any components.")

        path = Path(pack.datapack_output_path, "data", pack.namespace, self.__class__.datapack_subdirectory_name, self.tag_type, *self.sub_directories, f"{self.internal_name}.json")
        os.makedirs(path.parent, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)

    @classmethod
    def from_datapack_files(cls, data_path: "Path") -> list["CustomTag"]:
        """Path should be the root of the pack"""
        tags = []
        for tag_path_absolute in BaseResource.get_all_resource_paths(cls, data_path):
            with open(tag_path_absolute, "r", encoding="utf-8") as file:
                tags.append(
                    cls.from_dict(
                        tag_path_absolute.stem,
                        tag_path_absolute.parts[-2],  # type: ignore[arg-type]
                        json.load(file),
                    )
                )
        return tags

    def get_first_non_tag_item(self) -> "CustomItem | str":
        """Recursively searches the tag in a depth-first search for the first non-tag item (e.g. if a tag contains a tag, search that tag etc.)"""
        for value in self.values:
            if isinstance(value, CustomTag):
                return value.get_first_non_tag_item()
            return value
        raise ValueError("No non-tag items found in the tag")
