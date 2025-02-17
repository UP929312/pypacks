import os
import json
import shutil
from pathlib import Path
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from pypacks.resources.item_model_definition import ModelItemModel, ItemModelType

if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.resources.custom_item import CustomItem
    from pypacks.scripts.repos.all_items import MinecraftItem

# TODO: Support non cubes? Player heads? Custom models?


@dataclass
class CustomItemModelDefinition:
    internal_name: str
    model: "ItemModelType | str" = "item/iron_sword"  # or <namespace>:<model_name>
    hand_animation_on_swap: bool = True  # Whether the down-and-up animation should be played in first-person view when the item stack is changed. (default: true)
    showcase_item: "MinecraftItem | CustomItem | None" = None  # This is if you want it to show up in a debug command (for testing)

    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="items")

    def __post_init__(self) -> None:
        if isinstance(self.model, str):
            self.model = ModelItemModel(self.model)  # pyright: ignore

    def get_reference(self, pack_namespace: str) -> str:
        return f"{pack_namespace}:{self.internal_name}"

    def to_dict(self) -> dict[str, Any]:
        assert isinstance(self.model, ItemModelType)
        return self.model.to_dict() | ({"hand_animation_on_swap": False} if not self.hand_animation_on_swap else {})

    def create_resource_pack_files(self, pack: "Pack") -> None:
        # https://www.discord.com/channels/154777837382008833/1323240917792063489
        # https://minecraft.wiki/w/Items_model_definition
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name, exist_ok=True)

        # Item model definition
        with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(), file, indent=4)

    def generate_give_command(self, pack_namespace: str) -> str:
        from pypacks.resources.custom_item import CustomItem
        from pypacks.additions.reference_book_config import DEV_ITEMS_REF_BOOK_CONFIG
        assert self.showcase_item is not None
        if isinstance(self.showcase_item, CustomItem):
            self.showcase_item.ref_book_config = DEV_ITEMS_REF_BOOK_CONFIG
            self.showcase_item.item_model = self
            return self.showcase_item.generate_give_command(pack_namespace)

        return CustomItem(
            self.internal_name, self.showcase_item, custom_name=self.internal_name,
            item_model=self, ref_book_config=DEV_ITEMS_REF_BOOK_CONFIG
        ).generate_give_command(pack_namespace)


@dataclass
class CustomTexture:
    internal_name: str
    texture_bytes: bytes

    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="textures/item")

    def create_resource_pack_files(self, pack: "Pack") -> None:
        # The resource pack requires 3 things for a custom texture:
        # 1. The model definition/config (in items/<internal_name>.json)
        # 2. The model components, including textures, parent, etc. (in models/item/<internal_name>.json)
        # 3. The texture itself (in textures/item/<internal_name>.png)
        # ├── assets/
        # │   └── <pack namespace>/
        # │       ├── models/
        # │       │   └── item/
        # │       │       └── <internal_name>.json  # Defines the item's appearance in-game
        # │       ├── items/
        # │       │   └── <internal_name>.json      # Defines the item's behavior or properties
        # │       └── textures/
        # │           └── item/
        # │               └── <internal_name>.png   # The texture for the item
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/"models"/"item", exist_ok=True)
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name, exist_ok=True)

        layers = {"layer0": f"{pack.namespace}:item/{self.internal_name}"}
        with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/"models"/"item"/f"{self.internal_name}.json", "w") as file:
            json.dump({"parent": "minecraft:item/generated", "textures": layers}, file, indent=4)

        CustomItemModelDefinition(internal_name=self.internal_name, model=f"{pack.namespace}:item/{self.internal_name}").create_resource_pack_files(pack)

        with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name/f"{self.internal_name}.png", "wb") as file:
            file.write(self.texture_bytes)


@dataclass
class FacePaths:
    """This is used when rendering a simple symmetric block won't work (for now)"""
    # If a face is None, it will use the front texture
    front: str
    back: str | None
    top: str | None
    bottom: str | None
    left: str | None
    right: str | None
    horizontally_rotatable: bool = False
    vertically_rotatable: bool = False

    def __post_init__(self) -> None:
        # IGNORE, OUTDATED: We have 3 options, axial (NESW+Up+Down), cardinal (NESW), and on_axis (north-south, east-west, up-down)
        assert self.front is not None
        if all((x is None) for x in [self.back, self.top, self.bottom, self.left, self.right]):  # If it's just the front face.
            self.block_type = "symmetric_cube"
            return
        if any((x is None) for x in [self.back, self.top, self.bottom, self.left, self.right]):
            raise ValueError("Invalid FacePaths object, must have one of: Front | (Front, Back, Top, Bottom, Left, Right)")
        self.block_type = "asymmetric_cube"


@dataclass
class SymmetricCubeModel:
    """AsymmetricCubeModel is a model that has different textures on each face."""
    internal_name: str
    texture_path: str

    def create_resource_pack_files(self, pack: "Pack") -> None:
        # Requires the following file structure:
        # ├── assets/
        # │   └── <pack namespace>/
        # │       ├── models/
        # │       │   └── item/
        # │       │       └── <internal_name>.json  # Defines the item's appearance in-game
        # │       ├── items/
        # │       │   └── <internal_name>.json      # Defines the item's behavior or properties
        # │       └── textures/
        # │           └── item/
        # │               └── <internal_name>.png   # The texture for the item
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/"models"/"item", exist_ok=True)
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/"textures"/"item", exist_ok=True)

        layers = {"all": f"{pack.namespace}:item/{self.internal_name}"}
        with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/"models"/"item"/f"{self.internal_name}.json", "w") as file:
            json.dump({"parent": "minecraft:block/cube_all", "textures": layers}, file, indent=4)

        # Item model definition
        CustomItemModelDefinition(internal_name=self.internal_name, model=f"{pack.namespace}:item/{self.internal_name}").create_resource_pack_files(pack)

        # Texture
        shutil.copyfile(self.texture_path, Path(pack.resource_pack_path)/"assets"/pack.namespace/"textures"/"item"/f"{self.internal_name}.png")


@dataclass
class AsymmetricCubeModel:
    """AsymmetricCubeModel is a model that has different textures on each face."""
    internal_name: str
    face_paths: "FacePaths"

    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="blockstates")

    def create_resource_pack_files(self, pack: "Pack") -> None:
        # Requires the following file structure:
        # ├── assets/
        # │   └── <pack namespace>/
        # │       ├── blockstates/
        # │       │   └── <custom_block>.json
        # │       ├── models/
        # │       │   └── item/
        # │       │       └── <custom_block>.json
        # │       ├── items/
        # │       │   └── <custom_block>.json
        # │       └── textures/
        # │           └── item/
        # │               └── <custom_block>_<top&bottom&front&back&left&right>.png

        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name, exist_ok=True)
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/"models"/"item", exist_ok=True)
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/"textures"/"item", exist_ok=True)

        with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump({
                "variants": {
                    "": {"model": f"{pack.namespace}:block/{self.internal_name}"},
                }
            }, file, indent=4)

        with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/"models"/"item"/f"{self.internal_name}.json", "w") as file:
            axial_mapping = {
                "up": "top",
                "down": "bottom",
                "north": "front",
                "south": "back",
                "east": "left",
                "west": "right",
            }
            json.dump({
                "parent": "block/cube",
                "textures": {
                    direction: f"{pack.namespace}:item/{self.internal_name}_{face}"
                    for direction, face in axial_mapping.items()
                } | {
                    "particle": f"{pack.namespace}:item/{self.internal_name}_front"  # This just stops errors in the logs
                }
            }, file, indent=4)

        CustomItemModelDefinition(internal_name=self.internal_name, model=f"{pack.namespace}:item/{self.internal_name}").create_resource_pack_files(pack)

        for face in ["top", "bottom", "front", "back", "left", "right"]:
            if getattr(self.face_paths, face) is not None:
                path = Path(pack.resource_pack_path)/"assets"/pack.namespace/"textures"/"item"/f"{self.internal_name}_{face}.png"
                with open(path, "wb") as file:
                    file.write(Path(getattr(self.face_paths, face)).read_bytes())


@dataclass
class SlabModel:
    internal_name: str
    texture_path: str

    def create_resource_pack_files(self, pack: "Pack") -> None:
        # Requires the following file structure:
        # ├── assets/
        # │   └── <namespace>/
        # │       ├── blockstates/
        # │       │   └── <slab_name>.json
        # │       ├── models/
        # │       │   ├── block/
        # │       │   │   ├── <slab_name>.json
        # │       │   │   ├── <slab_name>_top.json
        # │       │   │   └── <slab_name>_bottom.json
        # │       │   └── item/
        # │       │       └── <slab_name>.json
        # │       └── textures/
        # │           └── block/
        # │               ├── <slab_name>_top.png
        # │               ├── <slab_name>_bottom.png
        # │               └── <slab_name>_side.png
        with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/"blockstates"/f"{self.internal_name}_slab.json", "w") as file:
            json.dump({
                # Create the blockstates file, pointing to the 3 different models
                "variants": {
                    "type=bottom": {"model": f"{pack.namespace}:item/{self.internal_name}_slab"},
                    "type=top":    {"model": f"{pack.namespace}:item/{self.internal_name}_slab_top"},
                    "type=double": {"model": f"{pack.namespace}:item/{self.internal_name}"},
                }
            }, file, indent=4)

        for suffix in ["slab", "slab_top"]:
            with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/"models"/"item"/f"{self.internal_name}_{suffix}.json", "w") as file:
                json.dump({
                    "parent": "minecraft:block/slab",
                    "textures": {
                        "bottom": f"{pack.namespace}:item/{self.internal_name}",
                        "side": f"{pack.namespace}:item/{self.internal_name}",
                        "top": f"{pack.namespace}:item/{self.internal_name}",
                    }
                }, file, indent=4)

        CustomItemModelDefinition(internal_name=f"{self.internal_name}_slab", model=f"{pack.namespace}:item/{self.internal_name}_slab").create_resource_pack_files(pack)

    # def add_variants(self, pack: "Pack", stairs: bool = False, slabs: bool = False,) -> None:
        # C:\Users\%USERNAME%\AppData\Roaming\.minecraft\versions\1.21.4\1.21.4\assets\minecraft\models\block
        # Fences are too much work (maybe?)
        # Walls aren't wood, but are also like fences
        # Doors and trapdoors need to flip and that's annoying to do
        # Pressure plates are basically buttons that also need to react
        # Fencegates are doors, so they're out.
        # Boat/boat chest??? Should be able to re-skin an entity?
        # Signs and hanging signs are editable, so probably not them (for now)
