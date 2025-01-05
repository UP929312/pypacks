from dataclasses import dataclass, field
from typing import Literal, Any, TypeAlias


def check_color(color: tuple[float, float, float]) -> None:
    assert 0 <= color[0] <= 1.0, "Red must be between 0 and 1"
    assert 0 <= color[1] <= 1.0, "Green must be between 0 and 1"
    assert 0 <= color[2] <= 1.0, "Blue must be between 0 and 1"

# TODO: Type Range dispatch, and special model types.

# ================================================================================================
# region: MODEL

@dataclass
class ModelItemModel:
    """Render a plain model from the models directory."""
    item_model_name: str  # Specifies the path to the model file of the item, in form of a Namespaced ID.
    tints: list[
        "ConstantTint | DyeTint | GrassTint | FireworkTint | PotionTint | MapColorTint | TeamTint | CustomModelDataTint"
    ] = field(default_factory=list)  # Optional. List of tint components to apply to the model.

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:model",
            "model": {
                "type": "minecraft:model",
                "model": self.item_model_name,
            } | ({
                "tints": [tint.to_dict() for tint in self.tints],
            } if self.tints else {}),
        }

@dataclass
class ConstantTint:
    """Return a constant RGB color."""
    color: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:constant",
            "value": list(self.color),
        }


@dataclass
class DyeTint:
    """Return value from minecraft:dyed_color component or default if not present"""
    default: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def to_dict(self) -> dict[str, Any]:
        check_color(self.default)
        return {
            "type": "minecraft:dye",
            "default": list(self.default),
        }


@dataclass
class GrassTint:
    """Return grass color at specific climate parameters, based on textures/colormap/grass.png"""
    temperature: float = 0.5
    downfall: float = 0.5

    def to_dict(self) -> dict[str, Any]:
        assert 0 <= self.temperature <= 1.0, "Temperature must be between 0 and 1"
        assert 0 <= self.downfall <= 1.0, "Downfall must be between 0 and 1"
        return {
            "type": "minecraft:grass",
            "temperature": self.temperature,
            "downfall": self.downfall,
        }


@dataclass
class FireworkTint:
    """Return average of colors from minecraft:firework_explosion component or default color if there are none."""
    default: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def to_dict(self) -> dict[str, Any]:
        check_color(self.default)
        return {
            "type": "minecraft:firework",
            "default": list(self.default),
        }


@dataclass
class PotionTint:
    """Return color from minecraft:potion_contents component:
        if component is present:
            custom_color value, if there is one present in component
            default color, if effect list is empty
            average of effect colors
        else, default color"""
    default: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def to_dict(self) -> dict[str, Any]:
        check_color(self.default)
        return {
            "type": "minecraft:potion",
            "default": list(self.default),
        }


@dataclass
class MapColorTint:
    """Return value from minecraft:map_color component or default color if component is not present."""
    default: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def to_dict(self) -> dict[str, Any]:
        check_color(self.default)
        return {
            "type": "minecraft:map_color",
            "default": list(self.default),
        }


@dataclass
class TeamTint:
    """Returns the team color of context entity, if any. Else, when there is no context entity, entity is not in a team or team has no color, return default."""
    default: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def to_dict(self) -> dict[str, Any]:
        check_color(self.default)
        return {
            "type": "minecraft:team",
            "default": list(self.default),
        }


@dataclass
class CustomModelDataTint:
    """Return value from colors list in minecraft:custom_model_data component."""
    index: int = 0  # Optional. Index for field in colors. Default: 0.
    default: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def to_dict(self) -> dict[str, Any]:
        check_color(self.default)
        return {
            "type": "minecraft:custom_model_data",
            "index": self.index,
            "default": list(self.default),
        }


TintsType: TypeAlias = ConstantTint | DyeTint | GrassTint | FireworkTint | PotionTint | MapColorTint | TeamTint | CustomModelDataTint

# endregion
# ================================================================================================
# region: COMPOSITE

@dataclass
class CompositeItemModel:
    """Render multiple sub-models in the same space."""
    # https://minecraft.wiki/w/Items_model_definition#composite
    models: list["str | ItemModelType"]  #  List of Item model objects to render.

    def to_dict(self) -> dict[str, Any]:
        return {
            "model": {
                "type": "minecraft:composite",
                "models": [
                    (
                        model.to_dict()["model"] if isinstance(model, ItemModelType) else
                        {
                            "type": "minecraft:model",
                            "model": model,
                        } 
                    )
                    for model in self.models
                ],
            }
        }

# endregion
# ================================================================================================
# region: CONDITIONAL

@dataclass
class ConditionalItemModel:
    # https://minecraft.wiki/w/Items_model_definition#conditional
    property_to_satisfy: "ConditionalBooleanPropertyType"
    true_model: "str | ItemModelType"  # The Item model object when the property is true.
    false_model: "str | ItemModelType"  # The Item model object when the property is false.

    def to_dict(self) -> dict[str, Any]:
        return {
            "model": {
                "type": "minecraft:condition",
                **self.property_to_satisfy.to_dict(),
                "on_true": self.true_model.to_dict()["model"] if isinstance(self.true_model, ItemModelType) else ({
                    "type": "model",
                    "model": self.true_model,
                }),
                "on_false": self.false_model.to_dict()["model"] if isinstance(self.false_model, ItemModelType) else ({
                    "type": "model",
                    "model": self.false_model,
                }),
            }
        }


class UsingItemConditional:
    """Return true if player is currently using this item."""
    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:using_item"}


class BrokenConditional:
    """Return true if the item is damageable and has only one use remaining before breaking."""
    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:broken"}


class DamagedConditional:
    """Return true if the item is damageable and has been used at least once."""
    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:damaged"}


@dataclass
class HasComponentConditional:
    """Return true if the given component is present on the item."""
    component: str  # Component name.
    ignore_default: bool = False   # Optional. If default component value should be handled as "no component". Default: false.

    def to_dict(self) -> dict[str, str | bool]:
        return {"property": "minecraft:has_component", "component": self.component, "ignore_default": self.ignore_default}


class FishingRodCastConditional:
    """Return true if there is a fishing bobber attached to currently used fishing rod."""
    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:fishing_rod/cast"}


class BundleHasSelectedItemConditional:
    """Return true if bundle is "open", i.e. it has selected item visible in GUI."""
    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:bundle_has_selected_item"}


class SelectedConditional:
    """Return true if item is selected on a hotbar."""
    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:selected"}


class CarriedConditional:
    """Return true if item is carried between slots in GUI (in the cursor)"""
    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:carried"}


class ExtendedViewConditional:
    """Return true if player has requested extended details by holding shift key down.
    Only works when item is displayed in UI.
    Note: not a keybind, can't be rebound."""
    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:extended_view"}

@dataclass
class KeyDownConditional:
    """Return true if key is pressed."""
    key: Literal[
        "key.jump", "key.sneak", "key.sprint", "key.left", "key.right", "key.back", "key.forward"
        "key.attack", "key.pickItem", "key.use", "key.drop", "key.hotbar.1", "key.hotbar.2",
        "key.hotbar.3", "key.hotbar.4", "key.hotbar.5", "key.hotbar.6", "key.hotbar.7", "key.hotbar.8",
        "key.hotbar.9", "key.inventory", "key.swapOffhand", "key.loadToolbarActivator"
        "key.saveToolbarActivator", "key.playerlist", "key.chat", "key.command", "key.socialInteractions", "key.advancements",
        "key.spectatorOutlines", "key.screenshot", "key.smoothCamera", "key.fullscreen", "key.togglePerspective",
    ]

    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:key_down", "keybind": self.key}


class ViewEntityConditional:
    """When not spectating, return true if context entity is the local player entity, i.e. the one controlled by client.
    When spectating, return true if context entity is the spectated entity.
    If context entity is not present, will return false."""

    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:view_entity"}


@dataclass
class CustomModelDataConditional:
    """Return value from flags list in minecraft:custom_model_data component."""
    index: int = 0  #  Optional. Index for field in flags. Default: 0.

    def to_dict(self) -> dict[str, str | int]:
        return {"property": "minecraft:custom_model_data", "index": self.index}


ConditionalBooleanPropertyType: TypeAlias = UsingItemConditional | BrokenConditional | DamagedConditional | HasComponentConditional | FishingRodCastConditional | BundleHasSelectedItemConditional | SelectedConditional | CarriedConditional | ExtendedViewConditional | KeyDownConditional | ViewEntityConditional | CustomModelDataConditional
# endregion
# ================================================================================================
# region: SELECT DISPATCH


@dataclass
class SelectItemModel:
    """Render an item model based on discrete property."""
    # https://minecraft.wiki/w/Items_model_definition#select
    property_to_satisfy: "SelectPropertyType" = field(default_factory=lambda: MainHandSelectProperty())  # The property to satisfy.
    cases: list["SelectCase"] = field(default_factory=lambda: [
        SelectCase(when="left", model="item/diamond_sword"), SelectCase(when="right", model="item/wooden_sword")
    ])  # List of cases to match.
    fallback_model: "str | ItemModelType | None" = None  # The Item model object if no valid entry was found. Optional, but will render a "missing" error model instead.

    def to_dict(self) -> dict[str, Any]:
        return {
            "model": {
                "type": "minecraft:select",
                **self.property_to_satisfy.to_dict(),
                "cases": [case.to_dict() for case in self.cases],
            } | (
                {
                    "fallback": (self.fallback_model.to_dict()["model"] if isinstance(self.fallback_model, ItemModelType) else {
                        "type": "minecraft:model",
                        "model": self.fallback_model,
                    })
                } if self.fallback_model else {}
            )
        } 


@dataclass
class SelectCase:
    """Used to match the seelct cases for select item model."""
    when: str | list[str]
    model: "str | ItemModelType"

    def to_dict(self) -> dict[str, Any]:
        return {
            "when": self.when,
            "model": self.model.to_dict() if isinstance(self.model, ItemModelType) else {
                "type": "minecraft:model",
                "model": self.model,
            },
        }


class MainHandSelectProperty:
    """Return main hand of holding player."""
    # https://minecraft.wiki/w/Items_model_definition#main_hand
    # Values: "left", "right"

    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:main_hand"}


class ChargeTypeSelectProperty:
    """Return charge type stored in minecraft:charged_projectiles component."""
    # https://minecraft.wiki/w/Items_model_definition#charge_type
    # Values: "none", "rocket", "arrow"

    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:charge_type"}


class TrimMaterialSelectProperty:
    """Return value of material field from minecraft:trim component, if present."""
    # https://minecraft.wiki/w/Items_model_definition#trim_material
    # Values: Namespaced ID trim material.

    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:trim_material"}


@dataclass
# block_state
class BlockStateSelectProperty:
    """Return value for some property from minecraft:block_state component."""
    # https://minecraft.wiki/w/Items_model_definition#block_state
    # Values: Block state.
    block_state_property: str

    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:block_state", "block_state_property": self.block_state_property}


class DisplayContextSelectProperty:
    """Return context this item is rendered in."""
    # https://minecraft.wiki/w/Items_model_definition#trim_material
    # Values: `none`, `thirdperson_lefthand`, `thirdperson_righthand`, `firstperson_lefthand`, `firstperson_righthand`, `head`, `gui`, `ground`, `fixed`

    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:display_context"}


@dataclass
class LocalTimeSelectProperty:
    """Returns the current time formatted according to a given pattern. The value is updated every second.
    For full format documentation for locale, time zone and pattern, see ICU (International Components for Unicode) documentation."""
    # https://minecraft.wiki/w/Items_model_definition#local_time
    # Values: Any string.

    locale: str | None = "en_US"  # Value describing locale Default "" which means "root" locale (a set of defaults, including English names).
    # Optional. Locale to use for formatting. Default: "en_US".
    # cs_AU@numbers=thai;calendar=japanese: Czech language, Australian formatting, Thai numerals and Japanese calendar.
    time_zone: str | None = "UTC"  # describes format to be used for time formatting.
    # Examples: Europe/Stockholm, GMT+0:45
    pattern: str | None = None #  Optional. Describing time. If not present, defaults to timezone set on client.
    # yyyy-MM-dd: 4-digit year number, then 2-digit month number, then 2-digit day of month number, all zero-padded if needed, separated by -.
    # HH:mm:ss: current time (hours, minutes, seconds), 24-hour cycle, all zero-padded to 2 digits of needed, separated by :.

    def to_dict(self) -> dict[str, str]:
        return {
            "property": "minecraft:local_time"
        } | ({
            "locale": self.locale,
        } if self.locale else {}) | ({
            "time_zone": self.time_zone,
        } if self.time_zone else {}) | ({
            "pattern": self.pattern,
        } if self.pattern else {})


class ContextDimensionSelectProperty:
    """Return the ID of the dimension in context, if any."""
    # https://minecraft.wiki/w/Items_model_definition#context_dimension
    # Values: Namespaced dimension ID.

    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:context_dimension"}


class ContextEntityTypeSelectProperty:
    """Return the holding entity type, if present."""
    # https://minecraft.wiki/w/Items_model_definition#context_entity_type
    # Values: Namespaced entity type ID.

    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:context_entity_type"}


@dataclass
class CustomModelDataSelectProperty:
    """Return value from strings list in minecraft:custom_model_data component."""
    index: int = 0
    # Values: Any string.

    def to_dict(self) -> dict[str, str | int]:
        return {"property": "minecraft:custom_model_data", "index": self.index}


SelectPropertyType: TypeAlias = (
    MainHandSelectProperty | ChargeTypeSelectProperty | TrimMaterialSelectProperty | BlockStateSelectProperty | DisplayContextSelectProperty |
    LocalTimeSelectProperty | ContextDimensionSelectProperty | ContextEntityTypeSelectProperty | CustomModelDataSelectProperty
)
# endregion
# ================================================================================================
# region: RANGE DISPATCH
RangeDispatchPropertyType = Literal[
    "minecraft:bundle/fullness", "minecraft:damage", "minecraft:count", "minecraft:cooldown", "minecraft:time", "minecraft:compass", "minecraft:crossbow/pull",
    "minecraft:use_duration", "minecraft:use_cycle", "minecraft:custom_model_data"
]

@dataclass
class RangeDispatchItemModel:
    """Render an item model based on numeric property. Will select last entry with threshold less or equal to property value."""
    # https://minecraft.wiki/w/Items_model_definition#range_dispatch
    # TODO: Type hint all the Range dispatches, as 
    property_to_satisfy: RangeDispatchPropertyType
    scale: float = 1.0  # Optional. Factor to multiply property value with. Default: 1.0.
    entries: dict[int | float, "str | ItemModelType"] = field(default_factory=dict)  # A mapping of threshold to item model name.
    additional_data: dict[str, Any] = field(default_factory=dict)  # e.g. {"normalize": True} - (for damage).
    fallback_model: "str | ItemModelType | None" = None  #  The Item model object if no valid entry was found. Optional, but will render a "missing" error model instead.

    def to_dict(self) -> dict[str, Any]:
        return {
            "model": {
                "type": "minecraft:range_dispatch",
                "property": self.property_to_satisfy,
                "scale": self.scale,
                **self.additional_data,
                "entries": [
                    {"threshold": threshold, "model": model.to_dict()["model"] if isinstance(model, ItemModelType) else {"type": "minecraft:model", "model": model}}
                    for threshold, model in self.entries.items()
                ],
            } | (
                {
                    "fallback": (self.fallback_model.to_dict()["model"] if isinstance(self.fallback_model, ItemModelType) else {
                        "type": "minecraft:model",
                        "model": self.fallback_model,
                    })
                } if self.fallback_model else {}
            )
        }
# endregion
# ================================================================================================
# region: EMPTY

class EmptyItemModel:
    """Does not render anything."""
    # https://minecraft.wiki/w/Items_model_definition#empty
    def to_dict(self) -> dict[str, Any]:
        return {"model": {"type": "minecraft:empty"}}

# endregion
# ================================================================================================
# region: BUNDLE SELECTED ITEM

class BundleSelectedItemModel:
    """Render the selected stack in minecraft:bundle_contents component, if present, otherwise does nothing."""
    # https://minecraft.wiki/w/Items_model_definition#bundle/selected_item
    def to_dict(self) -> dict[str, Any]:
        return {"model": {"type": "minecraft:bundle/selected_item"}}

# endregion
# ================================================================================================
# region: SPECIAL

SpecialItemModelType = Literal[
    "minecraft:bed", "minecraft:banner", "minecraft:conduit", "minecraft:chest", "minecraft:decorated_pot", "minecraft:head",
    "minecraft:shulker_box", "minecraft:shield", "minecraft:standing_sign", "minecraft:hanging_sign", "minecraft:trident"
]


@dataclass
class SpecialItemModel:
    """Render a special model."""
    # https://minecraft.wiki/w/Items_model_definition#special_model_types
    # TODO: Type this too.
    model_type: SpecialItemModelType
    base: str  #  Namespaced ID of model in models directory, to providing transformations, particle texture and GUI light.
    additional_data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "model": {
                "type": "minecraft:special",
                "model": {
                    "type": self.model_type,
                    **self.additional_data
                },
                "base": self.base,
            }
        }

# endregion
# ================================================================================================

ItemModelType: TypeAlias = (
    ModelItemModel | CompositeItemModel | ConditionalItemModel | SelectItemModel | RangeDispatchItemModel | EmptyItemModel | BundleSelectedItemModel | SpecialItemModel
)
