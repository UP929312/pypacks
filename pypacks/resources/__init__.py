# =============================================================================
# Resources
from pypacks.resources.custom_loot_tables.custom_loot_table import (
    BinomialDistributionEntry, UniformDistributionEntry, SingleItemRangeEntry,
    SingleItemPool, SimpleRangePool,
    CustomLootTable, SimpleRangeLootTable, SingleItemLootTable,
    LootContextTypes, LootContextPredicateTypes,
)
from pypacks.resources.custom_loot_tables.functions import (  # All 39...
    ApplyBonusFunction, CopyComponentsFunction, CopyCustomDataFunction, CopyNameFunction, CopyStateFunction,
    EnchantRandomlyFunction, EnchantWithLevelsFunction, EnchantedCountIncreaseFunction,
    ExplorationMapFunction, ExplosionDecayFunction, FillPlayerHeadFunction, FilteredFunction,
    FurnaceMeltFunction, LimitCountFunction, ModifyContentsFunction,
    ReferenceCallFunction, SequenceFunction, SetAttributesFunction,
    SetBannerPatternFunction, SetBookCoverFunction, SetComponentsFunction,
    SetContentsFunction, SetCountFunction, SetCustomDataFunction,
    SetCustomModelDataFunction, SetDamageFunction, SetEnchantsFunction,
    SetInstrumentFunction, SetFireWorkExplosion, SetFireworksFunction,
    SetItemFunction, SetLootTableFunction,
    SetLoreFunction, SetNameFunction, SetPotionFunction,
    SetStewEffectFunction, SetWrittenBookPagesFunction, SetWritableBookPagesFunction,
    ToggleToolTipsFunction,
)
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

__all__ = [
    # Resources
    "BinomialDistributionEntry", "UniformDistributionEntry", "SingleItemRangeEntry",
    "SingleItemPool", "SimpleRangePool",
    "CustomLootTable", "SimpleRangeLootTable", "SingleItemLootTable",
    "LootContextTypes", "LootContextPredicateTypes",

    "ApplyBonusFunction", "CopyComponentsFunction", "CopyCustomDataFunction", "CopyNameFunction", "CopyStateFunction",
    "EnchantRandomlyFunction", "EnchantWithLevelsFunction", "EnchantedCountIncreaseFunction",
    "ExplorationMapFunction", "ExplosionDecayFunction", "FillPlayerHeadFunction", "FilteredFunction",
    "FurnaceMeltFunction", "LimitCountFunction", "ModifyContentsFunction",
    "ReferenceCallFunction", "SequenceFunction", "SetAttributesFunction",
    "SetBannerPatternFunction", "SetBookCoverFunction", "SetComponentsFunction",
    "SetContentsFunction", "SetCountFunction", "SetCustomDataFunction",
    "SetCustomModelDataFunction", "SetDamageFunction", "SetEnchantsFunction",
    "SetInstrumentFunction", "SetFireWorkExplosion", "SetFireworksFunction",
    "SetItemFunction", "SetLootTableFunction",
    "SetLoreFunction", "SetNameFunction", "SetPotionFunction",
    "SetStewEffectFunction", "SetWrittenBookPagesFunction", "SetWritableBookPagesFunction",
    "ToggleToolTipsFunction",

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
    "CustomJukeboxSong",
    "CustomLanguage",
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
]
