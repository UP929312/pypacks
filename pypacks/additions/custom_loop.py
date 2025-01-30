from dataclasses import dataclass, field

from pypacks.resources.custom_mcfunction import MCFunction


@dataclass
class CustomLoop:
    """This class manages loops, so you can run code every x seconds or ticks"""
    internal_name: str
    interval_in_ticks: int  # How long to wait before running the command again, to convert seconds to ticks, multiply by 20
    command: "str | MCFunction"

    scoreboard_objective_name: str = field(init=False, repr=False, hash=False, default="loop_dispatch_counters")

    def generate_global_tick_counter(self) -> str:
        return f"scoreboard players add global_tick_counter {self.scoreboard_objective_name} 1"

    def generate_set_constant_command(self) -> str:
        return f"scoreboard players set {self.interval_in_ticks} constants {self.interval_in_ticks}"

    @staticmethod
    def generate_loop_manager_function(loops: list["CustomLoop"], pack_namespace: str) -> MCFunction:
        return MCFunction(
            f"loop_manager",
            [
                *[
                    f"scoreboard players operation {loop.internal_name}_intervals loop_dispatch_counters = global_tick_counter loop_dispatch_counters"
                    for loop in loops
                ],
                *[
                    # scoreboard players operation <targets> <targetObjective> <operation> <source> <sourceObjective>‌
                    f"scoreboard players operation {loop.internal_name}_intervals {loop.scoreboard_objective_name} %= {loop.interval_in_ticks} constants"
                    for loop in loops
                ],
                *[
                    f"execute if score {loop.internal_name}_intervals {loop.scoreboard_objective_name} matches 0 run {loop.command.get_run_command(pack_namespace) if isinstance(loop.command, MCFunction) else loop.command}"
                    for loop in loops
                ],
            ],
        )
