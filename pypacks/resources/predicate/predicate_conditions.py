from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal

from pypacks.utils import recursively_remove_nones_from_data

if TYPE_CHECKING:
    from pypacks.scripts.repos.all_entity_names import MinecraftEntity
    from pypacks.providers.int_provider import IntRange
    from pypacks.resources.custom_damage_type import CustomDamageType
    from pypacks.resources.custom_dimension import CustomDimension
    from pypacks.additions.item_components import PotionEffect
    from pypacks.resources.world_gen.biome import CustomBiome
    from pypacks.resources.world_gen.structure import CustomStructure
    from pypacks.resources.custom_tag import CustomTag

    from pypacks.providers.int_provider import UniformIntProvider
    from pypacks.resources.custom_item import CustomItem
    from pypacks.resources.custom_predicate import Predicate

FluidType = Literal["minecraft:water", "minecraft:flowing_water", "minecraft:lava", "minecraft:flowing_lava"]


# ====================================================================================================================


@dataclass
class DamageTypeTag:
    direct_entity: "EntityCondition | None" = None
    source_entity: "EntityCondition | None" = None
    is_direct: bool = False  #  If true, checks if the damage is direct (i.e. the direct and source entities are the same), if false checks if the damage is not direct. Omitted to not check.
    tags: dict["str | CustomDamageType", str | bool] = field(default_factory=lambda: {"minecraft:is_lightning": True})  # Maps damage type tag to if it's expected or not

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return recursively_remove_nones_from_data({
            "direct_entity": self.direct_entity.to_dict(pack_namespace) if self.direct_entity else None,
            "source_entity": self.source_entity.to_dict(pack_namespace) if self.source_entity else None,
            "is_direct": self.is_direct,
            "tags": [{"id": key.get_reference(pack_namespace) if isinstance(key, CustomDamageType) else key, "expected": value}
                     for key, value in self.tags.items()]
        })


# ====================================================================================================================


@dataclass
class EntityDistance:
    absolute: "float | IntRange | None" = None
    horizontal: "float | IntRange | None" = None
    x: "float | IntRange | None" = None
    y: "float | IntRange | None" = None
    z: "float | IntRange | None" = None

    def to_dict(self) -> dict[str, Any]:
        return recursively_remove_nones_from_data({
            "absolute": self.absolute.to_dict() if isinstance(self.absolute, IntRange) else self.absolute,
            "horizontal": self.horizontal.to_dict() if isinstance(self.horizontal, IntRange) else self.horizontal,
            "x": self.x.to_dict() if isinstance(self.x, IntRange) else self.x,
            "y": self.y.to_dict() if isinstance(self.y, IntRange) else self.y,
            "z": self.z.to_dict() if isinstance(self.z, IntRange) else self.z,
        })


@dataclass
class EntityFlags:
    is_baby: bool | None = None  # Test whether the entity is or is not a baby variant.
    is_on_fire: bool | None = None  # Test whether the entity is or is not on fire.
    is_sneaking: bool | None = None  # Test whether the entity is or is not sneaking.
    is_spinting: bool | None = None  # Test whether the entity is or is not sprinting.
    is_swimming: bool | None = None  # Test whether the entity is or is not swimming.
    is_on_ground: bool | None = None  # Test whether the entity is or is not on the ground.
    is_flying: bool | None = None  # Test whether the entity is or is not flying (with elytra or in creative mode).

    def to_dict(self) -> dict[str, bool]:
        return recursively_remove_nones_from_data({
            "is_baby": self.is_baby,
            "is_on_fire": self.is_on_fire,
            "is_sneaking": self.is_sneaking,
            "is_spinting": self.is_spinting,
            "is_swimming": self.is_swimming,
            "is_on_ground": self.is_on_ground,
            "is_flying": self.is_flying,
        })


@dataclass
class MovementCheck:
    x: "float | IntRange | None" = None  # Test the movement speed along the x-axis in blocks/s.
    y: "float | IntRange | None" = None  # Test the movement speed along the y-axis in blocks/s.
    z: "float | IntRange | None" = None  # Test the movement speed along the z-axis in blocks/s.
    horizontal_speed: "float | IntRange | None" = None  # Test the horizontal movement speed along in blocks/s.
    vertical_speed: "float | IntRange | None" = None  # Test the vertical movement speed along in blocks/s.
    fall_distance: "float | IntRange | None" = None  # Test the fall distance of the entity in blocks.

    def to_dict(self) -> dict[str, Any]:
        return recursively_remove_nones_from_data({
            "x": self.x.to_dict() if isinstance(self.x, IntRange) else self.x,
            "y": self.y.to_dict() if isinstance(self.y, IntRange) else self.y,
            "z": self.z.to_dict() if isinstance(self.z, IntRange) else self.z,
            "horizontal_speed": self.horizontal_speed.to_dict() if isinstance(self.horizontal_speed, IntRange) else self.horizontal_speed,
            "vertical_speed": self.vertical_speed.to_dict() if isinstance(self.vertical_speed, IntRange) else self.vertical_speed,
            "fall_distance": self.fall_distance.to_dict() if isinstance(self.fall_distance, IntRange) else self.fall_distance,
        })


EquipmentSlotType = Literal["mainhand", "offhand", "head", "chest", "legs", "feet", "body"]
SlotType = Literal[
    "armor.body", "armor.chest", "armor.feet", "armor.head", "armor.legs",
    "container.*", "container.0", "container.1", "container.10", "container.11", "container.12", "container.13", "container.14", "container.15", "container.16",
    "container.17", "container.18", "container.19", "container.2", "container.20", "container.21", "container.22", "container.23", "container.24", "container.25",
    "container.26", "container.27", "container.28", "container.29", "container.3", "container.30", "container.31", "container.32", "container.33", "container.34",
    "container.35", "container.36", "container.37", "container.38", "container.39", "container.4", "container.40", "container.41", "container.42", "container.43",
    "container.44", "container.45", "container.46", "container.47", "container.48", "container.49", "container.5", "container.50", "container.51", "container.52",
    "container.53", "container.6", "container.7", "container.8", "container.9",
    "contents", "enderchest.*", "enderchest.0", "enderchest.1", "enderchest.10", "enderchest.11", "enderchest.12", "enderchest.13", "enderchest.14",
    "enderchest.15", "enderchest.16", "enderchest.17", "enderchest.18", "enderchest.19", "enderchest.2", "enderchest.20", "enderchest.21", "enderchest.22",
    "enderchest.23", "enderchest.24", "enderchest.25", "enderchest.26", "enderchest.3", "enderchest.4", "enderchest.5", "enderchest.6", "enderchest.7",
    "enderchest.8", "enderchest.9",
    "horse.*", "horse.0", "horse.1", "horse.10", "horse.11", "horse.12", "horse.13", "horse.14", "horse.2", "horse.3", "horse.4", "horse.5", "horse.6", "horse.7",
    "horse.8", "horse.9", "horse.chest", "horse.saddle", 
    "hotbar.*", "hotbar.0", "hotbar.1", "hotbar.2", "hotbar.3", "hotbar.4", "hotbar.5", "hotbar.6", "hotbar.7", "hotbar.8",
    "inventory.*", "inventory.0", "inventory.1", "inventory.10", "inventory.11", "inventory.12", "inventory.13", "inventory.14", "inventory.15", "inventory.16",
    "inventory.17", "inventory.18", "inventory.19", "inventory.2", "inventory.20", "inventory.21", "inventory.22", "inventory.23", "inventory.24", "inventory.25",
    "inventory.26", "inventory.3", "inventory.4", "inventory.5", "inventory.6", "inventory.7", "inventory.8", "inventory.9",
    "player.crafting.*", "player.crafting.0", "player.crafting.1", "player.crafting.2", "player.crafting.3", "player.cursor",
    "villager.*", "villager.0", "villager.1", "villager.2", "villager.3", "villager.4", "villager.5", "villager.6", "villager.7",
    "weapon", "weapon.*", "weapon.mainhand", "weapon.offhand",
]

@dataclass
class EntityCondition:
    entity_type: "list[MinecraftEntity] | CustomTag" = field(default_factory=list)  # The entity types to test.
    distance: "EntityDistance | None" = None  # To test the distance to the entity this predicate is invoked upon.
    effects: list["PotionEffect | dict[str, Any]"] = field(default_factory=list)  # For testing the active status effects on the entity.
    equipment: dict[EquipmentSlotType, "ItemCondition"] = field(default_factory=dict)  # For testing the items that this entity holds in its equipment slots.
    flags: "EntityFlags | None" = None  # To test flags of the entity.
    location: "LocationTag | None" = None  # Test properties of this entity's location.
    nbt: str | None = None  # Test NBT data of this entity. The outer braces { } of the NBT must be included within this string.
    passenger: "EntityCondition | None" = None  # Test the entity directly riding this entity.
    slots: dict[SlotType, "ItemCondition"] = field(default_factory=dict)  # Test for items in specific inventory slots.
    stepping_on: "LocationTag | None" = None  # Test properties of the block the entity is standing on.
    movement_affected_by: "LocationTag | None" = None  # Test properties of the block 0.5 blocks below the block the entity is standing on.
    team: str | None = None  # Passes if the team of this entity matches this string.
    targeted_entity: "EntityCondition | None" = None  # Test properties of the entity which this entity is targeting for attacks.
    vehicle: "EntityCondition | None" = None  # Test properties of the vehicle entity that this entity is riding upon.
    movement: "MovementCheck | None" = None  # Test the movement of the entity.
    periodic_tick: "int | None" = None  # If present, only succeeds if the age of the entity is divisible by the given number.
    type_specific: dict[str, Any] = field(default_factory=dict)  # To test entity properties that can only be applied to certain entity types.
    # TODO: Type the rest of the entity specific ones?

    def __post_init__(self) -> None:
        from pypacks.additions.item_components import PotionEffect
        for effect in self.effects:
            if isinstance(effect, PotionEffect):
                assert effect.show_icon, "Cannot override the show_icon attribute of the PotionEffect in the EntityCondition, Request from #Skezza"
                assert effect.show_particles, "Cannot override the show_particles attribute of the PotionEffect in the EntityCondition, Request from #Skezza"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        from pypacks.additions.item_components import PotionEffect
        return recursively_remove_nones_from_data({
            "type": self.entity_type if isinstance(self.entity_type, list) else self.entity_type.get_reference(pack_namespace),  # For tags
            "distance": self.distance.to_dict() if self.distance else None,
            "effects": [effect.to_dict() if isinstance(effect, PotionEffect) else effect for effect in self.effects],
            "equipment": {slot: item.to_dict(pack_namespace) for slot, item in self.equipment.items()},
            "flags": self.flags.to_dict() if self.flags else None,
            "location": self.location.to_dict(pack_namespace) if self.location else None,
            "nbt": self.nbt,
            "passenger": self.passenger.to_dict(pack_namespace) if self.passenger else None,
            "slots": {slot: item.to_dict(pack_namespace) for slot, item in self.slots.items()},
            "stepping_on": self.stepping_on.to_dict(pack_namespace) if self.stepping_on else None,
            "movement_affected_by": self.movement_affected_by.to_dict(pack_namespace) if self.movement_affected_by else None,
            "team": self.team,
            "targeted_entity": self.targeted_entity.to_dict(pack_namespace) if self.targeted_entity else None,
            "vehicle": self.vehicle.to_dict(pack_namespace) if self.vehicle else None,
            "movement": self.movement.to_dict() if self.movement else None,
            "periodic_tick": self.periodic_tick,
            "type_specific": self.type_specific,
        })

# [NBT Compound / JSON Object] type_specific: To test entity properties that can only be applied to certain entity types. Supersedes lightning_bolt, player, fishing_hook and catType.
# [String] type: Dictates which type-specific properties to test for.
# The possible values for [String] type and associated extra contents:

# axolotl
# [String] variant: One axolotl variant (an [String] ID) — Valid values are lucy, wild, gold, cyan or blue.
# cat
# [String] variant: Any number of cat variant(s) (an [String] ID, or a [String] tag with #, or an [NBT List / JSON Array] array containing [String] IDs) — Valid values are white, black, red, siamese, british_shorthair, calico, persian, ragdoll, tabby, all_black or jellie.
# fishing_hook: Test properties of the fishing hook that just got reeled in by this entity.
# [Boolean] in_open_water: Whether the fishing hook was in open water.
# fox
# [String] variant: One fox variant (an [String] ID) — Valid values are red or snow.
# frog
# [String] variant: Any number of frog variant(s) (an [String] ID, or a [String] tag with #, or an [NBT List / JSON Array] array containing [String] IDs) — Valid values are cold, temperate or warm.
# horse
# [String] variant: One horse base color (an [String] ID) — Valid values are white, creamy, chestnut, brown, black, gray or dark_brown.
# Testing for a horse's markings is not possible with this sub-predicate.

# lightning: To check information about this lightning bolt; fails when entity is not a lightning bolt.
# [Int][NBT Compound / JSON Object] blocks_set_on_fire: Tests the number of blocks set on fire by this lightning bolt. Use an object with [Int] min and [Int] max to test for a range of values (inclusive).
# [NBT Compound / JSON Object] entity_struck: Test the properties of entities struck by this lightning bolt. Passes if at least one of the struck entities matches the entered conditions.
# All possible conditions for entities[]
# llama
# [String] variant: One llama variant (an [String] ID) — Valid values are creamy, white, brown or gray.
# mooshroom
# [String] variant: One mooshroom variant (an [String] ID) — Valid values are red or brown.
# painting
# [String] variant: Any number of painting variant(s) (an [String] ID, or a [String] tag with #, or an [NBT List / JSON Array] array containing [String] IDs).
# parrot
# [String] variant: One parrot variant (an [String] ID) — Valid values are red_blue, blue, green, yellow_blue or gray.

# player: Tests properties unique to players; fails when this entity is not a player.
# [NBT Compound / JSON Object] looking_at: Test properties of the entity that this player is looking at, as long as it is visible and within a radius of 100 blocks. Visibility is defined through the line from the player's eyes to the entity's eyes, rather than the direction that the player is looking in.
# All possible conditions for entities[]
# [NBT Compound / JSON Object] advancements: To test the player's advancements.
# [Boolean] <advancement id>: Test whether an advancement is granted or not granted. Key is an advancement ID, value is true or false to test for granted/not granted respectively.
# [NBT Compound / JSON Object] <advancement id>: Test whether specific criteria of an advancement are marked as complete.
# [Boolean] <criterion id>: Key is one of the criteria of the advancement, value is true or false to test for completed/not completed respectively.
# [NBT List / JSON Array] gamemode: Test the game modes of this player. Any values in this list will match. Valid values are survival, creative, adventure and spectator.
# [Int][NBT Compound / JSON Object] level: Tests if experience level of this player. Use an object with [Int] min and [Int] max to test for a range of values (inclusive).
# [NBT Compound / JSON Object] recipes: To test if recipes are known or unknown to this player.
# [Boolean] <recipe id>: Key is the recipe ID; value is true or false to test for known/unknown respectively.
# [NBT List / JSON Array] stats: To test this player's statistics.
# [NBT Compound / JSON Object] A statistic to test.
# [String] type: The statistic type. Valid values are minecraft:custom, minecraft:crafted, minecraft:used, minecraft:broken, minecraft:mined, minecraft:killed, minecraft:picked_up, minecraft:dropped and minecraft:killed_by.
# [String] stat: The statistic ID to test.
# [Int][NBT Compound / JSON Object] value: Tests the value of the statistic. Use an object with [Int] min and [Int] max to test for a range of values (inclusive).
# [NBT Compound / JSON Object] input: Test the inputs of this player.
# [Boolean] forward: Tests whether the player is inputting Walk Forward.
# [Boolean] backward: Tests whether the player is inputting Walk Backward.
# [Boolean] left: Tests whether the player is inputting Strafe Left.
# [Boolean] right: Tests whether the player is inputting Strafe Right.
# [Boolean] jump: Tests whether the player is inputting Jump.
# [Boolean] sneak: Tests whether the player is inputting Sneak.
# [Boolean] sprint: Tests whether the player is inputting Sprint.

# rabbit
# [String] variant: One rabbit variant (an [String] ID) — Valid values are brown, white, black, white_splotched, gold, salt or evil.
# raider
# [Boolean] is_captain: Tests whether the raider is a captain.
# [Boolean] has_raid: Tests whether the raider is part of a raid.
# salmon
# [String] variant: One salmon size (an [String] ID) — Valid values are small, medium or large.
# sheep
# [Boolean] sheared: Whether the sheep has been sheared (true) or still has wool (false).
# [String] color: One sheep color (an [String] ID) — Valid values are white, orange, magenta, light_blue, yellow, lime, pink, gray, light_gray, cyan, purple, blue, brown, green, red or black.
# slime
# [Int][NBT Compound / JSON Object] size: Tests the size of this slime or magma cube. Use an object with [Int] min and [Int] max to test for a range of values (inclusive).
# tropical_fish
# [String] variant: One tropical fish variant (an [String] ID) — Valid values are kob, sunstreak, snooper, dasher, brinely, spotty, flopper, stripey, glitter, blockfish, betty or clayfish.
# Testing for a tropical fish's base color or pattern color is not possible with this sub-predicate.

# villager
# [String] variant: One villager variant (biome) (an [String] ID) — Valid values are desert, jungle, plains, savannah, snow, swamp or taiga.
# Testing for a villager's profession or level is not possible with this sub-predicate.

# wolf
# [NBT List / JSON Array][String] variant: Any number of wolf variant(s) (an [String] ID, or a [String] tag with #, or an [NBT List / JSON Array] array containing [String] IDs).


# ====================================================================================================================


@dataclass
class BlockPredicate:
    blocks: "list[str] | CustomTag" = field(default_factory=list)  # The block at the location. Test fails if the location is unloaded.
    nbt: "dict[str, Any] | None" = None  # Tests the block NBT.
    state: "dict[str, Any] | None" = None  # Tests the block state.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "blocks": self.blocks if isinstance(self.blocks, list) else self.blocks.get_reference(pack_namespace),  # For tags
            "nbt": self.nbt,
            "state": self.state,
        }


@dataclass
class FluidPredicate:
    fluids: "list[FluidType] | CustomTag" = field(default_factory=list)  # The block at the location. Test fails if the location is unloaded.
    state: "dict[str, Any] | None" = None  # Fluid property key and value pair. Test will fail if the fluid doesn't have this property.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "fluids": self.fluids.get_reference(pack_namespace) if isinstance(self.fluids, CustomTag) else self.fluids,
            "state": self.state,
        }


@dataclass
class LocationTag:
    biomes: "list[CustomBiome | str] | CustomTag" = field(default_factory=list)  # The biome at this location.
    block: "BlockPredicate | None" = None  # The block at the location. Test fails if the location is unloaded.
    dimension: "str | CustomDimension | None" = None  # The dimension of the location.
    fluids: "FluidPredicate | None" = None  # The fluid at this block.
    light_level: "int | IntRange | None" = None  # The visible light level. Calculated using max(time_adjusted_sky_light, block_light). Use an object with [Int] min and [Int] max keys to test for a range of values (inclusive).
    x_position: "float | IntRange | None" = None  # Tests for the absolute position of this location.
    y_position: "float | IntRange | None" = None  # Tests for the absolute position of this location.
    z_position: "float | IntRange | None" = None  # Tests for the absolute position of this location.
    smokey: bool = False  # When true, success if the block is closely above a campfire or soul campfire. When false, success if not.
    can_see_sky: bool = False  # When true, success if the block has maximum sky_light (i.e. is under clear sky). When false, success if not.
    structures: "list[str | CustomStructure] | CustomTag" = field(default_factory=list)  # The structure the location is currently in.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        from pypacks.providers.int_provider import IntRange
        from pypacks.resources.custom_dimension import CustomDimension
        from pypacks.resources.world_gen.biome import CustomBiome
        from pypacks.resources.world_gen.structure import CustomStructure
        return recursively_remove_nones_from_data({
            "biomes": [
                biome.get_reference(pack_namespace) if isinstance(biome, CustomBiome) else biome for biome in self.biomes
            ] if isinstance(self.biomes, list) else self.biomes.get_reference(pack_namespace),  # For tags
            "block": self.block.to_dict(pack_namespace) if self.block is not None else self.block,
            "dimension": self.dimension.get_reference(pack_namespace) if isinstance(self.dimension, CustomDimension) else self.dimension,
            "fluid": self.fluids.to_dict(pack_namespace) if self.fluids else None,
            "light": self.light_level.to_dict() if isinstance(self.light_level, IntRange) else self.light_level,
            "position": {
                "x": self.x_position.to_dict() if isinstance(self.x_position, IntRange) else self.x_position,
                "y": self.y_position.to_dict() if isinstance(self.y_position, IntRange) else self.y_position,
                "z": self.z_position.to_dict() if isinstance(self.z_position, IntRange) else self.z_position
            },
            "smokey": self.smokey,
            "can_see_sky": self.can_see_sky,
            "structures": [
                structure.get_reference(pack_namespace) if isinstance(structure, CustomStructure) else structure for structure in self.structures
            ] if isinstance(self.structures, list) else self.structures.get_reference(pack_namespace),  # For tags
        })


# ====================================================================================================================


@dataclass
class ItemCondition:
    items: list["str | CustomItem"]  # Tests if the type of item in the item stack matches any of the listed values.
    count: "int | UniformIntProvider | None" = None  # Tests the number of items in this item stack. Use an integer provider for an allowed range
    components: dict[str, Any] = field(default_factory=dict)  # Matches exact item component values. Each key in this object corresponds to a component to test, with its value as the desired data to compare.
    predicates: list["Predicate"] = field(default_factory=list)  # Matches item sub-predicates.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        from pypacks.providers.int_provider import UniformIntProvider
        from pypacks.resources.custom_item import CustomItem
        return recursively_remove_nones_from_data({
            "items": [item.get_reference(pack_namespace) if isinstance(item, CustomItem) else item for item in self.items],
            "count": self.count.to_dict() if isinstance(self.count, UniformIntProvider) else self.count,
            "components": self.components or None,
            "predicates": [predicate.to_dict(pack_namespace) for predicate in self.predicates]
        })


# ====================================================================================================================
