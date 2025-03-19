import os
from typing import Any

import requests

from pypacks.resources.base_resource import overridden_repr
from pypacks.resources.custom_dimension import CustomDimension, CustomDimensionType


for cls in [CustomDimension, ]:
    cls.__repr__ = overridden_repr  # type: ignore[assignment]


all_data: dict[str, Any] = requests.get("https://raw.githubusercontent.com/misode/mcmeta/refs/heads/summary/data/dimension/data.min.json").json()


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

names = []
instances: list["CustomDimension"] = []
for item_name, data in all_data.items():
    dimension = CustomDimension.from_dict(item_name, data)
    # if loot_table.internal_name in ["archaeology_ocean_ruin_cold", "entities_fox"]:
    #     rint(data)
    names.append(dimension.internal_name)
    instances.append(dimension)

lines += [f"{x.internal_name.upper()} = {repr(x)}" for x in instances]

output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\minecraft\\dimensions.py"
with open(output_path, "w") as file:
    file.write("\n".join(lines)+"\n")
