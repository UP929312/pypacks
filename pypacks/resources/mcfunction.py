from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pypacks.datapack import Datapack

@dataclass
class MCFunction:
    """Creates a minecraft function file"""
    internal_name: str
    commands: list[str]
    sub_directories: list[str] = field(default_factory=list)  # Allow this to be a str

    datapack_subdirectory_name: str = field(init=False, repr=False, default="function")

    def __post_init__(self) -> None:
        assert len("".join(self.commands)) <= 2_000_000, "MCFunction files must be less than 2 million characters!"

    def get_reference(self, datapack: "Datapack") -> str:
        return f"{datapack.namespace}:{'/'.join(self.sub_directories)}/{self.internal_name}"

    def create_datapack_files(self, datapack: "Datapack") -> None:
        # Can't use / here because of *self.sub_directories
        path = Path(datapack.datapack_output_path, "data", datapack.namespace, self.__class__.datapack_subdirectory_name,
                            *self.sub_directories, f"{self.internal_name}.mcfunction")
        with open(path, "w") as file:
            file.write("\n".join(self.commands))

    # Untested
    # def __or__(self, other: "MCFunction") -> "MCFunction":
    #     # So we can merge functions by doing | on them
    #     return MCFunction(
    #         internal_name=f"{self.internal_name}",
    #         commands=self.commands + other.commands,
    #         sub_directories=self.sub_directories,
    #     )

    # def __ror__(self, other: "MCFunction") -> "MCFunction":
    #     return self.__or__(other)
