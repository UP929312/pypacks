import os
from typing import TYPE_CHECKING

from pypacks.generate import generate_base_pack, generate_resource_pack, generate_font_pack
from pypacks.resources.custom_advancement import CustomAdvancement

from pypacks.image_generation import add_icon_to_base

if TYPE_CHECKING:
    from pypacks.book_generator import ReferenceBookCategory

    # from pypacks.resources.custom_advancement import CustomAdvancement
    from pypacks.resources.custom_item import CustomItem
    from pypacks.resources.custom_jukebox_song import CustomJukeboxSong
    from pypacks.resources.custom_painting import CustomPainting
    from pypacks.resources.custom_recipe import Recipe
    from pypacks.resources.custom_sound import CustomSound
    from pypacks.resources.custom_tag import CustomTag

class Datapack:
    def __init__(
        self, name: str, description: str, namespace: str, pack_icon_path: str | None = None,
        world_name: str | None = None,
        datapack_output_path: str = "", resource_pack_path: str = "",
        custom_advancements: list["CustomAdvancement"] | None = None,
        custom_items: list["CustomItem"] | None = None,
        custom_jukebox_songs: list["CustomJukeboxSong"] | None = None,
        custom_paintings: list["CustomPainting"] | None = None,
        custom_recipes: list["Recipe"] | None = None,
        custom_sounds: list["CustomSound"] | None = None,
        custom_tags: list["CustomTag"] | None = None,
    ) -> None:
        """Given a nice name for the datapack, a description, a namespace (usually a version of the datapack without spaces or punctuation, all lowercase),
        A path to a pack icon (optional), a world name (if you're not passing in a datapack output path, so it'll automatically be put in that world)
        A datapack output path (where the datapack will be saved, optional), a resource pack path (where the resource pack will be saved),
        And a list of custom elements."""
        self.name = name
        self.description = description
        self.namespace = namespace
        self.pack_icon_path = pack_icon_path
        self.datapack_output_path = datapack_output_path
        self.resource_pack_path = resource_pack_path
        self.world_name = world_name

        self.custom_advancements = custom_advancements or []
        self.custom_recipes = custom_recipes or []
        self.custom_items = custom_items or []
        self.custom_tags = custom_tags or []

        if self.datapack_output_path == "" and self.world_name:
            self.datapack_output_path = f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\.minecraft\\saves\\{world_name}\\datapacks\\{name}"
        if self.resource_pack_path == "":
            self.resource_pack_path = f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\.minecraft\\resourcepacks\\{name}"

        self.data_pack_format_version = 60
        self.resource_pack_format_version = 46

        # REFERENCE BOOK CATEGORIES ==================================================================================
        # Get all the categories by removing duplicates via name
        # Can't use set() because they're unhashable
        self.reference_book_categories: list["ReferenceBookCategory"] = []
        for item in self.custom_items:
            if item.book_category.name not in [x.name for x in self.reference_book_categories]:
                item.book_category.icon_image_bytes = add_icon_to_base(image_path=item.book_category.image_path)
                self.reference_book_categories.append(item.book_category)
        assert len(self.reference_book_categories) <= 20, "There can only be 12 reference book categories!"
        # Make sure none of the categories are too filled
        for category in self.reference_book_categories:
            # TODO: Remove this, I want multiple pages where possible
            assert len([x for x in self.custom_items if x.book_category.name == category.name]) <= 18, f"Category {category.name} has too many items (>18)!"
        # ============================================================================================================
        for item in [x for x in self.custom_items if x.on_right_click]:
            self.custom_advancements.append(CustomAdvancement.generate_right_click_functionality(item, self))

        self.custom_paintings = custom_paintings or []
        self.custom_sounds = custom_sounds or []
        self.custom_jukebox_songs = custom_jukebox_songs or []

        self.font_mapping = {}  # Is populated later

        self.generate_pack()

    def generate_pack(self) -> None:
        print(f"Generating data pack @ {self.datapack_output_path}")
        print(f"Generating resource pack @ {self.resource_pack_path}")
        # Needs to go in this order
        generate_resource_pack(self)
        generate_font_pack(self)
        generate_base_pack(self)
