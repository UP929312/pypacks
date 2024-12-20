from typing import TYPE_CHECKING

from pypacks.resources.mcfunction import MCFunction
from pypacks.utils import extract_item_type_and_components

if TYPE_CHECKING:
    from .datapack import Datapack
    from .resources.custom_item import CustomItem


def create_wall(custom_items: list["CustomItem"], datapack: "Datapack") -> MCFunction:
    mapping = {i: divmod(i, 4) for i in range(len(custom_items))}

    mcfunction = MCFunction("create_wall", [
        f"fill ~ ~ ~ ~{len(custom_items)//4} ~3 ~ stone_bricks",
        "kill @e[tag=wall_item_frame]"
    ])

    for i, custom_item in enumerate(custom_items):
        x, y = mapping[i]
        _, components = extract_item_type_and_components(custom_item, datapack)
        mcfunction.commands.append(
            f"summon minecraft:item_frame ~{x} ~{y} ~1 {{Tags:[wall_item_frame], Item: {{id: \"{custom_item.base_item}\", components: {components}}}, Facing: 3}}"
        )
    return mcfunction
