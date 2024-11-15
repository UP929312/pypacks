from pypacks.generate import generate_base_pack, generate_resource_pack, generate_font_pack

from pypacks.resources.recipe import *
from pypacks.resources.custom_item import CustomItem

class Datapack:
    def __init__(
        self, name: str, description: str, namespace: str, pack_icon_path: str | None = None,
        datapack_output_path: str = "", resource_pack_path: str = "",
        base_recipes: list[ShapelessCraftingRecipe | ShapedCraftingRecipe | FurnaceRecipe | SmokerRecipe] | None = None,
        custom_items: list[CustomItem] | None = None
    ) -> None:
        self.name = name
        self.description = description
        self.namespace = namespace
        self.pack_icon_path = pack_icon_path
        self.datapack_output_path = datapack_output_path
        self.resource_pack_path = resource_pack_path
        self.base_recipes = base_recipes or []
        self.custom_items = custom_items or []

        self.data_pack_format_version = 60
        self.resource_pack_format_version = 45

        self.font_mapping = {}

        if datapack_output_path == "":
            raise ValueError("Datapack output path must be set")
        if resource_pack_path == "":
            raise ValueError("Resource pack path must be set")

        self.generate_pack()

    def generate_pack(self) -> None:
        print(f"Generating data pack @ {self.datapack_output_path}")
        print(f"Generating resource pack @ {self.resource_pack_path}")
        generate_resource_pack(self)
        generate_font_pack(self)
        generate_base_pack(self)