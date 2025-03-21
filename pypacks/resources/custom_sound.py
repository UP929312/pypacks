import json
import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Any
from dataclasses import dataclass, field

from pypacks.utils import recursively_remove_nones_from_data
from pypacks.resources.base_resource import BaseResource

if TYPE_CHECKING:
    from pypacks.pack import Pack


@dataclass
class CustomSound(BaseResource):
    # https://minecraft.wiki/w/Sounds.json
    internal_name: str
    ogg_path: "str | Path"
    volume: float = 1.0
    pitch: float = 1.0
    stream: bool = False
    subtitle: str | None = None

    resource_pack_subdirectory_name: str = field(init=False, repr=False, default="sounds")

    def __post_init__(self) -> None:
        assert 0 <= self.volume <= 1, "Volume must be between 0 and 1"
        assert 0.5 <= self.pitch <= 2, "Pitch must be between 0.5 and 2"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        """Is created in "assets"/pack.namespace/"sounds.json" with a list of sounds (rather than different files) """
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "sounds": [
                {
                    "name": self.get_reference(pack_namespace),
                    "volume": self.volume,
                    "pitch": self.pitch,
                    "stream": self.stream,
                },
            ],
            "subtitle": self.subtitle,  # Add subtitles if they're not empty
        })

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "CustomSound":
        # Sounds can either be the complicated sound format, or simply
        # The path to a sound file from the "<namespace>/sounds" folder (excluding the .ogg file extension).
        if isinstance(data["sounds"][0], str):
            return cls(
                internal_name,
                ogg_path=data["sounds"][0].split(":")[1]+".ogg",
                volume=1.0,
                pitch=1.0,
                stream=False,
                subtitle=None,
            )
        return cls(
            internal_name,
            ogg_path=data["sounds"][0]["name"].split(":")[1]+".ogg",
            volume=data["sounds"][0].get("volume", 1.0),
            pitch=data["sounds"][0].get("pitch", 1.0),
            stream=data["sounds"][0].get("stream", False),
            subtitle=data.get("subtitle", None),
        )

    def get_run_command(self, pack_namespace: str) -> str:
        return f"playsound {self.get_reference(pack_namespace)} master @a[distance=..10] ~ ~ ~ {self.volume} {self.pitch}"

    def create_resource_pack_files(self, pack: "Pack") -> None:
        path = Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name
        os.makedirs(path, exist_ok=True)
        shutil.copyfile(self.ogg_path, path/f"{self.internal_name}.ogg")

    @classmethod
    def from_resource_pack_files(cls, assets_path: Path) -> list["CustomSound"]:
        with open(assets_path/"sounds.json", encoding="utf-8") as file:
            sounds_raw: dict[str, Any] = json.load(file)
            sounds = [cls.from_dict(sound_event, sound_data) for sound_event, sound_data in sounds_raw.items()]
            for sound in sounds:
                sound.ogg_path = assets_path/"sounds"/sound.ogg_path
            return sounds
