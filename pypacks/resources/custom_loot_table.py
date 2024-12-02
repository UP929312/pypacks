import json
from typing import TYPE_CHECKING, Literal
from dataclasses import dataclass, field

from pypacks.resources.custom_predicate import Predicate

if TYPE_CHECKING:
    from pypacks.datapack import Datapack

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


class ItemModifier:
    # https://minecraft.wiki/w/Item_modifier
    pass

class NumberProvider:
    # https://minecraft.wiki/w/Loot_table#Number_provider
    pass

class Entry:
    # https://minecraft.wiki/w/Loot_table#Entry
    pass

# class RandomSequence:
#     # https://minecraft.wiki/w/Random_sequence_format#NBT_structure
#     include_sequence_id: bool = True
#     include_world_seed: bool = True
#     salt: int = 0   # Data version = "4179"


@dataclass
class Pool:
    # https://minecraft.wiki/w/Loot_table#Pool
    conditions: list[Predicate] | None
    functions: list[ItemModifier] | None
    rolls: NumberProvider
    bonus_rolls: NumberProvider | None
    entries: list[Entry]


@dataclass
class CustomLootTable:
    # https://minecraft.wiki/w/Loot_table
    internal_name: str
    loot_table_type: LootContextTypes
    functions: list[ItemModifier] | None = None   # God damn.
    pools: list[dict[str, str]] | None = None
    # random_sequence: RandomSequence | None

    datapack_subdirectory_name: str = field(init=False, default="loot_table")

    def to_dict(self, datapack: "Datapack") -> dict[str, str]:
        data: dict[str, str] = {}
        return data

    def create_datapack_files(self, datapack: "Datapack") -> None:
        with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/{self.__class__.datapack_subdirectory_name}/{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(datapack), file, indent=4)

    def generate_give_command(self, datapack: "Datapack") -> str:
        data = '{"id": "minecraft:painting", "variant": "%s:%s"}' % (datapack.namespace, self.internal_name)
        return 'give @p minecraft:painting[minecraft:entity_data=%s]' % data