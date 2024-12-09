import os
import json
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from pypacks.book_generator import ReferenceBook
from pypacks.resources.custom_recipe import SmithingTrimRecipe, ALL_RECIPES
from pypacks.resources.custom_font import CustomFont, BookImage
from pypacks.resources.custom_item import CustomItem

if TYPE_CHECKING:
    from .datapack import Datapack

from .utils import IMAGES_PATH
from .image_generation.ref_book_icon_gen import add_centered_overlay


BASE_IMAGES: dict[str, Path] = {x: Path(IMAGES_PATH, "reference_book_icons", f"{x}.png") for x in (
    "empty_1_x_1", "blank_icon",
)}
EXTRA_ICON_BASE_PATH = Path(IMAGES_PATH)/"reference_book_icons"/"extra_icon_base_2.png"


def generate_resource_pack(datapack: "Datapack") -> None:
    # ================================================================================================
    # pack.mcmeta
    with open(Path(datapack.resource_pack_path)/"pack.mcmeta", "w") as file:
        json.dump({"pack": {"pack_format": datapack.resource_pack_format_version, "description": datapack.description}}, file, indent=4)
    # pack.png
    if datapack.pack_icon_path is not None:
        shutil.copyfile(datapack.pack_icon_path, Path(datapack.resource_pack_path)/"pack.png")
    # ================================================================================================
    # All the fonts and images for the reference book
    if datapack.font_mapping:
        datapack.custom_font.create_resource_pack_files(datapack)
    # ================================================================================================
    # Custom item images, model.json, item.json, etc & custom paintings (move files, create folder) & custom sounds (move sound files, create folder)
    for element in datapack.custom_items+datapack.custom_blocks+datapack.custom_paintings+datapack.custom_sounds:
        element.create_resource_pack_files(datapack)
    # ================================================================================================
    # Create the sounds.json file.
    with open(Path(datapack.resource_pack_path, "assets", datapack.namespace, "sounds.json"), "w") as file:
        json.dump({sound.internal_name: sound.create_sound_entry(datapack) for sound in datapack.custom_sounds}, file, indent=4)
    # ================================================================================================

def generate_font_pack(datapack: "Datapack") -> "CustomFont":
    # TODO: Could this move to the reference book generator?
    # https://www.youtube.com/watch?v=i4l2Ym_0VZg   <- Just cool
    # Create the providers file
    all_elements = [
        *[   # BASE IMAGES, Spaces, Empty icon, logo
            BookImage(name=image_name, image_bytes=Path(image_path).read_bytes())
            for image_name, image_path in BASE_IMAGES.items()
        ],
        # Logo (scaled, better resolution)
        BookImage("logo_256_x_256", Path(IMAGES_PATH, "reference_book_icons", "logo_256_x_256.png").read_bytes(), height=100, y_offset=16),
        BookImage("satchel_icon", add_centered_overlay(image_bytes=Path(IMAGES_PATH, "reference_book_icons", "satchel.png").read_bytes()), height=20, y_offset=10),
        BookImage("information_icon", add_centered_overlay(image_bytes=Path(IMAGES_PATH, "reference_book_icons", "information_icon.png").read_bytes(),
                                                           base_image_path=EXTRA_ICON_BASE_PATH, resize_to_16x16=False), height=18, y_offset=14),
        *[  # Category icons
            BookImage(f"{category.internal_name}_category_icon", image_bytes=category.icon_image_bytes)
            for category in datapack.reference_book_categories
        ],
        *[  # Custom items
            BookImage(f"{item.internal_name}_icon", image_bytes=item.icon_image_bytes)
            for item in datapack.custom_items
        ],
        *[  # Custom recipes
            BookImage(f"custom_recipe_for_{custom_recipe.internal_name}_icon", image_bytes=custom_recipe.recipe_image_bytes, y_offset=6)
            for custom_recipe in [x for x in datapack.custom_recipes if not isinstance(x, SmithingTrimRecipe) and isinstance(x.result, CustomItem)]
        ],
        *[  # Custom recipe icons
            BookImage(f"{recipe.recipe_block_name}_icon",
                      image_bytes=add_centered_overlay(image_bytes=Path(IMAGES_PATH, "recipe_icons", f"{recipe.recipe_block_name}.png").read_bytes(),
                                                       base_image_path=EXTRA_ICON_BASE_PATH, resize_to_16x16=False),
                      height=18, y_offset=14)
            for recipe in ALL_RECIPES
        ],
    ]
    return CustomFont("all_fonts", all_elements)

def generate_base_pack(datapack: "Datapack") -> None:
    os.makedirs(Path(datapack.datapack_output_path)/"data"/datapack.namespace, exist_ok=True)
    # ================================================================================================
    # pack.mcmeta
    with open(Path(datapack.datapack_output_path, "pack.mcmeta"), "w") as file:
        json.dump({"pack": {"pack_format": datapack.data_pack_format_version, "description": datapack.description}}, file, indent=4)
    # pack.png
    if datapack.pack_icon_path is not None:
        shutil.copyfile(datapack.pack_icon_path, Path(datapack.datapack_output_path, "pack.png"))
    # ================================================================================================
    # Load + Tick functions
    os.makedirs(Path(datapack.datapack_output_path)/"data"/"minecraft"/"tags"/"function", exist_ok=True)
    with open(Path(datapack.datapack_output_path)/"data"/"minecraft"/"tags"/"function"/"load.json", "w") as file:
        json.dump({"values": [f"{datapack.namespace}:load"]}, file, indent=4)

    with open(Path(datapack.datapack_output_path)/"data"/"minecraft"/"tags"/"function"/"tick.json", "w") as file:
        json.dump({"values": [f"{datapack.namespace}:tick"]}, file, indent=4)
    # ================================================================================================
    # Give commands
    os.makedirs(Path(datapack.datapack_output_path)/"data"/datapack.namespace/"function"/"give", exist_ok=True)

    with open(Path(datapack.datapack_output_path)/"data"/datapack.namespace/"function"/"give_all.mcfunction", "w") as file:
        file.write("\n".join([custom_item.generate_give_command(datapack) for custom_item in datapack.custom_items]))
    # And give the book
    book = ReferenceBook(datapack.custom_items)
    with open(Path(datapack.datapack_output_path)/"data"/datapack.namespace/"function"/"give_reference_book.mcfunction", "w") as file:
        file.write(f"\n# Give the book\n{book.generate_give_command(datapack)}")
    # ================================================================================================
    # Resources
    os.makedirs(Path(datapack.datapack_output_path)/"data"/datapack.namespace/"function"/"right_click", exist_ok=True)

    for item in (
        datapack.custom_items+datapack.custom_recipes+datapack.custom_jukebox_songs+datapack.custom_predicates+
        datapack.custom_paintings+datapack.custom_advancements+datapack.custom_loot_tables+
        datapack.mcfunctions+datapack.custom_tags
    ):
        if item.datapack_subdirectory_name is not None:  # Custom items don't have a subdirectory
            os.makedirs(Path(datapack.datapack_output_path)/"data"/datapack.namespace/item.datapack_subdirectory_name, exist_ok=True)
        if hasattr(item, "sub_directories"):
            os.makedirs(Path(datapack.datapack_output_path, "data", datapack.namespace, item.datapack_subdirectory_name, *item.sub_directories), exist_ok=True)  # type: ignore
        item.create_datapack_files(datapack)

    # Testing command
    # shutil.copyfile(Path(PYPACKS_ROOT)/"scripts"/"setup_testing.mcfunction", Path(datapack.datapack_output_path)/"data"/datapack.namespace/"function"/"setup_testing.mcfunction")
    # ================================================================================================
