from pypacks import Pack, BlockRaycast, EntityRaycast
from pypacks.resources import CustomItem

import os
os.chdir(os.path.dirname(__file__))  # This is only required when you're in a subdirectory, for your project, ignore this part!

# ============================================================================================================
# Block Raycasts:

# Simple block raycast, when activated, in a straight line, sets a block to stone where the ray hits.
simple_block_raycast = BlockRaycast(
    "block_raycast",
    on_block_hit_command="setblock ~ ~ ~ minecraft:stone",
    no_blocks_hit_command="say Failed to find a block in the range!",
)

# We can also configure it slightly more, for example increasing the length:
longer_block_raycast = BlockRaycast(
    "longer_block_raycast",
    on_block_hit_command="setblock ~ ~ ~ minecraft:stone",
    max_distance_in_blocks=20,
)

# Or changing it's precision:
accurate_block_raycast = BlockRaycast(
    "accurate_block_raycast",
    on_block_hit_command="setblock ~ ~ ~ minecraft:stone",
    distance_between_iterations=0.001,  # 10x more accurate, but 10x more expensive
)

# Additionally, we can also change the way it works, rather than going until it hits a non-traversable blocks, we can go until we find a specific block
# This is how CustomBlocks work, we go until we find the block the player placed.
specific_block_raycast = BlockRaycast(
    "specific_block_raycast",
    on_block_hit_command="setblock ~ ~ ~ minecraft:diamond_block",
    blocks_to_detect="minecraft:stone",
    if_or_unless="if",
)

# Finally, we can also run a command at each iteration of the raycast, useful for debugging and such, here we'll show a small particle
particle_trail_raycast = BlockRaycast(
    "particle_trail_raycast",
    on_block_hit_command="setblock ~ ~ ~ minecraft:stone",
    command_ran_each_iteration="particle minecraft:flame ~ ~ ~",
)
# ============================================================================================================
# Entity Raycasts:

# Similar to how we have block raycasts, we can also check for the presence of entities.
# Here, we give glowing to the cow that's closest to the player, but still within their line of sight.
simple_entity_raycast = EntityRaycast(
    "simple_entity_raycast",
    on_entity_hit_command="effect give @n[distance=..1] glowing 2 0",
    no_entities_hit_command="say No entities hit!",
    entity_to_detect="minecraft:cow",
)

# Like the block raycast, we can also change the distance and precision of the raycast.
longer_entity_raycast = EntityRaycast(
    "longer_entity_raycast",
    on_entity_hit_command="effect give @n[distance=..1] glowing 2 0",
    max_distance_in_blocks=20,  # Longer range
    distance_between_iterations=0.001,  # More accurate
)

# We can also allow any mob to be detected, not just one or a list of entities
all_entity_raycast = EntityRaycast(
    "all_entity_raycast",
    on_entity_hit_command="effect give @n[distance=..1] glowing 2 0",
    entity_to_detect="all",
)

# Finally, we can also give a list of entities to detect, rather than just one, either through a CustomTag, or list of entity types
list_of_entities_raycast = EntityRaycast(
    "list_of_entities_raycast",
    on_entity_hit_command="effect give @n[distance=..1] glowing 2 0",
    entity_to_detect=["minecraft:cow", "minecraft:chicken"],
)

# ============================================================================================================
# Custom items

# We need a way to trigger these raycasts, luckily, CustomItem's on_right_click parameter allows us to do that by just passing in the raycast.
# simple_block_raycast, longer_block_raycast, accurate_block_raycast, specific_block_raycast, particle_trail_raycast
# simple_entity_raycast, longer_entity_raycast, all_entity_raycast, list_of_entities_raycast

simple_block_raycast_item = CustomItem("simple_block_raycast_item", "minecraft:stick", "Simple Block Raycast", on_right_click=simple_block_raycast)
longer_block_raycast_item = CustomItem("longer_block_raycast_item", "minecraft:stick", "Longer Block Raycast", on_right_click=longer_block_raycast)
accurate_block_raycast_item = CustomItem("accurate_block_raycast_item", "minecraft:stick", "Accurate Block Raycast", on_right_click=accurate_block_raycast)
specific_block_raycast_item = CustomItem("specific_block_raycast_item", "minecraft:stick", "Specific Block Raycast", on_right_click=specific_block_raycast)
particle_trail_raycast_item = CustomItem("particle_trail_raycast_item", "minecraft:stick", "Particle Trail Raycast", on_right_click=particle_trail_raycast)

simple_entity_raycast_item = CustomItem("simple_entity_raycast_item", "minecraft:stick", "Simple Entity Raycast", on_right_click=simple_entity_raycast)
longer_entity_raycast_item = CustomItem("longer_entity_raycast_item", "minecraft:stick", "Longer Entity Raycast", on_right_click=longer_entity_raycast)
all_entity_raycast_item = CustomItem("all_entity_raycast_item", "minecraft:stick", "All Entity Raycast", on_right_click=all_entity_raycast)
list_of_entities_raycast_item = CustomItem("list_of_entities_raycast_item", "minecraft:stick", "List of Entities Raycast", on_right_click=list_of_entities_raycast)

# ============================================================================================================

datapack = Pack(
    name="PyPacks Raycasting Example Pack",
    description="A datapack which showcases all the raycasting functionality",
    namespace="pypacks_raycasting",
    world_name="PyPacksWorld",  # Change me to your world name, and it'll automatically go there!
    custom_items=[
        simple_block_raycast_item, longer_block_raycast_item, accurate_block_raycast_item, specific_block_raycast_item, particle_trail_raycast_item,
        simple_entity_raycast_item, longer_entity_raycast_item, all_entity_raycast_item, list_of_entities_raycast_item
    ],
)
