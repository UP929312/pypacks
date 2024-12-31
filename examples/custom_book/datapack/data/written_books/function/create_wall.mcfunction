fill ~ ~ ~ ~0 ~3 ~ stone_bricks
kill @e[tag=wall_item_frame]
summon minecraft:item_frame ~0 ~0 ~1 {Tags:[wall_item_frame], Item: {id: "minecraft:written_book", components: {'custom_name': '[{"text": "Written Book", "italic": false}]', 'written_book_content': {'title': 't', 'author': 'a', 'pages': ['[{"text": "abc\\n"}, {"text": "def\\ue000"}]']}}}, Facing: 3}