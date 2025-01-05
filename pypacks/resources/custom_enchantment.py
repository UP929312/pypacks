import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Any, TYPE_CHECKING

from pypacks.utils import recursively_remove_nones_from_data

if TYPE_CHECKING:
    from pypacks.datapack import Datapack
    from pypacks.resources.custom_item import CustomItem


@dataclass
class EnchantEffect:
    effect: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "effect": self.effect,
        }

@dataclass
class CustomEnchantment:
    # https://minecraft.wiki/w/Enchantment_definition
    internal_name: str
    description: dict[str, Any]  # A JSON text component - The description of the enchantment.
    exclusive_set: str | list[str] = field(repr=False, default_factory=list)  # One or more enchantments (an ID, a #tag, or an array containing IDs) - Enchantments that are incompatible with this enchantment
    supported_items: str | list[str] = field(repr=False, default_factory=list)  # One or more items (an ID, a #tag, or an array containing IDs) - Items on which this enchantment can be applied using an anvil or using the /enchant command.
    primary_items: str | list[str] = field(repr=False, default_factory=list)  # One or more items (an ID, a #tag, or an array containing IDs) - `MUST be a subset of supported_items` - Items for which this enchantment appears in an enchanting table. If empty, defaults to being the same as supported_items.
    weight: int = field(repr=False, default=1024)  # 1-1024 | Controls the probability of this enchantment when enchanting. The probability is determined weight/total weight * 100%, where total_weight is the sum of the weights of all available enchantments.
    max_level: int = field(repr=False, default=1)  # 1-255 | The maximum level of this enchantment.
    min_cost_base: int = field(repr=False, default=1)  # 1-100 | The minimum base cost of this enchantment in levels. The base cost range will be modified before use.
    per_level_increase_min: int = field(repr=False, default=1)  # 0-100 | The amount of levels added to the minimum for each level above level I.
    max_cost_base: int = field(repr=False, default=1)  # 1-100 | The maximum base cost of this enchantment in levels. The base cost range will be modified before use.
    per_level_increase_max: int = field(repr=False, default=1)  # 0-100 | The amount of levels added to the maximum for each level above level I.
    anvil_cost: int = field(repr=False, default=1)  # 0-100 |  The base cost when applying this enchantment to another item using an anvil. Halved when adding using a book, multiplied by the level of the enchantment.
    slots: Literal["any", "hand", "mainhand", "offhand", "armor", "feet", "legs", "chest", "head", "body"] = "any"  # List of equipment slots that this enchantment works in.
    effects: list[EnchantEffect] = field(repr=False, default_factory=list)  #  Effect components - Controls the effect of the enchantment.

    datapack_subdirectory_name: str = field(init=False, repr=False, default="enchantment")

    def __post_init__(self) -> None:
        assert 0 < self.weight <= 1024, "Weight must be between 1 and 1024"
        assert 0 < self.max_level <= 255, "Max level must be between 1 and 255"

    def to_dict(self, datapack_namespace: str) -> dict[str, Any]:
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "description": self.description,
            "exclusive_set": self.exclusive_set,
            "supported_items": self.supported_items,
            "primary_items": self.primary_items,
            "weight": self.weight,
            "max_level": self.max_level,
            "min_cost": {
                "base": self.min_cost_base,
                "per_level_above_first": self.per_level_increase_min,
            },
            "max_cost": {
                "base": self.max_cost_base,
                "per_level_above_first": self.per_level_increase_max,
            },
            "anvil_cost": self.anvil_cost,
            "slots": self.slots,
            "effects": [effect.to_dict() for effect in self.effects],
        })

    def create_datapack_files(self, datapack: "Datapack") -> None:
        with open(Path(datapack.datapack_output_path)/"data"/datapack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(datapack.namespace), file, indent=4)
