import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from pypacks.pack import Pack


@dataclass
class CustomDimension:
    internal_name: str
    dimension_type: "CustomDimensionType | Literal['overworld', 'the_nether', 'the_end', 'overworld_caves']"
    biome: str = "minecraft:the_end"  # The biome of the dimension.
    noise_settings: Literal[
        "minecraft:overworld", "minecraft:nether", "minecraft:end", "minecraft:large_biomes", "minecraft:amplified", "minecraft:floating_islands", "minecraft:caves"
    ] = "minecraft:overworld"  # The noise settings of the dimension.


    datapack_subdirectory_name: str = field(init=False, repr=False, default="dimension")

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": self.dimension_type.get_reference(pack_namespace) if isinstance(self.dimension_type, CustomDimensionType) else self.dimension_type,
            # TODO: More inputs here
            "generator": {
                "type": "minecraft:noise",
                "biome_source": {
                    "type": "minecraft:fixed",
                    "biome": self.biome,
                },
                "settings": self.noise_settings,
            }
        }

    def create_datapack_files(self, pack: "Pack") -> None:
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)
        if isinstance(self.dimension_type, CustomDimensionType):
            self.dimension_type.create_datapack_files(pack)



@dataclass
class CustomDimensionType:
    """Defines properties of a dimension such as world height build limits, the ambient light, and more."""
    internal_name: str
    height: int = 384  # The total height in which blocks can exist within this dimension. Must be between 16 and 4064 and be a multiple of 16. The maximum building height = min_y + height - 1, which cannot be greater than 2031.
    logical_height: int = 384  # The maximum height to which chorus fruits and nether portals can bring players within this dimension. This excludes portals that were already built above the limit as they still connect normally. Cannot be greater than `height`.
    minimum_y: int = -64  #  The minimum height in which blocks can exist within this dimension. Must be between -2032 and 2031 and be a multiple of 16 (effectively making 2016 the maximum).
    coordinate_scale: float = 1.0  # The multiplier applied to coordinates when leaving the dimension. Value between 0.00001 and 30000000.0 (both inclusive)。
    ambient_light: float = 0.0  # How much light the dimension has. When set to 0, it completely follows the light level; when set to 1, there is no ambient lighting. 

    monster_spawn_light_level: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] = 7  #  Maximum light required when the monster spawns. The formula of this light is: max(sky light - 10, block light) during thunderstorms, and max(internal sky light, block light) during other weather.
    monster_spawn_block_light_limit: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] = 0  # Maximum block light required when the monster spawns.
    ultrawarm: bool = False  # Whether the dimensions behaves like the nether (water evaporates and sponges dry) or not. Also lets stalactites drip lava and causes lava to spread faster and thinner.
    natural: bool = True  #  When false, compasses spin randomly, and using a bed to set the respawn point or sleep, is disabled. When true, nether portals can spawn zombified piglins, and creaking hearts can spawn creakings.
    has_skylight: bool = True  # Whether the dimension has skylight or not.
    has_ceiling: bool = False  # Whether the dimension has a bedrock ceiling. Note that this is only a logical ceiling. It is unrelated with whether the dimension really has a block ceiling.
    piglin_safe: bool = False  # When false, Piglins and hoglins shake and transform to zombified entities.
    bed_works: bool = True  # When false, the bed blows up when trying to sleep, when true, works like normal.
    respawn_anchor_works: bool = False  # When false, the respawn anchor blows up when trying to set spawn point.
    has_raids: bool = True  # Whether players with the Bad Omen effect can cause a raid.
    infiniburn: str = "#minecraft:infiniburn_overworld"  # Takes a block tag where all these blocks burn forever.
    effects: Literal["minecraft:overworld", "minecraft:the_nether", "minecraft:the_end"] = "minecraft:overworld"  # Determines the dimension effect used for this dimension. Setting to overworld makes the dimension have clouds, sun, stars and moon. Setting to the nether makes the dimension have thick fog blocking that sight, similar to the nether. Setting to the end makes the dimension have dark spotted sky similar to the end, ignoring the sky and fog color.

    datapack_subdirectory_name: str = field(init=False, repr=False, default="dimension_type")

    def get_reference(self, pack_namespace: str) -> str:
        return f"{pack_namespace}:{self.internal_name}"


    def __post_init__(self) -> None:
        assert 16 <= self.height <= 4064, f"Height must be between 16 and 4064, recieved {self.height}"
        assert self.height % 16 == 0, f"Height must be a multiple of 16, recieved {self.height}"
        assert self.logical_height <= self.height, f"Logical height must be less than or equal to height, recieved {self.logical_height} and {self.height}"
        assert -2032 <= self.minimum_y <= 2031, f"Minimum y must be between -2032 and 2031, recieved {self.minimum_y}"
        assert 0.00001 <= self.coordinate_scale <= 30000000.0, f"Coordinate scale must be between 0.00001 and 30000000.0, recieved {self.coordinate_scale}"
        assert 0.0 <= self.ambient_light <= 1.0, f"Ambient light must be between 0.0 and 1.0, recieved {self.ambient_light}"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "ultrawarm": self.ultrawarm,
            "natural": self.natural,
            "coordinate_scale": self.coordinate_scale,
            "has_skylight": self.has_skylight,
            "has_ceiling": self.has_ceiling,
            "ambient_light": self.ambient_light,
            "monster_spawn_light_level": self.monster_spawn_light_level,
            "monster_spawn_block_light_limit": self.monster_spawn_block_light_limit,
            "piglin_safe": self.piglin_safe,
            "bed_works": self.bed_works,
            "respawn_anchor_works": self.respawn_anchor_works,
            "has_raids": self.has_raids,
            "logical_height": self.logical_height,
            "min_y": self.minimum_y,
            "height": self.height,
            "infiniburn": self.infiniburn,
            "effects": self.effects
        }

    def create_datapack_files(self, pack: "Pack") -> None:
        # If created via the CustomDimension, the subdir might not exist
        os.makedirs(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name, exist_ok=True)

        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)


# ============================================================================================================
# PRESETS:

OverworldDimension = CustomDimensionType(
    "overworld",
    height=384,
    logical_height=384,
    minimum_y=-64,
    coordinate_scale=1.0,
    ambient_light=0.0,
    monster_spawn_light_level=7,
    monster_spawn_block_light_limit=0,
    ultrawarm=False,
    natural=True,
    has_skylight=True,
    has_ceiling=False,
    piglin_safe=False,
    bed_works=True,
    respawn_anchor_works=False,
    has_raids=True,
    infiniburn="#minecraft:infiniburn_overworld",
    effects="minecraft:overworld"
)

NetherDimension = CustomDimensionType(
    "the_nether",
    height=128,
    logical_height=128,
    minimum_y=0,
    coordinate_scale=8.0,
    ambient_light=0.1,
    monster_spawn_light_level=7,
    monster_spawn_block_light_limit=15,
    ultrawarm=True,
    natural=False,
    has_skylight=False,
    has_ceiling=True,
    piglin_safe=True,
    bed_works=False,
    respawn_anchor_works=True,
    has_raids=False,
    infiniburn="#minecraft:infiniburn_nether",
    effects="minecraft:the_nether"
)

EndDimension = CustomDimensionType(
    "the_end",
    height=256,
    logical_height=256,
    minimum_y=0,
    coordinate_scale=1.0,
    ambient_light=0.0,
    monster_spawn_light_level=7,
    monster_spawn_block_light_limit=0,
    ultrawarm=False,
    natural=False,
    has_skylight=False,
    has_ceiling=False,
    piglin_safe=False,
    bed_works=False,
    respawn_anchor_works=False,
    has_raids=True,
    infiniburn="#minecraft:infiniburn_end",
    effects="minecraft:the_end"
)

# ============================================================================================================


@dataclass
class MoodSound:
    sound: str = "minecraft:ambient.cave"  # The sound event to play.
    tick_delay: int = 6000  # The mininum delay between two plays
    block_search_extent: int = 8  #  Determines the cubic range of possible positions to find place to play the mood sound. The player is at the center of the cubic range, and the edge length is 2 * block_search_extent.
    offset: int = 2  #  The higher the value makes the sound source further away from the player.

    def to_dict(self) -> dict[str, Any]:
        return {
            "sound": self.sound,
            "tick_delay": self.tick_delay,
            "block_search_extent": self.block_search_extent,
            "offset": self.offset
        }


# @dataclass
# class CustomBiome:
#     has_precipitation: bool = True  # Determines whether or not the biome has precipitation (rain and snow)
#     temperature: float = 0.8  #  Controls gameplay features like grass and foliage color, and a height adjusted temperature (which controls whether raining or snowing if `has_precipitation` is true, and generation details of some features).
#     temperature_modifier: Literal["none", "frozen"] = "none"
#     downfall: float = 0.4  # Controls grass and foliage color.
#     fog_color: int = 12638463  # Decimal value converted from Hex color to use for fog.
#     sky_color: int = 7907327  # Decimal value converted from Hex color to use for sky.
#     water_color: int = 4159204  # Decimal value converted from Hex color to use for water blocks and cauldrons.
#     water_fog_color: int = 329011  # Decimal value converted from Hex color to use for fog underwater.
#     foliage_color: int | None = None  # Decimal value converted from Hex color to use for tree leaves and vines. If not present, the value depends on downfall and the temperature.
#     grass_color: int | None = None  # Decimal value converted from Hex color to use for grass blocks, short grass, tall grass, ferns, tall ferns, and sugar cane. If not present, the value depends on downfall and temperature.
#     grass_color_modifier: Literal["none", "dark_forest", "swamp"] | None = None
#     mood_sound: MoodSound | None = field(default_factory=lambda: MoodSound("minecraft:ambient.cave", 6000, 8, 2))  #  Settings for mood sound.

#     datapack_subdirectory_name: str = field(init=False, repr=False, default="worldgen/biome")
