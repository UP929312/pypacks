import json
import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from pypacks.image_manipulation.png_utils import get_png_height

if TYPE_CHECKING:
    from pypacks.pack import Pack

# TODO: Allow non-bitmap fonts


@dataclass
class FontImage:
    """Represents an image in a book."""
    name: str
    image_bytes: bytes
    height: int | None = None  # Override, if a custom height is passed in, it won't use the image_bytes height
    y_offset: int | None = None  # Is vertical/up, not shifted down

    def __post_init__(self) -> None:
        assert self.height is None or 0 < self.height <= 256, "Height must be between 1 and 256"
        assert 0 < get_png_height(image_bytes=self.image_bytes, enforce_square=False) <= 256, f"Image height must be between 1 and 256, was {get_png_height(image_bytes=self.image_bytes)}"

    def to_dict(self, pack_namespace: str, char: str) -> dict[str, Any]:
        return {
            "type": "bitmap",
            "file": f"{pack_namespace}:font/{self.name}.png",
            "height": self.height if self.height is not None else get_png_height(image_bytes=self.image_bytes),
            "ascent": self.y_offset if self.y_offset is not None else min(get_png_height(image_bytes=self.image_bytes) // 2, 16),
            "chars": [char],
        }


@dataclass
class CustomFont:
    """Adds a custom font to the resource pack. Not invokable manually, used internally (for now)"""
    name: str
    font_elements: list[FontImage]

    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="font")

    def get_mapping(self) -> dict[str, str]:
        # Returns a mapping of element name to it's char | Generate \uE000 - \uE999
        return {element.name: f"\\uE{i:03}" for i, element in enumerate(self.font_elements)}

    def to_dict(self, pack_namespace: str) -> list[dict[str, Any]]:
        mapping = self.get_mapping()
        return [
            element.to_dict(pack_namespace, mapping[element.name])
            for element in self.font_elements
        ]

    def create_resource_pack_files(self, pack: "Pack") -> None:
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name, exist_ok=True)
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/"textures"/"font", exist_ok=True)

        for font_element in self.font_elements:
            with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/"textures"/"font"/f"{font_element.name}.png", "wb") as file:
                file.write(font_element.image_bytes)

        with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name/f"{self.name}.json", "w") as file:
            file.write(json.dumps({"providers": self.to_dict(pack.namespace)}, indent=4).replace("\\\\", "\\"))  # Replace double backslashes with single backslashes
