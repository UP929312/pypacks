from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING, Literal, TypedDict

from pypacks.resources.item_components import PotionEffect


if TYPE_CHECKING:
    from pypacks.resources.custom_loot_tables.custom_loot_table import Entry
    from pypacks.resources.custom_loot_tables.number_provider import (
        ConstantNumberProvider, BinomialNumberProvider, ScoreboardNumberProvider, StorageNumberProvider, UniformNumberProvider,
    )
    from pypacks.resources.item_components import AttributeModifier, FireworkExplosion, MapDecorationType, BannerPattern


# https://minecraft.wiki/w/Item_modifier


@dataclass
class LootTableFunction:
    function_name: str
    function_parameters: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        # raise NotImplemented  # TODO: Rewrite the ones in loot tables to use these, and not this generic, make it raise NotImplemented
        return {"function": self.function_name, **self.function_parameters}


@dataclass
class ApplyBonusFunction:
    """Applies a predefined bonus formula to the count of the item stack."""
    enchantment: str  # ID of an enchantment on the tool provided by loot context used for level calculation.
    formula: str | Literal["binomial_with_bonus_count", "uniform_bonus_count", "ore_drops"]  # A resource location. Can be binomial_with_bonus_count for a binomial distribution (with n=level + extra, p=probability), uniform_bonus_count for uniform distribution (from 0 to level * bonusMultiplier), or ore_drops for a special function used for ore drops in the vanilla game (Count *= (max(1; randomInt(0(inclusive) .. (Level + 2)(exclusive))))).
    extra: int | None  # For formula 'binomial_with_bonus_count', the extra value.
    probability: int | None  # For formula 'binomial_with_bonus_count', the probability.
    bonus_multiplier: int | None  # For formula 'uniform_bonus_count', the bonus multiplier.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:apply_bonus",
            "enchantment": self.enchantment,
            "formula": self.formula,
            "extra": self.extra,
            "probability": self.probability,
            "bonusMultiplier": self.bonus_multiplier,
        }


@dataclass
class CopyComponentsFunction:
    """Copies components from a specified source onto an item."""
    source: str  # Source type to pull from. Specifies an entity or block entity from loot context. Only allowed value is block_entity
    include: list[str] | None = None  # Optional. A list of components to include. If omitted, all components are copied.
    exclude: list[str] | None = None  # Optional. A list of components to exclude.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:copy_components",
            "source": self.source,
        } | ({
            "include": self.include,
        } if self.include is not None else {}) | ({
            "exclude": self.exclude,
        } if self.exclude is not None else {})


class CopyOperation(TypedDict):
    source: str  # The NBT path to copy from.
    target: str  # The NBT path to copy to, starting from the item's components tag.
    op: Literal["replace", "append", "merge"]  # Set to replace to replace any existing contents of the target NBT path, append to append to a list or array, or merge to merge into a compound tag.


@dataclass
class CopyCustomDataFunction:
    """Copies NBT values from a specified block entity or entity, or from command storage to the item's minecraft:custom_data component."""
    source_type: Literal["context", "storage"]  # Information of the block entity, entity or storage to copy NBT from.
    source_target: None | Literal["block_entity", "this", "killer", "direct_killer", "killer_player"] = None  # Included only if type is set to context. Specifies an entity or block entity from loot context to copy NBT from
    source_storage: None | str = None  # Included only if type is set to storage. A resource location specifying the storage ID to copy NBT from.
    ops: list[CopyOperation] = field(default=list)  # type: ignore[arg-type]  # An NBT operation.

    def to_dict(self) -> dict[str, Any]:
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


@dataclass
class CopyNameFunction:
    """Copies an entity's or a block entity's name tag into the item's `minecraft:custom_name` component."""
    source: Literal["block_entity", "this", "killer", "killer_player"]  # The target whose name is to be copied. Specifies an entity or block entity from loot context.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:copy_name",
            "source": self.source,
        }


@dataclass
class CopyStateFunction:
    """Copies block state properties provided by loot context to the item's minecraft:block_state component."""
    block: str  # A block ID. Function fails if the block doesn't match the properties list.
    properties: list[str]  # A list of properties to copy. The name of a block state to copy.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:copy_state",
            "block": self.block,
            "properties": self.properties,
        }


@dataclass
class EnchantRandomlyFunction:
    """Enchants the item with one randomly-selected enchantment. The power of the enchantment, if applicable, is random. A book converts to an enchanted book when enchanted."""
    options: list[str] | str | None = None  # Optional. One or more enchantment(s) (an  ID, or a  tag with #, or an  array containing  IDs). List of enchantments to choose from. If omitted, all enchantments are possible.
    only_compatible: bool = True  # Optional, defaults to true. Whether only enchantments that are compatible with the item should be chosen (i.e. the item is listed in the enchantments supported_items). Books are always considered compatible.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:enchant_randomly",
        } | ({
            "options": self.options,
        } if self.options is not None else {}) | ({
            "onlyCompatible": self.only_compatible,
        } if not self.only_compatible else {})


@dataclass
class EnchantWithLevelsFunction:
    """Enchants the item, with the specified enchantment level (roughly equivalent to using an enchantment table at that level). A book converts to an enchanted book."""
    levels: "ConstantNumberProvider | BinomialNumberProvider | ScoreboardNumberProvider | StorageNumberProvider | UniformNumberProvider"  # Specifies the enchantment level to use.
    options: list[str] | str | None = None  # Optional. One or more enchantment(s) (an  ID, or a  tag with #, or an  array containing  IDs). List of enchantments to choose from. If omitted, all enchantments are possible.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:enchant_with_levels",
            "levels": self.levels.to_dict(),
        } | ({
            "options": self.options,
        } if self.options is not None else {})


@dataclass
class EnchantedCountIncreaseFunction:
    """Adjusts the stack size based on the level of the specified enchantment on the killer entity provided by loot context."""
    count: "ConstantNumberProvider | BinomialNumberProvider | ScoreboardNumberProvider | StorageNumberProvider | UniformNumberProvider"  # Specifies the number of additional items per level of the enchantment. Note the number may be fractional, rounded after multiplying by the enchantment level.
    limit: int = 0  # Specifies the maximum amount of items in the stack after the enchantment calculation. If the value is 0, no limit is applied.
    enchantment: str = ""  # One enchantment (an  ID). The enchantment whose levels should be used to calculate the count.

    def to_dict(self) -> dict[str, Any]:
        assert self.enchantment, "An enchantment must be provided."
        return {
            "function": "minecraft:enchanted_count_increase",
            "count": self.count.to_dict(),
            "limit": self.limit,
            "enchantment": self.enchantment,
        }


@dataclass
class ExplorationMapFunction:
    """If the origin is provided by loot context, converts an empty map into an explorer map leading to a nearby generated structure."""
    destination: str = "on_treasure_maps"  # A tag of structure to locate.
    decoration: "MapDecorationType" = "mansion"  # The icon used to mark the destination on the map. Accepts any of the map icon text IDs (case insensitive). If mansion or monument is used, the color of the lines on the item texture changes to match the corresponding explorer map.
    zoom: int = 2  # The zoom level of the resulting map. Defaults to 2.
    search_radius: int = 50  # The size, in chunks, of the area to search for structures. The area checked is square, not circular. Radius 0 causes only the current chunk to be searched, radius 1 causes the current chunk and eight adjacent chunks to be searched, and so on. Defaults to 50.
    skip_existing_chunks: bool = True  # Don't search in chunks that have already been generated. Defaults to true.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:exploration_map",
            "destination": self.destination,
            "decoration": self.decoration,
            "zoom": self.zoom,
            "search_radius": self.search_radius,
            "skip_existing_chunks": self.skip_existing_chunks,
        }


class ExplosionDecayFunction:
    """Removes some items from a stack, if the explosion radius is provided by loot context. Each item in the item stack has a chance of 1/explosion radius to be lost."""

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:explosion_decay",
        }


@dataclass
class FillPlayerHeadFunction:
    """Adds required item tags of a player head."""
    entity: Literal["this", "killer", "direct_killer", "killer_player"]  # Specifies a player to be used for the player head. Specifies an entity from loot context.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:fill_player_head",
            "entity": self.entity,
        }


@dataclass
class FilteredFunction:
    """Applies another function only to items that match item predicate."""
    item_filter: dict[str, Any]  # A predicate to test against the item stack.
    modifier: dict[str, Any]  # Functions to apply to matching items.

    # TODO: Look into this...
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

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:filtered",
            "item_filter": self.item_filter,
            "modifier": self.modifier,
        }


class FurnaceMeltFunction:
    """Smelts the item as it would be in a furnace without changing its count."""

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:furnace_melt",
        }


@dataclass
class LimitCountFunction:
    """Limits the count of every item stack."""
    limit: "ConstantNumberProvider | BinomialNumberProvider | ScoreboardNumberProvider | StorageNumberProvider | UniformNumberProvider | None"  # An integer to specify the exact limit to use.
    min: "ConstantNumberProvider | BinomialNumberProvider | ScoreboardNumberProvider | StorageNumberProvider | UniformNumberProvider | None" = None  # Optional. A number provider. Minimum limit to use.
    max: "ConstantNumberProvider | BinomialNumberProvider | ScoreboardNumberProvider | StorageNumberProvider | UniformNumberProvider | None" = None  # Optional. A number provider. Maximum limit to use.

    def to_dict(self) -> dict[str, Any]:
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


@dataclass
class ModifyContentsFunction:
    """"Applies a function to every item inside an inventory component. If component does not exist, it is not added."""
    components: Literal["bundle_contents", "charged_projectiles", "container"]  # A target component.
    modifier: list[LootTableFunction] | LootTableFunction  # Function or list of functions to be applied to every item inside the container.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:modify_contents",
            "contents": self.components,
            "modifier": [x.to_dict() for x in self.modifier] if isinstance(self.modifier, list) else self.modifier.to_dict(),
        }


class ReferenceCallFunction:
    """Call sub-functions"""
    reference: str  # Location of function to call

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:reference",
            "name": self.reference,
        }


@dataclass
class SequenceFunction:
    """Applies a list of functions in sequence."""
    functions: list["LootTableFunction"]  # Location of function to call. An item modifier. The same classes that are as described in this file.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:sequence",
            "functions": [x.to_dict() for x in self.functions],
        }


@dataclass
class SetAttributesFunction:
    """Add attribute modifiers to the item."""
    modifiers: list["AttributeModifier"]
    replace: bool = True  # Set to true to replace the existing item attributes with the attributes in  modifiers. If false, the lines are appended to the list of existing attributes. Defaults to true.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:set_attributes",
            "modifiers": [x.to_dict() for x in self.modifiers],
            "replace": self.replace,
        }


@dataclass
class SetBannerPatternFunction:
    """Adds or replaces banner patterns of a banner. Function successfully adds patterns into NBT tag even if invoked on a non-banner."""
    patterns: list["BannerPattern"]
    append: bool = True  # If true, the patterns are applied on top of the banner's existing patterns.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:set_banner_pattern",
            "patterns": [x.to_dict() for x in self.patterns],
            "append": self.append,
        }


@dataclass
class SetBookCoverFunction:
    """Sets the cover details of the minecraft:written_book_content component. If present, any pages in the book are left untouched."""
    author: str | None = None  # Optional. Sets the author of the book. If omitted, the original author is kept (or an empty string is used if there was no component).
    generation: int | None = None  # Optional. Sets the generation value of the book (original, copy, etc.). Allowed values are 0 to 3. If omitted, the original generation is kept (or 0 is used if there was no component).
    title: dict[str, str] | None = None  # Optional. Sets the title of the book as a raw JSON text component. If omitted, the original title is kept (or an empty string is used if there was no component).

    def to_dict(self) -> dict[str, Any]:
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


@dataclass
class SetComponentsFunction:
    """Sets components of an item."""
    components: dict[str, Any]  # A map of components ID to component value. Components with a `!` prefix (e.g. "!minecraft:damage": {}) causes this component to be removed.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:set_components",
            "components": self.components,
        }


@dataclass
class SetContentsFunction:
    """Sets the contents of a container block item to a list of entries."""
    entries: list["Entry"]  # A list of loot table entry producer to provide item stacks.
    content_type: str  # The block entity type to be written in BlockEntityTag.id.

    def to_dict(self) -> dict[str, Any]:
        raise Exception("This function is not yet implemented.")  # TODO: Do this
        return {
            "function": "minecraft:set_contents",
            "entries": [x.to_dict() for x in self.entries],  # TODO: This needs datapack (for some entries)...
            "type": self.content_type,
        }


@dataclass
class SetCountFunction:
    """Sets the stack size."""
    count: "ConstantNumberProvider | BinomialNumberProvider | ScoreboardNumberProvider | StorageNumberProvider | UniformNumberProvider"  # Specifies the stack size to set.
    add: bool = False  # If true, change is relative to current count. Defaults to false.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:set_count",
            "count": self.count.to_dict(),
            "add": self.add,
        }


@dataclass
class SetCustomDataFunction:
    """Sets the minecraft:custom_data component."""
    tag: str  # The data to merge onto the item's minecraft:custom_data component, within a JSON string. The outer braces { } of the component must be present within this JSON string. Additional care is required when the NBT contains quotation marks ", as they must be escaped from the JSON syntax with a backslash \.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:set_custom_data",
            "tag": self.tag,
        }


@dataclass
class SetCustomModelDataFunction:
    """Sets the minecraft:custom_model_data component."""
    value: "ConstantNumberProvider | BinomialNumberProvider | ScoreboardNumberProvider | StorageNumberProvider | UniformNumberProvider"  # Specifies the custom model data value.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:set_custom_model_data",
            "value": self.value.to_dict(),
        }


@dataclass
class SetDamageFunction:
    """Sets the item's damage value (durability)."""
    damage: "ConstantNumberProvider | BinomialNumberProvider | ScoreboardNumberProvider | StorageNumberProvider | UniformNumberProvider"  # Specifies the damage fraction to set (1.0 is undamaged, 0.0 is zero durability left).
    add: bool = False  # If true, change is relative to current damage. Defaults to false.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:set_damage",
            "damage": self.damage.to_dict(),
            "add": self.add,
        }


@dataclass
class SetEnchantsFunction:
    """Sets the item's enchantments. A book converts to an enchanted book."""
    enchantments: dict[str, "ConstantNumberProvider | BinomialNumberProvider | ScoreboardNumberProvider | StorageNumberProvider | UniformNumberProvider"]  # Enchantments to set.
    add: bool = False  # Optional. If true, change is relative to current level. A nonexistent enchantment is presumed to start at 0. Defaults to false.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:set_enchants",
            "enchantments": {k: v.to_dict() for k, v in self.enchantments.items()},
            "add": self.add,
        }


@dataclass
class SetFireworksFunction:
    """Sets the item tags for fireworks items."""
    explosions: list["FireworkExplosion"]  # Optional. Specifies firework explosions.
    flight_duration: int | None  # Optional, allowed values are 0 to 255. Determines flight duration measured in number of gunpowder. If omitted, the flight duration of the item is left untouched (or set to 0 if the component did not exist before).

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:set_fireworks",
        } | (
            {"explosions": [x.to_dict() for x in self.explosions]}
            if self.explosions else {}
        ) | (
            {"flight": self.flight_duration}
            if self.flight_duration is not None else {}
        )


@dataclass
class SetFireWorkExplosion:
    firework_explosion: "FireworkExplosion"

    def to_dict(self) -> dict[str, Any]:
        return self.firework_explosion.to_dict()


@dataclass
class SetInstrumentFunction:
    """Sets the item tags for instrument items to a random value from a tag."""
    options: str  # The resource location started with # of an instrument tag, one of the listings is selected randomly.

    def to_dict(self) -> dict[str, Any]:
        assert self.options.startswith("#"), "The options must start with a # and be an instrument tag!"
        return {
            "function": "minecraft:set_instrument",
            "options": self.options,
        }


@dataclass
class SetItemFunction:
    """Replaces item type without changing count or components."""
    item_id: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:set_item",
            "item": self.item_id,
        }


@dataclass
class SetLootTableFunction:
    """Sets the loot table for a container block when placed and opened."""
    name: str  # Specifies the resource location of the loot table to be used.
    seed: int | None = None  # Optional. Specifies the loot table seed. If absent or set to 0, the seed won't be put into the NBT, and a random seed is used when opening the continer.
    block_entity_type: str = ""  # The block entity type to be written in BlockEntityTag.id.

    def to_dict(self) -> dict[str, Any]:
        assert self.block_entity_type, "The block entity type must be provided."
        return {
            "function": "minecraft:set_loot_table",
            "name": self.name,
            "type": self.block_entity_type
        } | ({
            "seed": self.seed,
        } if self.seed is not None else {})


@dataclass
class SetLoreFunction:
    """Adds or changes the item's lore."""
    lore: list[dict[str, Any]]  # List of lines to append or replace on the item's lore, following the Raw JSON text format. Components requiring resolution are resolved only if entity successfully targets an entity.
    entity: Literal["this", "killer", "direct_killer", "killer_player"] | None = None  # Specifies an entity to act as @s when referenced in the JSON text component. Specifies an entity from loot context.
    mode: Literal["append", "insert", "replace_all", "replace_section"] = "replace_all"  # Determines how existing lore component should be modified.
    offset: int = 0  # Only used if mode is set to "insert" or "replace_section". Specifies index to insert or replace lines of lore from. Defaults to 0
    size: int | None = None  # Only used if  mode is set to "replace_section". Specifies the size of the range to be replaced. If omitted, the size of lore field is used.

    def to_dict(self) -> dict[str, Any]:
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


@dataclass
class SetNameFunction:
    """Adds or changes the item's custom name."""
    name: dict[str, Any]  # A JSON text component, overwriting the previous custom name on the item. Components requiring resolution are resolved only if entity successfully targets an entity.
    entity: Literal["this", "killer", "direct_killer", "killer_player"] | None = None  # Specifies an entity to act as @s when referenced in the JSON text component. Specifies an entity from loot context.
    target: Literal["custom_name", "item_name"] = "custom_name"  # Optional. Allowed values are custom_name or item_name, corresponding with the component to be set. Defaults to custom_name.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:set_name",
            "name": self.name,
            "target": self.target,
        } | ({
            "entity": self.entity,
        } if self.entity is not None else {})


@dataclass
class SetPotionFunction:
    """Sets the Potion tag of an item."""
    potion_id: str | Literal["empty"]  # The potion ID. Set to "empty" to remove the Potion tag.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:set_potion",
            "id": self.potion_id,
        }


@dataclass
class SetStewEffectFunction:
    """Sets the status effects for suspicious stew. Fails if invoked on an item that is not suspicious stew."""
    effects: dict[PotionEffect, int]  # A map of effect to duration

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:set_stew_effect",
            "effects": [
                {
                    "type": effect.effect_name,
                    "duration": effect.duration,
                }
                for effect in self.effects
            ]
        }


@dataclass
class SetWritableBookPagesFunction:
    """Manipulates the pages of the minecraft:writable_book_content component."""
    pages: list[dict[str, Any]]  # A list of pages as raw JSON text components.
    mode: Literal["append", "insert", "replace_all", "replace_section"] = "replace_all"  # Determines how existing pages should be modified.
    offset: int = 0  # Only used if mode is set to "insert" or "replace_section". Specifies index to insert or replace pages from. Defaults to 0
    size: int | None = None  # Only used if  mode is set to "replace_section". Specifies the size of the range to be replaced. If omitted, the size of pages field is used.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:set_writable_book_pages",
            "pages": self.pages,
            "mode": self.mode,
        } | ({
            "offset": self.offset,
        } if self.mode in ["insert", "replace_section"] else {}) | ({
            "size": self.size,
        } if self.mode == "replace_section" else {})


@dataclass
class SetWrittenBookPagesFunction(SetWritableBookPagesFunction):
    """Manipulates the pages of the minecraft:writable_book_content component."""

    def to_dict(self) -> dict[str, Any]:
        return SetWritableBookPagesFunction(pages=self.pages, mode=self.mode, offset=self.offset, size=self.size).to_dict() | {"function": "minecraft:set_written_book_pages"}


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
class ToggleToolTipsFunction:
    toggles: ToolTipToggleType  # Toggles which tooltips are visible.

    def to_dict(self) -> dict[str, Any]:
        return {
            "function": "minecraft:toggle_tooltips",
            "toggles": {
                k: v for k, v in self.toggles.items() if v is not None
            },
        }
