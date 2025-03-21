from dataclasses import dataclass, field
from typing import Any

from pypacks.resources.base_resource import BaseResource
from pypacks.utils import recursively_remove_nones_from_data


@dataclass
class CustomNoise(BaseResource):
    """A noise is a technical JSON file that can be referenced by a density function and surface rule.

    Amplitudes is a list of floats of sub-noise. The frequency of a sub-noise at index (from 0) in the list is 2^(- firstOctave + index),
    and the amplitude (the value of the sub-noise ranges from -amplitude to +amplitude) of this sub-noise is about
    1.04 * doubleValueAtIndex * 2^(sizeOfThisList - index - 1) / (2^sizeOfThisList - 1) (assuming the range of 3D Improved Perlin Noise is ±1.04).
    For each sub-noise, two 3D improved perlin noises are created and their average is taken.
    The final range of this noise value is ± 10 * sumOfSubNoises / ( 3 * ( 1 + 1 / m ) ),
    where m is the number of elements in the list after removing the leading and trailing zero elements"""
    # https://minecraft.wiki/w/Noise
    internal_name: str
    first_octave: int = 1  # First octave
    amplitudes: list[float] = field(default_factory=lambda: [1.0])

    datapack_subdirectory_name: str = field(init=False, repr=False, default="worldgen/noise")

    def to_dict(self) -> dict[str, Any]:
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "firstOctave": self.first_octave,
            "amplitudes": self.amplitudes,
        })

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "CustomNoise":
        return cls(
            internal_name,
            first_octave=data["firstOctave"],
            amplitudes=data["amplitudes"],
        )
