import os
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pypacks.generate import generate_base_pack, generate_resource_pack, generate_font_pack
from pypacks.resources.custom_advancement import CustomAdvancement
from pypacks.resources.mcfunction import MCFunction
from pypacks.image_generation.ref_book_icon_gen import add_centered_overlay
from pypacks.raycasting import generate_default_raycasting_functions, ray_transitive_blocks_tag


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

    # TODO
    # on_tick_command: str | None = None
    # on_load_command: str | None = None

    custom_advancements: list["CustomAdvancement"] = field(default_factory=list)
    custom_blocks: list["CustomBlock"] = field(default_factory=list)
    custom_items: list["CustomItem"] = field(default_factory=list)
    custom_jukebox_songs: list["CustomJukeboxSong"] = field(default_factory=list)
    custom_loot_tables: list["CustomLootTable"] = field(default_factory=list)
    custom_paintings: list["CustomPainting"] = field(default_factory=list)
    custom_predicates: list["Predicate"] = field(default_factory=list)
    custom_recipes: list["Recipe"] = field(default_factory=list)
    custom_sounds: list["CustomSound"] = field(default_factory=list)
    custom_tags: list["CustomTag"] = field(default_factory=list)
    mcfunctions: list["MCFunction"] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.datapack_output_path == "" and self.world_name:
            self.datapack_output_path = f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\.minecraft\\saves\\{self.world_name}\\datapacks\\{self.name}"
        if self.resource_pack_path == "":
            self.resource_pack_path = f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\.minecraft\\resourcepacks\\{self.name}"

        self.data_pack_format_version = 61
        self.resource_pack_format_version = 46

        self.add_internal_functions()
        self.generate_pack()

    def add_internal_functions(self) -> None:
        # ============================================================================================================
        for item in [x for x in self.custom_items if x.on_right_click]:
            self.custom_advancements.append(CustomAdvancement.generate_right_click_functionality(item, self))
        # ==================================================================================
        # Adding all the blocks' items to the list
        for block in self.custom_blocks:
            if block.block_item is not None:
                self.custom_items.append(block.block_item)  # The custom item
            if block.loot_table is not None:
                self.custom_loot_tables.append(block.loot_table)
            self.custom_advancements.append(block.create_advancement(self))  # Advancement for placing the block
            self.mcfunctions.extend(block.generate_functions(self))  # Raycasting functions

        if self.custom_blocks:
            self.mcfunctions.extend(generate_default_raycasting_functions(self))
            self.mcfunctions.append(self.custom_blocks[0].on_tick_function(self))
            self.mcfunctions.append(self.custom_blocks[0].generate_detect_rotation_function())
            self.custom_tags.append(ray_transitive_blocks_tag)
        # ==================================================================================
        # Adding all the paintings' items to the list
        for painting in self.custom_paintings:
            self.custom_items.append(painting.generate_custom_item(self))
        for song in self.custom_jukebox_songs:
            self.custom_items.append(song.generate_custom_item(self))
        # ==================================================================================
        # REFERENCE BOOK CATEGORIES
        # Get all the categories by removing duplicates via name
        # Can't use set() because they're unhashable
        self.reference_book_categories: list["ReferenceBookCategory"] = []
        for item in self.custom_items:
            if item.book_category.name not in [x.name for x in self.reference_book_categories]:
                with open(item.book_category.image_path, "rb") as file:
                    item.book_category.icon_image_bytes = add_centered_overlay(image_bytes=file.read())
                self.reference_book_categories.append(item.book_category)
        assert len(self.reference_book_categories) <= 20, "There can only be 20 reference book categories!"
        # Make sure none of the categories are too filled
        for category in self.reference_book_categories:
            # TODO: Remove this, I want multiple pages where possible
            assert len([x for x in self.custom_items if x.book_category.name == category.name]) <= 18, f"Category {category.name} has too many items (>18)!"
        # ==================================================================================

        self.mcfunctions.append(MCFunction("load", [
            f"function {self.namespace}:raycast/load",
            f"gamerule maxCommandChainLength {10_000_000}",
            f"scoreboard objectives add player_yaw dummy",
            f"scoreboard objectives add player_pitch dummy",
            f"say Loaded into {self.name}!",
        ]))
        self.mcfunctions.append(MCFunction("tick", [
            f"function {self.namespace}:custom_blocks/all_blocks_tick" if self.custom_blocks else "",
        ]))

    def generate_pack(self) -> None:
        print(f"Generating data pack @ {self.datapack_output_path}")
        print(f"Generating resource pack @ {self.resource_pack_path}")
        print(r"C:\Users\%USERNAME%\AppData\Roaming\.minecraft\logs")  # TODO: Eventually remove this I suppose
        # Needs to go in this order
        self.custom_font = generate_font_pack(self)
        self.font_mapping = self.custom_font.get_mapping()
        generate_resource_pack(self)
        generate_base_pack(self)
