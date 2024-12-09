import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Any
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from pypacks.datapack import Datapack


@dataclass
class CustomSound:
    internal_name: str
    ogg_path: str
    volume: float = 1.0
    pitch: float = 1.0
    subtitle: str = ""
    stream: bool = False

    datapack_subdirectory_name: str = field(init=False, repr=False, default="sound")

    def __post_init__(self) -> None:
        assert 0 <= self.volume <= 1, "Volume must be between 0 and 1"
        assert 0.5 <= self.pitch <= 2, "Pitch must be between 0.5 and 2"
    
    def create_resource_pack_files(self, datapack: "Datapack") -> None:
        os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"sounds", exist_ok=True)
        shutil.copyfile(self.ogg_path, Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"sounds"/f"{self.internal_name}.ogg")

    def create_sound_entry(self, datapack: "Datapack") -> dict[str, list[dict[str, Any]] | str]:
        return {
            "sounds": [
                {
                    "name": f"{datapack.namespace}:{self.internal_name}",
                    "volume": self.volume,
                    "pitch": self.pitch,
                    "stream": True if self.stream else False,
                }
            ]
        } | (  # Add subtitles if they're not empty
            {
                "subtitle": self.subtitle
            } if self.subtitle else {}
        )
