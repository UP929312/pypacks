import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Any
from dataclasses import dataclass, field

from pypacks.resources.base_resource import BaseResource
from pypacks.resources.custom_item import CustomItem
from pypacks.additions.reference_book_config import PAINTING_REF_BOOK_CONFIG
from pypacks.additions.item_components import Components, EntityData
from pypacks.utils import recursively_remove_nones_from_data

if TYPE_CHECKING:
    from pypacks.pack import Pack


@dataclass
class CustomPainting(BaseResource):
    # https://minecraft.wiki/w/Painting_variant_definition
    internal_name: str
    image_path: "str | Path"
    title: str | None = None
    author: str | None = None
    width_in_blocks: int = 1
    height_in_blocks: int = 1

    datapack_subdirectory_name: str = field(init=False, repr=False, default="painting_variant")
    resource_pack_subdirectory_name: str = field(init=False, repr=False, default="textures/painting")

    def __post_init__(self) -> None:
        assert 1 <= self.width_in_blocks <= 16, "Width must be between 1 and 16"
        assert 1 <= self.height_in_blocks <= 16, "Height must be between 1 and 16"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "asset_id": self.get_reference(pack_namespace),
            "width": self.width_in_blocks,
            "height": self.height_in_blocks,
            "title": {"color": "yellow", "text": self.title} if self.title is not None else None,
            "author": {"color": "gray", "text": self.author} if self.author is not None else None,
        })

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "CustomPainting":
        return cls(
            internal_name,
            data["asset_id"].split(":")[-1],
            title=data.get("title", {}).get("text") or data.get("title", {}).get("translate", "UNKNOWN"),
            author=data.get("author", {}).get("text") or data.get("author", {}).get("translate", "UNKNOWN"),
            width_in_blocks=data.get("width", 1),
            height_in_blocks=data.get("height", 1),
        )

    def create_resource_pack_files(self, pack: "Pack") -> None:
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name, exist_ok=True)
        shutil.copyfile(self.image_path, Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name/f"{self.internal_name}.png")

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

    @classmethod
    def from_combined_files(cls, data_path: "Path", assets_path: "Path") -> list["CustomPainting"]:
        paintings: list["CustomPainting"] = cls.from_datapack_files(data_path)  # pyright: ignore
        for painting in paintings:
            path = assets_path/painting.resource_pack_subdirectory_name/f"{painting.image_path}.png"
            if path.exists():
                painting.image_path = path
            else:
                raise FileNotFoundError(f"Could not find the image file for painting {painting.internal_name} at {path}")
        return paintings


# Original paintings:
KEBAB = CustomPainting("kebab", "", "Kebab med tre pepperoni", "Kristoffer Zetterstrand", 1, 1)
AZTEC = CustomPainting("aztec", "", "de_aztec", "Kristoffer Zetterstrand", 1, 1)
ALBANIA = CustomPainting("albania", "", "Albanian", "Kristoffer Zetterstrand", 1, 1)
AZTEC2 = CustomPainting("aztec2", "", "de_aztec", "Kristoffer Zetterstrand", 1, 1)
BOMB = CustomPainting("bomb", "", "Target Successfully Bombed", "Kristoffer Zetterstrand", 1, 1)
PLANT = CustomPainting("plant", "", "Paradisträd", "Kristoffer Zetterstrand", 1, 1)
WASTELAND = CustomPainting("wasteland", "", "Wasteland", "Kristoffer Zetterstrand", 1, 1)
MEDITATIVE = CustomPainting("meditative", "", "Meditative", "Sarah Boeving", 1, 1)

WANDERER = CustomPainting("wanderer", "", "Wanderer", "Kristoffer Zetterstrand", 1, 2)
GRAHAM = CustomPainting("graham", "", "Graham", "Kristoffer Zetterstrand", 1, 2)
PRAIRIE_RIDE = CustomPainting("prairie_ride", "", "Prairie Ride", "Sarah Boeving", 1, 2)

POOL = CustomPainting("pool", "", "The Pool", "Kristoffer Zetterstrand", 2, 1)
COURBET = CustomPainting("courbet", "", "Bonjour Monsieur Courbet", "Kristoffer Zetterstrand", 2, 1)
SUNSET = CustomPainting("sunset", "", "sunset_dense", "Kristoffer Zetterstrand", 2, 1)
SEA = CustomPainting("sea", "", "Seaside", "Kristoffer Zetterstrand", 2, 1)
CREEBET = CustomPainting("creebet", "", "Creebet", "Kristoffer Zetterstrand", 2, 1)

MATCH = CustomPainting("match", "", "Match", "Kristoffer Zetterstrand", 2, 2)
BUST = CustomPainting("bust", "", "Bust", "Kristoffer Zetterstrand", 2, 2)
STAGE = CustomPainting("stage", "", "The Stage Is Set", "Kristoffer Zetterstrand", 2, 2)
VOID = CustomPainting("void", "", "The void", "Kristoffer Zetterstrand", 2, 2)
SKULL_AND_ROSES = CustomPainting("skull_and_roses", "", "Skull and Roses", "Kristoffer Zetterstrand", 2, 2)
WITHER = CustomPainting("wither", "", "Wither", "Mojang (Jens Bergensten)", 2, 2)
BAROQUE = CustomPainting("baroque", "", "Baroque", "Sarah Boeving", 2, 2)
HUMBLE = CustomPainting("humble", "", "Humble", "Sarah Boeving", 2, 2)

BOUQUET = CustomPainting("bouquet", "", "Bouquet", "Kristoffer Zetterstrand", 3, 3)
CAVEBIRD = CustomPainting("cavebird", "", "Cave Bird", "Kristoffer Zetterstrand", 3, 3)
COTAN = CustomPainting("cotan", "", "Cotán", "Kristoffer Zetterstrand", 3, 3)
ENDBOSS = CustomPainting("endboss", "", "End Boss", "Kristoffer Zetterstrand", 3, 3)
FERN = CustomPainting("fern", "", "Fern", "Kristoffer Zetterstrand", 3, 3)
OWLEMONS = CustomPainting("owlemons", "", "Owlemons", "Kristoffer Zetterstrand", 3, 3)
SUNFLOWERS = CustomPainting("sunflowers", "", "Sunflowers", "Kristoffer Zetterstrand", 3, 3)
TIDES = CustomPainting("tides", "", "Tides", "Kristoffer Zetterstrand", 3, 3)

BACKYARD = CustomPainting("backyard", "", "Backyard", "Kristoffer Zetterstrand", 3, 4)
POND = CustomPainting("pond", "", "Pond", "Kristoffer Zetterstrand", 3, 4)

FIGHTERS = CustomPainting("fighters", "", "Fighters", "Kristoffer Zetterstrand", 4, 2)
CHANGING = CustomPainting("changing", "", "Changing", "Kristoffer Zetterstrand", 4, 2)
FINDING = CustomPainting("finding", "", "Finding", "Kristoffer Zetterstrand", 4, 2)
LOWMIST = CustomPainting("lowmist", "", "Lowmist", "Kristoffer Zetterstrand", 4, 2)
PASSAGE = CustomPainting("passage", "", "Passage", "Kristoffer Zetterstrand", 4, 2)

MORTAL_COIL = CustomPainting("mortal_coil", "", "Mortal Coil", "Kristoffer Zetterstrand", 4, 3)
KONG = CustomPainting("donkey_kong", "", "Kong", "Kristoffer Zetterstrand", 4, 3)

POINTER = CustomPainting("pointer", "", "Pointer", "Kristoffer Zetterstrand", 4, 4)
PIGSCENE = CustomPainting("pigscene", "", "Pigscene", "Kristoffer Zetterstrand", 4, 4)
SKULL_ON_FIRE = CustomPainting("burning_skull", "", "Skull on Fire", "Kristoffer Zetterstrand", 4, 4)
ORB = CustomPainting("orb", "", "Orb", "Kristoffer Zetterstrand", 4, 4)
UNPACKED = CustomPainting("unpacked", "", "Unpacked", "Sarah Boeving", 4, 4)

ALL_DEFAULT_PAINTINGS = [
    KEBAB, AZTEC, ALBANIA, AZTEC2, BOMB, PLANT, WASTELAND, MEDITATIVE,
    WANDERER, GRAHAM, PRAIRIE_RIDE,
    POOL, COURBET, SUNSET, SEA, CREEBET,
    MATCH, BUST, STAGE, VOID, SKULL_AND_ROSES, WITHER, BAROQUE, HUMBLE,
    BOUQUET, CAVEBIRD, COTAN, ENDBOSS, FERN, OWLEMONS, SUNFLOWERS, TIDES,
    BACKYARD, POND,
    FIGHTERS, CHANGING, FINDING, LOWMIST, PASSAGE,
    MORTAL_COIL, KONG,
    POINTER, PIGSCENE, SKULL_ON_FIRE, ORB, UNPACKED,
]
