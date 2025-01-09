# =============================================================================
# Resources
from pypacks.resources.constants import MinecraftColor
from pypacks.resources.custom_advancement import CustomAdvancement, Criteria
from pypacks.resources.custom_block import CustomBlock
from pypacks.resources.custom_enchantment import CustomEnchantment, EnchantEffect
from pypacks.resources.custom_model import FacePaths, CustomItemModelDefinition
from pypacks.resources.custom_item import CustomItem
from pypacks.resources.custom_jukebox_song import CustomJukeboxSong
from pypacks.resources.custom_mcfunction import MCFunction
from pypacks.resources.custom_loot_tables import CustomLootTable
from pypacks.resources.custom_loot_tables import *  # noqa: F401, F403

from pypacks.resources.custom_painting import CustomPainting
from pypacks.resources.custom_predicate import Predicate
from pypacks.resources.custom_recipe import (
    Recipe, ShapelessCraftingRecipe, ShapedCraftingRecipe, CraftingTransmuteRecipe, FurnaceRecipe, BlastFurnaceRecipe,
    CampfireRecipe, SmithingTransformRecipe, SmithingTrimRecipe, SmokerRecipe, StonecutterRecipe
)
from pypacks.resources.custom_sound import CustomSound
from pypacks.resources.custom_tag import CustomTag

from pypacks.resources.item_components import (
    AttributeModifier, ArmorTrim, Bee, BundleContents, BucketEntityData, Components, Cooldown, Consumable, ContainerContents, DeathProtection, EntityData,
    Equippable, FireworkExplosion, Firework, Food, Instrument, JukeboxPlayable, LodestoneTracker, MapData, MapDecoration, PotionEffect, PotionContents,
    ToolRule, Tool, TropicalFishData, UseRemainder, WrittenBookContent,
)
from pypacks.resources.item_model_definition import (
    ModelItemModel, ConstantTint, DyeTint, GrassTint, FireworkTint, PotionTint, MapColorTint, TeamTint, CustomModelDataTint,
    CompositeItemModel,
    ConditionalItemModel, UsingItemConditional, BrokenConditional, DamagedConditional, HasComponentConditional, FishingRodCastConditional, BundleHasSelectedItemConditional, SelectedConditional, CarriedConditional, ExtendedViewConditional, KeyDownConditional, ViewEntityConditional, CustomModelDataConditional,
    SelectItemModel, SelectCase, MainHandSelectProperty, ChargeTypeSelectProperty, TrimMaterialSelectProperty, BlockStateSelectProperty, DisplayContextSelectProperty, LocalTimeSelectProperty, ContextDimensionSelectProperty, ContextEntityTypeSelectProperty, CustomModelDataSelectProperty,
    RangeDispatchItemModel,
    EmptyItemModel,
    BundleSelectedItemModel,
    SpecialItemModel,
    ItemModelType,
)
# =============================================================================
from pypacks.scripts.repos.all_item_instances import DEFAULT_ITEMS

from pypacks.pack import Pack

from pypacks.reference_book_config import RefBookCategory, RefBookConfig, MISC_REF_BOOK_CATEGORY, PAINTING_REF_BOOK_CATEGORY, CUSTOM_BLOCKS_REF_BOOK_CATEGORY

__all__ = [
    "MinecraftColor",
    "CustomAdvancement", "Criteria",
    "CustomBlock",
    "CustomEnchantment", "EnchantEffect",
    "FacePaths", "CustomItemModelDefinition",
    "CustomItem",
    "CustomJukeboxSong",
    "MCFunction",
    "CustomLootTable",
    "CustomPainting",
    "Predicate",
    "Recipe", "ShapelessCraftingRecipe", "ShapedCraftingRecipe", "CraftingTransmuteRecipe", "FurnaceRecipe", "BlastFurnaceRecipe", "SmokerRecipe",
    "CampfireRecipe", "SmithingTransformRecipe", "SmithingTrimRecipe", "StonecutterRecipe",
    "CustomSound",
    "CustomTag",

    "AttributeModifier", "ArmorTrim", "Bee", "BundleContents", "BucketEntityData", "Components", "Cooldown", "Consumable", "ContainerContents", "DeathProtection", "EntityData",
    "Equippable", "FireworkExplosion", "Firework", "Food", "Instrument", "JukeboxPlayable", "LodestoneTracker", "MapData", "MapDecoration", "PotionEffect", "PotionContents",
    "ToolRule", "Tool", "TropicalFishData", "UseRemainder", "WrittenBookContent",

    "ModelItemModel", "ConstantTint", "DyeTint", "GrassTint", "FireworkTint", "PotionTint", "MapColorTint", "TeamTint", "CustomModelDataTint",
    "CompositeItemModel",
    "ConditionalItemModel", "UsingItemConditional", "BrokenConditional", "DamagedConditional", "HasComponentConditional", "FishingRodCastConditional", "BundleHasSelectedItemConditional", "SelectedConditional", "CarriedConditional", "ExtendedViewConditional", "KeyDownConditional", "ViewEntityConditional", "CustomModelDataConditional",
    "SelectItemModel", "SelectCase", "MainHandSelectProperty", "ChargeTypeSelectProperty", "TrimMaterialSelectProperty", "BlockStateSelectProperty", "DisplayContextSelectProperty", "LocalTimeSelectProperty", "ContextDimensionSelectProperty", "ContextEntityTypeSelectProperty", "CustomModelDataSelectProperty",
    "RangeDispatchItemModel",
    "EmptyItemModel",
    "BundleSelectedItemModel",
    "SpecialItemModel",
    "ItemModelType",

    "DEFAULT_ITEMS",

    "Pack",

    "RefBookCategory", "RefBookConfig", "MISC_REF_BOOK_CATEGORY", "PAINTING_REF_BOOK_CATEGORY", "CUSTOM_BLOCKS_REF_BOOK_CATEGORY",
]
