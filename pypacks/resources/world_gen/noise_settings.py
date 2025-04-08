from dataclasses import dataclass, field
from typing import Any

from pypacks.utils import recursively_remove_nones_from_data
from pypacks.resources.base_resource import BaseResource


@dataclass
class CustomNoiseSettings(BaseResource):
    """Noise settings are for generating the shape of the terrain and noise caves, and what blocks the terrain is generated with"""
    # https://minecraft.wiki/w/Noise_settings
    internal_name: str
    sea_level: int = 63  # The sea level in this dimension. Note that this value only affects world generation. The sea level for mob spawning is a fixed value 63.
    disable_mob_generation: bool = False  # Disables creature spawning upon chunk generation.
    ore_veins_enabled: bool = True  # Whether ore veins generate.
    aquifers_enabled: bool = True  # Whether aquifers generate. If set to false, almost all caves below sea level are filled with water.
    legacy_random_source: bool = False  # Whether to use the old random number generator from before 1.18 for world generation.
    default_block: str = "minecraft:stone"  # The default block used for the terrain.
    default_fluid: str = "minecraft:water"  # The default block used for seas and lakes.
    spawn_target: list[dict[str, Any]] = field(default_factory=list)  # (Required, but can be empty) A list of climate parameters to specify the points around which the player tries to spawn. The game selects some horizonal locations that are not more than 2560 blocks away from the origin (0,0), then sample the noise values ("depth" noise and "offset" are always 0), and calculate ((x^2+z^2)^2) / 390625 + (the square of the mininum distance to the ranges in the list). The player spawns near the location where this value is smallest.  # TODO: Type this
    noise_min_y: int = -2032  # The minimum Y coordinate where terrain starts generating. Value between -2032 and 2031 (both inclusive). Must be divisible by 16.
    noise_height: int = 4064  # The total height where terrain generates. Value between 0 and 4064 (both inclusive). Must be divisible by 16. And min_y + height cannot exceed 2032.
    noise_size_horizontal: int = 4  # Value between 0 and 4 (both inclusive)
    noise_size_vertical: int = 4  # Value between 0 and 4 (both inclusive)
    noise_router: dict[str, Any] = field(default_factory=dict)  # The noise router routes density functions to noise parameters used for world generation.
    surface_rule: dict[str, Any] = field(default_factory=dict)  # The main surface rule to place blocks in the terrain.

    # https://minecraft.wiki/w/Noise_router
    # https://minecraft.wiki/w/Surface_rule

    datapack_subdirectory_name: str = field(init=False, repr=False, default="worldgen/noise_settings")

    def __post_init__(self) -> None:
        if self.noise_min_y < -2032 or self.noise_min_y > 2031:
            raise ValueError("noise_min_y must be between -2032 and 2031")
        if self.noise_height < 0 or self.noise_height > 4064:
            raise ValueError("noise_height must be between 0 and 4064")
        if self.noise_size_horizontal < 0 or self.noise_size_horizontal > 4:
            raise ValueError("noise_size_horizontal must be between 0 and 4")
        if self.noise_size_vertical < 0 or self.noise_size_vertical > 4:
            raise ValueError("noise_size_vertical must be between 0 and 4")

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "sea_level": self.sea_level,
            "disable_mob_generation": self.disable_mob_generation,
            "ore_veins_enabled": self.ore_veins_enabled,
            "aquifers_enabled": self.aquifers_enabled,
            "legacy_random_source": self.legacy_random_source,
            "default_block": self.default_block,
            "default_fluid": self.default_fluid,
            "spawn_target": self.spawn_target,
            "noise": {
                "min_y": self.noise_min_y,
                "height": self.noise_height,
                "size_horizontal": self.noise_size_horizontal,
                "size_vertical": self.noise_size_vertical,
            },
            "router": self.noise_router,
            "surface_rule": self.surface_rule,
        })

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "CustomNoiseSettings":  # type: ignore[override]  # TODO: Test if this can have subdirs
        return cls(
            internal_name=internal_name,
            sea_level=data["sea_level"],
            disable_mob_generation=data["disable_mob_generation"],
            ore_veins_enabled=data["ore_veins_enabled"],
            aquifers_enabled=data["aquifers_enabled"],
            legacy_random_source=data["legacy_random_source"],
            default_block=data["default_block"],
            default_fluid=data["default_fluid"],
            spawn_target=data["spawn_target"],
            noise_min_y=data["noise"]["min_y"],
            noise_height=data["noise"]["height"],
            noise_size_horizontal=data["noise"]["size_horizontal"],
            noise_size_vertical=data["noise"]["size_vertical"],
            noise_router=data["router"],
            surface_rule=data["surface_rule"],
        )
