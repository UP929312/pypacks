# Additions:
from pypacks.additions.config import Config
from pypacks.additions.constants import MinecraftColor
from pypacks.additions.item_components import (
    AttributeModifier, ArmorTrim, Bee, BundleContents, BucketEntityData, Components, Cooldown, Consumable, ContainerContents, DeathProtection, EntityData,
    Equippable, FireworkExplosion, Firework, Food, Instrument, JukeboxPlayable, LodestoneTracker, MapData, MapDecoration, PotionEffect, PotionContents,
    ToolRule, Tool, TropicalFishData, UseRemainder, WrittenBookContent,
)
from pypacks.additions.raycasting import BlockRaycast, EntityRaycast
from pypacks.additions.reference_book_config import RefBookCategory, RefBookConfig, MISC_REF_BOOK_CATEGORY, PAINTING_REF_BOOK_CATEGORY, CUSTOM_BLOCKS_REF_BOOK_CATEGORY
# =============================================================================
# Providers:
from pypacks.providers.enchantment_provider import (
    SingleEnchantmentProvider, EnchantmentsByCostProvider, EnchantmentsByCostWithDifficultyProvider,
)
from pypacks.providers.int_provider import (
    IntProvider, ConstantIntProvider, UniformIntProvider, BiasedToBottomIntProvider, ClampedIntProvider, ClampedNormalIntProvider, WeightedListIntProvider,
)
from pypacks.providers.number_provider import (
    ConstantNumberProvider, UniformNumberProvider, BinomialNumberProvider, ScoreboardNumberProvider, StorageNumberProvider,
)
# =============================================================================
# Resources
from pypacks.resources.custom_loot_tables import *  # noqa: F401, F403
from pypacks.resources.world_gen import (
    CustomStructure, JigsawStructureType, SingleCustomStructure, CustomStructureSet, RandomSpreadPlacementType, ConcentricRingsPlacementType, CustomBiome, MoodSound
)
from pypacks.resources.world_gen.entity_spawner import SpawnOverride, DisableSpawnOverrideCategory
from pypacks.resources.custom_advancement import CustomAdvancement, Criteria
from pypacks.additions.custom_block import CustomBlock
from pypacks.resources.custom_damage_type import CustomDamageType, DamageTypeTranslation
from pypacks.resources.custom_dimension import CustomDimension, CustomDimensionType, OverworldDimension, NetherDimension, EndDimension
from pypacks.resources.custom_enchantment import (
    CustomEnchantment,
    EnchantValueEffect, SetValueEffect, AddValueEffect, MultiplyValueEffect, RemoveBinomialValueEffect, AllOfValueEffect,
    EnchantmentEntityEffect, AllOfEntityEffect, ApplyMobEffectEntityEffect,  DamageEntityEntityEffect, ChangeItemDamageEntityEffect, ExplodeEntityEffect, IgniteEntityEffect,
    PlaySoundEntityEffect, ReplaceBlockEntityEffect, ReplaceDiskEntityEffect, RunFunctionEntityEffect, SetBlockPropertiesEntityEffect, SpawnParticlesEntityEffect, SummonEntityEntityEffect

)
from pypacks.resources.custom_model import FacePaths, CustomItemModelDefinition
from pypacks.resources.custom_item import CustomItem
from pypacks.resources.custom_font import CustomFont
from pypacks.resources.custom_jukebox_song import CustomJukeboxSong
from pypacks.resources.custom_language import CustomLanguage
from pypacks.resources.custom_mcfunction import MCFunction

from pypacks.resources.custom_painting import CustomPainting
from pypacks.resources.custom_predicate import Predicate
from pypacks.resources.custom_recipe import (
    Recipe, CustomCrafterRecipe, ShapedCraftingRecipe, ShapelessCraftingRecipe, CraftingTransmuteRecipe, FurnaceRecipe, BlastFurnaceRecipe,
    CampfireRecipe, SmithingTransformRecipe, SmithingTrimRecipe, SmokerRecipe, StonecutterRecipe
)
from pypacks.resources.custom_sound import CustomSound
from pypacks.resources.custom_tag import CustomTag

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
try:
    from pypacks.scripts.repos.all_item_instances import DEFAULT_ITEMS
except ImportError:
    DEFAULT_ITEMS = {}

from pypacks.pack import Pack

__all__ = [
    # Additions
    "Config",
    "MinecraftColor",
    "AttributeModifier", "ArmorTrim", "Bee", "BundleContents", "BucketEntityData", "Components", "Cooldown", "Consumable", "ContainerContents", "DeathProtection", "EntityData",
    "Equippable", "FireworkExplosion", "Firework", "Food", "Instrument", "JukeboxPlayable", "LodestoneTracker", "MapData", "MapDecoration", "PotionEffect", "PotionContents",
    "BlockRaycast", "EntityRaycast",
    "ToolRule", "Tool", "TropicalFishData", "UseRemainder", "WrittenBookContent",
    "RefBookCategory", "RefBookConfig", "MISC_REF_BOOK_CATEGORY", "PAINTING_REF_BOOK_CATEGORY", "CUSTOM_BLOCKS_REF_BOOK_CATEGORY",
    # Providers
    "SingleEnchantmentProvider", "EnchantmentsByCostProvider", "EnchantmentsByCostWithDifficultyProvider",
    "IntProvider", "ConstantIntProvider", "UniformIntProvider", "BiasedToBottomIntProvider", "ClampedIntProvider", "ClampedNormalIntProvider", "WeightedListIntProvider",
    "ConstantNumberProvider", "UniformNumberProvider", "BinomialNumberProvider", "ScoreboardNumberProvider", "StorageNumberProvider",
    # Resources
    "CustomStructure", "JigsawStructureType", "SingleCustomStructure", "CustomStructureSet", "RandomSpreadPlacementType", "ConcentricRingsPlacementType", "SpawnOverride", "DisableSpawnOverrideCategory", "CustomBiome", "MoodSound",
    "CustomAdvancement", "Criteria",
    "CustomBlock",
    "CustomDamageType", "DamageTypeTranslation",
    "CustomDimension", "CustomDimensionType", "OverworldDimension", "NetherDimension", "EndDimension",
    "CustomEnchantment",
    "EnchantValueEffect", "SetValueEffect", "AddValueEffect", "MultiplyValueEffect", "RemoveBinomialValueEffect", "AllOfValueEffect",
    "EnchantmentEntityEffect", "AllOfEntityEffect", "ApplyMobEffectEntityEffect", "DamageEntityEntityEffect", "ChangeItemDamageEntityEffect", "ExplodeEntityEffect", "IgniteEntityEffect",
    "PlaySoundEntityEffect", "ReplaceBlockEntityEffect", "ReplaceDiskEntityEffect", "RunFunctionEntityEffect", "SetBlockPropertiesEntityEffect", "SpawnParticlesEntityEffect", "SummonEntityEntityEffect",
    "FacePaths", "CustomItemModelDefinition",
    "CustomItem",
    "CustomFont",
    "CustomLanguage",
    "CustomJukeboxSong",
    "MCFunction",
    "CustomLootTable",
    "CustomPainting",
    "Predicate",
    "Recipe", "CustomCrafterRecipe", "ShapedCraftingRecipe", "ShapelessCraftingRecipe", "CraftingTransmuteRecipe", "FurnaceRecipe", "BlastFurnaceRecipe", "SmokerRecipe",
    "CampfireRecipe", "SmithingTransformRecipe", "SmithingTrimRecipe", "StonecutterRecipe",
    "CustomSound",
    "CustomTag",

    "ModelItemModel", "ConstantTint", "DyeTint", "GrassTint", "FireworkTint", "PotionTint", "MapColorTint", "TeamTint", "CustomModelDataTint",
    "CompositeItemModel",
    "ConditionalItemModel", "UsingItemConditional", "BrokenConditional", "DamagedConditional", "HasComponentConditional", "FishingRodCastConditional", "BundleHasSelectedItemConditional", "SelectedConditional", "CarriedConditional", "ExtendedViewConditional", "KeyDownConditional", "ViewEntityConditional", "CustomModelDataConditional",
    "SelectItemModel", "SelectCase", "MainHandSelectProperty", "ChargeTypeSelectProperty", "TrimMaterialSelectProperty", "BlockStateSelectProperty", "DisplayContextSelectProperty", "LocalTimeSelectProperty", "ContextDimensionSelectProperty", "ContextEntityTypeSelectProperty", "CustomModelDataSelectProperty",
    "RangeDispatchItemModel",
    "EmptyItemModel",
    "BundleSelectedItemModel",
    "SpecialItemModel",
    "ItemModelType",

    # Script Repos
    "DEFAULT_ITEMS",

    # Pack.py
    "Pack",
]
