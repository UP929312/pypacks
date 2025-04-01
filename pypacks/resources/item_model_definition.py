from dataclasses import dataclass, field
from typing import Literal, Any, TYPE_CHECKING

from pypacks.additions.constants import MinecraftColor
from pypacks.utils import recursively_remove_nones_from_data

if TYPE_CHECKING:
    from pypacks.scripts.repos.models import MinecraftModels
    from pypacks.resources.custom_predicate import Predicate


def check_color(color: tuple[float, float, float]) -> None:
    assert 0 <= color[0] <= 1.0, "Red must be between 0 and 1"
    assert 0 <= color[1] <= 1.0, "Green must be between 0 and 1"
    assert 0 <= color[2] <= 1.0, "Blue must be between 0 and 1"


class ItemModel:
    """Parent item model, don't instantiate yourself!"""
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ItemModel":
        cls_ = ITEM_MODEL_NAME_TO_CLASSES[data["type"]]
        return cls_.from_dict(data)

# ================================================================================================
# region: MODEL


@dataclass
class ModelItemModel(ItemModel):
    """Render a plain model from the models directory."""
    item_model_name: "str | MinecraftModels"  # Specifies the path to the model file of the item, in form of a Namespaced ID.
    tints: list["Tint"] = field(default_factory=list)  # Optional. List of tint components to apply to the model.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:model",
            "model": {
                "type": "minecraft:model",
                "model": self.item_model_name,
            } | ({
                "tints": [tint.to_dict(pack_namespace) for tint in self.tints],
            } if self.tints else {}),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ModelItemModel":
        return cls(
            data["model"]["model"],
            tints=[tint.from_dict() for tint in data.get("tints", [])],
        )


# ==== Tints
class Tint:
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Tint":
        cls_ = TINT_NAME_TO_CLASSES[data["type"]]
        return cls_.from_dict(data)


@dataclass
class ConstantTint(Tint):
    """Return a constant RGB color."""
    color: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:constant",
            "value": list(self.color),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConstantTint":
        return cls(
            data["value"]
        )


@dataclass
class DyeTint(Tint):
    """Return value from minecraft:dyed_color component or default if not present"""
    default: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def __post_init__(self) -> None:
        check_color(self.default)

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:dye",
            "default": list(self.default),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DyeTint":
        return cls(
            data["default"]
        )


@dataclass
class GrassTint(Tint):
    """Return grass color at specific climate parameters, based on textures/colormap/grass.png"""
    temperature: float = 0.5
    downfall: float = 0.5

    def __post_init__(self) -> None:
        assert 0 <= self.temperature <= 1.0, "Temperature must be between 0 and 1"
        assert 0 <= self.downfall <= 1.0, "Downfall must be between 0 and 1"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:grass",
            "temperature": self.temperature,
            "downfall": self.downfall,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GrassTint":
        return cls(
            data["temperature"],
            data["downfall"],
        )


@dataclass
class FireworkTint(Tint):
    """Return average of colors from minecraft:firework_explosion component or default color if there are none."""
    default: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def __post_init__(self) -> None:
        check_color(self.default)

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:firework",
            "default": list(self.default),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FireworkTint":
        return cls(
            data["default"],
        )


@dataclass
class PotionTint(Tint):
    """Return color from minecraft:potion_contents component:
        if component is present:
            custom_color value, if there is one present in component
            default color, if effect list is empty
            average of effect colors
        else, default color"""
    default: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def __post_init__(self) -> None:
        check_color(self.default)

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:potion",
            "default": list(self.default),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PotionTint":
        return cls(
            data["default"],
        )


@dataclass
class MapColorTint(Tint):
    """Return value from minecraft:map_color component or default color if component is not present."""
    default: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def __post_init__(self) -> None:
        check_color(self.default)

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:map_color",
            "default": list(self.default),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MapColorTint":
        return cls(
            data["default"],
        )


@dataclass
class TeamTint(Tint):
    """Returns the team color of context entity, if any. Else, when there is no context entity, entity is not in a team or team has no color, return default."""
    default: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def __post_init__(self) -> None:
        check_color(self.default)

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:team",
            "default": list(self.default),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TeamTint":
        return cls(
            data["default"],
        )


@dataclass
class CustomModelDataTint(Tint):
    """Return value from colors list in minecraft:custom_model_data component."""
    index: int = 0  # Optional. Index for field in colors. Default: 0.
    default: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        check_color(self.default)
        return {
            "type": "minecraft:custom_model_data",
            "index": self.index,
            "default": list(self.default),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CustomModelDataTint":
        return cls(
            data.get("index", 0),
            data["default"],
        )


TINT_NAME_TO_CLASSES: dict[str, type["Tint"]] = {
    "minecraft:constant": ConstantTint,
    "minecraft:dye": DyeTint,
    "minecraft:grass": GrassTint,
    "minecraft:firework": FireworkTint,
    "minecraft:potion": PotionTint,
    "minecraft:map_color": MapColorTint,
    "minecraft:team": TeamTint,
    "minecraft:custom_model_data": CustomModelDataTint,

}

# endregion
# ================================================================================================
# region: COMPOSITE


@dataclass
class CompositeItemModel(ItemModel):
    """Render multiple sub-models in the same space."""
    # https://minecraft.wiki/w/Items_model_definition#composite
    models: list["str | ItemModel"]  # List of Item model objects to render.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "model": {
                "type": "minecraft:composite",
                "models": [
                    (
                        model.to_dict(pack_namespace)["model"] if isinstance(model, ItemModel) else
                        {
                            "type": "minecraft:model",
                            "model": model,
                        }
                    )
                    for model in self.models
                ],
            }
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CompositeItemModel":
        return cls(
            models=[x.from_dict() for x in data["model"]["models"]],
        )


# endregion
# ================================================================================================
# region: CONDITIONAL


@dataclass
class ConditionalItemModel(ItemModel):
    # https://minecraft.wiki/w/Items_model_definition#conditional
    property_to_satisfy: "ConditionalBooleanPropertyType"
    true_model: "str | ItemModel"  # The Item model object when the property is true.
    false_model: "str | ItemModel"  # The Item model object when the property is false.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "model": {
                "type": "minecraft:condition",
                **self.property_to_satisfy.to_dict(pack_namespace),
                "on_true": self.true_model.to_dict(pack_namespace)["model"] if isinstance(self.true_model, ItemModel) else ({
                    "type": "model",
                    "model": self.true_model,
                }),
                "on_false": self.false_model.to_dict(pack_namespace)["model"] if isinstance(self.false_model, ItemModel) else ({
                    "type": "model",
                    "model": self.false_model,
                }),
            }
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConditionalItemModel":
        property_to_satisfy = CONDITIONAL_BOOLEAN_PROPERTY_NAME_TO_CLASSES[data["property"]]
        return cls(
            property_to_satisfy=property_to_satisfy.from_dict(data),
            true_model=ItemModel.from_dict(data["on_true"]),
            false_model=ItemModel.from_dict(data["on_false"]),
        )


class ConditionalBooleanPropertyType:
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConditionalBooleanPropertyType":
        cls_ = CONDITIONAL_BOOLEAN_PROPERTY_NAME_TO_CLASSES[data["property"]]
        return cls_.from_dict(data)


class UsingItemConditional(ConditionalBooleanPropertyType):
    """Return true if player is currently using this item."""
    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:using_item"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UsingItemConditional":
        return cls()


class BrokenConditional(ConditionalBooleanPropertyType):
    """Return true if the item is damageable and has only one use remaining before breaking."""
    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:broken"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BrokenConditional":
        return cls()


class DamagedConditional(ConditionalBooleanPropertyType):
    """Return true if the item is damageable and has been used at least once."""
    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:damaged"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DamagedConditional":
        return cls()


@dataclass
class HasComponentConditional(ConditionalBooleanPropertyType):
    """Return true if the given component is present on the item."""
    component: str  # Component name.
    ignore_default: bool = False   # Optional. If default component value should be handled as "no component". Default: false.

    def to_dict(self, pack_namespace: str) -> dict[str, str | bool]:
        return {"property": "minecraft:has_component", "component": self.component, "ignore_default": self.ignore_default}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HasComponentConditional":
        return cls(
            component=data["component"],
            ignore_default=data.get("ignore_default", False),
        )


class FishingRodCastConditional(ConditionalBooleanPropertyType):
    """Return true if there is a fishing bobber attached to currently used fishing rod."""
    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:fishing_rod/cast"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FishingRodCastConditional":
        return cls()


class BundleHasSelectedItemConditional(ConditionalBooleanPropertyType):
    """Return true if bundle is "open", i.e. it has selected item visible in GUI."""
    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:bundle_has_selected_item"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BundleHasSelectedItemConditional":
        return cls()


class SelectedConditional(ConditionalBooleanPropertyType):
    """Return true if item is selected on a hotbar."""
    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:selected"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SelectedConditional":
        return cls()


class CarriedConditional(ConditionalBooleanPropertyType):
    """Return true if item is carried between slots in GUI (in the cursor)"""
    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:carried"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CarriedConditional":
        return cls()


@dataclass
class ComponentConditional(ConditionalBooleanPropertyType):
    """Uses component item sub predicates to match item components."""
    predicate: "str | Predicate"
    value: str | list[dict[str, str]]
    # https://minecraft.wiki/w/Items_model_definition#component

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        from pypacks.resources.custom_predicate import Predicate
        return {
            "property": "minecraft:component",
            "predicate": self.predicate.to_dict(pack_namespace) if isinstance(self.predicate, Predicate) else self.predicate,
            "value": self.value}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ComponentConditional":
        return cls(
            data["predicate"],
            data["value"],
        )


class ExtendedViewConditional(ConditionalBooleanPropertyType):
    """Return true if player has requested extended details by holding shift key down.
    Only works when item is displayed in UI.
    Note: not a keybind, can't be rebound."""
    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:extended_view"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExtendedViewConditional":
        return cls()


@dataclass
class KeyDownConditional(ConditionalBooleanPropertyType):
    """Return true if key is pressed."""
    key: Literal[
        "key.jump", "key.sneak", "key.sprint", "key.left", "key.right", "key.back", "key.forward"
        "key.attack", "key.pickItem", "key.use", "key.drop", "key.hotbar.1", "key.hotbar.2",
        "key.hotbar.3", "key.hotbar.4", "key.hotbar.5", "key.hotbar.6", "key.hotbar.7", "key.hotbar.8",
        "key.hotbar.9", "key.inventory", "key.swapOffhand", "key.loadToolbarActivator"
        "key.saveToolbarActivator", "key.playerlist", "key.chat", "key.command", "key.socialInteractions", "key.advancements",
        "key.spectatorOutlines", "key.screenshot", "key.smoothCamera", "key.fullscreen", "key.togglePerspective",
    ]

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:key_down", "keybind": self.key}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "KeyDownConditional":
        return cls(
            data["keybind"]
        )


class ViewEntityConditional(ConditionalBooleanPropertyType):
    """When not spectating, return true if context entity is the local player entity, i.e. the one controlled by client.
    When spectating, return true if context entity is the spectated entity.
    If context entity is not present, will return false."""

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:view_entity"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ViewEntityConditional":
        return cls()


@dataclass
class CustomModelDataConditional(ConditionalBooleanPropertyType):
    """Return value from flags list in minecraft:custom_model_data component."""
    index: int = 0  # Optional. Index for field in flags. Default: 0.

    def to_dict(self, pack_namespace: str) -> dict[str, str | int]:
        return {"property": "minecraft:custom_model_data", "index": self.index}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CustomModelDataConditional":
        return cls(
            data["index"]
        )


CONDITIONAL_BOOLEAN_PROPERTY_NAME_TO_CLASSES: dict[str, type[ConditionalBooleanPropertyType]] = {
    "minecraft:using_item": UsingItemConditional,
    "minecraft:broken": BrokenConditional,
    "minecraft:damaged": DamagedConditional,
    "minecraft:has_component": HasComponentConditional,
    "minecraft:fishing_rod/cast": FishingRodCastConditional,
    "minecraft:bundle_has_selected_item": BundleHasSelectedItemConditional,
    "minecraft:selected": SelectedConditional,
    "minecraft:carried": CarriedConditional,
    "minecraft:component": ComponentConditional,
    "minecraft:extended_view": ExtendedViewConditional,
    "minecraft:key_down": KeyDownConditional,
    "minecraft:view_entity": ViewEntityConditional,
    "minecraft:custom_model_data": CustomModelDataConditional,
}

# endregion
# ================================================================================================
# region: SELECT DISPATCH


@dataclass
class SelectItemModel(ItemModel):
    """Render an item model based on discrete property."""
    # https://minecraft.wiki/w/Items_model_definition#select
    property_to_satisfy: "SelectProperty" = field(default_factory=lambda: MainHandSelectProperty())  # The property to satisfy.
    cases: list["SelectCase"] = field(default_factory=lambda: [
        SelectCase(when="left", model="item/diamond_sword"), SelectCase(when="right", model="item/wooden_sword")
    ])  # List of cases to match.
    fallback_model: "str | ItemModel | None" = None  # The Item model object if no valid entry was found. Optional, but will render a "missing" error model instead.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "model": {
                "type": "minecraft:select",
                **self.property_to_satisfy.to_dict(pack_namespace),
                "cases": [case.to_dict(pack_namespace) for case in self.cases],
            } | (
                {
                    "fallback": (self.fallback_model.to_dict(pack_namespace)["model"] if isinstance(self.fallback_model, ItemModel) else {
                        "type": "minecraft:model",
                        "model": self.fallback_model,
                    })
                } if self.fallback_model else {}
            )
        }


class SelectProperty:
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SelectProperty":
        cls_ = SELECT_PROPERTY_NAME_TO_CLASSES[data["property"]]
        return cls_.from_dict(data)


@dataclass
class SelectCase:
    """Used to match the seelct cases for select item model."""
    when: str | list[str]
    model: "str | ItemModel"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "when": self.when,
            "model": self.model.to_dict(pack_namespace) if isinstance(self.model, ItemModel) else {
                "type": "minecraft:model",
                "model": self.model,
            },
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SelectCase":
        return cls(
            data["when"],
            ItemModel.from_dict(data["model"]),
        )


class MainHandSelectProperty(SelectProperty):
    """Return main hand of holding player."""
    # https://minecraft.wiki/w/Items_model_definition#main_hand
    # Values: "left", "right"

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:main_hand"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MainHandSelectProperty":
        return cls()


class ChargeTypeSelectProperty(SelectProperty):
    """Return charge type stored in minecraft:charged_projectiles component."""
    # https://minecraft.wiki/w/Items_model_definition#charge_type
    # Values: "none", "rocket", "arrow"

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:charge_type"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ChargeTypeSelectProperty":
        return cls()


class TrimMaterialSelectProperty(SelectProperty):
    """Return value of material field from minecraft:trim component, if present."""
    # https://minecraft.wiki/w/Items_model_definition#trim_material
    # Values: Namespaced ID trim material.

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:trim_material"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TrimMaterialSelectProperty":
        return cls()


@dataclass
class BlockStateSelectProperty(SelectProperty):
    """Return value for some property from minecraft:block_state component."""
    # https://minecraft.wiki/w/Items_model_definition#block_state
    # Values: Block state.
    block_state_property: str

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:block_state", "block_state_property": self.block_state_property}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BlockStateSelectProperty":
        return cls(
            data["block_state_property"]
        )


class DisplayContextSelectProperty(SelectProperty):
    """Return context this item is rendered in."""
    # https://minecraft.wiki/w/Items_model_definition#trim_material
    # Values: `none`, `thirdperson_lefthand`, `thirdperson_righthand`, `firstperson_lefthand`, `firstperson_righthand`, `head`, `gui`, `ground`, `fixed`

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:display_context"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DisplayContextSelectProperty":
        return cls()


@dataclass
class LocalTimeSelectProperty(SelectProperty):
    """Returns the current time formatted according to a given pattern. The value is updated every second.
    For full format documentation for locale, time zone and pattern, see ICU (International Components for Unicode) documentation."""
    # https://minecraft.wiki/w/Items_model_definition#local_time
    # Values: Any string.

    locale: str | None = "en_US"  # Value describing locale Default "" which means "root" locale (a set of defaults, including English names).
    # Optional. Locale to use for formatting. Default: "en_US".
    # cs_AU@numbers=thai;calendar=japanese: Czech language, Australian formatting, Thai numerals and Japanese calendar.
    time_zone: str | None = "UTC"  # describes format to be used for time formatting.
    # Examples: Europe/Stockholm, GMT+0:45
    pattern: str | None = None  # Optional. Describing time. If not present, defaults to timezone set on client.
    # yyyy-MM-dd: 4-digit year number, then 2-digit month number, then 2-digit day of month number, all zero-padded if needed, separated by -.
    # HH:mm:ss: current time (hours, minutes, seconds), 24-hour cycle, all zero-padded to 2 digits of needed, separated by :.

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {
            "property": "minecraft:local_time"
        } | ({
            "locale": self.locale,
        } if self.locale else {}) | ({
            "time_zone": self.time_zone,
        } if self.time_zone else {}) | ({
            "pattern": self.pattern,
        } if self.pattern else {})

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LocalTimeSelectProperty":
        return cls(
            data.get("locale", "en_US"),
            data.get("time_zone", "UTC"),
            data.get("pattern", None),
        )


class ContextDimensionSelectProperty(SelectProperty):
    """Return the ID of the dimension in context, if any."""
    # https://minecraft.wiki/w/Items_model_definition#context_dimension
    # Values: Namespaced dimension ID.

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:context_dimension"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ContextDimensionSelectProperty":
        return cls()


class ContextEntityTypeSelectProperty(SelectProperty):
    """Return the holding entity type, if present."""
    # https://minecraft.wiki/w/Items_model_definition#context_entity_type
    # Values: Namespaced entity type ID.

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:context_entity_type"}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ContextEntityTypeSelectProperty":
        return cls()


@dataclass
class CustomModelDataSelectProperty(SelectProperty):
    """Return value from strings list in minecraft:custom_model_data component."""
    # https://minecraft.wiki/w/Items_model_definition#custom_model_data_3
    # Values: Any string.
    index: int = 0

    def to_dict(self, pack_namespace: str) -> dict[str, str | int]:
        return {"property": "minecraft:custom_model_data", "index": self.index}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CustomModelDataSelectProperty":
        return cls(
            data["index"]
        )


@dataclass
class ComponentSelectProperty(SelectProperty):
    """Return value from a component. If the selected value comes from a registry and the current datapacks does not provide it,
    the entry will be silently ignored."""
    # https://minecraft.wiki/w/Items_model_definition#component_2
    # Values: Depends on the target component type.
    component: str  # Namespaced ID of the component type.

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {"property": "minecraft:component", "component": self.component}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ComponentSelectProperty":
        return cls(
            data["component"]
        )


SELECT_PROPERTY_NAME_TO_CLASSES: dict[str, type[SelectProperty]] = {
    "minecraft:main_hand": MainHandSelectProperty,
    "minecraft:charge_type": ChargeTypeSelectProperty,
    "minecraft:trim_material": TrimMaterialSelectProperty,
    "minecraft:block_state": BlockStateSelectProperty,
    "minecraft:display_context": DisplayContextSelectProperty,
    "minecraft:local_time": LocalTimeSelectProperty,
    "minecraft:context_dimension": ContextDimensionSelectProperty,
    "minecraft:context_entity_type": ContextEntityTypeSelectProperty,
    "minecraft:custom_model_data": CustomModelDataSelectProperty,
    "minecraft:component": ComponentSelectProperty,
}

# endregion
# ================================================================================================
# region: RANGE DISPATCH


@dataclass
class RangeDispatchItemModel(ItemModel):
    """Render an item model based on numeric property. Will select last entry with threshold less or equal to property value."""
    # https://minecraft.wiki/w/Items_model_definition#range_dispatch
    property_to_satisfy: "RangeDispatchPropertyType"
    scale: float = 1.0  # Factor to multiply property value with.
    entries: dict[int | float, "str | ItemModel"] = field(default_factory=dict)  # A mapping of threshold to item model name.
    fallback_model: "str | ItemModel | None" = None  # The Item model object if no valid entry was found. Optional, but will render a "missing" error model instead.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "model": {
                "type": "minecraft:range_dispatch",
                **self.property_to_satisfy.to_dict(pack_namespace),
                "scale": self.scale,
                "entries": [
                    {"threshold": threshold, "model": (model.to_dict(pack_namespace)["model"] if isinstance(model, ItemModel) else {"type": "minecraft:model", "model": model})}
                    for threshold, model in self.entries.items()
                ],
            } | (
                {
                    "fallback": (self.fallback_model.to_dict(pack_namespace)["model"] if isinstance(self.fallback_model, ItemModel) else {
                        "type": "minecraft:model",
                        "model": self.fallback_model,
                    })
                } if self.fallback_model else {}
            )
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RangeDispatchItemModel":
        return cls(
            RangeDispatchPropertyType.from_dict(data["model"]),
            data["model"].get("scale", 1.0),
            entries={entry["threshold"]: ItemModel.from_dict(entry["model"]) for entry in data["model"]["entries"]},
            fallback_model=ItemModel.from_dict(data["fallback"]) if data.get("fallback") else None,
        )


class RangeDispatchPropertyType:
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RangeDispatchPropertyType":
        cls_ = RANGE_DISPATCH_PROPERTY_NAME_TO_CLASSES[data["property"]]
        return cls_.from_dict(data)


@dataclass
class BundleFullnessRangeDispatchProperty(RangeDispatchPropertyType):
    """Return the fullness of the bundle."""
    # Return weight of minecraft:bundle_contents component or 0 if not present.
    # Values: 0-64 (Maybe?)

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {
            "property": "minecraft:bundle/fullness",
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BundleFullnessRangeDispatchProperty":
        return cls()


@dataclass
class CompassRangeDispatchProperty(RangeDispatchPropertyType):
    """Return an angle, scaled from 0.0 to 1.0 in x-z plane between holder position and target.
    If target is not valid (not present, in other dimension or too close to holder position) random value will be returned.
    Target can be spawn, lodestone, recovery or none.
    If wobble is true, value will oscillate for some time around target before settling.
    Spawn: points at world spawn.
    Lodestone: points at location stored in minecraft:lodestone_tracker component.
    Recovery: points at last player death location.
    None: always return an invalid target."""
    # Values: 0.0-1.0

    target: Literal["spawn", "lodestone", "recovery", "none"] = "none"
    wobble: bool = True  # If True, value will oscillate for some time around target before settling.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "property": "minecraft:compass",
            "target": self.target,
            "wobble": self.wobble,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CompassRangeDispatchProperty":
        return cls(
            data["target"],
            data.get("wobble", True),
        )


@dataclass
class CooldownRangeDispatchProperty(RangeDispatchPropertyType):
    """Return remaining cooldown for item, scaled between 0.0 to 1.0."""
    # Values: 0.0-1.0

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {
            "property": "minecraft:cooldown",
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CooldownRangeDispatchProperty":
        return cls()


@dataclass
class CountRangeDispatchProperty(RangeDispatchPropertyType):
    """Return stack size."""
    # Values: 0-64 | 0-1/0-16 (things that stack less) | 0.0-1.0 (if normalized)
    normalize: bool = True  # If True, return count divided by minecraft:max_stack_size component, clamped to 0.0 to 1.0. If False, return count clamped to 0 to minecraft:max_stack_size.

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {
            "property": "minecraft:count",
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CountRangeDispatchProperty":
        return cls()


@dataclass
class CrossbowPullRangeDispatchProperty(RangeDispatchPropertyType):
    """Return crossbow pull."""
    # Values: Unknown

    def to_dict(self, pack_namespace: str) -> dict[str, str]:
        return {
            "property": "minecraft:crossbow/pull",
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CrossbowPullRangeDispatchProperty":
        return cls()


@dataclass
class DamageRangeDispatchProperty(RangeDispatchPropertyType):
    """Return damage."""
    # Values: 0 | 0-max damage | 0-1.0 (if normalized)
    normalize: bool = True

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "property": "minecraft:damage",
            "normalize": self.normalize,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DamageRangeDispatchProperty":
        return cls(data.get("normalize", True))


@dataclass
class TimeRangeDispatchProperty(RangeDispatchPropertyType):
    """Return value of a in-game time, scaled between 0.0 to 1.0."""
    # Values: 0.0-1.0
    source: Literal["daytime", "moon_phase", "random"] = "daytime"
    wobble: bool = True  # If True, value will oscillate for some time around target before settling

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "property": "minecraft:time",
            "source": self.source,
            "wobble": self.wobble,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TimeRangeDispatchProperty":
        return cls(
            data["source"],
            data.get("wobble", True),
        )


@dataclass
class UseCycleRangeDispatchProperty(RangeDispatchPropertyType):
    """Return remaining use ticks modulo period."""
    # Values: 0.0+ (0.0-use time max)

    period: float = 1.0  # Must be positive.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "property": "minecraft:use_cycle",
            "period": self.period,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UseCycleRangeDispatchProperty":
        return cls(
            data.get("period", 1.0),
        )


@dataclass
class CustomModelDataRangeDispatchProperty(RangeDispatchPropertyType):
    """Return value from floats list in minecraft:custom_model_data component."""
    # Values: 0 | 0.0+

    index: int = 0  # Index for field in floats

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "property": "minecraft:custom_model_data",
            "index": self.index,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CustomModelDataRangeDispatchProperty":
        return cls(
            data.get("index", 0),
        )


RANGE_DISPATCH_PROPERTY_NAME_TO_CLASSES: dict[str, type[RangeDispatchPropertyType]] = {
    "minecraft:bundle/fullness": BundleFullnessRangeDispatchProperty,
    "minecraft:compass": CompassRangeDispatchProperty,
    "minecraft:cooldown": CooldownRangeDispatchProperty,
    "minecraft:count": CountRangeDispatchProperty,
    "minecraft:crossbow/pull": CrossbowPullRangeDispatchProperty,
    "minecraft:damage": DamageRangeDispatchProperty,
    "minecraft:time": TimeRangeDispatchProperty,
    "minecraft:use_cycle": UseCycleRangeDispatchProperty,
    "minecraft:custom_model_data": CustomModelDataRangeDispatchProperty,
}

# endregion
# ================================================================================================
# region: EMPTY


class EmptyItemModel(ItemModel):
    """Does not render anything."""
    # https://minecraft.wiki/w/Items_model_definition#empty
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {"model": {"type": "minecraft:empty"}}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EmptyItemModel":
        return cls()


# endregion
# ================================================================================================
# region: BUNDLE SELECTED ITEM


class BundleSelectedItemModel(ItemModel):
    """Render the selected stack in minecraft:bundle_contents component, if present, otherwise does nothing."""
    # https://minecraft.wiki/w/Items_model_definition#bundle/selected_item
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {"model": {"type": "minecraft:bundle/selected_item"}}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BundleSelectedItemModel":
        return cls()


# endregion
# ================================================================================================
# region: SPECIAL


@dataclass
class SpecialItemModel(ItemModel):
    """Render a special model."""
    # https://minecraft.wiki/w/Items_model_definition#special_model_types
    model_type: "SpecialItemModelType"
    base: str  # Namespaced ID of model in models directory, to providing transformations, particle texture and GUI light.  # TODO: Support CustomModel here?

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "model": {
                "type": "minecraft:special",
                "model": self.model_type.to_dict(pack_namespace),
                "base": self.base,
            }
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SpecialItemModel":
        return cls(
            model_type=SpecialItemModelType.from_dict(data["model"]["model"]),
            base=data["model"]["base"],
        )


@dataclass
class SpecialItemModelType:
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SpecialItemModelType":
        cls_ = SPECIAL_ITEM_MODEL_TYPE_NAME_TO_CLASSES[data["type"]]
        return cls_.from_dict(data)


@dataclass
class BannerSpecialItemModelType(SpecialItemModelType):
    """Render a banner with patterns from minecraft:banner_patterns component."""
    # https://minecraft.wiki/w/Items_model_definition#banner
    color: "MinecraftColor"  # Color of the banner base, one of 16 predefined colors.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:banner",
            "color": self.color.name,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BannerSpecialItemModelType":
        return cls(
            data["color"],
        )


@dataclass
class BedSpecialItemModelType(SpecialItemModelType):
    """Render a whole bed."""
    # https://minecraft.wiki/w/Items_model_definition#bed
    texture: str  # Namespaced ID for the texture in the beds texture atlas without the .png suffix. By default this includes textures in textures/entity/bed/, without the prefix.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:bed",
            "texture": self.texture,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BedSpecialItemModelType":
        return cls(
            data["texture"],
        )


@dataclass
class ChestSpecialItemModelType(SpecialItemModelType):
    """Render a single chest."""
    # https://minecraft.wiki/w/Items_model_definition#chest
    texture: str  # Namespaced ID for the texture in the chests texture atlas without the .png suffix. By default this includes textures in textures/entity/chest/, without the prefix.
    openness: float = 0.0  # Render the chest in the specified open state, between 0.0 (fully closed) to 1.0 (fully open). Default: 0.0.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:chest",
            "texture": self.texture,
            "openness": self.openness,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ChestSpecialItemModelType":
        return cls(
            data["texture"],
            data.get("openness", 0.0),
        )


@dataclass
class ConduitSpecialItemModelType(SpecialItemModelType):
    """Render conduit."""
    # https://minecraft.wiki/w/Items_model_definition#conduit
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:conduit",
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConduitSpecialItemModelType":
        return cls()


@dataclass
class DecoratedPotSpecialItemModelType(SpecialItemModelType):
    """Render a decorated pot. Uses values from minecraft:pot_decorations component."""
    # https://minecraft.wiki/w/Items_model_definition#decorated_pot
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:decorated_pot",
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DecoratedPotSpecialItemModelType":
        return cls()


@dataclass
class HeadSpecialItemModelType(SpecialItemModelType):
    """Render a head. Uses profile from minecraft:profile component when applicable."""
    # https://minecraft.wiki/w/Items_model_definition#head
    kind: Literal["skeleton", "wither_skeleton", "player", "zombie", "creeper", "piglin", "dragon"]
    texture: str | None = None  # Optional. Namespaced ID for the texture, without textures/entity/ prefix and .png suffix.
    # If absent, default texture will be used, depending on kind field. Additionally, if present, minecraft:profile component is ignored.
    animation: float = 0.0  # Optional. Controlling head animation if available for this kind of head (like Piglin ears or Ender Dragon jaw). Default: 0.0.
    # The dragon animation is 10 units long. Mouth fully closed at -2.5 and fully open at 2.5
    # The piglin ears wiggle out of sync. The left ear period is 8.3333 and right ear period is 10.0

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "type": "minecraft:head",
            "kind": self.kind,
            "texture": self.texture,
            "animation": self.animation,
        })

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HeadSpecialItemModelType":
        return cls(
            data["kind"],
            data.get("texture"),
            data.get("animation", 0.0),
        )


@dataclass
class ShieldSpecialItemModelType(SpecialItemModelType):
    """Render a shield. Uses patterns from minecraft:banner_patterns component and color from minecraft:base_color component."""
    # https://minecraft.wiki/w/Items_model_definition#shield
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:shield",
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ShieldSpecialItemModelType":
        return cls()


@dataclass
class ShulkerBoxSpecialItemModelType(SpecialItemModelType):
    """Render a shulker box."""
    # https://minecraft.wiki/w/Items_model_definition#shulker_box
    texture: str  # Namespaced ID for the texture in the shulker boxes texture atlas without the .png suffix. By default this includes textures in textures/entity/shulker/, without the prefix.
    openness: float = 0.0  # Render the shulker box in the specified open state, between 0.0 (fully closed) to 1.0 (fully open). Default: 0.0.
    orientation: Literal["up", "down", "north", "south", "west", "east"] = "up"  # Orientation for rendering. Default: up.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:shulker_box",
            "texture": self.texture,
            "openness": self.openness,
            "orientation": self.orientation,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ShulkerBoxSpecialItemModelType":
        return cls(
            data["texture"],
            data.get("openness", 0.0),
            data.get("orientation", "up"),
        )


@dataclass
class StandingSignSpecialItemModelType(SpecialItemModelType):
    """Render a standing sign."""
    # https://minecraft.wiki/w/Items_model_definition#standing_sign
    wood_type: Literal["oak", "spruce", "birch", "acacia", "cherry", "jungle", "dark_oak", "pale_oak", "mangrove", "bamboo", "crimson", "warped"] = "oak"
    texture: str | None = None  # Namespaced ID for the texture in the signs texture atlas without the .png suffix. By default this includes textures in textures/entity/signs/, without the prefix. If present, wood_type field is ignored.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:standing_sign",
            "wood_type": self.wood_type,
            "texture": self.texture,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StandingSignSpecialItemModelType":
        return cls(
            data["wood_type"],
            data.get("texture"),
        )


@dataclass
class HangingSignSpecialItemModelType(SpecialItemModelType):
    """Render a hanging sign."""
    # https://minecraft.wiki/w/Items_model_definition#hanging_sign
    wood_type: Literal["oak", "spruce", "birch", "acacia", "cherry", "jungle", "dark_oak", "pale_oak", "mangrove", "bamboo", "crimson", "warped"] = "oak"
    texture: str | None = None  # Namespaced ID for the texture in the signs texture atlas without the .png suffix. By default this includes textures in textures/entity/signs/, without the prefix. If present, wood_type field is ignored.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:hanging_sign",
            "wood_type": self.wood_type,
            "texture": self.texture,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HangingSignSpecialItemModelType":
        return cls(
            data["wood_type"],
            data.get("texture"),
        )


@dataclass
class TridentSpecialItemModelType(SpecialItemModelType):
    """Render a trident."""
    # https://minecraft.wiki/w/Items_model_definition#trident
    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "minecraft:trident",
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TridentSpecialItemModelType":
        return cls()


SPECIAL_ITEM_MODEL_TYPE_NAME_TO_CLASSES: dict[str, type["SpecialItemModelType"]] = {
    "minecraft:banner": BannerSpecialItemModelType,
    "minecraft:bed": BedSpecialItemModelType,
    "minecraft:chest": ChestSpecialItemModelType,
    "minecraft:conduit": ConduitSpecialItemModelType,
    "minecraft:decorated_pot": DecoratedPotSpecialItemModelType,
    "minecraft:head": HeadSpecialItemModelType,
    "minecraft:shield": ShieldSpecialItemModelType,
    "minecraft:shulker_box": ShulkerBoxSpecialItemModelType,
    "minecraft:standing_sign": StandingSignSpecialItemModelType,
    "minecraft:hanging_sign": HangingSignSpecialItemModelType,
    "minecraft:trident": TridentSpecialItemModelType,
}

# endregion
# ================================================================================================

ITEM_MODEL_NAME_TO_CLASSES: dict[str, type["ItemModel"]] = {
    "minecraft:model": ModelItemModel,
    "minecraft:composite": CompositeItemModel,
    "minecraft:condition": ConditionalItemModel,
    "minecraft:select": SelectItemModel,
    "minecraft:range_dispatch": RangeDispatchItemModel,
    "minecraft:empty": EmptyItemModel,
    "minecraft:bundle/selected_item": BundleSelectedItemModel,
    "minecraft:special": SpecialItemModel,
}
