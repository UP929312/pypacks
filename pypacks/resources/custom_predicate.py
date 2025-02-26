import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Any

from pypacks.providers.int_provider import IntRange
from pypacks.providers.number_provider import NumberProvider

if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.resources.custom_enchantment import CustomEnchantment
    from pypacks.resources.predicate.predicate_conditions import DamageTypeTag, EntityCondition, LocationTag, ItemCondition


@dataclass
class Predicate:
    # https://minecraft.wiki/w/Predicate
    internal_name: str

    datapack_subdirectory_name: str = field(init=False, repr=False, default="predicate")

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        raise NotImplementedError
    
    def get_reference(self, pack_namespace: str) -> str:
        return f"{pack_namespace}:{self.internal_name}"

    def create_datapack_files(self, pack: "Pack") -> None:
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)


@dataclass
class AllOfPredicate(Predicate):
    """Evaluates a list of predicates and passes if all of them pass. Invokable from any context."""
    terms: list[Predicate]  # The list of predicates to evaluate.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "condition": "all_of",
            "terms": [term.to_dict(pack_namespace) for term in self.terms]
        }


@dataclass
class AnyOfPredicate(Predicate):
    """Evaluates a list of predicates and passes if any one of them passes. Invokable from any context."""
    terms: list[Predicate]  # The list of predicates to evaluate.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "condition": "any_of",
            "terms": [term.to_dict(pack_namespace) for term in self.terms]
        }


@dataclass
class BlockStatePropertyPredicate(Predicate):
    """Checks the mined block and its block states. Requires block state provided by loot context, and always fails if not provided."""
    block: str  # A block ID. The test fails if the block doesn't match.
    properties: dict[str, str | bool | dict[str, str]] | None = None  # A map of block state names to values. Errors if the block doesn't have these properties.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "condition": "block_state_property",
            "block": self.block,
            "properties": self.properties
        }


@dataclass
class DamageSourcePropertiesPredicate(Predicate):
    """Checks properties of the damage source. Requires origin and damage source provided by loot context, and always fails if not provided."""
    predicate: "DamageTypeTag"  # Predicate applied to the damage source.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "condition": "damage_source_properties",
            "predicate": self.predicate.to_dict(pack_namespace)
        }


@dataclass
class EnchantmentActiveCheckPredicate(Predicate):
    """Checks if the enchantment has been active. Requires enchantment active status provided by loot context, and always fails if not provided. It is therefore only usable from the enchanted_location loot context."""
    active: bool

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "condition": "enchantment_active_check",
            "active": self.active
        }


@dataclass
class EntityPropertiesPredicate(Predicate):
    """Checks properties of an entity. Invokable from any context."""
    entity: Literal["this", "attacker", "direct_attacker", "attacking_player"]  #  The entity to check. Specifies an entity from loot context. 
    predicate: "EntityCondition"  # Predicate applied to entity, uses same structure as advancements.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "condition": "entity_properties",
            "entity": self.entity,
            "predicate": self.predicate.to_dict(pack_namespace)
        }


@dataclass
class EntityScoresPredicate(Predicate):
    """Checks the scoreboard scores of an entity. Requires the specified entity provided by loot context, and always fails if not provided."""
    entity: Literal["this", "attacker", "direct_attacker", "attacking_player"]  # The entity to check. Specifies an entity from loot context.
    scores: dict[str, "IntRange"]  # Scores to check. All specified scores must pass for the condition to pass.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "condition": "entity_scores",
            "entity": self.entity,
            "scores": {key: value.to_dict() for key, value in self.scores.items()},
        }


@dataclass
class InvertedPredicate(Predicate):
    """Inverts another predicate condition. Invokable from any context."""
    term: Predicate  # The condition to be negated, following the same structure as outlined here, recursively.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "condition": "inverted",
            "term": self.term.to_dict(pack_namespace)
        }


@dataclass
class KilledByPlayerPredicate(Predicate):
    """Checks if there is a attacking_player entity provided by loot context.
    Requires attacking_player entity provided by loot context, and always fails if not provided."""
    
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "condition": "killed_by_player"
        }


@dataclass
class LocationCheckPredicate(Predicate):
    """Checks the current location against location criteria. Requires origin provided by loot context, and always fails if not provided."""
    predicate: "LocationTag"  # Predicate applied to location, uses same structure as advancements.
    offsetX: int = 0  # An optional x offset to the location.
    offsetY: int = 0  # An optional y offset to the location.
    offsetZ: int = 0  # An optional z offset to the location.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "condition": "location_check",
            "offsetX": self.offsetX,
            "offsetY": self.offsetY,
            "offsetZ": self.offsetZ,
            "predicate": self.predicate.to_dict(pack_namespace)
        }


@dataclass
class MatchToolPredicate(Predicate):
    """Checks tool used to mine the block. Requires tool provided by loot context, and always fails if not provided."""
    predicate: "ItemCondition"  # Predicate applied to item, uses same structure as advancements.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "condition": "match_tool",
            "predicate": self.predicate.to_dict(pack_namespace)
        }


@dataclass
class RandomChancePredicate(Predicate):
    """Generates a random number between 0.0 and 1.0, and checks if it is less than a specified value. Invokable from any context."""
    chance: "NumberProvider"  # Success rate as a number 0.0–1.0.

    # def __post_init__(self) -> None:
    #     assert 0 <= self.chance.value <= 1, "Chance must be between 0 and 1."

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "condition": "random_chance",
            "chance": self.chance.to_dict()
        }


@dataclass
class RandomChanceWithEnchantedBonusPredicate(Predicate):
    """Generates a random number between 0.0 and 1.0, and checks if it is less than the value determined using the level of a given enchantment.
    Requires attacker entity provided by loot context, and if not provided, the enchantment level is regarded as 0."""
    unenchanted_chance: float  # The success rate to use when the enchantment is not present; 0.0–1.0.
    enchanted_chance: float  # Level-based value. The success rate based on the level when then enchantment is present; 0.0–1.0.
    enchantment: "str | CustomEnchantment"  # The enchantment whose level to use for the chance calculation. If the enchantment is not present, uses 0 as level.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        from pypacks.resources.custom_enchantment import CustomEnchantment
        return {
            "condition": "random_chance_with_enchanted_bonus",
            "unenchanted_chance": self.unenchanted_chance,
            "enchanted_chance": self.enchanted_chance,
            "enchantment": self.enchantment.get_reference(pack_namespace) if isinstance(self.enchantment, CustomEnchantment) else self.enchantment
        }


@dataclass
class ReferencePredicate(Predicate):
    """Invokes a predicate file and returns its result. Invokable from any context."""
    name: "str | Predicate"  # The resource location of the predicate to invoke. A cyclic reference causes a parsing failure.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "condition": "reference",
            "name": self.name.get_reference(pack_namespace) if isinstance(self.name, Predicate) else self.name
        }


@dataclass
class SurvivesExplosionPredicate(Predicate):
    """Checks if the entity survives an explosion. Requires origin provided by loot context, and always fails if not provided."""
    
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "condition": "survives_explosion"
        }


@dataclass
class TableBonusPredicate(Predicate):
    """Passes with probability picked from a list, indexed by enchantment power. Requires tool provided by loot context.
    If not provided, the enchantment level is regarded as 0."""
    enchantment: "str | CustomEnchantment"
    chances: list[float]  # List of probabilities for enchantment power, indexed from 0.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        from pypacks.resources.custom_enchantment import CustomEnchantment
        return {
            "condition": "table_bonus",
            "enchantment": self.enchantment.get_reference(pack_namespace) if isinstance(self.enchantment, CustomEnchantment) else self.enchantment,
            "chances": self.chances
        }


@dataclass
class TimeCheckPredicate(Predicate):
    """Compares the current day time (or rather, 24000 * day count + day time) against given values. Invokable from any context."""
    number_provider: "int | NumberProvider"  # The time to compare the day time against.
    period: int | None = None  # If present, the day time is first reduced modulo the given number before being checked against the value. For example, setting this to 24000 causes the checked time to be equal to the current daytime.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        # TODO: Test/figure this out?
        return {
            "condition": "time_check",
            "value": self.number_provider.to_dict() if isinstance(self.number_provider, NumberProvider) else self.number_provider,
        } | {"period": self.period} if self.period is not None else {}
    # time_check—Compares the current day time (or rather, 24000 * day count + day time) against given values. Invokable from any context.
    # [NBT Compound / JSON Object] value: The time to compare the day time against.
    # [Int][NBT Compound / JSON Object] min: A number provider. The minimum value.
    # [Int][NBT Compound / JSON Object] max: A number provider. The maximum value.
    # [Int] value: Shorthand version of [NBT Compound / JSON Object] value above, used to check for a single value only. Number providers cannot be used in this shorthand form.
    # [Int] period: If present, the day time is first reduced modulo the given number before being checked against [NBT Compound / JSON Object][Int] value. For example, setting this to 24000 causes the checked time to be equal to the current daytime.


@dataclass
class ValueCheckPredicate(Predicate):
    """Compares a number against another number or range of numbers. Invokable from any context."""
    value: "int | NumberProvider"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "condition": "value_check",
            "value": self.value.to_dict() if isinstance(self.value, NumberProvider) else self.value,
    }
    # value_check—Compares a number against another number or range of numbers. Invokable from any context.
    # [Int][NBT Compound / JSON Object] value: A number provider. The number to test.
    # [NBT Compound / JSON Object] range: The range of numbers to compare [Int][NBT Compound / JSON Object] value against.
    # [Int][NBT Compound / JSON Object] min: A number provider. The minimum value.
    # [Int][NBT Compound / JSON Object] max: A number provider. The maximum value.
    # [Int] range: Shorthand version of [NBT Compound / JSON Object] range above, used to compare [Int][NBT Compound / JSON Object] value against a single number only. Number providers cannot be used in this shorthand form.


@dataclass
class WeatherCheckPredicate(Predicate):
    """Checks the current game weather. Invokable from any context."""
    raining: bool = False  # If true, the condition passes only if it is raining or thundering.
    thundering: bool = False  # If true, the condition passes only if it is thundering.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "condition": "weather_check",
            "raining": self.raining,
            "thundering": self.thundering
        }
