from typing import Any, Literal

from dataclasses import dataclass, field


# ==========================================================================================

@dataclass
class AttributeModifier:
    """Adds an attribute modifier.
    Warning, some only work when using the right equipment, e.g. mining efficiency only works with an axe on wood, or pickaxe on stone."""
    attribute_type: Literal[
        "armor", "armor_toughness", "attack_damage", "attack_knockback", "generic.attack_reach", "attack_speed", "flying_speed",
        "follow_range", "knockback_resistance", "luck", "max_absorption", "max_health", "movement_speed", "scale", "step_height",
        "jump_strength", "block_interaction_range", "entity_interaction_range", "spawn_reinforcements", "block_break_speed",
        "gravity", "safe_fall_distance", "fall_damage_multiplier", "burning_time", "explosion_knockback_resistance", "mining_efficiency",
        "movement_efficiency", "oxygen_bonus", "sneaking_speed", "submerged_mining_speed", "sweeping_damage_ratio", "tempt_range",
        "water_movement_efficiency"
    ]
    slot: Literal["any", "hand", "armor", "mainhand", "offhand", "head", "chest", "legs", "feet", "body"] = "any"
    amount: int = 1
    operation: Literal["add_value", "add_multiplied_base", "add_multiplied_total"] = "add_value"

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.attribute_type,
            "amount": self.amount,
            "operation": self.operation,
            "id": f"attribute_modifier.{self.attribute_type}",
        }

# ==========================================================================================


@dataclass
class EntityData:
    """Adds entity data to the item. Used in paintings, armor stands, item frames, etc"""
    data: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return self.data

# ==========================================================================================


@dataclass
class Equippable:
    slot: Literal["head", "chest", "legs", "feet", "body", "mainhand", "offhand"]
    equip_sound: str | None = None  # Sound event to play when the item is equipped
    model: str | None = None
    dispensable: bool = True  # whether the item can be equipped by using a Dispenser

    def to_dict(self) -> dict[str, Any]:
        return {
            "slot": self.slot,
            "equip_sound": self.equip_sound,
            "model": self.model,
            "dispensable": True if self.dispensable else None,  # Defaults to False
        }


# ==========================================================================================


@dataclass
class Consumable:
    # https://minecraft.wiki/w/Data_component_format#consumable
    # https://www.minecraft.net/en-us/article/minecraft-snapshot-24w34a
    consume_seconds: float = 1.6  # how long it takes to consume the item in seconds
    animation: Literal["none", "eat", "drink", "block", "bow", "spear", "crossbow", "spyglass", "toot_horn", "brush", "bundle"] | None = None  # the animation to play when consuming the item
    sound: str | None = None  # the sound to play when consuming the item
    has_consume_particles: bool = True  # whether to show particles when consuming the item
    on_consume_effects: list[str] | None = None  # a list of status effects to apply when consuming the item

    def to_dict(self) -> dict[str, Any]:
        assert self.sound is None, "sound is not yet supported"
        assert self.on_consume_effects is None, "on_consume_effects is not yet supported"
        return {
            "consume_seconds": self.consume_seconds,
            "animation": self.animation,
            "sound": self.sound,  # "entity.generic.eat"
            "has_consume_particles": False if not self.has_consume_particles else None,  # Defaults to True
            "on_consume_effects": self.on_consume_effects,
        }


# ==========================================================================================


@dataclass
class Food:
    nutrition: int
    saturation: int
    can_always_eat: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "nutrition": self.nutrition,
            "saturation": self.saturation,
            "can_always_eat": True if self.can_always_eat else None,  # Defaults to False
        }


# ==========================================================================================


@dataclass
class UseRemainder:
    # TODO: Allow this to have components!
    item: str
    count: int = 1

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.item,
            "count": self.count,
        }


# ==========================================================================================


@dataclass
class JukeboxPlayable:
    song: str = "pigstep"
    show_in_tooltip: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "song": self.song,
            "show_in_tooltip": False if not self.show_in_tooltip else None,  # Defaults to True
        }


# ==========================================================================================


@dataclass
class LodestoneTracker:
    x: int
    y: int
    z: int
    dimension: Literal["overworld", "nether", "end"] = "overworld"
    tracked: bool = True

    allowed_items: list[str] = field(init=False, default_factory=lambda: ["minecraft:compass"])

    def to_dict(self) -> dict[str, Any]:
        return {
            "target": {
                "pos": [self.x, self.y, self.z],
                "dimension": self.dimension,
            },
            "tracked": False if not self.tracked else None,  # Defaults to True
        }


# ==========================================================================================

@dataclass
class ToolRule:
    blocks: str | list[str]  # The blocks to match with. Can be a block ID or a block tag with a #, or a list of block IDs.
    speed: float = 1.0  # If the blocks match, overrides the default mining speed. Optional.
    correct_for_drops: bool = True  # If the blocks match, overrides whether or not this tool is considered correct to mine at its most efficient speed, and to drop items if the block's loot table requires it. Optional.

    def to_dict(self) -> dict[str, Any]:
        return {"blocks": self.blocks, "speed": self.speed, "correct_for_drops": self.correct_for_drops}


@dataclass
class Tool:
    # https://minecraft.wiki/w/Data_component_format#tool
    default_mining_speed: float = 1.0  # The default mining speed of this tool, used if no rules override it. Defaults to 1.0.
    damage_per_block: int = 1  # The amount of durability to remove each time a block is broken with this tool. Must be a non-negative integer.
    rules: list[ToolRule] | None = None  # A list of rules for the blocks that this tool has a special behavior with.

    def to_dict(self) -> dict[str, Any]:
        return {
            "default_mining_speed": self.default_mining_speed,
            "damage_per_block": self.damage_per_block,
            "rules": [rule.to_dict() for rule in self.rules] if self.rules is not None else None,
        }


# ==========================================================================================


@dataclass
class Instrument:
    """Used for the goat horn, can take a default minecraft sound or a custom sound, create a custom sound using CustomSound, then 
    For sound_id, use {namespace}:{sound_internal_name}"""
    # https://minecraft.wiki/w/Data_component_format#instrument
    sound_id: str | Literal["ponder_goat_horn", "sing_goat_horn", "seek_goat_horn", "feel_goat_horn", "admire_goat_horn", "call_goat_horn", "yearn_goat_horn", "dream_goat_horn"]  # https://minecraft.wiki/w/Sounds.json#Sound_events
    description: str | None = None  # A string for the description of the sound.
    use_duration: int = 5  # A non-negative integer for how long the use duration is.
    instrument_range: int = 256  #  A non-negative float for the range of the sound (normal horns are 256).

    allowed_items: list[str] = field(init=False, default_factory=lambda: ["minecraft:goat_horn"])

    def to_dict(self) -> dict[str, Any]:
        # TODO: Allow a sound_id OR sound_event, or CustomSound (needs datapack though ):  )
        #DEFAULTS = "ponder_goat_horn", "sing_goat_horn", "seek_goat_horn", "feel_goat_horn", "admire_goat_horn", "call_goat_horn", "yearn_goat_horn", "dream_goat_horn"
        assert self.use_duration >= 0, "use_duration must be a non-negative integer"
        assert self.instrument_range >= 0, "range must be a non-negative integer"
        return {
            "description": self.description,
            "range": self.instrument_range,
            "sound_event": {"sound_id": self.sound_id},
            "use_duration": self.use_duration,
        }



# ==========================================================================================



@dataclass
class WritableBookContent:
    # https://minecraft.wiki/w/Data_component_format#writable_book_content
    pages: list[list[dict[str, str | bool]]] = field(default_factory=lambda: [[{"text": "Hello"}, {"text": "World"}]])  # Should be a list of pages, where a page is a list of objects, e.g. {text: "Hello, world!"}

    allowed_items: list[str] = field(init=False, default_factory=lambda: ["minecraft:writable_book"])

    def to_dict(self) -> dict[str, Any]:
        return {"pages": [str(x) for x in self.pages]}



@dataclass
class WrittenBookContent:
    # https://minecraft.wiki/w/Data_component_format#written_book_content
    title: str
    author: str = "PyPacks"
    pages: list[list[dict[str, str | bool]]] = field(default_factory=lambda: [[{"text": "Hello"}, {"text": "World"}]])  # Should be a list of pages, where a page is a list of objects, e.g. {text: "Hello, world!"}

    allowed_items: list[str] = field(init=False, default_factory=lambda: ["minecraft:written_book"])

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "author": self.author,
            "pages": [str(x) for x in self.pages],
        }


# ==========================================================================================

@dataclass
class Cooldown:
    seconds: float = 5.0
    cooldown_group: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "seconds": self.seconds,
            "cooldown_group": self.cooldown_group,
        }

# ==========================================================================================


EnchantmentType = Literal[
    "aqua_affinity", "bane_of_arthropods", "binding_curse", "blast_protection", "breach", "channeling",
    "density", "depth_strider", "efficiency", "feather_falling", "fire_aspect", "fire_protection", "flame",
    "fortune", "frost_walker", "impaling", "infinity", "knockback", "looting", "loyalty", "luck_of_the_sea",
    "lure", "mending", "multishot", "piercing", "power", "projectile_protection", "protection", "punch",
    "quick_charge", "respiration", "riptide", "sharpness", "silk_touch", "smite", "soul_speed", "sweeping_edge",
    "swift_sneak", "thorns", "unbreaking", "vanishing_curse", "wind_burst",
]

# ==========================================================================================


@dataclass
class CustomItemData:
    durability: int | None = None  # https://minecraft.wiki/w/Data_component_format#max_damage  <-- Tools only
    lost_durability: int | None = None  # https://minecraft.wiki/w/Data_component_format#damage  <-- Tools only
    enchantment_glint_override: bool = False  # https://minecraft.wiki/w/Data_component_format#enchantment_glint_override
    glider: bool = False  # https://minecraft.wiki/w/Data_component_format#glider
    unbreakable: bool = False  # https://minecraft.wiki/w/Data_component_format#unbreakable
    destroyed_in_lava: bool = True  # https://minecraft.wiki/w/Data_component_format#damage_resistant & https://minecraft.wiki/w/Tag#Damage_type_tags
    hide_tooltip: bool = False  # https://minecraft.wiki/w/Data_component_format#hide_tooltip
    hide_additional_tooltip: bool = False  # https://minecraft.wiki/w/Data_component_format#hide_additional_tooltip
    repaired_by: list[str] | None = None  # https://minecraft.wiki/w/Data_component_format#repairable  List of string or #tags
    repair_cost: int | None = None  # https://minecraft.wiki/w/Data_component_format#repair_cost  <-- Tools only

    enchantments: dict[EnchantmentType, int] | None = None  # https://minecraft.wiki/w/Data_component_format#enchantments
    loaded_projectiles: list[str] | None = None  # https://minecraft.wiki/w/Data_component_format#charged_projectiles  <-- Crossbows only, and only arrows
    player_head_username: "str | None" = None  # https://minecraft.wiki/w/Data_component_format#profile  <-- Player/Mob heads only
    custom_head_texture: "str | None" = None  # https://minecraft.wiki/w/Data_component_format#profile  <-- Player/Mob heads only
    ominous_bottle_amplifier: Literal[0, 1, 2, 3, 4] | None = None  # https://minecraft.wiki/w/Data_component_format#ominous_bottle_amplifier  <-- Ominous bottles only

    entity_data: "EntityData | None" = None
    cooldown: "Cooldown | None" = None
    equippable_slots: "Equippable | None" = None  # https://minecraft.wiki/w/Data_component_format#equippable
    consumable: "Consumable | None" = None  # https://minecraft.wiki/w/Data_component_format#consumable
    food: "Food | None" = None  # https://minecraft.wiki/w/Data_component_format#food
    use_remainder: "UseRemainder | None" = None
    jukebox_playable: "JukeboxPlayable | None" = None
    lodestone_tracker: "LodestoneTracker | None" = None
    tool: "Tool | None" = None
    instrument: "Instrument | None" = None  # <-- Goat horn only
    written_book_content: "WrittenBookContent | None" = None  # <-- Written book only
    writable_book_content: "WritableBookContent | None" = None  # <-- Book and Quill only
    attribute_modifiers: list[AttributeModifier] | None = None

    def __post_init__(self) -> None:
        assert self.durability is None or self.durability > 0, "durability must be a positive integer"
        assert self.lost_durability is None or self.lost_durability >= 0, "lost_durability must be a non-negative integer"
        assert (self.lost_durability is None or self.durability is None) or self.lost_durability <= self.durability, "lost_durability must be less than or equal to durability"
        assert self.repair_cost is None or self.repair_cost >= 0, "repair_cost must be a non-negative integer"
        assert not (self.player_head_username and self.custom_head_texture), "Cannot have both player_head_username and custom_head_texture"

    def to_dict(self) -> dict[str, Any]:
        profile = {"properties": [{"name": "textures", "value": self.custom_head_texture}]} if self.custom_head_texture else None
        return {
            "max_damage":                 self.durability if self.durability is not None else None,
            "damage":                     self.lost_durability if self.lost_durability is not None else None,
            "enchantment_glint_override": True if self.enchantment_glint_override else None,
            "glider":                     {} if self.glider else None,
            "unbreakable":                {"show_in_tooltip": False} if self.unbreakable else None,
            "damage_resistant":           {"types": "#minecraft:is_fire"} if not self.destroyed_in_lava else None,  # TODO: Test me
            "hide_tooltip":               True if self.hide_tooltip else None,  # Defaults to False
            "hide_additional_tooltip":    True if self.hide_additional_tooltip else None,  # Defaults to False
            "repairable":                 {"items": ", ".join(self.repaired_by)} if self.repaired_by is not None else None,
            "repair_cost":                self.repair_cost if self.repair_cost is not None else None,

            "enchantments":               self.enchantments if self.enchantments is not None else None,
            "charged_projectiles":        [{"id": projectile for projectile in self.loaded_projectiles}] if self.loaded_projectiles is not None else None,
            "profile":                    self.player_head_username if self.player_head_username else profile,
            "ominous_bottle_amplifier":   self.ominous_bottle_amplifier if self.ominous_bottle_amplifier is not None else None,

            "entity_data":                self.entity_data.to_dict() if self.entity_data is not None else None,
            "use_cooldown":               self.cooldown.to_dict() if self.cooldown is not None else None,
            "attribute_modifiers":        {"modifiers": [modifier.to_dict() for modifier in self.attribute_modifiers]} if self.attribute_modifiers is not None else None,
            "equippable":                 self.equippable_slots.to_dict() if self.equippable_slots is not None else None,
            "consumable":                 self.consumable.to_dict() if self.consumable is not None else None,
            "food":                       self.food.to_dict() if self.food is not None else None,
            "use_remainder":              self.use_remainder.to_dict() if self.use_remainder is not None else None,
            "jukebox_playable":           self.jukebox_playable.to_dict() if self.jukebox_playable is not None else None,
            "lodestone_tracker":          self.lodestone_tracker.to_dict() if self.lodestone_tracker is not None else None,
            "tool":                       self.tool.to_dict() if self.tool is not None else None,
            "instrument":                 self.instrument.to_dict() if self.instrument is not None else None,
            "written_book_content":       self.written_book_content.to_dict() if self.written_book_content is not None else None,
            "writable_book_content":      self.writable_book_content.to_dict() if self.writable_book_content is not None else None,
        }  # fmt: skip


# banner_patterns  MEH
# base_color - for shields MEH
# bees - for beehives/nests MEH
# block_entity_data MEH
# block_state MEH
# bucket_entity_data MEH
# bundle_contents Mehh
# can_break Mehhh
# can_place_on Meh
# consumable More work for effects and sound.
# container YES (for chests) =======================================
# container_loot MEH
# damage_resistant Hmmm  Maybe to make it resistant to lava like netherite? =======================================
# damage_resistant={types:"#minecraft:is_fire"}

# debug_stick_state no.
# death_protection HMMMM (totem of undying)
# dyed_color - leather armor only? MEH
# enchantable # NOT YET (custom enchants maybe?)
# equippable REDO, more stuff
# firework_explosion MEH
# fireworks MEH
# intangible_projectile MEH
# note_block_sound
# potion_contents
# recipes  - for knowledge book
# stored_enchantments MEH - For enchanted books?
# suspicious_stew_effects MEH
# tooltip_style maybe?
# trim MEH
