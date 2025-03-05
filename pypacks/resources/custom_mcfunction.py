import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from pypacks.scripts.repos.mcfunction_header_patterns import (
    MACRO_PATTERN, MACRO_MESSAGE, VARIABLE_PAIR_PATTERNS, VARIABLE_MESSAGE, FUNCTION_PATTERNS, FUNCTION_MESSAGE,
)

if TYPE_CHECKING:
    from pypacks.pack import Pack


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

    @property
    def _is_empty(self) -> bool:
        return not any(self.commands)

    def get_run_command(self, pack_namespace: str) -> str:
        return f"function {self.get_reference(pack_namespace)}"

    def do_function_checks(self, pack: "Pack") -> None:
        command_lines = [x.get_reference(pack.namespace) if isinstance(x, MCFunction) else x for x in self.commands]
        # Verify / lines
        lines_startwith_with_slash = [x for x in command_lines if x.startswith("/")]
        if lines_startwith_with_slash:
            print(f"Warning, {self.internal_name}.mcfunction has lines starting with /: {lines_startwith_with_slash}")
        # Verify Macro lines
        if pack.config.warn_about_non_marked_macro_line:
            for line in command_lines:
                if "$(" in line and not line.startswith("$"):
                    print(f"Warning, {self.internal_name}.mcfunction has lines without macro prefix: `{line}`")

    def generate_headers(self, pack_namespace: str) -> str:
        commands_str = "\n".join([x.get_reference(pack_namespace) if isinstance(x, MCFunction) else x for x in self.commands])
        # Macros
        detected_macros = tuple(sorted(set(re.findall(MACRO_PATTERN, commands_str))))
        # Detected functions
        detected_functions = tuple(sorted(set([x.group(1) for pattern in FUNCTION_PATTERNS for x in re.finditer(pattern, commands_str)])))
        # Variables required
        variables: list[tuple[str, str]] = []
        for pattern in VARIABLE_PAIR_PATTERNS:
            for match in re.finditer(pattern, commands_str):
                variables.append((match.group(1), match.group(2)))  # Group 1, 2 (player, objective)
        detected_variables = tuple(sorted(set(variables), key=lambda x: (x[1], x[0])))  # Group by objective, then player
        # Combine
        pairings = {
            detected_macros:    MACRO_MESSAGE+"\n".join([f"# - {x}" for x in detected_macros]),  # fmt: skip
            detected_functions: FUNCTION_MESSAGE+'\n'.join([f'# - {x}' for x in detected_functions]),
            detected_variables: VARIABLE_MESSAGE+'\n'.join([f'# - Player: {x[0]}, Objective: {x[1]}' for x in detected_variables]),
        }
        return "\n".join([message for found_instances, message in pairings.items() if found_instances]) + ("\n\n" if any(pairings.values()) else "")

    def create_datapack_files(self, pack: "Pack") -> None:
        # Get all the lines
        commands_str = "\n".join([x.get_reference(pack.namespace) if isinstance(x, MCFunction) else x for x in self.commands])
        if (not commands_str.strip()) and not self.create_if_empty:
            return
        self.do_function_checks(pack)
        function_headers = self.generate_headers(pack.namespace)
        # Incase you embed mcfunctions:
        for mcfunction in [x for x in self.commands if isinstance(x, MCFunction)]:
            mcfunction.create_datapack_files(pack)
        # Can't use / here because of *self.sub_directories
        path = Path(pack.datapack_output_path, "data", pack.namespace, self.__class__.datapack_subdirectory_name,
                    *self.sub_directories, f"{self.internal_name}.mcfunction")
        with open(path, "w") as file:
            file.write(function_headers+commands_str)

    @staticmethod
    def create_run_macro_function() -> "MCFunction":
        return MCFunction("run_macro_function", [
            "$$(command)",
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
