import json
import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Any
from dataclasses import dataclass, field

from pypacks.resources.custom_item import CustomItem
from pypacks.reference_book_config import PAINTING_REF_BOOK_CONFIG
from pypacks.resources.item_components import Components, EntityData

if TYPE_CHECKING:
    from pypacks.pack import Pack


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

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        data = {
            "asset_id": f"{pack_namespace}:{self.internal_name}",
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

    def create_datapack_files(self, pack: "Pack") -> None:
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)

    def create_resource_pack_files(self, pack: "Pack") -> None:
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/"textures"/"painting", exist_ok=True)
        shutil.copyfile(self.image_path, Path(pack.resource_pack_path)/"assets"/pack.namespace/"textures"/"painting"/f"{self.internal_name}.png")

    def generate_custom_item(self, pack: "Pack") -> "CustomItem":
        return CustomItem(
            self.internal_name,
            "minecraft:painting",
            self.title or self.internal_name,
            components=Components(entity_data=EntityData({"id": "minecraft:painting", "variant": f"{pack.namespace}:{self.internal_name}"})),
            ref_book_config=PAINTING_REF_BOOK_CONFIG
        )

    def generate_give_command(self, pack: "Pack") -> str:
        return self.generate_custom_item(pack).generate_give_command(pack.namespace)
