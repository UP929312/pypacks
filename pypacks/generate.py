import os
import json
import shutil
from typing import TYPE_CHECKING

from pypacks.book_generator import ReferenceBook
from pypacks.resources.custom_font import CustomFont, BookImage

if TYPE_CHECKING:
    from .datapack import Datapack

from .utils import PYPACKS_ROOT, inline_open
from .image_generation import add_icon_to_base


BASE_IMAGES: dict[str, bytes] = {x: inline_open(f"{PYPACKS_ROOT}/assets/images/{x}.png", "rb") for x in (  # TODO: os.pathlib.join
    "empty_16_x_16", "empty_8_x_8", "empty_4_x_4", "empty_2_x_2", "empty_1_x_1", "icon_base", "logo",
)}
ref_book_items = [f"{PYPACKS_ROOT}/assets/images/satchel.png"]


def generate_resource_pack(datapack: "Datapack") -> None:
    os.makedirs(os.path.join(datapack.resource_pack_path, "assets", datapack.namespace, "items"), exist_ok=True)
    os.makedirs(os.path.join(datapack.resource_pack_path, "assets", datapack.namespace, "font"), exist_ok=True)
    os.makedirs(os.path.join(datapack.resource_pack_path, "assets", datapack.namespace, "sounds"), exist_ok=True)
    os.makedirs(os.path.join(datapack.resource_pack_path, "assets", datapack.namespace, "models", "item"), exist_ok=True)
    os.makedirs(os.path.join(datapack.resource_pack_path, "assets", datapack.namespace, "textures", "item"), exist_ok=True)
    os.makedirs(os.path.join(datapack.resource_pack_path, "assets", datapack.namespace, "textures", "font"), exist_ok=True)
    os.makedirs(os.path.join(datapack.resource_pack_path, "assets", datapack.namespace, "textures", "painting"), exist_ok=True)

    # ================================================================================================

    # pack.mcmeta
    with open(f"{datapack.resource_pack_path}/pack.mcmeta", "w") as file:
        json.dump({"pack": {"pack_format": datapack.resource_pack_format_version, "description": datapack.description}}, file, indent=4)

    # pack.png
    if datapack.pack_icon_path is not None:
        with open(datapack.pack_icon_path, "rb") as file:
            image_contents = file.read()
        with open(f"{datapack.resource_pack_path}/pack.png", "wb") as file:
            file.write(image_contents)

    # ================================================================================================
    # Custom item images, model.json, item.json, etc
    for custom_item in datapack.custom_items:
        custom_item.create_resource_pack_files(datapack)
    # ================================================================================================
    # Copy from file_location to the resource pack
    for category in datapack.reference_book_categories:
        # Copy & generate the icon, too
        with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/font/{category.name.lower()}_category_icon.png", "wb") as file:
            file.write(add_icon_to_base(image_path=category.image_path))

    # Custom back button:
    with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/font/satchel_icon.png", "wb") as file:
        file.write(add_icon_to_base(image_path=f"{PYPACKS_ROOT}/assets/images/satchel.png"))
    # ================================================================================================
    # Copy over the base images to the resource pack (icons, spacers, etc)
    for image in BASE_IMAGES.keys():
        image_name = image.split("/")[-1].removesuffix(".png")
        shutil.copyfile(f"{PYPACKS_ROOT}/assets/images/{image}.png", f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/font/{image_name}.png")

    # Paintings
    for painting in datapack.custom_paintings:
        shutil.copyfile(painting.image_path, f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/painting/{painting.internal_name}.png")

    # Default assets
    for asset in os.listdir(f"{PYPACKS_ROOT}/assets/images/blocks"):
        shutil.copyfile(f"{PYPACKS_ROOT}/assets/images/blocks/{asset}", f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/{asset}")
    for asset in os.listdir(f"{PYPACKS_ROOT}/assets/images/recipes"):
        shutil.copyfile(f"{PYPACKS_ROOT}/assets/images/recipes/{asset}", f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/{asset}")

    # Annoyingly putting this here manually:
    shutil.copyfile(f"{PYPACKS_ROOT}/assets/images/logo_256_x_256.png", f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/font/logo_256_x_256.png")

    # ================================================================================================
    # Sounds
    for sound in datapack.custom_sounds:
        shutil.copyfile(sound.ogg_path, f"{datapack.resource_pack_path}/assets/{datapack.namespace}/sounds/{sound.internal_name}.ogg")

    # Create the sounds.json file.
    with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/sounds.json", "w") as file:
        json.dump({sound.internal_name: sound.create_sound_entry(datapack) for sound in datapack.custom_sounds}, file, indent=4)
    # ================================================================================================
    # Custom Blocks
    # for custom_block in datapack.custom_blocks:
    #     custom_block.create_resource_pack_files(datapack)

def generate_font_pack(datapack: "Datapack") -> dict[str, str]:
    # TODO: Could this move to the reference book generator?
    # https://www.youtube.com/watch?v=i4l2Ym_0VZg   <- Just cool
    # Create the providers file
    all_elements = [
        *[   # BASE IMAGES, Spaces, Empty icon, logo
            BookImage(name=image_name, image_bytes=image_bytes)
            for image_name, image_bytes in BASE_IMAGES.items()
        ],
        *[  # Custom items
            BookImage(f"{item.internal_name}_icon", image_bytes=item.icon_image_bytes)
            for item in datapack.custom_items
        ],
        *[  # Satchel, not much else
            BookImage(icon_path.split("/")[-1].removesuffix(".png")+"_icon", image_bytes=inline_open(icon_path), height=20, y_offset=10)
            for icon_path in ref_book_items
        ],
        *[  # Category icons
            BookImage(f"{category.name.lower()}_category_icon", image_bytes=category.icon_image_bytes)  # type: ignore[arg-type]
            for category in datapack.reference_book_categories
        ],
        *[  # Logo (scaled, better resolution)
            BookImage(image_name, image_bytes, height=100, y_offset=16)
            for image_name, image_bytes in [("logo_256_x_256", inline_open(f"{PYPACKS_ROOT}/assets/images/logo_256_x_256.png")),]
        ],
    ]

    custom_font = CustomFont("all_fonts", all_elements)
    custom_font.create_resource_pack_files(datapack)
    return custom_font.font_mapping

def generate_base_pack(datapack: "Datapack") -> None:
    os.makedirs(os.path.join(datapack.datapack_output_path), exist_ok=True)
    # ================================================================================================
    # pack.mcmeta
    with open(f"{datapack.datapack_output_path}/pack.mcmeta", "w") as file:
        json.dump({"pack": {"pack_format": datapack.data_pack_format_version, "description": datapack.description}}, file, indent=4)

    # pack.png
    if datapack.pack_icon_path is not None:
        shutil.copyfile(datapack.pack_icon_path, f"{datapack.datapack_output_path}/pack.png")
    # ================================================================================================
    # Load + Tick functions

    # Make the load and tick functions
    os.makedirs(os.path.join(datapack.datapack_output_path, "data", "minecraft", "tags", "function"), exist_ok=True)  # makes /data/minecraft/tags/function
    with open(f"{datapack.datapack_output_path}/data/minecraft/tags/function/load.json", "w") as file:
        json.dump({"values": [f"{datapack.namespace}:load"]}, file, indent=4)

    with open(f"{datapack.datapack_output_path}/data/minecraft/tags/function/tick.json", "w") as file:
        json.dump({"values": [f"{datapack.namespace}:tick"]}, file, indent=4)
    # ================================================================================================
    # Give commands
    os.makedirs(os.path.join(datapack.datapack_output_path, "data", datapack.namespace, "function", "give"), exist_ok=True)  # makes /data/{datapack_name}/function/give

    with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/function/give_all.mcfunction", "w") as file:
        file.write("\n".join([custom_item.generate_give_command(datapack) for custom_item in datapack.custom_items]))
    # And give the book
    book = ReferenceBook(datapack.custom_items)
    with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/function/give_reference_book.mcfunction", "w") as file:
        file.write(f"\n# Give the book\n{book.generate_give_command(datapack)}")
    # ================================================================================================
    # Resources
    os.makedirs(os.path.join(datapack.datapack_output_path, "data", datapack.namespace, "function", "right_click"), exist_ok=True)

    for item in (
        datapack.custom_items+datapack.custom_recipes+datapack.custom_jukebox_songs+datapack.custom_predicates+
        datapack.custom_paintings+datapack.custom_advancements+datapack.custom_loot_tables+
        datapack.mcfunctions+datapack.custom_tags
    ):
        if item.datapack_subdirectory_name is not None:  # Custom items don't have a subdirectory
            os.makedirs(os.path.join(datapack.datapack_output_path, "data", datapack.namespace, item.datapack_subdirectory_name), exist_ok=True)
        if hasattr(item, "sub_directories"):
            os.makedirs(os.path.join(datapack.datapack_output_path, "data", datapack.namespace, item.datapack_subdirectory_name, *item.sub_directories), exist_ok=True)  # type: ignore
        item.datapack_subdirectory_name
        item.create_datapack_files(datapack)

    # Testing command
    # shutil.copyfile(f"{PYPACKS_ROOT}/scripts/setup_testing.mcfunction", f"{datapack.datapack_output_path}/data/{datapack.namespace}/function/setup_testing.mcfunction")
    # ================================================================================================