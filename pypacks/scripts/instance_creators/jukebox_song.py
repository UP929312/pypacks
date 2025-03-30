import os
from typing import Any

import requests

from pypacks.resources.custom_jukebox_song import CustomJukeboxSong


all_data: dict[str, Any] = requests.get("https://raw.githubusercontent.com/misode/mcmeta/refs/heads/summary/data/jukebox_song/data.min.json").json()
output_path = f"C:\\Users\\{os.environ['USERNAME']}\\Desktop\\pypacks\\pypacks\\minecraft\\jukebox_songs.py"

lines = [
    "from pypacks.resources.custom_jukebox_song import CustomJukeboxSong",
    "",
    "",
]

instances = [CustomJukeboxSong.from_dict(item_name, data) for item_name, data in all_data.items()]
lines += [f"{x.internal_name.upper().replace('5', 'FIVE').replace('11', 'ELEVEN').replace('13', 'THIRTEEN')} = {repr(x)}" for x in instances]

with open(output_path, "w", encoding="utf-8") as file:
    file.write("\n".join(lines)+"\n")
