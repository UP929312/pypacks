from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

from pypacks.resources.custom_item import CustomItem
from pypacks.resources.item_components import CustomItemData, WrittenBookContent
from pypacks.utils import chunk_list

if TYPE_CHECKING:
    from pypacks.datapack import Datapack

ICONS_PER_ROW = 6
ROWS_PER_PAGE = 5
# \n has to be \\n
# \uE<x><x><x> has to be \\uE<x><x><x>
# https://github.com/Stoupy51/python_datapack/blob/main/src/python_datapack/manual/main.py

@dataclass
class ItemIcon:
    unicode_char: str
    item: CustomItem | None
    # "hoverEvent": {"action": "show_text", "contents": ""}
    # "clickEvent": {"action": "change_page", "value": str(get_page_number(result_item))}
    # "clickEvent": {"action": "open_url", "value": str(get_page_number(result_item))}

    def get_json_data(self, datapack: "Datapack") -> dict[str, Any]:
        return_value = {
            "text": f"{self.unicode_char}{datapack.font_mapping['empty_1_x_1']}", "font": f"{datapack.namespace}:all_fonts",
            "color": "white", "underlined": False, "bold": False,
        }
        if self.item is not None:
            return_value["hoverEvent"] = {"action": "show_text", "contents": self.item.custom_name or self.item.base_item}
            return_value["clickEvent"] = {"action": "change_page", "value": "1"}
        return return_value

def generate_3_x_1_spacing(datapack: "Datapack") -> dict[str, Any]:
    return {"text": datapack.font_mapping['empty_1_x_1']+datapack.font_mapping['empty_1_x_1']+datapack.font_mapping['empty_1_x_1'],
            "color": "white", "underlined": False, "bold": False, "font": f"{datapack.namespace}:all_fonts"}

def generate_backslash_n_twice() -> dict[str, Any]:
    return {"text": "\n\n", "color": "white", "underlined": False, "bold": False, "font": "minecraft:default"}

@dataclass
class BookIconRow:
    icons: list[ItemIcon]

    def make_row(self, datapack: "Datapack") -> list[dict[str, str | bool]]:
        """Returns 3 single pixel spacers, 6 icons, and a double new-line"""
        if len(self.icons) < ICONS_PER_ROW:
            self.icons += [ItemIcon(datapack.font_mapping["icon_base"], None) for _ in range(6-len(self.icons))]
        icons = [
            generate_3_x_1_spacing(datapack),
            *[x.get_json_data(datapack) for x in self.icons],
            generate_backslash_n_twice()
        ]
        return icons

def generate_grid_page(datapack: "Datapack", title: str, custom_items: list[CustomItem]) -> list[dict[str, Any]]:
    items: list[ItemIcon] = [ItemIcon(datapack.font_mapping.get(item.item_id, datapack.font_mapping["unknown_icon"]), item)
                            for item in custom_items]
    elements = [{"text": title+"\n\n", "underlined": True, "bold": True}]
    groups_of_six = chunk_list(items, ICONS_PER_ROW)
    for group_of_six in groups_of_six:
        elements.extend(BookIconRow(group_of_six).make_row(datapack))
    for _ in range(ROWS_PER_PAGE-len(groups_of_six)):
        elements.extend(BookIconRow([]).make_row(datapack))
    return elements


class ReferenceBook:
    def __init__(self, items: list[CustomItem]) -> None:
        self.items = items

    def add_index(self, title: str) -> None:
        pass

    def generate_cover_page(self, datapack: "Datapack") -> list[dict[str, str | bool]]:
        return [
            {"text": f"{datapack.name} Reference Book"+"\n\n", "underlined": True},
            {"text": datapack.font_mapping["logo"], "color": "white", "underlined": False, "bold": False, "font": f"{datapack.namespace}:all_fonts"},
        ]

    def _(self) -> None:
        # CURRENT PLAN:
        # Have a mapping of icon_name -> unicode_char, e.g. "ruby" -> "\\uE006"
        # That way we can reference them nicely.
        # \\uE000 = Empty 16x16
        # \\uE001 = Empty 8x8
        # \\uE002 = Empty 4x4
        # \\uE003 = Empty 2x2
        # \\uE004 = Empty 1x1
        # \\uE005 = Test image
        # \\uE006 = Test icon (ruby)
        # 6(icon+spacer = 20) = 120
        # 3 pixels of space, 6 (icon+spacer), new line
        # /give @p written_book[written_book_content={"title": "abc", "author": "Title", "pages": ['[{"text": "Testing\\n"}, {"text": "Testing\\n"}, {text: "\\uE004\\uE004\\uE004\\uE006\\uE004\\uE006\\uE004\\uE006\\uE004\\uE006\\uE004\\uE006\\uE004\\uE006\\uE004", color: "white", font: "pypacks_testing:test_font_image"}]']}]
        # /give @p written_book[written_book_content={"title": "abc", "author": "Title", "pages": ['[{"text": "Testing\\n"}, {"text": "Testing\\n"}, {text: "\\uE004\\uE004\\uE004\\uE006\\uE004\\uE006\\uE004\\uE006\\uE004\\uE006\\uE004\\uE006\\uE004\\uE006\\uE004", color: "white", font: "pypacks_testing:test_font_image"}]']}]
        pass

    def generate_item(self, datapack: "Datapack") -> "CustomItem":
        cover_page = self.generate_cover_page(datapack)
        page = generate_grid_page(datapack, "Item list:", self.items)

        custom_data = CustomItemData(written_book_content=WrittenBookContent(f"{datapack.name} Reference Book", "PyPacks", [cover_page, page]))
        return CustomItem("minecraft:written_book", f"{datapack.name}_reference_book", additional_item_data=custom_data)

    def generate_give_command(self, datapack: "Datapack", namespace: str) -> str:
        return self.generate_item(datapack).generate_give_command(datapack, namespace)