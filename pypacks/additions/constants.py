from enum import Enum
from typing import Literal


class MinecraftColor(Enum):
    BLACK = 0x000000
    DARK_BLUE = 0x0000AA
    DARK_GREEN = 0x00AA00
    DARK_AQUA = 0x00AAAA
    DARK_RED = 0xAA0000
    DARK_PURPLE = 0xAA00AA
    GOLD = 0xFFAA00
    GRAY = 0xAAAAAA
    DARK_GRAY = 0x555555
    BLUE = 0x5555FF
    GREEN = 0x55FF55
    AQUA = 0x55FFFF
    RED = 0xFF5555
    LIGHT_PURPLE = 0xFF55FF
    YELLOW = 0xFFFF55
    WHITE = 0xFFFFFF


COLOUR_CODE_MAPPINGS = {
    "&0": "black",
    "&1": "dark_blue",
    "&2": "dark_green",
    "&3": "dark_aqua",
    "&4": "dark_red",
    "&5": "dark_purple",
    "&6": "gold",
    "&7": "gray",
    "&8": "dark_gray",
    "&9": "blue",
    "&a": "green",
    "&b": "aqua",
    "&c": "red",
    "&d": "light_purple",
    "&e": "yellow",
    "&f": "white",
    # "&l": "bold",
    # "&m": "strikethrough",
    # "&n": "underline",
    # "&o": "italic",
    # "&r": "reset",
    # obfuscated?
}


Slabs = Literal["oak_slab", "spruce_slab", "birch_slab", "jungle_slab", "acacia_slab", "dark_oak_slab", "mangrove_slab", "cherry_slab", "pale_oak_slab",
                "bamboo_slab", "bamboo_mosaic_slab", "crimson_slab", "warped_slab", "stone_slab", "cobblestone_slab", "mossy_cobblestone_slab", "smooth_stone_slab",
                "stone_brick_slab", "mossy_stone_brick_slab", "granite_slab", "polished_granite_slab", "diorite_slab", "polished_diorite_slab", "andesite_slab",
                "polished_andesite_slab", "cobbled_deepslate_slab", "deepslate_brick_slab", "deepslate_tile_slab", "tuff_slab", "polished_tuff_slab",
                "tuff_brick_slab", "brick_slab", "mud_brick_slab", "resin_brick_slab", "sandstone_slab", "smooth_sandstone_slab", "cut_sandstone_slab",
                "red_sandstone_slab", "smooth_red_sandstone_slab", "cut_red_sandstone_slab", "prismarine_slab", "prismarine_brick_slab", "dark_prismarine_slab",
                "nether_brick_slab", "red_nether_brick_slab", "blackstone_slab", "polished_blackstone_slab", "polished_blackstone_brick_slab", "end_stone_brick_slab",
                "purpur_slab", "quartz_slab", "smooth_quartz_slab", "cut_copper_slab", "exposed_cut_copper_slab", "weathered_cut_copper_slab", "oxidised_cut_copper_slab",
                "waxed_cut_copper_slab", "waxed_exposed_cut_copper_slab", "waxed_weathered_cut_copper_slab", "waxed_oxidised_cut_copper_slab"]


SPAWN_EGGS = [
    "minecraft:axoltl_spawn_egg",
    "minecraft:bat_spawn_egg",
    "minecraft:bee_spawn_egg",
    "minecraft:blaze_spawn_egg",
    "minecraft:cat_spawn_egg",
    "minecraft:cave_spider_spawn_egg",
    "minecraft:chicken_spawn_egg",
    "minecraft:cod_spawn_egg",
    "minecraft:cow_spawn_egg",
    "minecraft:creeper_spawn_egg",
    "minecraft:dolphin_spawn_egg",
    "minecraft:donkey_spawn_egg",
    "minecraft:drowned_spawn_egg",
    "minecraft:elder_guardian_spawn_egg",
    "minecraft:enderman_spawn_egg",
    "minecraft:endermite_spawn_egg",
    "minecraft:evoker_spawn_egg",
    "minecraft:fox_spawn_egg",
    "minecraft:ghast_spawn_egg",
    "minecraft:glow_squid_spawn_egg",
    "minecraft:goat_spawn_egg",
    "minecraft:guardian_spawn_egg",
    "minecraft:hoglin_spawn_egg",
    "minecraft:horse_spawn_egg",
    "minecraft:husk_spawn_egg",
    "minecraft:llama_spawn_egg",
    "minecraft:magma_cube_spawn_egg",
    "minecraft:mooshroom_spawn_egg",
    "minecraft:mule_spawn_egg",
    "minecraft:ocelot_spawn_egg",
    "minecraft:panda_spawn_egg",
    "minecraft:parrot_spawn_egg",
    "minecraft:phantom_spawn_egg",
    "minecraft:pig_spawn_egg",
    "minecraft:piglin_spawn_egg",
    "minecraft:piglin_brute_spawn_egg",
    "minecraft:pillager_spawn_egg",
    "minecraft:polar_bear_spawn_egg",
    "minecraft:pufferfish_spawn_egg",
    "minecraft:rabbit_spawn_egg",
    "minecraft:ravager_spawn_egg",
    "minecraft:salmon_spawn_egg",
    "minecraft:sheep_spawn_egg",
    "minecraft:shulker_spawn_egg",
    "minecraft:silverfish_spawn_egg",
    "minecraft:skeleton_spawn_egg",
    "minecraft:skeleton_horse_spawn_egg",
    "minecraft:slime_spawn_egg",
    "minecraft:spider_spawn_egg",
    "minecraft:squid_spawn_egg",
    "minecraft:stray_spawn_egg",
    "minecraft:strider_spawn_egg",
    "minecraft:trader_llama_spawn_egg",
    "minecraft:tropical_fish_spawn_egg",
    "minecraft:turtle_spawn_egg",
    "minecraft:vex_spawn_egg",
    "minecraft:villager_spawn_egg",
    "minecraft:vindicator_spawn_egg",
    "minecraft:wandering_trader_spawn_egg",
    "minecraft:witch_spawn_egg",
    "minecraft:wither_skeleton_spawn_egg",
    "minecraft:wolf_spawn_egg",
    "minecraft:zoglin_spawn_egg",
    "minecraft:zombie_spawn_egg",
    "minecraft:zombie_horse_spawn_egg",
    "minecraft:zombie_villager_spawn_egg",
    "minecraft:zombified_piglin_spawn_egg",
]


INEDIBLE_ITEMS = [
    *SPAWN_EGGS,

    "minecraft:oak_boat",
    "minecraft:spruce_boat",
    "minecraft:birch_boat",
    "minecraft:jungle_boat",
    "minecraft:acacia_boat",
    "minecraft:dark_oak_boat",
    "minecraft:mangrove_boat",
    "minecraft:cherry_boat",
    "minecraft:pale_oak_boat",

    "minecraft:oak_chest_boat",
    "minecraft:spruce_chest_boat",
    "minecraft:birch_chest_boat",
    "minecraft:jungle_chest_boat",
    "minecraft:acacia_chest_boat",
    "minecraft:dark_oak_chest_boat",
    "minecraft:mangrove_chest_boat",
    "minecraft:cherry_chest_boat",
    "minecraft:pale_oak_chest_boat",

    "minecraft:egg",
    "minecraft:ender_pearl",
    "minecraft:snowball",
    "minecraft:trident",

    "minecraft:boat",
    "minecraft:crossbow",
    "minecraft:bow",
    "minecraft:goat_horn",
    "minecraft:experience_bottle",
    "minecraft:firework_rocket",
]


THROWABLE_ITEMS = [
    "minecraft:snowball",
    "minecraft:egg",
    "minecraft:ender_pearl",
    "minecraft:splash_potion",
    "minecraft:lingering_potion",
    "minecraft:ender_eye",
    "minecraft:wind_charge",
    "minecraft:trident",
    "minecraft:experience_bottle",
]

# A lot more

MobCapCategories = Literal[
    "monster", "creature", "ambient", "axolotls", "underground_water_creature", "water_ambient", "water_creature", "misc", None
]
# Monster = Hostile mobs
# Creature = Passive mobs
# Ambient = Bats
# Axolotls = Axolotls
# Underground water creature = Glow squids
# Water ambient = Dolphins and squids
# Water creature = Fish (cod, salmon, pufferfish and tropical fish)
# Misc = Item frames, etc (non mobs/animals)

MOB_TO_CATEGORY: dict[str, MobCapCategories] = {
    "allay": "creature",
    "armadillo": "creature",
    "axolotl": "axolotls",
    "bat": "ambient",  # Only ambient
    "bee": "creature",
    "blaze": "monster",
    "bogged": "monster",
    "breeze": "monster",
    "camel": "creature",
    "cat": "creature",
    "cave_spider": "monster",
    "chicken": "creature",
    "cod": "water_creature",
    "cow": "creature",
    "creaking": "monster",
    "creeper": "monster",
    "dolphin": "water_ambient",  # Water ambient = Squids and dolphins only
    "donkey": "creature",
    "drowned": "monster",
    "elder_guardian": None,
    "enderman": "monster",
    "endermite": "monster",
    "evoker": "monster",
    "fox": "creature",
    "frog": "creature",
    "ghast": "monster",
    "glow_squid": "underground_water_creature",  # Only underground water creature
    "goat": "creature",
    "guardian": "monster",
    "hoglin": "monster",
    "horse": "creature",
    "husk": "monster",
    "iron_golem": None,
    "llama": "creature",
    "magma_cube": "monster",
    "mooshroom": "creature",
    "mule": "creature",
    "ocelot": "creature",
    "panda": "creature",
    "parrot": "creature",
    "phantom": "monster",
    "pig": "creature",
    "piglin": "monster",
    "piglin_brute": "monster",
    "pillager": "monster",
    "polar_bear": "creature",
    "pufferfish": "water_creature",
    "rabbit": "creature",
    "ravager": "monster",
    "salmon": "water_creature",
    "sheep": "creature",
    "shulker": "monster",
    "silverfish": "monster",
    "skeleton": "monster",
    "skeleton_horse": "creature",
    "slime": "monster",
    "sniffer": "creature",
    "snow_golem": None,
    "spider": "monster",
    "squid": "water_ambient",  # Water ambient = Squids and dolphins only
    "stray": "monster",
    "strider": "creature",
    "tadpole": None,
    "trader_llama": "creature",
    "tropical_fish": "water_creature",
    "turtle": "creature",
    "vex": "monster",
    "villager": None,
    "vindicator": "monster",
    "wandering_trader": "creature",
    "warden": None,
    "witch": "monster",
    "wither_skeleton": "monster",
    "wolf": "creature",
    "zoglin": "monster",
    "zombie": "monster",
    "zombie_horse": "creature",
    "zombie_villager": "monster",
    "zombified_piglin": "monster",
}
