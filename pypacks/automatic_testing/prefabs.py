from dataclasses import dataclass

from pypacks.automatic_testing.testing_framework import Test
from pypacks.resources.custom_item import CustomItem

from pypacks.automatic_testing.testing_blocks import *


@dataclass
class FurnacePrefab:
    input_item: "str"
    expected_item: "str | CustomItem"

    def create_blocks(self) -> "Test":
        output_string = self.expected_item.internal_name if isinstance(self.expected_item, CustomItem) else self.expected_item
        return Test("Furnace Test", [  # type: ignore
            Air(), Hopper([self.input_item]),     Air(),
            Air(), Furnace(),                     Air(),  # fmt: skip
            Air(), ExpectedHopper(output_string), Air(),  # fmt: skip
        ])


@dataclass
class CrafterPrefab:
    name: str
    input_item: "str"
    expected_item: "str | CustomItem"
    input_count: int = 1
    expected_count: int = 1
    shape: list[int] = []

    def create_blocks(self) -> "Test":
        return Test("Custom Crafting Recipe Test", [  # type: ignore
            Air(), Hopper({self.input_item: self.expected_count}), Air(),
            Air(), AutoCrafter(self.shape),                        AddedRedstoneBlock(),  # fmt: skip
            Air(), ExpectedHopper(""),                             RemovedRedstoneBlock(),  # fmt: skip
        ])
