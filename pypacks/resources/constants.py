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


Slabs = Literal["oak_slab", "spruce_slab", "birch_slab", "jungle_slab", "acacia_slab", "dark_oak_slab", "mangrove_slab", "cherry_slab", "pale_oak_slab",
                "bamboo_slab", "bamboo_mosaic_slab", "crimson_slab", "warped_slab", "stone_slab", "cobblestone_slab", "mossy_cobblestone_slab", "smooth_stone_slab",
                "stone_brick_slab", "mossy_stone_brick_slab", "granite_slab", "polished_granite_slab", "diorite_slab", "polished_diorite_slab", "andesite_slab",
                "polished_andesite_slab", "cobbled_deepslate_slab", "deepslate_brick_slab", "deepslate_tile_slab", "tuff_slab", "polished_tuff_slab",
                "tuff_brick_slab", "brick_slab", "mud_brick_slab", "resin_brick_slab", "sandstone_slab", "smooth_sandstone_slab", "cut_sandstone_slab",
                "red_sandstone_slab", "smooth_red_sandstone_slab", "cut_red_sandstone_slab", "prismarine_slab", "prismarine_brick_slab", "dark_prismarine_slab",
                "nether_brick_slab", "red_nether_brick_slab", "blackstone_slab", "polished_blackstone_slab", "polished_blackstone_brick_slab", "end_stone_brick_slab",
                "purpur_slab", "quartz_slab", "smooth_quartz_slab", "cut_copper_slab", "exposed_cut_copper_slab", "weathered_cut_copper_slab", "oxidised_cut_copper_slab",
                "waxed_cut_copper_slab", "waxed_exposed_cut_copper_slab", "waxed_weathered_cut_copper_slab", "waxed_oxidised_cut_copper_slab"]

# AXIAL = {"facing": ["up", "down", "north", "east", "south", "west"]}
# CARDINAL = {"facing": ["north", "east", "south", "west"]}
# ON_AXIS = {"axis": ["x", "y", "z"]}
# ROTATION_16 = {"rotation": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]}

# BLOCKS_WITH_BLOCK_STATES = {
#     # "anvil": CARDINAL,
#     # "amethyst_bud": AXIAL,
#     "amethyst_cluster": AXIAL,
#     # Banners have 16 directions, 0-15
#     "barrel": AXIAL,
#     "basalt": ON_AXIS,  # east–west, vertically and north-south
#     "polished_basalt": ON_AXIS,  # east–west, vertically and north-south
#     "bee_nest": CARDINAL,
#     "beehive": CARDINAL,
#     # "bell": CARDINAL,
#     "blast_furnace": CARDINAL,
#     "bamboo_block": ON_AXIS,  # east–west, vertically and north-south
#     "bone_block": ON_AXIS,  # east–west, vertically and north-south
#     # "campfire": CARDINAL,
#     # "chain": ON_AXIS,  # east–west, vertically and north-south
#     "chest": CARDINAL,
#     "ender_chest": CARDINAL,
#     "chiseled_bookshelf": CARDINAL,
#     "command_block": AXIAL,
#     "creaking_heart": ON_AXIS,  # east–west, vertically and north-south
#     # "decorated_pot": CARDINAL,
#     "deepslate": ON_AXIS,  # east–west, vertically and north-south
#     "dispenser": AXIAL,
#     "dropper": AXIAL,
#     # "end_portal_frame": CARDINAL,
#     # "end_rod": AXIAL,
#     # "fence_gate": CARDINAL,
#     "pearlescent_froglight": CARDINAL,
#     "verdant_froglight": CARDINAL,
#     "ochre_froglight": CARDINAL,
#     "furnace": CARDINAL,
#     "white_glazed_terracotta": CARDINAL,
#     "orange_glazed_terracotta": CARDINAL,
#     "magenta_glazed_terracotta": CARDINAL,
#     "light_blue_glazed_terracotta": CARDINAL,
#     "yellow_glazed_terracotta": CARDINAL,
#     "lime_glazed_terracotta": CARDINAL,
#     "pink_glazed_terracotta": CARDINAL,
#     "gray_glazed_terracotta": CARDINAL,
#     "light_gray_glazed_terracotta": CARDINAL,
#     "cyan_glazed_terracotta": CARDINAL,
#     "purple_glazed_terracotta": CARDINAL,
#     "blue_glazed_terracotta": CARDINAL,
#     "brown_glazed_terracotta": CARDINAL,
#     "green_glazed_terracotta": CARDINAL,
#     "red_glazed_terracotta": CARDINAL,
#     "black_glazed_terracotta": CARDINAL,
#     # "grindstone": CARDINAL,
#     # "oak_hanging_sign": ROTATION_16,
#     # "spruce_hanging_sign": ROTATION_16,
#     # "birch_hanging_sign": ROTATION_16,
#     # "jungle_hanging_sign": ROTATION_16,
#     # "acacia_hanging_sign": ROTATION_16,
#     # "dark_oak_hanging_sign": ROTATION_16,
#     # "mangrove_hanging_sign": ROTATION_16,
#     # "cherry_hanging_sign": ROTATION_16,
#     # "pale_oak_hanging_sign": ROTATION_16,
#     # "bamboo_hanging_sign": ROTATION_16,
#     # "crimson_hanging_sign": ROTATION_16,
#     # "warped_hanging_sign": ROTATION_16,
#     "hay_block": ON_AXIS,  # east–west, vertically and north-south
#     # "hopper": CARDINAL,
#     "jack_o_lantern": CARDINAL,
#     # "lectern": CARDINAL,
#     # "lightning_rod": AXIAL,
#     "acacia_log": ON_AXIS,  # east–west, vertically and north-south
#     "birch_log": ON_AXIS,  # east–west, vertically and north-south
#     "dark_oak_log": ON_AXIS,  # east–west, vertically and north-south
#     "jungle_log": ON_AXIS,  # east–west, vertically and north-south
#     "oak_log": ON_AXIS,  # east–west, vertically and north-south
#     "spruce_log": ON_AXIS,  # east–west, vertically and north-south
#     "mangrove_log": ON_AXIS,  # east–west, vertically and north-south
#     "cherry_log": ON_AXIS,  # east–west, vertically and north-south
#     "pale_oak_log": ON_AXIS,  # east–west, vertically and north-south
#     "crimson_stem": ON_AXIS,  # east–west, vertically and north-south
#     "warped_stem": ON_AXIS,  # east–west, vertically and north-south
#     "loom": CARDINAL,
#     "observer": AXIAL,
#     "piston": AXIAL,
#     "sticky_piston": AXIAL,
#     "pumpkin": CARDINAL,
#     "carved_pumpkin": CARDINAL,
#     "purpur_pillar": ON_AXIS,  # east–west, vertically and north-south
#     "quartz_pillar": ON_AXIS,  # east–west, vertically and north-south
#     "comparator": CARDINAL,
#     # "repeater": CARDINAL,
#     "shulker_box": AXIAL,
#     "white_shulker_box": AXIAL,
#     "orange_shulker_box": AXIAL,
#     "magenta_shulker_box": AXIAL,
#     "light_blue_shulker_box": AXIAL,
#     "yellow_shulker_box": AXIAL,
#     "lime_shulker_box": AXIAL,
#     "pink_shulker_box": AXIAL,
#     "gray_shulker_box": AXIAL,
#     "light_gray_shulker_box": AXIAL,
#     "cyan_shulker_box": AXIAL,
#     "purple_shulker_box": AXIAL,
#     "blue_shulker_box": AXIAL,
#     "brown_shulker_box": AXIAL,
#     "green_shulker_box": AXIAL,
#     "red_shulker_box": AXIAL,
#     "black_shulker_box": AXIAL,
#     "oak_sign": ROTATION_16,
#     "spruce_sign": ROTATION_16,
#     "birch_sign": ROTATION_16,
#     "jungle_sign": ROTATION_16,
#     "acacia_sign": ROTATION_16,
#     "dark_oak_sign": ROTATION_16,
#     "mangrove_sign": ROTATION_16,
#     "cherry_sign": ROTATION_16,
#     "pale_oak_sign": ROTATION_16,
#     "bamboo_sign": ROTATION_16,
#     "crimson_sign": ROTATION_16,
#     "warped_sign": ROTATION_16,
#     # "small_dripleaf": CARDINAL,
#     "smoker": CARDINAL,
#     "oak_stairs": CARDINAL,
#     "spruce_stairs": CARDINAL,
#     "birch_stairs": CARDINAL,
#     "jungle_stairs": CARDINAL,
#     "acacia_stairs": CARDINAL,
#     "dark_oak_stairs": CARDINAL,
#     "mangrove_stairs": CARDINAL,
#     "cherry_stairs": CARDINAL,
#     "pale_oak_stairs": CARDINAL,
#     "crimson_stairs": CARDINAL,
#     "warped_stairs": CARDINAL,
#     # "stonecutter": CARDINAL,
#     "vault": CARDINAL,
# }
# AXIAL_BLOCKS = [key for key, value in BLOCKS_WITH_BLOCK_STATES.items() if value == AXIAL]
# CARDINAL_BLOCKS = [key for key, value in BLOCKS_WITH_BLOCK_STATES.items() if value == CARDINAL]
# ON_AXIS_BLOCKS = [key for key, value in BLOCKS_WITH_BLOCK_STATES.items() if value == ON_AXIS]
# ROTATION_16_BLOCKS = [key for key, value in BLOCKS_WITH_BLOCK_STATES.items() if value == ROTATION_16]

# DIRECTION_TO_BLOCKS = {
#     "axial": AXIAL_BLOCKS,
#     "cardinal": CARDINAL_BLOCKS,
#     "on_axis": ON_AXIS_BLOCKS,
# }

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

# A lot more
