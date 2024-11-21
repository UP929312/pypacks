from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pypacks.datapack import Datapack

@dataclass
class CustomTag:
    name: str
    folder_name: str
    values: list[str]

    def create_json_file(self, datapack: "Datapack") -> None:
        with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/tags/{self.folder_name}/{self.name}.json", "w") as f:
            f.write(f'{{"values": {self.values}}}')