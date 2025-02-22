import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pypacks.pack import Pack

MACRO_PATTERN = re.compile(r"(?<=\$\()[A-Za-z0-9_]*(?=\))")
MACRO_MESSAGE = "# This function requires the following macros to be passed in:\n"


@dataclass
class MCFunction:
    """Creates a minecraft function file.
    The order that functions get executed within a single tick is:
    - Functions that belong to #minecraft:tick, from top to bottom.
    - Functions that are scheduled on that tick, from whichever one was added to the queue first.
    - Functions invoked from advancements.
    - Functions invoked from enchantments."""  # To run a function if the executer is console: /execute unless entity @s[type=player] run function
    internal_name: str
    commands: list["str | MCFunction"]
    sub_directories: list[str] = field(default_factory=list)  # Allow this to be a str

    create_if_empty: bool = field(init=False, repr=False, default=False)
    datapack_subdirectory_name: str = field(init=False, repr=False, default="function")

    def __post_init__(self) -> None:
        file_contents = "\n".join([x.get_reference("#"*32) if isinstance(x, MCFunction) else x for x in self.commands])
        assert len(file_contents) <= 2_000_000, "MCFunction files must be less than ~2 million characters!"

    def get_reference(self, pack_namespace: str) -> str:
        return f"{pack_namespace}:{'/'.join(self.sub_directories)}{'/' if self.sub_directories else ''}{self.internal_name}"

    def get_run_command(self, pack_namespace: str) -> str:
        return f"function {self.get_reference(pack_namespace)}"

    def create_datapack_files(self, pack: "Pack") -> None:
        for mcfunction in [x for x in self.commands if isinstance(x, MCFunction)]:
            mcfunction.create_datapack_files(pack)
        commands_str = "\n".join([x.get_reference(pack.namespace) if isinstance(x, MCFunction) else x for x in self.commands])
        if (not commands_str.strip()) and not self.create_if_empty:
            return
        detected_macros = list(sorted(set(re.findall(MACRO_PATTERN, commands_str))))
        # Can't use / here because of *self.sub_directories
        path = Path(pack.datapack_output_path, "data", pack.namespace, self.__class__.datapack_subdirectory_name,
                    *self.sub_directories, f"{self.internal_name}.mcfunction")
        with open(path, "w") as file:
            if detected_macros:
                macro_list = "\n".join([f"# - {x}" for x in detected_macros])
                file.write(f"{MACRO_MESSAGE}{macro_list}\n\n"+commands_str)
                return
            file.write(commands_str)

    @staticmethod
    def create_run_macro_function() -> "MCFunction":
        return MCFunction("run_macro_function", [
            "$$(command)",
            ], ["utils"],
        )

    @staticmethod
    def create_scoreboard_value_to_location_functions(pack_namespace: str) -> "MCFunction":
        return MCFunction("scoreboard_value_to_location", [
            # Reads from three values, then calls the function with those values (x, y, z), requires objective inputs to be set with x, y, z.
            f"execute store result storage {pack_namespace}:macro pos.x int 1 run scoreboard players get x inputs",
            f"execute store result storage {pack_namespace}:macro pos.y int 1 run scoreboard players get y inputs",
            f"execute store result storage {pack_namespace}:macro pos.z int 1 run scoreboard players get z inputs",
            f"$function $(function_name) with storage {pack_namespace}:macro pos",  # Passes in x, y, z
            ], ["utils"],
        )

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
