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
    "empty_16_x_16", "empty_8_x_8", "empty_4_x_4", "empty_2_x_2", "empty_1_x_1", "icon_base", "unknown_icon", "logo"
)]

def generate_resource_pack(datapack: "Datapack") -> None:
    os.makedirs(os.path.join(datapack.resource_pack_path, "assets", datapack.namespace, "items"), exist_ok=True)
    os.makedirs(os.path.join(datapack.resource_pack_path, "assets", datapack.namespace, "models", "item"), exist_ok=True)
    os.makedirs(os.path.join(datapack.resource_pack_path, "assets", datapack.namespace, "textures", "item"), exist_ok=True)
    os.makedirs(os.path.join(datapack.resource_pack_path, "assets", datapack.namespace, "textures", "icon"), exist_ok=True)
    os.makedirs(os.path.join(datapack.resource_pack_path, "assets", datapack.namespace, "textures", "font"), exist_ok=True)
    os.makedirs(os.path.join(datapack.resource_pack_path, "assets", datapack.namespace, "font"), exist_ok=True)  # makes /assets/minecraft/font

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
    # Custom item images copied over
    for custom_item in datapack.custom_items:
        custom_item.create_resource_pack_files(datapack)
        if custom_item.texture_path is not None:
            shutil.copyfile(custom_item.texture_path, f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/font/{custom_item.item_id}.png")
            # Create the icons for the custom items
            add_icon_to_base(custom_item.texture_path, f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/font/{custom_item.item_id}.png")

    # ================================================================================================

    # Copy over the base images to the resource pack
    for image in BASE_IMAGES:
        image_name = image.split("/")[-1].removesuffix(".png")
        shutil.copyfile(image, f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/font/{image_name}.png")


def generate_font_pack(datapack: "Datapack") -> None:
    # Create the providers file & mapping
    chars = [f"\\uE{i:03}" for i in range(0, 100)]  # Generate \uE000 - \uE999
    mapping = {}
    providers = []
    for i, image in enumerate(BASE_IMAGES+[x.texture_path for x in datapack.custom_items if x.texture_path is not None]):
        image_name = image.split("/")[-1].removesuffix(".png")
        mapping[image_name] = chars[i]
        height = get_png_dimensions(image)[1]
        provider = {"type": "bitmap", "file": f"{datapack.namespace}:font/{image_name}.png", "height": height, "ascent": min(height//2, 16), "chars": [chars[i]]}
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
        with open(datapack.pack_icon_path, "rb") as f:
            image_contents = f.read()
        with open(f"{datapack.datapack_output_path}/pack.png", "wb") as f:
            f.write(image_contents)

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

    # Shaped & Shapeless crafting recipes (add recipe files)
    os.makedirs(os.path.join(datapack.datapack_output_path, "data", datapack.namespace, "recipe"), exist_ok=True)  # makes /data/{datapack.namespace}/recipe
    for recipe in datapack.base_recipes:
        with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/recipe/{recipe.name}.json", "w") as f:
            f.write(recipe.to_file_contents())

    # ================================================================================================
    # Items

    # Add to give all command
    book = ReferenceBook(datapack.custom_items)
    with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/function/give_all.mcfunction", "w") as f:
        f.write("\n".join([custom_item.generate_give_command(datapack, datapack.namespace) for custom_item in datapack.custom_items+[book]]))
    # for custom_item in datapack.custom_items:
    #     pass
    # ================================================================================================
