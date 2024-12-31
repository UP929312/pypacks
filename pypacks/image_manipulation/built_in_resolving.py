from pathlib import Path

from pypacks.utils import PYPACKS_ROOT

BANNERS = ["white_banner", "orange_banner", "magenta_banner", "light_blue_banner", "yellow_banner", "lime_banner", "pink_banner", "gray_banner", "light_gray_banner", "cyan_banner", "purple_banner", "blue_banner", "brown_banner", "green_banner", "red_banner", "black_banner"]
HEADS = ["player_head", "zombie_head", "creeper_head", "skeleton_skull", "wither_skeleton_skull", "dragon_head"]
SPAWN_EGGS = [
    "axoltl_spawn_egg", "bat_spawn_egg", "bee_spawn_egg", "blaze_spawn_egg", "cat_spawn_egg", "cave_spider_spawn_egg", "chicken_spawn_egg", "cod_spawn_egg",
    "cow_spawn_egg", "creeper_spawn_egg", "dolphin_spawn_egg", "donkey_spawn_egg", "drowned_spawn_egg", "elder_guardian_spawn_egg", "enderman_spawn_egg",
    "endermite_spawn_egg", "evoker_spawn_egg", "fox_spawn_egg", "ghast_spawn_egg", "glow_squid_spawn_egg", "goat_spawn_egg", "guardian_spawn_egg",
    "hoglin_spawn_egg", "horse_spawn_egg", "husk_spawn_egg", "llama_spawn_egg", "magma_cube_spawn_egg", "mooshroom_spawn_egg", "mule_spawn_egg",
    "ocelot_spawn_egg", "panda_spawn_egg", "parrot_spawn_egg", "phantom_spawn_egg", "pig_spawn_egg", "piglin_spawn_egg", "piglin_brute_spawn_egg",
    "pillager_spawn_egg", "polar_bear_spawn_egg", "pufferfish_spawn_egg", "rabbit_spawn_egg", "ravager_spawn_egg", "salmon_spawn_egg", "sheep_spawn_egg"
    "shulker_spawn_egg", "silverfish_spawn_egg", "skeleton_spawn_egg", "skeleton_horse_spawn_egg", "slime_spawn_egg", "spider_spawn_egg", "squid_spawn_egg",
    "stray_spawn_egg", "strider_spawn_egg", "trader_llama_spawn_egg", "tropical_fish_spawn_egg", "turtle_spawn_egg", "vex_spawn_egg", "villager_spawn_egg",
    "vindicator_spawn_egg", "wandering_trader_spawn_egg", "witch_spawn_egg", "wither_skeleton_spawn_egg", "wolf_spawn_egg", "zoglin_spawn_egg", "zombie_spawn_egg",
    "zombie_horse_spawn_egg", "zombie_villager_spawn_egg", "zombified_piglin_spawn_egg",
]
# Base ======
image_mapping = {}
# Banners ======
image_mapping |= {banner: Path(PYPACKS_ROOT)/"assets"/"images"/"minecraft_renders_override"/"banner.png" for banner in BANNERS}
# Heads ======
image_mapping |= {head: Path(PYPACKS_ROOT)/"assets"/"images"/"minecraft_renders_override"/"player_head.png" for head in HEADS}
# Spawn Eggs ======
image_mapping |= {spawn_egg: Path(PYPACKS_ROOT)/"assets"/"images"/"minecraft_renders_override"/"spawn_egg.png" for spawn_egg in SPAWN_EGGS}
# Random others ======
image_mapping |= {
    "shield": Path(PYPACKS_ROOT)/"assets"/"images"/"minecraft_renders_override"/"shield.png",
    "decorated_pot": Path(PYPACKS_ROOT)/"assets"/"images"/"minecraft_renders_override"/"decorated_pot.png",
    "chest": Path(PYPACKS_ROOT)/"assets"/"images"/"minecraft_renders_override"/"chest.png",
}

def resolve_default_item_image(base_item: str) -> Path:
    if base_item.removeprefix('minecraft:') in image_mapping:
        return image_mapping[base_item.removeprefix('minecraft:')]
    path = Path(PYPACKS_ROOT)/"assets"/"images"/"minecraft_renders_cache"/"items"/f"{base_item.removeprefix('minecraft:')}.png"
    if path.exists():
        return path
    return Path(PYPACKS_ROOT)/"assets"/"images"/"reference_book_icons"/"unknown.png"
