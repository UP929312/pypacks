import os
from dataclasses import dataclass, field
from pathlib import Path
from sys import platform
from typing import TYPE_CHECKING

from pypacks.additions.config import Config
from pypacks.additions.create_wall import create_wall
from pypacks.additions.custom_chunk_scanner import CustomChunkScanner
from pypacks.additions.custom_loop import CustomLoop
from pypacks.additions.custom_ore_generation import CustomOreGeneration
from pypacks.additions.raycasting import Raycast  # Needed to create the base raycast functions
from pypacks.additions.reference_book_config import RefBookCategory

from pypacks.resources.custom_item import CustomItem
from pypacks.resources.custom_mcfunction import MCFunction
from pypacks.resources.world_gen.world_gen_objects import WorldGenResources  # For default factory
from pypacks.generate import generate_datapack, generate_resource_pack, generate_base_font


if TYPE_CHECKING:
    from pypacks.additions.custom_block import CustomBlock
    from pypacks.additions.raycasting import BlockRaycast, EntityRaycast

    from pypacks.resources.entities import EntityVariant
    from pypacks.resources.custom_advancement import CustomAdvancement
    from pypacks.resources.custom_damage_type import CustomDamageType
    from pypacks.resources.custom_dimension import CustomDimension
    from pypacks.resources.custom_enchantment import CustomEnchantment
    from pypacks.resources.custom_font import CustomAutoAssignedFont
    from pypacks.resources.custom_game_test import CustomGameTest, CustomTestEnvironment
    from pypacks.resources.custom_jukebox_song import CustomJukeboxSong
    from pypacks.resources.custom_language import CustomLanguage
    from pypacks.resources.custom_loot_tables.custom_loot_table import CustomLootTable
    from pypacks.resources.custom_model import CustomItemRenderDefinition
    from pypacks.resources.custom_painting import CustomPainting
    from pypacks.resources.custom_predicate import Predicate
    from pypacks.resources.custom_recipe import Recipe
    from pypacks.resources.custom_sound import CustomSound
    from pypacks.resources.custom_tag import CustomTag
    from pypacks.resources.custom_model import CustomModelDefinition, CustomTexture

    from pypacks.additions.custom_crafter import CustomCrafter


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

    config: Config = field(default_factory=Config)

    on_tick_function: "MCFunction | None" = None
    on_load_function: "MCFunction | None" = None

    custom_advancements: list["CustomAdvancement"] = field(default_factory=list)
    custom_damage_types: list["CustomDamageType"] = field(default_factory=list)
    custom_dimensions: list["CustomDimension"] = field(default_factory=list)
    custom_enchantments: list["CustomEnchantment"] = field(default_factory=list)
    custom_entity_variants: list["EntityVariant"] = field(default_factory=list)
    custom_fonts: list["CustomAutoAssignedFont"] = field(default_factory=list)
    custom_game_tests: list["CustomGameTest"] = field(default_factory=list)
    custom_test_environments: list["CustomTestEnvironment"] = field(default_factory=list)
    custom_jukebox_songs: list["CustomJukeboxSong"] = field(default_factory=list)
    custom_languages: list["CustomLanguage"] = field(default_factory=list)
    custom_loot_tables: list["CustomLootTable"] = field(default_factory=list)
    custom_mcfunctions: list["MCFunction"] = field(default_factory=list)
    custom_paintings: list["CustomPainting"] = field(default_factory=list)
    custom_predicates: list["Predicate"] = field(default_factory=list)
    custom_recipes: list["Recipe"] = field(default_factory=list)
    custom_sounds: list["CustomSound"] = field(default_factory=list)
    custom_tags: list["CustomTag"] = field(default_factory=list)
    custom_textures: list["CustomTexture"] = field(default_factory=list)
    custom_model_definitions: list["CustomModelDefinition"] = field(default_factory=list)
    custom_item_render_definitions: list["CustomItemRenderDefinition"] = field(default_factory=list)
    world_gen_resources: "WorldGenResources" = field(default_factory=WorldGenResources)

    custom_items: list["CustomItem"] = field(default_factory=list)
    custom_blocks: list["CustomBlock"] = field(default_factory=list)
    custom_raycasts: list["BlockRaycast | EntityRaycast"] = field(default_factory=list)
    custom_crafters: list["CustomCrafter"] = field(default_factory=list)
    custom_loops: list["CustomLoop"] = field(default_factory=list)
    custom_ore_generations: list["CustomOreGeneration"] = field(default_factory=list)
    custom_chunk_scanners: list["CustomChunkScanner"] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.minecraft_location = f"C:/Users/{os.environ['USERNAME']}/AppData/Roaming/.minecraft" if platform == "win32" else "~/Library/Application Support/minecraft"
        if self.datapack_output_path == "" and self.world_name:
            self.datapack_output_path = f"{self.minecraft_location}/saves/{self.world_name}/datapacks/{self.name}"
        if self.resource_pack_path == "":
            self.resource_pack_path = f"{self.minecraft_location}/resourcepacks/{self.name}"

        self.datapack_output_path = Path(self.datapack_output_path)  # type: ignore[assignment]
        self.resource_pack_path = Path(self.resource_pack_path)  # type: ignore[assignment]

        self.data_pack_format_version = 71
        self.resource_pack_format_version = 55

        # Don't love this, but oh well (for the future, when I add more world gen stuff)
        self.custom_structures = self.world_gen_resources.custom_structures
        self.custom_structure_sets = self.world_gen_resources.custom_structure_sets
        self.custom_biomes = self.world_gen_resources.custom_biomes

        assert self.namespace.islower(), "Namespace must be all lowercase"
        assert all(x in "abcdefghijklmnopqrstuvwxyz0123456789_-." for x in self.namespace), "Namespace must only contain letters, numbers, _, -, and ."

    def add_internal_functions(self) -> None:
        # ==================================================================================
        # Custom Damage Types
        for custom_damage_type in self.custom_damage_types:
            self.custom_languages.extend([
                translation.to_custom_language(self.namespace, custom_damage_type.internal_name)
                for translation in custom_damage_type.translations  # type: ignore[union-attr]
                if custom_damage_type.translations is not None
            ])
        # =================================================================================
        # Custom Languages
        if self.custom_languages:
            self.custom_languages[0].combine_languages(self)
            if self.config.enable_language_propogation:
                self.custom_languages[0].propogate_to_all_similar_languages(self)
        # ==================================================================================
        # Custom Raycasts
        if self.custom_raycasts or self.custom_blocks or any(x for x in self.custom_items if x.on_right_click):
            self.custom_mcfunctions.extend(Raycast.generate_default_raycast_functions(self.namespace))
        # ==================================================================================
        # Custom Structure places (needs to be before on_right_click)
        for structure in [x for x in self.custom_structures if hasattr(x, "is_simple_resource")]:
            self.custom_items.append(structure.generate_custom_item(self.namespace))  # type: ignore[union-attr]
        # =================================================================================
        # Custom loops, chunk scanners, and ore generations
        for custom_ore_generation in self.custom_ore_generations:
            self.custom_chunk_scanners.append(custom_ore_generation.create_chunk_scanner(self.namespace))
            self.custom_mcfunctions.append(custom_ore_generation.create_generate_ore_function(self.namespace))
            self.custom_mcfunctions.extend(custom_ore_generation.create_ore_vein_function(self.namespace))  # This runs multiple times, which is fine...
        if self.custom_chunk_scanners:
            self.custom_mcfunctions.append(CustomChunkScanner.generate_mark_and_call_function(self.namespace))
            self.custom_loops.append(CustomChunkScanner.generate_check_chunk_loop(self.namespace))
        if self.custom_loops or self.custom_ore_generations:  # Has to go after the chunk scanner
            self.custom_mcfunctions.append(CustomLoop.generate_loop_manager_function(self.custom_loops, self.namespace))
        # ==================================================================================
        # Custom right click on items (and drops)
        for item in [x for x in self.custom_items if x.on_right_click]:
            self.custom_advancements.append(item.generate_right_click_advancement(self.namespace))
            self.custom_mcfunctions.append(item.create_right_click_revoke_advancement_function(self.namespace))
        has_on_drop_items = [x for x in self.custom_items if x.on_item_drop]
        if has_on_drop_items:
            self.custom_mcfunctions.extend(CustomItem.generate_on_drop_execute_loop(self.namespace))
            self.custom_mcfunctions.append(MCFunction.create_run_macro_function())
        # ==================================================================================
        # Custom crafters:
        for crafter in self.custom_crafters:
            self.custom_mcfunctions.append(crafter.on_tick(self.namespace))
            self.custom_items.append(crafter.generate_custom_item())
            self.custom_recipes.extend(crafter.recipes)
            # The crafter block itself...
            if crafter.crafter_block_crafting_recipe is not None:
                self.custom_recipes.append(crafter.crafter_block_crafting_recipe)
        # ==================================================================================
        # Adding all the blocks' items to the list
        for block in self.custom_blocks:
            if block.block_item is not None:
                self.custom_items.append(block.block_item)  # The custom item
            if block.loot_table is not None:
                self.custom_loot_tables.append(block.loot_table)  # When breaking the block
            self.custom_mcfunctions.append(block.generate_place_function(self.namespace))  # Function for placing the block (not by raycast)
            self.custom_advancements.append(block.create_advancement(self.namespace))  # Advancement for placing the block
            self.custom_mcfunctions.extend(block.generate_functions(self.namespace))  # Raycasting functions

        if self.custom_blocks:
            self.custom_mcfunctions.append(self.custom_blocks[0].on_tick_function(self))
            self.custom_mcfunctions.append(self.custom_blocks[0].generate_detect_rotation_function())
        # ==================================================================================
        # Adding all the paintings', jukebox's and enchanted books' items to the list
        for painting in self.custom_paintings:
            self.custom_items.append(painting.generate_custom_item(self))
        for song in self.custom_jukebox_songs:
            self.custom_items.append(song.generate_custom_item(self))
        for enchantment in self.custom_enchantments:
            self.custom_items.append(enchantment.generate_custom_item(self.namespace))
        # ==================================================================================
        # Get all the reference book categories
        if self.config.generate_reference_book:
            self.reference_book_categories = RefBookCategory.get_unique_categories(
                [x.ref_book_config.category for x in (self.custom_items+self.custom_dimensions) if not x.ref_book_config.hidden]
            )
        # ==================================================================================
        # Item models (well, the display items)
        if self.custom_item_render_definitions:
            give_all_item_models = MCFunction("give_all_item_models", [
                custom_item_model_def.generate_give_command(self.namespace)
                for custom_item_model_def in [x for x in self.custom_item_render_definitions if x.showcase_item is not None]
            ])
            self.custom_mcfunctions.append(give_all_item_models)
        # ==================================================================================
        self.internal_load_mcfunction = MCFunction("internal_load", [
            f"gamerule maxCommandChainLength {10_000_000}" if self.config.generate_reference_book else "",  # This is generally for the reference book
            "scoreboard objectives add raycast dummy" if (self.custom_items or self.custom_blocks or self.custom_raycasts) else "",
            f"scoreboard objectives add {self.custom_loops[0].scoreboard_objective_name} dummy" if self.custom_loops else "",
            "scoreboard objectives add constants dummy" if self.custom_loops else "",
            "scoreboard objectives add player_yaw dummy" if self.custom_blocks else "",
            "scoreboard objectives add player_pitch dummy" if self.custom_blocks else "",
            "scoreboard objectives add coords dummy" if self.custom_chunk_scanners else "",
            "scoreboard objectives add inputs dummy" if self.custom_chunk_scanners else "",
            *[
                f"scoreboard objectives add {item.internal_name}_cooldown dummy \"Cooldown Timer For {item.internal_name}\"" + "\n" +
                f"execute as @a run scoreboard players set @s {item.internal_name}_cooldown 0"
                for item in self.custom_items if item.on_right_click and item.use_right_click_cooldown is not None
            ],
            "scoreboard players set 16 constants 16" if self.custom_chunk_scanners else "",
            *{
                custom_loop.generate_set_constant_command()
                for custom_loop in self.custom_loops
            },
            f"say Loaded into {self.name}!" if self.name != "Minecraft" else "",
        ])
        # ==================================================================================
        self.internal_tick_mcfunction = MCFunction("internal_tick", [
            *[
                f"execute as @a[scores={{{item.internal_name}_cooldown=1..}}] run scoreboard players remove @s {item.internal_name}_cooldown 1"
                for item in self.custom_items if item.on_right_click and item.use_right_click_cooldown is not None  # TODO: Move these to a different file?
            ],  # TODO: Move this to its own function and just call it here...
            *[
                custom_crafter_tick.on_tick(self.namespace).get_run_command(self.namespace)
                for custom_crafter_tick in self.custom_crafters
            ],  # TODO: Move this to its own function and just call it here...
            self.custom_loops[0].generate_global_tick_counter() if self.custom_loops else "",
            self.custom_loops[0].generate_loop_manager_function(self.custom_loops, self.namespace).get_run_command(self.namespace) if self.custom_loops else "",
            f"function {self.namespace}:custom_blocks/all_blocks_tick" if self.custom_blocks else "",
            CustomItem.generate_on_drop_execute_loop(self.namespace)[1].get_run_command(self.namespace) if has_on_drop_items else "",
        ])
        if not self.internal_load_mcfunction.is_empty:
            self.custom_mcfunctions.append(self.internal_load_mcfunction)
        if not self.internal_tick_mcfunction.is_empty:
            self.custom_mcfunctions.append(self.internal_tick_mcfunction)
        # ==================================================================================
        if self.custom_items and self.config.generate_create_wall_command:
            self.custom_mcfunctions.append(create_wall(self.custom_items, self.namespace))
        if self.config.generate_reference_book:
            self.custom_items = sorted(self.custom_items, key=lambda x: self.reference_book_categories.index(x.ref_book_config.category))
        # ==================================================================================
        # Base font, required for reference book
        if self.config.generate_reference_book:
            self.custom_fonts.insert(0, generate_base_font(self))
            self.font_mapping = self.custom_fonts[0].get_mapping()
        # ==================================================================================

    def generate_pack(self) -> "Pack":
        self.add_internal_functions()
        self.generate_minecraft_pack()
        print(f"Generating data pack @ {self.datapack_output_path}/data/{self.namespace}")
        print(f"Generating resource pack @ {self.resource_pack_path}/assets/{self.namespace}")
        print(f"{self.minecraft_location}/logs/latest.log")
        # Needs to go in this order (I think?)
        generate_datapack(self)
        generate_resource_pack(self)
        return self

    def generate_minecraft_pack(self) -> None:
        from pypacks.resources.custom_tag import CustomTag
        tags = [
            CustomTag("tick", [
                self.internal_tick_mcfunction.get_reference(self.namespace) if not self.internal_tick_mcfunction.is_empty else None,  # type: ignore[list-item]
                self.on_tick_function.get_reference(self.namespace) if self.on_tick_function is not None else None,  # type: ignore[list-item]
            ], tag_type="function"),
            CustomTag("load", [
                self.internal_load_mcfunction.get_reference(self.namespace) if not self.internal_load_mcfunction.is_empty else None,  # type: ignore[list-item]
                self.on_load_function.get_reference(self.namespace) if self.on_load_function is not None else None,  # type: ignore[list-item]
            ], tag_type="function"),
        ]
        minecraft = Pack("Minecraft", "", "minecraft", datapack_output_path=self.datapack_output_path,
                         custom_tags=tags, config=Config(generate_create_wall_command=False, generate_reference_book=False))
        generate_datapack(minecraft)

    @classmethod
    def from_existing_pack(cls, datapack_path: "str | Path", resource_pack_path: "str | Path") -> "Pack":
        datapack_path = Path(datapack_path)
        resource_pack_path = Path(resource_pack_path)
        from pypacks.resources.custom_advancement import CustomAdvancement
        from pypacks.resources.custom_damage_type import CustomDamageType
        from pypacks.resources.custom_dimension import CustomDimension
        from pypacks.resources.custom_enchantment import CustomEnchantment
        from pypacks.resources.entities import ALL_ENTITY_VARIANTS
        # from pypacks.resources.custom_font import CustomAutoAssignedFont
        from pypacks.resources.custom_game_test import CustomGameTest, CustomTestEnvironment
        from pypacks.resources.custom_jukebox_song import CustomJukeboxSong
        from pypacks.resources.custom_language import CustomLanguage
        from pypacks.resources.custom_loot_tables import CustomLootTable
        from pypacks.resources.custom_model import CustomItemRenderDefinition, CustomModelDefinition, CustomTexture
        from pypacks.resources.custom_painting import CustomPainting
        from pypacks.resources.custom_predicate import Predicate
        from pypacks.resources.custom_recipe import Recipe
        from pypacks.resources.custom_sound import CustomSound
        from pypacks.resources.custom_tag import CustomTag
        # from pypacks.resources.world_gen.world_gen_objects import WorldGenResources
        # All WorldGenResources

        entity_variants_2d = [x.from_datapack_files(datapack_path) for x in ALL_ENTITY_VARIANTS]  # TODO: Needs from_combined_files
        # print(CustomLanguage.from_resource_pack_files(resource_pack_path))
        print(Recipe.from_datapack_files(datapack_path))
        return Pack(
            name="", description="", namespace="a",
            custom_advancements=CustomAdvancement.from_datapack_files(datapack_path),
            custom_damage_types=CustomDamageType.from_datapack_files(datapack_path),
            custom_dimensions=CustomDimension.from_datapack_files(datapack_path),
            custom_enchantments=CustomEnchantment.from_datapack_files(datapack_path),
            custom_entity_variants=[x for sublist in entity_variants_2d for x in sublist if x],
            # custom_fonts=CustomAutoAssignedFont.from_datapack_files(datapack_path),
            custom_game_tests=CustomGameTest.from_datapack_files(datapack_path),
            custom_test_environments=CustomTestEnvironment.from_datapack_files(datapack_path),
            custom_jukebox_songs=CustomJukeboxSong.from_combined_files(datapack_path, resource_pack_path),
            custom_languages=CustomLanguage.from_resource_pack_files(resource_pack_path),
            custom_loot_tables=CustomLootTable.from_datapack_files(datapack_path),
            custom_mcfunctions=MCFunction.from_datapack_files(datapack_path),
            custom_paintings=CustomPainting.from_combined_files(datapack_path, resource_pack_path),
            custom_predicates=Predicate.from_datapack_files(datapack_path),
            # custom_recipes=Recipe.from_datapack_files(datapack_path),
            custom_sounds=CustomSound.from_resource_pack_files(resource_pack_path),
            custom_tags=CustomTag.from_datapack_files(datapack_path),
            custom_textures=CustomTexture.from_resource_pack_files(resource_pack_path),
            custom_model_definitions=CustomModelDefinition.from_datapack_files(resource_pack_path),
            custom_item_render_definitions=CustomItemRenderDefinition.from_datapack_files(resource_pack_path),
            # world_gen_resources=WorldGenResources.from_datapack_files(datapack_path),
        )
