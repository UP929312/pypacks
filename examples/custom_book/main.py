from pypacks import Datapack, CustomItem, Components
from pypacks.resources.item_components import WrittenBookContent
from pypacks.written_book_framework import FormattedWrittenBook

written_book = CustomItem("already_written_in_book", "minecraft:written_book", "Written Book", components=Components(
    written_book_content=WrittenBookContent(
        "t", "a", [[{"text": "abc\n"}, {"text": f"def\\uE000"}]])
    )
)

from pypacks.resources.item_components import WrittenBookContent
from pypacks.utils import to_component_string, _to_snbt

# a = WrittenBookContent("t", "a", [[{"text": "abc\n"}, {"text": "def\uE000, \uE0001"}]])
# print(a)
# b = a.to_dict()
# print(b)
# c = to_component_string(b)
# print(c)

dummy_datapack = Datapack("a", "b", "c")

from pypacks.reference_book_generator import ReferenceBook
ref_book = ReferenceBook([])
pages = [x.get_json_data() for x in ref_book.generate_pages(dummy_datapack)]
# print(pages)
written_book_contents = WrittenBookContent("t", "a", pages)
print(written_book_contents.to_dict())
custom_item_data = Components(written_book_content=written_book_contents)
custom_item = CustomItem("already_written_in_book", "minecraft:written_book", "Written Book", components=custom_item_data)
print(custom_item.generate_give_command(dummy_datapack))

# import os
# os.chdir(os.path.dirname(__file__))

# datapack = Datapack(
#     "Written Book", "???", "written_books",
#     custom_items=[written_book],
#     resource_pack_path=os.path.join(os.path.dirname(__file__), "resource_pack"),
#     datapack_output_path=os.path.join(os.path.dirname(__file__), "datapack")
# )