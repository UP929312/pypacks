import json
import os
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pypacks.datapack import Datapack

@dataclass
class CustomTag:
    internal_name: str
    sub_directories: list[str]
    values: list[str]
    replace: bool = False

    datapack_subdirectory_name: str = field(init=False, default="tags")

    def to_dict(self, datapack: "Datapack") -> dict[str, bool | list[str]]:
        return {
            "replace": self.replace,
            "values": self.values
        }

    def create_datapack_files(self, datapack: "Datapack") -> None:
        path = os.path.join(datapack.datapack_output_path, "data", datapack.namespace, self.__class__.datapack_subdirectory_name,
                            *self.sub_directories, f"{self.internal_name}.json")
        with open(path, "w") as file:
            json.dump(self.to_dict(datapack), file, indent=4)
