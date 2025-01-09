from pypacks.automatic_testing.testing_blocks import *  # noqa: F403
from math import sqrt
import os


class TestList:
    def __init__(self, tests: list["Test"]) -> None:
        self.tests = tests

    def to_file(self, path: str, origin_relative_x: int, origin_relative_y: int, origin_relative_z: int) -> None:
        with open(path, "w") as file:
            clear_space = f"#Empty aread\nfill ~-3 ~2 ~2 ~3 ~7 ~{2+(len(self.tests)*2)} air\n\n"
            commands = "\n".join([test.generate_commands(origin_relative_x, origin_relative_y, test_index*2+origin_relative_z) for test_index, test in enumerate(self.tests)])
            file.write(clear_space+commands)


class Test:
    def __init__(self, name: str, blocks: list[BlockType]) -> None:
        self.name = name
        self.blocks: list["BlockType"] = blocks  # type: ignore[assignment]
        self.size = int(sqrt(len(self.blocks)))

    def generate_commands(self, x: int, y: int, z: int) -> str:
        # Figure out what size square the list is in:
        lines = [self.blocks[i*self.size:(i+1)*self.size] for i in range(self.size)]
        commands = []
        for relative_y, line in enumerate(lines):
            for relative_x, block in enumerate(line):
                command = block.to_setblock_command(x+(self.size-relative_x), y+(self.size-relative_y), z)
                commands.append(command)
        return f"# {self.name}\n"+"\n".join(commands) + "\n"


furnace_test = Test("Furnace Test", [  # type: ignore
    Air(), Hopper(["minecraft:porkchop"]), Air(),
    Air(), Furnace(),                      Air(),  # fmt: skip
    Air(), ExpectedHopper(""),             Air(),  # fmt: skip
])
custom_furnace_recipe_test = Test("Custom Furnace Recipe Test", [  # type: ignore
    Air(), Hopper(["minecraft:feather"]), Air(),
    Air(), Furnace(),                     Air(),  # fmt: skip
    Air(), ExpectedHopper(""),            Air(),  # fmt: skip
])
custom_crafting_recipe_test = Test("Custom Crafting Recipe Test", [  # type: ignore
    Air(), Hopper({"minecraft:iron_ingot": 4}), Air(),
    Air(), AutoCrafter([1, 3, 4, 5, 7]),        AddedRedstoneBlock(),  # fmt: skip
    Air(), ExpectedHopper(""),                  RemovedRedstoneBlock(),  # fmt: skip
])

test_list = TestList([furnace_test, custom_furnace_recipe_test, custom_crafting_recipe_test])
path = f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\.minecraft\\saves\\PyPacksWorld\\datapacks\\PyPacks Tests\\data\\pypacks_tests\\function\\test.mcfunction"
test_list.to_file(path, 0, 2, 0)
print(f"Saving tests to {path}")
