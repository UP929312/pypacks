import os
import json
import shutil
from pathlib import Path
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pypacks.datapack import Datapack

# TODO: Support non cubes? Player heads? Custom models?


@dataclass
class ItemModel:
    internal_name: str
    texture_bytes: bytes

    def create_resource_pack_files(self, datapack: "Datapack") -> None:
        # The resource pack requires 3 things:
        # 1. The model definition/config (in items/<internal_name>.json)
        # 2. The model components, including textures, parent, etc. (in models/item/<internal_name>.json)
        # 3. The texture itself (in textures/item/<internal_name>.png)
        os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"models"/"item", exist_ok=True)
        os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"items", exist_ok=True)
        os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"textures"/"item", exist_ok=True)
        os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"textures"/"font", exist_ok=True)

        layers = {"layer0": f"{datapack.namespace}:item/{self.internal_name}"}
        with open(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"models"/"item"/f"{self.internal_name}.json", "w") as file:
            json.dump({"parent": "minecraft:item/generated", "textures": layers}, file, indent=4)

        with open(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"items"/f"{self.internal_name}.json", "w") as file:
            json.dump({"model": {"type": "minecraft:model", "model": f"{datapack.namespace}:item/{self.internal_name}"}}, file, indent=4)

        with open(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"textures"/"item"/f"{self.internal_name}.png", "wb") as file:
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
        if any([(x is None) for x in [self.back, self.top, self.bottom, self.left, self.right]]):
            raise ValueError("Invalid FacePaths object, must have one of: Front | (Front, Back, Top, Bottom, Left, Right)")
        self.block_type = "asymmetric_cube"


@dataclass
class SymmetricCubeModel:
    """AsymmetricCubeModel is a model that has different textures on each face."""
    internal_name: str
    texture_path: str

    def create_resource_pack_files(self, datapack: "Datapack") -> None:
        # Requires the following file structure:
        # ├── assets/
        # │   └── <datapack namespace>/
        # │       ├── models/
        # │       │   └── item/
        # │       │       └── <internal_name>.json  # Defines the item's appearance in-game
        # │       ├── items/
        # │       │   └── <internal_name>.json      # Defines the item's behavior or properties
        # │       └── textures/
        # │           └── item/
        # │               └── <internal_name>.png   # The texture for the item
        os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"models"/"item", exist_ok=True)
        os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"items", exist_ok=True)
        os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"textures"/"item", exist_ok=True)

        layers = {"all": f"{datapack.namespace}:item/{self.internal_name}"}
        with open(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"models"/"item"/f"{self.internal_name}.json", "w") as file:
            json.dump({"parent": "minecraft:block/cube_all", "textures": layers}, file, indent=4)

        # Item model definition
        with open(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"items"/f"{self.internal_name}.json", "w") as file:
            json.dump({"model": {"type": "minecraft:model", "model": f"{datapack.namespace}:item/{self.internal_name}"}}, file, indent=4)

        shutil.copyfile(self.texture_path, Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"textures"/"item"/f"{self.internal_name}.png")


@dataclass
class AsymmetricCubeModel:
    """AsymmetricCubeModel is a model that has different textures on each face."""
    internal_name: str
    face_paths: "FacePaths"

    def create_resource_pack_files(self, datapack: "Datapack") -> None:
        # Requires the following file structure:
        # ├── assets/
        # │   └── <datapack namespace>/
        # │       ├── blockstates/
        # │       │   └── <custom_block>.json
        # │       ├── models/
        # │       │   └── item/
        # │       │       └── <custom_block>.json
        # │       ├── items/
        # │       │   └── <custom_block>.json
        # │       └── textures/
        # │           └── item/
        # │               └── <custom_block>_<top&bottom&front&back&left&right.png

        os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"blockstates", exist_ok=True)
        os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"models"/"item", exist_ok=True)
        os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"items", exist_ok=True)
        os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"textures"/"item", exist_ok=True)

        with open(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"blockstates"/f"{self.internal_name}.json", "w") as file:
            json.dump({
                "variants": {
                    "": {"model": f"{datapack.namespace}:block/{self.internal_name}"},
                }
            }, file, indent=4)

        with open(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"models"/"item"/f"{self.internal_name}.json", "w") as file:
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
                    direction: f"{datapack.namespace}:item/{self.internal_name}_{face}"
                    for direction, face in axial_mapping.items()
                } | {
                    "particle": f"{datapack.namespace}:item/{self.internal_name}_front"  # This just stops errors in the logs
                }
            }, file, indent=4)

        with open(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"items"/f"{self.internal_name}.json", "w") as file:
            json.dump({"model": {"type": "minecraft:model", "model": f"{datapack.namespace}:item/{self.internal_name}"}}, file, indent=4)

        for face in ["top", "bottom", "front", "back", "left", "right"]:
            if getattr(self.face_paths, face) is not None:
                path = Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"textures"/"item"/f"{self.internal_name}_{face}.png"
                with open(path, "wb") as file:
                    file.write(Path(getattr(self.face_paths, face)).read_bytes())


@dataclass
class SlabModel:
    internal_name: str
    texture_path: str

    def create_resource_pack_files(self, datapack: "Datapack") -> None:
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
        with open(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"blockstates"/f"{self.internal_name}_slab.json", "w") as file:
            json.dump({
                # Create the blockstates file, pointing to the 3 different models
                "variants": {
                    "type=bottom": {"model": f"{datapack.namespace}:item/{self.internal_name}_slab"},
                    "type=top":    {"model": f"{datapack.namespace}:item/{self.internal_name}_slab_top"},
                    "type=double": {"model": f"{datapack.namespace}:item/{self.internal_name}"},
                    # "type=double": {"model": f"{datapack.namespace}:item/{self.internal_name}_slab"},
                }
            }, file, indent=4)

        for suffix in ["slab", "slab_top"]:
            with open(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"models"/"item"/f"{self.internal_name}_{suffix}.json", "w") as file:
                json.dump({
                    "parent": "minecraft:block/slab",
                    "textures": {
                        "bottom": f"{datapack.namespace}:item/{self.internal_name}",
                        "side": f"{datapack.namespace}:item/{self.internal_name}",
                        "top": f"{datapack.namespace}:item/{self.internal_name}",
                    }
                }, file, indent=4)

        with open(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"items"/f"{self.internal_name}_slab.json", "w") as file:
            json.dump({"model": {"type": "minecraft:model", "model": f"{datapack.namespace}:item/{self.internal_name}_slab"}}, file, indent=4)

    # def add_variants(self, datapack: "Datapack", stairs: bool = False, slabs: bool = False,) -> None:
        # C:\Users\%USERNAME%\AppData\Roaming\.minecraft\versions\1.21.4\1.21.4\assets\minecraft\models\block
        # Fences are too much work (maybe?)
        # Walls aren't wood, but are also like fences
        # Doors and trapdoors need to flip and that's annoying to do
        # Pressure plates are basically buttons that also need to react
        # Fencegates are doors, so they're out.
        # Boat/boat chest??? Should be able to re-skin an entity?
        # Signs and hanging signs are editable, so probably not them (for now)


# @dataclass
# class CustomItemModel:
#     model: str = "item/iron_sword"

#     def create_resource_pack_files(self, datapack: "Datapack") -> None:
#         # https://www.discord.com/channels/154777837382008833/1323240917792063489
#         # https://minecraft.wiki/w/Items_model_definition
#         data = {
#             "model": {
#                 "type": "model",
#                 "model": self.model,  # "item/iron_sword"
#                 "tints": [
#                     {
#                         "type": "dye",
#                         "default": -1
#                     }
#                 ]
#             }
#         }

# ====================================================================================================================
# Glints
