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
    command: "str | MCFunction"  # TODO: Support command`s` as well (need to potentially have something create a function for it)

    scoreboard_objective_name: str = field(init=False, repr=False, hash=False, default="loop_dispatch_counters")
    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="function/custom_blocks")

    def generate_global_tick_counter(self) -> str:
        return f"scoreboard players add global_tick_counter {self.scoreboard_objective_name} 1"

    def generate_set_constant_command(self) -> str:
        return f"scoreboard players set {self.interval_in_ticks} constants {self.interval_in_ticks}"

    def create_datapack_files(self, pack: "Pack") -> None:
        if isinstance(self.command, MCFunction):
            return self.command.create_datapack_files(pack)

    @staticmethod
    def generate_loop_manager_function(loops: list["CustomLoop"], pack_namespace: str) -> MCFunction:
        return MCFunction(
            "loop_manager",
            [
                (
                    f"scoreboard players operation {loop.internal_name}_intervals loop_dispatch_counters = global_tick_counter loop_dispatch_counters \n" +
                    f"scoreboard players operation {loop.internal_name}_intervals {loop.scoreboard_objective_name} %= {loop.interval_in_ticks} constants \n" +
                    f"execute if score {loop.internal_name}_intervals {loop.scoreboard_objective_name} matches 0 run {loop.command.get_run_command(pack_namespace) if isinstance(loop.command, MCFunction) else loop.command}"
                )
                for loop in loops
            ],
        )
