import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pypacks.pack import Pack


@dataclass
class CustomTag:
    internal_name: str
    values: list[str]
    sub_directories: list[str]
    replace: bool = False

    datapack_subdirectory_name: str = field(init=False, repr=False, default="tags")

    def to_dict(self, pack_namespace: str) -> dict[str, bool | list[str]]:
        return {
            "replace": self.replace,
            "values": self.values
        }

    def create_datapack_files(self, pack: "Pack") -> None:
        path = Path(pack.datapack_output_path, "data", pack.namespace, self.__class__.datapack_subdirectory_name,
                    *self.sub_directories, f"{self.internal_name}.json")
        with open(path, "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)
