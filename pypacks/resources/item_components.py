from typing import Any, Literal

from dataclasses import dataclass, field

from pypacks.utils import to_snbt

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
            "dispensable": True if self.dispensable else None,
        }


# ==========================================================================================


@dataclass
class Consumable:
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
            "has_consume_particles": True if self.has_consume_particles else None,
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
            "can_always_eat": True if self.can_always_eat else None,
        }


# ==========================================================================================


@dataclass
class UseRemainder:
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
    # https://minecraft.wiki/w/Data_component_format#instrument
    sound_id: Literal["ponder_goat_horn", "sing_goat_horn", "seek_goat_horn", "feel_goat_horn", "admire_goat_horn", "call_goat_horn", "yearn_goat_horn", "dream_goat_horn"]  # https://minecraft.wiki/w/Sounds.json#Sound_events
    use_duration: int = 5  # A non-negative integer for how long the use duration is.
    range: int = 16  #  A non-negative float for the range of the sound.

    def to_dict(self) -> dict[str, Any]:  # TODO: Add range and use_duration
        assert self.use_duration >= 0, "use_duration must be a non-negative integer"
        assert self.range >= 0, "range must be a non-negative integer"
        assert self.use_duration == 5, "use_duration not yet supported"
        assert self.range == 16, "range not yet supported"
        return self.sound_id  # type: ignore
        # TODO: I accidentally deleted this, whoops
        # return {
        #     "sound_event": {
        #         "sound_id": self.sound_id,
        #     },
        #     "use_duration": self.use_duration,
        #     "range": self.range,
        # }


# ==========================================================================================


@dataclass
class WrittenBookContent:
    # https://minecraft.wiki/w/Data_component_format#written_book_content
    title: str
    author: str = "PyPacks"
    pages: list[list[dict[str, str | bool]]] = field(default_factory=lambda: [[{"text": "Hello"}, {"text": "World"}]])  # Should be a list of pages, where a page is a list of objects, e.g. {text: "Hello, world!"}

    def to_dict(self) -> dict[str, Any]:
        # pages_formatted = 
        return {
            "title": self.title,
            "author": self.author,
            # "pages": [to_snbt(page) for page in self.pages],
            "pages": [str(x) for x in self.pages],
        }


# ==========================================================================================


@dataclass
class CustomItemData:
    damage: int | None = None  # NOT WEAPON DAMAGE, LOST DURABILITY, https://minecraft.wiki/w/Data_component_format#damage
    glider: bool = False  # https://minecraft.wiki/w/Data_component_format#glider
    unbreakable: bool = False  # https://minecraft.wiki/w/Data_component_format#unbreakable
    equippable_slots: "Equippable | None" = None  # https://minecraft.wiki/w/Data_component_format#equippable
    consumable: "Consumable | None" = None  # https://minecraft.wiki/w/Data_component_format#consumable
    food: "Food | None" = None  # https://minecraft.wiki/w/Data_component_format#food
    use_remainder: "UseRemainder | None" = None
    jukebox_playable: "JukeboxPlayable | None" = None
    lodestone_tracker: "LodestoneTracker | None" = None
    tool: "Tool | None" = None
    instrument: "Instrument | None" = None
    written_book_content: "WrittenBookContent | None" = None

    def to_dict(self) -> dict[str, Any]:
        # assert self.durability is None or self.durability >= 0, "durability must be a non-negative integer"
        assert self.damage is None or self.damage >= 0, "damage must be a non-negative integer"
        return {
            # "durability":         self.durability if self.durability is not None else None,
            "damage":               self.damage if self.damage is not None else None,
            "glider":               {} if self.glider else None,
            "unbreakable":          {"show_in_tooltip": False} if self.unbreakable else None,
            "equippable":           self.equippable_slots.to_dict() if self.equippable_slots is not None else None,
            "consumable":           self.consumable.to_dict() if self.consumable is not None else None,
            "food":                 self.food.to_dict() if self.food is not None else None,
            "use_remainder":        self.use_remainder.to_dict() if self.use_remainder is not None else None,
            "jukebox_playable":     self.jukebox_playable.to_dict() if self.jukebox_playable is not None else None,
            "lodestone_tracker":    self.lodestone_tracker.to_dict() if self.lodestone_tracker is not None else None,
            "tool":                 self.tool.to_dict() if self.tool is not None else None,
            "instrument":           self.instrument.to_dict() if self.instrument is not None else None,
            "written_book_content": self.written_book_content.to_dict() if self.written_book_content is not None else None,
        }  # fmt: skip

# attribute_modifiers PROBABLY
# banner_patterns
# base_color # MEH
# bees MEH
# block_entity_data MEH
# block_state MEH
# bucket_entity_data MEH
# bundle_contents Mehh
# can_break Mehhh
# can_place_on Meh
# charged_projectiles HMMM
# consumable More work for effects and sound.
# container MEH
# container_loot MEH (for chests)
# damage_resistant Hmmm
# debug_stick_state no.
# death_protection HMMMM (totem of undying)
# dyed_color MEH
# enchantable # MAYBE?
# enchantment_glint_override MEH
# enchantments
# entity_data MEH
# equippable REDO, more stuff
# firework_explosion MEH
# fireworks MEH
# hide_additional_tooltip
# hide_tooltip PROBABLY
# intangible_projectile MEH
# note_block_sound
# ominous_bottle_amplifier
# potion_contents
# profile (for heads)
# recipes
# repairable
# repair_cost
# stored_enchantments MEH
# suspicious_stew_effects MEH
# tooltip_style maybe?
# trim MEH
# use_cooldown
# writable_book_content MEH
