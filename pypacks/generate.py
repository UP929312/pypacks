import os
import json
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from pypacks.reference_book_generator import ReferenceBook
from pypacks.resources.custom_recipe import SmithingTrimRecipe, ALL_RECIPES
from pypacks.resources.custom_font import CustomFont, FontImage
from pypacks.resources.custom_item import CustomItem
from .utils import IMAGES_PATH
from .image_manipulation.ref_book_icon_gen import add_centered_overlay

if TYPE_CHECKING:
    from .datapack import Datapack


EXTRA_ICON_BASE_PATH = Path(IMAGES_PATH)/"reference_book_icons"/"extra_icon_base.png"


def generate_resource_pack(datapack: "Datapack") -> None:
    os.makedirs(datapack.resource_pack_path, exist_ok=True)
    # ================================================================================================
    # pack.mcmeta
    with open(Path(datapack.resource_pack_path)/"pack.mcmeta", "w") as file:
        json.dump({"pack": {"pack_format": datapack.resource_pack_format_version, "description": datapack.description}}, file, indent=4)
    # pack.png
    if datapack.pack_icon_path is not None:
        shutil.copyfile(datapack.pack_icon_path, Path(datapack.resource_pack_path)/"pack.png")
    # ================================================================================================
    # Custom item images, model.json, item.json, etc & custom paintings (move files, create folder) & custom sounds (move sound files, create folder) & custom font (built in)
    for element in datapack.custom_items+datapack.custom_blocks+datapack.custom_paintings+datapack.custom_sounds+datapack.custom_fonts:
        element.create_resource_pack_files(datapack)
    # ================================================================================================
    # Create the sounds.json file.
    if datapack.custom_sounds:
        with open(Path(datapack.resource_pack_path, "assets", datapack.namespace, "sounds.json"), "w") as file:
            json.dump({sound.internal_name: sound.create_sound_entry(datapack) for sound in datapack.custom_sounds}, file, indent=4)
    # ================================================================================================


def generate_font_pack(datapack: "Datapack") -> "CustomFont":
    # TODO: Could this move to the reference book generator?
    # https://www.youtube.com/watch?v=i4l2Ym_0VZg   <- Just cool
    # Create the providers file
    all_elements = [
        FontImage("empty_1_x_1", Path(IMAGES_PATH, "reference_book_icons", "empty_1_x_1.png").read_bytes()),
        FontImage("blank_icon", Path(IMAGES_PATH, "reference_book_icons", "blank_icon.png").read_bytes()),
        FontImage("logo_256_x_256", Path(IMAGES_PATH, "reference_book_icons", "logo_256_x_256.png").read_bytes(), height=100, y_offset=16),
        FontImage("information_icon", add_centered_overlay(image_bytes=Path(IMAGES_PATH, "reference_book_icons", "information_icon.png").read_bytes(),
                                                           base_image_path=EXTRA_ICON_BASE_PATH, resize_to_16x16=False), height=18, y_offset=14),
        FontImage("satchel_icon", add_centered_overlay(image_bytes=Path(IMAGES_PATH, "reference_book_icons", "satchel.png").read_bytes()), height=20, y_offset=10),
        *[  # Category icons
            FontImage(f"{category.internal_name}_category_icon", image_bytes=add_centered_overlay(Path(category.image_path).read_bytes()))
            for category in datapack.reference_book_categories
        ],
        *[  # Custom items
            FontImage(f"{item.internal_name}_icon", image_bytes=add_centered_overlay(item.image_bytes))
            for item in datapack.custom_items
        ],
        *[  # Custom recipes
            FontImage(f"custom_recipe_for_{custom_recipe.internal_name}_icon", image_bytes=custom_recipe.recipe_image_bytes, y_offset=6)
            for custom_recipe in [x for x in datapack.custom_recipes if not isinstance(x, SmithingTrimRecipe) and isinstance(x.result, CustomItem)]
        ],
        *[  # Custom recipe icons
            FontImage(f"{recipe.recipe_block_name}_icon",
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

    if datapack.custom_blocks:
        with open(Path(datapack.datapack_output_path)/"data"/"minecraft"/"tags"/"function"/"tick.json", "w") as file:
            json.dump({"values": [f"{datapack.namespace}:tick"]}, file, indent=4)
    # ================================================================================================
    # Give commands
    if datapack.custom_items:
        os.makedirs(Path(datapack.datapack_output_path)/"data"/datapack.namespace/"function"/"give", exist_ok=True)

        with open(Path(datapack.datapack_output_path)/"data"/datapack.namespace/"function"/"give_all.mcfunction", "w") as file:
            file.write("\n".join([custom_item.generate_give_command(datapack) for custom_item in datapack.custom_items]))
        # And give the book
        book = ReferenceBook(datapack.custom_items)
        with open(Path(datapack.datapack_output_path)/"data"/datapack.namespace/"function"/"give_reference_book.mcfunction", "w") as file:
            file.write(f"\n# Give the book\n{book.generate_give_command(datapack)}")
    # ================================================================================================
    # Resources
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
