from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, Any, TypeAlias, Sequence

from pypacks.resources.base_resource import BaseResource
from pypacks.resources.custom_predicate import Predicate
from pypacks.utils import recursively_remove_nones_from_data
from pypacks.resources.custom_loot_tables.functions import LootTableFunction, SetCountFunction, SetComponentsFunction
from pypacks.providers.number_provider import NumberProvider, UniformNumberProvider

if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.resources.custom_item import CustomItem

LootContextTypes = Literal["empty", "chest", "fishing", "entity", "equipment", "archaeology", "vault",
                           "gift", "barter", "advancement_reward", "generic", "block", "shearing"]
LootContextPredicateTypes = Literal["command", "selector", "advancement_entity", "block_use", "enchanted_damage", "enchanted_item", "enchanted_location",
                                    "enchanted_entity", "hit_block"]
# guaranteed_context_parameters = {
#     "empty": [],  # None
#     "chest": ["Origin"],  # `Origin`: The center of the chest
#     "fishing": ["Origin", "Tool"],  # `Origin`: The position of the fishing bobber | `Tool`: The fishing rod item that the player cast
#     "entity": ["this", "Origin", "Damage Source"],  # `this` entity: The entity that died | `Origin`: The location of the entity's death | `Damage source`: The source of the damage that caused the entity to die
#     "equipment": ["Origin", "this"],  # `Origin`: The position of the entity being spawned | `this` entity: The entity being spawned.
#     "archaeology": ["Origin"],  # `Origin`: The center of the suspicious block
#     "vault": ["Origin"],  # `Origin`: The center of the vault
#     "gift": ["this", "Origin"],  # `Origin`: The cat, villager or sniffer's location | `this` entity: The cat, villager or sniffer that gave the gift / The chicken that laid the item
#     "barter": ["this"],  # `this` entity: The piglin bartered with.
#     "advancement_reward": ["this"],  # `this` entity: The player that earned the advancement | `Origin`: The player's location when they gained the advancement
#     "generic": [],  # N/A
#     "block": ["Block state", "Origin", "Tool"],  # `Block state`: The block that was broken | `Origin`: The center of the broken block | `Tool`: The tool used to mine the block
#     "sheering": ["Origin"],  # `Origin`: The position of the entity being sheared
# }
# potential_context_parameters = {
#     "empty": [],  # None
#     "chest": ["this"],  # `this` entity: The entity that opened the chest
#     "fishing": ["this"],  # `this` entity: The fishing bobber
#     "entity": ["attacker", "direct_attacker", "attacking_player"],  # `attacker` entity: The entity that was the source of the final damage to the victim entity | `direct_attacker` entity: The entity that directly contacted the victim entity to kill them | `attacking_player` entity: The player that most recently damaged the victim entity
#     "equipment": [],
#     "archaeology": ["this"],  # `this` entity: The entity that used the brush on the suspicious block
#     "vault": ["this"],  # `this` entity: The entity that opened the vault. Not present for item display inside vaults
#     "gift": [],
#     "barter": [],
#     "advancement_reward": [],
#     "generic": [],  # N/A
#     "block": ["this", "Block", "Explosion radius"],  # `this` entity: The player that mined the block, or the entity that caused the explosion | `Block` entity: Any block entity data of the block that was broken, if it was a block entity | `Explosion` radius: The radius of the explosion that broke the block, if broken via an explosion
#     "sheering": ["this"],  # `this` entity: The entity being sheared
# }


# class RandomSequence:
#     # https://minecraft.wiki/w/Random_sequence_format#NBT_structure
#     include_sequence_id: bool = True
#     include_world_seed: bool = True
#     salt: int = 0   # Data version = "4179"

# ================================================================================================================== #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ENTRY~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ================================================================================================================== #


@dataclass
class SingletonEntry:
    """Base entry"""
    # https://minecraft.wiki/w/Loot_table#Entry

    item: "str | CustomItem | None" = None
    functions: list["LootTableFunction"] = field(default_factory=list)
    conditions: list["Predicate"] = field(default_factory=list)
    weight: int = 1
    quality: int = 0

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "type": "minecraft:item",
            "name": str(self.item) if self.item else None,
            "functions": [x.to_dict(pack_namespace) for x in self.functions] if self.functions else None,
            "conditions": [x.to_dict(pack_namespace) for x in self.conditions] if self.conditions else None,
            "weight": self.weight if self.weight != 1 else None,
            "quality": self.quality if self.quality != 0 else None,
        })

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SingletonEntry":
        internal_name = "INCOMPLETE"
        # if data.get("type") != "minecraft:item":
        #     rint(data)
        return cls(
            item=data.get("name"),
            functions=[LootTableFunction.from_dict(function) for function in data.get("functions", [])],
            conditions=[Predicate.from_dict(internal_name, condition) for condition in data.get("conditions", [])],
            weight=data.get("weight", 1),
            quality=data.get("quality", 0),
        )

    __repr__ = BaseResource.__repr__


# ================================================================================================================== #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~POOLS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ================================================================================================================== #


@dataclass
class Pool:
    # https://minecraft.wiki/w/Loot_table#Pool
    conditions: Sequence["Predicate"] = field(default_factory=list)
    functions: list[LootTableFunction] = field(default_factory=list)
    rolls: "int | NumberProvider" = 1
    bonus_rolls: int = 0
    entries: list[SingletonEntry] = field(default_factory=list)

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "conditions": [condition.to_dict(pack_namespace) for condition in self.conditions] if self.conditions else None,
            "functions": [function.to_dict(pack_namespace) for function in self.functions] if self.functions else None,
            "rolls": self.rolls,
            "bonus_rolls": self.bonus_rolls,
            "entries": [entry.to_dict(pack_namespace) for entry in self.entries]

        })

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Pool":
        internal_name = "INCOMPLETE"
        return cls(
            conditions=[Predicate.from_dict(internal_name, condition) for condition in data.get("conditions", [])],
            functions=[LootTableFunction.from_dict(function) for function in data.get("functions", [])],
            rolls=int(data["rolls"]) if isinstance(data["rolls"], (int, float)) else NumberProvider.from_dict(data["rolls"]),
            bonus_rolls=int(data.get("bonus_rolls", 0)),
            entries=[SingletonEntry.from_dict(entry) for entry in data["entries"]],
        )

    __repr__ = BaseResource.__repr__


@dataclass
class SimpleRangePool:
    item: "str | CustomItem"
    min_count: int
    max_count: int

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        from pypacks.resources.custom_item import CustomItem
        return {
            "rolls": 1,
            "entries": [
                SingletonEntry(
                    item=self.item,
                    functions=[  # pyright: ignore
                        SetCountFunction(number_provider=UniformNumberProvider(min=self.min_count, max=self.max_count)),
                    ] + ([
                        SetComponentsFunction(components=self.item.to_dict(pack_namespace))
                    ] if isinstance(self.item, CustomItem) else []),
                ).to_dict(pack_namespace),
            ],
        }


@dataclass
class SingleItemPool:
    item: "str | CustomItem"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return SimpleRangePool(self.item, min_count=1, max_count=1).to_dict(pack_namespace)


LootTablePool: TypeAlias = "Pool | SingleItemPool | SimpleRangePool"

# ================================================================================================================== #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LOOT TABLES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ================================================================================================================== #


@dataclass
class CustomLootTable(BaseResource):
    # https://minecraft.wiki/w/Loot_table
    internal_name: str
    pools: Sequence["LootTablePool"] = field(default_factory=list)
    functions: list["LootTableFunction"] = field(default_factory=list)
    random_sequence: str | None = None
    loot_table_type: LootContextTypes = "generic"

    datapack_subdirectory_name: str = field(init=False, repr=False, default="loot_table")

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return recursively_remove_nones_from_data(  # type: ignore[no-any-return]
            {
                "pools": [pool.to_dict(pack_namespace) for pool in self.pools] if self.pools else None,
                "functions": [function.to_dict(pack_namespace) for function in self.functions] if self.functions else None,
                "random_sequence": self.random_sequence,
                "type": self.loot_table_type if self.loot_table_type != "generic" else None,
            }
        )

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "CustomLootTable":
        return cls(
            internal_name,
            pools=[Pool.from_dict(pool) for pool in data.get("pools", [])],
            functions=[LootTableFunction.from_dict(function) for function in data.get("functions", [])],
            random_sequence=data.get("random_sequence"),
            loot_table_type=data.get("type", "generic").removeprefix("minecraft:"),
        )

    def generate_give_command(self, pack: "Pack") -> str:
        return f"loot give @s loot {self.get_reference(pack.namespace)}"

    def get_spawn_command(self, pack_namespace: str) -> str:
        return f"loot spawn ~ ~ ~ loot {self.get_reference(pack_namespace)}"


class SingleItemLootTable(CustomLootTable):
    """Simple Util class for a loot table with a single item."""
    def __init__(self, internal_name: str, item: "str | CustomItem") -> None:
        super().__init__(internal_name, pools=[SingleItemPool(item)])


class SimpleRangeLootTable(CustomLootTable):
    """Simple Util class for a loot table with a single item with a simple range."""
    def __init__(self, internal_name: str, item: "str | CustomItem", min_count: int = 1, max_count: int = 1) -> None:
        super().__init__(internal_name, pools=[SimpleRangePool(item, min_count, max_count)])
