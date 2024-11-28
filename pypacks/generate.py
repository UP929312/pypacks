import os
import json
import shutil
from typing import TYPE_CHECKING

from pypacks.book_generator import ReferenceBook

if TYPE_CHECKING:
    from .datapack import Datapack

from .utils import PYPACKS_ROOT, get_png_dimensions
from .image_generation import add_icon_to_base


BASE_IMAGES = [f"{PYPACKS_ROOT}/assets/images/{x}.png" for x in (  # TODO: os.pathlib.join
    "empty_16_x_16", "empty_8_x_8", "empty_4_x_4", "empty_2_x_2", "empty_1_x_1", "icon_base", "logo", # "logo_512_x_512",
)]

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
    for image in BASE_IMAGES:
        image_name = image.split("/")[-1].removesuffix(".png")
        shutil.copyfile(image, f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/font/{image_name}.png")

    # Paintings
    for painting in datapack.custom_paintings:
        shutil.copyfile(painting.image_path, f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/painting/{painting.internal_name}.png")

    # Default assets
    for asset in os.listdir(f"{PYPACKS_ROOT}/assets/images/blocks"):
        shutil.copyfile(f"{PYPACKS_ROOT}/assets/images/blocks/{asset}", f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/{asset}")
    for asset in os.listdir(f"{PYPACKS_ROOT}/assets/images/recipes"):
        shutil.copyfile(f"{PYPACKS_ROOT}/assets/images/recipes/{asset}", f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/{asset}")

    # ================================================================================================
    # Sounds
    for sound in datapack.custom_sounds:
        shutil.copyfile(sound.ogg_path, f"{datapack.resource_pack_path}/assets/{datapack.namespace}/sounds/{sound.internal_name}.ogg")

    # Create the sounds.json file.
    with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/sounds.json", "w") as file:
        json.dump({sound.internal_name: sound.create_sound_entry(datapack) for sound in datapack.custom_sounds}, file, indent=4)
    # ================================================================================================
    # Custom Blocks
    for custom_block in datapack.custom_blocks:
        custom_block.create_resource_pack_files(datapack)


def generate_font_pack(datapack: "Datapack") -> None:
    # Create the providers file & mapping
    chars = [f"\\uE{i:03}" for i in range(0, 100)]  # Generate \uE000 - \uE999
    mapping = {}
    providers = []
    ref_book_items = [f"{PYPACKS_ROOT}/assets/images/satchel.png"]
    BASE_IMAGE_COUNT, CUSTOM_ITEM_COUNT, CUSTOM_REF_BOOK_ICONS, CATEGORY_COUNT = len(BASE_IMAGES), len(datapack.custom_items), len(ref_book_items), len(datapack.reference_book_categories)
    # TODO: Clean this up, so many loops.

    # Create the fonts for all the base images
    for i, image in enumerate(BASE_IMAGES):
        image_name = image.split("/")[-1].removesuffix(".png")
        mapping[image_name] = chars[i]
        height = get_png_dimensions(image)[1]
        provider = {"type": "bitmap", "file": f"{datapack.namespace}:font/{image_name}.png", "height": height, "ascent": min(height//2, 16), "chars": [chars[i]]}
        providers.append(provider)
    # Create the fonts for all the custom items
    for i, item in enumerate(datapack.custom_items, BASE_IMAGE_COUNT):
        mapping[f"{item.internal_name}_icon"] = chars[i]
        height = get_png_dimensions(image_bytes=item.icon_image_bytes)[1]
        provider = {"type": "bitmap", "file": f"{datapack.namespace}:font/{item.internal_name}_icon.png", "height": height, "ascent": min(height//2, 16), "chars": [chars[i]]}
        providers.append(provider)
    # Create custom buttons
    for i, icon_path in enumerate(ref_book_items, BASE_IMAGE_COUNT+CUSTOM_ITEM_COUNT):
        icon_name = icon_path.split("/")[-1].removesuffix(".png")
        mapping[f"{icon_name}_icon"] = chars[i]
        height = 20  # get_png_dimensions(image_path=icon_path)[1]
        provider = {"type": "bitmap", "file": f"{datapack.namespace}:font/{icon_name}_icon.png", "height": height, "ascent": min(height//2, 16), "chars": [chars[i]]}
        providers.append(provider)
    # Create the fonts for all the category icons
    for i, category in enumerate(datapack.reference_book_categories, BASE_IMAGE_COUNT+CUSTOM_ITEM_COUNT+CUSTOM_REF_BOOK_ICONS):
        mapping[category.name.lower()+"_category_icon"] = chars[i]
        height = get_png_dimensions(image_bytes=category.icon_image_bytes)[1]
        provider = {"type": "bitmap", "file": f"{datapack.namespace}:font/{category.name.lower()}_category_icon.png", "height": height, "ascent": min(height//2, 16), "chars": [chars[i]]}
        providers.append(provider)
    # for i, image_name in enumerate(["logo_512_x_512"], BASE_IMAGE_COUNT+CUSTOM_ITEM_COUNT+CUSTOM_REF_BOOK_ICONS+CATEGORY_COUNT):
    #     mapping[image_name] = chars[i]
    #     height = 100
    #     provider = {"type": "bitmap", "file": f"{datapack.namespace}:font/{image_name}.png", "height": height, "ascent": min(height//2, 16), "chars": [chars[i]]}
    #     providers.append(provider)

    # https://www.youtube.com/watch?v=i4l2Ym_0VZg   <- Just cool
    with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/font/all_fonts.json", "w") as file:
        file.write(json.dumps({"providers": providers}, indent=4).replace("\\\\", "\\"))  # Replace double backslashes with single backslashes
    datapack.font_mapping = mapping


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

    # with open(f"{datapack.datapack_output_path}/data/minecraft/tags/function/tick.json", "w") as file:
    #     json.dump({"values": [f"{datapack.namespace}:tick"]}, file, indent=4)
    # ================================================================================================
    # Give commands
    os.makedirs(os.path.join(datapack.datapack_output_path, "data", datapack.namespace, "function", "give"), exist_ok=True)  # makes /data/{datapack_name}/function/give

    # Add to give all command
    all_items = datapack.custom_items + datapack.custom_paintings + datapack.custom_jukebox_songs
    with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/function/give_all.mcfunction", "w") as file:
        file.write("\n".join([custom_item.generate_give_command(datapack) for custom_item in all_items]))
    # And give the book
    book = ReferenceBook(datapack.custom_items)
    with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/function/give_reference_book.mcfunction", "w") as file:
        file.write(f"\n# Give the book\n{book.generate_give_command(datapack)}")
    # ================================================================================================
    # Resources
    os.makedirs(os.path.join(datapack.datapack_output_path, "data", datapack.namespace, "function", "right_click"), exist_ok=True)

    for item in (
        datapack.custom_items+datapack.custom_recipes+datapack.custom_jukebox_songs+datapack.custom_predicates+
        datapack.custom_paintings+datapack.custom_advancements+datapack.custom_loot_tables
    ):
        if item.datapack_subdirectory_name is not None:  # Custom items don't have a subdirectory
            os.makedirs(os.path.join(datapack.datapack_output_path, "data", datapack.namespace, item.datapack_subdirectory_name), exist_ok=True)
        item.datapack_subdirectory_name
        item.create_datapack_files(datapack)

    os.makedirs(os.path.join(datapack.datapack_output_path, "data", datapack.namespace, "custom_blocks"), exist_ok=True)
    for custom_block in datapack.custom_blocks:
        # f"execute as @e[type=item_display, tag={datapack.namespace}.custom_block, predicate=!{namespace}:check_vanilla_blocks] at @s run function {datapack.namespace}:custom_blocks/destroy"
        os.makedirs(os.path.join(datapack.datapack_output_path, "data", datapack.namespace, "custom_blocks", custom_block.internal_name), exist_ok=True)
        custom_block.create_datapack_files(datapack)

    for item in datapack.mcfunctions+datapack.custom_tags:
        os.makedirs(os.path.join(datapack.datapack_output_path, "data", datapack.namespace, item.datapack_subdirectory_name, *item.sub_directories), exist_ok=True)
        item.create_datapack_files(datapack)

    # Testing command
    # shutil.copyfile(f"{PYPACKS_ROOT}/scripts/setup_testing.mcfunction", f"{datapack.datapack_output_path}/data/{datapack.namespace}/function/setup_testing.mcfunction")
    # ================================================================================================