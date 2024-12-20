import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Any

if TYPE_CHECKING:
    from pypacks.datapack import Datapack

# https://minecraft.wiki/w/Predicate#JSON_format
PredicateConditionType = Literal["all_of", "any_of", "block_state_property", "damage_source_properties", "enchantment_active_check",
                                 "entity_properties", "entity_scores", "inverted", "killed_by_player", "location_check", "match_tool",
                                 "random_chance", "random_chance_with_enchanted_bonus", "reference", "survives_explosion",
                                 "table_bonus", "time_check", "value_check", "weather_check"]
# TODO: Do I want to type this as classes?


@dataclass
class Predicate:
    # https://minecraft.wiki/w/Predicate
    internal_name: str
    condition: PredicateConditionType
    extra_data: dict[str, Any] | None = None

    datapack_subdirectory_name: str = field(init=False, repr=False, default="predicate")

    def to_dict(self, datapack: "Datapack") -> dict[str, str]:
        return {
            "condition": self.condition,
            **(self.extra_data or {})
        }

    def create_datapack_files(self, datapack: "Datapack") -> None:
        with open(Path(datapack.datapack_output_path)/"data"/datapack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(datapack), file, indent=4)

# The root element of the predicate.
#  condition: The resource location of the condition type to check.
# Other parts of the predicate, specified below.
# The possible values for  condition and associated extra contents:

# all_of—Evaluates a list of predicates and passes if all of them pass. Invokable from any context.
#  terms: The list of predicates to evaluate. A predicate within this array must be a  object.
#  A predicate, following this structure recursively.
# any_of—Evaluates a list of predicates and passes if any one of them passes. Invokable from any context.
#  terms: The list of predicates to evaluate. A predicate within this array must be a  object.
#  A predicate, following this structure recursively.
# block_state_property—Checks the mined block and its block states. Requires block state provided by loot context, and always fails if not provided.
#  block: A block ID. The test fails if the block doesn't match.
#  properties: (Optional) A map of block state names to values. Errors if the block doesn't have these properties.
#  name: A block state and a exact value. The value is a string.
#  name: A block state name and a ranged value to match.
#  min: The min value.
#  max: The max value.
# damage_source_properties—Checks properties of the damage source. Requires origin and damage source provided by loot context, and always fails if not provided.
#  predicate: Predicate applied to the damage source.
# Tags common to all damage types[]
# enchantment_active_check—Checks if the enchantment has been active. Requires enchantment active status provided by loot context, and always fails if not provided. It is therefore only usable from the enchanted_location loot context.
#  active: Whether to check for an active (true) or inactive (false) enchantment.
# entity_properties—Checks properties of an entity. Invokable from any context.
#  entity: The entity to check. Specifies an entity from loot context. Can be this, attacker, direct_attacker, or attacking_player.
#  predicate: Predicate applied to entity, uses same structure as advancements.
# All possible conditions for entities[]
# entity_scores—Checks the scoreboard scores of an entity. Requires the specified entity provided by loot context, and always fails if not provided.
#  entity: The entity to check. Specifies an entity from loot context. Can be this, attacker, direct_attacker, or attacking_player.
#  scores: Scores to check. All specified scores must pass for the condition to pass.
#  A score: Key name is the objective while the value specifies a range of score values required for the condition to pass.
#  min: A number provider. Minimum score. Optional.
#  max: A number provider. Maximum score. Optional.
#  A score: Shorthand version of the other syntax above, to check the score against a single number only. Key name is the objective while the value is the required score.
# inverted—Inverts another predicate condition. Invokable from any context.
#  term: The condition to be negated, following the same structure as outlined here, recursively.
# killed_by_player—Checks if there is a attacking_player entity provided by loot context. Requires attacking_player entity provided by loot context, and always fails if not provided.
# location_check—Checks the current location against location criteria. Requires origin provided by loot context, and always fails if not provided.
#  offsetX: An optional x offset to the location.
#  offsetY: An optional y offset to the location.
#  offsetZ: An optional z offset to the location.
#  predicate: Predicate applied to location, uses same structure as advancements.
# Tags common to all locations[]
# match_tool—Checks tool used to mine the block. Requires tool provided by loot context, and always fails if not provided.
#  predicate: Predicate applied to item, uses same structure as advancements.
# All possible conditions for items[]
# random_chance—Generates a random number between 0.0 and 1.0, and checks if it is less than a specified value. Invokable from any context.
#  chance: A number provider. Success rate as a number 0.0–1.0.
# random_chance_with_enchanted_bonus—Generates a random number between 0.0 and 1.0, and checks if it is less than the value determined using the level of a given enchantment. Requires attacker entity provided by loot context, and if not provided, the enchantment level is regarded as 0.
#  unenchanted_chance: The success rate to use when the enchantment is not present; 0.0–1.0.
#  enchanted_chance: level-based value. The success rate based on the level when then enchantment is present; 0.0–1.0.
#  enchantment: One enchantment (an  ID). The enchantment whose level to use for the chance calculation. If the enchantment is not present, uses 0 as level.
# reference—Invokes a predicate file and returns its result. Invokable from any context.
#  name: The resource location of the predicate to invoke. A cyclic reference causes a parsing failure.
# survives_explosion—Returns success with 1 ÷ explosion radius probability. Requires explosion radius provided by loot context, and always success if not provided.
# table_bonus—Passes with probability picked from a list, indexed by enchantment power. Requires tool provided by loot context. If not provided, the enchantment level is regarded as 0.
#  enchantment: Resource location of enchantment.
#  chances: List of probabilities for enchantment power, indexed from 0.
# time_check—Compares the current day time (or rather, 24000 * day count + day time) against given values. Invokable from any context.
#  value: The time to compare the day time against.
#  min: A number provider. The minimum value.
#  max: A number provider. The maximum value.
#  value: Shorthand version of  value above, used to check for a single value only. Number providers cannot be used in this shorthand form.
#  period: If present, the day time is first reduced modulo the given number before being checked against  value. For example, setting this to 24000 causes the checked time to be equal to the current daytime.
# value_check—Compares a number against another number or range of numbers. Invokable from any context.
#  value: A number provider. The number to test.
#  range: The range of numbers to compare  value against.
#  min: A number provider. The minimum value.
#  max: A number provider. The maximum value.
#  range: Shorthand version of  range above, used to compare  value against a single number only. Number providers cannot be used in this shorthand form.
# weather_check—Checks the current game weather. Invokable from any context.
#  raining: If true, the condition passes only if it is raining or thundering.
#  thundering: If true, the condition passes only if it is thundering.
