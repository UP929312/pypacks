import json
from typing import TYPE_CHECKING
from dataclasses import dataclass, field

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

    datapack_subdirectory_name: str = field(init=False, default="painting_variant")

    def __post_init__(self) -> None:
        assert 1 <= self.width_in_blocks <= 16, "Width must be between 1 and 16"
        assert 1 <= self.height_in_blocks <= 16, "Height must be between 1 and 16"#

    def to_dict(self, datapack: "Datapack") -> dict[str, str]:
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
        return data

    def create_datapack_files(self, datapack: "Datapack") -> None:
        with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/{self.__class__.datapack_subdirectory_name}/{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(datapack), file, indent=4)

    def generate_give_command(self, datapack: "Datapack") -> str:
        data = '{"id": "minecraft:painting", "variant": "%s:%s"}' % (datapack.namespace, self.internal_name)
        return 'give @p minecraft:painting[minecraft:entity_data=%s]' % data