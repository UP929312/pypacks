from dataclasses import dataclass, field
import json
import os
from pathlib import Path
from typing import Any, Literal, TYPE_CHECKING

from pypacks.utils import recursively_remove_nones_from_data
from pypacks.resources.world_gen.entity_spawner import SpawnOverride

if TYPE_CHECKING:
    from pypacks.pack import Pack


@dataclass
class CustomBiome:
    # https://minecraft.wiki/w/Biome_definition
    internal_name: str
    has_precipitation: bool = True  # Determines whether or not the biome has precipitation (rain and snow)
    temperature: float = 0.8  # Controls gameplay features like grass and foliage color, and a height adjusted temperature (which controls whether raining or snowing if `has_precipitation` is true, and generation details of some features).
    temperature_modifier: Literal["none", "frozen"] = "none"
    downfall: float = 0.4  # Controls grass and foliage color.
    fog_color: int = 12638463  # Decimal value converted from Hex color to use for fog.
    sky_color: int = 7907327  # Decimal value converted from Hex color to use for sky.
    water_color: int = 4159204  # Decimal value converted from Hex color to use for water blocks and cauldrons.
    water_fog_color: int = 329011  # Decimal value converted from Hex color to use for fog underwater.
    foliage_color: int | None = None  # Decimal value converted from Hex color to use for tree leaves and vines. If not present, the value depends on downfall and the temperature.
    grass_color: int | None = None  # Decimal value converted from Hex color to use for grass blocks, short grass, tall grass, ferns, tall ferns, and sugar cane. If not present, the value depends on downfall and temperature.
    grass_color_modifier: Literal["none", "dark_forest", "swamp"] = "none"
    mood_sound: "MoodSound | None" = field(default_factory=lambda: MoodSound("minecraft:ambient.cave", 6000, 8, 2))  # Settings for mood sound.
    features: "FeatureGenerationSteps" = field(default_factory=lambda: FeatureGenerationSteps())
    creature_spawn_probability: float | None = None  # Higher value results in more creatures spawned in world generation. Must be between 0.0 and 0.9999999 (inclusive)
    spawners: list[SpawnOverride] = field(default_factory=list)

    datapack_subdirectory_name: str = field(init=False, repr=False, default="worldgen/biome")

    def __post_init__(self) -> None:
        assert self.creature_spawn_probability is None or (0.0 <= self.creature_spawn_probability <= 0.9999999), "creature_spawn_probability must be between 0.0 and 0.9999999 (inclusive)"
        assert self.features == FeatureGenerationSteps(), "Feature generation steps are not yet supported."

    def get_reference(self, pack_namespace: str) -> str:
        return f"{pack_namespace}:{self.internal_name}"

    def to_dict(self) -> dict[str, Any]:
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "has_precipitation": self.has_precipitation,
            "temperature": self.temperature,
            "temperature_modifier": self.temperature_modifier if self.temperature_modifier != "none" else None,
            "downfall": self.downfall,
            "effects": {
                "fog_color": self.fog_color,
                "sky_color": self.sky_color,
                "water_color": self.water_color,
                "water_fog_color": self.water_fog_color,
                "foliage_color": self.foliage_color,
                "grass_color": self.grass_color,
                "grass_color_modifier": self.grass_color_modifier if self.grass_color_modifier != "none" else None,
                "mood_sound": self.mood_sound.to_dict() if self.mood_sound else None
            },
            "carvers": [],
            **self.features.to_dict(),
            "creature_spawn_probability": self.creature_spawn_probability,
            "spawn_costs": {},  # TODO: Add me
            "spawners": SpawnOverride.combine_spawn_overrides(self.spawners),  # type: ignore[arg-type]
        })

    def create_datapack_files(self, pack: "Pack") -> None:
        # We need to create the subdir if this is being created as part of a custom dimension:
        os.makedirs(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name, exist_ok=True)
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(), file, indent=4)


class PlacedFeature:  # TODO: Type me
    pass


@dataclass
class FeatureGenerationSteps:
    raw_generation: list[str | PlacedFeature] = field(default_factory=list)  # Used by small end island features.
    lakes: list[str | PlacedFeature] = field(default_factory=list)  # Used by lava lakes
    local_modifications: list[str | PlacedFeature] = field(default_factory=list)  # Used for amethyst geodes and icebergs
    underground_structures: list[str | PlacedFeature] = field(default_factory=list)  # Used for dungeons and overworld fossils
    surface_structures: list[str | PlacedFeature] = field(default_factory=list)  # Used for desert wells and blue ice patches
    strongholds: list[str | PlacedFeature] = field(default_factory=list)  # Not currently used in vanilla
    underground_ores: list[str | PlacedFeature] = field(default_factory=list)  # Used for overworld ore blobs, overworld dirt/gravel/stone variant blobs, and sand/gravel/clay disks
    underground_decoration: list[str | PlacedFeature] = field(default_factory=list)  # Used for infested block blobs, nether gravel and blackstone blobs, and all nether ore blobs
    fluid_springs: list[str | PlacedFeature] = field(default_factory=list)  # Used for water and lava springs
    vegetal_decoration: list[str | PlacedFeature] = field(default_factory=list)  # Used for trees, bamboo, cacti, kelp, and other ground and ocean vegetation
    top_layer_modifications: list[str | PlacedFeature] = field(default_factory=list)  # Used for surface freezing

    def to_dict(self) -> dict[str, Any]:
        return {
            "features": [
                self.raw_generation,
                self.lakes,
                self.local_modifications,
                self.underground_structures,
                self.surface_structures,
                self.strongholds,
                self.underground_ores,
                self.underground_decoration,
                self.fluid_springs,
                self.vegetal_decoration,
                self.top_layer_modifications
            ]
        }


@dataclass
class MoodSound:
    sound: str = "minecraft:ambient.cave"  # The sound event to play.
    tick_delay: int = 6000  # The mininum delay between two plays
    block_search_extent: int = 8  # Determines the cubic range of possible positions to find place to play the mood sound. The player is at the center of the cubic range, and the edge length is 2 * block_search_extent.
    offset: int = 2  # The higher the value makes the sound source further away from the player.

    def to_dict(self) -> dict[str, Any]:
        return {
            "sound": self.sound,
            "tick_delay": self.tick_delay,
            "block_search_extent": self.block_search_extent,
            "offset": self.offset
        }
