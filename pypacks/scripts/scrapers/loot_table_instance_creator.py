import os
from dataclasses import fields, MISSING
from typing import Any

import requests

from pypacks.resources.custom_loot_tables.custom_loot_table import CustomLootTable, Pool, SingletonEntry
from pypacks.resources.custom_loot_tables.functions import SetCountFunction


def overridden_repr(self) -> str:  # type: ignore[no-untyped-def]
    """This function overrides the dataclasses "__repr" function to only show non-default attributes, so when we create them, it doesn't
    show unnecessary information, i.e. ones that are already default."""
    # Calculate default values, considering both default and default_factory
    default_values = {
        field.name: (field.default_factory() if field.default_factory is not MISSING else field.default)
        for field in fields(self)
        if field.default is not MISSING or field.default_factory is not MISSING
    }

    # Exclude fields with `init=False` or `repr=False` and those that match defaults
    non_default_attrs = {
        key: value for key, value in self.__dict__.items()
        if key not in {field.name for field in fields(self) if not field.init or not field.repr}
        and (key not in default_values or default_values[key] != value)
    }

    # Return formatted non-default attributes
    return f"{self.__class__.__name__}({', '.join(f'{key}={repr(value)}' for key, value in non_default_attrs.items())})"


for cls in [CustomLootTable, Pool, SingletonEntry, SetCountFunction]:  # CustomItem
    cls.__repr__ = overridden_repr  # type: ignore[assignment]


all_loot_table_data: dict[str, Any] = requests.get("https://raw.githubusercontent.com/misode/mcmeta/refs/heads/summary/data/loot_table/data.min.json").json()

# loot_table_name = "spawners/trail_chamber/key"
# data = {'type': 'minecraft:chest', 'pools': [{'bonus_rolls': 0.0, 'entries': [{'type': 'minecraft:item', 'name': 'minecraft:trial_key'}], 'rolls': 1.0}], 'random_sequence': 'minecraft:spawners/trial_chamber/key'}
# a = CustomLootTable.from_dict(loot_table_name, data)
# rint(a)

lines = [
    "from pypacks.resources.custom_loot_tables.custom_loot_table import CustomLootTable, Pool, SingletonEntry",
    "from pypacks.resources.custom_loot_tables.functions import (",
    "    SetStewEffectFunction, SetCountFunction, EnchantRandomlyFunction, EnchantWithLevelsFunction, SetDamageFunction, SetPotionFunction, SetInstrumentFunction,",
    "    ExplorationMapFunction, SetNameFunction, EnchantedCountIncreaseFunction, FurnaceSmeltFunction, SetOminousBottleAmplifier, SetEnchantsFunction,",
    ")",
    "from pypacks.providers.number_provider import UniformNumberProvider",
    "from pypacks.providers.enchantment_level_based_provider import LinearEnchantmentLevelBasedProvider",
    "from pypacks.additions.item_components import PotionEffect",
    "from pypacks.resources.custom_tag import CustomTag",
    "from pypacks.resources.predicate.predicate_conditions import DamageTypeTag, LocationTag, EntityCondition",
    "from pypacks.resources.custom_predicate import KilledByPlayerPredicate, EntityPropertiesPredicate, RandomChancePredicate, DamageSourcePropertiesPredicate, RandomChanceWithEnchantedBonusPredicate, LocationCheckPredicate, InvertedPredicate",
    "",
    "",
]

loot_table_names = []
loot_tables_instances = []
for loot_table_name, data in all_loot_table_data.items():
    if data["type"] == "minecraft:block":  # For now, ignore these... there's so many
        continue
    loot_table = CustomLootTable.from_dict(loot_table_name, data)
    # if loot_table.internal_name in ["archaeology_ocean_ruin_cold", "entities_fox"]:
    #     rint(data)
    loot_table_names.append(loot_table_name)
    loot_tables_instances.append(loot_table)

lines += [f"{x.internal_name.upper()} = {repr(x)}" for x in loot_tables_instances]

output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\minecraft\\loot_tables.py"
with open(output_path, "w") as file:
    file.write("\n".join(lines)+"\n")
