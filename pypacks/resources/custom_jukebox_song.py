import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pypacks.resources.custom_item import CustomItem
from pypacks.additions.item_components import Components, JukeboxPlayable

# from pypacks.utils import get_ogg_duration
if TYPE_CHECKING:
    from pypacks.pack import Pack


@dataclass
class CustomJukeboxSong:
    """Create a CustomSound first, then set it's internal_name & audio_path to be the same as the sound's internal_name + ogg_path"""
    internal_name: str
    description: str
    ogg_path: str
    comparator_output: int
    length_in_seconds: float  # | None = None  # Leave None to calculate it automatically (although it's recommended to set it manually)

    datapack_subdirectory_name: str = field(init=False, repr=False, default="jukebox_song")

    # def __post_init__(self) -> None:
    #     if True:#if self.length_in_seconds is None:
    #         with open(self.ogg_path, 'rb') as file:
    #             rint("Guessed song length: ", get_ogg_duration(file.read()))
    #             # self.length_in_seconds = get_ogg_duration(file.read())

    def get_reference(self, pack_namespace: str) -> str:
        return f"{pack_namespace}:{self.internal_name}"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "sound_event": {"sound_id": f"{pack_namespace}:{self.internal_name}"},
            "description": {"text": self.description, "color": "white"},
            "length_in_seconds": float(self.length_in_seconds),
            "comparator_output": self.comparator_output,
        }

    def create_datapack_files(self, pack: "Pack") -> None:
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)

    def generate_custom_item(self, pack: "Pack") -> "CustomItem":
        return CustomItem(
            self.internal_name,
            "minecraft:music_disc_cat",
            self.internal_name.replace("_", " ").title(),
            components=Components(jukebox_playable=JukeboxPlayable(self))
        )

    def generate_give_command(self, pack: "Pack") -> str:
        return self.generate_custom_item(pack).generate_give_command(pack.namespace)

    def generate_play_command(self, pack: "Pack") -> str:
        return f"playsound {self.get_reference(pack.namespace)} master @s ~ ~ ~ 1 1"
