import os
import json
import shutil
from pathlib import Path
from typing import TYPE_CHECKING

from pypacks.additions.reference_book_generator import ReferenceBook
from pypacks.resources.custom_recipe import SmithingTrimRecipe, ALL_RECIPES_TYPES
from pypacks.resources.custom_font import CustomFont, BitMapFontChar, SpaceFontChar
from pypacks.resources.custom_item import CustomItem
from pypacks.utils import IMAGES_PATH
from pypacks.image_manipulation.border_generation import add_border

if TYPE_CHECKING:
    from pypacks.pack import Pack


EXTRA_ICON_BASE_PATH = Path(IMAGES_PATH)/"reference_book_icons"/"extra_icon_base.png"


def generate_resource_pack(pack: "Pack") -> None:
    os.makedirs(pack.resource_pack_path, exist_ok=True)
    assert isinstance(pack.resource_pack_path, Path)
    # ================================================================================================
    # pack.mcmeta
    with open(pack.resource_pack_path/"pack.mcmeta", "w") as file:
        json.dump({"pack": {"pack_format": pack.resource_pack_format_version, "description": pack.description}}, file, indent=4)
    # pack.png
    if pack.pack_icon_path is not None:
        shutil.copyfile(pack.pack_icon_path, pack.resource_pack_path/"pack.png")
    # ================================================================================================
    # Custom item images, model.json, item.json, etc & custom paintings (move files, create folder) & custom sounds (move sound files, create folder) & custom font (built in)
    for element in (
        pack.custom_items + pack.custom_blocks + pack.custom_paintings + pack.custom_sounds + pack.custom_fonts + pack.custom_languages +
        pack.custom_entity_variants + pack.custom_item_render_definitions + pack.custom_model_definitions + pack.custom_textures
    ):
        element.create_resource_pack_files(pack)
    # ================================================================================================
    # Create the sounds.json file.
    if pack.custom_sounds:
        with open(pack.resource_pack_path/"assets"/pack.namespace/"sounds.json", "w") as file:
            json.dump({sound.internal_name: sound.create_sound_entry(pack.namespace) for sound in pack.custom_sounds}, file, indent=4)
    # ================================================================================================


def generate_base_font(pack: "Pack") -> "CustomFont":
    # TODO: Could this move to the reference book generator?
    # https://www.youtube.com/watch?v=i4l2Ym_0VZg   <- Just cool
    # Create the providers file
    all_elements = [
        SpaceFontChar("1_pixel_indent", width=1),
        BitMapFontChar("blank_icon", Path(IMAGES_PATH, "reference_book_icons", "blank_icon.png").read_bytes()),
        BitMapFontChar("logo_256_x_256", Path(IMAGES_PATH, "reference_book_icons", "logo_256_x_256.png").read_bytes(), height=100, y_offset=16),
        BitMapFontChar("information_icon", add_border(image_bytes=Path(IMAGES_PATH, "reference_book_icons", "information_icon.png").read_bytes(),
                                                      base_image_path=EXTRA_ICON_BASE_PATH), height=18, y_offset=14),
        (
            BitMapFontChar("play_icon", add_border(image_bytes=Path(IMAGES_PATH, "reference_book_icons", "play_icon.png").read_bytes(),
                                                   base_image_path=EXTRA_ICON_BASE_PATH), height=18, y_offset=14)
            if [x for x in pack.custom_items
                if hasattr(x, "components") and hasattr(x.components, "instrument") and x.components.instrument is not None]
            else None
        ),
        BitMapFontChar("satchel_icon", add_border(image_bytes=Path(IMAGES_PATH, "reference_book_icons", "satchel.png").read_bytes()), height=20, y_offset=10),
        *[  # Category icons
            BitMapFontChar(f"{category.internal_name}_category_icon", image_bytes=add_border(Path(category.image_path).read_bytes()), height=20, y_offset=10)
            for category in pack.reference_book_categories
        ],
        *[  # Custom items
            BitMapFontChar(f"{item.internal_name}_icon", image_bytes=add_border(Path(item.path).read_bytes()), height=20, y_offset=10)
            for item in pack.custom_items
        ],
        *[  # Custom recipes
            BitMapFontChar(f"custom_recipe_for_{custom_recipe.internal_name}_icon", image_bytes=custom_recipe.generate_recipe_image(), y_offset=6)
            for custom_recipe in [x for x in pack.custom_recipes if not isinstance(x, SmithingTrimRecipe) and isinstance(x.result, CustomItem)]
        ],
        *[  # Custom recipe icons
            BitMapFontChar(
                f"{recipe.recipe_block_name}_icon",
                image_bytes=add_border(image_bytes=Path(IMAGES_PATH, "recipe_icons", f"{recipe.recipe_block_name}.png").read_bytes(),
                                       base_image_path=EXTRA_ICON_BASE_PATH),
                height=18, y_offset=14,
            )
            for recipe in [recipe for recipe in ALL_RECIPES_TYPES if recipe in [type(x) for x in pack.custom_recipes]]  # type: ignore[comparison-overlap]
        ],
    ]
    return CustomFont("all_fonts", [x for x in all_elements if x is not None])   # type: ignore[misc]


def generate_datapack(pack: "Pack") -> None:
    assert isinstance(pack.datapack_output_path, Path)
    os.makedirs(pack.datapack_output_path/"data"/pack.namespace, exist_ok=True)
    # ================================================================================================
    # pack.mcmeta
    with open(pack.datapack_output_path/"pack.mcmeta", "w") as file:
        json.dump({"id": pack.namespace, "pack": {"pack_format": pack.data_pack_format_version, "description": pack.description}}, file, indent=4)
    # pack.png
    if pack.pack_icon_path is not None:
        shutil.copyfile(pack.pack_icon_path, pack.datapack_output_path/"pack.png")
    # ================================================================================================
    # Give commands
    if pack.custom_items:
        os.makedirs(pack.datapack_output_path/"data"/pack.namespace/"function"/"give", exist_ok=True)
        with open(pack.datapack_output_path/"data"/pack.namespace/"function"/"give_all.mcfunction", "w") as file:
            file.write("\n".join([custom_item.generate_give_command(pack.namespace) for custom_item in pack.custom_items]))
        # And give the book
        if pack.config.generate_reference_book:
            ReferenceBook(pack.custom_items).create_datapack_files(pack)

    if pack.config.generate_reference_book and pack.custom_fonts:
        from pypacks.additions.font_tester import FontTestingBook
        FontTestingBook().create_datapack_files(pack)

    # ================================================================================================
    # Resources
    for item in (
        pack.custom_items + pack.custom_recipes + pack.custom_jukebox_songs + pack.custom_predicates +
        pack.custom_paintings + pack.custom_advancements + pack.custom_loot_tables +
        pack.custom_mcfunctions + pack.custom_tags + pack.custom_enchantments + pack.custom_damage_types +
        pack.custom_dimensions + pack.custom_structures + pack.custom_structure_sets + pack.custom_raycasts +
        pack.custom_loops + pack.custom_chunk_scanners + pack.custom_ore_generations + pack.custom_entity_variants +
        pack.custom_test_environments + pack.custom_game_tests
    ):
        if item.datapack_subdirectory_name is not None:  # Custom items don't have a subdirectory
            os.makedirs(pack.datapack_output_path/"data"/pack.namespace/item.datapack_subdirectory_name, exist_ok=True)
        if hasattr(item, "sub_directories"):
            os.makedirs(Path(pack.datapack_output_path, "data", pack.namespace, item.datapack_subdirectory_name, *item.sub_directories), exist_ok=True)  # pyright: ignore
        item.create_datapack_files(pack)

    # Testing command
    # shutil.copyfile(Path(PYPACKS_ROOT)/"scripts"/"setup_testing.mcfunction", Path(datapack.datapack_output_path)/"data"/datapack.namespace/"function"/"setup_testing.mcfunction")
    # ================================================================================================
