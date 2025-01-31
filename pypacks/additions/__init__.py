from typing import TypeAlias

from pypacks.additions.constants import MinecraftColor
from pypacks.additions.custom_block import CustomBlock
from pypacks.additions.raycasting import BlockRaycast, EntityRaycast
from pypacks.additions.custom_crafter import CustomCrafter
from pypacks.additions.custom_loop import CustomLoop
from pypacks.additions.item_components import (
    AttributeModifier, ArmorTrim, Bee, BundleContents, BucketEntityData, Components, Cooldown, Consumable, ContainerContents, DeathProtection, EntityData,
    Equippable, FireworkExplosion, Firework, Food, Instrument, JukeboxPlayable, LodestoneTracker, MapData, MapDecoration, PotionEffect, PotionContents,
    ToolRule, Tool, TropicalFishData, UseRemainder, WrittenBookContent,
)
from pypacks.additions.reference_book_config import RefBookCategory, RefBookConfig, MISC_REF_BOOK_CATEGORY, PAINTING_REF_BOOK_CATEGORY, CUSTOM_BLOCKS_REF_BOOK_CATEGORY
# =============================================================================
CustomAddition: TypeAlias = "CustomBlock | BlockRaycast | EntityRaycast | CustomCrafter | CustomLoop"
AllCustomAdditions = [
    CustomBlock, BlockRaycast, EntityRaycast, CustomCrafter, CustomLoop
]

__all__ = [
    "MinecraftColor",
    "CustomBlock",
    "BlockRaycast",
    "EntityRaycast",
    "CustomCrafter",
    "CustomLoop",
    "AttributeModifier", "ArmorTrim", "Bee", "BundleContents", "BucketEntityData", "Components", "Cooldown", "Consumable", "ContainerContents", "DeathProtection", "EntityData",
    "Equippable", "FireworkExplosion", "Firework", "Food", "Instrument", "JukeboxPlayable", "LodestoneTracker", "MapData", "MapDecoration", "PotionEffect", "PotionContents",
    "ToolRule", "Tool", "TropicalFishData", "UseRemainder", "WrittenBookContent",
    "RefBookCategory", "RefBookConfig", "MISC_REF_BOOK_CATEGORY", "PAINTING_REF_BOOK_CATEGORY", "CUSTOM_BLOCKS_REF_BOOK_CATEGORY",
]