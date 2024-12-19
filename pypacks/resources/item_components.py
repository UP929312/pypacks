from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal


if TYPE_CHECKING:
    from pypacks.datapack import Datapack
    from pypacks.resources.custom_sound import CustomSound
    from pypacks.resources.custom_jukebox_song import CustomJukeboxSong
    from pypacks.resources.custom_item import CustomItem


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
            "slot": self.slot,
        }


# ==========================================================================================


@dataclass
class BannerPattern:
    """List of all patterns applied to the banner or the shield."""
    # https://minecraft.wiki/w/Data_component_format#banner_patterns
    pattern: Literal["base", "stripe_bottom", "stripe_top", "stripe_left", "stripe_right", "stripe_center", "stripe_middle", "stripe_downright",
                     "stripe_downleft", "small_stripes", "cross", "straight_cross", "diagonal_left", "diagonal_right", "diagonal_up_left",
                     "diagonal_up_right", "half_vertical", "half_vertical_right", "half_horizontal", "half_horizontal_bottom", "square_bottom_left",
                     "square_bottom_right", "square_top_left", "square_top_right", "triangle_bottom", "triangle_top", "triangles_bottom",
                     "triangles_top", "circle", "rhombus", "border", "curly_border", "bricks", "gradient", "gradient_up", "creeper", "skull",
                     "flower", "mojang", "globe", "piglin", "flow", "guster"]  # The pattern type.
    color: Literal["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"]  # The color for this pattern.

    allowed_items: list[str] = field(init=False, repr=False, hash=False, default_factory=lambda: ["banner", "shield"])

    def to_dict(self) -> dict[str, Any]:
        return {
            "pattern": self.pattern,
            "color": self.color,
        }


# ==========================================================================================


@dataclass
class Consumable:
    # https://minecraft.wiki/w/Data_component_format#consumable

    consume_seconds: float = 1.6  # How long it takes to consume the item in seconds
    animation: Literal["none", "eat", "drink", "block", "bow", "spear", "crossbow", "spyglass", "toot_horn", "brush", "bundle"] = "none"  # The animation to play when consuming the item
    sound: str | None = None  # The sound to play when consuming the item
    has_consume_particles: bool = True  # Whether to show particles when consuming the item

    # on_consume_effects: list["PotionEffect"] | None = None  # a list of status effects to apply when consuming the item
    # on_consume_remove_effects: list["str | PotionEffect"] | Literal["all"] | None = None  # a list of status effects to remove when consuming the item
    # on_consume_teleport_diameter: int | None = None  # the diameter of the teleportation area when consuming the item
    # TODO: Consume sounds and effects

    # If type is apply_effects:
    #   effects: A list of effect instances applied once consumed.
    #     id: The ID of the effect.
    #     probability: The chance for the above effects to be applied once consumed. Must be a positive float between 0.0 and 1.0. Defaults to 1.0.
    # If type is remove_effects:
    #     effects: A set of effects removed once consumed, as either a single ID or list of IDs.
    # If type is clear_all_effects: Clears all effects of the consumer.
    # If type is teleport_randomly:
    #     diameter: The diameter that the consumer is teleported within. Defaults to 16.0.

    def to_dict(self) -> dict[str, Any]:
        assert self.sound is None, "sound is not yet supported"
        # assert self.on_consume_effects is None, "on_consume_effects is not yet supported"
        return {
            "consume_seconds": self.consume_seconds,
            "animation": self.animation,
            "sound": self.sound,  # "entity.generic.eat"
            "has_consume_particles": False if not self.has_consume_particles else None,  # Defaults to True
            # "on_consume_effects": self.on_consume_effects,
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
class FireworkExplosion:
    """The explosion effect stored by this firework star."""
    # https://minecraft.wiki/w/Data_component_format#firework_explosion

    shape: Literal["small_ball", "large_ball", "star", "creeper", "burst"]  # The shape of the explosion.
    colors: list[int]  # The colors of the initial particles of the explosion, randomly selected from. This is a list of RGB ints, i.e. 0-16777215.
    fade_colors: list[int] = field(default_factory=list)  # The colors of the fading particles of the explosion, randomly selected from. This is a list of RGB ints, i.e. 0-16777215.
    has_trail: bool = False  # Whether or not the explosion has a trail effect (diamond).
    has_twinkle: bool = False  # Whether or not the explosion has a twinkle effect (glowstone dust).

    def to_dict(self) -> dict[str, Any]:
        assert [0 <= x <= 16777215 for x in self.colors], f"colours must be a list of RGB values, e.g. [16777215], recieved: {self.colors}"
        assert [0 <= x <= 16777215 for x in self.fade_colors] if self.fade_colors else True, f"fade_colours must be a list of RGB values, e.g. [16777215], recieved: {self.fade_colors}"
        return {
            "shape": self.shape,
            "colors": self.colors,
        } | ({
            "fade_colors": self.fade_colors if self.fade_colors else None,  # (Can have no fade colours)
        } if self.fade_colors else {}) | ({
            "trail": True if self.has_trail else None,  # Defaults to False
        } if self.has_trail else {}) | ({
            "twinkle": True if self.has_twinkle else None,  # Defaults to False
        } if self.has_twinkle else {})


@dataclass
class Firework:
    """The effects and duration stored in a firework.
    Passing in a negative flight duration will act like a positive one, but the firework won't explode (just fly up for the duration)."""

    explosions: list[FireworkExplosion]  # List of the explosion effects caused by this firework rocket.
    flight_duration: int = 1  # The flight duration of this firework rocket, i.e. the number of gunpowders used to craft it.

    allowed_items: list[str] = field(init=False, repr=False, hash=False, default_factory=lambda: ["firework_rocket"])

    def to_dict(self) -> dict[str, Any]:
        assert len(self.explosions) <= 256, "Firework can only have a maximum of 256 explosions"
        assert -128 <= self.flight_duration <= 127, "Flight duration must be an integer between -128 and 127"
        return {
            "explosions": [explosion.to_dict() for explosion in self.explosions],
            "flight_duration": self.flight_duration,
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
    item: "str | CustomItem"
    count: int = 1

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        from pypacks.resources.custom_item import CustomItem
        return {
            "id": self.item.base_item if isinstance(self.item, CustomItem) else self.item,
            "count": self.count,
        } | ({"components": self.item.to_dict(datapack.namespace)} if isinstance(self.item, CustomItem) else {})


# ==========================================================================================


@dataclass
class JukeboxPlayable:
    song: "str | CustomJukeboxSong" = "pigstep"
    show_in_tooltip: bool = True

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        from pypacks.resources.custom_jukebox_song import CustomJukeboxSong
        return {
            "song": f"{datapack.namespace}:{self.song.internal_name}" if isinstance(self.song, CustomJukeboxSong) else self.song,
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

    allowed_items: list[str] = field(init=False, repr=False, hash=False, default_factory=lambda: ["compass"])

    def to_dict(self) -> dict[str, Any]:
        return {
            "target": {
                "pos": [self.x, self.y, self.z],
                "dimension": self.dimension,
            },
            "tracked": False if not self.tracked else None,  # Defaults to True
        }


# ==========================================================================================

MapDecorationType = Literal[
    "player", "frame", "red_marker", "blue_marker", "target_x", "target_point", "player_off_map", "player_off_limits", "mansion", "monument",
    "banner_white", "banner_orange", "banner_magenta", "banner_light_blue", "banner_yellow", "banner_lime", "banner_pink", "banner_gray",
    "banner_light_gray", "banner_cyan", "banner_purple", "banner_blue", "banner_brown", "banner_green", "banner_red", "banner_black",
    "red_x", "desert_village", "plains_village", "savanna_village", "snowy_village", "taiga_village", "jungle_pyramid", "swamp_hut",
]

@dataclass(frozen=True)
class MapDecoration:
    type: MapDecorationType
    x: int
    z: int
    rotation: int = 0

    allowed_items: list[str] = field(init=False, repr=False, hash=False, default_factory=lambda: ["filled_map", "map"])

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "x": self.x,
            "z": self.z,
            "rotation": self.rotation,
        }

@dataclass
class MapData:
    map_id: int | None = None
    map_color: int | None = None
    map_decorations: list[MapDecoration] | None = None

    allowed_items: list[str] = field(init=False, repr=False, hash=False, default_factory=lambda: ["filled_map", "map"])

    def to_dict(self) -> dict[str, Any]:
        return {
            "map_id": self.map_id if self.map_id is not None else None,
            "map_color": self.map_color if self.map_color is not None else None,
            "map_decorations": {hash(x): x.to_dict() for x in self.map_decorations} if self.map_decorations is not None else None,
        }


# ==========================================================================================

PotionEffectType = Literal[
    "speed", "slowness", "haste", "mining_fatigue", "strength", "instant_health", "instant_damage", "jump_boost", "nausea", "regeneration",
    "resistance", "fire_resistance", "water_breathing", "invisibility", "blindness", "night_vision", "hunger", "weakness", "poison", "wither",
    "health_boost", "absorption", "saturation", "glowing", "levitation", "luck", "unluck", "slow_falling", "conduit_power", "dolphins_grace",
    "bad_omen", "hero_of_the_village", "darkness", "trial_omen", "raid_omen", "wind_charged", "weaving", "oozing", "infested",
]


@dataclass
class PotionEffect:
    """Adds an effect to the item, e.g. a potion effect"""
    # https://minecraft.wiki/w/Effect

    effect_name: PotionEffectType  # The ID of the effect, e.g. "jump_boost"
    amplifier: int = 0  # The amplifier of the effect, with level I having value 0. Optional, defaults to 0.
    duration: int | Literal["infinity"] = 1  # The duration of the effect in ticks. Value -1 is treated as infinity. Values 0 or less than -2 are treated as 1. Optional, defaults to 1 tick.
    ambient: bool = False  # Whether or not this is an effect provided by a beacon and therefore should be less intrusive on the screen. Optional, defaults to false.
    show_particles: bool = True  # Whether or not this effect produces particles. Optional, defaults to true.
    show_icon: bool = True  # Whether or not an icon should be shown for this effect. Optional, defaults to true.

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.effect_name,
            "amplifier": self.amplifier if self.amplifier != 0 else None,  # Defaults to 0
            "duration": -1 if self.duration == "infinity" else self.duration,
            "ambient": True if self.ambient else None,  # Defaults to False
            "show_particles": False if not self.show_particles else None,  # Defaults to True
            "show_icon": False if not self.show_icon else None,  # Defaults to True
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
    """Used for the goat horn, can take a default minecraft sound or a custom sound"""
    # https://minecraft.wiki/w/Data_component_format#instrument
    # https://minecraft.wiki/w/Sounds.json#Sound_events
    sound_id: "str | CustomSound" | Literal["ponder_goat_horn", "sing_goat_horn", "seek_goat_horn", "feel_goat_horn",
                                            "admire_goat_horn", "call_goat_horn", "yearn_goat_horn", "dream_goat_horn"]
    description: str | None = None  # A string for the description of the sound.
    use_duration: int = 5  # A non-negative integer for how long the use duration is.
    instrument_range: int = 256  #  A non-negative float for the range of the sound (normal horns are 256).

    allowed_items: list[str] = field(init=False, repr=False, hash=False, default_factory=lambda: ["goat_horn"])

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        from pypacks.resources.custom_sound import CustomSound
        assert 0 < self.use_duration <= 60, "use_duration must be a non-negative integer"
        assert 0 < self.instrument_range, "range must be a non-negative integer"
        return {
            "description": self.description,
            "range": self.instrument_range,
            "sound_event": {"sound_id": f"{datapack.namespace}:{self.sound_id.internal_name}" if isinstance(self.sound_id, CustomSound) else self.sound_id},
            "use_duration": self.use_duration,
        }



# ==========================================================================================



@dataclass
class WritableBookContent:
    # https://minecraft.wiki/w/Data_component_format#writable_book_content
    pages: list[str] = field(default_factory=lambda: ["Hello World"])  # Should be a list of pages as str (doesn't support JSON)

    allowed_items: list[str] = field(init=False, repr=False, hash=False, default_factory=lambda: ["writable_book"])

    def to_dict(self) -> dict[str, Any]:
        return {"pages": self.pages}


@dataclass
class WrittenBookContent:
    # https://minecraft.wiki/w/Data_component_format#written_book_content
    title: str = "Written Book"
    author: str = "PyPacks"
    pages: list[list[dict[str, str | bool]]] = field(default_factory=lambda: [[{"text": "Hello"}, {"text": "World"}]])  # Should be a list of pages, where a page is a list of objects, e.g. {text: "Hello, world!"}

    allowed_items: list[str] = field(init=False, repr=False, hash=False, default_factory=lambda: ["written_book"])

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
    durability: int | None = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#max_damage  <-- Tools only
    lost_durability: int | None = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#damage  <-- Tools only
    enchantment_glint_override: bool = field(default=False, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#enchantment_glint_override
    glider: bool = field(default=False, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#glider
    unbreakable: bool = field(default=False, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#unbreakable
    destroyed_in_lava: bool = field(default=True, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#damage_resistant & https://minecraft.wiki/w/Tag#Damage_type_tags
    hide_tooltip: bool = field(default=False, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#hide_tooltip
    hide_additional_tooltip: bool = field(default=False, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#hide_additional_tooltip
    repaired_by: list[str] | None = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#repairable  List of string or #tags
    repair_cost: int | None = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#repair_cost  <-- Tools only?

    enchantments: dict[EnchantmentType, int] | None = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#enchantments
    loaded_projectiles: list[Literal["arrow", "tipped_arrow", "spectral_arrow", "firework_rocket"] | str] | None = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#charged_projectiles  <-- Crossbows only, and only arrows
    player_head_username: "str | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#profile  <-- Player/Mob heads only
    custom_head_texture: "str | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#profile  <-- Player/Mob heads only
    note_block_sound: "str | CustomSound | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#note_block_sound  <-- Player heads only
    ominous_bottle_amplifier: Literal[0, 1, 2, 3, 4] | None = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#ominous_bottle_amplifier  <-- Ominous bottles only

    attribute_modifiers: list[AttributeModifier] | None = field(default=None, kw_only=True)
    banner_patterns: list[BannerPattern] | None = field(default=None, kw_only=True)
    cooldown: "Cooldown | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#use_cooldown
    consumable: "Consumable | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#consumable
    entity_data: "EntityData | None" = field(default=None, kw_only=True)
    equippable_slots: "Equippable | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#equippable
    firework_explosion: "FireworkExplosion | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#firework_explosion
    firework: "Firework | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#firework
    food: "Food | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#food
    jukebox_playable: "JukeboxPlayable | None" = field(default=None, kw_only=True)
    lodestone_tracker: "LodestoneTracker | None" = field(default=None, kw_only=True)
    map_data: "MapData | None" = field(default=None, kw_only=True)
    tool: "Tool | None" = field(default=None, kw_only=True)
    instrument: "Instrument | None" = field(default=None, kw_only=True)
    use_remainder: "UseRemainder | None" = field(default=None, kw_only=True)
    written_book_content: "WrittenBookContent | None" = field(default=None, kw_only=True)
    writable_book_content: "WritableBookContent | None" = field(default=None, kw_only=True)

    def __post_init__(self) -> None:
        assert self.durability is None or self.durability > 0, "durability must be a positive integer"
        assert self.lost_durability is None or self.lost_durability >= 0, "lost_durability must be a non-negative integer"
        assert (self.lost_durability is None or self.durability is None) or self.lost_durability <= self.durability, "lost_durability must be less than or equal to durability"
        assert self.repair_cost is None or self.repair_cost >= 0, "repair_cost must be a non-negative integer"
        assert not (self.player_head_username and self.custom_head_texture), "Cannot have both player_head_username and custom_head_texture"
        assert self.cooldown is None or self.cooldown.seconds > 0, "cooldown seconds must be positive, to remove the cooldown, set it to None (or don't pass it in.)"

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        from pypacks.resources.custom_sound import CustomSound
        profile = {"properties": [{"name": "textures", "value": self.custom_head_texture}]} if self.custom_head_texture else None
        return {
            "max_damage":                 self.durability,
            "damage":                     self.lost_durability,
            "enchantment_glint_override": True if self.enchantment_glint_override else None,
            "glider":                     {} if self.glider else None,
            "unbreakable":                {"show_in_tooltip": False} if self.unbreakable else None,
            "damage_resistant":           {"types": "#minecraft:is_fire"} if not self.destroyed_in_lava else None,  # TODO: Test me, well, replace is_fire for lava
            "hide_tooltip":               True if self.hide_tooltip else None,  # Defaults to False
            "hide_additional_tooltip":    True if self.hide_additional_tooltip else None,  # Defaults to False
            "repairable":                 {"items": ", ".join(self.repaired_by)} if self.repaired_by is not None else None,
            "repair_cost":                self.repair_cost,

            "enchantments":               self.enchantments,
            "charged_projectiles":        [{"id": projectile} for projectile in self.loaded_projectiles] if self.loaded_projectiles is not None else None,
            "profile":                    self.player_head_username if self.player_head_username else profile,
            "note_block_sound":           self.note_block_sound.get_reference(datapack) if isinstance(self.note_block_sound, CustomSound) else self.note_block_sound,
            "ominous_bottle_amplifier":   self.ominous_bottle_amplifier,

            "attribute_modifiers":        {"modifiers": [modifier.to_dict() for modifier in self.attribute_modifiers]} if self.attribute_modifiers is not None else None,
            "banner_patterns":            [pattern.to_dict() for pattern in self.banner_patterns] if self.banner_patterns is not None else None,
            "consumable":                 self.consumable.to_dict() if self.consumable is not None else None,
            "entity_data":                self.entity_data.to_dict() if self.entity_data is not None else None,
            "equippable":                 self.equippable_slots.to_dict() if self.equippable_slots is not None else None,
            "firework_explosion":         self.firework_explosion.to_dict() if self.firework_explosion is not None else None,
            "fireworks":                  self.firework.to_dict() if self.firework is not None else None,
            "food":                       self.food.to_dict() if self.food is not None else None,
            "jukebox_playable":           self.jukebox_playable.to_dict(datapack) if self.jukebox_playable is not None else None,
            "lodestone_tracker":          self.lodestone_tracker.to_dict() if self.lodestone_tracker is not None else None,
            "map_color":                  self.map_data.to_dict()["map_color"] if self.map_data is not None else None,
            "map_id":                     self.map_data.to_dict()["map_id"] if self.map_data is not None else None,
            "map_decorations":            self.map_data.to_dict()["map_decorations"] if self.map_data is not None else None,
            "tool":                       self.tool.to_dict() if self.tool is not None else None,
            "instrument":                 self.instrument.to_dict(datapack) if self.instrument is not None else None,
            "use_cooldown":               self.cooldown.to_dict() if self.cooldown is not None else None,
            "use_remainder":              self.use_remainder.to_dict(datapack) if self.use_remainder is not None else None,
            "written_book_content":       self.written_book_content.to_dict() if self.written_book_content is not None else None,
            "writable_book_content":      self.writable_book_content.to_dict() if self.writable_book_content is not None else None,
        }  # fmt: skip


# base_color - for shields MEH
# bees - for beehives/nests MEH
# block_entity_data MEH
# block_state MEH
# bucket_entity_data MEH
# bundle_contents Mehh
# can_break Mehhh
# can_place_on Meh
# consumable More work for effects and sound. ---
# container YES (for chests) =======================================
# container_loot MEH
# damage_resistant Hmmm  Maybe to make it resistant to lava like netherite? =======================================
# damage_resistant={types:"#minecraft:is_fire"}
# debug_stick_state no.
# death_protection HMMMM (totem of undying)
# dyed_color - leather armor only? MEH
# enchantable # NOT YET (custom enchants maybe?)
# equippable REDO, more stuff
# intangible_projectile MEH
# lock
# pot_decorations
# potion_contents --------------------------------
# recipes  - for knowledge book
# stored_enchantments MEH - For enchanted books?
# suspicious_stew_effects MEH
# tooltip_style maybe?
# trim MEH
