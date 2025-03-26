import os
import json
import shutil
from pathlib import Path
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal

from pypacks.resources.base_resource import BaseResource
from pypacks.resources.item_model_definition import ModelItemModel, ItemModel

if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.resources.custom_item import CustomItem
    from pypacks.scripts.repos.all_items import MinecraftItem

# TODO: Support non cubes? Player heads? Custom models?

# TODO: Add readmes/docstrings to each class in here, sometimes it's confusing... Done but kinda


@dataclass
class CustomItemRenderDefinition(BaseResource):
    # TODO: Flesh this out, there's lots more I haven't covered from:
    # https://minecraft.wiki/w/Model
    # https://www.discord.com/channels/154777837382008833/1323240917792063489
    # https://minecraft.wiki/w/Items_model_definition
    internal_name: str
    model: "ItemModel | str" = "item/iron_sword"  # or <namespace>:<model_name>
    hand_animation_on_swap: bool = True  # Whether the down-and-up animation should be played in first-person view when the item stack is changed. (default: true)
    showcase_item: "MinecraftItem | CustomItem | None" = None  # This is if you want it to show up in a debug command (for testing)

    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="items")

    def __post_init__(self) -> None:
        if isinstance(self.model, str):
            self.model = ModelItemModel(self.model)  # pyright: ignore

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        assert isinstance(self.model, ItemModel)
        return self.model.to_dict() | ({"hand_animation_on_swap": False} if not self.hand_animation_on_swap else {})

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "CustomItemRenderDefinition":
        return cls(
            internal_name,
            model=ItemModel.from_dict(data),
            hand_animation_on_swap=data.get("hand_animation_on_swap", True)
        )

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
class CustomTexture(BaseResource):
    """A simple class which copies the textures from your source to the resource pack."""
    internal_name: str
    path_to_texture: Path | str
    sub_directories: list[str] = field(default_factory=list)

    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="textures")

    def create_resource_pack_files(self, pack: "Pack") -> None:
        path = Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name/Path(*self.sub_directories)
        os.makedirs(path, exist_ok=True)
        shutil.copyfile(self.path_to_texture, path/f"{self.internal_name}.png")

    @classmethod
    def from_resource_pack_files(cls, assets_path: "Path") -> list["CustomTexture"]:
        """Path should be the root of the pack"""
        return [
            cls(file_path.stem, file_path, sub_directories=file_path.parts[len(assets_path.parts)+1:])  # type: ignore[arg-type]
            for file_path in assets_path.glob(f"**/{cls.resource_pack_subdirectory_name}/**/*.png")
            if "textures/font" not in str(file_path)
        ]


@dataclass
class CustomModelDefinition(BaseResource):
    """A class which maps the textures to the model in <namespace>/models/<subdirectories>/<internal_name>.json"""
    internal_name: str
    parent: str = "minecraft:item/generated"
    model_type: Literal["item", "block"] = "item"  # Doesn't dictate where it goes, just the type of model
    sub_directories: list[str] = field(default_factory=list)

    resource_pack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="models")

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        layer_type = "layer0" if "item" in self.parent else "all"
        layers = {layer_type: f"{pack_namespace}:{self.model_type}/{self.internal_name}"}  # TODO: Probably allow a layer *value*
        return {"parent": self.parent, "textures": layers}

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any], sub_directories: list[str]) -> "CustomModelDefinition":  # type: ignore[override]
        return cls(
            internal_name,
            parent=data["parent"],
            model_type="item" if "item" in data["parent"] else "block",
            sub_directories=sub_directories,
        )


@dataclass
class CustomItemTexture(BaseResource):
    """A simple util class which creates the necessary files for a custom item texture (textures, models, render definitions)."""
    internal_name: str
    path_to_texture: Path | str

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
        CustomTexture(self.internal_name, self.path_to_texture, sub_directories=["item"]).create_resource_pack_files(pack)
        CustomModelDefinition(self.internal_name, parent="minecraft:item/generated", model_type="item", sub_directories=["item"]).create_resource_pack_files(pack)
        CustomItemRenderDefinition(internal_name=self.internal_name, model=f"{pack.namespace}:item/{self.internal_name}").create_resource_pack_files(pack)


@dataclass
class FacePaths:
    """This is used when rendering a simple symmetric block won't work"""
    # If a face is None, it will use the front texture
    front: "str | Path"
    back: "str | Path | None"
    top: "str | Path | None"
    bottom: "str | Path | None"
    left: "str | Path | None"
    right: "str | Path | None"
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
    """SymmetricCubeModel is a model that has the same textures for each face."""
    internal_name: str
    texture_path: "str | Path"

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
        CustomModelDefinition(self.internal_name, parent="minecraft:block/cube_all", model_type="item", sub_directories=["item"]).create_resource_pack_files(pack)
        CustomItemRenderDefinition(internal_name=self.internal_name, model=f"{pack.namespace}:item/{self.internal_name}").create_resource_pack_files(pack)
        CustomTexture(self.internal_name, self.texture_path, sub_directories=["item"]).create_resource_pack_files(pack)


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
        # │       ├── items/  (Handled by CustomItemRenderDefinition)
        # │       │   └── <custom_block>.json
        # │       └── textures/ (Handled by CustomTexture)
        # │           └── item/
        # │               └── <custom_block>_<top&bottom&front&back&left&right>.png

        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name, exist_ok=True)  # Blockstates
        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/"models"/"item", exist_ok=True)

        with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/self.__class__.resource_pack_subdirectory_name/f"{self.internal_name}.json", "w", encoding="utf-8") as file:
            json.dump({
                "variants": {
                    "": {"model": f"{pack.namespace}:block/{self.internal_name}"},
                }
            }, file, indent=4)

        with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/"models"/"item"/f"{self.internal_name}.json", "w", encoding="utf-8") as file:
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

        CustomItemRenderDefinition(internal_name=self.internal_name, model=f"{pack.namespace}:item/{self.internal_name}").create_resource_pack_files(pack)

        for face in ["top", "bottom", "front", "back", "left", "right"]:
            if getattr(self.face_paths, face) is not None:
                CustomTexture(f"{self.internal_name}_{face}", getattr(self.face_paths, face), sub_directories=["item"]).create_resource_pack_files(pack)


@dataclass
class SlabModel(BaseResource):
    internal_name: str  # including the "_slab" suffix
    texture_path: "str | Path"

    def create_resource_pack_files(self, pack: "Pack") -> None:
        # Requires the following file structure:
        # ├── assets/
        # │   └── <namespace>/
        # │       ├── blockstates/
        # │       │   └── <slab_name>.json
        # │       ├── items/    (Handled by CustomItemRenderDefinition)
        # │       │   └── <slab_name>.json
        # │       ├── models/
        # │       │   └── item/
        # │       │       ├── <slab_name>.json
        # │       │       └── <slab_name>_top.json
        # │       └── textures/    (Handled by CustomBlock)
        # │           └── block/
        # │               ├── <slab_name>_top.png
        # │               ├── <slab_name>_bottom.png
        # │               └── <slab_name>_side.png

        os.makedirs(Path(pack.resource_pack_path)/"assets"/pack.namespace/"blockstates", exist_ok=True)
        # Blockstates
        with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/"blockstates"/f"{self.internal_name}.json", "w", encoding="utf-8") as file:
            json.dump({
                # Create the blockstates file, pointing to the 3 different models
                "variants": {
                    "type=bottom": {"model": f"{pack.namespace}:item/{self.internal_name}"},
                    "type=top":    {"model": f"{pack.namespace}:item/{self.internal_name}_top"},  # fmt: skip
                    "type=double": {"model": f"{pack.namespace}:item/{self.internal_name.removeprefix('_slab)')}"},
                }
            }, file, indent=4)

        CustomItemRenderDefinition(internal_name=self.internal_name, model=f"{pack.namespace}:item/{self.internal_name}").create_resource_pack_files(pack)

        # Models/Item
        for suffix in ["", "_top"]:
            with open(Path(pack.resource_pack_path)/"assets"/pack.namespace/"models"/"item"/f"{self.internal_name}{suffix}.json", "w", encoding="utf-8") as file:
                json.dump({
                    "parent": "minecraft:block/slab",
                    "textures": {
                        "bottom": f"{pack.namespace}:item/{self.internal_name.removesuffix('_slab')}",  # Point to the regular texture
                        "side": f"{pack.namespace}:item/{self.internal_name.removesuffix('_slab')}",  # Point to the regular texture
                        "top": f"{pack.namespace}:item/{self.internal_name.removesuffix('_slab')}",  # Point to the regular texture
                }
            }, file, indent=4)

    # def add_variants(self, pack: "Pack", stairs: bool = False, slabs: bool = False,) -> None:
        # C:\Users\%USERNAME%\AppData\Roaming\.minecraft\versions\1.21.4\1.21.4\assets\minecraft\models\block
        # Fences are too much work (maybe?)
        # Walls aren't wood, but are also like fences
        # Doors and trapdoors need to flip and that's annoying to do
        # Pressure plates are basically buttons that also need to react
        # Fencegates are doors, so they're out.
        # Boat/boat chest??? Should be able to re-skin an entity?
        # Signs and hanging signs are editable, so probably not them (for now)
