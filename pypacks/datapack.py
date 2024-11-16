from typing import TYPE_CHECKING

from pypacks.generate import generate_base_pack, generate_resource_pack, generate_font_pack

from pypacks.image_generation import add_icon_to_base
from pypacks.resources.recipe import Recipe

if TYPE_CHECKING:
    from pypacks.book_generator import ReferenceBookCategory
    from pypacks.resources.custom_item import CustomItem
    from pypacks.resources.custom_painting import CustomPainting
    from pypacks.resources.custom_sound import CustomSound

class Datapack:
    def __init__(
        self, name: str, description: str, namespace: str, pack_icon_path: str | None = None,
        datapack_output_path: str = "", resource_pack_path: str = "",
        base_recipes: list["Recipe"] | None = None,
        custom_items: list["CustomItem"] | None = None,
        custom_paintings: list["CustomPainting"] | None = None,
        custom_sounds: list["CustomSound"] | None = None,
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

        # Get all the categories by removing duplicates via name
        # Can't use set() because they're unhashable
        self.reference_book_categories: list["ReferenceBookCategory"] = []
        for item in self.custom_items:
            if item.book_category.name not in [x.name for x in self.reference_book_categories]:
                item.book_category.icon_image_bytes = add_icon_to_base(image_path=item.book_category.image_path)
                self.reference_book_categories.append(item.book_category)

        self.custom_paintings = custom_paintings or []
        self.custom_sounds = custom_sounds or []

        self.font_mapping = {}  # Is populated later

        if datapack_output_path == "":
            raise ValueError("Datapack output path must be set")
        if resource_pack_path == "":
            raise ValueError("Resource pack path must be set")

        self.generate_pack()

    def generate_pack(self) -> None:
        print(f"Generating data pack @ {self.datapack_output_path}")
        print(f"Generating resource pack @ {self.resource_pack_path}")
        # Needs to go in this order
        generate_resource_pack(self)
        generate_font_pack(self)
        generate_base_pack(self)