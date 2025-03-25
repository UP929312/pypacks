import json
import os
import shutil
from pathlib import Path
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from pypacks.image_manipulation.png_utils import get_png_height
from pypacks.resources.base_resource import BaseResource

if TYPE_CHECKING:
    from pypacks.pack import Pack


@dataclass
class CustomFont(BaseResource):
    """Adds a custom font to the resource pack"""
    internal_name: str
    providers: list["BitMapFontChar | SpaceFontChar | TTFFontProvider | ReferenceFontProvider"]

    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="font")

    def get_reference(self, pack_namespace: str) -> str:
        return f"{pack_namespace}:{self.internal_name}.json"  # TODO: Is this correct?

    def get_mapping(self) -> dict[str, str]:
        # Returns a mapping of element name to it's char | Generate \uE000 - \uE999 for BitMapFontChars
        # This is so players can use images using pack.font_mapping["my_image"] rather than manually giving them random
        # Unicode characters or remember that "A" maps to the image, "B" maps to an icon, etc.
        # Edit: I use 100 as the start because \u0020 is a space, and so messes everything up.
        return {element.name: f"\\u{i:04}" for i, element in enumerate(self.providers, 100) if isinstance(element, AutoAssignBitMapFontChar)}

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        mapping = self.get_mapping()
        return {
            "providers": [
                provider.to_dict(pack_namespace, mapping[provider.name]) if isinstance(provider, AutoAssignBitMapFontChar) else provider.to_dict(pack_namespace)
                for provider in self.providers
            ]
        }

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "CustomFont":
        return cls(
            internal_name,
            [FONT_TYPE_NAMES_TO_CLASSES[provider["type"]].from_dict(internal_name+"_font", provider) for provider in data["providers"]],
        )

    def create_resource_pack_files(self, pack: "Pack") -> None:
        for provider in self.providers:
            provider.create_resource_pack_files(pack)  # Ports over things like images, .ttf files, etc.

        path = Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name
        os.makedirs(path, exist_ok=True)

        with open(path/f"{self.internal_name}.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(self.to_dict(pack.namespace), indent=4).replace("\\\\", "\\"))

    def get_test_command(self, pack_namespace: str) -> str:
        return f"tellraw @s {{\"text\": \"Hello World!\", \"font\": \"{self.get_reference(pack_namespace)}\"}}"


# =================================================================================================


@dataclass
class TTFFontProvider:
    """Represents an entire TTF/OTF font pack
    The ttf provider embeds already-compiled TrueType and OpenType fonts"""
    internal_name: str
    font_path: str | Path
    oversample: int = 2  # The resolution to render at. Values that don't match the glyph's native em sizing division or DPI cause it to be anti-aliased.
    horizontal_shift: int = 0  # Defines how much each glyph contained in this font is moved horizontally
    vertical_shift: int = 0  # Defines how much each glyph contained in this font is moved vertically
    size: int = 8  # This field is similar to a bitmap provider's height field. This is a divisor by which the em-size of the font's glyphs are to be divided and then fitted into the bitmap grid. This value can vary greatly across different fonts.
    skip: list[str] = field(default_factory=list)  # A list of the characters to which this font has no assignment. If provided the strings are concatenated together and then act as if it were originally a string. This allows the same input as a bitmap provider's chars.

    def __post_init__(self) -> None:
        assert str(self.font_path).endswith(".ttf"), "Font path must end with .ttf!"
        assert self.oversample > 0, "Oversample must be greater than 0"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        # TTF Fonts require the following structure:
        # assets/
        # ├── <namespace>/
        # │   ├── font/
        # │   │   ├── <name>.json
        # │   │   └── <name>.ttf/otf
        return {
            "type": "ttf",
            "file": f"{pack_namespace}:{self.internal_name}.ttf",
            "oversample": self.oversample,
            "shift": [self.horizontal_shift, self.vertical_shift],
            "size": self.size,
            "skip": self.skip,
        }

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "TTFFontProvider":
        return cls(
            internal_name,
            data["file"].split(":")[1]+".ttf",  # TODO: Add this
            oversample=data.get("oversample", 2),
            horizontal_shift=data.get("shift", [0, 0])[0],
            vertical_shift=data.get("shift", [0, 0])[1],
            size=data.get("size", 8),
            skip=data.get("skip", []),
        )

    def create_resource_pack_files(self, pack: "Pack") -> None:
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/"font", exist_ok=True)
        shutil.copy(self.font_path, Path(pack.resource_pack_path)/"assets"/pack.namespace/"font"/f"{self.internal_name}.ttf")


# =================================================================================================


@dataclass
class BitMapFontChar:
    """Represents an image in a book."""
    name: str  # e.g. "logo"
    image_bytes: bytes = field(repr=False)  # The bytes of the image to be used
    height: int | None = None  # Override, if a custom height is passed in, it won't use the image_bytes height
    y_offset: int | None = None  # Is vertical/up, not shifted down
    chars: list[str] = field(default_factory=list)  # A list of characters to be shown for this image

    def __post_init__(self) -> None:
        assert self.height is None or 0 < self.height <= 256, "Height must be between 1 and 256"
        assert 0 < get_png_height(image_bytes=self.image_bytes, enforce_square=False) <= 256, f"Image height must be between 1px and 256px, was {get_png_height(image_bytes=self.image_bytes)}"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "bitmap",
            "file": f"{pack_namespace}:font/{self.name}.png",
            "height": self.height if self.height is not None else get_png_height(image_bytes=self.image_bytes),
            "ascent": self.y_offset if self.y_offset is not None else min(get_png_height(image_bytes=self.image_bytes) // 2, 16),
            "chars": self.chars,
        }

    @classmethod
    def from_dict(cls, name: str, data: dict[str, Any]) -> "BitMapFontChar":
        DEFAULT_IMAGE = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x14\x00\x00\x00\x14\x04\x03\x00\x00\x00\x7f\xa7\x00>\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\x15PLTE\x8dG2\x84?*\xf9\xee\xd0\xe0\xd2\xaem-\x1a\xcc\xb9\x98\xc9\xb7\x96|\xb7H\xcb\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x00\x16tEXtSoftware\x00Paint.NET 5.1\xf7\x83\xf7\x93\x00\x00\x00\xb4eXIfII*\x00\x08\x00\x00\x00\x05\x00\x1a\x01\x05\x00\x01\x00\x00\x00J\x00\x00\x00\x1b\x01\x05\x00\x01\x00\x00\x00R\x00\x00\x00(\x01\x03\x00\x01\x00\x00\x00\x02\x00\x00\x001\x01\x02\x00\x0e\x00\x00\x00Z\x00\x00\x00i\x87\x04\x00\x01\x00\x00\x00h\x00\x00\x00\x00\x00\x00\x00`\x00\x00\x00\x01\x00\x00\x00`\x00\x00\x00\x01\x00\x00\x00Paint.NET 5.1\x00\x03\x00\x00\x90\x07\x00\x04\x00\x00\x000230\x01\xa0\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x05\xa0\x04\x00\x01\x00\x00\x00\x92\x00\x00\x00\x00\x00\x00\x00\x02\x00\x01\x00\x02\x00\x04\x00\x00\x00R98\x00\x02\x00\x07\x00\x04\x00\x00\x000100\x00\x00\x00\x00c\xa4&\xc4RN\xfd\xcc\x00\x00\x000IDAT\x18\xd3c\x80\x03F\x06&%(0a`2\x86\x82\x10\x06&\xb340H\xc6\xc9$\xa8\x96V\n\x10\xa2\xcc\xa1P\x10\xc2 \xe2\x02\x01..\x00\xa4>3\x91\x90Q\x876\x00\x00\x00\x00IEND\xaeB`\x82"
        return cls(
            name,
            DEFAULT_IMAGE,  # TODO: Add this
            height=data.get("height", None),
            y_offset=data.get("ascent", None),
            chars=data.get("chars", []),
        )

    def create_resource_pack_files(self, pack: "Pack") -> None:
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/"textures"/"font", exist_ok=True)  # TODO: Another textures/<x> attribute?
        with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/"textures"/"font"/f"{self.name}.png", "wb") as file:
            file.write(self.image_bytes)


class AutoAssignBitMapFontChar(BitMapFontChar):
    """Represents an image in a book, but automatically assigns a character to it."""
    def __init__(self, name: str, image_bytes: bytes, height: int | None = None, y_offset: int | None = None) -> None:
        super().__init__(name, image_bytes, height, y_offset, chars=[])  # Need to override init to set chars

    def to_dict(self, pack_namespace: str, char: str) -> dict[str, Any]:  # type: ignore[override]
        return super().to_dict(pack_namespace) | {"chars": [char]}


@dataclass
class SpaceFontChar:
    """Show chosen characters as spaces."""
    width: int = 1  # Defines how wide the space character is
    chars: list[str] = field(default_factory=lambda: [" "])  # A list of characters to be shown as spaces

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "space",
            "advances": {char: self.width for char in self.chars},
        }

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "SpaceFontChar":
        return cls(
            width=list(data.get("advances", {}).values())[0],
            chars=list(data.get("advances", {}).keys()),
        )

    def create_resource_pack_files(self, pack: "Pack") -> None:
        pass


@dataclass
class ReferenceFontProvider:
    font: "str | CustomFont"  # Name of the font or a CustomFont object

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        # TODO: Maybe make this a regular str/path? Otherwise nested fonts won't work, but how many fonts are people adding?
        # I suppose it allows you to point to other font files (in a different pack?).
        return {
            "type": "reference",
            "file": f"{pack_namespace}:font/{self.font}.json" if not isinstance(self.font, CustomFont) else self.font.get_reference(pack_namespace),
        }

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "ReferenceFontProvider":
        return cls(
            data["file"],
        )

    def create_resource_pack_files(self, pack: "Pack") -> None:
        pass


FONT_TYPE_NAMES_TO_CLASSES: dict[str, type["TTFFontProvider | BitMapFontChar | SpaceFontChar | ReferenceFontProvider"]] = {
    "ttf": TTFFontProvider,
    "bitmap": BitMapFontChar,
    "space": SpaceFontChar,
    "reference": ReferenceFontProvider,
}
