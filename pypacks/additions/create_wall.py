from pypacks.resources.custom_mcfunction import MCFunction
from pypacks.resources.custom_item import CustomItem


def create_wall(custom_items: list["CustomItem"], pack_namespace: str) -> MCFunction:
    mapping = {i: divmod(i, 4) for i in range(len(custom_items))}

    mcfunction = MCFunction("create_wall", [
        f"fill ~ ~ ~ ~{len(custom_items)//4} ~3 ~ stone_bricks",
        "kill @e[tag=wall_item_frame]"
    ])

    for i, custom_item in enumerate(custom_items):
        x, y = mapping[i]

        components = custom_item.to_dict(pack_namespace) if isinstance(custom_item, CustomItem) else {}
        mcfunction.commands.append(
            f"summon minecraft:item_frame ~{x} ~{y} ~1 {{Tags:[wall_item_frame], Item: {{id: \"{custom_item.base_item}\", components: {components}}}, Facing: 3}}"
        )
    return mcfunction
