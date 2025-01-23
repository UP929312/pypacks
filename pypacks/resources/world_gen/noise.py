from dataclasses import dataclass, field
import json
import os
from pathlib import Path
from typing import Any, TYPE_CHECKING

from pypacks.utils import recursively_remove_nones_from_data

if TYPE_CHECKING:
    from pypacks.pack import Pack


@dataclass
class CustomNoise:
    """A noise is a technical JSON file that can be referenced by a density function and surface rule.

    Amplitudes is a list of floats of sub-noise. The frequency of a sub-noise at index (from 0) in the list is 2^(- firstOctave + index),
    and the amplitude (the value of the sub-noise ranges from -amplitude to +amplitude) of this sub-noise is about
    1.04 * doubleValueAtIndex * 2^(sizeOfThisList - index - 1) / (2^sizeOfThisList - 1) (assuming the range of 3D Improved Perlin Noise is ±1.04).
    For each sub-noise, two 3D improved perlin noises are created and their average is taken.
    The final range of this noise value is ± 10 * sumOfSubNoises / ( 3 * ( 1 + 1 / m ) ),
    where m is the number of elements in the list after removing the leading and trailing zero elements"""
    # https://minecraft.wiki/w/Noise
    internal_name: str
    first_octave: int = 1  #  First octave
    amplitudes: list[float] = field(default_factory=lambda: [1.0])

    datapack_subdirectory_name: str = field(init=False, repr=False, default="worldgen/noise")

    def get_reference(self, pack_namespace: str) -> str:
        return f"{pack_namespace}:{self.internal_name}"

    def to_dict(self) -> dict[str, Any]:
        return recursively_remove_nones_from_data({
           "firstOctave": self.first_octave,
            "amplitudes": self.amplitudes,
        })

    def create_datapack_files(self, pack: "Pack") -> None:
        # We need to create the subdir if this is being created as part of a custom dimension:
        os.makedirs(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name, exist_ok=True)
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(), file, indent=4)
