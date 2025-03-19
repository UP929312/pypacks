import os
import json
from dataclasses import fields, MISSING
from pathlib import Path
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from pypacks.pack import Pack

T = TypeVar("T")


class BaseResource:
    datapack_subdirectory_name: str = "unknown"
    resource_pack_subdirectory_name: str = "unknown"

    """Stores common methods and variables for most resources"""
    def __init__(self, internal_name: str) -> None:
        self.internal_name = internal_name

    def get_reference(self, pack_namespace: str) -> str:
        if hasattr(self, "sub_directories"):
            return f"{pack_namespace}:{'/'.join(self.sub_directories)}{'/' if self.sub_directories else ''}{self.internal_name}"  # pyright: ignore
        return f"{pack_namespace}:{self.internal_name}"

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "BaseResource":
        raise NotImplementedError

    def create_datapack_files(self, pack: "Pack") -> None:
        path = Path(pack.datapack_output_path, "data", pack.namespace, self.__class__.datapack_subdirectory_name)
        if hasattr(self, "sub_directories"):
            path = Path(path, *self.sub_directories)  # pyright: ignore
        os.makedirs(path, exist_ok=True)
        with open(path/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)

    def create_resource_pack_files(self, pack: "Pack") -> None:
        path = Path(pack.resource_pack_path, "assets", pack.namespace, self.__class__.resource_pack_subdirectory_name)
        if hasattr(self, "sub_directories"):
            path = Path(path, *self.sub_directories)  # pyright: ignore
        os.makedirs(path, exist_ok=True)
        with open(path/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)

    @staticmethod
    def get_all_resource_paths(cls_: type["BaseResource"], root_path: "Path", file_type: str = ".json") -> list["Path"]:
        """Returns an absolute path for all resources of type, used by MCFunction and CustomTag"""
        item_paths = []
        functions_directory = str(root_path/"data"/"pypacks_testing"/cls_.datapack_subdirectory_name)+"/"
        for root, _, files in os.walk(functions_directory):
            for file_name in files:
                if file_name.endswith(file_type):
                    item_paths.append(Path(root+"/"+file_name))
        return item_paths

    @classmethod
    def from_datapack_files(cls: type[T], root_path: "Path") -> list[T]:
        """Path should be the root of the pack"""
        return [  # TODO: Change the **/ to **/data/namespace, etc.
            cls.from_dict(file_path.stem, json.load(file_path.open("r")))  # type: ignore[attr-defined]
            for file_path in root_path.glob(f"**/{cls.datapack_subdirectory_name}/**/*.json")  # type: ignore[attr-defined]
        ]

    @classmethod
    def from_resource_pack_files(cls: type[T], root_path: "Path") -> list[T]:
        """Path should be the root of the pack"""
        assert issubclass(cls, BaseResource)
        if any(f.name == "sub_directories" for f in fields(cls)):  # type: ignore[attr-defined]
            return [
                cls.from_dict(
                    file_path.stem, json.load(file_path.open("r")),
                    sub_directories=list(file_path.relative_to(root_path).parent.parts[1:]),  # type: ignore[attr-defined]
                )
                for file_path in root_path.glob(f"**/{cls.resource_pack_subdirectory_name}/**/*.json")
            ]
        return [
            cls.from_dict(file_path.stem, json.load(file_path.open("r")))  # type: ignore[attr-defined]
            for file_path in root_path.glob(f"**/{cls.resource_pack_subdirectory_name}/**/*.json")
        ]

    @classmethod
    def from_combined_files(cls: type[T], datapack_root_path: "Path", resource_pack_root_path: "Path") -> list[T]:
        """Path should be the root of the pack"""
        raise NotImplementedError


def overridden_repr(self) -> str:  # type: ignore[no-untyped-def]
    """This function overrides the dataclasses "__repr__" function to only show non-default attributes, so when we create them, it doesn't
    show unnecessary information, i.e. ones that are already default."""
    # Calculate default values, considering both default and default_factory
    default_values = {
        field.name: (field.default_factory() if field.default_factory is not MISSING else field.default)
        for field in fields(self)
        if field.default is not MISSING or field.default_factory is not MISSING
    }

    # Exclude fields with `init=False` (normally class attributes like datapack_sub_directory) or `repr=False` and those that match defaults
    non_default_attrs = {
        key: value for key, value in self.__dict__.items()
        if key not in {field.name for field in fields(self) if not field.init or not field.repr}  # TODO: Why do we exclude repr=False again?
        and (key not in default_values or default_values[key] != value)
    }

    # Return formatted non-default attributes
    return f"{self.__class__.__name__}({', '.join(f'{key}={repr(value)}' for key, value in non_default_attrs.items())})"
