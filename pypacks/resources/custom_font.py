import json
import os
from pathlib import Path
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from pypacks.utils import get_png_height

if TYPE_CHECKING:
    from pypacks.datapack import Datapack


@dataclass
class BookImage:
    """Represents an image in a book."""
    name: str
    image_bytes: bytes
    height: int | None = None  # Override, if a custom height is passed in, it won't use the image_bytes height
    y_offset: int | None = None  # Is vertical + up, not shifted down

    def __post_init__(self) -> None:
        assert self.height is None or 0 < self.height <= 256, "Height must be between 1 and 256"
        assert 0 < get_png_height(image_bytes=self.image_bytes, enforce_square=False) <= 256, "Image height must be between 1 and 256"


@dataclass
class CustomFont:
    """Adds a custom font to the resource pack. Not invokable manually, used internally (for now)"""
    name: str
    font_elements: list[BookImage]

    def get_mapping(self) -> dict[str, str]:
        # Returns a mapping of element name to it's char | Generate \uE000 - \uE999
        return {element.name.split("\\")[-1].removesuffix('.png'): f"\\uE{i:03}" for i, element in enumerate(self.font_elements)}

    def to_dict(self, datapack: "Datapack") -> list[dict[str, Any]]:
        mapping = self.get_mapping()
        return [
            {
                "type": "bitmap",
                "file": f"{datapack.namespace}:font/{element.name}.png",
                "height": element.height if element.height is not None else get_png_height(image_bytes=element.image_bytes),
                "ascent": element.y_offset if element.y_offset is not None else min(get_png_height(image_bytes=element.image_bytes) // 2, 16),
                "chars": [mapping[element.name]],
            }
            for element in self.font_elements
        ]

    def create_resource_pack_files(self, datapack: "Datapack") -> None:
        os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"font", exist_ok=True)
        os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"textures"/"font", exist_ok=True)
        for font_element in self.font_elements:
            with open(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"font"/f"{font_element.name}.png", "wb") as file:
                file.write(font_element.image_bytes)
        with open(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"textures"/"font"/f"{self.name}.json", "w") as file:
            file.write(json.dumps({"providers": self.to_dict(datapack)}, indent=4).replace("\\\\", "\\"))  # Replace double backslashes with single backslashes
