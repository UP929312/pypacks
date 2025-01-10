import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from pypacks.generate import generate_base_pack, generate_resource_pack, generate_font_pack
from pypacks.resources.custom_advancement import CustomAdvancement
from pypacks.resources.custom_item import CustomItem
from pypacks.resources.custom_model import CustomItemModelDefinition
from pypacks.resources.custom_mcfunction import MCFunction
from pypacks.reference_book_config import RefBookCategory
from pypacks.raycasting import generate_default_raycasting_functions
from pypacks.create_wall import create_wall


if TYPE_CHECKING:
    from pypacks.resources.custom_block import CustomBlock
    from pypacks.resources.custom_enchantment import CustomEnchantment
    from pypacks.resources.custom_jukebox_song import CustomJukeboxSong
    from pypacks.resources.custom_loot_tables.custom_loot_table import CustomLootTable
    from pypacks.resources.custom_painting import CustomPainting
    from pypacks.resources.custom_predicate import Predicate
    from pypacks.resources.custom_recipe import Recipe
    from pypacks.resources.custom_sound import CustomSound
    from pypacks.resources.custom_tag import CustomTag


@dataclass
class Pack:
    """Given a nice name for the datapack and resouce pack, a description, a namespace (usually a version of the datapack without spaces or punctuation, all lowercase),
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

    # TODO: on_tick_function and on_load_function
    # on_tick_command: MCFunction | None = None
    # on_load_command: MCFunction | None = None

    custom_advancements: list["CustomAdvancement"] = field(default_factory=list)
    custom_blocks: list["CustomBlock"] = field(default_factory=list)
    custom_enchantments: list["CustomEnchantment"] = field(default_factory=list)
    custom_items: list["CustomItem"] = field(default_factory=list)
    custom_jukebox_songs: list["CustomJukeboxSong"] = field(default_factory=list)
    custom_loot_tables: list["CustomLootTable"] = field(default_factory=list)
    custom_paintings: list["CustomPainting"] = field(default_factory=list)
    custom_predicates: list["Predicate"] = field(default_factory=list)
    custom_recipes: list["Recipe"] = field(default_factory=list)
    custom_sounds: list["CustomSound"] = field(default_factory=list)
    custom_tags: list["CustomTag"] = field(default_factory=list)
    custom_mcfunctions: list["MCFunction"] = field(default_factory=list)
    custom_item_model_definitions: list[CustomItemModelDefinition] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.datapack_output_path == "" and self.world_name:
            self.datapack_output_path = f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\.minecraft\\saves\\{self.world_name}\\datapacks\\{self.name}"
        if self.resource_pack_path == "":
            self.resource_pack_path = f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\.minecraft\\resourcepacks\\{self.name}"

        self.datapack_output_path = Path(self.datapack_output_path)  # type: ignore[assignment]
        self.resource_pack_path = Path(self.resource_pack_path)  # type: ignore[assignment]

        self.data_pack_format_version = 61
        self.resource_pack_format_version = 46

        self.add_internal_functions()
        self.generate_pack()

    def add_internal_functions(self) -> None:
        # ============================================================================================================
        for item in [x for x in self.custom_items if x.on_right_click]:
            self.custom_advancements.append(CustomAdvancement.generate_right_click_functionality(item, self.namespace))
            self.custom_mcfunctions.append(item.create_right_click_revoke_advancement_function(self.namespace))
        # ==================================================================================
        # Adding all the blocks' items to the list
        for block in self.custom_blocks:
            if block.block_item is not None:
                self.custom_items.append(block.block_item)  # The custom item
            if block.loot_table is not None:
                self.custom_loot_tables.append(block.loot_table)  # When breaking the block
            self.custom_advancements.append(block.create_advancement(self.namespace))  # Advancement for placing the block
            self.custom_mcfunctions.extend(block.generate_functions(self.namespace))  # Raycasting functions

        if self.custom_blocks:
            self.custom_mcfunctions.extend(generate_default_raycasting_functions(self.namespace))
            self.custom_mcfunctions.append(self.custom_blocks[0].on_tick_function(self))
            self.custom_mcfunctions.append(self.custom_blocks[0].generate_detect_rotation_function())
        # ==================================================================================
        # Adding all the paintings' and jukebox's items to the list
        for painting in self.custom_paintings:
            self.custom_items.append(painting.generate_custom_item(self))
        for song in self.custom_jukebox_songs:
            self.custom_items.append(song.generate_custom_item(self))
        for enchantment in self.custom_enchantments:
            self.custom_items.append(enchantment.generate_custom_item(self.namespace))
        # ==================================================================================
        # Get all the reference book categories
        self.reference_book_categories = RefBookCategory.get_unique_categories([x.ref_book_config.category for x in self.custom_items if not x.ref_book_config.hidden])
        # ==================================================================================
        # Item models (well, the items)
        give_all_item_models = MCFunction("give_all_item_models", [
            custom_item_model_def.generate_give_command(self.namespace)
            for custom_item_model_def in [x for x in self.custom_item_model_definitions if x.showcase_item is not None]
        ])
        self.custom_mcfunctions.append(give_all_item_models)
        # ==================================================================================
        load_mcfunciton = MCFunction("load", [
            f"function {self.namespace}:raycast/load" if (self.custom_items or self.custom_blocks) else "",
            f"gamerule maxCommandChainLength {10_000_000}",  # This is generally for the reference book
            "scoreboard objectives add player_yaw dummy" if self.custom_blocks else "",  # For custom blocks
            "scoreboard objectives add player_pitch dummy" if self.custom_blocks else "",  # For custom blocks
            *[
                f"scoreboard objectives add {item.internal_name}_cooldown dummy \"Cooldown Timer For {item.internal_name}\"" + "\n" +
                f"execute as @a run scoreboard players set @s {item.internal_name}_cooldown 0"
                for item in self.custom_items if item.on_right_click and item.use_right_click_cooldown is not None
            ],
            f"say Loaded into {self.name}!",
        ])
        load_mcfunciton.create_if_empty = False
        tick_mcfunction = MCFunction("tick", [
            *[
                f"execute as @a[scores={{{item.internal_name}_cooldown=1..}}] run scoreboard players remove @s {item.internal_name}_cooldown 1"
                for item in self.custom_items if item.on_right_click and item.use_right_click_cooldown is not None
            ],
            f"function {self.namespace}:custom_blocks/all_blocks_tick" if self.custom_blocks else "",
        ])
        tick_mcfunction.create_if_empty = False
        self.custom_mcfunctions.extend([load_mcfunciton, tick_mcfunction])
        if self.custom_items:
            self.custom_mcfunctions.append(create_wall(self.custom_items, self.namespace))

    def generate_pack(self) -> None:
        print(f"Generating data pack @ {self.datapack_output_path}")
        print(f"Generating resource pack @ {self.resource_pack_path}")
        print(r"C:\Users\%USERNAME%\AppData\Roaming\.minecraft\logs")  # TODO: Eventually remove this I suppose
        # Needs to go in this order
        self.custom_fonts = [generate_font_pack(self)]
        self.font_mapping = self.custom_fonts[0].get_mapping()
        generate_resource_pack(self)
        generate_base_pack(self)
