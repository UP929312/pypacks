
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from pypacks.additions.item_components import ArmorTrimMaterialType, ArmorTrimType, PotionContents
from pypacks.resources.custom_jukebox_song import CustomJukeboxSong
from pypacks.resources.custom_tag import CustomTag
from pypacks.utils import recursively_remove_nones_from_data
from pypacks.providers.int_provider import IntRange

if TYPE_CHECKING:
    from pypacks.additions.item_components import EnchantmentType


class DataComponentPredicate:
    """Data component predicates (historically known as item sub-predicates) are used to check conditions about data components.
    They are used in minecraft:item_predicate argument type, item modifiers, loot predicates, advancement criteria, and entity and block predicates.
    They return a pass or fail result to the invoker, who acts differently based on this result."""
    # https://minecraft.wiki/w/Data_component_predicate
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "DataComponentPredicate":
        key = list(data.keys())[0]
        cls = DATA_COMPONENT_PREDICATE_NAME_TO_CLASSES[key]
        return cls.from_dict(internal_name, data[key])

    def list_of_str_or_tag_or_str_or_obj(self, pack_namespace: str, value: Any) -> list[str] | str | None:
        """Helper function to convert a list of strings or tags to a list of strings."""
        if isinstance(value, CustomTag):
            return value.get_reference(pack_namespace)
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            return [x.get_reference(pack_namespace) if hasattr(x, "get_reference") else x for x in value]  # type: ignore[no-untyped-call]
        return None


# @dataclass
# class AttributeModifierPredicate(DataComponentPredicate):
#     attribute_modifiers: list["AttributeModifier"] | CustomTag | str | None = None  # Any number of attribute modifiers. If more than one attribute modifier is specified, succeeds when any one of them matches the testing attribute modifier.
#     count: >?
#     attribute: str
#     operation: Literal["=", "<", "<=", ">", ">="]
#     amount: float
#     slot: Literal["mainhand", "offhand", "head", "chest", "legs", "feet", "any"] = "any"
#     id: str = None
#     name: str

#     def to_dict(self) -> dict[str, Any]:
#         return recursively_remove_nones_from_data({
#             "minecraft:attribute_modifiers": {
#                 "modifiers": {
#                     "contains": Attribute
#                     "attribute": self.attribute,
#                     "operation": self.operation,
#                     "amount": self.amount,
#                     "slot": self.slot,
#                     "id": self.id,
#                     "name": self.name
#                 }
#             }
#         })


# bundle_contents
# Checks item stacks in the bundle_contents data component.

# [NBT Compound / JSON Object] minecraft:bundle_contents
# [NBT Compound / JSON Object] items: (Optional) A collection predicate of item stack.
# [NBT List / JSON Array] contains: (Optional. Can be empty) Checks if there is any item stack passing a test. To succeed, each test must be passed by at least one item stack, but one item stack does not have to pass all the tests.
# [NBT Compound / JSON Object]: A test.
# All possible conditions for items[]
# [Int] size: (Optional) Checks the total number of item stacks. Matches an exact [Int]value, or checks if the value is between a range.
# [NBT Compound / JSON Object] size: (Optional) Another format.
# [Int] max: (Optional) The maximum value.
# [Int] min: (Optional) The minimum value.
# [NBT List / JSON Array] count: (Optional. Can be empty) Checks the number of item stacks that pass a test.
# [NBT Compound / JSON Object]: A test and required number.
# [NBT Compound / JSON Object] test: A test.
# All possible conditions for items[]
# [Int] count: Matches an exact [Int]value, or checks if the value is between a range.
# [NBT Compound / JSON Object] count: Another format.
# [Int] max: The maximum value.
# [Int] min: The minimum value.

@dataclass
class EnchantmentComponentPredicate(DataComponentPredicate):
    """Checks enchantments on the item (enchantments in the enchantments data component)."""
    # https://minecraft.wiki/w/Data_component_predicate#enchantments
    enchantments: list["EnchantmentType | str"] | CustomTag | str | None = None  # Any number of enchantments (or tag with #), If more than one enchantment is specified, succeeds when any one of them is present.
    levels: "IntRange | int | None" = None

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "minecraft:enchantments": [
                {
                    "enchantments": self.list_of_str_or_tag_or_str_or_obj(pack_namespace, self.enchantments),
                    "levels": self.levels.to_dict() if isinstance(self.levels, IntRange) else self.levels
                }
            ],
        })

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "EnchantmentComponentPredicate":
        return cls(
            enchantments=data["enchantments"],
            levels=IntRange.from_dict(data["levels"]) if "min" in data.get("levels", {}) else data.get("levels")
        )


@dataclass
class JukeboxPlayableComponentPredicate(DataComponentPredicate):
    """Checks jukebox song in the jukebox_playable data component.
    None = Any song"""
    # https://minecraft.wiki/w/Data_component_predicate#jukebox_playable
    songs: list["str | CustomJukeboxSong"] | CustomTag | str | None = None  # Any number of songs, If more than one song is specified, succeeds when any one of them is present.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "minecraft:jukebox_playable": {
                "songs": self.list_of_str_or_tag_or_str_or_obj(pack_namespace, self.songs)
            }
        })

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "JukeboxPlayableComponentPredicate":
        return cls(
            songs=data["songs"]
        )


@dataclass
class PotionContentsComponentPredicate(DataComponentPredicate):
    """Checks [String] potion field in the potion_contents data component. Fails if there is no potion field in the component."""
    # https://minecraft.wiki/w/Data_component_predicate#potion_contents
    potion_contents: list["str | PotionContents"] | CustomTag | str | None = None  # Any number of potion types. If more than one potion type is specified, succeeds when any one of them matches the testing potion field.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {"minecraft:potion_contents": self.list_of_str_or_tag_or_str_or_obj(pack_namespace, self.potion_contents)}

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "PotionContentsComponentPredicate":
        return cls(
            potion_contents=data["potion_contents"]
        )


@dataclass
class StoredEnchantmentsComponentPredicate(DataComponentPredicate):
    """Checks enchantments on an enchanted book (enchantments in the stored_enchantments data component)."""
    # https://minecraft.wiki/w/Data_component_predicate#stored_enchantments
    enchantments: list["str | EnchantmentType"] | CustomTag | str | None = None
    levels: "IntRange | int | None" = None

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        data = EnchantmentComponentPredicate(self.enchantments, self.levels).to_dict(pack_namespace)
        data["minecraft:stored_enchantments"] = data.pop("minecraft:enchantments")
        return data

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "StoredEnchantmentsComponentPredicate":
        return cls(
            enchantments=data["enchantments"],
            levels=IntRange.from_dict(data["levels"]) if "min" in data.get("levels", {}) else data.get("levels")
        )


@dataclass
class TrimComponentPredicate(DataComponentPredicate):
    """Checks trim data component in the trim data component."""
    # https://minecraft.wiki/w/Data_component_predicate#trim
    material: list["str | ArmorTrimType"] | CustomTag | str | None = None  # Any number of trim materials. If more than one trim material is specified, succeeds when any one of them matches the testing trim material.
    pattern: list["str | ArmorTrimMaterialType"] | CustomTag | str | None = None  # Any number of trim patterns. If more than one trim pattern is specified, succeeds when any one of them matches the testing trim pattern.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "minecraft:trim": {
                "material": self.list_of_str_or_tag_or_str_or_obj(pack_namespace, self.material),
                "pattern": self.list_of_str_or_tag_or_str_or_obj(pack_namespace, self.pattern),
            }
        })


# @dataclass
# class WrittenBookContentComponentPredicate(DataComponentPredicate):
#     """Checks written_book_content data component in the written_book_content data component."""
#     # https://minecraft.wiki/w/Data_component_predicate#written_book_content
#     pages: list["str"] | CustomTag | str | None = None
#     size: "IntRange | int | None" = None
#     pages_contains: list["str"] | CustomTag | str | None = None  # Any number of pages. If more than one page is specified, succeeds when any one of them matches the testing page.

# written_book_content
# Checks written_book_content data component.

# [NBT Compound / JSON Object] minecraft:written_book_content
# [NBT Compound / JSON Object] pages: (Optional) A collection predicate of page. Checks the raw texts of pages instead of filtered texts.
# [NBT List / JSON Array] contains: (Optional. Can be empty) Checks if there is any page passing a test. To succeed, each test must be passed by at least one page, but one page does not have to pass all the tests.
# [Undefined]: A test. A text component. Matches the full text of a page.
# [Int] size: (Optional) Checks the total number of pages. Matches an exact [Int]value, or checks if the value is between a range.
# [NBT Compound / JSON Object] size: (Optional) Another format.
# [Int] max: (Optional) The maximum value.
# [Int] min: (Optional) The minimum value.
# [NBT List / JSON Array] count: (Optional. Can be empty) Checks the number of pages that pass a test.
# [NBT Compound / JSON Object]: A test and required number.
# [Undefined] test: A test. A text component. Matches the full text of a page.
# [Int] count: Matches an exact [Int]value, or checks if the value is between a range.
# [NBT Compound / JSON Object] count: Another format.
# [Int] max: The maximum value.
# [Int] min: The minimum value.
# [String] author: (Optional) Matches the full string of author.
# [String] title: (Optional) Matches the full string of title. Checks raw title instead of filtered title.
# [Int] generation: (Optional) Checks the number of times this written book has been copied. 0 = original, 1 = copy of original, 2 = copy of copy, 3 = tattered. Matches an exact [Int]value, or checks if the value is between a range.
# [NBT Compound / JSON Object] generation: (Optional) Another format.
# [Int] max: (Optional) The maximum value.
# [Int] min: (Optional) The minimum value.
# [Boolean] resolved: (Optional) Checks whether the JSON text components have already been resolved (the [Boolean] resolved field in the data component is true).


DATA_COMPONENT_PREDICATE_NAME_TO_CLASSES: dict[str, type["DataComponentPredicate"]] = {
    "minecraft:enchantments": EnchantmentComponentPredicate,
    "minecraft:jukebox_playable": JukeboxPlayableComponentPredicate,
    "minecraft:potion_contents": PotionContentsComponentPredicate,
    "minecraft:stored_enchantments": StoredEnchantmentsComponentPredicate,
    "minecraft:trim": TrimComponentPredicate,
}
