# Crafting
setblock ~ ~2 ~2 minecraft:crafting_table
clear @p
give @p minecraft:iron_ingot 6
give @p minecraft:stick 2
give @p minecraft:stone 1
give @p minecraft:spruce_planks 1

# Furnace
setblock ~ ~2 ~4 minecraft:furnace
give @p minecraft:coal 1
give @p minecraft:diamond 1

# Smoker
setblock ~ ~2 ~6 minecraft:smoker
give @p minecraft:coal 1
give @p minecraft:redstone 1

# Campfire
setblock ~ ~2 ~8 minecraft:campfire
give @p minecraft:lapis_lazuli 1

# Painting
summon minecraft:painting ~-1 ~3 ~11 {variant: "pypacks_testing:logo_art", facing: 1}

# Jukebox
setblock ~ ~2 ~15 minecraft:jukebox
give @p minecraft:lapis_lazuli 1
give @p minecraft:music_disc_cat[jukebox_playable={"song": "pypacks_testing:rick_roll"}]