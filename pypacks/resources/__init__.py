# =============================================================================
# Loot table
from pypacks.resources.custom_loot_tables.custom_loot_table import (
    SingleItemPool, SimpleRangePool,
    CustomLootTable, SimpleRangeLootTable, SingleItemLootTable,
    LootContextTypes, LootContextPredicateTypes,
)
from pypacks.resources.custom_loot_tables.functions import (  # All 39...
    ApplyBonusFunction, CopyComponentsFunction, CopyCustomDataFunction, CopyNameFunction, CopyStateFunction,
    EnchantRandomlyFunction, EnchantWithLevelsFunction, EnchantedCountIncreaseFunction,
    ExplorationMapFunction, ExplosionDecayFunction, FillPlayerHeadFunction, FilteredFunction,
    FurnaceSmeltFunction, LimitCountFunction, ModifyContentsFunction,
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
# =============================================================================
# Entities
from pypacks.resources.entities.spawn_conditions import BiomeSpawnCondition, StructureSpawnCondition, MoonBrightnessSpawnCondition
from pypacks.resources.entities import EntityVariant
from pypacks.resources.entities.cat_variant import CatVariant
from pypacks.resources.entities.chicken_variant import ChickenVariant
from pypacks.resources.entities.cow_variant import CowVariant
from pypacks.resources.entities.frog_variant import FrogVariant
from pypacks.resources.entities.pig_variant import PigVariant
from pypacks.resources.entities.wolf_variant import WolfVariant
# =============================================================================
# World Gen
from pypacks.resources.world_gen import (  # type: ignore[attr-defined]
    CustomStructure, JigsawStructureType, SingleCustomStructure, CustomStructureSet, RandomSpreadPlacementType, ConcentricRingsPlacementType, CustomBiome, MoodSound, GameTestStructure,
    WorldGenResources,
)
from pypacks.resources.world_gen.entity_spawner import SpawnOverride, DisableSpawnOverrideCategory
# =============================================================================
# Regular
from pypacks.resources.custom_advancement import CustomAdvancement, Criteria
from pypacks.resources.custom_damage_type import CustomDamageType, DamageTypeTranslation
from pypacks.resources.custom_dimension import CustomDimension, CustomDimensionType, OverworldDimension, NetherDimension, EndDimension
from pypacks.resources.custom_enchantment import (
    CustomEnchantment,
    EnchantValueEffect, SetValueEffect, AddValueEffect, MultiplyValueEffect, RemoveBinomialValueEffect, AllOfValueEffect,
    EnchantmentEntityEffect, AllOfEntityEffect, ApplyMobEffectEntityEffect,  DamageEntityEntityEffect, ChangeItemDamageEntityEffect, ExplodeEntityEffect, IgniteEntityEffect,
    PlaySoundEntityEffect, ReplaceBlockEntityEffect, ReplaceDiskEntityEffect, RunFunctionEntityEffect, SetBlockPropertiesEntityEffect, SpawnParticlesEntityEffect, SummonEntityEntityEffect

)
from pypacks.resources.custom_model import FacePaths, CustomItemRenderDefinition, CustomModelDefinition, CustomTexture
from pypacks.resources.custom_item import CustomItem
from pypacks.resources.custom_font import CustomAutoAssignedFont, BitMapFontChar, SpaceFontChar, TTFFontProvider, ReferenceFontProvider
from pypacks.resources.custom_game_test import (
    CustomGameTest, AllOfEnvironment, FunctionEnvironment, GameRulesEnvironment, TimeOfDayEnvironment, WeatherEnvironment, CustomTestEnvironment,
)
from pypacks.resources.custom_jukebox_song import CustomJukeboxSong
from pypacks.resources.custom_language import CustomLanguage
from pypacks.resources.custom_mcfunction import MCFunction

from pypacks.resources.custom_painting import CustomPainting
from pypacks.resources.custom_predicate import (
    Predicate,
    AllOfPredicate, AnyOfPredicate, BlockStatePropertyPredicate, DamageSourcePropertiesPredicate, EnchantmentActiveCheckPredicate, EntityPropertiesPredicate,
    EntityScoresPredicate, InvertedPredicate, KilledByPlayerPredicate, LocationCheckPredicate, MatchToolPredicate, RandomChancePredicate,
    RandomChanceWithEnchantedBonusPredicate, ReferencePredicate, SurvivesExplosionPredicate, TableBonusPredicate, TimeCheckPredicate, ValueCheckPredicate,
    WeatherCheckPredicate,
)
from pypacks.resources.predicate.predicate_conditions import (
    DamageTypeTag, EntityDistance, EntityFlags, MovementCheck, EntityCondition, BlockPredicate, FluidPredicate, LocationTag, ItemCondition,
)
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
    SelectItemModel, SelectCase, MainHandSelectProperty, ChargeTypeSelectProperty, TrimMaterialSelectProperty, BlockStateSelectProperty, DisplayContextSelectProperty, LocalTimeSelectProperty, ContextDimensionSelectProperty, ContextEntityTypeSelectProperty, CustomModelDataSelectProperty, ComponentSelectProperty,
    RangeDispatchItemModel, BundleFullnessRangeDispatchProperty, CompassRangeDispatchProperty, CooldownRangeDispatchProperty, CrossbowPullRangeDispatchProperty, CountRangeDispatchProperty, CustomModelDataRangeDispatchProperty, DamageRangeDispatchProperty, RangeDispatchPropertyType, TimeRangeDispatchProperty, UseCycleRangeDispatchProperty,
    EmptyItemModel,
    BundleSelectedItemModel,
    SpecialItemModel, BannerSpecialItemModelType, BedSpecialItemModelType, ChestSpecialItemModelType, ConduitSpecialItemModelType, DecoratedPotSpecialItemModelType, HangingSignSpecialItemModelType, HeadSpecialItemModelType, ShieldSpecialItemModelType, ShulkerBoxSpecialItemModelType, StandingSignSpecialItemModelType, TridentSpecialItemModelType,
    ItemModel,
)

__all__ = [
    # Loot Table
    "SingleItemPool", "SimpleRangePool",
    "CustomLootTable", "SimpleRangeLootTable", "SingleItemLootTable",
    "LootContextTypes", "LootContextPredicateTypes",

    "ApplyBonusFunction", "CopyComponentsFunction", "CopyCustomDataFunction", "CopyNameFunction", "CopyStateFunction",
    "EnchantRandomlyFunction", "EnchantWithLevelsFunction", "EnchantedCountIncreaseFunction",
    "ExplorationMapFunction", "ExplosionDecayFunction", "FillPlayerHeadFunction", "FilteredFunction",
    "FurnaceSmeltFunction", "LimitCountFunction", "ModifyContentsFunction",
    "ReferenceCallFunction", "SequenceFunction", "SetAttributesFunction",
    "SetBannerPatternFunction", "SetBookCoverFunction", "SetComponentsFunction",
    "SetContentsFunction", "SetCountFunction", "SetCustomDataFunction",
    "SetCustomModelDataFunction", "SetDamageFunction", "SetEnchantsFunction",
    "SetInstrumentFunction", "SetFireWorkExplosion", "SetFireworksFunction",
    "SetItemFunction", "SetLootTableFunction",
    "SetLoreFunction", "SetNameFunction", "SetPotionFunction",
    "SetStewEffectFunction", "SetWrittenBookPagesFunction", "SetWritableBookPagesFunction",
    "ToggleToolTipsFunction",

    # Entities
    "BiomeSpawnCondition", "StructureSpawnCondition", "MoonBrightnessSpawnCondition", "EntityVariant",
    "CatVariant", "ChickenVariant", "CowVariant", "FrogVariant", "PigVariant", "WolfVariant",

    # Predicate Conditions
    "AllOfPredicate", "AnyOfPredicate", "BlockStatePropertyPredicate", "DamageSourcePropertiesPredicate", "EnchantmentActiveCheckPredicate",
    "EntityPropertiesPredicate", "EntityScoresPredicate", "InvertedPredicate", "KilledByPlayerPredicate",
    "LocationCheckPredicate", "MatchToolPredicate", "RandomChancePredicate", "RandomChanceWithEnchantedBonusPredicate",
    "ReferencePredicate", "SurvivesExplosionPredicate", "TableBonusPredicate", "TimeCheckPredicate", "ValueCheckPredicate",
    "WeatherCheckPredicate",
    "DamageTypeTag", "EntityDistance", "EntityFlags", "MovementCheck", "EntityCondition", "BlockPredicate", "FluidPredicate", "LocationTag", "ItemCondition",

    # World Gen
    "CustomStructure", "JigsawStructureType", "SingleCustomStructure", "CustomStructureSet", "RandomSpreadPlacementType", "ConcentricRingsPlacementType",
    "SpawnOverride", "DisableSpawnOverrideCategory", "CustomBiome", "MoodSound", "GameTestStructure", "WorldGenResources",

    # More
    "CustomAdvancement", "Criteria",
    "CustomDamageType", "DamageTypeTranslation",
    "CustomDimension", "CustomDimensionType", "OverworldDimension", "NetherDimension", "EndDimension",
    "CustomEnchantment",
    "EnchantValueEffect", "SetValueEffect", "AddValueEffect", "MultiplyValueEffect", "RemoveBinomialValueEffect", "AllOfValueEffect",
    "EnchantmentEntityEffect", "AllOfEntityEffect", "ApplyMobEffectEntityEffect", "DamageEntityEntityEffect", "ChangeItemDamageEntityEffect", "ExplodeEntityEffect", "IgniteEntityEffect",
    "PlaySoundEntityEffect", "ReplaceBlockEntityEffect", "ReplaceDiskEntityEffect", "RunFunctionEntityEffect", "SetBlockPropertiesEntityEffect", "SpawnParticlesEntityEffect", "SummonEntityEntityEffect",
    "FacePaths", "CustomItemRenderDefinition", "CustomModelDefinition", "CustomTexture",
    "CustomItem",
    "CustomAutoAssignedFont", "BitMapFontChar", "SpaceFontChar", "TTFFontProvider", "ReferenceFontProvider",
    "CustomGameTest", "AllOfEnvironment", "FunctionEnvironment", "GameRulesEnvironment", "TimeOfDayEnvironment", "WeatherEnvironment", "CustomTestEnvironment",
    "CustomJukeboxSong",
    "CustomLanguage",
    "MCFunction",
    "CustomLootTable",
    "CustomPainting",

    "Predicate",

    # Rest
    "Recipe", "CustomCrafterRecipe", "ShapedCraftingRecipe", "ShapelessCraftingRecipe", "CraftingTransmuteRecipe", "FurnaceRecipe", "BlastFurnaceRecipe", "SmokerRecipe",
    "CampfireRecipe", "SmithingTransformRecipe", "SmithingTrimRecipe", "StonecutterRecipe",
    "CustomSound",
    "CustomTag",

    "ModelItemModel", "ConstantTint", "DyeTint", "GrassTint", "FireworkTint", "PotionTint", "MapColorTint", "TeamTint", "CustomModelDataTint",
    "CompositeItemModel",
    "ConditionalItemModel", "UsingItemConditional", "BrokenConditional", "DamagedConditional", "HasComponentConditional", "FishingRodCastConditional", "BundleHasSelectedItemConditional", "SelectedConditional", "CarriedConditional", "ExtendedViewConditional", "KeyDownConditional", "ViewEntityConditional", "CustomModelDataConditional",
    "SelectItemModel", "SelectCase", "MainHandSelectProperty", "ChargeTypeSelectProperty", "TrimMaterialSelectProperty", "BlockStateSelectProperty", "DisplayContextSelectProperty", "LocalTimeSelectProperty", "ContextDimensionSelectProperty", "ContextEntityTypeSelectProperty", "CustomModelDataSelectProperty", "ComponentSelectProperty",
    "RangeDispatchItemModel", "BundleFullnessRangeDispatchProperty", "CompassRangeDispatchProperty", "CooldownRangeDispatchProperty", "CrossbowPullRangeDispatchProperty", "CountRangeDispatchProperty", "CustomModelDataRangeDispatchProperty", "DamageRangeDispatchProperty", "RangeDispatchPropertyType", "TimeRangeDispatchProperty", "UseCycleRangeDispatchProperty",
    "EmptyItemModel",
    "BundleSelectedItemModel",
    "SpecialItemModel", "BannerSpecialItemModelType", "BedSpecialItemModelType", "ChestSpecialItemModelType", "ConduitSpecialItemModelType", "DecoratedPotSpecialItemModelType", "HangingSignSpecialItemModelType", "HeadSpecialItemModelType", "ShieldSpecialItemModelType", "ShulkerBoxSpecialItemModelType", "StandingSignSpecialItemModelType", "TridentSpecialItemModelType",
    "ItemModel",
]
