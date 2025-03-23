import os
from typing import Any

import requests

from pypacks.resources.custom_loot_tables.custom_loot_table import CustomLootTable

all_loot_table_data: dict[str, Any] = requests.get("https://raw.githubusercontent.com/misode/mcmeta/refs/heads/summary/data/loot_table/data.min.json").json()

lines = [
    "from pypacks.additions.item_components import PotionEffect",
    "from pypacks.providers.number_provider import UniformNumberProvider",
    "from pypacks.providers.enchantment_level_based_provider import LinearEnchantmentLevelBasedProvider",
    "from pypacks.resources.custom_loot_tables.custom_loot_table import CustomLootTable, Pool, SingletonEntry",
    "from pypacks.resources.custom_loot_tables.functions import (",
    "    SetStewEffectFunction, SetCountFunction, EnchantRandomlyFunction, EnchantWithLevelsFunction, SetDamageFunction, SetPotionFunction, SetInstrumentFunction,",
    "    ExplorationMapFunction, SetNameFunction, EnchantedCountIncreaseFunction, FurnaceSmeltFunction, SetOminousBottleAmplifier, SetEnchantsFunction,",
    ")",
    "from pypacks.resources.custom_tag import CustomTag",
    "from pypacks.resources.predicate.predicate_conditions import DamageTypeTag, LocationTag, EntityCondition",
    "from pypacks.resources.custom_predicate import KilledByPlayerPredicate, EntityPropertiesPredicate, RandomChancePredicate, DamageSourcePropertiesPredicate, RandomChanceWithEnchantedBonusPredicate, LocationCheckPredicate, InvertedPredicate",
    "",
    "",
]

loot_tables_instances = [
    CustomLootTable.from_dict(loot_table_name.replace("/", "_"), data)
    for loot_table_name, data in all_loot_table_data.items()
    if data["type"] != "minecraft:block"
]

lines += [f"{x.internal_name.upper().replace('/', '_')} = {repr(x)}" for x in loot_tables_instances]

output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\minecraft\\loot_tables.py"
with open(output_path, "w", encoding="utf-8") as file:
    file.write("\n".join(lines)+"\n")
