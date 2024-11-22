from typing import TypeVar


def items_formatter(items: list[str] | dict[str, int] | None, count_or_slot: str) -> str:
    if items is None:
        return ""
    if isinstance(items, dict):
        items_string = ", ".join([f'{{id:"{item}", {count_or_slot}:{count}}}' for item, count in items.items()])
    else:
        items_string = ", ".join([f'{{id:"{item}"}}' for item in items])
    return "{Items:[" + items_string + "]}"


class Air:
    def to_setblock_command(self, x: int, y: int, z: int) -> str:
        return f"setblock ~{x} ~{y} ~{z} minecraft:air"


class Hopper:
    def __init__(self, items: list[str] | dict[str, int] | None = None) -> None:
        self.items = items
    
    def to_setblock_command(self, x, y, z) -> str:
        return f"setblock ~{x} ~{y} ~{z} minecraft:hopper[]"+items_formatter(self.items, "count")


class Furnace:
    def to_setblock_command(self, x: int, y: int, z: int) -> str:
        # Slot 1 is the fuel slot, 0 is the ingredient slot, 2 is the result slot
        return f"setblock ~{x} ~{y} ~{z} minecraft:furnace[]"+items_formatter({"minecraft:coal": 1}, "Slot")


class ExpectedHopper(Hopper):
    """Acts like a regular hopper, but the test framework will wait a few seconds and verify it's item is what we expect"""
    def __init__(self, expected_item: str) -> None:
        super().__init__([])
        self.expected_item = expected_item
    
    def to_setblock_command(self, x, y, z) -> str:
        return f"setblock ~{x} ~{y} ~{z} minecraft:hopper[]"


class AutoCrafter:
    def __init__(self, slots_disabled: list[int] | None = None) -> None:
        self.slots_disabled = slots_disabled or []
    
    def to_setblock_command(self, x, y, z) -> str:
        disabled_slots_string = ("{disabled_slots:" + f"[I; {', '.join([str(x) for x in self.slots_disabled])}]" + "}") if self.slots_disabled else ""
        return f"setblock ~{x} ~{y} ~{z} minecraft:crafter[]{disabled_slots_string}"


class RemovedRedstoneBlock:
    def to_setblock_command(self, x, y, z) -> str:
        return f"setblock ~{x} ~{y} ~{z} minecraft:redstone_block"


class AddedRedstoneBlock:
    def to_setblock_command(self, x, y, z) -> str:
        return f"setblock ~{x} ~{y} ~{z} minecraft:redstone_block"


BlockType = TypeVar("BlockType", Air, Hopper, Furnace, ExpectedHopper, AutoCrafter, RemovedRedstoneBlock, AddedRedstoneBlock)
