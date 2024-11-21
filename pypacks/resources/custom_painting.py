import json
import shutil
from typing import TYPE_CHECKING
from dataclasses import dataclass

# from pypacks.utils import get_png_dimensions

if TYPE_CHECKING:
    from pypacks.datapack import Datapack

@dataclass
class CustomPainting:
    internal_name: str
    image_path: str
    title: str | None = None
    author: str | None = None
    width_in_blocks: int = 1
    height_in_blocks: int = 1

    def __post_init__(self) -> None:
        assert 1 <= self.width_in_blocks <= 16, "Width must be between 1 and 16"
        assert 1 <= self.height_in_blocks <= 16, "Height must be between 1 and 16"

    def create_json_file(self, datapack: "Datapack") -> None:
        data = {
            "asset_id": f"{datapack.namespace}:{self.internal_name}",
            "width": self.width_in_blocks,
            "height": self.height_in_blocks,
        }
        if self.title is not None:
            data["title"] = {
                "color": "yellow",
                "text": self.title,
            }
        if self.author is not None:
            data["author"] = {
                "color": "gray",
                "text": self.author,
            }
        with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/painting_variant/{self.internal_name}.json", "w") as f:
            json.dump(data, f, indent=4)

    def generate_give_command(self, datapack: "Datapack") -> str:
        data = '{"id": "minecraft:painting", "variant": "%s:%s"}' % (datapack.namespace, self.internal_name)
        return 'give @p minecraft:painting[minecraft:entity_data=%s]' % data