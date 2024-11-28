import os
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pypacks.datapack import Datapack

@dataclass
class MCFunction:
    """Creates a minecraft function file"""
    internal_name: str
    commands: list[str]
    sub_directories: list[str] = field(default_factory=list)  # Allow this to be a str

    datapack_subdirectory_name: str = field(init=False, default="function")

    def create_datapack_files(self, datapack: "Datapack") -> None:
        path = os.path.join(datapack.datapack_output_path, "data", datapack.namespace, self.__class__.datapack_subdirectory_name,
                            *self.sub_directories, f"{self.internal_name}.mcfunction")
        with open(path, "w") as file:
            file.write("\n".join(self.commands))