from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from pypacks.resources.base_resource import BaseResource
from pypacks.resources.custom_item import CustomItem
from pypacks.additions.item_components import Components, JukeboxPlayable

# from pypacks.utils import get_ogg_duration
if TYPE_CHECKING:
    from pypacks.pack import Pack


@dataclass
class CustomJukeboxSong(BaseResource):
    """Create a CustomSound first, then set it's internal_name & audio_path to be the same as the sound's internal_name + ogg_path, e.g.
    CustomJukeboxSong(custom_sound.internal_name, "My Song", custom_sound.ogg_path, 4, 5)"""
    internal_name: str
    description: str
    ogg_path: "str | Path"
    comparator_output: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    length_in_seconds: float  # | None = None  # Leave None to calculate it automatically (although it's recommended to set it manually)

    sub_directories: list[str] = field(default_factory=list)  # Used to nest and organise items nicely

    datapack_subdirectory_name: str = field(init=False, repr=False, default="jukebox_song")
    # resource_pack_subdirectory_name: str = field(init=False, repr=False, default="sounds")

    # def __post_init__(self) -> None:
    #     if True:#if self.length_in_seconds is None:
    #         with open(self.ogg_path, 'rb') as file:
    #             rint("Guessed song length: ", get_ogg_duration(file.read()))
    #             # self.length_in_seconds = get_ogg_duration(file.read())

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "sound_event": {"sound_id": f"{pack_namespace}:{self.internal_name}"},
            "description": {"text": self.description, "color": "white"},
            "length_in_seconds": float(self.length_in_seconds),
            "comparator_output": self.comparator_output,
        }

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any], sub_directories: list[str]) -> "CustomJukeboxSong":
        return cls(
            internal_name,
            description=data["description"] if isinstance(data["description"], str) else data["description"].get("translate", "UNKNOWN:UNKNOWN"),
            ogg_path=(data["sound_event"] if isinstance(data.get("sound_event"), str) else data.get("sound_event", {}).get("sound_id", "UKNOWN:UKNOWN")).split(":")[-1],
            comparator_output=data["comparator_output"],
            length_in_seconds=data["length_in_seconds"],
            sub_directories=sub_directories,
        )

    @classmethod
    def from_combined_files(cls, data_path: "Path", assets_path: "Path") -> list["CustomJukeboxSong"]:
        jukebox_songs: list["CustomJukeboxSong"] = cls.from_datapack_files(data_path)  # pyright: ignore
        for jukebox_song in jukebox_songs:
            path = assets_path/"sounds"/f"{jukebox_song.ogg_path}.ogg"
            if path.exists():
                jukebox_song.ogg_path = path
            else:
                raise FileNotFoundError(f"Could not find the ogg file for {cls.__name__} {jukebox_song.internal_name} at {path}")
        return jukebox_songs

    def generate_custom_item(self, pack_namespace: str) -> "CustomItem":
        return CustomItem(
            self.internal_name,
            "minecraft:music_disc_cat",
            self.internal_name.replace("_", " ").title(),
            components=Components(jukebox_playable=JukeboxPlayable(self))
        )

    def generate_give_command(self, pack_namespace: str) -> str:
        return self.generate_custom_item(pack_namespace).generate_give_command(pack_namespace)

    def generate_play_command(self, pack: "Pack") -> str:
        return f"playsound {self.get_reference(pack.namespace)} master @s ~ ~ ~ 1 1"
