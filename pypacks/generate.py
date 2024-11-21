import os
import json
import shutil
from typing import TYPE_CHECKING

from pypacks.book_generator import ReferenceBook

if TYPE_CHECKING:
    from .datapack import Datapack

from .utils import PYPACKS_ROOT, get_png_dimensions
from .image_generation import add_icon_to_base


BASE_IMAGES = [f"{PYPACKS_ROOT}/assets/images/{x}.png" for x in (
    "empty_16_x_16", "empty_8_x_8", "empty_4_x_4", "empty_2_x_2", "empty_1_x_1", "icon_base", "logo",
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
    with open(f"{datapack.resource_pack_path}/pack.mcmeta", "w") as f:
        json.dump({"pack": {"pack_format": datapack.resource_pack_format_version, "description": datapack.description}}, f, indent=4)

    # pack.png
    if datapack.pack_icon_path is not None:
        with open(datapack.pack_icon_path, "rb") as f:
            image_contents = f.read()
        with open(f"{datapack.resource_pack_path}/pack.png", "wb") as f:
            f.write(image_contents)

    # ================================================================================================
    # Custom item images, model.json, item.json, etc
    for custom_item in datapack.custom_items:
        custom_item.create_resource_pack_files(datapack)
    # ================================================================================================
    # Copy from file_location to the resource pack
    for category in datapack.reference_book_categories:
        # shutil.copyfile(category.image_path, f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/font/{category.name}_category.png")
        # Copy & generate the icon, too
        with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/font/{category.name}_category_icon.png", "wb") as file:
            file.write(add_icon_to_base(image_path=category.image_path))

    # Custom back button:
    with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/font/satchel_icon.png", "wb") as file:
        file.write(add_icon_to_base(image_path=f"{PYPACKS_ROOT}/assets/images/satchel.png"))
    # ================================================================================================
    # Copy over the base images to the resource pack (icons, spacers, etc)
    for image in BASE_IMAGES:
        image_name = image.split("/")[-1].removesuffix(".png")
        shutil.copyfile(image, f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/font/{image_name}.png")

    for painting in datapack.custom_paintings:
        shutil.copyfile(painting.image_path, f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/painting/{painting.internal_name}.png")

    # ================================================================================================
    for sound in datapack.custom_sounds:
        shutil.copyfile(sound.ogg_path, f"{datapack.resource_pack_path}/assets/{datapack.namespace}/sounds/{sound.internal_name}.ogg")

    # Create the sounds.json file.
    with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/sounds.json", "w") as f:
        json.dump({sound.internal_name: sound.create_sound_entry(datapack) for sound in datapack.custom_sounds}, f, indent=4)
    # ================================================================================================


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
        mapping[f"{item.item_id}_icon"] = chars[i]
        height = get_png_dimensions(image_bytes=item.icon_image_bytes)[1]
        provider = {"type": "bitmap", "file": f"{datapack.namespace}:font/{item.item_id}_icon.png", "height": height, "ascent": min(height//2, 16), "chars": [chars[i]]}
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

    # https://www.youtube.com/watch?v=i4l2Ym_0VZg   <- Just cool
    with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/font/all_fonts.json", "w") as f:
        f.write(json.dumps({"providers": providers}, indent=4).replace("\\\\", "\\"))  # Replace double backslashes with single backslashes
    datapack.font_mapping = mapping


def generate_base_pack(datapack: "Datapack") -> None:
    # ================================================================================================
    os.makedirs(os.path.join(datapack.datapack_output_path), exist_ok=True)
    # pack.mcmeta
    with open(f"{datapack.datapack_output_path}/pack.mcmeta", "w") as f:
        json.dump({"pack": {"pack_format": datapack.data_pack_format_version, "description": datapack.description}}, f, indent=4)

    # pack.png
    if datapack.pack_icon_path is not None:
        shutil.copyfile(datapack.pack_icon_path, f"{datapack.datapack_output_path}/pack.png")

    # ================================================================================================
    # Load + Tick functions (and function folder)
    # Ensure the directory exists
    os.makedirs(os.path.join(datapack.datapack_output_path, "data", datapack.namespace, "function"), exist_ok=True)  # makes /data/{datapack_name}/function

    # Make the load and tick functions
    os.makedirs(os.path.join(datapack.datapack_output_path, "data", "minecraft", "tags", "function"), exist_ok=True)  # makes /data/minecraft/tags/function
    with open(f"{datapack.datapack_output_path}/data/minecraft/tags/function/load.json", "w") as f:
        json.dump({"values": [f"{datapack.namespace}:load"]}, f, indent=4)
    with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/function/load.mcfunction", "w") as f:
        f.write(f"Loaded in {datapack.name}!")

    # with open(f"{datapack.datapack_output_path}/data/minecraft/tags/function/tick.json", "w") as f:
    #     json.dump({"values": [f"{datapack.namespace}:tick"]}, f, indent=4)
    # with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/function/tick.mcfunction", "w") as f:
    #     f.write("say Tick!")

    # ================================================================================================
    # Items

    # Add to give all command
    book = ReferenceBook(datapack.custom_items)
    all_items = [book] + datapack.custom_items + datapack.custom_paintings + datapack.custom_jukebox_songs
    with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/function/give_all.mcfunction", "w") as f:
        f.write("\n".join([custom_item.generate_give_command(datapack) for custom_item in all_items]))
    # And give the book
    with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/function/give_reference_book.mcfunction", "w") as f:
        f.write(f"\n# Give the book\n{book.generate_give_command(datapack)}")
    # ================================================================================================
    os.makedirs(os.path.join(datapack.datapack_output_path, "data", datapack.namespace, "recipe"), exist_ok=True)  # makes /data/{datapack.namespace}/recipe
    os.makedirs(os.path.join(datapack.datapack_output_path, "data", datapack.namespace, "painting_variant"), exist_ok=True)
    os.makedirs(os.path.join(datapack.datapack_output_path, "data", datapack.namespace, "jukebox_song"), exist_ok=True)
    os.makedirs(os.path.join(datapack.datapack_output_path, "data", datapack.namespace, "tags"), exist_ok=True)
    os.makedirs(os.path.join(datapack.datapack_output_path, "data", datapack.namespace, "advancement"), exist_ok=True)
    # Recipes, Paintings, Jukebox songs, Tags, Advancements
    for item in datapack.custom_recipes+datapack.custom_jukebox_songs+datapack.custom_paintings+datapack.custom_tags+datapack.custom_advancements:
        item.create_json_file(datapack)

    # Testing command
    shutil.copyfile(f"{PYPACKS_ROOT}/scripts/setup_testing.mcfunction", f"{datapack.datapack_output_path}/data/{datapack.namespace}/function/setup_testing.mcfunction")
    # ================================================================================================