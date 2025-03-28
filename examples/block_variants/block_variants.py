from pypacks import Pack
from pypacks.resources import CustomItem
from pypacks.additions import CustomBlock, Config

import os
os.chdir(os.path.dirname(__file__))

namespace = "pypacks_block_variants"

ruby = CustomItem(f"{namespace}_ruby", "minecraft:emerald", "Special Ruby", lore=["Custom Ruby, ooh!"], texture_path="images/ruby.png")
ruby_ore = CustomItem(f"{namespace}_ruby_ore", "minecraft:redstone_ore", "Ruby Ore", texture_path="images/ruby_ore.png")
ruby_ore_block = CustomBlock.from_item(ruby_ore, regular_drops=ruby)
ruby_ore_slab = ruby_ore_block.create_slab("stone_slab")

datapack = Pack(
    name="PyPacks Block Variant", description="A Datapack showcasing block variants (slabs, stairs, etc.)", namespace="pypacks_block_variants",
    world_name="PyPacksWorld",
    custom_items=[ruby, ],
    custom_blocks=[ruby_ore_block, ruby_ore_slab],
    config=Config.empty_config(),
).generate_pack()
