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
    title: str
    author: str
    width_in_blocks: int
    height_in_blocks: int
    image_path: str

    def __post_init__(self) -> None:
        assert 1 <= self.width_in_blocks <= 16, "Width must be between 1 and 16"
        assert 1 <= self.height_in_blocks <= 16, "Height must be between 1 and 16"

    def create_json_file(self, datapack: "Datapack") -> None:
        with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/painting_variant/{self.internal_name}.json", "w") as f:
            json.dump({
                "asset_id": f"{datapack.namespace}:{self.internal_name}",
                # "author": self.author,
                # "title": self.title,  # TODO: Add this
                "width": self.width_in_blocks,
                "height": self.height_in_blocks,
            }, f, indent=4)

    def generate_give_command(self, datapack: "Datapack") -> str:
        data = '{"id": "minecraft:painting", "variant": "%s:%s"}' % (datapack.namespace, self.internal_name)
        return 'give @p minecraft:painting[minecraft:entity_data=%s]' % data