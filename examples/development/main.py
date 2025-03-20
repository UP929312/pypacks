from pypacks import Pack
from pypacks.resources import *  # noqa: F403
from pypacks.additions.item_components import *  # noqa: F403
from pypacks.additions import *  # noqa: F403


import os
os.chdir(os.path.dirname(__file__))

# ============================================================================================================
# region: Custom Paintings, Sounds, Jukebox Songs and Ref Book Categories
custom_painting = CustomPainting("logo_art", "images/logo_512_x_512.png", title="My Masterpiece", width_in_blocks=4, height_in_blocks=4)
custom_sound = CustomSound("rick_roll", "sounds/rick_roll.ogg", 1.0, 1.0)
custom_jukebox_song = CustomJukeboxSong(custom_sound.internal_name, "Rick Roll", custom_sound.ogg_path, 4, 5)
weapons_category = RefBookCategory("weapons", "Weapons", "images/sword.png")
usable_category = RefBookCategory("usable", "Usable", "images/goat_horn.png")
consumable_category = RefBookCategory("consumable", "Consumable", "images/steak.png")
# endregion
# ============================================================================================================
# region: Custom Raycasts
block_ray_cast = BlockRaycast("block_ray_cast", on_block_hit_command="setblock ~ ~ ~ minecraft:stone", no_blocks_hit_command="say Failed!", max_distance_in_blocks=6)
entity_ray_cast = EntityRaycast("entity_ray_cast", on_entity_hit_command="effect give @e[distance=..1] glowing 2 0", no_entities_hit_command="say No entities hit!")
block_blocking_entity_ray_cast = EntityRaycast("block_blocking_entity_ray_cast", on_entity_hit_command="effect give @e[distance=..1] glowing 2 0", no_entities_hit_command="say No entities hit (or block blocked)!", stop_for_blocks=True)
# endregion
# ============================================================================================================
# region: Custom Items
# Custom Items
ruby = CustomItem("ruby", "minecraft:emerald", "Special Ruby", lore=["Custom Ruby, ooh!"], texture_path="images/ruby.png", ref_book_config=RefBookConfig(description="A special ruby, found in the depths of the earth."))
topaz = CustomItem("topaz", "minecraft:redstone", "Topaz", texture_path="images/topaz.png", components=Components(equippable=Equippable("chest")))
weak_axe = CustomItem("weak_axe", "minecraft:netherite_axe", "Weak Axe", components=Components(durability=10, lost_durability=5), ref_book_config=RefBookConfig(category=weapons_category))
flying_helmet = CustomItem("flying_helmet", "minecraft:iron_helmet", "Flying Helmet", components=Components(glider=True, consumable=Consumable(0.5, "drink"), food=Food(5, 0, True), use_remainder=UseRemainder("minecraft:diamond", 2)), ref_book_config=RefBookConfig(category=usable_category))
playable_lapis = CustomItem("playable_lapis", "minecraft:lapis_lazuli", "Playable Lapis", max_stack_size=99, rarity="epic", components=Components(jukebox_playable=JukeboxPlayable("pigstep")), ref_book_config=RefBookConfig(category=usable_category))
musical_horn = CustomItem("musical_horn", "minecraft:goat_horn", "Musical Horn", components=Components(instrument=Instrument("minecraft:item.goat_horn.sound.5", "Custom description?", 5, 256)), ref_book_config=RefBookConfig(category=usable_category))
rick_roll_horn = CustomItem("never_going_to_give_you_up", "minecraft:goat_horn", "Rick Roll", components=Components(instrument=Instrument(custom_sound, "Rick Roll", 5, 256)), ref_book_config=RefBookConfig(category=usable_category))
written_book = CustomItem("already_written_in_book", "minecraft:written_book", "Written Book", components=Components(written_book_content=WrittenBookContent("Hello, World!", "Author", [[{"text": "abc\n"}, {"text": "def"}]])),)
writable_book = CustomItem("writable_book", "minecraft:writable_book", "Writable Book", components=Components(writable_book_content=WritableBookContent(["Hello world"])))
lodestone_tracker = CustomItem("lodestone_tracker", "minecraft:compass", components=Components(lodestone_tracker=LodestoneTracker(126, 68, -41)))
speedy_porkchop = CustomItem("speedy_porkchop", "minecraft:porkchop", "Fast hand, extreme axe", components=Components(tool=Tool(2, 0, [ToolRule("#mineable/axe", 10)])))
unbreakable_axe = CustomItem("unbreakable_axe", "minecraft:stone_axe", "Unbreakable Axe", components=Components(unbreakable=True), ref_book_config=RefBookConfig(category=weapons_category))
player_head = CustomItem("custom_player_head_skin", "minecraft:player_head", "My Skin", components=Components(player_head_username="Skezza"))
sharpness_fish = CustomItem("sharpness_fish", "minecraft:cod", "Sharpness Fish", components=Components(enchantments={"sharpness": 5}), ref_book_config=RefBookConfig(category=consumable_category))
enchantment_spruce_door = CustomItem("shiny_door", "minecraft:spruce_door", "Shiny Door", components=Components(enchantment_glint_override=True))
attribute_modified_axe = CustomItem("attribute_modified_axe", "minecraft:wooden_axe", "Attribute Modified Axe", components=Components(attribute_modifiers=[AttributeModifier(attribute_type="attack_damage", amount=10, operation="add_value", slot="mainhand")]), ref_book_config=RefBookConfig(category=weapons_category))
repairable_axe = CustomItem("repairable_axe", "minecraft:stone_axe", "Repairable Axe", components=Components(durability=1000, lost_durability=500, repair_cost=5, repaired_by=["minecraft:stone"]), ref_book_config=RefBookConfig(category=weapons_category))
slow_enderpearl_recharge = CustomItem("slow_enderpearl_recharge", "minecraft:ender_pearl", "Slow Enderpearl Recharge", components=Components(cooldown=Cooldown(10)))
right_clickable_feather = CustomItem("right_clickable_feather", "minecraft:feather", "Right Clickable Feather", on_right_click="summon minecraft:arrow ^ ^ ^")
right_clickable_nether_quartz = CustomItem("right_clickable_nether_quartz", "minecraft:quartz", "Right Clickable Nether Quartz", on_right_click="give @a grass_block", components=Components(cooldown=Cooldown(seconds=3)))
custom_head_texture = CustomItem("custom_head_texture", "minecraft:player_head", "Custom Head Texture", components=Components(custom_head_texture="eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvZjg3N2M5NTA5NTg3YjNiODhjOTI3Zjc0YWE2NjlhZTg3MjVhMTRmZjU1ZGY2ZGUwMDRjNDFlMjYxNzg1YTJmOCJ9fX0="))
ray_gun = CustomItem("ray_gun", "minecraft:blaze_rod", "Ray Gun", on_right_click=block_ray_cast, ref_book_config=RefBookConfig(category=weapons_category))
entity_finder = CustomItem("entity_finder", "minecraft:stick", "Entity Finder", on_right_click=entity_ray_cast, ref_book_config=RefBookConfig(category=weapons_category))
block_blocked_entity_finder = CustomItem("block_blocked_entity_finder", "minecraft:breeze_rod", "Block Blocking Entity Finder", on_right_click=block_blocking_entity_ray_cast, ref_book_config=RefBookConfig(category=weapons_category))
pre_charged_crossbow = CustomItem("pre_charged_crossbow", "minecraft:crossbow", "Pre Charged Crossbow", components=Components(loaded_projectiles=["minecraft:arrow", "minecraft:arrow", "minecraft:arrow"]), ref_book_config=RefBookConfig(category=weapons_category))
steak_to_ruby_when_eaten = CustomItem("steak_to_ruby_when_eaten", "minecraft:cooked_beef", "Steak to Ruby When Eat", components=Components(consumable=Consumable(0.5, "eat"), food=Food(5, 0, True), use_remainder=UseRemainder(ruby)), ref_book_config=RefBookConfig(category=consumable_category))
custom_firework = CustomItem("custom_firework", "minecraft:firework_rocket", "Custom Firework", components=Components(firework=Firework(flight_duration=3, explosions=[FireworkExplosion(shape="star", colors=[16711680, 65280], fade_colors=[255, 16776960], has_trail=True, has_twinkle=True)])), ref_book_config=RefBookConfig(category=usable_category))
custom_firework_hex = CustomItem("custom_firework_hex", "minecraft:firework_rocket", "Custom Firework Hex", components=Components(firework=Firework(flight_duration=1, explosions=[FireworkExplosion(shape="large_ball", colors=[0xFF0000])])), ref_book_config=RefBookConfig(category=usable_category))
map_with_decoration = CustomItem("map_with_decoration", "minecraft:filled_map", "Map With Decoration", components=Components(map_data=MapData(map_id=1, map_decorations=[MapDecoration("red_x", 120, -46, 0)])), ref_book_config=RefBookConfig(category=usable_category))
colored_map = CustomItem("colored_map", "minecraft:filled_map", "Colored Map", components=Components(map_data=MapData(map_color=0x0000FF)), ref_book_config=RefBookConfig(category=usable_category))
map_with_id = CustomItem("map_with_id", "minecraft:filled_map", "Map with ID", components=Components(map_data=MapData(map_id=1)), ref_book_config=RefBookConfig(category=usable_category))
banner = CustomItem("banner", "minecraft:white_banner", "Banner", components=Components(banner_patterns=[BannerPattern("stripe_left", "red"), BannerPattern("stripe_bottom", "blue")]))
edible_item = CustomItem("edible_witch_spawn_egg", "minecraft:witch_spawn_egg", "Edible Witch Spawn Egg", components=Components(consumable=Consumable(0.5, "drink"), food=Food(5, 0, True)))
note_block_sound_head = CustomItem("note_block_sound_head", "minecraft:player_head", "Note Block Sound Head", components=Components(note_block_sound=custom_sound))
eating_gives_you_speed = CustomItem("eating_gives_you_speed", "minecraft:cooked_rabbit", "Eating Gives You Speed", components=Components(consumable=Consumable(0.5, "eat", on_consume_effects=[PotionEffect("speed", 1, 20*10)]), food=Food(can_always_eat=True)), ref_book_config=RefBookConfig(category=consumable_category))
eating_removes_speed = CustomItem("eating_removes_you_speed", "minecraft:cooked_rabbit", "Eating Removes You Speed", components=Components(consumable=Consumable(0.5, "eat", on_consume_remove_effects=[PotionEffect("speed")]), food=Food(can_always_eat=True)), ref_book_config=RefBookConfig(category=consumable_category))
eating_teleports = CustomItem("eating_teleports", "minecraft:cooked_rabbit", "Eating Teleports", components=Components(consumable=Consumable(0.5, "eat", on_consume_teleport_diameter=5), food=Food(can_always_eat=True)), ref_book_config=RefBookConfig(category=consumable_category))
eating_gives_you_speed_and_teleports = CustomItem("eating_gives_you_speed_and_teleports", "minecraft:cooked_rabbit", "Eating Gives You Speed And Teleports", components=Components(consumable=Consumable(0.5, "eat", on_consume_effects=[PotionEffect("speed", 1, 20*10)], on_consume_teleport_diameter=10), food=Food(can_always_eat=True)), ref_book_config=RefBookConfig(category=consumable_category))
eating_plays_rick_roll = CustomItem("eating_plays_rick_roll", "minecraft:cooked_cod", "Eating Plays Rick Roll", components=Components(consumable=Consumable(0.5, "eat", consuming_sound=custom_sound), food=Food(can_always_eat=True)), ref_book_config=RefBookConfig(category=consumable_category))
colorful_shield = CustomItem("colorful_shield", "minecraft:shield", "Colorful Shield", components=Components(shield_base_color="red"), ref_book_config=RefBookConfig(category=usable_category))
bee_nest = CustomItem("bee_nest", "minecraft:bee_nest", "Bee Nest", components=Components(bees=[Bee(), Bee(), Bee(), Bee()]))
bundle = CustomItem("bundle", "minecraft:bundle", "Bundle", components=Components(bundle_contents=BundleContents({"minecraft:emerald": 5, ruby: 3})), ref_book_config=RefBookConfig(category=usable_category))
filled_barrel = CustomItem("filled_barrel", "minecraft:barrel", "Filled Barrel", components=Components(container_contents=ContainerContents({"minecraft:diamond": 5, ruby: 3})), ref_book_config=RefBookConfig(category=usable_category))
custom_potion = CustomItem("custom_potion", "minecraft:potion", "Custom Potion", components=Components(potion_contents=PotionContents(custom_color=0xFF0000, effects=[PotionEffect("speed", 1, 20*10)])), ref_book_config=RefBookConfig(category=consumable_category))
decorated_pot = CustomItem("decorated_pot", "decorated_pot", "Decorated Pot", components=Components(pot_decorations=["angler_pottery_sherd", "brick", "arms_up_pottery_sherd", "skull_pottery_sherd"]))
death_protection_star = CustomItem("death_protection_star", "minecraft:nether_star", "Death Protection Star", components=Components(death_protection=DeathProtection(apply_affects=[PotionEffect("fire_resistance", 2, 20*5)])), ref_book_config=RefBookConfig(category=consumable_category))
dyed_helmet = CustomItem("dyed_helmet", "minecraft:leather_helmet", "Dyed Helmet", components=Components(dye_color=0xFF00FF))
trimmed_leggings = CustomItem("trimmed_leggings", "minecraft:leather_leggings", "Trimmed Leggings", components=Components(armor_trim=ArmorTrim("host", "emerald")), ref_book_config=RefBookConfig(category=usable_category))
suspicious_stew = CustomItem("suspicious_stew", "minecraft:suspicious_stew", "Suspicious Stew", components=Components(suspicious_stew_effects={"speed": 5*20}), ref_book_config=RefBookConfig(category=consumable_category))
spider_spawner = CustomItem("spider_spawner", "minecraft:spawner", "Spider Spawner", components=Components(block_entity_data={"id": "mob_spawner", "SpawnData": {"entity": {"id": "spider"}}}))
upper_slab = CustomItem("upper_slab", "minecraft:stone_slab", "Upper Slab", components=Components(block_state={"type": "top"}))
fish_bucket = CustomItem("fish_bucket", "minecraft:tropical_fish_bucket", "Fish Bucket", components=Components(bucket_entity_data=BucketEntityData(bucket_variant_tag=TropicalFishData(size="large", pattern=1, body_color="light_blue", pattern_color="yellow"))), ref_book_config=RefBookConfig(category=usable_category))
loot_table_chest = CustomItem("loot_table_chest", "minecraft:chest", "Loot Table Chest", components=Components(container_loot_table="minecraft:chests/village/village_butcher"))
on_drop_gold_ingot = CustomItem("on_drop_gold_ingot", "minecraft:gold_ingot", "On Drop Gold Ingot", on_item_drop="say Hi!")
on_drop_copper_ingot = CustomItem("on_drop_copper_ingot", "minecraft:copper_ingot", "On Drop Copper Ingot", on_item_drop="kill @s")
custom_shield = CustomItem("custom_shield", "minecraft:gray_dye", "Custom Shield", components=Components(blocks_attacks=BlocksAttacks(damage_reductions=[DamageReduction(["mob_attack", "arrow"])])))
custom_weapon = CustomItem("custom_weapon", "minecraft:diamond_sword", "Custom Weapon", components=Components(weapon=Weapon()))
overlay = CustomItem("custom_overlay", "minecraft:stone", "Custom Overlay", components=Components(equippable=Equippable(camera_overlay=CustomTexture("overlay", "images/overlay.png"))))

# invalid_component = CustomItem("invalid_component", "minecraft:sword", "Invalid Component", components=Components(map_data=MapData(map_id=1)))
# fish_bucket222 = CustomItem("minecraft:tropical_fish_bucket", "fish_bucket", "Fish Bucket", components=Components.from_list([BucketEntityData(bucket_variant_tag=TropicalFishData(size="large", pattern=1, body_color="light_blue", pattern_color="yellow"))]), ref_book_config=RefBookConfig(category=usable_category))
# test = CustomItem("minecraft:emerald", "test", "Test", components=Components.from_list([Equippable("chest")]), ref_book_config=RefBookConfig(category=weapons_category))

# edible_bow = CustomItem("minecraft:bow", "edible_bow", "Yummy Bow", components=Components(consumable=Consumable(0.5, "drink"), food=Food(5, 0, True)))
# edible_item = CustomItem("minecraft:witch_spawn_egg", "edible_witch_spawn_egg", "Edible Witch Spawn Egg", components=Components(consumable=Consumable(0.5, "drink"), food=Food(5, 0, True)))

custom_items = [
    ruby, topaz, weak_axe, flying_helmet, playable_lapis, musical_horn, written_book, rick_roll_horn,
    speedy_porkchop, unbreakable_axe, player_head, writable_book, sharpness_fish,  # lodestone_tracker
    enchantment_spruce_door, attribute_modified_axe, repairable_axe, slow_enderpearl_recharge,
    right_clickable_feather, right_clickable_nether_quartz, custom_head_texture, ray_gun, entity_finder,
    block_blocked_entity_finder,  # edible_item
    pre_charged_crossbow, steak_to_ruby_when_eaten, custom_firework, custom_firework_hex, map_with_decoration,
    colored_map, map_with_id, banner, note_block_sound_head, eating_gives_you_speed, eating_removes_speed,
    eating_teleports, eating_gives_you_speed_and_teleports, eating_plays_rick_roll, colorful_shield, bee_nest,
    bundle, filled_barrel, custom_potion, decorated_pot, death_protection_star, dyed_helmet, trimmed_leggings,
    suspicious_stew, spider_spawner, upper_slab, fish_bucket, loot_table_chest, on_drop_gold_ingot,
    on_drop_copper_ingot, custom_shield, custom_weapon, overlay,
]
# endregion
# ============================================================================================================
# region: Custom Tags
ruby_or_topaz_tag = CustomTag("ruby_or_topaz", [ruby, topaz], "item")
# endregion
# ============================================================================================================
# region: Custom Recipes
# Custom recipes
cobble_recipe = ShapelessCraftingRecipe("cobblestone_recipe", "minecraft:cobblestone", ["minecraft:stone", "minecraft:stick"], 2)
door_recipe = ShapelessCraftingRecipe("door_recipe", "minecraft:oak_door", ["minecraft:stick", ["minecraft:oak_planks", "minecraft:spruce_planks"]])
iron_helmet_recipe = ShapedCraftingRecipe("iron_helmet_recipe", "minecraft:iron_helmet", ["iii", "   ", "iii"], {"i": "minecraft:iron_ingot"})
burnable_diamond_recipe = FurnaceRecipe("burnable_diamond_recipe", "minecraft:diamond", "minecraft:charcoal", 1, 40)
smokable_redstone_recipe = SmokerRecipe("smokable_redstone_recipe", "minecraft:redstone", "minecraft:diamond", 100, 20)
lapis_campfire_recipe = CampfireRecipe("lapis_campfire_recipe", "minecraft:lapis_lazuli", "minecraft:cooked_beef", 100, 20)
ruby_recipe = ShapelessCraftingRecipe("ruby_recipe", ruby, ["minecraft:emerald", "minecraft:redstone"], recipe_category="equipment")
ruby_furnace_recipe = FurnaceRecipe("ruby_furnace_recipe", ruby, "minecraft:emerald", 1, 40)
moss_to_pale_recipe = StonecutterRecipe("moss_to_pale_recipe", "minecraft:pale_moss_block", "minecraft:moss_block")
ruby_stonecutter_recipe = StonecutterRecipe("ruby_stonecutter_recipe", ruby, "minecraft:redstone")
ruby_campfire_recipe = CampfireRecipe("ruby_campfire_recipe", ruby, "redstone", 100, 20)
ruby_smithing_tranform_recipe = SmithingTransformRecipe("ruby_transform_recipe", ruby, "gold_ingot", "iron_ingot", "redstone")
ruby_or_topaz_to_player_head = ShapelessCraftingRecipe("ruby_or_topaz_to_player_head", player_head, [ruby_or_topaz_tag])

recipes: list[Recipe] = [
    cobble_recipe, door_recipe, iron_helmet_recipe, burnable_diamond_recipe, smokable_redstone_recipe, lapis_campfire_recipe, ruby_recipe,
    ruby_furnace_recipe, moss_to_pale_recipe, ruby_stonecutter_recipe, ruby_campfire_recipe, ruby_smithing_tranform_recipe, ruby_or_topaz_to_player_head
]
# endregion
# ============================================================================================================
# region: Custom Blocks
ruby_ore = CustomItem("ruby_ore", "minecraft:redstone_ore", "Ruby Ore", texture_path="images/ruby_ore.png", ref_book_config=RefBookConfig(category=CUSTOM_BLOCKS_REF_BOOK_CATEGORY))
ruby_ore_block = CustomBlock.from_item(ruby_ore, drops=ruby)
# ruby_ore_slab = ruby_ore_block.create_slab("stone_slab")

topaz_ore = CustomItem("topaz_ore", "minecraft:gold_ore", "Topaz Ore", texture_path="images/topaz_ore.png", ref_book_config=RefBookConfig(category=CUSTOM_BLOCKS_REF_BOOK_CATEGORY))
topaz_ore_block = CustomBlock.from_item(topaz_ore, drops=SimpleRangeLootTable("topaz_ore_drops", topaz, 1, 4))

chocolate_block_item = CustomItem("chocolate_block", "dark_oak_log", "Chocolate Block", texture_path="images/chocolate_block/top_side.png", ref_book_config=RefBookConfig(category=CUSTOM_BLOCKS_REF_BOOK_CATEGORY))
faces = {"front": "side_side", "back": "side_side", "top": "top_side", "bottom": "top_side", "left": "long_side", "right": "long_side"}
chocolate_block = CustomBlock.from_item(chocolate_block_item, block_texture=FacePaths(**{key: f"images/chocolate_block/{value}.png" for key, value in faces.items()}, horizontally_rotatable=True, vertically_rotatable=False))

debug_block_item = CustomItem("debug_block", "sponge", "Debug Block", texture_path="images/debug_block/front.png", ref_book_config=RefBookConfig(category=CUSTOM_BLOCKS_REF_BOOK_CATEGORY))
faces_strings = ["front", "back", "top", "bottom", "left", "right"]
debug_block = CustomBlock.from_item(debug_block_item, block_texture=FacePaths(**{item: f"images/debug_block/{item}.png" for item in faces_strings}, horizontally_rotatable=True, vertically_rotatable=True))

custom_blocks = [ruby_ore_block, topaz_ore_block, chocolate_block, debug_block, ]  # ruby_ore_slab
# endregion
# ============================================================================================================
# region: Custom Loot Tables
emerald_loot_table = CustomLootTable("emerald_loot_table", [SimpleRangePool("emerald", 1, 3)])
# ruby_loot_table = CustomLootTable("ruby_loot_table", [SimpleRangePool(ruby, 1, 3)])
glider_helmet_loot_table = CustomLootTable("glider_helmet_loot_table", [SingleItemPool(flying_helmet)])
loot_tables = [emerald_loot_table, glider_helmet_loot_table]
# endregion
# ============================================================================================================
# region: Custom Item Render Definitions
blue_sword = CustomItemRenderDefinition("blue_sword", ModelItemModel("minecraft:item/iron_sword", tints=[ConstantTint((0.0, 0.0, 1.0))]), showcase_item="iron_sword")
hold_model = CustomItemRenderDefinition("hold_model", ConditionalItemModel(
        SelectedConditional(),
        true_model=ModelItemModel("minecraft:item/iron_sword", tints=[ConstantTint((0.0, 1.0, 0.0))]),
        false_model=ModelItemModel("minecraft:item/iron_sword", tints=[ConstantTint((1.0, 0.0, 0.0))]),
    ),
    showcase_item="iron_sword"
)
composite_model = CustomItemRenderDefinition("composite_model", CompositeItemModel(
        models=[
            ModelItemModel("minecraft:block/oak_pressure_plate"),
            ModelItemModel("minecraft:item/beef"),
        ],
    ),
    showcase_item="acacia_door"
)
empty_model = CustomItemRenderDefinition("empty_model", EmptyItemModel(), showcase_item="acacia_door")
hand_model = CustomItemRenderDefinition("hand_model", SelectItemModel(property_to_satisfy=MainHandSelectProperty(), cases=[
        SelectCase(when="left", model="item/diamond_sword"), SelectCase(when="right", model="item/wooden_sword"),
    ]),
    showcase_item="golden_sword",
)
range_dispatch = CustomItemRenderDefinition(
    "range_dispatch",
    RangeDispatchItemModel(
        property_to_satisfy=DamageRangeDispatchProperty(normalize=True),
        entries={
            0.8: ModelItemModel("item/diamond_sword"),
        },
        fallback_model="item/wooden_sword",
    ),
    showcase_item="golden_sword",
)
bundle_model = CustomItemRenderDefinition("bundle_model", BundleSelectedItemModel(), showcase_item="bundle")
special_model = CustomItemRenderDefinition("special_model", SpecialItemModel(
    ShulkerBoxSpecialItemModelType(texture="minecraft:shulker_green", openness=0.3, orientation="up"),
    base="minecraft:block/copper_bulb"), showcase_item="acacia_sign",
)
fire_aspect_sword = CustomItemRenderDefinition(
    "fire_aspect_sword", ConditionalItemModel(
        ComponentConditional("enchantments", [{"enchantments": "minecraft:fire_aspect"}]),
        true_model=ModelItemModel("minecraft:item/golden_sword"),
        false_model=ModelItemModel("minecraft:item/diamond_sword"),
    ), showcase_item="minecraft:iron_sword",
)
custom_item_render_definitions = [blue_sword, hold_model, empty_model, composite_model, hand_model, range_dispatch, bundle_model, special_model, fire_aspect_sword]
# endregion
# ============================================================================================================
# region: Custom Enchants
give_arrow_function = MCFunction("give_arrow", commands=["give @a minecraft:arrow 1"])
custom_enchantment = CustomEnchantment(
    "give_item", "Give Item", "minecraft:quick_charge", "minecraft:crossbow", weight=10, max_level=1, min_cost_base=1, per_level_increase_min=10,
    max_cost_base=50, per_level_increase_max=0, anvil_cost=0, slots=["mainhand"], effects=[
        EnchantmentEntityEffect("minecraft:post_attack", RunFunctionEntityEffect(give_arrow_function),
                                enchanted="attacker", affected="attacker"),
    ],
)
custom_enchantments = [custom_enchantment]
# endregion
# ============================================================================================================
# region: Custom MCFunctions:
take_me_home = MCFunction("take_me_home", ["execute in overworld run tp @s 120 69 -46"])
# endregion
# ============================================================================================================
# region: World Generation
custom_structure_set = CustomStructureSet(
    "my_structure_set",
    {"minecraft:ancient_city": 1.0}
)
# ocean_monument_structure = CustomStructure(
#     "my_custom_structure",
#     "#minecraft:has_structure/ocean_monument",
#     entity_spawn_overrides=[
#         SpawnOverride(entity_name="minecraft:guardian", weight=1, min_count=2, max_count=4),
#         DisableSpawnOverrideCategory("axolotls"),
#         DisableSpawnOverrideCategory("underground_water_creature"),
#     ],
# )
custom_biome = CustomBiome("overworld_biome")
bee_explosion_structure = SingleCustomStructure(
    "bee_explosion_structure",
    "structures/bee_explosion.nbt",
    [custom_biome],
)
overworld_dimension = CustomDimension("overworld", "overworld", custom_biome)
my_little_house = SingleCustomStructure(
    "my_little_house_structure",
    "structures/my_little_house.nbt",
    [custom_biome],
)
# endregion
# ============================================================================================================
# region: Custom Dimensions
my_dimension = CustomDimension(
    "my_dimension", CustomDimensionType(
        "my_dimension_type", height=1024, logical_height=1024, minimum_y=0, coordinate_scale=1, ambient_light=0,  # Goes from 0-1024
    ),
    biome="minecraft:the_end", noise_settings="minecraft:amplified",  # Amplified overworld, but set in the nether
)

# endregion
# ============================================================================================================
# region: Custom Damage Type:
my_custom_damage_type = CustomDamageType(
    "halucination",
    translations=[DamageTypeTranslation("en_gb", "%s halucinated", "%s was made to halucinate by %s using %s", "%s halucinated whilst trying to escape %s")],
    exhaustion=0.0, scaling="never", effects="hurt", death_message_type="default",
)
# endregion
# ============================================================================================================
# region: Custom Crafter
custom_crafter = CustomCrafter(
    "my_custom_crafter", "My custom crafter", ShapedCraftingRecipe("custom_crafter_recipe", "air", ["C C", "C C", "CCC"], {"C": "minecraft:copper_ingot"}),
    recipes=[
        CustomCrafterRecipe("topaz_recipe", topaz, [
            ruby,  "",  ruby,
            ruby,  "",  ruby,
            ruby, ruby, ruby,
        ]),
        CustomCrafterRecipe("custom_crafting_for_base_chest", "minecraft:chest", [
            "#minecraft:planks", "#minecraft:planks", "#minecraft:planks",
            "#minecraft:planks", "",                  "#minecraft:planks",  # fmt: skip
            "#minecraft:planks", "#minecraft:planks", "#minecraft:planks"
        ]),
    ]
)
# endregion
# ============================================================================================================
# region: Custom Loop
# every_sixty_seconds = CustomLoop("every_sixty_seconds", 20 * 60, "playsound minecraft:ui.button.click block @a")
# endregion
# ============================================================================================================
# region: Custom Language
custom_languages = CustomLanguage.from_all_translation_keys(
    {
        "pypacks.item.ruby": {
            "en_gb": "Ruby", "fr_fr": "Rubis", "de_de": "Rubin", "es_es": "Rubí", "it_it": "Rubino", "pt_br": "Rubi", "nl_nl": "Robijn",
        },
        "pypacks.item.topaz": {
            "en_gb": "Topaz", "fr_fr": "Topaze", "de_de": "Topas", "es_es": "Topacio", "it_it": "Topazio", "pt_br": "Topázio", "nl_nl": "Topaas",
        },
    }
)
# endregion
# ============================================================================================================
# region: Custom Fonts
ttf_font = CustomAutoAssignedFont("ttf_font", [TTFFontProvider("ttf_font", "fonts/Monocraft.ttf", size=9)])
# endregion
# ============================================================================================================
# region: Custom Ore Generation
ruby_generation = CustomOreGeneration("ruby_generation", ruby_ore_block, chance_of_spawning_in_a_chunk=2)
# endregion
# ============================================================================================================
# region: Entity Variants
sand_cat = CatVariant("sand_cat", texture_path="images/sand_cat.png")
sand_chicken = ChickenVariant("sand_chicken", texture_path="images/sand_chicken.png")
sand_cow = CowVariant("sand_cow", texture_path="images/sand_cow.png")
sand_frog = FrogVariant("sand_frog", texture_path="images/sand_frog.png")
sand_pig = PigVariant("sand_pig", texture_path="images/sand_pig.png")
sand_wolf = WolfVariant("sand_wolf", wild_texture_path="images/sand_wolf.png", tame_texture_path="images/sand_wolf_tame.png", angry_texture_path="images/sand_wolf_angry.png")
entity_variants: list[EntityVariant] = [sand_pig, sand_cow, sand_chicken, sand_cat, sand_frog, sand_wolf]
# endregion
# ============================================================================================================
# region: Custom Item Definitions and Custom Models
# tick_model_definition = CustomModelDefinition("tick", subdirectories=["item"])
# tick_render_definition = CustomItemRenderDefinition("tick", "minecraft:gui/sprites/container/beacon/confirm", showcase_item="iron_sword")
# endregion
# ============================================================================================================
# region: Custom Tests
crafting_environment = AllOfEnvironment(
    "crafting_environment",
    definitions=[
        FunctionEnvironment("iron_block_crafting_recipe_environment"),
    ],
)
iron_block_crafting_recipe = CustomGameTest(
    "iron_block_crafting_recipe", crafting_environment, GameTestStructure("iron_block_crafting_structure", "structures/iron_block_crafting_recipe.nbt"),
    max_ticks=20, setup_ticks=20,
)
# endregion
# ============================================================================================================
datapack = Pack(
    name="PyPacks Testing", description="A cool datapack", namespace="pypacks_testing",
    pack_icon_path="pack_icon.png", world_name="PyPacksWorld",
    custom_recipes=recipes,
    custom_items=custom_items,
    custom_sounds=[custom_sound],
    custom_mcfunctions=[give_arrow_function, take_me_home],
    custom_paintings=[custom_painting],
    custom_jukebox_songs=[custom_jukebox_song],
    custom_blocks=custom_blocks,
    custom_loot_tables=loot_tables,
    custom_languages=custom_languages,
    # custom_model_definitions=[tick_model_definition],
    custom_item_render_definitions=[*custom_item_render_definitions],  # tick_render_definition],
    custom_enchantments=custom_enchantments,
    custom_dimensions=[my_dimension, overworld_dimension],
    custom_damage_types=[my_custom_damage_type],
    # custom_advancements=[eating_advancement],
    custom_crafters=[custom_crafter],
    custom_raycasts=[block_ray_cast, entity_ray_cast],
    custom_tags=[ruby_or_topaz_tag],
    # custom_loops=[every_sixty_seconds],
    custom_fonts=[ttf_font],
    custom_entity_variants=entity_variants,
    custom_game_tests=[iron_block_crafting_recipe],
    custom_test_environments=[crafting_environment],
    world_gen_resources=WorldGenResources(
        custom_structures=[bee_explosion_structure, my_little_house],
        custom_structure_sets=[custom_structure_set],
    ),
    custom_ore_generations=[ruby_generation],
    config=Config(warn_about_tags_with_custom_items=False),
).generate_pack()
