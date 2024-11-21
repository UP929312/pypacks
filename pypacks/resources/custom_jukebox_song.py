import json
from typing import TYPE_CHECKING
from dataclasses import dataclass

# from pypacks.utils import get_ogg_duration

if TYPE_CHECKING:
    from pypacks.datapack import Datapack

@dataclass
class CustomJukeboxSong:
    """Create a CustomSound first, then set it's internal_name & audio_path to be the same as the sound's internal_name + ogg_path"""
    internal_name: str
    description: str
    ogg_path: str
    comparator_output: int
    length_in_seconds: float #  | None = None  # Leave None to calculate it automatically (although it's recommended to set it manually)

    # def __post_init__(self) -> None:
    #     if True:#if self.length_in_seconds is None:
    #         with open(self.ogg_path, 'rb') as f:
    #             print("Guessed song length: ", get_ogg_duration(f.read()))
    #             # self.length_in_seconds = get_ogg_duration(f.read())

    def create_json_file(self, datapack: "Datapack") -> None:
        # print(f"{datapack.datapack_output_path}/data/{datapack.namespace}/jukebox_song/{self.internal_name}.json")
        with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/jukebox_song/{self.internal_name}.json", "w") as f:
            json.dump({
                "sound_event": {"sound_id": f"{datapack.namespace}:{self.internal_name}"},
                "description": {"text": self.description, "color": "white"},
                "length_in_seconds": float(self.length_in_seconds),  # type: ignore[union-attr]
                "comparator_output": self.comparator_output,
            }, f, indent=4)

    def generate_give_command(self, datapack: "Datapack") -> str:
        data = '{"song": "%s:%s"}' % (datapack.namespace, self.internal_name)
        return 'give @p minecraft:music_disc_cat[jukebox_playable=%s]' % data