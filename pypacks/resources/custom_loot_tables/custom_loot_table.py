import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Any, TypeAlias

from pypacks.utils import recusively_remove_nones_from_dict, extract_item_type_and_components
from pypacks.resources.custom_loot_tables.functions import LootTableFunction

if TYPE_CHECKING:
    from pypacks.datapack import Datapack
    from pypacks.resources.custom_item import CustomItem

LootContextTypes = Literal["empty", "chest", "fishing", "entity", "equipment", "archaeology", "vault",
                          "gift", "barter", "advancement_reward", "generic", "block", "sheering"]
LootContextPredicateTypes = Literal["command", "selector", "advancement_entity", "block_use", "enchanted_damage", "enchanted_item", "enchanted_location",
                                    "enchanted_entity", "hit_block"]
guaranteed_context_parameters = {
    "empty": [],  # None
    "chest": ["Origin"],  # `Origin`: The center of the chest
    "fishing": ["Origin", "Tool"],  # `Origin`: The position of the fishing bobber | `Tool`: The fishing rod item that the player cast
    "entity": ["this", "Origin", "Damage Source"],  # `this` entity: The entity that died | `Origin`: The location of the entity's death | `Damage source`: The source of the damage that caused the entity to die
    "equipment": ["Origin", "this"],  # `Origin`: The position of the entity being spawned | `this` entity: The entity being spawned.
    "archaeology": ["Origin"],  # `Origin`: The center of the suspicious block
    "vault": ["Origin"],  # `Origin`: The center of the vault
    "gift": ["this", "Origin"],  # `Origin`: The cat, villager or sniffer's location | `this` entity: The cat, villager or sniffer that gave the gift / The chicken that laid the item
    "barter": ["this"],  # `this` entity: The piglin bartered with.
    "advancement_reward": ["this"],  # `this` entity: The player that earned the advancement | `Origin`: The player's location when they gained the advancement
    "generic": [],  # N/A
    "block": ["Block state", "Origin", "Tool"],  # `Block state`: The block that was broken | `Origin`: The center of the broken block | `Tool`: The tool used to mine the block
    "sheering": ["Origin"],  # `Origin`: The position of the entity being sheared
}
potential_context_parameters = {
    "empty": [],  # None
    "chest": ["this"],  # `this` entity: The entity that opened the chest
    "fishing": ["this"],  # `this` entity: The fishing bobber
    "entity": ["attacker", "direct_attacker", "attacking_player"],  # `attacker` entity: The entity that was the source of the final damage to the victim entity | `direct_attacker` entity: The entity that directly contacted the victim entity to kill them | `attacking_player` entity: The player that most recently damaged the victim entity
    "equipment": [],
    "archaeology": ["this"],  # `this` entity: The entity that used the brush on the suspicious block
    "vault": ["this"],  # `this` entity: The entity that opened the vault. Not present for item display inside vaults
    "gift": [],
    "barter": [],
    "advancement_reward": [],
    "generic": [],  # N/A
    "block": ["this", "Block", "Explosion radius"],  # `this` entity: The player that mined the block, or the entity that caused the explosion | `Block` entity: Any block entity data of the block that was broken, if it was a block entity | `Explosion` radius: The radius of the explosion that broke the block, if broken via an explosion
    "sheering": ["this"],  # `this` entity: The entity being sheared
}


# class RandomSequence:
#     # https://minecraft.wiki/w/Random_sequence_format#NBT_structure
#     include_sequence_id: bool = True
#     include_world_seed: bool = True
#     salt: int = 0   # Data version = "4179"

# ================================================================================================================== #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ENTRY~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ================================================================================================================== #


@dataclass
class Entry:
    """Base entry"""
    # https://minecraft.wiki/w/Loot_table#Entry

    # functions: list[ItemModifier] | None = None
    # conditions: list[Predicate] | None = None
    # weight: int = 1
    # quality: int = 0

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        return {}


@dataclass
class SingleItemRangeEntry(Entry):
    """Simple range entry for a single (custom) item."""
    item: "str | CustomItem"
    min_count: int = 1
    max_count: int = 1

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        item_type, combined_components = extract_item_type_and_components(self.item, datapack)
        return {
            "type": "minecraft:item",
            "name": item_type,
            "functions":
                [LootTableFunction("minecraft:set_count", {"count": {"min": self.min_count, "max": self.max_count}}).to_dict()] +
                ([LootTableFunction("minecraft:set_components", {"components": combined_components}).to_dict()] if combined_components else []),
        }


@dataclass
class BinomialDistributionEntry(Entry):
    """Binomial distribution entry for a single (custom) item."""
    item: "str | CustomItem"
    min_count: int
    max_count: int

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        item_type, combined_components = extract_item_type_and_components(self.item, datapack)
        return {
            "type": "minecraft:item",
            "name": item_type,
            "functions":
                [LootTableFunction("minecraft:set_count", {"binomial": {"min": self.min_count, "max": self.max_count}})] +  # TODO: Remove this, use the number provider
                ([LootTableFunction("minecraft:set_components", {"components": combined_components})] if combined_components else []),
        }


@dataclass
class UniformDistributionEntry(Entry):
    item: "str | CustomItem"
    min_count: int = 1
    max_count: int = 1

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        item_type, combined_components = extract_item_type_and_components(self.item, datapack)
        return {
            "type": "minecraft:item",
            "name": item_type,
            "functions":
                [LootTableFunction("minecraft:set_count", {"uniform": {"min": self.min_count, "max": self.max_count}}).to_dict()] +
                ([LootTableFunction("minecraft:set_components", {"components": combined_components}).to_dict()] if combined_components else []),
        }


PoolTableEntry: TypeAlias = "SingleItemRangeEntry | BinomialDistributionEntry | UniformDistributionEntry | Entry"

# ================================================================================================================== #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~POOLS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ================================================================================================================== #


@dataclass
class Pool:
    # https://minecraft.wiki/w/Loot_table#Pool
    # conditions: list[Predicate] | None
    functions: list[LootTableFunction] | None
    rolls: int = 1
    bonus_rolls: int | None = None
    entries: list[Entry] = field(default_factory=list)

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        data = {
            "rolls": self.rolls,
            "entries": [entry.to_dict(datapack) for entry in self.entries]
        }
        # if self.bonus_rolls:
        #     data["bonus_rolls"] = self.bonus_rolls
        # if self.conditions:
        #     data["conditions"] = [condition.to_dict(datapack) for condition in self.conditions]
        # if self.functions:
        #     data["functions"] = [function.to_dict(datapack) for function in self.functions]
        return data


@dataclass
class SimpleRangePool:
    item: "str | CustomItem"
    min_count: int
    max_count: int

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        return {
            "rolls": 1,
            "entries": [SingleItemRangeEntry(self.item, self.min_count, self.max_count).to_dict(datapack)]
        }


@dataclass
class SingleItemPool:
    item: "str | CustomItem"

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        return SimpleRangePool(self.item, min_count=1, max_count=1).to_dict(datapack)


LootTablePool: TypeAlias = "Pool | SingleItemPool | SimpleRangePool"

# ================================================================================================================== #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LOOT TABLES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ================================================================================================================== #


@dataclass
class CustomLootTable:
    # https://minecraft.wiki/w/Loot_table
    internal_name: str
    pools: list[LootTablePool] = field(default_factory=list)
    # functions: list[ItemModifier] | None = None   # God damn.
    # random_sequence: RandomSequence | None
    loot_table_type: LootContextTypes = "generic"

    datapack_subdirectory_name: str = field(init=False, repr=False, default="loot_table")

    def get_reference(self, datapack: "Datapack") -> str:
        return f"{datapack.namespace}:{self.internal_name}"

    def to_dict(self, datapack: "Datapack") -> dict[str, str]:
        return recusively_remove_nones_from_dict({
            "type": self.loot_table_type,
            "pools": [pool.to_dict(datapack) for pool in self.pools]
        })

    def create_datapack_files(self, datapack: "Datapack") -> None:
        with open(Path(datapack.datapack_output_path)/"data"/datapack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(datapack), file, indent=4)

    def generate_give_command(self, datapack: "Datapack") -> str:
        return f"loot give @p loot {datapack.namespace}:{self.internal_name}"


class SingleItemLootTable(CustomLootTable):
    def __init__(self, internal_name: str, item: "str | CustomItem"):
        self.internal_name = internal_name
        self.item = item

        super().__init__(internal_name, pools=[SingleItemPool(item)])

    # def to_dict(self, datapack: "Datapack") -> dict[str, str]:
    #     return recusively_remove_nones_from_dict({
    #         "type": "generic",
    #         "pools": [SingleItemPool(self.item).to_dict(datapack)]
    #     })


class SimpleRangeLootTable(CustomLootTable):
    def __init__(self, internal_name: str, item: "str | CustomItem", min_count: int = 1, max_count: int = 1) -> None:
        self.internal_name = internal_name
        self.item = item
        self.min_count = min_count
        self.max_count = max_count

        super().__init__(internal_name, pools=[SimpleRangePool(item, min_count, max_count)])

    # def to_dict(self, datapack: "Datapack") -> dict[str, str]:
    #     return recusively_remove_nones_from_dict({
    #         "type": "generic",
    #         "pools": [SimpleRangePool(self.item, self.min_count, self.max_count).to_dict(datapack)]
    #     })
