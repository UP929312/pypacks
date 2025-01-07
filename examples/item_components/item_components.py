# from pypacks import Pack, CustomItem, Components, CustomSound, CustomJukeboxSong
# from pypacks.resources.item_components import *  # type: ignore[import]

# # ============================================================================================================
# custom_sound = CustomSound("rick_roll", "sounds/rick_roll.ogg", 1.0, 1.0)
# custom_jukebox_song = CustomJukeboxSong(custom_sound.internal_name, "Rick Roll", custom_sound.ogg_path, 4, 5)
# # ============================================================================================================
# # region: Custom Items
# # Custom Items
# ruby = CustomItem("minecraft:emerald", "ruby", "&cSpecial &4Ruby", lore=["Custom &cRuby&f, ooh!"], texture_path="images/ruby.png")
# topaz = CustomItem("minecraft:redstone", "topaz", "Topaz", texture_path="images/topaz.png", components=Components(equippable=Equippable("chest")))
# weak_axe = CustomItem("minecraft:netherite_axe", "weak_axe", "Weak Axe", components=Components(durability=10, lost_durability=5))
# flying_helmet = CustomItem("minecraft:iron_helmet", "flying_helmet", "Flying Helmet", components=Components(glider=True, consumable=Consumable(0.5, "drink"), food=Food(5, 0, True), use_remainder=UseRemainder("minecraft:diamond", 2)))
# playable_lapis = CustomItem("minecraft:lapis_lazuli", "playable_lapis", "Playable Lapis", max_stack_size=99, rarity="epic", components=Components(jukebox_playable=JukeboxPlayable("pigstep", True)))
# musical_horn = CustomItem("minecraft:goat_horn", "musical_horn", "Musical Horn", components=Components(instrument=Instrument("minecraft:item.goat_horn.sound.5", "Custom description?", 5, 256)))
# rick_roll_horn = CustomItem("minecraft:goat_horn", "never_going_to_give_you_up", "Rick Roll", components=Components(instrument=Instrument(custom_sound, "Rick Roll", 5, 256)))
# rick_roll_horn_from_sound = CustomItem("minecraft:goat_horn", "never_going_to_give_you_up_from_sound", "Rick Roll From Sound", components=Components(instrument=Instrument(custom_sound, "Rick Roll From Sound", 3, 256)))
# written_book = CustomItem("minecraft:written_book", "already_written_in_book", "Written Book", components=Components(written_book_content=WrittenBookContent("Hello, World!", "Author", [[{"text": "abc\n"}, {"text": "def"}]])),)
# writable_book = CustomItem("minecraft:writable_book", "writable_book", "Writable Book", components=Components(writable_book_content=WritableBookContent(["Hello world"])))
# lodestone_tracker = CustomItem("minecraft:compass", "lodestone_tracker", components=Components(lodestone_tracker=LodestoneTracker(126, 68, -41)))
# speedy_porkchop = CustomItem("minecraft:porkchop", "speedy_porkchop", "Fast hand, extreme axe", components=Components(tool=Tool(2, 0, [ToolRule("#mineable/axe", 10)])))
# unbreakable_axe = CustomItem("minecraft:stone_axe", "unbreakable_axe", "Unbreakable Axe", components=Components(unbreakable=True))
# player_head = CustomItem("minecraft:player_head", "custom_player_head_skin", "My Skin", components=Components(player_head_username="Skezza"))
# sharpness_fish = CustomItem("minecraft:cod", "sharpness_fish", "Sharpness Fish", components=Components(enchantments={"sharpness": 5}))
# enchantment_spruce_door = CustomItem("minecraft:spruce_door", "shiny_door", "Shiny Door", components=Components(enchantment_glint_override=True))
# attribute_modified_axe = CustomItem("minecraft:wooden_axe", "attribute_modified_axe", "Attribute Modified Axe", components=Components(attribute_modifiers=[AttributeModifier(attribute_type="attack_damage", amount=10, operation="add_value", slot="mainhand")]))
# repairable_axe = CustomItem("minecraft:stone_axe", "repairable_axe", "Repairable Axe", components=Components(durability=1000, lost_durability=500, repair_cost=5, repaired_by=["minecraft:stone"]))
# slow_enderpearl_recharge = CustomItem("minecraft:ender_pearl", "slow_enderpearl_recharge", "Slow Enderpearl Recharge", components=Components(cooldown=Cooldown(10)))
# right_clickable_feather = CustomItem("minecraft:feather", "right_clickable_feather", "Right Clickable Feather", on_right_click="summon minecraft:arrow ^ ^ ^")
# right_clickable_nether_quartz = CustomItem("minecraft:quartz", "right_clickable_nether_quartz", "Right Clickable Nether Quartz", on_right_click="give @a grass_block", components=Components(cooldown=Cooldown(seconds=3)))
# custom_head_texture = CustomItem("minecraft:player_head", "custom_head_texture", "Custom Head Texture", components=Components(custom_head_texture="eyJ0ZXh0dXJlcyI6eyJTS0lOIjp7InVybCI6Imh0dHA6Ly90ZXh0dXJlcy5taW5lY3JhZnQubmV0L3RleHR1cmUvZjg3N2M5NTA5NTg3YjNiODhjOTI3Zjc0YWE2NjlhZTg3MjVhMTRmZjU1ZGY2ZGUwMDRjNDFlMjYxNzg1YTJmOCJ9fX0="))
# ray_gun = CustomItem("minecraft:blaze_rod", "ray_gun", "Ray Gun", on_right_click="function pypacks_testing:raycast/populate_start_ray")
# pre_charged_crossbow = CustomItem("minecraft:crossbow", "pre_charged_crossbow", "Pre Charged Crossbow", components=Components(loaded_projectiles=["minecraft:arrow", "minecraft:arrow", "minecraft:arrow"]))
# steak_to_ruby_when_eaten = CustomItem("minecraft:cooked_beef", "steak_to_ruby_when_eaten", "Steak to Ruby When Eat", components=Components(consumable=Consumable(0.5, "eat"), food=Food(5, 0, True), use_remainder=UseRemainder(ruby)))
# custom_firework = CustomItem("minecraft:firework_rocket", "custom_firework", "Custom Firework", components=Components(firework=Firework(flight_duration=3, explosions=[FireworkExplosion(shape="star", colors=[16711680, 65280], fade_colors=[255, 16776960], has_trail=True, has_twinkle=True)])))
# custom_firework_hex = CustomItem("minecraft:firework_rocket", "custom_firework_hex", "Custom Firework Hex", components=Components(firework=Firework(flight_duration=1, explosions=[FireworkExplosion(shape="large_ball", colors=[0xFF0000])])))
# map_with_decoration = CustomItem("minecraft:filled_map", "map_with_decoration", "Map With Decoration", components=Components(map_data=MapData(map_id=1, map_decorations=[MapDecoration("red_x", 120, -46, 0)])))
# colored_map = CustomItem("minecraft:filled_map", "colored_map", "Colored Map", components=Components(map_data=MapData(map_color=0x0000FF)))
# map_with_id = CustomItem("minecraft:filled_map", "map_with_id", "Map with ID", components=Components(map_data=MapData(map_id=1)))
# banner = CustomItem("minecraft:white_banner", "banner", "Banner", components=Components(banner_patterns=[BannerPattern("stripe_left", "red"), BannerPattern("stripe_bottom", "blue")]))
# edible_item = CustomItem("minecraft:witch_spawn_egg", "edible_witch_spawn_egg", "Edible Witch Spawn Egg", components=Components(consumable=Consumable(0.5, "drink"), food=Food(5, 0, True)))
# note_block_sound_head = CustomItem("minecraft:player_head", "note_block_sound_head", "Note Block Sound Head", components=Components(note_block_sound=custom_sound))
# eating_gives_you_speed = CustomItem("minecraft:cooked_rabbit", "eating_gives_you_speed", "Eating Gives You Speed", components=Components(consumable=Consumable(0.5, "eat", on_consume_effects=[PotionEffect("speed", 1, 20*10)]), food=Food(can_always_eat=True)))
# eating_removes_speed = CustomItem("minecraft:cooked_rabbit", "eating_removes_you_speed", "Eating Removes You Speed", components=Components(consumable=Consumable(0.5, "eat", on_consume_remove_effects=[PotionEffect("speed")]), food=Food(can_always_eat=True)))
# eating_teleports = CustomItem("minecraft:cooked_rabbit", "eating_teleports", "Eating Teleports", components=Components(consumable=Consumable(0.5, "eat", on_consume_teleport_diameter=5), food=Food(can_always_eat=True)))
# eating_gives_you_speed_and_teleports = CustomItem("minecraft:cooked_rabbit", "eating_gives_you_speed_and_teleports", "Eating Gives You Speed And Teleports", components=Components(consumable=Consumable(0.5, "eat", on_consume_effects=[PotionEffect("speed", 1, 20*10)], on_consume_teleport_diameter=10), food=Food(can_always_eat=True)))
# eating_plays_rick_roll = CustomItem("minecraft:cooked_cod", "eating_plays_rick_roll", "Eating Plays Rick Roll", components=Components(consumable=Consumable(0.5, "eat", consuming_sound=custom_sound), food=Food(can_always_eat=True)))
# colorful_shield = CustomItem("minecraft:shield", "colorful_shield", "Colorful Shield", components=Components(shield_base_color="red"))
# bee_nest = CustomItem("minecraft:bee_nest", "bee_nest", "Bee Nest", components=Components(bees=[Bee(), Bee(), Bee(), Bee()]))
# bundle = CustomItem("minecraft:bundle", "bundle", "Bundle", components=Components(bundle_contents=BundleContents({"minecraft:emerald": 5, ruby: 3})))

# custom_items = [
#     ruby, topaz, weak_axe, flying_helmet, playable_lapis, musical_horn, written_book, rick_roll_horn,
#     rick_roll_horn_from_sound, lodestone_tracker, speedy_porkchop, unbreakable_axe, player_head, writable_book,
#     sharpness_fish, enchantment_spruce_door, attribute_modified_axe, repairable_axe, slow_enderpearl_recharge,
#     right_clickable_feather, right_clickable_nether_quartz, edible_item, custom_head_texture, ray_gun,
#     pre_charged_crossbow, steak_to_ruby_when_eaten, custom_firework, custom_firework_hex, map_with_decoration,
#     colored_map, map_with_id, banner, note_block_sound_head, eating_gives_you_speed, eating_removes_speed,
#     eating_teleports, eating_gives_you_speed_and_teleports, eating_plays_rick_roll, colorful_shield, bee_nest,
#     bundle,
# ]
# # endregion
# # ============================================================================================================

# pack = Pack(
#     "Item Components", "A cool pack", "item_components", "pack_icon.png", world_name="ItemComponents",
#     custom_items=custom_items,
#     custom_sounds=[custom_sound],
#     custom_jukebox_songs=[custom_jukebox_song],
# )
