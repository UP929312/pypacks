from pypacks import Datapack, CustomItem, CustomItemData, CustomPainting, CustomSound, CustomJukeboxSong
from pypacks.resources.custom_recipe import *
from pypacks import (
    Equippable, Consumable, Food, UseRemainder, JukeboxPlayable, ToolRule, Tool, Instrument, WrittenBookContent, ReferenceBookCategory, LodestoneTracker
)

# ============================================================================================================
# Custom recipes
feather_to_string_recipe = FurnaceRecipe("feather_to_string_recipe", "minecraft:feather", "minecraft:string", 1, 20)
# cobble_recipe = ShapelessCraftingRecipe("cobblestone_recipe", ["minecraft:stone", "minecraft:stick"], "minecraft:cobblestone", 2)
# door_recipe = ShapelessCraftingRecipe("door_recipe", ["minecraft:stick", ["minecraft:oak_planks", "minecraft:spruce_planks"]], "minecraft:oak_door", 1)
# iron_helmet_recipe = ShapedCraftingRecipe("iron_helmet_recipe", ["iii", "   ", "iii"], {"i": "minecraft:iron_ingot"}, "minecraft:iron_helmet", 1)
# burnable_diamond_recipe = FurnaceRecipe("burnable_diamond_recipe", "minecraft:diamond", "minecraft:charcoal", 1, 40)
# smokable_redstone_recipe = SmokerRecipe("smokable_redstone_recipe", "minecraft:redstone", "minecraft:diamond", 100, 20)
# lapis_campfire_recipe = CampfireRecipe("lapis_campfire_recipe", "minecraft:lapis_lazuli", "minecraft:cooked_beef", 100, 20)
# recipes = [cobble_recipe, door_recipe, iron_helmet_recipe, burnable_diamond_recipe, smokable_redstone_recipe, lapis_campfire_recipe]
recipes = [feather_to_string_recipe]
# # ============================================================================================================

# custom_painting = CustomPainting("logo_art", "My Masterpiece", "Skezza", 4, 4, "images/logo_512_x_512.png")
# custom_sound = CustomSound("rick_roll", "sounds/rick_roll.ogg", 1.0, 1.0)
# custom_jukebox_song = CustomJukeboxSong(custom_sound.internal_name, "Rick Roll", custom_sound.ogg_path, 4, 5)
# # reference_book_category = ReferenceBookCategory("cool_things", "images/sword.png")
# # ============================================================================================================
# # Custom Items
# ruby = CustomItem("minecraft:emerald", "ruby", "Special Ruby", texture_path="images/ruby.png")
# topaz = CustomItem("minecraft:redstone", "topaz", "Topaz Ore", texture_path="images/topaz.png", additional_item_data=CustomItemData(equippable_slots=Equippable("chest")))
# custom_helmet = CustomItem("minecraft:iron_helmet", "flying_helmet", "Flying Helmet", additional_item_data=CustomItemData(glider=True, consumable=Consumable(0.5, "drink"), food=Food(5, 0, True), use_remainder=UseRemainder("minecraft:diamond", 2)))
# playable_lapis = CustomItem("minecraft:lapis_lazuli", "playable_lapis", "Playable Lapis", max_stack_size=99, rarity="epic", additional_item_data=CustomItemData(jukebox_playable=JukeboxPlayable("pigstep", True)))
# musical_horn = CustomItem("minecraft:goat_horn", "musical_horn", "Musical Horn", additional_item_data=CustomItemData(instrument=Instrument("minecraft:item.goat_horn.sound.5", "Custom description?", 10, 256)))
# rick_roll_horn = CustomItem("minecraft:goat_horn", "never_going_to_give_you_up", "Rick Roll", additional_item_data=CustomItemData(instrument=Instrument(f"{namespace}:rick_roll", "Rick Roll", 10, 256)))
# weak_axe = CustomItem("minecraft:netherite_axe", "weak_axe", "Weak Axe", additional_item_data=CustomItemData(durability=10, lost_durability=5))#, book_category=reference_book_category)
# written_book = CustomItem("minecraft:written_book", "already_written_in_book", "Written Book", additional_item_data=CustomItemData(written_book_content=WrittenBookContent("Hello, World!", "Author", [[{"text": "abc\n"}, {"text": "def"}]])),)
# lodestone_tracker = CustomItem("minecraft:compass", "lodestone_tracker", additional_item_data=CustomItemData(lodestone_tracker=LodestoneTracker(50, 50, 50)))
# speedy_porkchop = CustomItem("minecraft:porkchop", "speedy_porkchop", "Fast hand, extreme axe", additional_item_data=CustomItemData(tool=Tool(2, 0, [ToolRule("#mineable/axe", 10)])))
# unbreakable_axe = CustomItem("minecraft:stone_axe", "unbreakable_axe", "Unbreakable Axe", additional_item_data=CustomItemData(unbreakable=True))
# custom_items = [ruby, topaz, custom_helmet, playable_lapis, musical_horn, weak_axe, written_book, rick_roll_horn, lodestone_tracker, speedy_porkchop, unbreakable_axe]
# ============================================================================================================

world_name = "PyPacksWorld"
datapack_name = "PyPacks Tests"
namespace = "pypacks_tests"

datapack = Datapack(datapack_name, "The testing framework datapack", namespace, world_name=world_name,
                    custom_recipes=recipes,
                    # custom_items=custom_items, custom_sounds=[custom_sound],
                    # custom_paintings=[custom_painting],
                    # custom_jukebox_songs=[custom_jukebox_song],
                )
