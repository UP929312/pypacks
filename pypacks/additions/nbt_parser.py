# This is a simple NBT parser that can read NBT files and return the data as a Python dictionary.
import struct
import gzip
from io import BufferedReader, BytesIO
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Structure:
    size: tuple[int, int, int]
    blocks: list["Block"]
    palette: list[dict[str, Any]] = field(repr=False)  # The palette is a list of dictionaries, each containing the block name and properties.
    entities: list[dict[str, Any]] = field(repr=False)
    data_version: int = field(repr=False)

    @classmethod
    def from_nbt(cls, nbt: dict[str, Any]) -> "Structure":
        # Blocks  # [{'pos': [0, 1, 1], 'state': 0}, {'pos': [0, 0, 1], 'state': 1}, {'pos': [0, 0, 2], 'state': 1}, {'pos': [0, 1, 2], 'state': 1}, {'pos': [0, 3, 0], 'state': 1}, {'pos': [0, 3, 1], 'state': 1}, {'pos': [0, 3, 2], 'state': 1}, {'nbt': {'mode': 'start', 'powered': 0, 'id': 'minecraft:test_block', 'message': ''}, 'pos': [0, 0, 0], 'state': 2}, {'nbt': {'crafting_ticks_remaining': 0, 'triggered': 0, 'disabled_slots': [], 'Items': [{'count': 1, 'Slot': 0, 'id': 'minecraft:iron_ingot'}, {'count': 1, 'Slot': 1, 'id': 'minecraft:iron_ingot'}, {'count': 1, 'Slot': 2, 'id': 'minecraft:iron_ingot'}, {'count': 1, 'Slot': 3, 'id': 'minecraft:iron_ingot'}, {'count': 1, 'Slot': 4, 'id': 'minecraft:iron_ingot'}, {'count': 1, 'Slot': 5, 'id': 'minecraft:iron_ingot'}, {'count': 1, 'Slot': 6, 'id': 'minecraft:iron_ingot'}, {'count': 1, 'Slot': 7, 'id': 'minecraft:iron_ingot'}, {'count': 1, 'Slot': 8, 'id': 'minecraft:iron_ingot'}], 'id': 'minecraft:crafter'}, 'pos': [0, 1, 0], 'state': 3}, {'nbt': {'Items': [], 'id': 'minecraft:chest'}, 'pos': [0, 2, 0], 'state': 4}, {'nbt': {'id': 'minecraft:comparator', 'OutputSignal': 0}, 'pos': [0, 2, 1], 'state': 5}, {'nbt': {'mode': 'accept', 'powered': 0, 'id': 'minecraft:test_block', 'message': ''}, 'pos': [0, 2, 2], 'state': 6}]
        nbt = nbt['']
        palette = nbt["palette"]  # [{'Name': 'minecraft:stone_bricks'}, {'Name': 'minecraft:air'}, {'Properties': {'mode': 'start'}, 'Name': 'minecraft:test_block'}, {'Properties': {'orientation': 'up_west', 'triggered': 'false', 'crafting': 'false'}, 'Name': 'minecraft:crafter'}, {'Properties': {'waterlogged': 'false', 'facing': 'east', 'type': 'single'}, 'Name': 'minecraft:chest'}, {'Properties': {'mode': 'compare', 'powered': 'false', 'facing': 'north'}, 'Name': 'minecraft:comparator'}, {'Properties': {'mode': 'accept'}, 'Name': 'minecraft:test_block'}]
        size = tuple(nbt['size'])
        blocks = nbt['blocks']
        entities = nbt['entities']
        data_version = nbt['DataVersion']
        block_instances = [Block(block.get("Name", "air"), tuple(block["pos"]), block.get("nbt", {}), block.get("properties", {})) for block in blocks]
        return cls(size, block_instances, [], entities, data_version)  # palette


@dataclass
class Block:
    block_type: str
    block_pos: tuple[int, int, int]
    block_nbt: dict[str, Any]
    block_properties: dict[str, Any]


class NBTParser:
    TAG_END = 0
    TAG_BYTE = 1
    TAG_SHORT = 2
    TAG_INT = 3
    TAG_LONG = 4
    TAG_FLOAT = 5
    TAG_DOUBLE = 6
    TAG_BYTE_ARRAY = 7
    TAG_STRING = 8
    TAG_LIST = 9
    TAG_COMPOUND = 10
    TAG_INT_ARRAY = 11
    TAG_LONG_ARRAY = 12

    def __init__(self, data: str | bytes) -> None:
        self.stream = BufferedReader(BytesIO(data))  # type: ignore[arg-type]
        self.output = self.read()

    def read(self) -> Any:
        tag_type = self.read_byte()
        if tag_type == self.TAG_END:
            return None
        return {self.read_string(): self.read_tag(tag_type)}

    def read_tag(self, tag_type: int) -> Any:
        mapping = {
            self.TAG_BYTE: lambda: self.read_byte(),
            self.TAG_SHORT: lambda: self.read_short(),
            self.TAG_INT: lambda: self.read_int(),
            self.TAG_LONG: lambda: self.read_long(),
            self.TAG_FLOAT: lambda: struct.unpack('>f', self.stream.read(4))[0],
            self.TAG_DOUBLE: lambda: struct.unpack('>d', self.stream.read(8))[0],
            self.TAG_BYTE_ARRAY: lambda: self.read_byte_array(),
            self.TAG_STRING: lambda: self.read_string(),
            self.TAG_LIST: lambda: self.read_list(),
            self.TAG_COMPOUND: lambda: self.read_compound(),
            self.TAG_INT_ARRAY: lambda: self.read_int_array(),
            self.TAG_LONG_ARRAY: lambda: self.read_long_array(),
        }
        if tag_type not in mapping:
            raise ValueError(f"Unknown tag type {tag_type}")
        else:
            return mapping[tag_type]()

    def read_byte(self) -> int:  # Refed multiple times
        return struct.unpack('>b', self.stream.read(1))[0]  # type: ignore[no-any-return]

    def read_short(self) -> int:  # Refed multiple times
        return struct.unpack('>h', self.stream.read(2))[0]  # type: ignore[no-any-return]

    def read_int(self) -> int:  # Refed multiple times
        return struct.unpack('>i', self.stream.read(4))[0]  # type: ignore[no-any-return]

    def read_long(self) -> float:  # Refed multiple times
        return struct.unpack('>q', self.stream.read(8))[0]  # type: ignore[no-any-return]

    def read_byte_array(self) -> list[int]:
        length = self.read_int()
        return list(self.stream.read(length))

    def read_string(self) -> str:
        length = self.read_short()
        return self.stream.read(length).decode('utf-8')

    def read_list(self) -> list[Any]:
        tag_type = self.read_byte()
        length = self.read_int()
        return [self.read_tag(tag_type) for _ in range(length)]

    def read_compound(self) -> dict[Any, Any]:
        compound = {}
        while True:
            tag_type = self.read_byte()
            if tag_type == self.TAG_END:
                break
            name = self.read_string()
            compound[name] = self.read_tag(tag_type)
        return compound

    def read_int_array(self) -> list[int]:
        length = self.read_int()
        return [self.read_int() for _ in range(length)]

    def read_long_array(self) -> list[float]:
        length = self.read_int()
        return [self.read_long() for _ in range(length)]

    @staticmethod
    def from_file(filename: str) -> "NBTParser":
        with gzip.open(filename, 'rb') as f:
            return NBTParser(f.read())


# Example usage:
data = NBTParser.from_file(r"C:\Users\Ben\Desktop\pypacks\examples\development\structures\iron_block_crafting_recipe.nbt")
# rint(data.output)
structure = Structure.from_nbt(data.output)
# rint(structure)
