from pypacks import Pack, CustomItem, Components
from pypacks.additions.item_components import WrittenBookContent
from pypacks.additions.reference_book_generator import ReferenceBook
# from pypacks.written_book_framework import FormattedWrittenBook

written_book = CustomItem("already_written_in_book", "minecraft:written_book", "Written Book", components=Components(
    written_book_content=WrittenBookContent(
        "t", "a", [[{"text": "abc\n"}, {"text": "def\\uE000"}]])
    )
)

# IGNORE ALL THIS!!!! #####################

# from pypacks.utils import _to_snbt

# a = WrittenBookContent("t", "a", [[{"text": "abc\n"}, {"text": "def\uE000, \uE0001"}]])
# rint(a)
# b = a.to_dict()
# rint(b)
# rint(c)

dummy_datapack = Pack("a", "b", "c")

ref_book = ReferenceBook([])
pages = [x.get_json_data() for x in ref_book.generate_pages(dummy_datapack)]
# rint(pages)
written_book_contents = WrittenBookContent("t", "a", pages)
# rint(written_book_contents.to_dict())
custom_item_data = Components(written_book_content=written_book_contents)
custom_item = CustomItem("already_written_in_book", "minecraft:written_book", "Written Book", components=custom_item_data)
# rint(custom_item.generate_give_command(dummy_datapack.namespace))

# import os
# os.chdir(os.path.dirname(__file__))

# datapack = Datapack(
#     "Written Book", "???", "written_books",
#     custom_items=[written_book],
#     resource_pack_path=os.path.join(os.path.dirname(__file__), "resource_pack"),
#     datapack_output_path=os.path.join(os.path.dirname(__file__), "datapack")
# )
