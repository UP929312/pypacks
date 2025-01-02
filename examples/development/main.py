from pypacks import (
    Datapack, CustomItem, Components, CustomPainting, CustomSound, CustomJukeboxSong, CustomBlock,
    CustomLootTable, RefBookCategory,
    FacePaths, RefBookConfig, CUSTOM_BLOCKS_REF_BOOK_CATEGORY,
)
from pypacks.resources.custom_loot_tables import SimpleRangePool, SingleItemPool, SimpleRangeLootTable
from pypacks.resources.custom_model import CustomItemModelDefinition
from pypacks.resources.custom_recipe import *
from pypacks.resources.item_components import *
from pypacks import ConstantTint

import os

from pypacks.resources.item_model_definition import ModelItemModel
os.chdir(os.path.dirname(__file__))

# ============================================================================================================
custom_painting = CustomPainting("logo_art", "images/logo_512_x_512.png", title="My Masterpiece", width_in_blocks=4, height_in_blocks=4)
custom_sound = CustomSound("rick_roll", "sounds/rick_roll.ogg", 1.0, 1.0)
custom_jukebox_song = CustomJukeboxSong(custom_sound.internal_name, "Rick Roll", custom_sound.ogg_path, 4, 5)
weapons_category = RefBookCategory("weapons", "Weapons", "images/sword.png")
usable_category = RefBookCategory("usable", "Usable", "images/goat_horn.png")
consumable_category = RefBookCategory("consumable", "Consumable", "images/steak.png")
# ============================================================================================================
# region: Custom Items
# Custom Items
ruby = CustomItem("ruby", "minecraft:emerald", "&cSpecial &4Ruby", lore=["Custom &cRuby&f, ooh!"], texture_path="images/ruby.png", ref_book_config=RefBookConfig(description="A special rube, found in the depths of the earth."))
topaz = CustomItem("topaz", "minecraft:redstone", "Topaz", texture_path="images/topaz.png", components=Components(equippable=Equippable("chest")))
weak_axe = CustomItem("weak_axe", "minecraft:netherite_axe", "Weak Axe", components=Components(durability=10, lost_durability=5), ref_book_config=RefBookConfig(category=weapons_category))
flying_helmet = CustomItem("flying_helmet", "minecraft:iron_helmet", "Flying Helmet", components=Components(glider=True, consumable=Consumable(0.5, "drink"), food=Food(5, 0, True), use_remainder=UseRemainder("minecraft:diamond", 2)), ref_book_config=RefBookConfig(category=usable_category))
playable_lapis = CustomItem("playable_lapis", "minecraft:lapis_lazuli", "Playable Lapis", max_stack_size=99, rarity="epic", components=Components(jukebox_playable=JukeboxPlayable("pigstep", True)), ref_book_config=RefBookConfig(category=usable_category))
musical_horn = CustomItem("musical_horn", "minecraft:goat_horn", "Musical Horn", components=Components(instrument=Instrument("minecraft:item.goat_horn.sound.5", "Custom description?", 5, 256)), ref_book_config=RefBookConfig(category=usable_category))
rick_roll_horn = CustomItem("never_going_to_give_you_up", "minecraft:goat_horn", "Rick Roll", components=Components(instrument=Instrument(custom_sound, "Rick Roll", 5, 256)), ref_book_config=RefBookConfig(category=usable_category))
rick_roll_horn_from_sound = CustomItem("never_going_to_give_you_up_from_sound", "minecraft:goat_horn", "Rick Roll From Sound", components=Components(instrument=Instrument(custom_sound, "Rick Roll From Sound", 3, 256)), ref_book_config=RefBookConfig(category=usable_category))
written_book = CustomItem("already_written_in_book", "minecraft:written_book", "Written Book", components=Components(written_book_content=WrittenBookContent("Hello, World!", "Author", [[{"text": "abc\n"}, {"text": "def"}]])),)
writable_book = CustomItem("writable_book", "minecraft:writable_book", "Writable Book", components=Components(writable_book_content=WritableBookContent(["Hello world"])))
lodestone_tracker = CustomItem("lodestone_tracker", "minecraft:compass", components=Components(lodestone_tracker=LodestoneTracker(126, 68, -41)))
speedy_porkchop = CustomItem("speedy_porkchop", "minecraft:porkchop", "Fast hand, extreme axe", components=Components(tool=Tool(2, 0, [ToolRule("#mineable/axe", 10)])))
unbreakable_axe = CustomItem("unbreakable_axe", "minecraft:stone_axe", "Unbreakable Axe", components=Components(unbreakable=True), ref_book_config=RefBookConfig(category=weapons_category))
player_head = CustomItem("custom_player_head_skin", "minecraft:player_head", "My Skin", components=Components(player_head_username="Skezza"))
sharpness_fish = CustomItem("sharpness_fish", "minecraft:cod", "Sharpness Fish", components=Components(enchantments={"sharpness": 5}), ref_book_config=RefBookConfig(category=consumable_category))
enchantment_spruce_door = CustomItem("shiny_door", "minecraft:spruce_door", "Shiny Door", components=Components(enchantment_glint_override=True))
attribute_modified_axe = CustomItem("attribute_modified_axe", "minecraft:wooden_axe", "Attribute Modified Axe", components=Components(attribute_modifiers=[AttributeModifier(attribute_type="attack_damage", amount=10, operation="add_value", slot="mainhand")]), ref_book_config=RefBookConfig(category=weapons_category))
repairable_axe = CustomItem("repairable_axe", "minecraft:stone_axe", "Repairable Axe", components=Components(durability=1000, lost_durability=500, repair_cost=5, repaired_by=["minecraft:stone"]), ref_book_config=RefBookConfig(category=weapons_category))
slow_enderpearl_recharge = CustomItem("slow_enderpearl_recharge", "minecraft:ender_pearl", "Slow Enderpearl Recharge", components=Components(cooldown=Cooldown(10)))
right_clickable_feather = CustomItem("right_clickable_feather", "minecraft:feather", "Right Clickable Feather", on_right_click="summon minecraft:arrow ^ ^ ^")
right_clickable_nether_quartz = CustomItem("right_clickable_nether_quartz", "minecraft:quartz", "Right Clickable Nether Quartz", on_right_click="give @a grass_block", components=Components(cooldown=Cooldown(seconds=3)))
custom_head_texture = CustomItem("custom_head_texture", "minecraft:player_head", "Custom Head Texture", components=Components(custom_head_texture="eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvZjg3N2M5NTA5NTg3YjNiODhjOTI3Zjc0YWE2NjlhZTg3MjVhMTRmZjU1ZGY2ZGUwMDRjNDFlMjYxNzg1YTJmOCJ9fX0="))
ray_gun = CustomItem("ray_gun", "minecraft:blaze_rod", "Ray Gun", on_right_click="function pypacks_testing:raycast/populate_start_ray", ref_book_config=RefBookConfig(category=weapons_category))
pre_charged_crossbow = CustomItem("pre_charged_crossbow", "minecraft:crossbow", "Pre Charged Crossbow", components=Components(loaded_projectiles=["minecraft:arrow", "minecraft:arrow", "minecraft:arrow"]), ref_book_config=RefBookConfig(category=weapons_category))
steak_to_ruby_when_eaten = CustomItem("steak_to_ruby_when_eaten", "minecraft:cooked_beef", "Steak to Ruby When Eat", components=Components(consumable=Consumable(0.5, "eat"), food=Food(5, 0, True), use_remainder=UseRemainder(ruby)), ref_book_config=RefBookConfig(category=consumable_category))
custom_firework = CustomItem("custom_firework", "minecraft:firework_rocket", "Custom Firework", components=Components(firework=Firework(flight_duration=3, explosions=[FireworkExplosion(shape="star", colors=[16711680, 65280], fade_colors=[255, 16776960], has_trail=True, has_twinkle=True)])), ref_book_config=RefBookConfig(category=usable_category))
custom_firework_hex = CustomItem("custom_firework_hex", "minecraft:firework_rocket", "Custom Firework Hex", components=Components(firework=Firework(flight_duration=1, explosions=[FireworkExplosion(shape="large_ball", colors=[0xFF0000])])), ref_book_config=RefBookConfig(category=usable_category))
map_with_decoration = CustomItem("map_with_decoration", "minecraft:filled_map", "Map With Decoration", components=Components(map_data=MapData(map_id=1, map_decorations=[MapDecoration("red_x", 120, -46, 0)])), ref_book_config=RefBookConfig(category=usable_category))
colored_map = CustomItem("colored_map", "minecraft:filled_map", "Colored Map", components=Components(map_data=MapData(map_color=0x0000FF)), ref_book_config=RefBookConfig(category=usable_category))
map_with_id = CustomItem("map_with_id", "minecraft:filled_map", "Map with ID", components=Components(map_data=MapData(map_id=1)), ref_book_config=RefBookConfig(category=usable_category))
banner = CustomItem("banner", "minecraft:white_banner", "Banner", components=Components(banner_patterns=[BannerPattern("stripe_left", "red"), BannerPattern("stripe_bottom", "blue")]))
edible_item = CustomItem("edible_witch_spawn_egg", "minecraft:witch_spawn_egg", "Edible Witch Spawn Egg", components=Components(consumable=Consumable(0.5, "drink"), food=Food(5, 0, True)))
note_block_sound_head = CustomItem("note_block_sound_head", "minecraft:player_head", "Note Block Sound Head", components=Components(note_block_sound=custom_sound))
eating_gives_you_speed = CustomItem("eating_gives_you_speed", "minecraft:cooked_rabbit", "Eating Gives You Speed", components=Components(consumable=Consumable(0.5, "eat", on_consume_effects=[PotionEffect("speed", 1, 20*10)]), food=Food(can_always_eat=True)), ref_book_config=RefBookConfig(category=consumable_category))
eating_removes_speed = CustomItem("eating_removes_you_speed", "minecraft:cooked_rabbit", "Eating Removes You Speed", components=Components(consumable=Consumable(0.5, "eat", on_consume_remove_effects=[PotionEffect("speed")]), food=Food(can_always_eat=True)), ref_book_config=RefBookConfig(category=consumable_category))
eating_teleports = CustomItem("eating_teleports", "minecraft:cooked_rabbit", "Eating Teleports", components=Components(consumable=Consumable(0.5, "eat", on_consume_teleport_diameter=5), food=Food(can_always_eat=True)), ref_book_config=RefBookConfig(category=consumable_category))
eating_gives_you_speed_and_teleports = CustomItem("eating_gives_you_speed_and_teleports", "minecraft:cooked_rabbit", "Eating Gives You Speed And Teleports", components=Components(consumable=Consumable(0.5, "eat", on_consume_effects=[PotionEffect("speed", 1, 20*10)], on_consume_teleport_diameter=10), food=Food(can_always_eat=True)), ref_book_config=RefBookConfig(category=consumable_category))
eating_plays_rick_roll = CustomItem("eating_plays_rick_roll", "minecraft:cooked_cod", "Eating Plays Rick Roll", components=Components(consumable=Consumable(0.5, "eat", consuming_sound=custom_sound), food=Food(can_always_eat=True)), ref_book_config=RefBookConfig(category=consumable_category))
colorful_shield = CustomItem("colorful_shield", "minecraft:shield", "Colorful Shield", components=Components(shield_base_color="red"), ref_book_config=RefBookConfig(category=usable_category))
bee_nest = CustomItem("bee_nest", "minecraft:bee_nest", "Bee Nest", components=Components(bees=[Bee(), Bee(), Bee(), Bee()]))
bundle = CustomItem("bundle", "minecraft:bundle", "Bundle", components=Components(bundle_contents=BundleContents({"minecraft:emerald": 5, ruby: 3})), ref_book_config=RefBookConfig(category=usable_category))
filled_barrel = CustomItem("filled_barrel", "minecraft:barrel", "Filled Barrel", components=Components(container_contents=ContainerContents({"minecraft:diamond": 5, ruby: 3})), ref_book_config=RefBookConfig(category=usable_category))
custom_potion = CustomItem("custom_potion", "minecraft:potion", "Custom Potion", components=Components(potion_contents=PotionContents(custom_color=0xFF0000, effects=[PotionEffect("speed", 1, 20*10)])), ref_book_config=RefBookConfig(category=consumable_category))
decorated_pot = CustomItem("decorated_pot", "decorated_pot", "decorated Pot", components=Components(pot_decorations=["angler_pottery_sherd", "brick", "arms_up_pottery_sherd", "skull_pottery_sherd"]))
death_protection_star = CustomItem("death_protection_star", "minecraft:nether_star", "Death Protection Star", components=Components(death_protection=DeathProtection(apply_affects=[PotionEffect("fire_resistance", 2, 20*5)])), ref_book_config=RefBookConfig(category=consumable_category))
dyed_helmet = CustomItem("dyed_helmet", "minecraft:leather_helmet", "Dyed Helmet", components=Components(dye_color=0xFF00FF), ref_book_config=RefBookConfig(category=weapons_category))
trimmed_leggings = CustomItem("trimmed_leggings", "minecraft:leather_leggings", "Trimmed Leggings", components=Components(armor_trim=ArmorTrim("host", "emerald")), ref_book_config=RefBookConfig(category=usable_category))
suspicious_stew = CustomItem("suspicious_stew", "minecraft:suspicious_stew", "Suspicious Stew", components=Components(suspicious_stew_effects={"speed": 5*20}), ref_book_config=RefBookConfig(category=consumable_category))
spider_spawner = CustomItem("spider_spawner", "minecraft:spawner", "Spider Spawner", components=Components(block_entity_data={"id": "mob_spawner", "SpawnData": {"entity": {"id": "spider"}}}), ref_book_config=RefBookConfig(category=usable_category))
upper_slab = CustomItem("upper_slab", "minecraft:stone_slab", "Upper Slab", components=Components(block_state={"type": "top"}))
fish_bucket = CustomItem("fish_bucket", "minecraft:tropical_fish_bucket", "Fish Bucket", components=Components(bucket_entity_data=BucketEntityData(bucket_variant_tag=TropicalFishData(size="large", pattern=1, body_color="light_blue", pattern_color="yellow"))), ref_book_config=RefBookConfig(category=usable_category))
loot_table_chest = CustomItem("loot_table_chest", "minecraft:chest", "Loot Table Chest", components=Components(container_loot_table="minecraft:chests/village/village_butcher"), ref_book_config=RefBookConfig(category=usable_category))

# fish_bucket222 = CustomItem("minecraft:tropical_fish_bucket", "fish_bucket", "Fish Bucket", components=Components.from_list([BucketEntityData(bucket_variant_tag=TropicalFishData(size="large", pattern=1, body_color="light_blue", pattern_color="yellow"))]), ref_book_config=RefBookConfig(category=usable_category))
# test = CustomItem("minecraft:emerald", "test", "Test", components=Components.from_list([Equippable("chest")]), ref_book_config=RefBookConfig(category=weapons_category))

# edible_bow = CustomItem("minecraft:bow", "edible_bow", "Yummy Bow", components=Components(consumable=Consumable(0.5, "drink"), food=Food(5, 0, True)))
# edible_item = CustomItem("minecraft:witch_spawn_egg", "edible_witch_spawn_egg", "Edible Witch Spawn Egg", components=Components(consumable=Consumable(0.5, "drink"), food=Food(5, 0, True)))

custom_items = [
    ruby, topaz, weak_axe, flying_helmet, playable_lapis, musical_horn, written_book, rick_roll_horn,
    rick_roll_horn_from_sound, lodestone_tracker, speedy_porkchop, unbreakable_axe, player_head, writable_book,
    sharpness_fish, enchantment_spruce_door, attribute_modified_axe, repairable_axe, slow_enderpearl_recharge,
    right_clickable_feather, right_clickable_nether_quartz, custom_head_texture, ray_gun,  # edible_item
    pre_charged_crossbow, steak_to_ruby_when_eaten, custom_firework, custom_firework_hex, map_with_decoration,
    colored_map, map_with_id, banner, note_block_sound_head, eating_gives_you_speed, eating_removes_speed,
    eating_teleports, eating_gives_you_speed_and_teleports, eating_plays_rick_roll, colorful_shield, bee_nest,
    bundle, filled_barrel, custom_potion, decorated_pot, death_protection_star, dyed_helmet, trimmed_leggings,
    suspicious_stew, spider_spawner, upper_slab, fish_bucket, loot_table_chest,
]
# endregion
# ============================================================================================================
# region: Custom Recipes
# Custom recipes
cobble_recipe = ShapelessCraftingRecipe("cobblestone_recipe", ["minecraft:stone", "minecraft:stick"], "minecraft:cobblestone", 2)
door_recipe = ShapelessCraftingRecipe("door_recipe", ["minecraft:stick", ["minecraft:oak_planks", "minecraft:spruce_planks"]], "minecraft:oak_door", 1)
iron_helmet_recipe = ShapedCraftingRecipe("iron_helmet_recipe", ["iii", "   ", "iii"], {"i": "minecraft:iron_ingot"}, "minecraft:iron_helmet", 1)
burnable_diamond_recipe = FurnaceRecipe("burnable_diamond_recipe", "minecraft:diamond", "minecraft:charcoal", 1, 40)
smokable_redstone_recipe = SmokerRecipe("smokable_redstone_recipe", "minecraft:redstone", "minecraft:diamond", 100, 20)
lapis_campfire_recipe = CampfireRecipe("lapis_campfire_recipe", "minecraft:lapis_lazuli", "minecraft:cooked_beef", 100, 20)
ruby_recipe = ShapelessCraftingRecipe("ruby_recipe", ["minecraft:emerald", "minecraft:redstone"], ruby, recipe_category="equipment")
ruby_furnace_recipe = FurnaceRecipe("ruby_furnace_recipe", "minecraft:emerald", ruby, 1, 40)
moss_to_pale_recipe = StonecutterRecipe("moss_to_pale_recipe", "minecraft:moss_block", "minecraft:pale_moss_block", 1)
ruby_stonecutter_recipe = StonecutterRecipe("ruby_stonecutter_recipe", "minecraft:redstone", ruby, 1)
ruby_campfire_recipe = CampfireRecipe("ruby_campfire_recipe", "redstone", ruby, 100, 20)
ruby_smithing_tranform_recipe = SmithingTransformRecipe("ruby_transform_recipe", "gold_ingot", "iron_ingot", "redstone", ruby)

recipes: list[Recipe] = [cobble_recipe, door_recipe, iron_helmet_recipe, burnable_diamond_recipe, smokable_redstone_recipe, lapis_campfire_recipe, ruby_recipe,
                         ruby_furnace_recipe, moss_to_pale_recipe, ruby_stonecutter_recipe, ruby_campfire_recipe, ruby_smithing_tranform_recipe]
# endregion
# ============================================================================================================
# region: Custom Blocks
ruby_ore = CustomItem("ruby_ore", "minecraft:redstone_ore", "Ruby Ore", texture_path="images/ruby_ore.png", ref_book_config=RefBookConfig(category=CUSTOM_BLOCKS_REF_BOOK_CATEGORY))
ruby_ore_block = CustomBlock.from_item(ruby_ore, drops=ruby)
# ruby_ore_slab = ruby_ore_block.create_slab("stone_slab")

topaz_ore = CustomItem("topaz_ore", "minecraft:gold_ore", "Topaz Ore", texture_path="images/topaz_ore.png", ref_book_config=RefBookConfig(category=CUSTOM_BLOCKS_REF_BOOK_CATEGORY))
topaz_ore_block = CustomBlock.from_item(topaz_ore, drops=SimpleRangeLootTable("topaz_ore_drops", topaz, 1, 4))

chocolate_block_item = CustomItem("chocolate_block", "dark_oak_log", "Chocolate Block", texture_path="images/chocolate_block/top_side.png", ref_book_config=RefBookConfig(category=CUSTOM_BLOCKS_REF_BOOK_CATEGORY))
faces = {"front": "side_side", "back": "side_side", "top": "top_side", "bottom": "top_side", "left": "long_side", "right": "long_side"}
chocolate_block = CustomBlock.from_item(chocolate_block_item, block_texture=FacePaths(**{key: f"images/chocolate_block/{value}.png" for key, value in faces.items()}, horizontally_rotatable=True, vertically_rotatable=False))

debug_block_item = CustomItem("debug_block", "sponge", "Debug Block", texture_path="images/debug_block/front.png", ref_book_config=RefBookConfig(category=CUSTOM_BLOCKS_REF_BOOK_CATEGORY))
faces_strings = ["front", "back", "top", "bottom", "left", "right"]
debug_block = CustomBlock.from_item(debug_block_item, block_texture=FacePaths(**{item: f"images/debug_block/{item}.png" for item in faces_strings}, horizontally_rotatable=True, vertically_rotatable=True))

custom_blocks = [ruby_ore_block, topaz_ore_block, chocolate_block, debug_block, ]  # ruby_ore_slab
# endregion
# ============================================================================================================
emerald_loot_table = CustomLootTable("emerald_loot_table", [SimpleRangePool("emerald", 1, 3)])
# ruby_loot_table = CustomLootTable("ruby_loot_table", [SimpleRangePool(ruby, 1, 3)])
glider_helmet_loot_table = CustomLootTable("glider_helmet_loot_table", [SingleItemPool(flying_helmet)])
loot_tables = [emerald_loot_table, glider_helmet_loot_table]

blue_sword = CustomItemModelDefinition("blue_sword", ModelItemModel("minecraft:item/iron_sword", tints=[ConstantTint((0.0, 0.0, 1.0))]))
custom_item_model_definitions = [blue_sword]

datapack = Datapack(
    "PyPacks Testing", "A cool datapack", "pypacks_testing", "pack_icon.png", world_name="PyPacksWorld",
    custom_recipes=recipes,
    custom_items=custom_items,
    custom_sounds=[custom_sound],
    custom_paintings=[custom_painting],
    custom_jukebox_songs=[custom_jukebox_song],
    custom_blocks=custom_blocks,
    custom_loot_tables=loot_tables,
    custom_item_model_definitions=custom_item_model_definitions,
    # custom_advancements=[eating_advancement],
)
