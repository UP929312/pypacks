# This is a simple NBT parser that can read NBT files and return the data as a Python dictionary.
import struct
import gzip
from io import BufferedReader, BufferedWriter, BytesIO
from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


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
        # palette = nbt["palette"]  # [{'Name': 'minecraft:stone_bricks'}, {'Name': 'minecraft:air'}, {'Properties': {'mode': 'start'}, 'Name': 'minecraft:test_block'}, {'Properties': {'orientation': 'up_west', 'triggered': 'false', 'crafting': 'false'}, 'Name': 'minecraft:crafter'}, {'Properties': {'waterlogged': 'false', 'facing': 'east', 'type': 'single'}, 'Name': 'minecraft:chest'}, {'Properties': {'mode': 'compare', 'powered': 'false', 'facing': 'north'}, 'Name': 'minecraft:comparator'}, {'Properties': {'mode': 'accept'}, 'Name': 'minecraft:test_block'}]
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

        self.output_stream = BytesIO()
        self.writer = BufferedWriter(self.output_stream)  # type: ignore

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
        return mapping[tag_type]()  # type: ignore[no-untyped-call]

    # =========================

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

    # =========================

    def write_byte(self, value: int) -> None:
        self.writer.write(struct.pack(">b", value))

    def write_short(self, value: int) -> None:
        self.writer.write(struct.pack(">h", value))

    def write_int(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"write_int expected an int, but got {value.__class__.__name__}: {value}")
        if not (-2_147_483_648 <= value <= 2_147_483_647):  # Check valid int range
            raise ValueError(f"write_int: value {value} is out of range for a 4-byte integer")
        # # rint(f"Writing int: {value}")
        self.writer.write(struct.pack(">i", value))

    def write_long(self, value: int) -> None:
        self.writer.write(struct.pack(">q", value))

    def write_float(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError(f"write_float expected a float, but got {value.__class__.__name__}: {value}")
        if not (-1.7976931348623157e+308 <= value <= 1.7976931348623157e+308):  # Check valid float range
            raise ValueError(f"write_float: value {value} is out of range for a 8-byte float")
        # rint(f"Writing float: {value}, type: {value.__class__.__name__}")
        self.writer.write(struct.pack(">f", value))

    def write_double(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError(f"write_double expected a float, but got {value.__class__.__name__}: {value}")
        if not (-1.7976931348623157e+308 <= value <= 1.7976931348623157e+308):  # Check valid double range
            raise ValueError(f"write_double: value {value} is out of range for a 8-byte double")
        # rint(f"Writing double: {value}, type: {value.__class__.__name__}")
        self.writer.write(struct.pack(">d", value))

    def write_byte_array(self, value: list[int]) -> None:
        self.write_int(len(value))
        self.writer.write(bytes(value))

    def write_string(self, value: str) -> None:
        encoded = value.encode("utf-8")
        self.write_short(len(encoded))
        self.writer.write(encoded)

    def write_list(self, value: list[Any]) -> None:
        tag_type = self.get_tag_type(value[0]) if value else self.TAG_END
        self.write_byte(tag_type)
        self.write_int(len(value))
        for item in value:
            self.write_tag(tag_type, item)

    def write_compound(self, value: dict[str, Any]) -> None:
        for key, val in value.items():
            tag_type = self.get_tag_type(val)
            self.write_byte(tag_type)
            self.write_string(key)
            self.write_tag(tag_type, val)
        self.write_byte(self.TAG_END)  # End of compound

    def write_int_array(self, value: list[int]) -> None:
        self.write_int(len(value))
        if not all(isinstance(i, int) for i in value):
            raise TypeError(f"write_int_array expected a list of ints, but got {value.__class__.__name__}: {value}")
        for item in value:
            self.write_int(item)

    def write_long_array(self, value: list[int]) -> None:
        self.write_int(len(value))
        if not all(isinstance(i, int) for i in value):
            raise TypeError(f"write_long_array expected a list of ints, but got {value.__class__.__name__}: {value}")
        for item in value:
            self.write_long(item)

    # =========================

    @staticmethod
    def get_tag_type(value: Any) -> int:
        """Infer the NBT tag type from a Python object."""
        if isinstance(value, bool):
            return NBTParser.TAG_BYTE
        if isinstance(value, int):
            return NBTParser.TAG_INT if -2_147_483_648 <= value <= 2_147_483_647 else NBTParser.TAG_LONG
        if isinstance(value, float):
            return NBTParser.TAG_DOUBLE
        if isinstance(value, str):
            return NBTParser.TAG_STRING
        if isinstance(value, bytes):
            return NBTParser.TAG_BYTE_ARRAY
        if isinstance(value, dict):
            return NBTParser.TAG_COMPOUND

        if isinstance(value, list):
            if not value:
                return NBTParser.TAG_LIST  # Empty lists default to TAG_LIST
            first_item = value[0]

            if isinstance(first_item, dict):
                return NBTParser.TAG_LIST  # List of compounds
            if isinstance(first_item, int):
                return NBTParser.TAG_INT_ARRAY  # List of ints
            if isinstance(first_item, float):
                return NBTParser.TAG_LIST  # List of floats
            if isinstance(first_item, str):
                return NBTParser.TAG_LIST  # List of strings (not int array!)

            # Default to list if mixed types
            return NBTParser.TAG_LIST

        raise ValueError(f"Unknown type {type(value)} for value {value}")

    def write_tag(self, tag_type: int, value: Any) -> None:
        # rint(f"Writing tag: {tag_type}, Value: {value} ({type(value).__name__})")
        tag_writers = {
            self.TAG_BYTE: self.write_byte,
            self.TAG_SHORT: self.write_short,
            self.TAG_INT: self.write_int,
            self.TAG_LONG: self.write_long,
            self.TAG_FLOAT: self.write_float,
            self.TAG_DOUBLE: self.write_double,
            self.TAG_BYTE_ARRAY: self.write_byte_array,
            self.TAG_STRING: self.write_string,
            self.TAG_LIST: self.write_list,
            self.TAG_COMPOUND: self.write_compound,
            self.TAG_INT_ARRAY: self.write_int_array,
            self.TAG_LONG_ARRAY: self.write_long_array,
        }

        """Write an NBT tag based on its type using the tag_writers mapping."""
        if tag_type in tag_writers:
            tag_writers[tag_type](value)  # type: ignore[operator]
        else:
            raise ValueError(f"Unknown tag type {tag_type}")

    def write(self) -> bytes:
        # Write the NBT data to the stream
        self.write_nbt(next(iter(self.output.keys())), next(iter(self.output.values())))
        self.writer.flush()
        return self.output_stream.getvalue()

    def write_nbt(self, name: str, data: Any) -> None:
        """Write the root tag."""
        self.write_byte(self.TAG_COMPOUND)  # Root is always a compound
        self.write_string(name)
        self.write_tag(self.get_tag_type(data), data)
        self.write_byte(self.TAG_END)  # End root compound

    @staticmethod
    def from_file(filename: "str | Path") -> "NBTParser":
        with gzip.open(filename, 'rb') as f:
            return NBTParser(f.read())

    def to_file(self, filename: "str | Path") -> None:
        """Save modified NBT data to a file."""
        with gzip.open(filename, "wb") as f:
            f.write(self.write())


# data = NBTParser.from_file(r"C:\Users\Ben\Desktop\pypacks\examples\development\structures\iron_block_crafting_recipe.nbt")
# rint(data.output)
# structure = Structure.from_nbt(data.output)
