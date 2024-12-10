import json
import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Any
from dataclasses import dataclass, field

# from pypacks.utils import get_png_dimensions

from pypacks.resources.custom_item import CustomItem
from pypacks.reference_book_config import PAINTING_REF_BOOK_CATEGORY, PAINTING_REF_BOOK_CONFIG
from pypacks.resources.item_components import CustomItemData, EntityData

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

    datapack_subdirectory_name: str = field(init=False, repr=False, default="painting_variant")

    def __post_init__(self) -> None:
        assert 1 <= self.width_in_blocks <= 16, "Width must be between 1 and 16"
        assert 1 <= self.height_in_blocks <= 16, "Height must be between 1 and 16"

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
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
        with open(Path(datapack.datapack_output_path)/"data"/datapack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(datapack), file, indent=4)

    def create_resource_pack_files(self, datapack: "Datapack") -> None:
        os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"textures"/"painting", exist_ok=True)
        shutil.copyfile(self.image_path, Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"textures"/"painting"/f"{self.internal_name}.png")

    def generate_custom_item(self, datapack: "Datapack") -> "CustomItem":
        return CustomItem(
            "minecraft:painting",
            self.internal_name,
            self.title or self.internal_name,
            additional_item_data=CustomItemData(entity_data=EntityData({"id": "minecraft:painting", "variant": f"{datapack.namespace}:{self.internal_name}"})),
            ref_book_config=PAINTING_REF_BOOK_CONFIG
        )

    def generate_give_command(self, datapack: "Datapack") -> str:
        return self.generate_custom_item(datapack).generate_give_command(datapack)
