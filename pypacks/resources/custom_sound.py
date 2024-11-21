from typing import TYPE_CHECKING, Any
from dataclasses import dataclass

if TYPE_CHECKING:
    from pypacks.datapack import Datapack


@dataclass
class CustomSound:
    internal_name: str
    ogg_path: str
    volume: float = 1.0
    pitch: float = 1.0

    def __post_init__(self) -> None:
        assert 0 <= self.volume <= 1, "Volume must be between 0 and 1"
        assert 0.5 <= self.pitch <= 2, "Pitch must be between 0.5 and 2"
    
    def create_sound_entry(self, datapack: "Datapack") -> dict[str, list[dict[str, Any]]]:
        return {
            "sounds": [
                {
                    "name": f"{datapack.namespace}:{self.internal_name}",
                    "volume": self.volume,
                    "pitch": self.pitch,
                    # "stream": True,
                }
            ]
        }
