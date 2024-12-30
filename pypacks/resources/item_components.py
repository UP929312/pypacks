from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal, TypeAlias


if TYPE_CHECKING:
    from pypacks.datapack import Datapack
    from pypacks.resources.custom_sound import CustomSound
    from pypacks.resources.custom_jukebox_song import CustomJukeboxSong
    from pypacks.resources.custom_item import CustomItem
    from pypacks.resources.custom_loot_tables.custom_loot_table import CustomLootTable

    from pypacks.scripts.loot_tables import LootTables
    from pypacks.scripts.damage_tags import DamageTagsType


# ==========================================================================================


# ArmorTrimItemType = Literal[
#     "bolt_armor_trim_smithing_template", "coast_armor_trim_smithing_template", "dune_armor_trim_smithing_template", "eye_armor_trim_smithing_template", 
#     "flow_armor_trim_smithing_template", "host_armor_trim_smithing_template", "netherite_upgrade_armor_trim_smithing_template", "raiser_armor_trim_smithing_template", 
#     "rib_armor_trim_smithing_template", "sentry_armor_trim_smithing_template", "shaper_armor_trim_smithing_template", "silence_armor_trim_smithing_template", 
#     "snout_armor_trim_smithing_template", "spire_armor_trim_smithing_template", "tide_armor_trim_smithing_template", "vex_armor_trim_smithing_template",
#     "ward_armor_trim_smithing_template", "wayfinder_armor_trim_smithing_template", "wild_armor_trim_smithing_template",
# ]
ArmorTrimType = Literal[
    "bolt", "coast", "dune", "eye", "flow", "host", "netherite_upgrade", "raiser", "rib", "sentry",
    "shaper", "silence", "snout", "spire", "tide", "vex", "ward", "wayfinder", "wild",
]
ArmorTrimMaterialType = Literal[
    "amethyst_shard", "copper_ingot", "diamond", "emerald", "gold_ingot", "iron_ingot",
    "lapis_lazuli", "nether_quartz", "netherite_ingot", "redstone", "resin_bricks",
]


@dataclass
class ArmorTrim:
    pattern: ArmorTrimType  # The ID of the trim pattern.
    material: ArmorTrimMaterialType  # The ID of the trim material, which applies a color to the trim.
    show_in_tooltip: bool = True  # Show or hide the trim on this item's tooltip. Defaults to true.

    def to_dict(self) -> dict[str, Any]:
        return {
            "pattern": self.pattern,
            "material": self.material,
            "show_in_tooltip": False if not self.show_in_tooltip else None,  # Defaults to True
        }


Trim = ArmorTrim  # Alias for ArmorTrim

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
    amount: float | int = 1.0
    operation: Literal["add_value", "add_multiplied_base", "add_multiplied_total"] = "add_value"

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.attribute_type,
            "amount": self.amount,
            "operation": self.operation,
            "id": f"attribute_modifier.{self.attribute_type}",
            "slot": self.slot,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AttributeModifier":
        return cls(
            attribute_type=data["type"].removeprefix("minecraft:"),
            slot=data.get("slot", "any"),
            amount=round(data.get("amount", 1), 3),
            operation=data.get("operation", "add_value"),
        )


# ==========================================================================================

ColorType = Literal["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"]
COLORS = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"]


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
    color: ColorType  # The color for this pattern.

    allowed_items: list[str] = field(init=False, repr=False, hash=False, default_factory=lambda: ["banner", "shield"])

    def to_dict(self) -> dict[str, Any]:
        return {
            "pattern": self.pattern,
            "color": self.color,
        }


# ==========================================================================================

@dataclass
class Bee:
    # https://minecraft.wiki/w/Data_component_format#bees
    entity_data: dict[str, Any] = field(default_factory=lambda: {"id": "bee", "CustomName" :'"CustomBee"'})  # The NBT data of the entity in the hive.
    min_ticks_in_hive: int = 60  # The minimum amount of time in ticks for this entity to stay in the hive.
    ticks_in_hive: int = 0  #  The amount of ticks the entity has stayed in the hive.

    allowed_items: list[str] = field(init=False, repr=False, hash=False, default_factory=lambda: ["bee_nest", "bee_hive"])
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_data": self.entity_data,
            "min_ticks_in_hive": self.min_ticks_in_hive,
            "ticks_in_hive": self.ticks_in_hive,
        }


# ==========================================================================================


@dataclass
class TropicalFishData:
    size: Literal["small", "large"] = "large"
    pattern: Literal[0, 1, 2, 3, 4, 5] = 0
    body_color: ColorType | int = "light_blue"
    pattern_color: ColorType | int = "red"

    def __int__(self) -> int:
        body_color_index = COLORS.index(self.body_color) if isinstance(self.body_color, str) else self.body_color
        pattern_color_index = COLORS.index(self.pattern_color) if isinstance(self.pattern_color, str) else self.pattern_color
        size_int = 0 if self.size == "small" else 1
        # rint(f"Shape {size_int}, Pattern {self.pattern}, Base Color {body_color_index}, Pattern Color {pattern_color_index}")
        return (
            pattern_color_index * (2 ** 24) +
            body_color_index    * (2 ** 16) +
            self.pattern        * (2 ** 8) +
            size_int            * (2 ** 0)
        )  # fmt: skip


@dataclass 
class BucketEntityData:
    no_ai: bool = False  # Turns into NoAI entity tag for all bucketable entities.
    silent: bool = False  # Turns into Silent entity tag for all bucketable entities.
    no_gravity: bool = False  # Turns into NoGravity entity tag for all bucketable entities.
    glowing: bool = False  #  Turns into Glowing entity tag for all bucketable entities.
    invulnerable: bool = False  # Turns into Invulnerable entity tag for all bucketable entities.
    health: float | None = None  # Turns into Health entity tag for all bucketable entities.
    age: int | None = None  # Turns into Age entity tag for axolotls and tadpoles.
    variant: int | None = None  # Turns into Variant entity tag for axolotls.
    hunting_cooldown: int | None = None  # Turns into the expiry time of the memory module has_hunting_cooldown for axolotls.
    bucket_variant_tag: "TropicalFishData | int | None" = None  # Turns into Variant entity tag for tropical fish.
    size: Literal["small", "medium", "large"] | None = None  #  Turns into type entity tag for salmon.

    allowed_items: list[str] = field(init=False, repr=False, hash=False, default_factory=lambda: [
        "tropical_fish_bucket", "cod_bucket", "salmon_bucket"
    ])

    def to_dict(self) -> dict[str, Any]:
        return {
            "NoAI": True if self.no_ai else None,
            "Silent": True if self.silent else None,
            "NoGravity": True if self.no_gravity else None,
            "Glowing": True if self.glowing else None,
            "Invulnerable": True if self.invulnerable else None,
            "Health": self.health if self.health is not None else None,
            "Age": self.age if self.age is not None else None,
            "Variant": self.variant if self.variant is not None else None,
            "HuntingCooldown": self.hunting_cooldown if self.hunting_cooldown is not None else None,
            "BucketVariantTag": int(self.bucket_variant_tag) if self.bucket_variant_tag is not None else None,
            "type": self.size if self.size is not None else None,
        }


# ==========================================================================================


@dataclass
class BundleContents:
    """A dict of item to count to fill the bundle with, e.g. {"minecraft:stone": 64}"""
    # https://minecraft.wiki/w/Data_component_format#bundle_contents
    items: dict["str | CustomItem", int] = field(default_factory=dict)

    def to_dict(self, datapack: "Datapack") -> list[dict[str, Any]]:
        from pypacks.resources.custom_item import CustomItem
        from pypacks.utils import extract_item_components
        return [
            {
                "id": item.base_item if isinstance(item, CustomItem) else item,
                "count": count,
            } | ({
                "components": extract_item_components(item, datapack),
            } if isinstance(item, CustomItem) and item.components.to_dict(datapack) else {})
            for item, count in self.items.items()
        ]


# ==========================================================================================

@dataclass
class _Effect:
    """Used internally to format effects for Consumables and DeathProtection"""
    apply_affects: list["PotionEffect"] = field(default_factory=list)
    remove_affects: list["str | PotionEffect"] | Literal["all"] = field(default_factory=list)
    teleport_diameter: float | int = 0
    base_dict_name: str = "on_consume_effects"

    def to_dict(self) -> dict[str, Any]:
        base_dict = ({self.base_dict_name: []})
        if self.apply_affects:
            base_dict[self.base_dict_name].append({"type": "apply_effects", "effects": [effect.to_dict() for effect in self.apply_affects]})
        if self.remove_affects and self.remove_affects != "all":
            base_dict[self.base_dict_name].append({"type": "remove_effects", "effects": [effect.effect_name if isinstance(effect, PotionEffect) else effect for effect in self.remove_affects]})
        if self.remove_affects == "all":
            base_dict[self.base_dict_name].append({"type": "clear_all_effects"})
        if self.teleport_diameter != 0:
            base_dict[self.base_dict_name].append({"type": "teleport_randomly", "diameter": float(self.teleport_diameter)})
        return base_dict


@dataclass
class Consumable:
    # https://minecraft.wiki/w/Data_component_format#consumable

    consume_seconds: float = 1.6  # How long it takes to consume the item in seconds
    animation: Literal["none", "eat", "drink", "block", "bow", "spear", "crossbow", "spyglass", "toot_horn", "brush", "bundle"] = "none"  # The animation to play when consuming the item
    consuming_sound: "str | CustomSound | None" = "entity.generic.eat"  # The sound to play when consuming the item
    has_consume_particles: bool = True  # Whether to show particles when consuming the item

    on_consume_effects: list["PotionEffect"] = field(default_factory=list)  # A list of status effects to apply when consuming the item
    on_consume_remove_effects: list["str | PotionEffect"] | Literal["all"] = field(default_factory=list)  # A list of status effects to remove when consuming the item
    on_consume_teleport_diameter: float | int = 0  # The diameter of the teleportation area when consuming the item (chorus fruit is 16.0)

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        from pypacks.resources.custom_sound import CustomSound
        base_dict = {
            "consume_seconds": self.consume_seconds,
            "animation": self.animation,
            "sound": {"sound_id": self.consuming_sound.get_reference(datapack) if isinstance(self.consuming_sound, CustomSound) else self.consuming_sound} if self.consuming_sound is not None else None,
            "has_consume_particles": False if not self.has_consume_particles else None,  # Defaults to True
        }
        if not self.on_consume_effects and not self.on_consume_remove_effects and self.on_consume_teleport_diameter == 0:
            return base_dict
        effect_dict = _Effect(self.on_consume_effects, self.on_consume_remove_effects, self.on_consume_teleport_diameter).to_dict()
        return base_dict | effect_dict


# ==========================================================================================

CONTAINER_BLOCKS = ["barrel", "chest", "shulker_box", "trapped_chest", "furnace", "blast_furnace", "smoker", "dispenser", "dropper", "enchanting_table", "brewing_stand", "beacon", "anvil", "hopper", "grindstone", "cartography_table", "loom", "stonecutter", "smithing_table", "crafter"]


@dataclass
class ContainerContents:
    # https://minecraft.wiki/w/Data_component_format#container
    items: dict["str | CustomItem", int] = field(default_factory=dict)  # The items in the container

    allowed_items: list[str] = field(init=False, repr=False, hash=False, default_factory=lambda: CONTAINER_BLOCKS)

    def to_dict(self, datapack: "Datapack") -> list[dict[str, Any]]:
        from pypacks.resources.custom_item import CustomItem
        from pypacks.utils import extract_item_components
        return [
            {
                "slot": i,
                "item": {
                    "id": item.base_item if isinstance(item, CustomItem) else item,
                    "count": count,
                } | ({
                    "components": extract_item_components(item, datapack),
                } if isinstance(item, CustomItem) and item.components.to_dict(datapack) else {}),
            }
            for i, (item, count) in enumerate(self.items.items())
        ]


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


@dataclass
class DeathProtection:
    # https://minecraft.wiki/w/Data_component_format#death_protection
    apply_affects: list["PotionEffect"] = field(default_factory=list)  # A list of status effects to apply when the entity dies
    remove_effects: list["str | PotionEffect"] | Literal["all"] = field(default_factory=list)  # A list of status effects to remove when the entity dies
    teleport_diameter: float | int = 0  # The diameter of the teleportation area when the entities dies (chorus fruit is 16.0)

    def to_dict(self) -> dict[str, Any]:
        return _Effect(self.apply_affects, self.remove_effects, self.teleport_diameter, base_dict_name="death_effects").to_dict()



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
    slot: Literal["head", "chest", "legs", "feet", "body", "mainhand", "offhand"] = "mainhand"  # The slot to put the item on
    equip_sound: "str | CustomSound" = "item.armor.equip_generic"  # Sound event to play when the item is equipped
    dispensable: bool = True  #  Whether the item can be dispensed by using a dispenser. Defaults to True.
    swappable: bool = True  # Whether the item can be equipped into the relevant slot by right-clicking.
    damage_on_hurt: bool = True  # Whether this item is damaged when the wearing entity is damaged. Defaults to True.
    entities_which_can_wear: str | list[str] | Literal["all"] = "all"  # The entities which can wear this item. Entity ID/Tag, or list of Entity IDs to limit.
    camera_overlay: str | None = field(repr=False, default=None)  #  The resource location of the overlay texture to use when equipped. The directory this refers to is assets/<namespace>/textures/<id>.

    def to_dict(self) -> dict[str, Any]:
        return {
            "slot": self.slot,
            "equip_sound": self.equip_sound,
            "dispensable": False if not self.dispensable else None,  # Defaults to True
            "swappable": False if not self.swappable else None,  # Defaults to True
            "damage_on_hurt": False if not self.damage_on_hurt else None,  # Defaults to True
            "entities_which_can_wear": self.entities_which_can_wear if self.entities_which_can_wear != "all" else None,  # Defaults to "all"
        } | ({
            "camera_overlay": self.camera_overlay,
        } if self.camera_overlay else {})

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Equippable":
        return cls(
            slot=data.get("slot", "mainhand"),
            equip_sound=data.get("equip_sound", "item.armor.equip_generic"),
            dispensable=data.get("dispensable", True),
            swappable=data.get("swappable", True),
            damage_on_hurt=data.get("damage_on_hurt", True),
            entities_which_can_wear=data.get("entities_which_can_wear", []),
            camera_overlay=data.get("camera_overlay"),
        )


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
    nutrition: int = 0
    saturation: int = 0
    can_always_eat: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "nutrition": self.nutrition,  # Defaults to 0 (cannot be None)
            "saturation": self.saturation,  # Defaults to 0 (cannot be None)
            "can_always_eat": True if self.can_always_eat else None,  # Defaults to False
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
    instrument_range: int = 256  # A non-negative float for the range of the sound (normal horns are 256).

    allowed_items: list[str] = field(init=False, repr=False, hash=False, default_factory=lambda: ["goat_horn"])

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        from pypacks.resources.custom_sound import CustomSound
        assert 0 < self.use_duration <= 60, "use_duration must be a non-negative integer"
        assert 0 < self.instrument_range, "range must be a non-negative integer"
        return {
            "description": self.description,
            "range": self.instrument_range,
            "sound_event": {"sound_id": self.sound_id.get_reference(datapack) if isinstance(self.sound_id, CustomSound) else self.sound_id},
            "use_duration": self.use_duration,
        }


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
    duration_in_ticks: int | Literal["infinity"] = 1  # The duration of the effect in ticks. Value -1 is treated as infinity. Values 0 or less than -2 are treated as 1. Optional, defaults to 1 tick.
    ambient: bool = False  # Whether or not this is an effect provided by a beacon and therefore should be less intrusive on the screen. Optional, defaults to false.
    show_particles: bool = True  # Whether or not this effect produces particles. Optional, defaults to true.
    show_icon: bool = True  # Whether or not an icon should be shown for this effect. Optional, defaults to true.

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.effect_name,
            "amplifier": self.amplifier if self.amplifier != 0 else None,  # Defaults to 0
            "duration": -1 if self.duration_in_ticks == "infinity" else self.duration_in_ticks,
            "ambient": True if self.ambient else None,  # Defaults to False
            "show_particles": False if not self.show_particles else None,  # Defaults to True
            "show_icon": False if not self.show_icon else None,  # Defaults to True
        }


# ==========================================================================================


@dataclass
class PotionContents:
    # https://minecraft.wiki/w/Data_component_format#potion_contents
    custom_color: int  # The overriding color of this potion texture, and/or the particles of the area effect cloud created.
    effects: list[PotionEffect] = field(default_factory=list)  # A list of the additional effects that this item should apply.

    allowed_items: list[str] = field(init=False, repr=False, hash=False, default_factory=lambda: ["potion", "splash_potion", "lingering_potion", "tipped_arrow"])

    def to_dict(self) -> dict[str, Any]:
        return {
            "custom_color": self.custom_color,
            "custom_effects": [effect.to_dict() for effect in self.effects],
        }


# ==========================================================================================


@dataclass
class ToolRule:
    # https://minecraft.wiki/w/Data_component_format#tool
    blocks: str | list[str] | Literal["#mineable/axe", "#mineable/pickaxe", "#mineable/shovel", "#mineable/hoe"]  # The blocks to match with. Can be a block ID or a block tag with a #, or a list of block IDs.
    speed: float = 1.0  # If the blocks match, overrides the default mining speed. Optional.
    correct_for_drops: bool = True  # If the blocks match, overrides whether or not this tool is considered correct to mine at its most efficient speed, and to drop items if the block's loot table requires it. Optional.

    def to_dict(self) -> dict[str, Any]:
        return {
            "blocks": self.blocks,
            "speed": self.speed if self.speed != 1 else None,  # Note: Changed but untested
            "correct_for_drops": self.correct_for_drops,
        }


@dataclass
class Tool:
    # https://minecraft.wiki/w/Data_component_format#tool
    default_mining_speed: float = 1.0  # The default mining speed of this tool, used if no rules override it. Defaults to 1.0.
    damage_per_block: int = 1  # The amount of durability to remove each time a block is broken with this tool. Must be a non-negative integer.
    rules: list[ToolRule] = field(default_factory=list)  # A list of rules for the blocks that this tool has a special behavior with.

    def to_dict(self) -> dict[str, Any]:
        assert self.damage_per_block >= 0, "damage_per_block must be a non-negative integer"
        return {
            "default_mining_speed": self.default_mining_speed,
            "damage_per_block": self.damage_per_block,
            "rules": [rule.to_dict() for rule in self.rules] if self.rules else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Tool":
        return cls(
            default_mining_speed=data.get("default_mining_speed", 1.0),
            damage_per_block=data.get("damage_per_block", 1),
            rules=[ToolRule(**rule) for rule in data.get("rules", [])],
        )


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


PotDecorationsType = Literal[
    "brick", "angler_pottery_sherd", "archer_pottery_sherd", "arms_up_pottery_sherd", "blade_pottery_sherd", "brewer_pottery_sherd",
    "burn_pottery_sherd", "danger_pottery_sherd", "explorer_pottery_sherd", "flow_pottery_sherd", "friend_pottery_sherd",
    "guster_pottery_sherd", "heart_pottery_sherd", "heartbreak_pottery_sherd", "howl_pottery_sherd", "miner_pottery_sherd",
    "mourner_pottery_sherd", "plenty_pottery_sherd", "prize_pottery_sherd", "scrape_pottery_sherd", "sheaf_pottery_sherd",
    "shelter_pottery_sherd", "skull_pottery_sherd", "snort_pottery_sherd",
]

EnchantmentType = Literal[
    "aqua_affinity", "bane_of_arthropods", "binding_curse", "blast_protection", "breach", "channeling",
    "density", "depth_strider", "efficiency", "feather_falling", "fire_aspect", "fire_protection", "flame",
    "fortune", "frost_walker", "impaling", "infinity", "knockback", "looting", "loyalty", "luck_of_the_sea",
    "lure", "mending", "multishot", "piercing", "power", "projectile_protection", "protection", "punch",
    "quick_charge", "respiration", "riptide", "sharpness", "silk_touch", "smite", "soul_speed", "sweeping_edge",
    "swift_sneak", "thorns", "unbreaking", "vanishing_curse", "wind_burst",
]

TOOLS = [
    "wooden_axe", "wooden_hoe", "wooden_pickaxe", "wooden_shovel", "wooden_sword",
    "stone_axe", "stone_hoe", "stone_pickaxe", "stone_shovel", "stone_sword",
    "iron_axe", "iron_hoe", "iron_pickaxe", "iron_shovel", "iron_sword",
    "golden_axe", "golden_hoe", "golden_pickaxe", "golden_shovel", "golden_sword",
    "diamond_axe", "diamond_hoe", "diamond_pickaxe", "diamond_shovel", "diamond_sword",
    "netherite_axe", "netherite_hoe", "netherite_pickaxe", "netherite_shovel", "netherite_sword",
]

# ==========================================================================================

ComponentType: TypeAlias = (
    ArmorTrim | AttributeModifier | BannerPattern | Bee | BucketEntityData | BundleContents | 
    Consumable | ContainerContents | Cooldown |
    DeathProtection | EntityData | Equippable | Firework | FireworkExplosion | Food |
    Instrument | JukeboxPlayable | LodestoneTracker | MapData | PotionContents | Tool | UseRemainder |
    WritableBookContent | WrittenBookContent
)

# ==========================================================================================


@dataclass
class Components:
    durability: int | None = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#max_damage  <-- Tools only
    lost_durability: int | None = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#damage  <-- Tools only
    enchantment_glint_override: bool = field(default=False, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#enchantment_glint_override
    glider: bool = field(default=False, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#glider
    unbreakable: bool = field(default=False, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#unbreakable
    enchantable_at_level: int | None = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#enchantable
    # survives_in_lava: bool = field(default=False, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#damage_resistant & https://minecraft.wiki/w/Tag#Damage_type_tags
    hide_tooltip: bool = field(default=False, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#hide_tooltip
    hide_additional_tooltip: bool = field(default=False, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#hide_additional_tooltip
    repaired_by: list[str] = field(default_factory=list, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#repairable  List of string or #tags
    repair_cost: int | None = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#repair_cost  <-- Tools only?

    block_entity_data: dict[str, Any] = field(default_factory=dict, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#block_entity_data  <-- Block entities only
    block_state: dict[str, Any] = field(default_factory=dict, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#block_state  <-- Blocks only
    container_loot_table: "LootTables | CustomLootTable | str | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#container_loot  <-- Containers only
    custom_head_texture: str | None = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#profile  <-- Player/Mob heads only
    damage_resistant_to: "DamageTagsType | str | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#damage_resistant  <-- Tools only
    enchantments: dict[EnchantmentType, int] = field(default_factory=dict, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#enchantments
    book_enchantments: dict[EnchantmentType, int] = field(default_factory=dict, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#stored_enchantments
    debug_stick_state: dict[str, Any] = field(default_factory=dict, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#debug_stick_state  <-- Debug sticks only
    dye_color: int | None = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#dyed_color  <-- Leather armor only
    intangible_projectile: bool = field(default=False, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#intangible_projectile  <-- Arrows only
    knowledge_book_recipes: list[str] = field(default_factory=list, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#recipes  <-- Knowledge books only
    loaded_projectiles: list[Literal["arrow", "tipped_arrow", "spectral_arrow", "firework_rocket"] | str] | None = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#charged_projectiles  <-- Crossbows only, and only arrows
    note_block_sound: "str | CustomSound | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#note_block_sound  <-- Player heads only
    ominous_bottle_amplifier: Literal[0, 1, 2, 3, 4] | None = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#ominous_bottle_amplifier  <-- Ominous bottles only
    player_head_username: "str | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#profile  <-- Player/Mob heads only
    pot_decorations: list["PotDecorationsType"] = field(default_factory=list, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#pot_decorations  <-- decorative pots only
    shield_base_color: "ColorType | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#base_color  <-- Shields only
    suspicious_stew_effects: dict[PotionEffectType, int] = field(default_factory=dict, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#suspicious_stew_effects  <-- Suspicious stew only
    tooltip_style: str | None = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#tooltip_style

    armor_trim: "ArmorTrim | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#trim  <-- Armor only
    attribute_modifiers: list[AttributeModifier] = field(default_factory=list, kw_only=True)
    bees: list[Bee] = field(default_factory=list, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#bees  <-- Beehives/bee_nest only
    banner_patterns: list[BannerPattern] = field(default_factory=list, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#banner_patterns  <-- Banners only
    bucket_entity_data: "BucketEntityData | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#bucket_entity_data  <-- Bucket of tropical fish only
    bundle_contents: "BundleContents | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#bundle_contents  <-- Bundles only
    cooldown: "Cooldown | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#use_cooldown
    consumable: "Consumable | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#consumable
    container_contents: "ContainerContents | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#container
    death_protection: "DeathProtection | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#death_protection
    entity_data: "EntityData | None" = field(default=None, kw_only=True)
    equippable: "Equippable | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#equippable
    firework_explosion: "FireworkExplosion | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#firework_explosion
    firework: "Firework | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#firework
    food: "Food | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#food
    instrument: "Instrument | None" = field(default=None, kw_only=True)
    jukebox_playable: "JukeboxPlayable | None" = field(default=None, kw_only=True)
    lodestone_tracker: "LodestoneTracker | None" = field(default=None, kw_only=True)
    map_data: "MapData | None" = field(default=None, kw_only=True)
    potion_contents: "PotionContents | None" = field(default=None, kw_only=True)  # https://minecraft.wiki/w/Data_component_format#potion_contents
    tool: "Tool | None" = field(default=None, kw_only=True)
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
        # assert not (self.damage_resistant_to and self.destroyed_in_lava), "Cannot have both damage_resistant_to and destroyed_in_lava set to True"

    @classmethod
    def from_list(cls, components: list[ComponentType]) -> "Components":
        # Convert all the keys from PascalCase to snake_case
        dictionary = {
            ''.join(['_'+c.lower() if c.isupper() else c for c in component.__class__.__name__]).lstrip('_'): component
            for component in components
        }
        return cls(**dictionary)  # type: ignore

    # def internally_validate_component_items(self, item: "CustomItem") -> None:
    #     if self.durability or self.lost_durability or self.repair_cost:
    #         assert item.base_item in TOOLS, "Durability, lost_durability, and repair_cost can only be used on tools!"
    #     if self.loaded_projectiles:
    #         assert item.base_item == "crossbow", "Loaded projectiles can only be used on crossbows!"
    #     if self.note_block_sound:
    #         assert item.base_item == "player_head", "Note block sound can only be used on player heads!"
    #     if self.pot_decorations:
    #         assert item.base_item == "decorated_pot", "Pot decorations can only be used on decorated_pots!"
    #     if self.shield_base_color:
    #         assert item.base_item == "shield", "Shield base color can only be used on shields!"
    #     if self.banner_patterns:
    #         assert item.base_item == "banner", "Banner patterns can only be used on banners!"
    #     if self.bees:
    #         assert item.base_item in ["bee_nest", "beehive"], "Bees can only be used on bee nests and beehives!"
    #     if self.bundle_contents:
    #         assert item.base_item == "bundle", "Bundle contents can only be used on bundles!"
    #     if self.damage_resistant and self.destroyed_in_lava:

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        from pypacks.resources.custom_sound import CustomSound
        from pypacks.resources.custom_loot_tables.custom_loot_table import CustomLootTable
        profile = {"properties": [{"name": "textures", "value": self.custom_head_texture}]} if self.custom_head_texture else None
        return {
            "max_damage":                 self.durability,
            "damage":                     self.lost_durability,
            "enchantment_glint_override": True if self.enchantment_glint_override else None,
            "glider":                     {} if self.glider else None,
            "unbreakable":                {"show_in_tooltip": False} if self.unbreakable else None,
            # "damage_resistant":          {"types": "#minecraft:is_fire"} if not self.destroyed_in_lava else None,
            "enchantable":                {"value": self.enchantable_at_level} if self.enchantable_at_level is not None else None,
            "hide_tooltip":               True if self.hide_tooltip else None,  # Defaults to False
            "hide_additional_tooltip":    True if self.hide_additional_tooltip else None,  # Defaults to False
            "repairable":                 {"items": ", ".join(self.repaired_by)} if self.repaired_by else None,
            "repair_cost":                self.repair_cost,

            "base_color":                 self.shield_base_color,
            "block_entity_data":          self.block_entity_data if self.block_entity_data else None,
            "block_state":                self.block_state if self.block_state else None,
            "container_loot":             ({"loot_table": (self.container_loot_table.get_reference(datapack) if isinstance(self.container_loot_table, CustomLootTable)
                                            else self.container_loot_table)}
                                            if self.container_loot_table is not None else None),  # fmt: skip
            "charged_projectiles":        [{"id": projectile} for projectile in self.loaded_projectiles] if self.loaded_projectiles is not None else None,
            "damage_resistant":           {"types": self.damage_resistant_to} if self.damage_resistant_to is not None else None,
            "debug_stick_state":          self.debug_stick_state if self.debug_stick_state else None,
            "dyed_color":                 self.dye_color,
            "enchantments":               self.enchantments if self.enchantments else None,
            "intangible_projectile":      {} if self.intangible_projectile else None,
            "note_block_sound":           self.note_block_sound.get_reference(datapack) if isinstance(self.note_block_sound, CustomSound) else self.note_block_sound,
            "ominous_bottle_amplifier":   self.ominous_bottle_amplifier,
            "profile":                    self.player_head_username if self.player_head_username else profile,
            "recipes":                   self.knowledge_book_recipes if self.knowledge_book_recipes else None,
            "suspicious_stew_effects":    [{"id": key, "duration": value} for key, value in self.suspicious_stew_effects.items()] if self.suspicious_stew_effects else None,
            "tooltip_style":              self.tooltip_style,

            "trim":                       self.armor_trim.to_dict() if self.armor_trim is not None else None,
            "attribute_modifiers":        {"modifiers": [modifier.to_dict() for modifier in self.attribute_modifiers]} if self.attribute_modifiers else None,
            "banner_patterns":            [pattern.to_dict() for pattern in self.banner_patterns] if self.banner_patterns else None,
            "bees":                       [bee.to_dict() for bee in self.bees] if self.bees else None,
            "bundle_contents":            self.bundle_contents.to_dict(datapack) if self.bundle_contents is not None else None,
            "bucket_entity_data":         self.bucket_entity_data.to_dict() if self.bucket_entity_data is not None else None,
            "consumable":                 self.consumable.to_dict(datapack) if self.consumable is not None else None,
            "container":                  self.container_contents.to_dict(datapack) if self.container_contents is not None else None,
            "death_protection":           self.death_protection.to_dict() if self.death_protection is not None else None,
            "entity_data":                self.entity_data.to_dict() if self.entity_data is not None else None,
            "equippable":                 self.equippable.to_dict() if self.equippable is not None else None,
            "firework_explosion":         self.firework_explosion.to_dict() if self.firework_explosion is not None else None,
            "fireworks":                  self.firework.to_dict() if self.firework is not None else None,
            "food":                       self.food.to_dict() if self.food is not None else None,
            "jukebox_playable":           self.jukebox_playable.to_dict(datapack) if self.jukebox_playable is not None else None,
            "lodestone_tracker":          self.lodestone_tracker.to_dict() if self.lodestone_tracker is not None else None,
            "map_color":                  self.map_data.to_dict()["map_color"] if self.map_data is not None else None,
            "map_id":                     self.map_data.to_dict()["map_id"] if self.map_data is not None else None,
            "map_decorations":            self.map_data.to_dict()["map_decorations"] if self.map_data is not None else None,
            "potion_contents":            self.potion_contents.to_dict() if self.potion_contents is not None else None,
            "pot_decorations":            self.pot_decorations if self.pot_decorations else None,
            "stored_enchantments":        self.book_enchantments if self.book_enchantments else None,
            "tool":                       self.tool.to_dict() if self.tool is not None else None,
            "instrument":                 self.instrument.to_dict(datapack) if self.instrument is not None else None,
            "use_cooldown":               self.cooldown.to_dict() if self.cooldown is not None else None,
            "use_remainder":              self.use_remainder.to_dict(datapack) if self.use_remainder is not None else None,
            "written_book_content":       self.written_book_content.to_dict() if self.written_book_content is not None else None,
            "writable_book_content":      self.writable_book_content.to_dict() if self.writable_book_content is not None else None,
        }  # fmt: skip

# can_break Mehhh
# can_place_on Meh
# lock  # https://minecraft.wiki/w/Data_component_format#lock
