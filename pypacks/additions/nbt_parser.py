# This is a simple NBT parser that can read NBT files and return the data as a Python dictionary.
import struct
import gzip
from io import BufferedReader, BytesIO
from dataclasses import dataclass
from typing import Any


@dataclass
class Structure:
    size: tuple[int, int, int]
    blocks: list[dict[str, Any]]
    entities: list[dict[str, Any]]
    data_version: int

    @classmethod
    def from_nbt(cls, nbt: dict[str, Any]) -> "Structure":
        nbt = nbt['']
        size = tuple(nbt['size'])
        blocks = nbt['blocks']
        entities = nbt['entities']
        data_version = nbt['DataVersion']
        return cls(size, blocks, entities, data_version)


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
        # mapping = {
        #     self.TAG_BYTE: self.read_byte(),
        #     self.TAG_SHORT: self.read_short(),
        #     self.TAG_INT: self.read_int(),
        #     self.TAG_LONG: self.read_long(),
        #     self.TAG_FLOAT: self.read_float(),
        #     self.TAG_DOUBLE: self.read_double(),
        #     self.TAG_BYTE_ARRAY: self.read_byte_array(),
        #     self.TAG_STRING: self.read_string(),
        #     self.TAG_LIST: self.read_list(),
        #     self.TAG_COMPOUND: self.read_compound(),
        #     self.TAG_INT_ARRAY: self.read_int_array(),
        #     self.TAG_LONG_ARRAY: self.read_long_array(),
        # }
        # if tag_type not in mapping:
        #     raise ValueError(f"Unknown tag type {tag_type}")
        # return mapping[tag_type]

        if tag_type == self.TAG_BYTE:
            return self.read_byte()
        if tag_type == self.TAG_SHORT:
            return self.read_short()
        if tag_type == self.TAG_INT:
            return self.read_int()
        if tag_type == self.TAG_LONG:
            return self.read_long()
        if tag_type == self.TAG_FLOAT:
            return self.read_float()
        if tag_type == self.TAG_DOUBLE:
            return self.read_double()
        if tag_type == self.TAG_BYTE_ARRAY:
            return self.read_byte_array()
        if tag_type == self.TAG_STRING:
            return self.read_string()
        if tag_type == self.TAG_LIST:
            return self.read_list()
        if tag_type == self.TAG_COMPOUND:
            return self.read_compound()
        if tag_type == self.TAG_INT_ARRAY:
            return self.read_int_array()
        if tag_type == self.TAG_LONG_ARRAY:
            return self.read_long_array()
        raise ValueError(f"Unknown tag type {tag_type}")

    def read_byte(self) -> int:
        return struct.unpack('>b', self.stream.read(1))[0]  # type: ignore[no-any-return]

    def read_short(self) -> int:
        return struct.unpack('>h', self.stream.read(2))[0]  # type: ignore[no-any-return]

    def read_int(self) -> int:
        return struct.unpack('>i', self.stream.read(4))[0]  # type: ignore[no-any-return]

    def read_long(self) -> float:
        return struct.unpack('>q', self.stream.read(8))[0]  # type: ignore[no-any-return]

    def read_float(self) -> float:
        return struct.unpack('>f', self.stream.read(4))[0]  # type: ignore[no-any-return]

    def read_double(self) -> float:
        return struct.unpack('>d', self.stream.read(8))[0]  # type: ignore[no-any-return]

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
print(data.output)
structure = Structure.from_nbt(data.output)
# rint(structure)
