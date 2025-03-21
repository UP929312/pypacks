from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pypacks.resources.custom_mcfunction import MCFunction

if TYPE_CHECKING:
    from pypacks.pack import Pack


@dataclass
class CustomLoop:
    """This class manages loops, so you can run code every x seconds or ticks"""
    internal_name: str
    interval_in_ticks: int  # How long to wait before running the command again, to convert seconds to ticks, multiply by 20
    commands: list["MCFunction | str"]

    scoreboard_objective_name: str = field(init=False, repr=False, hash=False, default="loop_dispatch_counters")
    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="function/custom_blocks")

    def generate_global_tick_counter(self) -> str:
        return f"scoreboard players add global_tick_counter {self.scoreboard_objective_name} 1"

    def generate_set_constant_command(self) -> str:
        return f"scoreboard players set {self.interval_in_ticks} constants {self.interval_in_ticks}"

    def get_command_to_run(self, pack_namespace: str) -> str:
        """This exists so we can be sure to call either the regular command (for single commands) or the new combined function"""
        if len(self.commands) == 1:
            if isinstance(self.commands[0], MCFunction):
                return self.commands[0].get_run_command(pack_namespace)
            return self.commands[0]
        return MCFunction(f"{self.internal_name}_combined_loop", []).get_run_command(pack_namespace)

    def create_datapack_files(self, pack: "Pack") -> None:
        if len(self.commands) == 1:
            if isinstance(self.commands[0], MCFunction):
                self.commands[0].create_datapack_files(pack)
            return
        # If they pass in multiple commands, we make a proxy function which gets called instead.
        combined_mcfunction = MCFunction(f"{self.internal_name}_combined_loop",
            [x.get_run_command(pack.namespace) if isinstance(x, MCFunction) else x for x in self.commands],
        )
        return combined_mcfunction.create_datapack_files(pack)

    @staticmethod
    def generate_loop_manager_function(loops: list["CustomLoop"], pack_namespace: str) -> MCFunction:
        return MCFunction(
            "loop_manager",
            [
                (
                    f"scoreboard players operation {loop.internal_name}_intervals loop_dispatch_counters = global_tick_counter loop_dispatch_counters \n" +
                    f"scoreboard players operation {loop.internal_name}_intervals {loop.scoreboard_objective_name} %= {loop.interval_in_ticks} constants \n" +
                    f"execute if score {loop.internal_name}_intervals {loop.scoreboard_objective_name} matches 0 run {loop.get_command_to_run(pack_namespace)}"
                )
                for loop in loops
            ],
        )
