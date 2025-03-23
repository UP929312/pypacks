from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING, Literal, TypedDict

from pypacks.resources.base_resource import BaseResource
from pypacks.additions.item_components import PotionEffect
from pypacks.resources.custom_predicate import Predicate
from pypacks.providers.number_provider import NumberProvider

if TYPE_CHECKING:
    from pypacks.resources.custom_loot_tables.custom_loot_table import SingletonEntry
    from pypacks.additions.item_components import AttributeModifier, FireworkExplosion, MapDecorationType, BannerPattern


class LootTableFunction:
    """A generic loot table function."""
    # https://minecraft.wiki/w/Item_modifier
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplementedError("Use the specific functions instead of this generic one.")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LootTableFunction":
        cls_: type["LootTableFunction"] = FUNCTION_NAME_TO_FUNCTION[data["function"].removeprefix("minecraft:")]
        return cls_.from_dict(data)

    __repr__ = BaseResource.__repr__


@dataclass
class ApplyBonusFunction(LootTableFunction):
    """Applies a predefined bonus formula to the count of the item stack.
    Formulas include:
    - binomial_with_bonus_count - binomial distribution (with n=level + extra, p=probability)
    - uniform_bonus_count - uniform distribution (from 0 to level * bonusMultiplier)
    - ore_drops - a special function used for ore drops in the vanilla game (Count *= (max(1; randomInt(0(inclusive) .. (Level + 2)(exclusive)))))."""
    enchantment: str  # ID of an enchantment on the tool provided by loot context used for level calculation.
    formula: str | Literal["binomial_with_bonus_count", "uniform_bonus_count", "ore_drops"]
    extra: int | None  # For formula 'binomial_with_bonus_count', the extra value.
    probability: int | None  # For formula 'binomial_with_bonus_count', the probability.
    bonus_multiplier: int | None  # For formula 'uniform_bonus_count', the bonus multiplier.

    def __post_init__(self) -> None:
        if self.formula == "binomial_with_bonus_count":
            assert self.extra is not None, "The extra value must be provided for the binomial_with_bonus_count formula."
            assert self.probability is not None, "The probability must be provided for the binomial_with_bonus_count formula."
            assert self.bonus_multiplier is None, "The bonus multiplier must not be provided for the binomial_with_bonus_count formula."
        elif self.formula == "uniform_bonus_count":
            assert self.extra is None, "The extra value must not be provided for the uniform_bonus_count formula."
            assert self.probability is None, "The probability must not be provided for the uniform_bonus_count formula."
            assert self.bonus_multiplier is not None, "The bonus multiplier must be provided for the uniform_bonus_count formula."
        elif self.formula == "ore_drops":
            assert self.extra is None, "The extra value must not be provided for the ore_drops formula."
            assert self.probability is None, "The probability must not be provided for the ore_drops formula."
            assert self.bonus_multiplier is None, "The bonus multiplier must not be provided for the ore_drops formula."

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:apply_bonus",
            "enchantment": self.enchantment,
            "formula": self.formula,
            "extra": self.extra,
            "probability": self.probability,
            "bonusMultiplier": self.bonus_multiplier,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ApplyBonusFunction":
        return cls(
            enchantment=data["enchantment"],
            formula=data["formula"],
            extra=data.get("extra"),
            probability=data.get("probability"),
            bonus_multiplier=data.get("bonusMultiplier"),
        )


@dataclass
class CopyComponentsFunction(LootTableFunction):
    """Copies components from a specified source onto an item."""
    source: str  # Source type to pull from. Specifies an entity or block entity from loot context. Only allowed value is block_entity
    include: list[str] | None = None  # Optional. A list of components to include. If omitted, all components are copied.
    exclude: list[str] | None = None  # Optional. A list of components to exclude.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:copy_components",
            "source": self.source,
        } | ({
            "include": self.include,
        } if self.include is not None else {}) | ({
            "exclude": self.exclude,
        } if self.exclude is not None else {})

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CopyComponentsFunction":
        return cls(
            source=data["source"],
            include=data.get("include"),
            exclude=data.get("exclude"),
        )


class CopyOperation(TypedDict):
    source: str  # The NBT path to copy from.
    target: str  # The NBT path to copy to, starting from the item's components tag.
    op: Literal["replace", "append", "merge"]  # Set to replace to replace any existing contents of the target NBT path, append to append to a list or array, or merge to merge into a compound tag.


@dataclass
class CopyCustomDataFunction(LootTableFunction):
    """Copies NBT values from a specified block entity or entity, or from command storage to the item's minecraft:custom_data component."""
    source_type: Literal["context", "storage"]  # Information of the block entity, entity or storage to copy NBT from.
    source_target: None | Literal["block_entity", "this", "killer", "direct_killer", "killer_player"] = None  # Included only if type is set to context. Specifies an entity or block entity from loot context to copy NBT from
    source_storage: None | str = None  # Included only if type is set to storage. A resource location specifying the storage ID to copy NBT from.
    ops: list[CopyOperation] = field(default=list)  # type: ignore[arg-type]  # An NBT operation.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        assert self.ops, "At least one operation must be provided."
        return {
            "function": "minecraft:copy_custom_data",
            "type": self.source_type,
            **({
                "target": self.source_target,
            } if self.source_type == "context" else {}) | ({
                "source": self.source_storage,
            } if self.source_type == "storage" else {}),
            "ops": self.ops,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CopyCustomDataFunction":
        return cls(
            source_type=data["type"],
            source_target=data.get("target"),
            source_storage=data.get("source"),
            ops=[CopyOperation(**op) for op in data["ops"]],  # type: ignore[typeddict-item]
        )


@dataclass
class CopyNameFunction(LootTableFunction):
    """Copies an entity's or a block entity's name tag into the item's `minecraft:custom_name` component."""
    source: Literal["block_entity", "this", "killer", "killer_player"]  # The target whose name is to be copied. Specifies an entity or block entity from loot context.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:copy_name",
            "source": self.source,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CopyNameFunction":
        return cls(
            source=data["source"],
        )


@dataclass
class CopyStateFunction(LootTableFunction):
    """Copies block state properties provided by loot context to the item's minecraft:block_state component."""
    block: str  # A block ID. Function fails if the block doesn't match the properties list.
    properties: list[str]  # A list of properties to copy. The name of a block state to copy.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:copy_state",
            "block": self.block,
            "properties": self.properties,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CopyStateFunction":
        return cls(
            block=data["block"],
            properties=data["properties"],
        )


@dataclass
class EnchantRandomlyFunction(LootTableFunction):
    """Enchants the item with one randomly-selected enchantment. The power of the enchantment, if applicable, is random. A book converts to an enchanted book when enchanted."""
    options: list[str] | str | None = None  # Optional. One or more enchantment(s) (an  ID, or a  tag with #, or an  array containing  IDs). List of enchantments to choose from. If omitted, all enchantments are possible.
    only_compatible: bool = True  # Optional, defaults to true. Whether only enchantments that are compatible with the item should be chosen (i.e. the item is listed in the enchantments supported_items). Books are always considered compatible.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:enchant_randomly",
        } | ({
            "options": self.options,
        } if self.options is not None else {}) | ({
            "onlyCompatible": self.only_compatible,
        } if not self.only_compatible else {})

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EnchantRandomlyFunction":
        return cls(
            options=data.get("options"),
            only_compatible=data.get("onlyCompatible", True),
        )


@dataclass
class EnchantWithLevelsFunction(LootTableFunction):
    """Enchants the item, with the specified enchantment level (roughly equivalent to using an enchantment table at that level). A book converts to an enchanted book."""
    levels: "NumberProvider | int"  # Specifies the enchantment level to use.
    options: list[str] | str | None = None  # Optional. One or more enchantment(s) (an  ID, or a  tag with #, or an  array containing  IDs). List of enchantments to choose from. If omitted, all enchantments are possible.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:enchant_with_levels",
            "levels": self.levels.to_dict() if isinstance(self.levels, NumberProvider) else self.levels,
        } | ({
            "options": self.options,
        } if self.options is not None else {})

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EnchantWithLevelsFunction":
        return cls(
            levels=int(data["levels"]) if isinstance(data["levels"], (int, float)) else NumberProvider.from_dict(data["levels"]),
            options=data.get("options"),
        )


@dataclass
class EnchantedCountIncreaseFunction(LootTableFunction):
    """Adjusts the stack size based on the level of the specified enchantment on the killer entity provided by loot context."""
    count: "NumberProvider"  # Specifies the number of additional items per level of the enchantment. Note the number may be fractional, rounded after multiplying by the enchantment level.
    limit: int = 0  # Specifies the maximum amount of items in the stack after the enchantment calculation. If the value is 0, no limit is applied.
    enchantment: str = ""  # One enchantment (an  ID). The enchantment whose levels should be used to calculate the count.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        assert self.enchantment, "An enchantment must be provided."
        return {
            "function": "minecraft:enchanted_count_increase",
            "count": self.count.to_dict(),
            "limit": self.limit,
            "enchantment": self.enchantment,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EnchantedCountIncreaseFunction":
        return cls(
            count=NumberProvider.from_dict(data["count"]),
            limit=data.get("limit", 0),
            enchantment=data.get("enchantment", ""),
        )


@dataclass
class ExplorationMapFunction(LootTableFunction):
    """If the origin is provided by loot context, converts an empty map into an explorer map leading to a nearby generated structure."""
    destination: str = "on_treasure_maps"  # A tag of structure to locate.
    decoration: "MapDecorationType" = "mansion"  # The icon used to mark the destination on the map. Accepts any of the map icon text IDs (case insensitive). If mansion or monument is used, the color of the lines on the item texture changes to match the corresponding explorer map.
    zoom: int = 2  # The zoom level of the resulting map. Defaults to 2.
    search_radius: int = 50  # The size, in chunks, of the area to search for structures. The area checked is square, not circular. Radius 0 causes only the current chunk to be searched, radius 1 causes the current chunk and eight adjacent chunks to be searched, and so on. Defaults to 50.
    skip_existing_chunks: bool = True  # Don't search in chunks that have already been generated. Defaults to true.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:exploration_map",
            "destination": self.destination,
            "decoration": self.decoration,
            "zoom": self.zoom,
            "search_radius": self.search_radius,
            "skip_existing_chunks": self.skip_existing_chunks,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExplorationMapFunction":
        return cls(
            destination=data.get("destination", "on_treasure_maps"),
            decoration=data.get("decoration", "mansion").removeprefix("minecraft:"),
            zoom=data.get("zoom", 2),
            search_radius=data.get("search_radius", 50),
            skip_existing_chunks=data.get("skip_existing_chunks", True),
        )


@dataclass
class ExplosionDecayFunction(LootTableFunction):
    """Removes some items from a stack, if the explosion radius is provided by loot context. Each item in the item stack has a chance of 1/explosion radius to be lost."""

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:explosion_decay",
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExplosionDecayFunction":
        return cls()


@dataclass
class FillPlayerHeadFunction(LootTableFunction):
    """Adds required item tags of a player head."""
    entity: Literal["this", "killer", "direct_killer", "killer_player"]  # Specifies a player to be used for the player head. Specifies an entity from loot context.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:fill_player_head",
            "entity": self.entity,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FillPlayerHeadFunction":
        return cls(
            entity=data["entity"],
        )


@dataclass
class FilteredFunction(LootTableFunction):
    """Applies another function only to items that match item predicate."""
    item_filter: dict[str, Any]  # A predicate to test against the item stack.
    modifier: dict[str, Any]  # Functions to apply to matching items.

    # TODO: Look into this... REALLY
    # All possible conditions for items:
    #     items: (Optional) One or more item(s) (an  ID, or a  tag with #, or an  array containing  IDs). Tests if the type of item in the item stack matches any of the listed values.
    #     count: (Optional) Tests the number of items in this item stack. Use an integer to test for a single value.
    #     count: (Optional) Another format.
    #     max: (Optional) The maximum value.
    #     min: (Optional) The minimum value.
    #     components: (Optional) Matches exact item component values. Each key in this object corresponds to a component to test, with its value as the desired data to compare.
    #         See data component format.
    #     predicates: (Optional) Matches item sub-predicates.
    #         See item sub-predicate.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:filtered",
            "item_filter": self.item_filter,
            "modifier": self.modifier,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FilteredFunction":
        return cls(
            item_filter=data["item_filter"],
            modifier=data["modifier"],
        )


@dataclass
class FurnaceSmeltFunction(LootTableFunction):
    """Smelts the item as it would be in a furnace without changing its count."""

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:furnace_smelt",
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FurnaceSmeltFunction":
        return cls()


@dataclass
class LimitCountFunction(LootTableFunction):
    """Limits the count of every item stack."""
    limit: "NumberProvider | None"  # An integer to specify the exact limit to use.
    min: "NumberProvider | None" = None  # Optional. A number provider. Minimum limit to use.
    max: "NumberProvider | None" = None  # Optional. A number provider. Maximum limit to use.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        assert self.limit or self.min or self.max, "At least one of limit, min, or max must be provided."
        assert not (self.limit and self.min), "Only one of limit or min can be provided."
        return {
            "function": "minecraft:limit_count",
        } | ({
            "limit": self.limit.to_dict(),
        } if self.limit is not None else {}) | ({
            "min": self.min.to_dict(),
        } if self.min is not None else {}) | ({
            "max": self.max.to_dict(),
        } if self.max is not None else {})

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LimitCountFunction":
        return cls(
            limit=NumberProvider.from_dict(data["limit"]) if data.get("limit") else None,
            min=NumberProvider.from_dict(data["min"]) if data.get("min") else None,
            max=NumberProvider.from_dict(data["max"]) if data.get("max") else None,
        )


@dataclass
class ModifyContentsFunction(LootTableFunction):
    """"Applies a function to every item inside an inventory component. If component does not exist, it is not added."""
    components: Literal["bundle_contents", "charged_projectiles", "container"]  # A target component.
    modifier: list[LootTableFunction] | LootTableFunction  # Function or list of functions to be applied to every item inside the container.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:modify_contents",
            "contents": self.components,
            "modifier": [x.to_dict(pack_namespace) for x in self.modifier] if isinstance(self.modifier, list) else self.modifier.to_dict(pack_namespace),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ModifyContentsFunction":
        return cls(
            components=data["contents"],
            modifier=[LootTableFunction.from_dict(x) for x in data["modifier"]],
        )


@dataclass
class ReferenceCallFunction(LootTableFunction):
    """Call sub-functions"""
    reference: str  # Location of function to call

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:reference",
            "name": self.reference,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ReferenceCallFunction":
        return cls(
            reference=data["name"],
        )


@dataclass
class SequenceFunction(LootTableFunction):
    """Applies a list of functions in sequence."""
    functions: list["LootTableFunction"]  # Sub-Functions to call

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:sequence",
            "functions": [x.to_dict(pack_namespace) for x in self.functions],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SequenceFunction":
        return cls(
            functions=[LootTableFunction.from_dict(x) for x in data["functions"]],
        )


@dataclass
class SetAttributesFunction(LootTableFunction):
    """Add attribute modifiers to the item."""
    modifiers: list["AttributeModifier"]
    replace: bool = True  # Set to true to replace the existing item attributes with the attributes in  modifiers. If false, the lines are appended to the list of existing attributes. Defaults to true.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:set_attributes",
            "modifiers": [x.to_dict() for x in self.modifiers],
            "replace": self.replace,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetAttributesFunction":
        return cls(
            modifiers=[AttributeModifier.from_dict(x) for x in data["modifiers"]],
            replace=data.get("replace", True),
        )


@dataclass
class SetBannerPatternFunction(LootTableFunction):
    """Adds or replaces banner patterns of a banner. Function successfully adds patterns into NBT tag even if invoked on a non-banner."""
    patterns: list["BannerPattern"]
    append: bool = True  # If true, the patterns are applied on top of the banner's existing patterns.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:set_banner_pattern",
            "patterns": [x.to_dict() for x in self.patterns],
            "append": self.append,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetBannerPatternFunction":
        return cls(
            patterns=[BannerPattern.from_dict(x) for x in data["patterns"]],
            append=data.get("append", True),
        )


@dataclass
class SetBookCoverFunction(LootTableFunction):
    """Sets the cover details of the minecraft:written_book_content component. If present, any pages in the book are left untouched."""
    author: str | None = None  # Optional. Sets the author of the book. If omitted, the original author is kept (or an empty string is used if there was no component).
    generation: int | None = None  # Optional. Sets the generation value of the book (original, copy, etc.). Allowed values are 0 to 3. If omitted, the original generation is kept (or 0 is used if there was no component).
    title: dict[str, str] | None = None  # Optional. Sets the title of the book as a raw JSON text component. If omitted, the original title is kept (or an empty string is used if there was no component).

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        assert self.author or self.generation or self.title, "At least one of author, generation, or title must be provided."
        return {
            "function": "minecraft:set_book_cover",
        } | ({
            "author": self.author,
        } if self.author is not None else {}) | ({
            "generation": self.generation,
        } if self.generation is not None else {}) | ({
            "title": self.title,
        } if self.title is not None else {})

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetBookCoverFunction":
        return cls(
            author=data.get("author"),
            generation=data.get("generation"),
            title=data.get("title"),
        )


@dataclass
class SetComponentsFunction(LootTableFunction):
    """Sets components of an item."""
    components: dict[str, Any]  # A map of components ID to component value. Components with a `!` prefix (e.g. "!minecraft:damage": {}) causes this component to be removed.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:set_components",
            "components": self.components,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetComponentsFunction":
        return cls(
            components=data["components"],
        )


@dataclass
class SetContentsFunction(LootTableFunction):
    """Sets the contents of a container block item to a list of entries."""
    entries: list["SingletonEntry"]  # A list of loot table entry producer to provide item stacks.
    content_type: str  # The block entity type to be written in BlockEntityTag.id.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:set_contents",
            "entries": [x.to_dict(pack_namespace) for x in self.entries],
            "type": self.content_type,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetContentsFunction":
        return cls(
            entries=[SingletonEntry.from_dict(x) for x in data["entries"]],
            content_type=data["type"],
        )


@dataclass
class SetCountFunction(LootTableFunction):
    """Sets the stack size."""
    number_provider: "int | NumberProvider"  # Specifies the stack size to set.
    add: bool = False  # If true, change is relative to current count. Defaults to false.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:set_count",
            "count": self.number_provider.to_dict() if isinstance(self.number_provider, NumberProvider) else self.number_provider,
            "add": self.add,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetCountFunction":
        return cls(
            number_provider=int(data["count"]) if isinstance(data["count"], (int, float)) else NumberProvider.from_dict(data["count"]),
            add=data.get("add", False),
        )


@dataclass
class SetCustomDataFunction(LootTableFunction):
    """Sets the minecraft:custom_data component."""
    tag: str  # The data to merge onto the item's minecraft:custom_data component, within a JSON string. The outer braces { } of the component must be present within this JSON string. Additional care is required when the NBT contains quotation marks ", as they must be escaped from the JSON syntax with a backslash \.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:set_custom_data",
            "tag": self.tag,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetCustomDataFunction":
        return cls(
            tag=data["tag"],
        )


@dataclass
class SetCustomModelDataFunction(LootTableFunction):
    """Sets the minecraft:custom_model_data component."""
    value: "NumberProvider"  # Specifies the custom model data value.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:set_custom_model_data",
            "value": self.value.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetCustomModelDataFunction":
        return cls(
            value=NumberProvider.from_dict(data["value"]),
        )


@dataclass
class SetDamageFunction(LootTableFunction):
    """Sets the item's damage value (durability)."""
    damage: "NumberProvider"  # Specifies the damage fraction to set (1.0 is undamaged, 0.0 is zero durability left).
    add: bool = False  # If true, change is relative to current damage. Defaults to false.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:set_damage",
            "damage": self.damage.to_dict(),
            "add": self.add,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetDamageFunction":
        return cls(
            damage=NumberProvider.from_dict(data["damage"]),
            add=data.get("add", False),
        )


@dataclass
class SetEnchantsFunction(LootTableFunction):
    """Sets the item's enchantments. A book converts to an enchanted book."""
    enchantments: dict[str, "NumberProvider | int"]  # Enchantments to set.
    add: bool = False  # Optional. If true, change is relative to current level. A nonexistent enchantment is presumed to start at 0. Defaults to false.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:set_enchantments",
            "enchantments": {k: (v.to_dict() if isinstance(v, NumberProvider) else v) for k, v in self.enchantments.items()},
            "add": self.add,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetEnchantsFunction":
        return cls(
            enchantments={k: (int(v) if isinstance(v, (int, float)) else NumberProvider.from_dict(v)) for k, v in data["enchantments"].items()},
            add=data.get("add", False),
        )


@dataclass
class SetFireworksFunction(LootTableFunction):
    """Sets the item tags for fireworks items."""
    explosions: list["FireworkExplosion"]  # Optional. Specifies firework explosions.
    flight_duration: int | None  # Optional, allowed values are 0 to 255. Determines flight duration measured in number of gunpowder. If omitted, the flight duration of the item is left untouched (or set to 0 if the component did not exist before).

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:set_fireworks",
        } | (
            {"explosions": [x.to_dict() for x in self.explosions]}
            if self.explosions else {}
        ) | (
            {"flight": self.flight_duration}
            if self.flight_duration is not None else {}
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetFireworksFunction":
        return cls(
            explosions=[FireworkExplosion.from_dict(x) for x in data.get("explosions", [])],
            flight_duration=data.get("flight"),
        )


@dataclass
class SetFireWorkExplosion(LootTableFunction):
    firework_explosion: "FireworkExplosion"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return self.firework_explosion.to_dict()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetFireWorkExplosion":
        return cls(
            firework_explosion=FireworkExplosion.from_dict(data),
        )


@dataclass
class SetInstrumentFunction(LootTableFunction):
    """Sets the item tags for instrument items to a random value from a tag."""
    options: str = "#minecraft:regular_goat_horns"  # The resource location started with # of an instrument tag, one of the listings is selected randomly.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        assert self.options.startswith("#"), "The options must start with a # and be an instrument tag!"
        return {
            "function": "minecraft:set_instrument",
            "options": self.options,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetInstrumentFunction":
        return cls(
            options=data["options"],
        )


@dataclass
class SetItemFunction(LootTableFunction):
    """Replaces item type without changing count or components."""
    item_id: str

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:set_item",
            "item": self.item_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetItemFunction":
        return cls(
            item_id=data["item"],
        )


BlockEntityType = Literal[
    "minecraft:banner", "minecraft:barrel", "minecraft:beacon", "minecraft:bed", "minecraft:beehive", "minecraft:bell", "minecraft:blast_furnace",
    "minecraft:brewing_stand", "minecraft:brushable_block", "minecraft:calibrated_sculk_sensor", "minecraft:campfire", "minecraft:chest",
    "minecraft:chiseled_bookshelf", "minecraft:command_block", "minecraft:comparator", "minecraft:conduit", "minecraft:crafter",
    "minecraft:creaking_heart", "minecraft:daylight_detector", "minecraft:decorated_pot", "minecraft:dispenser", "minecraft:dropper",
    "minecraft:enchanting_table", "minecraft:end_gateway", "minecraft:end_portal", "minecraft:ender_chest", "minecraft:furnace",
    "minecraft:hanging_sign", "minecraft:hopper", "minecraft:jigsaw", "minecraft:jukebox", "minecraft:lectern", "minecraft:mob_spawner",
    "minecraft:piston", "minecraft:sculk_catalyst", "minecraft:sculk_sensor", "minecraft:sculk_shrieker", "minecraft:shulker_box",
    "minecraft:sign", "minecraft:skull", "minecraft:smoker", "minecraft:structure_block", "minecraft:test_block", "minecraft:test_instance_block",
    "minecraft:trapped_chest", "minecraft:trial_spawner", "minecraft:vault",
]


@dataclass
class SetLootTableFunction(LootTableFunction):
    """Sets the loot table for a container block when placed and opened."""
    name: str  # Specifies the resource location of the loot table to be used.
    seed: int | None = None  # Specifies the loot table seed. If absent, the seed won't be put into the NBT, and a random seed is used when opening the continer.
    block_entity_type: BlockEntityType = "minecraft:banner"  # The block entity type to be written in BlockEntityTag.id.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        assert self.block_entity_type, "The block entity type must be provided."
        return {
            "function": "minecraft:set_loot_table",
            "name": self.name,
            "type": self.block_entity_type
        } | ({
            "seed": self.seed,
        } if self.seed is not None else {})

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetLootTableFunction":
        return cls(
            name=data["name"],
            seed=data.get("seed"),
            block_entity_type=data.get("type", ""),
        )


@dataclass
class SetLoreFunction(LootTableFunction):
    """Adds or changes the item's lore."""
    lore: list[dict[str, Any]]  # List of lines to append or replace on the item's lore, following the Raw JSON text format. Components requiring resolution are resolved only if entity successfully targets an entity.
    entity: Literal["this", "killer", "direct_killer", "killer_player"] | None = None  # Specifies an entity to act as @s when referenced in the JSON text component. Specifies an entity from loot context.
    mode: Literal["append", "insert", "replace_all", "replace_section"] = "replace_all"  # Determines how existing lore component should be modified.
    offset: int = 0  # Only used if mode is set to "insert" or "replace_section". Specifies index to insert or replace lines of lore from. Defaults to 0
    size: int | None = None  # Only used if  mode is set to "replace_section". Specifies the size of the range to be replaced. If omitted, the size of lore field is used.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:set_lore",
            "lore": self.lore,
            "mode": self.mode,
        } | ({
            "entity": self.entity,
        } if self.entity is not None else {}) | ({
            "offset": self.offset,
        } if self.mode in ["insert", "replace_section"] else {}) | ({
            "size": self.size,
        } if self.mode == "replace_section" else {})

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetLoreFunction":
        return cls(
            lore=data["lore"],
            entity=data.get("entity"),
            mode=data.get("mode", "replace_all"),
            offset=data.get("offset", 0),
            size=data.get("size"),
        )


@dataclass
class SetNameFunction(LootTableFunction):
    """Adds or changes the item's custom name."""
    name: dict[str, Any]  # A JSON text component, overwriting the previous custom name on the item. Components requiring resolution are resolved only if entity successfully targets an entity.
    entity: Literal["this", "killer", "direct_killer", "killer_player"] | None = None  # Specifies an entity to act as @s when referenced in the JSON text component. Specifies an entity from loot context.
    target: Literal["custom_name", "item_name"] = "custom_name"  # Optional. Allowed values are custom_name or item_name, corresponding with the component to be set. Defaults to custom_name.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:set_name",
            "name": self.name,
            "target": self.target,
        } | ({
            "entity": self.entity,
        } if self.entity is not None else {})

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetNameFunction":
        return cls(
            name=data["name"],
            entity=data.get("entity"),
            target=data.get("target", "custom_name"),
        )


@dataclass
class SetOminousBottleAmplifier(LootTableFunction):
    amplifier: "NumberProvider | float"
    conditions: list["Predicate"] = field(default_factory=list)

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:set_ominous_bottle_amplifier",
            "amplifier": self.amplifier.to_dict() if isinstance(self.amplifier, NumberProvider) else self.amplifier,
            "conditions": [x.to_dict(pack_namespace) for x in self.conditions],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetOminousBottleAmplifier":
        internal_name = "INCOMPLETE"
        return cls(
            amplifier=NumberProvider.from_dict(data["amplifier"]) if isinstance(data["amplifier"], dict) else data["amplifier"],
            conditions=[Predicate.from_dict(internal_name, x) for x in data.get("conditions", [])],
        )


@dataclass
class SetPotionFunction(LootTableFunction):
    """Sets the Potion tag of an item."""
    potion_id: str | Literal["empty"]  # The potion ID. Set to "empty" to remove the Potion tag.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:set_potion",
            "id": self.potion_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetPotionFunction":
        return cls(
            potion_id=data["id"],
        )


@dataclass
class SetStewEffectFunction(LootTableFunction):
    """Sets the status effects for suspicious stew. Fails if invoked on an item that is not suspicious stew."""
    effects: dict[PotionEffect, "int | NumberProvider"]  # A map of effect to duration

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        if [effect for effect in self.effects if isinstance(effect.duration_in_ticks, str) and effect.duration_in_ticks == "infinity"]:
            raise ValueError("Infinite duration is not supported for stew effects.")
        return {
            "function": "minecraft:set_stew_effect",
            "effects": [
                {
                    "type": effect.effect_name,
                    "duration": effect.duration_in_ticks.to_dict() if isinstance(effect.duration_in_ticks, NumberProvider) else effect.duration_in_ticks,  # type: ignore[union-attr]
                }
                for effect in self.effects
            ]
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetStewEffectFunction":
        return cls(
            effects={
                PotionEffect(effect["type"].removeprefix("minecraft:")): (
                    int(effect["duration"]) if isinstance(effect["duration"], (int, float)) else NumberProvider.from_dict(effect["duration"])
                )
                for effect in data["effects"]
            },
        )


@dataclass
class SetWritableBookPagesFunction(LootTableFunction):
    """Manipulates the pages of the minecraft:writable_book_content component."""
    pages: list[dict[str, Any]]  # A list of pages as raw JSON text components.
    mode: Literal["append", "insert", "replace_all", "replace_section"] = "replace_all"  # Determines how existing pages should be modified.
    offset: int = 0  # Only used if mode is set to "insert" or "replace_section". Specifies index to insert or replace pages from. Defaults to 0
    size: int | None = None  # Only used if  mode is set to "replace_section". Specifies the size of the range to be replaced. If omitted, the size of pages field is used.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:set_writable_book_pages",
            "pages": self.pages,
            "mode": self.mode,
        } | ({
            "offset": self.offset,
        } if self.mode in ["insert", "replace_section"] else {}) | ({
            "size": self.size,
        } if self.mode == "replace_section" else {})

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetWritableBookPagesFunction":
        return cls(
            pages=data["pages"],
            mode=data.get("mode", "replace_all"),
            offset=data.get("offset", 0),
            size=data.get("size"),
        )


@dataclass
class SetWrittenBookPagesFunction(SetWritableBookPagesFunction):
    """Manipulates the pages of the minecraft:writable_book_content component."""

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return (
            SetWritableBookPagesFunction(pages=self.pages, mode=self.mode, offset=self.offset, size=self.size).to_dict(pack_namespace) |
            {"function": "minecraft:set_written_book_pages"}
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SetWrittenBookPagesFunction":
        return cls(
            pages=data["pages"],
            mode=data.get("mode", "replace_all"),
            offset=data.get("offset", 0),
            size=data.get("size"),
        )


class ToolTipToggleType(TypedDict):
    """A map of supported item components to modify. All fields are optional."""
    attribute_modifiers: bool | None  # Changes the visibility of the tooltip displaying the item's attribute modifiers.
    can_break: bool | None  # Changes the visibility of the tooltip displaying the blocks the item can break in Adventure mode.
    can_place_on: bool | None  # Changes the visibility of the tooltip displaying the blocks the item can placed on in Adventure mode.
    dyed_color: bool | None  # Changes the visibility of the tooltip displaying dyed armor color.
    enchantments: bool | None  # Changes the visibility of the tooltip displaying the item's enchantments.
    stored_enchantments: bool | None  # Changes the visibility of the tooltip displaying the item's stored enchantments (for enchanted books).
    trim: bool | None  # Changes the visibility of the tooltip displaying the item's armor trim.
    unbreakable: bool | None  # Changes the visibility of the tooltip displaying the item's unbreakable status. Setting this to any value does not change whether the item is unbreakable.


@dataclass
class ToggleToolTipsFunction(LootTableFunction):
    toggles: ToolTipToggleType  # Toggles which tooltips are visible.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "function": "minecraft:toggle_tooltips",
            "toggles": {
                k: v for k, v in self.toggles.items() if v is not None
            },
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ToggleToolTipsFunction":
        return cls(
            toggles=data["toggles"],
        )


FUNCTION_NAME_TO_FUNCTION: dict[str, type["LootTableFunction"]] = {
    "apply_bonus": ApplyBonusFunction,
    "copy_components": CopyComponentsFunction,
    "copy_custom_data": CopyCustomDataFunction,
    "copy_name": CopyNameFunction,
    "copy_state": CopyStateFunction,
    "enchant_randomly": EnchantRandomlyFunction,
    "enchant_with_levels": EnchantWithLevelsFunction,
    "enchanted_count_increase": EnchantedCountIncreaseFunction,
    "exploration_map": ExplorationMapFunction,
    "explosion_decay": ExplosionDecayFunction,
    "fill_player_head": FillPlayerHeadFunction,
    "filtered": FilteredFunction,
    "furnace_smelt": FurnaceSmeltFunction,
    "limit_count": LimitCountFunction,
    "modify_contents": ModifyContentsFunction,
    "reference": ReferenceCallFunction,
    "sequence": SequenceFunction,
    "set_attributes": SetAttributesFunction,
    "set_banner_pattern": SetBannerPatternFunction,
    "set_book_cover": SetBookCoverFunction,
    "set_components": SetComponentsFunction,
    "set_contents": SetContentsFunction,
    "set_count": SetCountFunction,
    "set_custom_data": SetCustomDataFunction,
    "set_custom_model_data": SetCustomModelDataFunction,
    "set_damage": SetDamageFunction,
    "set_enchantments": SetEnchantsFunction,
    "set_fireworks": SetFireworksFunction,
    "set_instrument": SetInstrumentFunction,
    "set_item": SetItemFunction,
    "set_loot_table": SetLootTableFunction,
    "set_lore": SetLoreFunction,
    "set_ominous_bottle_amplifier": SetOminousBottleAmplifier,
    "set_name": SetNameFunction,
    "set_potion": SetPotionFunction,
    "set_stew_effect": SetStewEffectFunction,
    "set_writable_book_pages": SetWritableBookPagesFunction,
    "set_written_book_pages": SetWrittenBookPagesFunction,
    "toggle_tooltips": ToggleToolTipsFunction,
}
