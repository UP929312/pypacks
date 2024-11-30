import os
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pypacks.generate import generate_base_pack, generate_resource_pack, generate_font_pack
from pypacks.resources.custom_advancement import CustomAdvancement
from pypacks.resources.custom_font import CustomFont
from pypacks.resources.mcfunction import MCFunction
from pypacks.raycasting import generate_raycasting_functions, generate_place_functions, ray_transitive_blocks_tag

from pypacks.image_generation import add_icon_to_base

if TYPE_CHECKING:
    from pypacks.book_generator import ReferenceBookCategory

    from pypacks.resources.custom_item import CustomItem
    from pypacks.resources.custom_block import CustomBlock
    from pypacks.resources.custom_jukebox_song import CustomJukeboxSong
    from pypacks.resources.custom_loot_table import CustomLootTable
    from pypacks.resources.custom_painting import CustomPainting
    from pypacks.resources.custom_predicate import Predicate
    from pypacks.resources.custom_recipe import Recipe
    from pypacks.resources.custom_sound import CustomSound
    from pypacks.resources.custom_tag import CustomTag


@dataclass
class Datapack:
    """Given a nice name for the datapack, a description, a namespace (usually a version of the datapack without spaces or punctuation, all lowercase),
    A path to a pack icon (optional), a world name (if you're not passing in a datapack output path, so it'll automatically be put in that world)
    A datapack output path (where the datapack will be saved, optional), a resource pack path (where the resource pack will be saved),
    And a list of custom elements."""
    name: str
    description: str
    namespace: str
    pack_icon_path: str | None = None
    world_name: str | None = None
    datapack_output_path: str = ""
    resource_pack_path: str = ""

    custom_advancements: list["CustomAdvancement"] = field(default_factory=list)
    custom_blocks: list["CustomBlock"] = field(default_factory=list)
    custom_items: list["CustomItem"] = field(default_factory=list)
    custom_jukebox_songs: list["CustomJukeboxSong"] = field(default_factory=list)
    custom_loot_tables: list["CustomLootTable"] = field(default_factory=list)
    custom_paintings: list["CustomPainting"] = field(default_factory=list)
    custom_predicates: list["Predicate"] = field(default_factory=list)
    custom_recipes: list["Recipe"] = field(default_factory=list)  # type: ignore
    custom_sounds: list["CustomSound"] = field(default_factory=list)
    custom_tags: list["CustomTag"] = field(default_factory=list)
    mcfunctions: list["MCFunction"] = field(default_factory=list)

    def __post_init__(self) -> None:
        assert self.custom_loot_tables == [], "Custom loot tables are not yet supported"
        if self.datapack_output_path == "" and self.world_name:
            self.datapack_output_path = f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\.minecraft\\saves\\{self.world_name}\\datapacks\\{self.name}"
        if self.resource_pack_path == "":
            self.resource_pack_path = f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\.minecraft\\resourcepacks\\{self.name}"

        self.data_pack_format_version = 61
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
        # ==================================================================================
        # Adding all the blocks' items to the list
        for block in self.custom_blocks:
            self.custom_items.append(block.block_item)  # type: ignore
            self.mcfunctions.extend(block.generate_place_function(self))

        if self.custom_blocks:
            self.mcfunctions.extend(generate_raycasting_functions(self))
            self.custom_tags.append(ray_transitive_blocks_tag)
            self.mcfunctions.extend(generate_place_functions(self))
        # ==================================================================================

        self.mcfunctions.append(MCFunction("load", [f"say Loaded into {self.name}!\nfunction {self.namespace}:raycast/load"]))

        self.generate_pack()


    def generate_pack(self) -> None:
        print(f"Generating data pack @ {self.datapack_output_path}")
        print(f"Generating resource pack @ {self.resource_pack_path}")
        # Needs to go in this order
        generate_resource_pack(self)
        self.font_mapping = generate_font_pack(self)
        generate_base_pack(self)
