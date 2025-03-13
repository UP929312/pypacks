import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Any, TYPE_CHECKING, TypeAlias

from pypacks.resources.base_resource import BaseResource
from pypacks.utils import recursively_remove_nones_from_data

if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.scripts.repos.damage_types import DamageTypesType
    from pypacks.additions.item_components import PotionEffectType
    from pypacks.resources.custom_item import CustomItem
    from pypacks.resources.custom_mcfunction import MCFunction
    from pypacks.resources.custom_predicate import Predicate


@dataclass
class CustomEnchantment(BaseResource):
    # https://minecraft.wiki/w/Enchantment_definition
    internal_name: str
    description: dict[str, Any] | str  # A JSON text component - The description of the enchantment.
    exclusive_set: str | list[str] = field(repr=False, default_factory=list)  # One or more enchantments (an ID, a #tag, or an array containing IDs) - Enchantments that are incompatible with this enchantment
    supported_items: str | list[str] = field(repr=False, default_factory=list)  # One or more items (an ID, a #tag, or an array containing IDs) - Items on which this enchantment can be applied using an anvil or using the /enchant command.
    primary_items: str | list[str] = field(repr=False, default_factory=list)  # One or more items (an ID, a #tag, or an array containing IDs) - `MUST be a subset of supported_items` - Items for which this enchantment appears in an enchanting table. If empty, defaults to being the same as supported_items.
    weight: int = field(repr=False, default=1024)  # 1-1024 | Controls the probability of this enchantment when enchanting. The probability is determined weight/total weight * 100%, where total_weight is the sum of the weights of all available enchantments.
    max_level: int = field(repr=False, default=1)  # 1-255 | The maximum level of this enchantment.
    min_cost_base: int = field(repr=False, default=1)  # 1-100 | The minimum base cost of this enchantment in levels. The base cost range will be modified before use.
    per_level_increase_min: int = field(repr=False, default=1)  # 0-100 | The amount of levels added to the minimum for each level above level I.
    max_cost_base: int = field(repr=False, default=1)  # 1-100 | The maximum base cost of this enchantment in levels. The base cost range will be modified before use.
    per_level_increase_max: int = field(repr=False, default=1)  # 0-100 | The amount of levels added to the maximum for each level above level I.
    anvil_cost: int = field(repr=False, default=1)  # 0-100 |  The base cost when applying this enchantment to another item using an anvil. Halved when adding using a book, multiplied by the level of the enchantment.
    slots: list[Literal["any", "hand", "mainhand", "offhand", "armor", "feet", "legs", "chest", "head", "body"]] = field(default_factory=lambda: ["any"])  # List of equipment slots that this enchantment works in.
    effects: list["EnchantValueEffect | EnchantmentEntityEffect"] = field(repr=False, default_factory=list)  # Effect components - Controls the effect of the enchantment.

    datapack_subdirectory_name: str = field(init=False, repr=False, default="enchantment")

    def __post_init__(self) -> None:
        assert 0 < self.weight <= 1024, "Weight must be between 1 and 1024"
        assert 0 < self.max_level <= 255, "Max level must be between 1 and 255"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        effects = [effect.to_dict(pack_namespace) for effect in self.effects]
        effects_merged = {key: value for effect in effects for key, value in effect.items()}
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "description": self.description if isinstance(self.description, dict) else {"text": self.description},
            "exclusive_set": self.exclusive_set,
            "supported_items": self.supported_items,
            "primary_items": self.primary_items if self.primary_items else None,
            "weight": self.weight,
            "max_level": self.max_level,
            "min_cost": {
                "base": self.min_cost_base,
                "per_level_above_first": self.per_level_increase_min,
            },
            "max_cost": {
                "base": self.max_cost_base,
                "per_level_above_first": self.per_level_increase_max,
            },
            "anvil_cost": self.anvil_cost,
            "slots": self.slots,
            "effects": effects_merged if self.effects else None,
        })

    # @classmethod  # TODO: Do this
    # def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "CustomEnchantment":
    #     effects = [
    #         EnchantValueEffect(**data) if list(data.keys())[0] in  ValueEffectComponentIdType
    #         else EnchantmentEntityEffect(**data)
    #         for component_id, values in data.items() for value in values for component_id, value in value.items()
    #         for value in values for component_id, value in value.items()
    #     ]
    #     return cls(
    #         internal_name,
    #         description=data["description"],
    #         exclusive_set=data.get("exclusive_set", []),
    #         supported_items=data.get("supported_items", []),
    #         primary_items=data.get("primary_items", []),
    #         weight=data.get("weight", 1024),
    #         max_level=data.get("max_level", 1),
    #         min_cost_base=data.get("min_cost_base", 1),
    #         per_level_increase_min=data.get("per_level_increase_min", 1),
    #         max_cost_base=data.get("max_cost_base", 1),
    #         per_level_increase_max=data.get("per_level_increase_max", 1),
    #         anvil_cost=data.get("anvil_cost", 1),
    #         slots=data.get("slots", ["any"]),
    #         effects=effects,
    #     )

    def create_datapack_files(self, pack: "Pack") -> None:
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)

    def generate_custom_item(self, pack_namespace: str) -> "CustomItem":
        from pypacks.resources.custom_item import CustomItem
        from pypacks.additions.item_components import Components
        return CustomItem(
            f"{self.internal_name}_enchanted_book", "enchanted_book",
            custom_name=f"{self.description} Enchanted Book",
            components=Components(book_enchantments={self.get_reference(pack_namespace): 1})  # type: ignore[dict-item]
        )

# ====================================================================================================================
# region: VALUE EFFECTS:


ValueEffectComponentIdType = Literal[
    "minecraft:armor_effectiveness", "minecraft:damage", "minecraft:damage_protection", "minecraft:smash_damage_per_fallen_block",
    "minecraft:knockback", "minecraft:equipment_drops", "minecraft:ammo_use", "minecraft:projectile_piercing", "minecraft:block_experience",
    "minecraft:repair_with_xp", "minecraft:item_damage", "minecraft:projectile_count", "minecraft:trident_return_acceleration",
    "minecraft:projectile_spread", "minecraft:fishing_time_reduction", "minecraft:fishing_luck_bonus", "minecraft:mob_experience",
]


@dataclass
class EnchantValueEffect:
    component_id: "ValueEffectComponentIdType"  # The component ID of the effect.
    value_effect: "ValueEffect"  # Determines how to modify the value.
    requirements: "Predicate | None" = None  # Determines when the effect is active. Cannot be of type `minecraft:reference` - all predicates must be in-lined
    enchanted: Literal["attacker", "victim"] = "victim"  # Which entity has to have the enchantment

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            self.component_id: [
                {
                    "effect": self.value_effect,
                    "requirements": self.requirements.to_dict(pack_namespace) if self.requirements else None,
                    "enchanted": self.enchanted,
                },
            ]
        }


@dataclass
class SetValueEffect:
    """Sets the value to the specified value."""
    value: int | float  # Level based value determining the new value. - https://minecraft.wiki/w/Enchantment_definition#Level-based_value

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:set",
            "value": float(self.value),
        }


@dataclass
class AddValueEffect:
    """Adds the specified value to the old value."""
    value: int | float  # Level based value determining the value to add. - https://minecraft.wiki/w/Enchantment_definition#Level-based_value

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:add",
            "value": float(self.value),
        }


@dataclass
class MultiplyValueEffect:
    """Multiplies the old value with the specified factor."""
    factor: int | float  # Level based value determining the factor to multiply. - https://minecraft.wiki/w/Enchantment_definition#Level-based_value

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:multiply",
            "factor": float(self.factor),
        }


@dataclass
class RemoveBinomialValueEffect:
    """Runs multiple checks, each time reducing the value by 1 with the specified chance."""
    chance: float  # The chance to remove the value. - https://minecraft.wiki/w/Enchantment_definition#Level-based_value

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:remove_binomial",
            "chance": self.chance,
        }


@dataclass
class AllOfValueEffect:
    """Runs multiple value effects in series."""
    effects: list["ValueEffect"]

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:all_of",
            "effects": [effect.to_dict() for effect in self.effects],
        }


ValueEffect: TypeAlias = SetValueEffect | AddValueEffect | MultiplyValueEffect | RemoveBinomialValueEffect | AllOfValueEffect
# endregion
# ====================================================================================================================
# region: Attribute effects

# ???

# endregion
# ====================================================================================================================
# region: Entity effects

EntityEffectComponentIdType = Literal[
    "minecraft:hit_block", "minecraft:tick", "minecraft:projectile_spawned", "minecraft:post_attack",
]


@dataclass
class EnchantmentEntityEffect:
    component_id: "EntityEffectComponentIdType"
    entity_effect: "EntityEffect"
    requirements: "Predicate | None" = None
    enchanted: Literal["attacker", "victim", "damaging_entity"] = "victim"  # Which entity has to have the enchantment
    affected: Literal["attacker", "victim", "damaging_entity"] = "victim"  # Which entity is affected by the  effect.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            self.component_id: [
                {
                    "effect": self.entity_effect.to_dict(pack_namespace),
                    "requirements": self.requirements.to_dict(pack_namespace) if self.requirements else None,
                    "enchanted": self.enchanted,
                    "affected": self.affected,
                },
            ]
        }


@dataclass
class AllOfEntityEffect:
    """Runs multiple entity effects in sequence."""
    # https://minecraft.wiki/w/Enchantment_definition#all_of_2
    effects: list["EntityEffect"]

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:all_of",
            "effects": [effect.to_dict(pack_namespace) for effect in self.effects],
        }


@dataclass
class ApplyMobEffectEntityEffect:
    """Applies a status effect to the affected mob."""
    # https://minecraft.wiki/w/Enchantment_definition#apply_mob_effect
    effects: list["PotionEffectType"] | str  # The effects to apply (can also be a #tag).
    min_duration: float = 1.0  # Minimum possible duration of the effect in seconds
    max_duration: float = 5.0  # Maximum possible duration of the effect in seconds
    min_amplifier: float = 0.0  # Minimum possible amplifier of the effect
    max_amplifier: float = 1.0  # Maximum possible amplifier of the effect

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:apply_mob_effect",
            "to_apply": self.effects,
            "min_duration": self.min_duration,
            "max_duration": self.max_duration,
            "min_amplifier": self.min_amplifier,
            "max_amplifier": self.max_amplifier,
        }


@dataclass
class DamageEntityEntityEffect:
    """Deals (extra) damage to the affected entity."""
    # https://minecraft.wiki/w/Enchantment_definition#damage_entity
    damage_type: "DamageTypesType"
    min_damage: float = 0.5
    max_damage: float = 10.0

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:damage_entity",
            "damage_type": self.damage_type,
            "min_damage": self.min_damage,
            "max_damage": self.max_damage,
        }


@dataclass
class ChangeItemDamageEntityEffect:
    """Reduces the durability of the enchanted item."""
    # https://minecraft.wiki/w/Enchantment_definition#change_item_damage
    amount: int | float  # The amount to durability to remove from the item

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:change_item_damage",
            "amount": self.amount,
        }


ParticleTypes = Literal[
    "ambient_entity_effect", "angry_villager", "ash", "block", "block_crumble", "block_marker", "bubble", "bubble_column_up", "bubble_pop", "campfire_cosy_smoke",
    "campfire_signal_smoke", "cherry_leaves", "cloud", "composter", "crimson_spore", "crit", "current_down", "damage_indicator", "dolphin", "dragon_breath",
    "dripping_dripstone_lava", "dripping_dripstone_water", "dripping_honey", "dripping_lava", "dripping_obsidian_tear", "dripping_water", "dust", "dust_color_transition",
    "dust_pillar", "dust_plume", "effect", "egg_crack", "elder_guardian", "electric_spark", "enchant", "enchanted_hit", "end_rod", "entity_effect", "explosion",
    "explosion_emitter", "falling_dripstone_lava", "falling_dripstone_water", "falling_dust", "falling_honey", "falling_lava", "falling_nectar", "falling_obsidian_tear",
    "falling_spore_blossom", "falling_water", "firework", "fishing", "flame", "flash", "glow", "glow_squid_ink", "gust", "gust_emitter", "happy_villager", "heart",
    "infested", "instant_effect", "item", "item_cobweb", "item_slime", "item_snowball", "landing_honey", "landing_lava", "landing_obsidian_tear", "large_smoke",
    "lava", "mycelium", "nautilus", "note", "ominous_spawning", "pale_oak_leaves", "poof", "portal", "raid_omen", "rain", "reverse_portal", "scrape", "sculk_charge",
    "sculk_charge_pop", "sculk_soul", "shriek", "small_flame", "small_gust", "smoke", "sneeze", "snowflake", "sonic_boom", "soul", "soul_fire_flame", "spit",
    "splash", "spore_blossom_air", "squid_ink", "sweep_attack", "totem_of_undying", "trail", "trial_omen", "trial_spawner_detection", "trial_spawner_detection_ominous",
    "underwater", "vault_connection", "vibration", "warped_spore", "wax_off", "wax_on", "white_ash", "white_smoke", "witch"
]


@dataclass
class ExplodeEntityEffect:
    """Causes an explosion"""
    # https://minecraft.wiki/w/Enchantment_definition#explode
    attribute_to_user: bool = False  # Whether the explosion should be attributed to the user
    damage_type: "DamageTypesType" = "generic"
    immune_blocks: list[str] | str | None = field(default_factory=list)  # (an  ID, or a #tag, or an  array containing  IDs) - blocks that fully block the explosion and can't be destroyed.
    knockback_multiplier: float = 1.0  # The knockback multiplier of the explosion
    offset: tuple[float, float, float] = (0.0, 0.0, 0.0)  # X, Y, Z position offset to spawn the explosion.
    radius: float = 5.0  # The radius of the explosion
    create_fire: bool = True
    block_interaction: Literal["none", "block", "mob", "tnt", "trigger"] = "none"  # block = bed explosion, mob = creeper explosion, tnt = TNT explosion, trigger = wind charge
    small_particle: ParticleTypes = "explosion"
    large_particle: ParticleTypes = "explosion"
    sound: str = "entity.generic.explode"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:explode",
            "attribute_to_user": self.attribute_to_user,
            "damage_type": self.damage_type,
            "immune_blocks": self.immune_blocks,
            "knockback_multiplier": self.knockback_multiplier,
            "offset": list(self.offset),
            "radius": self.radius,
            "create_fire": self.create_fire,
            "block_interaction": self.block_interaction,
            "small_particle": self.small_particle,
            "large_particle": self.large_particle,
            "sound": self.sound,
        }


@dataclass
class IgniteEntityEffect:
    """Ignites the affected entity"""
    # https://minecraft.wiki/w/Enchantment_definition#ignite
    duration: float = 5.0

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:ignite",
            "duration": self.duration,
        }


@dataclass
class PlaySoundEntityEffect:
    """Plays a sound"""
    # https://minecraft.wiki/w/Enchantment_definition#play_sound
    sound: str  # The sound to play
    volume: float = 1.0  # Volume of the sound
    pitch: float = 1.0  # Pitch of the sound

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        assert 0.00001 <= self.volume <= 10.0, "Volume must be between 0.00001 and 10.0"
        assert 0.00001 <= self.pitch <= 2.0, "Volume must be between 0.00001 and 2.0"
        return {
            "type": "minecraft:play_sound",
            "sound": self.sound,
            "volume": self.volume,
            "pitch": self.pitch,
        }


@dataclass
class ReplaceBlockEntityEffect:
    """Places a block"""
    # https://minecraft.wiki/w/Enchantment_definition#replace_block
    block_state: dict[str, Any]
    offset: tuple[int, int, int]
    trigger_game_event: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] = 15
    predicate: "Predicate | None" = None

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:replace_block",
            "block_state": self.block_state,
            "offset": list(self.offset),
            "trigger_game_event": self.trigger_game_event,
            "predicate": self.predicate.to_dict(pack_namespace) if self.predicate else None,
        }


@dataclass
class ReplaceDiskEntityEffect:
    """Places a half-sphere?"""
    # https://minecraft.wiki/w/Enchantment_definition#replace_disk
    block_state: dict[str, Any]
    offset: tuple[int, int, int]
    radius: int
    height: int
    trigger_game_event: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] = 15
    predicate: "Predicate | None" = None

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:replace_disk",
            "block_state": self.block_state,
            "offset": list(self.offset),
            "radius": self.radius,
            "height": self.height,
            "trigger_game_event": self.trigger_game_event,
            "predicate": self.predicate.to_dict(pack_namespace) if self.predicate else None,
        }


@dataclass
class RunFunctionEntityEffect:
    """Run a function."""
    # https://minecraft.wiki/w/Enchantment_definition#run_function
    function: "str | MCFunction"  # Name of the function

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        from pypacks.resources.custom_mcfunction import MCFunction
        assert not isinstance(self.function, str) or " " not in self.function, f"Function name cannot contain spaces! Found: {self.function}"
        return {
            "type": "minecraft:run_function",
            "function": self.function.get_reference(pack_namespace) if isinstance(self.function, MCFunction) else self.function,
        }


@dataclass
class SetBlockPropertiesEntityEffect:
    """Sets the block properties of a block."""
    # https://minecraft.wiki/w/Enchantment_definition#set_block_properties
    block_states: dict[str, Any]
    offset: tuple[int, int, int]
    trigger_game_event: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] = 15

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:set_block_properties",
            "properties": self.block_states,
            "offset": list(self.offset),
            "trigger_game_event": self.trigger_game_event,
        }


@dataclass
class SpawnParticlesEntityEffect:
    """Spawns particles."""
    # https://minecraft.wiki/w/Enchantment_definition#spawn_particles
    particle: ParticleTypes
    horizontal_position_type: Literal["entity_position", "in_bounding_box"] = "entity_position"
    horizontal_position_offset: float = 0.0
    horizontal_position_scale: float = 1.0
    vertical_position_type: Literal["entity_position", "in_bounding_box"] = "entity_position"
    vertical_position_offset: float = 0.0
    vertical_position_scale: float = 1.0
    horizontal_velocity_base: float = 0.0
    horizontal_velocity_movement_scale: float = 1.0
    vertical_velocity_base: float = 0.0
    vertical_velocity_movement_scale: float = 1.0

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:spawn_particles",
            "particle": self.particle,
            "horizontal_position": {
                "type": self.horizontal_position_type,
                "offset": self.horizontal_position_offset,
                "scale": self.horizontal_position_scale,
            },
            "vertical_position": {
                "type": self.vertical_position_type,
                "offset": self.vertical_position_offset,
                "scale": self.vertical_position_scale,
            },
            "horizontal_velocity": {
                "base": self.horizontal_velocity_base,
                "movement_scale": self.horizontal_velocity_movement_scale,
            },
            "vertical_velocity": {
                "base": self.vertical_velocity_base,
                "movement_scale": self.vertical_velocity_movement_scale,
            },
        }


@dataclass
class SummonEntityEntityEffect:
    """Spawns an entity."""
    # https://minecraft.wiki/w/Enchantment_definition#summon_entity
    entity: str | list[str]  # One or more entity type(s) (an ID, or a #tag, or an array containing IDs) - The entity or entities [more information needed] to spawn
    join_team: bool = False  # Should the summoned entity join the team of the owner of the enchanted item?

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:summon_entity",
            "entity": self.entity,
            "join_team": self.join_team,
        }


EntityEffect: TypeAlias = (
    AllOfEntityEffect | ApplyMobEffectEntityEffect | DamageEntityEntityEffect | ChangeItemDamageEntityEffect | ExplodeEntityEffect | IgniteEntityEffect |
    PlaySoundEntityEffect | ReplaceBlockEntityEffect | ReplaceDiskEntityEffect | RunFunctionEntityEffect | SetBlockPropertiesEntityEffect |
    SpawnParticlesEntityEffect | SummonEntityEntityEffect
)
# endregion
# ====================================================================================================================
