from pypacks.resources.custom_item import CustomItem
from pypacks.additions.item_components import (
    AttributeModifier, Components, Cooldown, Consumable, DeathProtection, EntityData, Equippable,
    Food, Instrument, JukeboxPlayable, PotionEffect, Tool, ToolRule, UseRemainder,
)

ANCIENT_DEBRIS = CustomItem(internal_name="minecraft:ancient_debris", base_item="ancient_debris", components=Components())
APPLE = CustomItem(internal_name="minecraft:apple", base_item="apple", components=Components())
BAKED_POTATO = CustomItem(internal_name="minecraft:baked_potato", base_item="baked_potato", components=Components())
BEEF = CustomItem(internal_name="minecraft:beef", base_item="beef", components=Components())
BEETROOT = CustomItem(internal_name="minecraft:beetroot", base_item="beetroot", components=Components())
BEETROOT_SOUP = CustomItem(internal_name="minecraft:beetroot_soup", base_item="beetroot_soup", components=Components(), max_stack_size=1)
BLACK_CARPET = CustomItem(internal_name="minecraft:black_carpet", base_item="black_carpet", components=Components())
BLUE_CARPET = CustomItem(internal_name="minecraft:blue_carpet", base_item="blue_carpet", components=Components())
BOW = CustomItem(internal_name="minecraft:bow", base_item="bow", components=Components(), max_stack_size=1)
BREAD = CustomItem(internal_name="minecraft:bread", base_item="bread", components=Components())
BROWN_CARPET = CustomItem(internal_name="minecraft:brown_carpet", base_item="brown_carpet", components=Components())
BRUSH = CustomItem(internal_name="minecraft:brush", base_item="brush", components=Components(), max_stack_size=1)
CARROT = CustomItem(internal_name="minecraft:carrot", base_item="carrot", components=Components())
CARROT_ON_A_STICK = CustomItem(internal_name="minecraft:carrot_on_a_stick", base_item="carrot_on_a_stick", components=Components(), max_stack_size=1)
CARVED_PUMPKIN = CustomItem(internal_name="minecraft:carved_pumpkin", base_item="carved_pumpkin", components=Components())
CHAINMAIL_BOOTS = CustomItem(internal_name="minecraft:chainmail_boots", base_item="chainmail_boots", components=Components(), max_stack_size=1, rarity="uncommon")
CHAINMAIL_CHESTPLATE = CustomItem(internal_name="minecraft:chainmail_chestplate", base_item="chainmail_chestplate", components=Components(), max_stack_size=1, rarity="uncommon")
CHAINMAIL_HELMET = CustomItem(internal_name="minecraft:chainmail_helmet", base_item="chainmail_helmet", components=Components(), max_stack_size=1, rarity="uncommon")
CHAINMAIL_LEGGINGS = CustomItem(internal_name="minecraft:chainmail_leggings", base_item="chainmail_leggings", components=Components(), max_stack_size=1, rarity="uncommon")
CHICKEN = CustomItem(internal_name="minecraft:chicken", base_item="chicken", components=Components())
CHORUS_FRUIT = CustomItem(internal_name="minecraft:chorus_fruit", base_item="chorus_fruit", components=Components())
COD = CustomItem(internal_name="minecraft:cod", base_item="cod", components=Components())
COOKED_BEEF = CustomItem(internal_name="minecraft:cooked_beef", base_item="cooked_beef", components=Components())
COOKED_CHICKEN = CustomItem(internal_name="minecraft:cooked_chicken", base_item="cooked_chicken", components=Components())
COOKED_COD = CustomItem(internal_name="minecraft:cooked_cod", base_item="cooked_cod", components=Components())
COOKED_MUTTON = CustomItem(internal_name="minecraft:cooked_mutton", base_item="cooked_mutton", components=Components())
COOKED_PORKCHOP = CustomItem(internal_name="minecraft:cooked_porkchop", base_item="cooked_porkchop", components=Components())
COOKED_RABBIT = CustomItem(internal_name="minecraft:cooked_rabbit", base_item="cooked_rabbit", components=Components())
COOKED_SALMON = CustomItem(internal_name="minecraft:cooked_salmon", base_item="cooked_salmon", components=Components())
COOKIE = CustomItem(internal_name="minecraft:cookie", base_item="cookie", components=Components())
CREEPER_HEAD = CustomItem(internal_name="minecraft:creeper_head", base_item="creeper_head", components=Components(), rarity="uncommon")
CROSSBOW = CustomItem(internal_name="minecraft:crossbow", base_item="crossbow", components=Components(), max_stack_size=1)
CYAN_CARPET = CustomItem(internal_name="minecraft:cyan_carpet", base_item="cyan_carpet", components=Components())
DIAMOND_AXE = CustomItem(internal_name="minecraft:diamond_axe", base_item="diamond_axe", components=Components(), max_stack_size=1)
DIAMOND_BOOTS = CustomItem(internal_name="minecraft:diamond_boots", base_item="diamond_boots", components=Components(), max_stack_size=1)
DIAMOND_CHESTPLATE = CustomItem(internal_name="minecraft:diamond_chestplate", base_item="diamond_chestplate", components=Components(), max_stack_size=1)
DIAMOND_HELMET = CustomItem(internal_name="minecraft:diamond_helmet", base_item="diamond_helmet", components=Components(), max_stack_size=1)
DIAMOND_HOE = CustomItem(internal_name="minecraft:diamond_hoe", base_item="diamond_hoe", components=Components(), max_stack_size=1)
DIAMOND_HORSE_ARMOR = CustomItem(internal_name="minecraft:diamond_horse_armor", base_item="diamond_horse_armor", components=Components(), max_stack_size=1)
DIAMOND_LEGGINGS = CustomItem(internal_name="minecraft:diamond_leggings", base_item="diamond_leggings", components=Components(), max_stack_size=1)
DIAMOND_PICKAXE = CustomItem(internal_name="minecraft:diamond_pickaxe", base_item="diamond_pickaxe", components=Components(), max_stack_size=1)
DIAMOND_SHOVEL = CustomItem(internal_name="minecraft:diamond_shovel", base_item="diamond_shovel", components=Components(), max_stack_size=1)
DIAMOND_SWORD = CustomItem(internal_name="minecraft:diamond_sword", base_item="diamond_sword", components=Components(), max_stack_size=1)
DRAGON_HEAD = CustomItem(internal_name="minecraft:dragon_head", base_item="dragon_head", components=Components(), rarity="epic")
DRIED_KELP = CustomItem(internal_name="minecraft:dried_kelp", base_item="dried_kelp", components=Components())
ELYTRA = CustomItem(internal_name="minecraft:elytra", base_item="elytra", components=Components(), max_stack_size=1, rarity="epic")
ENCHANTED_GOLDEN_APPLE = CustomItem(internal_name="minecraft:enchanted_golden_apple", base_item="enchanted_golden_apple", components=Components(), rarity="rare")
ENDER_PEARL = CustomItem(internal_name="minecraft:ender_pearl", base_item="ender_pearl", components=Components(), max_stack_size=16)
FISHING_ROD = CustomItem(internal_name="minecraft:fishing_rod", base_item="fishing_rod", components=Components(), max_stack_size=1)
FLINT_AND_STEEL = CustomItem(internal_name="minecraft:flint_and_steel", base_item="flint_and_steel", components=Components(), max_stack_size=1)
GLOW_BERRIES = CustomItem(internal_name="minecraft:glow_berries", base_item="glow_berries", components=Components())
GOLDEN_APPLE = CustomItem(internal_name="minecraft:golden_apple", base_item="golden_apple", components=Components())
GOLDEN_AXE = CustomItem(internal_name="minecraft:golden_axe", base_item="golden_axe", components=Components(), max_stack_size=1)
GOLDEN_BOOTS = CustomItem(internal_name="minecraft:golden_boots", base_item="golden_boots", components=Components(), max_stack_size=1)
GOLDEN_CARROT = CustomItem(internal_name="minecraft:golden_carrot", base_item="golden_carrot", components=Components())
GOLDEN_CHESTPLATE = CustomItem(internal_name="minecraft:golden_chestplate", base_item="golden_chestplate", components=Components(), max_stack_size=1)
GOLDEN_HELMET = CustomItem(internal_name="minecraft:golden_helmet", base_item="golden_helmet", components=Components(), max_stack_size=1)
GOLDEN_HOE = CustomItem(internal_name="minecraft:golden_hoe", base_item="golden_hoe", components=Components(), max_stack_size=1)
GOLDEN_HORSE_ARMOR = CustomItem(internal_name="minecraft:golden_horse_armor", base_item="golden_horse_armor", components=Components(), max_stack_size=1)
GOLDEN_LEGGINGS = CustomItem(internal_name="minecraft:golden_leggings", base_item="golden_leggings", components=Components(), max_stack_size=1)
GOLDEN_PICKAXE = CustomItem(internal_name="minecraft:golden_pickaxe", base_item="golden_pickaxe", components=Components(), max_stack_size=1)
GOLDEN_SHOVEL = CustomItem(internal_name="minecraft:golden_shovel", base_item="golden_shovel", components=Components(), max_stack_size=1)
GOLDEN_SWORD = CustomItem(internal_name="minecraft:golden_sword", base_item="golden_sword", components=Components(), max_stack_size=1)
GRAY_CARPET = CustomItem(internal_name="minecraft:gray_carpet", base_item="gray_carpet", components=Components())
GREEN_CARPET = CustomItem(internal_name="minecraft:green_carpet", base_item="green_carpet", components=Components())
HONEY_BOTTLE = CustomItem(internal_name="minecraft:honey_bottle", base_item="honey_bottle", components=Components(), max_stack_size=16)
IRON_AXE = CustomItem(internal_name="minecraft:iron_axe", base_item="iron_axe", components=Components(), max_stack_size=1)
IRON_BOOTS = CustomItem(internal_name="minecraft:iron_boots", base_item="iron_boots", components=Components(), max_stack_size=1)
IRON_CHESTPLATE = CustomItem(internal_name="minecraft:iron_chestplate", base_item="iron_chestplate", components=Components(), max_stack_size=1)
IRON_HELMET = CustomItem(internal_name="minecraft:iron_helmet", base_item="iron_helmet", components=Components(), max_stack_size=1)
IRON_HOE = CustomItem(internal_name="minecraft:iron_hoe", base_item="iron_hoe", components=Components(), max_stack_size=1)
IRON_HORSE_ARMOR = CustomItem(internal_name="minecraft:iron_horse_armor", base_item="iron_horse_armor", components=Components(), max_stack_size=1)
IRON_LEGGINGS = CustomItem(internal_name="minecraft:iron_leggings", base_item="iron_leggings", components=Components(), max_stack_size=1)
IRON_PICKAXE = CustomItem(internal_name="minecraft:iron_pickaxe", base_item="iron_pickaxe", components=Components(), max_stack_size=1)
IRON_SHOVEL = CustomItem(internal_name="minecraft:iron_shovel", base_item="iron_shovel", components=Components(), max_stack_size=1)
IRON_SWORD = CustomItem(internal_name="minecraft:iron_sword", base_item="iron_sword", components=Components(), max_stack_size=1)
LEATHER_BOOTS = CustomItem(internal_name="minecraft:leather_boots", base_item="leather_boots", components=Components(), max_stack_size=1)
LEATHER_CHESTPLATE = CustomItem(internal_name="minecraft:leather_chestplate", base_item="leather_chestplate", components=Components(), max_stack_size=1)
LEATHER_HELMET = CustomItem(internal_name="minecraft:leather_helmet", base_item="leather_helmet", components=Components(), max_stack_size=1)
LEATHER_HORSE_ARMOR = CustomItem(internal_name="minecraft:leather_horse_armor", base_item="leather_horse_armor", components=Components(), max_stack_size=1)
LEATHER_LEGGINGS = CustomItem(internal_name="minecraft:leather_leggings", base_item="leather_leggings", components=Components(), max_stack_size=1)
LIGHT_BLUE_CARPET = CustomItem(internal_name="minecraft:light_blue_carpet", base_item="light_blue_carpet", components=Components())
LIGHT_GRAY_CARPET = CustomItem(internal_name="minecraft:light_gray_carpet", base_item="light_gray_carpet", components=Components())
LIME_CARPET = CustomItem(internal_name="minecraft:lime_carpet", base_item="lime_carpet", components=Components())
MACE = CustomItem(internal_name="minecraft:mace", base_item="mace", components=Components(), max_stack_size=1, rarity="epic")
MAGENTA_CARPET = CustomItem(internal_name="minecraft:magenta_carpet", base_item="magenta_carpet", components=Components())
MELON_SLICE = CustomItem(internal_name="minecraft:melon_slice", base_item="melon_slice", components=Components())
MILK_BUCKET = CustomItem(internal_name="minecraft:milk_bucket", base_item="milk_bucket", components=Components(), max_stack_size=1)
MUSHROOM_STEW = CustomItem(internal_name="minecraft:mushroom_stew", base_item="mushroom_stew", components=Components(), max_stack_size=1)
MUSIC_DISC_11 = CustomItem(internal_name="minecraft:music_disc_11", base_item="music_disc_11", components=Components(), max_stack_size=1, rarity="uncommon")
MUSIC_DISC_13 = CustomItem(internal_name="minecraft:music_disc_13", base_item="music_disc_13", components=Components(), max_stack_size=1, rarity="uncommon")
MUSIC_DISC_5 = CustomItem(internal_name="minecraft:music_disc_5", base_item="music_disc_5", components=Components(), max_stack_size=1, rarity="uncommon")
MUSIC_DISC_BLOCKS = CustomItem(internal_name="minecraft:music_disc_blocks", base_item="music_disc_blocks", components=Components(), max_stack_size=1, rarity="uncommon")
MUSIC_DISC_CAT = CustomItem(internal_name="minecraft:music_disc_cat", base_item="music_disc_cat", components=Components(), max_stack_size=1, rarity="uncommon")
MUSIC_DISC_CHIRP = CustomItem(internal_name="minecraft:music_disc_chirp", base_item="music_disc_chirp", components=Components(), max_stack_size=1, rarity="uncommon")
MUSIC_DISC_CREATOR = CustomItem(internal_name="minecraft:music_disc_creator", base_item="music_disc_creator", components=Components(), max_stack_size=1, rarity="rare")
MUSIC_DISC_CREATOR_MUSIC_BOX = CustomItem(internal_name="minecraft:music_disc_creator_music_box", base_item="music_disc_creator_music_box", components=Components(), max_stack_size=1, rarity="uncommon")
MUSIC_DISC_FAR = CustomItem(internal_name="minecraft:music_disc_far", base_item="music_disc_far", components=Components(), max_stack_size=1, rarity="uncommon")
MUSIC_DISC_MALL = CustomItem(internal_name="minecraft:music_disc_mall", base_item="music_disc_mall", components=Components(), max_stack_size=1, rarity="uncommon")
MUSIC_DISC_MELLOHI = CustomItem(internal_name="minecraft:music_disc_mellohi", base_item="music_disc_mellohi", components=Components(), max_stack_size=1, rarity="uncommon")
MUSIC_DISC_OTHERSIDE = CustomItem(internal_name="minecraft:music_disc_otherside", base_item="music_disc_otherside", components=Components(), max_stack_size=1, rarity="rare")
MUSIC_DISC_PIGSTEP = CustomItem(internal_name="minecraft:music_disc_pigstep", base_item="music_disc_pigstep", components=Components(), max_stack_size=1, rarity="rare")
MUSIC_DISC_PRECIPICE = CustomItem(internal_name="minecraft:music_disc_precipice", base_item="music_disc_precipice", components=Components(), max_stack_size=1, rarity="uncommon")
MUSIC_DISC_RELIC = CustomItem(internal_name="minecraft:music_disc_relic", base_item="music_disc_relic", components=Components(), max_stack_size=1, rarity="uncommon")
MUSIC_DISC_STAL = CustomItem(internal_name="minecraft:music_disc_stal", base_item="music_disc_stal", components=Components(), max_stack_size=1, rarity="uncommon")
MUSIC_DISC_STRAD = CustomItem(internal_name="minecraft:music_disc_strad", base_item="music_disc_strad", components=Components(), max_stack_size=1, rarity="uncommon")
MUSIC_DISC_WAIT = CustomItem(internal_name="minecraft:music_disc_wait", base_item="music_disc_wait", components=Components(), max_stack_size=1, rarity="uncommon")
MUSIC_DISC_WARD = CustomItem(internal_name="minecraft:music_disc_ward", base_item="music_disc_ward", components=Components(), max_stack_size=1, rarity="uncommon")
MUTTON = CustomItem(internal_name="minecraft:mutton", base_item="mutton", components=Components())
NETHER_STAR = CustomItem(internal_name="minecraft:nether_star", base_item="nether_star", components=Components(), rarity="rare")
NETHERITE_AXE = CustomItem(internal_name="minecraft:netherite_axe", base_item="netherite_axe", components=Components(), max_stack_size=1)
NETHERITE_BLOCK = CustomItem(internal_name="minecraft:netherite_block", base_item="netherite_block", components=Components())
NETHERITE_BOOTS = CustomItem(internal_name="minecraft:netherite_boots", base_item="netherite_boots", components=Components(), max_stack_size=1)
NETHERITE_CHESTPLATE = CustomItem(internal_name="minecraft:netherite_chestplate", base_item="netherite_chestplate", components=Components(), max_stack_size=1)
NETHERITE_HELMET = CustomItem(internal_name="minecraft:netherite_helmet", base_item="netherite_helmet", components=Components(), max_stack_size=1)
NETHERITE_HOE = CustomItem(internal_name="minecraft:netherite_hoe", base_item="netherite_hoe", components=Components(), max_stack_size=1)
NETHERITE_INGOT = CustomItem(internal_name="minecraft:netherite_ingot", base_item="netherite_ingot", components=Components())
NETHERITE_LEGGINGS = CustomItem(internal_name="minecraft:netherite_leggings", base_item="netherite_leggings", components=Components(), max_stack_size=1)
NETHERITE_PICKAXE = CustomItem(internal_name="minecraft:netherite_pickaxe", base_item="netherite_pickaxe", components=Components(), max_stack_size=1)
NETHERITE_SCRAP = CustomItem(internal_name="minecraft:netherite_scrap", base_item="netherite_scrap", components=Components())
NETHERITE_SHOVEL = CustomItem(internal_name="minecraft:netherite_shovel", base_item="netherite_shovel", components=Components(), max_stack_size=1)
NETHERITE_SWORD = CustomItem(internal_name="minecraft:netherite_sword", base_item="netherite_sword", components=Components(), max_stack_size=1)
OMINOUS_BOTTLE = CustomItem(internal_name="minecraft:ominous_bottle", base_item="ominous_bottle", components=Components(), rarity="uncommon")
ORANGE_CARPET = CustomItem(internal_name="minecraft:orange_carpet", base_item="orange_carpet", components=Components())
PIGLIN_HEAD = CustomItem(internal_name="minecraft:piglin_head", base_item="piglin_head", components=Components(), rarity="uncommon")
PINK_CARPET = CustomItem(internal_name="minecraft:pink_carpet", base_item="pink_carpet", components=Components())
PLAYER_HEAD = CustomItem(internal_name="minecraft:player_head", base_item="player_head", components=Components(), rarity="uncommon")
POISONOUS_POTATO = CustomItem(internal_name="minecraft:poisonous_potato", base_item="poisonous_potato", components=Components())
PORKCHOP = CustomItem(internal_name="minecraft:porkchop", base_item="porkchop", components=Components())
POTATO = CustomItem(internal_name="minecraft:potato", base_item="potato", components=Components())
POTION = CustomItem(internal_name="minecraft:potion", base_item="potion", components=Components(), max_stack_size=1)
PUFFERFISH = CustomItem(internal_name="minecraft:pufferfish", base_item="pufferfish", components=Components())
PUMPKIN_PIE = CustomItem(internal_name="minecraft:pumpkin_pie", base_item="pumpkin_pie", components=Components())
PURPLE_CARPET = CustomItem(internal_name="minecraft:purple_carpet", base_item="purple_carpet", components=Components())
RABBIT = CustomItem(internal_name="minecraft:rabbit", base_item="rabbit", components=Components())
RABBIT_STEW = CustomItem(internal_name="minecraft:rabbit_stew", base_item="rabbit_stew", components=Components(), max_stack_size=1)
RED_CARPET = CustomItem(internal_name="minecraft:red_carpet", base_item="red_carpet", components=Components())
ROTTEN_FLESH = CustomItem(internal_name="minecraft:rotten_flesh", base_item="rotten_flesh", components=Components())
SADDLE = CustomItem(internal_name="minecraft:saddle", base_item="saddle", components=Components(), max_stack_size=1)
SALMON = CustomItem(internal_name="minecraft:salmon", base_item="salmon", components=Components())
SHEARS = CustomItem(internal_name="minecraft:shears", base_item="shears", components=Components(), max_stack_size=1)
SHIELD = CustomItem(internal_name="minecraft:shield", base_item="shield", components=Components(), max_stack_size=1)
SKELETON_SKULL = CustomItem(internal_name="minecraft:skeleton_skull", base_item="skeleton_skull", components=Components(), rarity="uncommon")
SPIDER_EYE = CustomItem(internal_name="minecraft:spider_eye", base_item="spider_eye", components=Components())
STONE_AXE = CustomItem(internal_name="minecraft:stone_axe", base_item="stone_axe", components=Components(), max_stack_size=1)
STONE_HOE = CustomItem(internal_name="minecraft:stone_hoe", base_item="stone_hoe", components=Components(), max_stack_size=1)
STONE_PICKAXE = CustomItem(internal_name="minecraft:stone_pickaxe", base_item="stone_pickaxe", components=Components(), max_stack_size=1)
STONE_SHOVEL = CustomItem(internal_name="minecraft:stone_shovel", base_item="stone_shovel", components=Components(), max_stack_size=1)
STONE_SWORD = CustomItem(internal_name="minecraft:stone_sword", base_item="stone_sword", components=Components(), max_stack_size=1)
SUSPICIOUS_STEW = CustomItem(internal_name="minecraft:suspicious_stew", base_item="suspicious_stew", components=Components(), max_stack_size=1)
SWEET_BERRIES = CustomItem(internal_name="minecraft:sweet_berries", base_item="sweet_berries", components=Components())
TOTEM_OF_UNDYING = CustomItem(internal_name="minecraft:totem_of_undying", base_item="totem_of_undying", components=Components(), max_stack_size=1, rarity="uncommon")
TRIDENT = CustomItem(internal_name="minecraft:trident", base_item="trident", components=Components(), max_stack_size=1, rarity="rare")
TROPICAL_FISH = CustomItem(internal_name="minecraft:tropical_fish", base_item="tropical_fish", components=Components())
TURTLE_HELMET = CustomItem(internal_name="minecraft:turtle_helmet", base_item="turtle_helmet", components=Components(), max_stack_size=1)
WARPED_FUNGUS_ON_A_STICK = CustomItem(internal_name="minecraft:warped_fungus_on_a_stick", base_item="warped_fungus_on_a_stick", components=Components(), max_stack_size=1)
WHITE_CARPET = CustomItem(internal_name="minecraft:white_carpet", base_item="white_carpet", components=Components())
WIND_CHARGE = CustomItem(internal_name="minecraft:wind_charge", base_item="wind_charge", components=Components())
WITHER_SKELETON_SKULL = CustomItem(internal_name="minecraft:wither_skeleton_skull", base_item="wither_skeleton_skull", components=Components(), rarity="rare")
WOLF_ARMOR = CustomItem(internal_name="minecraft:wolf_armor", base_item="wolf_armor", components=Components(), max_stack_size=1)
WOODEN_AXE = CustomItem(internal_name="minecraft:wooden_axe", base_item="wooden_axe", components=Components(), max_stack_size=1)
WOODEN_HOE = CustomItem(internal_name="minecraft:wooden_hoe", base_item="wooden_hoe", components=Components(), max_stack_size=1)
WOODEN_PICKAXE = CustomItem(internal_name="minecraft:wooden_pickaxe", base_item="wooden_pickaxe", components=Components(), max_stack_size=1)
WOODEN_SHOVEL = CustomItem(internal_name="minecraft:wooden_shovel", base_item="wooden_shovel", components=Components(), max_stack_size=1)
WOODEN_SWORD = CustomItem(internal_name="minecraft:wooden_sword", base_item="wooden_sword", components=Components(), max_stack_size=1)
YELLOW_CARPET = CustomItem(internal_name="minecraft:yellow_carpet", base_item="yellow_carpet", components=Components())
ZOMBIE_HEAD = CustomItem(internal_name="minecraft:zombie_head", base_item="zombie_head", components=Components(), rarity="uncommon")

# Manually added:
GOAT_HORN_PONDER = CustomItem(internal_name="minecraft:goat_horn_ponder", base_item="minecraft:goat_horn", components=Components(instrument=Instrument(sound='minecraft:item.goat_horn.sound.0')), max_stack_size=1)
GOAT_HORN_SING = CustomItem(internal_name="minecraft:goat_horn_sing", base_item="minecraft:goat_horn", components=Components(instrument=Instrument(sound='minecraft:item.goat_horn.sound.1')), max_stack_size=1)
GOAT_HORN_SEEK = CustomItem(internal_name="minecraft:goat_horn_seek", base_item="minecraft:goat_horn", components=Components(instrument=Instrument(sound='minecraft:item.goat_horn.sound.2')), max_stack_size=1)
GOAT_HORN_FEEL = CustomItem(internal_name="minecraft:goat_horn_feel", base_item="minecraft:goat_horn", components=Components(instrument=Instrument(sound='minecraft:item.goat_horn.sound.3')), max_stack_size=1)
GOAT_HORN_ADMIRE = CustomItem(internal_name="minecraft:goat_horn_admire", base_item="minecraft:goat_horn", components=Components(instrument=Instrument(sound='minecraft:item.goat_horn.sound.4')), max_stack_size=1)
GOAT_HORN_CALL = CustomItem(internal_name="minecraft:goat_horn_call", base_item="minecraft:goat_horn", components=Components(instrument=Instrument(sound='minecraft:item.goat_horn.sound.5')), max_stack_size=1)
GOAT_HORN_YEARN = CustomItem(internal_name="minecraft:goat_horn_yearn", base_item="minecraft:goat_horn", components=Components(instrument=Instrument(sound='minecraft:item.goat_horn.sound.6')), max_stack_size=1)
GOAT_HORN_DREAM = CustomItem(internal_name="minecraft:goat_horn_dream", base_item="minecraft:goat_horn", components=Components(instrument=Instrument(sound='minecraft:item.goat_horn.sound.7')), max_stack_size=1)
KEBAB_PAINTING = CustomItem(internal_name="minecraft:kebab_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:kebab'})), max_stack_size=1)
AZTEC_PAINTING = CustomItem(internal_name="minecraft:aztec_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:aztec'})), max_stack_size=1)
ALBANIA_PAINTING = CustomItem(internal_name="minecraft:albania_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:albania'})), max_stack_size=1)
AZTEC2_PAINTING = CustomItem(internal_name="minecraft:aztec2_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:aztec2'})), max_stack_size=1)
BOMB_PAINTING = CustomItem(internal_name="minecraft:bomb_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:bomb'})), max_stack_size=1)
PLANT_PAINTING = CustomItem(internal_name="minecraft:plant_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:plant'})), max_stack_size=1)
WASTELAND_PAINTING = CustomItem(internal_name="minecraft:wasteland_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:wasteland'})), max_stack_size=1)
MEDITATIVE_PAINTING = CustomItem(internal_name="minecraft:meditative_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:meditative'})), max_stack_size=1)
WANDERER_PAINTING = CustomItem(internal_name="minecraft:wanderer_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:wanderer'})), max_stack_size=1)
GRAHAM_PAINTING = CustomItem(internal_name="minecraft:graham_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:graham'})), max_stack_size=1)
PRAIRIE_RIDE_PAINTING = CustomItem(internal_name="minecraft:prairie_ride_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:prairie_ride'})), max_stack_size=1)
POOL_PAINTING = CustomItem(internal_name="minecraft:pool_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:pool'})), max_stack_size=1)
COURBET_PAINTING = CustomItem(internal_name="minecraft:courbet_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:courbet'})), max_stack_size=1)
SUNSET_PAINTING = CustomItem(internal_name="minecraft:sunset_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:sunset'})), max_stack_size=1)
SEA_PAINTING = CustomItem(internal_name="minecraft:sea_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:sea'})), max_stack_size=1)
CREEBET_PAINTING = CustomItem(internal_name="minecraft:creebet_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:creebet'})), max_stack_size=1)
MATCH_PAINTING = CustomItem(internal_name="minecraft:match_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:match'})), max_stack_size=1)
BUST_PAINTING = CustomItem(internal_name="minecraft:bust_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:bust'})), max_stack_size=1)
STAGE_PAINTING = CustomItem(internal_name="minecraft:stage_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:stage'})), max_stack_size=1)
VOID_PAINTING = CustomItem(internal_name="minecraft:void_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:void'})), max_stack_size=1)
SKULL_AND_ROSES_PAINTING = CustomItem(internal_name="minecraft:skull_and_roses_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:skull_and_roses'})), max_stack_size=1)
WITHER_PAINTING = CustomItem(internal_name="minecraft:wither_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:wither'})), max_stack_size=1)
BAROQUE_PAINTING = CustomItem(internal_name="minecraft:baroque_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:baroque'})), max_stack_size=1)
HUMBLE_PAINTING = CustomItem(internal_name="minecraft:humble_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:humble'})), max_stack_size=1)
BOUQUET_PAINTING = CustomItem(internal_name="minecraft:bouquet_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:bouquet'})), max_stack_size=1)
CAVEBIRD_PAINTING = CustomItem(internal_name="minecraft:cavebird_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:cavebird'})), max_stack_size=1)
COTAN_PAINTING = CustomItem(internal_name="minecraft:cotan_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:cotan'})), max_stack_size=1)
ENDBOSS_PAINTING = CustomItem(internal_name="minecraft:endboss_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:endboss'})), max_stack_size=1)
FERN_PAINTING = CustomItem(internal_name="minecraft:fern_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:fern'})), max_stack_size=1)
OWLEMONS_PAINTING = CustomItem(internal_name="minecraft:owlemons_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:owlemons'})), max_stack_size=1)
SUNFLOWERS_PAINTING = CustomItem(internal_name="minecraft:sunflowers_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:sunflowers'})), max_stack_size=1)
TIDES_PAINTING = CustomItem(internal_name="minecraft:tides_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:tides'})), max_stack_size=1)
BACKYARD_PAINTING = CustomItem(internal_name="minecraft:backyard_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:backyard'})), max_stack_size=1)
POND_PAINTING = CustomItem(internal_name="minecraft:pond_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:pond'})), max_stack_size=1)
FIGHTERS_PAINTING = CustomItem(internal_name="minecraft:fighters_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:fighters'})), max_stack_size=1)
CHANGING_PAINTING = CustomItem(internal_name="minecraft:changing_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:changing'})), max_stack_size=1)
FINDING_PAINTING = CustomItem(internal_name="minecraft:finding_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:finding'})), max_stack_size=1)
LOWMIST_PAINTING = CustomItem(internal_name="minecraft:lowmist_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:lowmist'})), max_stack_size=1)
PASSAGE_PAINTING = CustomItem(internal_name="minecraft:passage_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:passage'})), max_stack_size=1)
MORTAL_COIL_PAINTING = CustomItem(internal_name="minecraft:mortal_coil_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:mortal_coil'})), max_stack_size=1)
DONKEY_KONG_PAINTING = CustomItem(internal_name="minecraft:donkey_kong_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:donkey_kong'})), max_stack_size=1)
POINTER_PAINTING = CustomItem(internal_name="minecraft:pointer_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:pointer'})), max_stack_size=1)
PIGSCENE_PAINTING = CustomItem(internal_name="minecraft:pigscene_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:pigscene'})), max_stack_size=1)
BURNING_SKULL_PAINTING = CustomItem(internal_name="minecraft:burning_skull_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:burning_skull'})), max_stack_size=1)
ORB_PAINTING = CustomItem(internal_name="minecraft:orb_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:orb'})), max_stack_size=1)
UNPACKED_PAINTING = CustomItem(internal_name="minecraft:unpacked_painting", base_item="minecraft:painting", components=Components(entity_data=EntityData(data={'id': 'minecraft:painting', 'variant': 'minecraft:unpacked'})), max_stack_size=1)

DEFAULT_ITEMS = {
    "ANCIENT_DEBRIS": ANCIENT_DEBRIS,
    "APPLE": APPLE,
    "BAKED_POTATO": BAKED_POTATO,
    "BEEF": BEEF,
    "BEETROOT": BEETROOT,
    "BEETROOT_SOUP": BEETROOT_SOUP,
    "BLACK_CARPET": BLACK_CARPET,
    "BLUE_CARPET": BLUE_CARPET,
    "BOW": BOW,
    "BREAD": BREAD,
    "BROWN_CARPET": BROWN_CARPET,
    "BRUSH": BRUSH,
    "CARROT": CARROT,
    "CARROT_ON_A_STICK": CARROT_ON_A_STICK,
    "CARVED_PUMPKIN": CARVED_PUMPKIN,
    "CHAINMAIL_BOOTS": CHAINMAIL_BOOTS,
    "CHAINMAIL_CHESTPLATE": CHAINMAIL_CHESTPLATE,
    "CHAINMAIL_HELMET": CHAINMAIL_HELMET,
    "CHAINMAIL_LEGGINGS": CHAINMAIL_LEGGINGS,
    "CHICKEN": CHICKEN,
    "CHORUS_FRUIT": CHORUS_FRUIT,
    "COD": COD,
    "COOKED_BEEF": COOKED_BEEF,
    "COOKED_CHICKEN": COOKED_CHICKEN,
    "COOKED_COD": COOKED_COD,
    "COOKED_MUTTON": COOKED_MUTTON,
    "COOKED_PORKCHOP": COOKED_PORKCHOP,
    "COOKED_RABBIT": COOKED_RABBIT,
    "COOKED_SALMON": COOKED_SALMON,
    "COOKIE": COOKIE,
    "CREEPER_HEAD": CREEPER_HEAD,
    "CROSSBOW": CROSSBOW,
    "CYAN_CARPET": CYAN_CARPET,
    "DIAMOND_AXE": DIAMOND_AXE,
    "DIAMOND_BOOTS": DIAMOND_BOOTS,
    "DIAMOND_CHESTPLATE": DIAMOND_CHESTPLATE,
    "DIAMOND_HELMET": DIAMOND_HELMET,
    "DIAMOND_HOE": DIAMOND_HOE,
    "DIAMOND_HORSE_ARMOR": DIAMOND_HORSE_ARMOR,
    "DIAMOND_LEGGINGS": DIAMOND_LEGGINGS,
    "DIAMOND_PICKAXE": DIAMOND_PICKAXE,
    "DIAMOND_SHOVEL": DIAMOND_SHOVEL,
    "DIAMOND_SWORD": DIAMOND_SWORD,
    "DRAGON_HEAD": DRAGON_HEAD,
    "DRIED_KELP": DRIED_KELP,
    "ELYTRA": ELYTRA,
    "ENCHANTED_GOLDEN_APPLE": ENCHANTED_GOLDEN_APPLE,
    "ENDER_PEARL": ENDER_PEARL,
    "FISHING_ROD": FISHING_ROD,
    "FLINT_AND_STEEL": FLINT_AND_STEEL,
    "GLOW_BERRIES": GLOW_BERRIES,
    "GOLDEN_APPLE": GOLDEN_APPLE,
    "GOLDEN_AXE": GOLDEN_AXE,
    "GOLDEN_BOOTS": GOLDEN_BOOTS,
    "GOLDEN_CARROT": GOLDEN_CARROT,
    "GOLDEN_CHESTPLATE": GOLDEN_CHESTPLATE,
    "GOLDEN_HELMET": GOLDEN_HELMET,
    "GOLDEN_HOE": GOLDEN_HOE,
    "GOLDEN_HORSE_ARMOR": GOLDEN_HORSE_ARMOR,
    "GOLDEN_LEGGINGS": GOLDEN_LEGGINGS,
    "GOLDEN_PICKAXE": GOLDEN_PICKAXE,
    "GOLDEN_SHOVEL": GOLDEN_SHOVEL,
    "GOLDEN_SWORD": GOLDEN_SWORD,
    "GRAY_CARPET": GRAY_CARPET,
    "GREEN_CARPET": GREEN_CARPET,
    "HONEY_BOTTLE": HONEY_BOTTLE,
    "IRON_AXE": IRON_AXE,
    "IRON_BOOTS": IRON_BOOTS,
    "IRON_CHESTPLATE": IRON_CHESTPLATE,
    "IRON_HELMET": IRON_HELMET,
    "IRON_HOE": IRON_HOE,
    "IRON_HORSE_ARMOR": IRON_HORSE_ARMOR,
    "IRON_LEGGINGS": IRON_LEGGINGS,
    "IRON_PICKAXE": IRON_PICKAXE,
    "IRON_SHOVEL": IRON_SHOVEL,
    "IRON_SWORD": IRON_SWORD,
    "LEATHER_BOOTS": LEATHER_BOOTS,
    "LEATHER_CHESTPLATE": LEATHER_CHESTPLATE,
    "LEATHER_HELMET": LEATHER_HELMET,
    "LEATHER_HORSE_ARMOR": LEATHER_HORSE_ARMOR,
    "LEATHER_LEGGINGS": LEATHER_LEGGINGS,
    "LIGHT_BLUE_CARPET": LIGHT_BLUE_CARPET,
    "LIGHT_GRAY_CARPET": LIGHT_GRAY_CARPET,
    "LIME_CARPET": LIME_CARPET,
    "MACE": MACE,
    "MAGENTA_CARPET": MAGENTA_CARPET,
    "MELON_SLICE": MELON_SLICE,
    "MILK_BUCKET": MILK_BUCKET,
    "MUSHROOM_STEW": MUSHROOM_STEW,
    "MUSIC_DISC_11": MUSIC_DISC_11,
    "MUSIC_DISC_13": MUSIC_DISC_13,
    "MUSIC_DISC_5": MUSIC_DISC_5,
    "MUSIC_DISC_BLOCKS": MUSIC_DISC_BLOCKS,
    "MUSIC_DISC_CAT": MUSIC_DISC_CAT,
    "MUSIC_DISC_CHIRP": MUSIC_DISC_CHIRP,
    "MUSIC_DISC_CREATOR": MUSIC_DISC_CREATOR,
    "MUSIC_DISC_CREATOR_MUSIC_BOX": MUSIC_DISC_CREATOR_MUSIC_BOX,
    "MUSIC_DISC_FAR": MUSIC_DISC_FAR,
    "MUSIC_DISC_MALL": MUSIC_DISC_MALL,
    "MUSIC_DISC_MELLOHI": MUSIC_DISC_MELLOHI,
    "MUSIC_DISC_OTHERSIDE": MUSIC_DISC_OTHERSIDE,
    "MUSIC_DISC_PIGSTEP": MUSIC_DISC_PIGSTEP,
    "MUSIC_DISC_PRECIPICE": MUSIC_DISC_PRECIPICE,
    "MUSIC_DISC_RELIC": MUSIC_DISC_RELIC,
    "MUSIC_DISC_STAL": MUSIC_DISC_STAL,
    "MUSIC_DISC_STRAD": MUSIC_DISC_STRAD,
    "MUSIC_DISC_WAIT": MUSIC_DISC_WAIT,
    "MUSIC_DISC_WARD": MUSIC_DISC_WARD,
    "MUTTON": MUTTON,
    "NETHER_STAR": NETHER_STAR,
    "NETHERITE_AXE": NETHERITE_AXE,
    "NETHERITE_BLOCK": NETHERITE_BLOCK,
    "NETHERITE_BOOTS": NETHERITE_BOOTS,
    "NETHERITE_CHESTPLATE": NETHERITE_CHESTPLATE,
    "NETHERITE_HELMET": NETHERITE_HELMET,
    "NETHERITE_HOE": NETHERITE_HOE,
    "NETHERITE_INGOT": NETHERITE_INGOT,
    "NETHERITE_LEGGINGS": NETHERITE_LEGGINGS,
    "NETHERITE_PICKAXE": NETHERITE_PICKAXE,
    "NETHERITE_SCRAP": NETHERITE_SCRAP,
    "NETHERITE_SHOVEL": NETHERITE_SHOVEL,
    "NETHERITE_SWORD": NETHERITE_SWORD,
    "OMINOUS_BOTTLE": OMINOUS_BOTTLE,
    "ORANGE_CARPET": ORANGE_CARPET,
    "PIGLIN_HEAD": PIGLIN_HEAD,
    "PINK_CARPET": PINK_CARPET,
    "PLAYER_HEAD": PLAYER_HEAD,
    "POISONOUS_POTATO": POISONOUS_POTATO,
    "PORKCHOP": PORKCHOP,
    "POTATO": POTATO,
    "POTION": POTION,
    "PUFFERFISH": PUFFERFISH,
    "PUMPKIN_PIE": PUMPKIN_PIE,
    "PURPLE_CARPET": PURPLE_CARPET,
    "RABBIT": RABBIT,
    "RABBIT_STEW": RABBIT_STEW,
    "RED_CARPET": RED_CARPET,
    "ROTTEN_FLESH": ROTTEN_FLESH,
    "SADDLE": SADDLE,
    "SALMON": SALMON,
    "SHEARS": SHEARS,
    "SHIELD": SHIELD,
    "SKELETON_SKULL": SKELETON_SKULL,
    "SPIDER_EYE": SPIDER_EYE,
    "STONE_AXE": STONE_AXE,
    "STONE_HOE": STONE_HOE,
    "STONE_PICKAXE": STONE_PICKAXE,
    "STONE_SHOVEL": STONE_SHOVEL,
    "STONE_SWORD": STONE_SWORD,
    "SUSPICIOUS_STEW": SUSPICIOUS_STEW,
    "SWEET_BERRIES": SWEET_BERRIES,
    "TOTEM_OF_UNDYING": TOTEM_OF_UNDYING,
    "TRIDENT": TRIDENT,
    "TROPICAL_FISH": TROPICAL_FISH,
    "TURTLE_HELMET": TURTLE_HELMET,
    "WARPED_FUNGUS_ON_A_STICK": WARPED_FUNGUS_ON_A_STICK,
    "WHITE_CARPET": WHITE_CARPET,
    "WIND_CHARGE": WIND_CHARGE,
    "WITHER_SKELETON_SKULL": WITHER_SKELETON_SKULL,
    "WOLF_ARMOR": WOLF_ARMOR,
    "WOODEN_AXE": WOODEN_AXE,
    "WOODEN_HOE": WOODEN_HOE,
    "WOODEN_PICKAXE": WOODEN_PICKAXE,
    "WOODEN_SHOVEL": WOODEN_SHOVEL,
    "WOODEN_SWORD": WOODEN_SWORD,
    "YELLOW_CARPET": YELLOW_CARPET,
    "ZOMBIE_HEAD": ZOMBIE_HEAD,
    "GOAT_HORN_PONDER": GOAT_HORN_PONDER,
    "GOAT_HORN_SING": GOAT_HORN_SING,
    "GOAT_HORN_SEEK": GOAT_HORN_SEEK,
    "GOAT_HORN_FEEL": GOAT_HORN_FEEL,
    "GOAT_HORN_ADMIRE": GOAT_HORN_ADMIRE,
    "GOAT_HORN_CALL": GOAT_HORN_CALL,
    "GOAT_HORN_YEARN": GOAT_HORN_YEARN,
    "GOAT_HORN_DREAM": GOAT_HORN_DREAM,
    "KEBAB_PAINTING": KEBAB_PAINTING,
    "AZTEC_PAINTING": AZTEC_PAINTING,
    "ALBANIA_PAINTING": ALBANIA_PAINTING,
    "AZTEC2_PAINTING": AZTEC2_PAINTING,
    "BOMB_PAINTING": BOMB_PAINTING,
    "PLANT_PAINTING": PLANT_PAINTING,
    "WASTELAND_PAINTING": WASTELAND_PAINTING,
    "MEDITATIVE_PAINTING": MEDITATIVE_PAINTING,
    "WANDERER_PAINTING": WANDERER_PAINTING,
    "GRAHAM_PAINTING": GRAHAM_PAINTING,
    "PRAIRIE_RIDE_PAINTING": PRAIRIE_RIDE_PAINTING,
    "POOL_PAINTING": POOL_PAINTING,
    "COURBET_PAINTING": COURBET_PAINTING,
    "SUNSET_PAINTING": SUNSET_PAINTING,
    "SEA_PAINTING": SEA_PAINTING,
    "CREEBET_PAINTING": CREEBET_PAINTING,
    "MATCH_PAINTING": MATCH_PAINTING,
    "BUST_PAINTING": BUST_PAINTING,
    "STAGE_PAINTING": STAGE_PAINTING,
    "VOID_PAINTING": VOID_PAINTING,
    "SKULL_AND_ROSES_PAINTING": SKULL_AND_ROSES_PAINTING,
    "WITHER_PAINTING": WITHER_PAINTING,
    "BAROQUE_PAINTING": BAROQUE_PAINTING,
    "HUMBLE_PAINTING": HUMBLE_PAINTING,
    "BOUQUET_PAINTING": BOUQUET_PAINTING,
    "CAVEBIRD_PAINTING": CAVEBIRD_PAINTING,
    "COTAN_PAINTING": COTAN_PAINTING,
    "ENDBOSS_PAINTING": ENDBOSS_PAINTING,
    "FERN_PAINTING": FERN_PAINTING,
    "OWLEMONS_PAINTING": OWLEMONS_PAINTING,
    "SUNFLOWERS_PAINTING": SUNFLOWERS_PAINTING,
    "TIDES_PAINTING": TIDES_PAINTING,
    "BACKYARD_PAINTING": BACKYARD_PAINTING,
    "POND_PAINTING": POND_PAINTING,
    "FIGHTERS_PAINTING": FIGHTERS_PAINTING,
    "CHANGING_PAINTING": CHANGING_PAINTING,
    "FINDING_PAINTING": FINDING_PAINTING,
    "LOWMIST_PAINTING": LOWMIST_PAINTING,
    "PASSAGE_PAINTING": PASSAGE_PAINTING,
    "MORTAL_COIL_PAINTING": MORTAL_COIL_PAINTING,
    "DONKEY_KONG_PAINTING": DONKEY_KONG_PAINTING,
    "POINTER_PAINTING": POINTER_PAINTING,
    "PIGSCENE_PAINTING": PIGSCENE_PAINTING,
    "BURNING_SKULL_PAINTING": BURNING_SKULL_PAINTING,
    "ORB_PAINTING": ORB_PAINTING,
    "UNPACKED_PAINTING": UNPACKED_PAINTING,
}
