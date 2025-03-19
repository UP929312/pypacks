# Additions:
from pypacks.additions.config import Config
from pypacks.additions.constants import MinecraftColor
from pypacks.additions.item_components import (
    AttributeModifier, ArmorTrim, Bee, BundleContents, BucketEntityData, Components, Cooldown, Consumable, ContainerContents, DeathProtection, EntityData,
    Equippable, FireworkExplosion, Firework, Food, Instrument, JukeboxPlayable, LodestoneTracker, MapData, MapDecoration, PotionEffect, PotionContents,
    ToolRule, Tool, TropicalFishData, UseRemainder, WrittenBookContent,
)
# =============================================================================
# Providers:
from pypacks.providers.enchantment_provider import (  # noqa: F401, F403
    SingleEnchantmentProvider, EnchantmentsByCostProvider, EnchantmentsByCostWithDifficultyProvider, EnchantmentProvider,
)
from pypacks.providers.float_provider import (  # noqa: F401, F403
    ConstantFloatProvider, UniformFloatProvider, ClampedNormalFloatProvider, TrapezoidFloatProvider, FloatProvider,

)
from pypacks.providers.height_provider import (  # noqa: F401, F403
    ConstantHeightProvider, UniformHeightProvider, BiasedToBottomHeightProvider, VeryBiasedToBottomHeightProvider, HeightProvider,
)
from pypacks.providers.int_provider import (  # noqa: F401, F403
    ConstantIntProvider, UniformIntProvider, BiasedToBottomIntProvider, ClampedIntProvider, ClampedNormalIntProvider, WeightedListIntProvider, IntProvider
)
from pypacks.providers.number_provider import (  # noqa: F401, F403
    ConstantNumberProvider, UniformNumberProvider, BinomialNumberProvider, ScoreboardNumberProvider, StorageNumberProvider, NumberProvider,
)

# =============================================================================
# Resources
from pypacks.resources.custom_loot_tables import *  # noqa: F401, F403
from pypacks.resources.world_gen import (  # type: ignore[attr-defined]
    CustomStructure, JigsawStructureType, SingleCustomStructure, CustomStructureSet, RandomSpreadPlacementType, ConcentricRingsPlacementType, CustomBiome, MoodSound,
    WorldGenResources,
)
from pypacks.resources.world_gen.entity_spawner import SpawnOverride, DisableSpawnOverrideCategory
from pypacks.resources.custom_advancement import CustomAdvancement, Criteria
from pypacks.additions.custom_block import CustomBlock
from pypacks.resources.custom_damage_type import CustomDamageType, DamageTypeTranslation
from pypacks.resources.custom_dimension import CustomDimension, CustomDimensionType, OverworldDimension, NetherDimension, EndDimension
from pypacks.resources.custom_enchantment import CustomEnchantment
from pypacks.resources.custom_model import FacePaths, CustomItemRenderDefinition, CustomModelDefinition, CustomTexture
from pypacks.resources.custom_item import CustomItem
from pypacks.resources.custom_font import CustomAutoAssignedFont, BitMapFontChar, SpaceFontChar, TTFFontProvider, ReferenceFontProvider
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
    ConditionalItemModel, UsingItemConditional, BrokenConditional, DamagedConditional, ComponentConditional, HasComponentConditional, FishingRodCastConditional, BundleHasSelectedItemConditional, SelectedConditional, CarriedConditional, ExtendedViewConditional, KeyDownConditional, ViewEntityConditional, CustomModelDataConditional,
    SelectItemModel, SelectCase, MainHandSelectProperty, ChargeTypeSelectProperty, TrimMaterialSelectProperty, BlockStateSelectProperty, DisplayContextSelectProperty, LocalTimeSelectProperty, ContextDimensionSelectProperty, ContextEntityTypeSelectProperty, CustomModelDataSelectProperty, ComponentSelectProperty,
    RangeDispatchItemModel, BundleFullnessRangeDispatchProperty, CompassRangeDispatchProperty, CooldownRangeDispatchProperty, CrossbowPullRangeDispatchProperty, CountRangeDispatchProperty, CustomModelDataRangeDispatchProperty, DamageRangeDispatchProperty, RangeDispatchPropertyType, TimeRangeDispatchProperty, UseCycleRangeDispatchProperty,
    EmptyItemModel,
    BundleSelectedItemModel,
    SpecialItemModel, BannerSpecialItemModelType, BedSpecialItemModelType, ChestSpecialItemModelType, ConduitSpecialItemModelType, DecoratedPotSpecialItemModelType, HangingSignSpecialItemModelType, HeadSpecialItemModelType, ShieldSpecialItemModelType, ShulkerBoxSpecialItemModelType, StandingSignSpecialItemModelType, TridentSpecialItemModelType,
    ItemModel,
)
# =============================================================================
try:
    from pypacks.minecraft.items import DEFAULT_ITEMS
except ImportError:  # This exists incase I break the file, so I can still override it (as it tries to load itin first)
    DEFAULT_ITEMS = {}

from pypacks.pack import Pack

__all__ = [
    # Additions
    "Config",
    "MinecraftColor",
    "AttributeModifier", "ArmorTrim", "Bee", "BundleContents", "BucketEntityData", "Components", "Cooldown", "Consumable", "ContainerContents", "DeathProtection", "EntityData",
    "Equippable", "FireworkExplosion", "Firework", "Food", "Instrument", "JukeboxPlayable", "LodestoneTracker", "MapData", "MapDecoration", "PotionEffect", "PotionContents",
    "ToolRule", "Tool", "TropicalFishData", "UseRemainder", "WrittenBookContent",
    # Providers
    "SingleEnchantmentProvider", "EnchantmentsByCostProvider", "EnchantmentsByCostWithDifficultyProvider", "EnchantmentProvider",
    "ConstantFloatProvider", "UniformFloatProvider", "ClampedNormalFloatProvider", "TrapezoidFloatProvider", "FloatProvider",
    "ConstantHeightProvider", "UniformHeightProvider", "BiasedToBottomHeightProvider", "VeryBiasedToBottomHeightProvider", "HeightProvider",
    "IntProvider", "ConstantIntProvider", "UniformIntProvider", "BiasedToBottomIntProvider", "ClampedIntProvider", "ClampedNormalIntProvider", "WeightedListIntProvider",
    "ConstantNumberProvider", "UniformNumberProvider", "BinomialNumberProvider", "ScoreboardNumberProvider", "StorageNumberProvider", "NumberProvider",
    # Resources
    "CustomStructure", "JigsawStructureType", "SingleCustomStructure", "CustomStructureSet", "RandomSpreadPlacementType", "ConcentricRingsPlacementType", "SpawnOverride", "DisableSpawnOverrideCategory", "CustomBiome", "MoodSound",
    "CustomAdvancement", "Criteria",
    "CustomBlock",
    "CustomDamageType", "DamageTypeTranslation",
    "CustomDimension", "CustomDimensionType", "OverworldDimension", "NetherDimension", "EndDimension",
    "CustomEnchantment",
    "WorldGenResources",
    "FacePaths", "CustomItemRenderDefinition", "CustomModelDefinition", "CustomTexture",
    "CustomItem",
    "CustomAutoAssignedFont", "BitMapFontChar", "SpaceFontChar", "TTFFontProvider", "ReferenceFontProvider",
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
    "ConditionalItemModel", "UsingItemConditional", "BrokenConditional", "DamagedConditional", "ComponentConditional", "HasComponentConditional", "FishingRodCastConditional", "BundleHasSelectedItemConditional", "SelectedConditional", "CarriedConditional", "ExtendedViewConditional", "KeyDownConditional", "ViewEntityConditional", "CustomModelDataConditional",
    "SelectItemModel", "SelectCase", "MainHandSelectProperty", "ChargeTypeSelectProperty", "TrimMaterialSelectProperty", "BlockStateSelectProperty", "DisplayContextSelectProperty", "LocalTimeSelectProperty", "ContextDimensionSelectProperty", "ContextEntityTypeSelectProperty", "CustomModelDataSelectProperty", "ComponentSelectProperty",
    "RangeDispatchItemModel", "BundleFullnessRangeDispatchProperty", "CompassRangeDispatchProperty", "CooldownRangeDispatchProperty", "CrossbowPullRangeDispatchProperty", "CountRangeDispatchProperty", "CustomModelDataRangeDispatchProperty", "DamageRangeDispatchProperty", "RangeDispatchPropertyType", "TimeRangeDispatchProperty", "UseCycleRangeDispatchProperty",
    "EmptyItemModel",
    "BundleSelectedItemModel",
    "SpecialItemModel", "BannerSpecialItemModelType", "BedSpecialItemModelType", "ChestSpecialItemModelType", "ConduitSpecialItemModelType", "DecoratedPotSpecialItemModelType", "HangingSignSpecialItemModelType", "HeadSpecialItemModelType", "ShieldSpecialItemModelType", "ShulkerBoxSpecialItemModelType", "StandingSignSpecialItemModelType", "TridentSpecialItemModelType",
    "ItemModel",

    # Script Repos
    "DEFAULT_ITEMS",

    # Pack.py
    "Pack",
]
