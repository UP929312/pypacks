from dataclasses import dataclass
from typing import Literal, Any


def check_color(color: tuple[float, float, float]) -> None:
    assert 0 <= color[0] <= 1.0, "Red must be between 0 and 1"
    assert 0 <= color[1] <= 1.0, "Green must be between 0 and 1"
    assert 0 <= color[2] <= 1.0, "Blue must be between 0 and 1"


@dataclass
class ConstantTint:
    """Return a constant RGB color."""
    color: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:constant",
            "value": self.color,
        }


@dataclass
class DyeTint:
    """Return value from minecraft:dyed_color component or default if not present"""
    default: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def to_dict(self) -> dict[str, Any]:
        check_color(self.default)
        return {
            "type": "minecraft:dye",
            "default": self.default,
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
            "default": self.default,
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
            "default": self.default,
        }


@dataclass
class MapColor:
    """Return value from minecraft:map_color component or default color if component is not present."""
    default: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def to_dict(self) -> dict[str, Any]:
        check_color(self.default)
        return {
            "type": "minecraft:map_color",
            "default": self.default,
        }


@dataclass
class Team:
    """Returns the team color of context entity, if any. Else, when there is no context entity, entity is not in a team or team has no color, return default."""
    default: tuple[float, float, float] = (1.0, 1.0, 1.0)

    def to_dict(self) -> dict[str, Any]:
        check_color(self.default)
        return {
            "type": "minecraft:team",
            "default": self.default,
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
            "default": self.default,
        }


@dataclass
class Composite:
    """Render multiple sub-models in the same space."""
    models: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:composite",
            "models": self.models,
        }

# ================================================================================================


@dataclass
class Conditional:
    property_to_satisfy: "ConditionalBooleanProperty"
    true_model: str
    false_model: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:conditional",
            "on_true": self.true_model,
            "on_false": self.false_model,
        } | self.property_to_satisfy.to_dict()


class ConditionalBooleanProperty:
    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError


class UsingItem(ConditionalBooleanProperty):
    """Return true if player is currently using this item."""
    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:using_item"}


class Broken(ConditionalBooleanProperty):
    """Return true if the item is damageable and has only one use remaining before breaking."""
    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:broken"}


class Damaged(ConditionalBooleanProperty):
    """Return true if the item is damageable and has been used at least once."""
    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:damaged"}


@dataclass
class HasComponent(ConditionalBooleanProperty):
    """Return true if the given component is present on the item."""
    component: str  # Component name.
    ignore_default: bool = False   # Optional. If default component value should be handled as "no component". Default: false.

    def to_dict(self) -> dict[str, str | bool]:
        return {"property": "minecraft:has_component", "component": self.component, "ignore_default": self.ignore_default}


class FishingRodCast(ConditionalBooleanProperty):
    """Return true if there is a fishing bobber attached to currently used fishing rod."""
    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:fishing_rod/cast"}


class BundleHasSelectedItem(ConditionalBooleanProperty):
    """Return true if bundle is "open", i.e. it has selected item visible in GUI."""
    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:bundle_has_selected_item"}


class Selected(ConditionalBooleanProperty):
    """Return true if item is selected on a hotbar."""
    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:selected"}


class Carried(ConditionalBooleanProperty):
    """Return true if item is carried between slots in GUI (in the cursor)"""
    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:carried"}


class ExtendedView(ConditionalBooleanProperty):
    """Return true if player has requested extended details by holding shift key down.
    Only works when item is displayed in UI.
    Note: not a keybind, can't be rebound."""
    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:extended_view"}


@dataclass
class KeyDown(ConditionalBooleanProperty):
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


class ViewEntity(ConditionalBooleanProperty):
    """When not spectating, return true if context entity is the local player entity, i.e. the one controlled by client.
    When spectating, return true if context entity is the spectated entity.
    If context entity is not present, will return false."""

    def to_dict(self) -> dict[str, str]:
        return {"property": "minecraft:view_entity"}


@dataclass
class CustomModelData:
    index: int = 0

    def to_dict(self) -> dict[str, str | int]:
        return {"property": "minecraft:custom_model_data", "index": self.index}


# ================================================================================================


SelectPropertyType = Literal[
    "minecraft:main_hand", "minecraft:charge_type", "minecraft:trim_material", "minecraft:block_state",
    "minecraft:display_context", "minecraft:local_time", "minecraft:context_dimension",
    "minecraft:context_entity_type", "minecraft:custom_model_data"
]


@dataclass
class Select:
    property_to_satisfy: "SelectPropertyType"
    cases: list["SelectCase"]
    fallback_model_name: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "minecraft:select",
            "property": self.property_to_satisfy,
            "cases": [case.to_dict() for case in self.cases],
        } | (
            {
                "fallback": {
                    "type": "minecraft:model",
                    "model": self.fallback_model_name,
                }
            } if self.fallback_model_name else {}
        )


@dataclass
class SelectCase:
    when: str | list[str]
    model_name: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "when": self.when,
            "model": {
                "type": "minecraft:model",
                "model": self.model_name,
            }
        }

# class SelectBooleanProperty:
#     def to_dict(self) -> dict:
#         raise NotImplementedError
