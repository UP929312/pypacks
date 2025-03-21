from dataclasses import dataclass, field
from typing import Any, Literal, TYPE_CHECKING

from pypacks.utils import recursively_remove_nones_from_data
from pypacks.resources.base_resource import BaseResource

if TYPE_CHECKING:
    from pypacks.resources.world_gen.structure import CustomStructure
    from pypacks.pack import Pack


@dataclass
class CustomStructureSet(BaseResource):
    """A structure set is used to determine the position of structures in the world during world generation.
    Structure sets are not referenced in a dimension or biome.
    Instead, the existence of the resource is enough to make the structures generate.
    The valid biomes of a structure are determined by the structure itself."""
    # https://minecraft.wiki/w/Structure_set
    internal_name: str
    structures: dict["CustomStructure | str", float] = field(default_factory=dict)
    placement_salt: int = 1  # A number that assists in randomization; see salt (cryptography, https://en.wikipedia.org/wiki/salt_(cryptography)). Must be a non-negative integer.
    placement_frequency: float = 1.0  # Probability to try to generate if other conditions below are met. Values between 0.0 to 1.0 (inclusive). Setting it to a number does not mean one structure is generated this often, only that the game attempts to generate one; biomes or terrain could lead to the structure not being generated.
    placement_frequency_reduction_method: Literal["default", "legacy_type_1", "legacy_type_2", "legacy_type_3"] = "default"  # Provides a random number generator algorithm for frequency. One of default (the random number depends on the seed, position and salt), legacy_type_1 (the random number depends only on the seed and position, and randomness only occurs when the locations differ greatly), legacy_type_2 (same as default, but with fixed salt: 10387320) and legacy_type_3 (the random number depends only on seed and position).
    exclusion_zone: dict["CustomStructure | str", int] = field(default_factory=dict)  # Specifies that it cannot be placed near a certain structures. Key (Structure) to Value (chunk_count (a value between 1 and 16))
    locate_offset: tuple[int, int, int] = field(default_factory=lambda: (0, 0, 0))  # The chunk coordinate offset given when using /locate structure. X, Y, Z: Value between -16 and 16.
    placement_type: "RandomSpreadPlacementType | ConcentricRingsPlacementType" = field(default_factory=lambda: RandomSpreadPlacementType())

    datapack_subdirectory_name: str = field(init=False, repr=False, default="worldgen/structure_set")

    def __post_init__(self) -> None:
        if self.placement_salt < 0:
            raise ValueError("placement_salt must be a non-negative integer")
        if self.placement_frequency is not None and (self.placement_frequency < 0.0 or self.placement_frequency > 1.0):
            raise ValueError("placement_frequency must be between 0.0 and 1.0")
        if self.locate_offset is not None and (self.locate_offset[0] < -16 or self.locate_offset[0] > 16):
            raise ValueError("locate_offset[0] must be between -16 and 16")
        if self.locate_offset is not None and (self.locate_offset[1] < -16 or self.locate_offset[1] > 16):
            raise ValueError("locate_offset[1] must be between -16 and 16")
        if self.locate_offset is not None and (self.locate_offset[2] < -16 or self.locate_offset[2] > 16):
            raise ValueError("locate_offset[2] must be between -16 and 16")

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        from pypacks.resources.world_gen.structure import CustomStructure
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "structures": [
                {"structure": structure.get_reference(pack_namespace) if isinstance(structure, CustomStructure) else structure, "weight": weight}
                for structure, weight in self.structures.items()
            ],
            "placement": {
                "salt": self.placement_salt,
                "frequency": self.placement_frequency if self.placement_frequency != 1.0 else None,
                "frequency_reduction_method": self.placement_frequency_reduction_method if self.placement_frequency_reduction_method != "default" else None,
                "exclusion_zone": ({
                    "other_set": list(self.exclusion_zone.keys())[0],
                    "chunk_count": list(self.exclusion_zone.values())[0]
                } if self.exclusion_zone else None),
                "locate_offset": ({
                    "X": self.locate_offset[0],
                    "Y": self.locate_offset[1],
                    "Z": self.locate_offset[2]
                } if self.locate_offset != (0, 0, 0) else None),
                **self.placement_type.to_dict(),
            }
        })

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "CustomStructureSet":
        return cls(
            internal_name,
            {structure["structure"]: structure["weight"] for structure in data["structures"]},
            data["placement"]["salt"],
            data["placement"].get("frequency", 1.0),
            data["placement"].get("frequency_reduction_method", "default"),
            {data["placement"]["exclusion_zone"]["other_set"]: data["placement"]["exclusion_zone"]["chunk_count"]} if data["placement"].get("exclusion_zone") else {},
            (data["placement"]["locate_offset"]["X"], data["placement"]["locate_offset"]["Y"], data["placement"]["locate_offset"]["Z"]) if data["placement"].get("locate_offset") else (0, 0, 0),
            [RandomSpreadPlacementType, ConcentricRingsPlacementType]["spread_type" in data["placement"]].from_dict(data["placement"])
        )

    def create_datapack_files(self, pack: "Pack") -> None:
        from pypacks.resources.world_gen.structure import CustomStructure
        super().create_datapack_files(pack)
        for structure in self.structures:
            if isinstance(structure, CustomStructure):
                structure.create_datapack_files(pack)


@dataclass
class RandomSpreadPlacementType:
    """Structures are spread evenly in the entire world. In vanilla, this placement type is used for most structures (like bastion remnants or swamp huts).
    The world is split into squares with side length of  spacing chunks. One structure is placed in a random position within each square.
    A structure can't be placed in  separation chunks along the positive X/Z edge of a square. """
    spread_type: Literal["linear", "triangular"] = "linear"  # One of linear or triangular.
    spacing: int = 1  # Average distance between two neighboring generation attempts. Value between 0 and 4096 (inclusive).
    separation: int = 0  # Minimum distance (in chunks) between two neighboring attempts. Value between 0 and 4096 (inclusive). Has to be strictly smaller than spacing. The maximum distance of two neighboring generation attempts is 2*spacing - separation.

    def __post_init__(self) -> None:
        if self.separation > self.spacing:
            raise ValueError("separation must be strictly smaller than spacing")
        if self.spacing < 1 or self.spacing > 4096:
            raise ValueError("spacing must be between 1 and 4096")
        if self.separation < 0 or self.separation > 4096:
            raise ValueError("seperation must be between 0 and 4096")

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:random_spread",
            "spread_type": self.spread_type if self.spread_type != "linear" else None,
            "spacing": self.spacing,
            "separation": self.separation
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RandomSpreadPlacementType":
        return cls(
            data.get("spread_type", "linear"),
            data["spacing"],
            data["separation"]
        )


@dataclass
class ConcentricRingsPlacementType:
    """A fixed number of structures is placed in concentric rings around the origin of the world. In vanilla, this placement is only used for strongholds."""
    distance: int = 0  # The thickness of a ring plus that of a gap between two rings. Value between 0 and 1023 (inclusive). Unit is 6 chunks
    count: int = 0  # The total number of generation attempts in this dimension. Value between 1 and 4095 (inclusive).
    preferred_biomes: list[str] | str = field(default_factory=list)  # (an ID, a #tag, or an array containing IDs) - Biomes in which the structure is likely to be generated.
    spread: int = 0  # How many attempts are on the closest ring to spawn. Value between 0 and 1023 (inclusive). The number of attempts on the Nth ring is: spread * (N^2 + 3 * N + 2) / 6, until the number of attempts reaches the total count.

    def __post_init__(self) -> None:
        if self.distance < 0 or self.distance > 1023:
            raise ValueError("distance must be between 0 and 1023")
        if self.count < 1 or self.count > 4095:
            raise ValueError("count must be between 1 and 4095")
        if self.spread < 0 or self.spread > 1023:
            raise ValueError("spread must be between 0 and 1023")

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:concentric_rings",
            "distance": self.distance,
            "count": self.count,
            "preferred_biomes": self.preferred_biomes,
            "spread": self.spread
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConcentricRingsPlacementType":
        return cls(
            data["distance"],
            data["count"],
            data.get("preferred_biomes", []),
            data["spread"]
        )
