from pypacks.automatic_testing.testing_blocks import Air, Hopper, Furnace, AutoCrafter, BlockType
from math import sqrt
import os


class TestList:
    def __init__(self, tests: list["Test"]) -> None:
        self.tests = tests

    def to_file(self, path: str, origin_relative_x: int, origin_relative_y: int, origin_relative_z: int) -> None:
        with open(path, "w") as file:
            file.write("\n".join([test.generate_commands(origin_relative_x, origin_relative_y, test_index*2+origin_relative_z) for test_index, test in enumerate(self.tests)]))

class Test:
    def __init__(self, name: str, blocks: list[BlockType]) -> None:
        self.name = name
        self.blocks = blocks
        self.size = int(sqrt(len(self.blocks)))

    def generate_commands(self, x: int, y: int, z: int) -> str:
        # Figure out what size square the list is in:
        lines = [self.blocks[i*self.size:(i+1)*self.size] for i in range(self.size)][::-1]
        commands = []
        for relative_y, line in enumerate(lines):
            for relative_x, block in enumerate(line):
                command = block.to_setblock_command(x, y+relative_y, z+relative_x)
                commands.append(command)
        return f"# {self.name}\n"+"\n".join(commands) + "\n"

furnace_test = Test("Furnace Test", [  # type: ignore
    Air(), Hopper(["minecraft:porkchop"]), Air(),
    Air(), Furnace(), Air(),
    Air(), Hopper(), Air(),
])
custom_furnace_recipe_test = Test("Custom Furnace Recipe Test", [  # type: ignore
    Air(), Hopper(["minecraft:feather"]), Air(),
    Air(), Furnace(), Air(),
    Air(), Hopper(), Air(),
])
custom_crafting_recipe_test = Test("Custom Crafting Recipe Test", [  # type: ignore
    Air(), Hopper({"minecraft:iron_ingot": 4}), Air(),
    Air(), AutoCrafter([1, 3, 4, 5, 7]), Air(),
    Air(), Hopper(), Air(),
])

test_list = TestList([furnace_test, custom_furnace_recipe_test, custom_crafting_recipe_test])
path = f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\.minecraft\\saves\\PyPacksWorld\\datapacks\\PyPacks Tests\\data\\pypacks_tests\\function\\test.mcfunction"
test_list.to_file(path, 0, 2, 0)
print(f"Saving tests to {path}")