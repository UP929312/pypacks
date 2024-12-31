from pypacks import Datapack, CustomItem, Components
from pypacks.resources.item_components import WrittenBookContent

written_book = CustomItem("already_written_in_book", "minecraft:written_book", "Written Book", components=Components(
    written_book_content=WrittenBookContent(
        "t", "a", [[{"text": "abc\n"}, {"text": f"def\uE000"}]])
    )
)

# Desired:
# give @p minecraft:written_book[custom_name="[{\"text\": \"Written Book\", \"italic\": false}]", written_book_content={"title": "t", "author": "a", "pages": ["[{'text': 'abc\\n'}, {'text': 'def\\ue000'}]"]}]
# "pages": ["[{'text': 'abc\\n'}, {'text': 'def\\ue000'}]"

from pypacks.resources.item_components import WrittenBookContent
from pypacks.utils import to_component_string, _to_snbt

a = WrittenBookContent("t", "a", [[{"text": "abc\n"}, {"text": "def\uE000"}]])
# print(a)
b = a.to_dict()
# print(b)
c = to_component_string(b)
# print(c)


import os
os.chdir(os.path.dirname(__file__))

datapack = Datapack(
    "Written Book", "???", "written_books",
    custom_items=[written_book],
    resource_pack_path=os.path.join(os.path.dirname(__file__), "resource_pack"),
    datapack_output_path=os.path.join(os.path.dirname(__file__), "datapack")
)