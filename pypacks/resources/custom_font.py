import json
import os
import shutil
from pathlib import Path
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from pypacks.image_manipulation.png_utils import get_png_height

if TYPE_CHECKING:
    from pypacks.pack import Pack


@dataclass
class CustomFont:
    """Adds a custom font to the resource pack. Not invokable manually, used internally (for now)"""
    name: str
    font_elements: list["BitMapFontChar | SpaceFontChar | TTFFontProvider | ReferenceFontProvider"]

    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="font")

    def get_reference(self, pack_namespace: str) -> str:
        return f"{pack_namespace}:{self.name}.json"

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
        for font_element in self.font_elements:
            font_element.create_resource_pack_files(pack)

        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name, exist_ok=True)

        with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name/f"{self.name}.json", "w") as file:
            file.write(json.dumps({"providers": self.to_dict(pack.namespace)}, indent=4).replace("\\\\", "\\"))  # Replace double backslashes with single backslashes

    def get_test_command(self, pack_namespace: str) -> str:
        return f"tellraw @p {{\"text\": \"Hello World!\", \"font\": \"{self.get_reference(pack_namespace)}\"}}"

# =================================================================================================


@dataclass
class TTFFontProvider:
    """Represents an entire TTF/OTF font pack
    The ttf provider embeds already-compiled TrueType and OpenType fonts"""
    name: str
    font_path: str | Path
    oversample: int = 2  # The resolution to render at. Values that don't match the glyph's native em sizing division or DPI cause it to be anti-aliased.
    horizontal_shift: int = 0  # Defines how much each glyph contained in this font is moved horizontally
    vertical_shift: int = 0  # Defines how much each glyph contained in this font is moved vertically
    size: int = 8  # This field is similar to a bitmap provider's height field. This is a divisor by which the em-size of the font's glyphs are to be divided and then fitted into the bitmap grid. This value can vary greatly across different fonts.
    skip: list[str] = field(default_factory=list)  # A list of the characters to which this font has no assignment. If provided the strings are concatenated together and then act as if it were originally a string. This allows the same input as a bitmap provider's chars.

    def __post_init__(self) -> None:
        self.file_type = "ttf"  # if str(self.font_path).endswith(".ttf") else "otf"
        assert str(self.font_path).endswith(".ttf"), "Font path must end with .ttf!"
        assert self.oversample > 0, "Oversample must be greater than 0"

    def to_dict(self, pack_namespace: str, _: str) -> dict[str, Any]:
        # TTF Fonts require the following structure:
        # assets/
        # ├── <namespace>/
        # │   ├── font/
        # │   │   ├── <name>.json
        # │   │   └── <name>.ttf/otf
        return {
            "type": "ttf",
            "file": f"{pack_namespace}:{self.name}.{self.file_type}",
            "oversample": self.oversample,
            "shift": [self.horizontal_shift, self.vertical_shift],
            "size": self.size,
            "skip": self.skip,
        }

    def create_resource_pack_files(self, pack: "Pack") -> None:
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/"font", exist_ok=True)
        shutil.copy(self.font_path, Path(pack.resource_pack_path)/"assets"/pack.namespace/"font"/f"{self.name}.{self.file_type}")


# =================================================================================================


@dataclass
class BitMapFontChar:
    """Represents an image in a book."""
    name: str  # e.g. "logo"
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

    def create_resource_pack_files(self, pack: "Pack") -> None:
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/"textures"/"font", exist_ok=True)

        with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/"textures"/"font"/f"{self.name}.png", "wb") as file:
            file.write(self.image_bytes)


@dataclass
class SpaceFontChar:
    """Show chosen characters as spaces."""
    name: str
    width: int = 1  # Defines how wide the space character is

    def to_dict(self, pack_namespace: str, char: str) -> dict[str, Any]:
        return {
            "type": "space",
            "advances": {
                char: self.width,
            }
        }

    def create_resource_pack_files(self, pack: "Pack") -> None:
        pass


@dataclass
class ReferenceFontProvider:
    name: str
    font: "str | CustomFont"

    def to_dict(self, pack_namespace: str, _: str) -> dict[str, Any]:
        return {
            "type": "reference",
            "file": f"{pack_namespace}:font/{self.font}.json" if not isinstance(self.font, CustomFont) else self.font.get_reference(pack_namespace),
        }

    def create_resource_pack_files(self, pack: "Pack") -> None:
        pass
