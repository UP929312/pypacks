from typing import TYPE_CHECKING, Any, Literal
from dataclasses import dataclass, field

from pypacks.resources.base_resource import BaseResource
from pypacks.utils import recursively_remove_nones_from_data

if TYPE_CHECKING:
    from pypacks.resources.custom_mcfunction import MCFunction
    from pypacks.resources.world_gen.structure import GameTestStructure
    from pypacks.pack import Pack


@dataclass
class CustomGameTest(BaseResource):
    """A test instance represents a test that can be run by the GameTest framework."""
    # https://minecraft.wiki/w/Test_instance_definition
    internal_name: str
    environment: "str | CustomTestEnvironment"  # The environment of this test.
    structure: "str | GameTestStructure"  # The structure to use for the test (or a path to a structure.nbt file).
    max_ticks: int  # A positive integer representing the maximum number of ticks allowed to pass before the test is considered timed out.
    setup_ticks: int = 0  # Represents a number of ticks to wait after placing the structure before starting the test. Must be a non-negative integer.
    required: bool = True  # Whether the test is considered required to pass for the full test suite to pass.
    rotation: Literal["none", "clockwise_90", "180", "counterclockwise_90"] = "none"  # Rotation to apply to the test structure.
    manual_only: bool = False  # Set to true for tests that are not included as part of automated test runs.
    sky_access: bool = False  # Whether the test needs clear access to the sky. Tests are enclosed in barrier blocks. If set to true, the top is left open.
    max_attempts: int = 1  # Number of attempts to run the test.
    required_successes: int = 1  # Number of attempts that must succeed for the test to be considered successful.
    type: Literal["block_based", "function"] = "block_based"  # The type of test.
    function: "MCFunction | str | None" = None  # The function to run for the test. Only used if type is "function".

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="test_instance")

    def __post_init__(self) -> None:
        if self.type == "function" and self.function is None:
            raise ValueError("A function must be provided for a function test.")
        if self.type != "function" and self.function is not None:
            raise ValueError("A function cannot be provided for a block-based test.")

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        from pypacks.resources.world_gen.structure import GameTestStructure
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "environment": self.environment.get_reference(pack_namespace) if isinstance(self.environment, CustomTestEnvironment) else self.environment,
            "structure": self.structure.get_reference(pack_namespace) if isinstance(self.structure, GameTestStructure) else self.structure,
            "max_ticks": self.max_ticks,
            "setup_ticks": self.setup_ticks if self.setup_ticks != 0 else None,
            "required": False if not self.required else None,
            "rotation": self.rotation if self.rotation != "none" else None,
            "manual_only": self.manual_only if self.manual_only else None,
            "sky_access": self.sky_access if self.sky_access else None,
            "max_attempts": self.max_attempts if self.max_attempts != 1 else None,
            "required_successes": self.required_successes if self.required_successes != 1 else None,
            "type": self.type,
        })

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "CustomGameTest":
        return cls(
            internal_name,
            environment=data["environment"],
            structure=data["structure"].split(":")[1],
            max_ticks=data["max_ticks"],
            setup_ticks=data.get("setup_ticks", 0),
            required=data.get("required", True),
            rotation=data.get("rotation", "none"),
            manual_only=data.get("manual_only", False),
            sky_access=data.get("sky_access", False),
            max_attempts=data.get("max_attempts", 1),
            required_successes=data.get("required_successes", 1),
            type=data.get("type", "block_based"),
            function=data.get("function"),
        )

    def get_run_command(self, pack_namespace: str) -> str:
        return f"test run {self.get_reference(pack_namespace)}"

    def create_datapack_files(self, pack: "Pack") -> None:
        super().create_datapack_files(pack)
        from pypacks.resources.world_gen.structure import GameTestStructure
        if isinstance(self.structure, GameTestStructure):
            self.structure.create_datapack_files(pack)

    # @classmethod
    # def from_datapack_files(cls, root_path: "Path") -> list["CustomGameTest"]:
    #     game_tests: list["CustomGameTest"] = super().from_datapack_files(root_path)  # type: ignore[assign]
    #     for game_test in game_tests:
    #         path: "Path" = root_path/"structure"/game_test.structure  # type: ignore[abc]
    #         if path.exists():
    #             game_test.structure = GameTestStructure(game_test.internal_name, path)
    #         else:
    #             raise FileNotFoundError(f"Structure file not found at {path}")
    #     return game_tests


@dataclass
class CustomTestEnvironment(BaseResource):
    """Do not instantiate this class directly. Use one of the subclasses instead."""
    internal_name: str

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="test_environment")

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "CustomTestEnvironment":
        cls_ = TEST_ENVIRONMENT_TO_CLASSES[data["type"]]
        return cls_.from_dict(internal_name, data)


@dataclass
class AllOfEnvironment(CustomTestEnvironment):
    """Applies multiple environments"""
    # https://minecraft.wiki/w/Test_environment_definition#all_of
    definitions: list["CustomTestEnvironment | str"]  # Another test environment.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "all_of",
            "definitions": [
                definition.get_reference(pack_namespace) if isinstance(definition, CustomTestEnvironment) else definition
                for definition in self.definitions
            ],
        }

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "AllOfEnvironment":
        return cls(
            internal_name,
            definitions=data["definitions"],
        )

    def create_datapack_files(self, pack: "Pack") -> None:
        super().create_datapack_files(pack)
        for definition in self.definitions:
            if isinstance(definition, CustomTestEnvironment):
                definition.create_datapack_files(pack)


@dataclass
class FunctionEnvironment(CustomTestEnvironment):
    """Uses functions to set up and tear down the test."""
    # https://minecraft.wiki/w/Test_environment_definition#function
    setup: "MCFunction | str | None" = None  # The function to use for setup.
    teardown: "MCFunction | str | None" = None  # The function to use for teardown.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        from pypacks.resources.custom_mcfunction import MCFunction
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "type": "function",
            "setup": self.setup.get_reference(pack_namespace) if isinstance(self.setup, MCFunction) else self.setup,
            "teardown": self.teardown.get_reference(pack_namespace) if isinstance(self.teardown, MCFunction) else self.teardown,
        })

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "FunctionEnvironment":
        return cls(
            internal_name,
            setup=data.get("setup"),
            teardown=data.get("teardown"),
        )


@dataclass
class GameRulesEnvironment(CustomTestEnvironment):
    """Applies game rules during the test, and resets them after tests have completed."""
    # https://minecraft.wiki/w/Test_environment_definition#game_rules
    bool_rules: dict[str, bool] = field(default_factory=dict)  # A map of boolean game rules to set and their value. (e.g. {"doDaylightCycle": False})
    int_rules: dict[str, int] = field(default_factory=dict)  # A map of integer game rules to set and their value. (e.g. {"randomTickSpeed": 0})

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "game_rules",
            "bool_rules": [{"rule": key, "value": value} for key, value in self.bool_rules.items()],
            "int_rules": [{"rule": key, "value": value} for key, value in self.int_rules.items()],
        }

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "GameRulesEnvironment":
        return cls(
            internal_name,
            bool_rules={rule["rule"]: rule["value"] for rule in data["bool_rules"]},
            int_rules={rule["rule"]: rule["value"] for rule in data["int_rules"]},
        )


@dataclass
class WeatherEnvironment(CustomTestEnvironment):
    """Applies specific weather during the test, and resets it after tests have completed."""
    # https://minecraft.wiki/w/Test_environment_definition#weather
    weather: Literal["clear", "rain", "thunder"]  # The weather to set.

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "weather",
            "weather": self.weather,
        }

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "WeatherEnvironment":
        return cls(
            internal_name,
            weather=data["weather"],
        )


@dataclass
class TimeOfDayEnvironment(CustomTestEnvironment):
    """Changes the time to the specified value, and resets it after tests have completed."""
    # https://minecraft.wiki/w/Test_environment_definition#time_of_day
    time: int  # The time of day to set in number of ticks

    def __post_init__(self) -> None:
        if self.time < 0:
            raise ValueError("Time must be a non-negative integer.")

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        return {
            "type": "time_of_day",
            "time": self.time,
        }

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "TimeOfDayEnvironment":
        return cls(
            internal_name,
            time=data["time"],
        )


TEST_ENVIRONMENT_TO_CLASSES: dict[str, type["CustomTestEnvironment"]] = {
    "all_of": AllOfEnvironment,
    "function": FunctionEnvironment,
    "game_rules": GameRulesEnvironment,
    "weather": WeatherEnvironment,
    "time_of_day": TimeOfDayEnvironment,
}
