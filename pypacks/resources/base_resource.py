import os
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from pypacks.pack import Pack

T = TypeVar("T")


class BaseResource:
    datapack_subdirectory_name: str = "unknown"

    """Stores common methods and variables for most resources"""
    def __init__(self, internal_name: str) -> None:
        self.internal_name = internal_name

    def get_reference(self, pack_namespace: str) -> str:
        if hasattr(self, "sub_directories"):
            return f"{pack_namespace}:{'/'.join(self.sub_directories)}{'/' if self.sub_directories else ''}{self.internal_name}"  # type: ignore[abc]
        return f"{pack_namespace}:{self.internal_name}"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "BaseResource":
        raise NotImplementedError

    def create_datapack_files(self, pack: "Pack") -> None:
        path = Path(pack.datapack_output_path, "data", pack.namespace, self.__class__.datapack_subdirectory_name)
        if hasattr(self, "sub_directories"):
            path = Path(path, *self.sub_directories)  # type: ignore[abc]
        path = Path(path, self.internal_name+".json")
        with open(path, "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)  # type: ignore[arg-type]

    @staticmethod
    def get_all_resource_paths(cls_: type["BaseResource"], root_path: "Path", file_type: str) -> list[tuple["Path", "Path"]]:
        """Returns a tuple of absolute path, relative path for all resources of type, used by MCFunction"""
        item_paths = []
        functions_directory = str(root_path/"data"/"pypacks_testing"/cls_.datapack_subdirectory_name)+"\\"
        for root, _, files in os.walk(functions_directory):
            for file_name in files:
                if file_name.endswith(file_type):
                    item_paths.append((Path(root+"/"+file_name), Path(str(root.removeprefix(functions_directory)))))  # TODO: This isn't right...
        return item_paths

    @classmethod
    def from_datapack_files(cls: type[T], root_path: "Path") -> list[T]:
        """Path should be the root of the pack"""
        return [
            cls.from_dict(file_path.stem, json.load(file_path.open("r")))  # type: ignore[abc]
            for file_path in root_path.glob(f"**/{cls.datapack_subdirectory_name}/*.json")  # type: ignore[abc]
        ]
