from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

from pypacks.resources.custom_item import CustomItem
from pypacks.resources.item_components import CustomItemData, WrittenBookContent
from pypacks.utils import chunk_list

if TYPE_CHECKING:
    from pypacks.datapack import Datapack

ICONS_PER_ROW = 5
ROWS_PER_PAGE = 4

LOGO_HORIZONTAL_SPACER = 6
ICON_ROW_INDENT = 2
# \n has to be \\n
# \uE<x><x><x> has to be \\uE<x><x><x>
# https://github.com/Stoupy51/python_datapack/blob/main/src/python_datapack/manual/main.py
# https://minecraft.fandom.com/wiki/Raw_JSON_text_format#Java_Edition

# =======================================================================================================================================

def generate_icon_row_spacing(datapack: "Datapack", pixels: int) -> dict[str, Any]:
    return {"text": "".join([datapack.font_mapping['empty_1_x_1'] for _ in range(pixels)]),
            "color": "white", "underlined": False, "bold": False, "font": f"{datapack.namespace}:all_fonts"}

def generate_backslashes(n: int) -> dict[str, Any]:
    return {"text": "".join(["\n" for _ in range(n)]), "color": "white", "underlined": False, "bold": False, "font": "minecraft:default"}

# =======================================================================================================================================

@dataclass
class ReferenceBookCategory:
    name: str
    image_path: str
    icon_image_bytes: bytes | None = None  # DON'T SET THIS MANUALLY

# =======================================================================================================================================

@dataclass(frozen=True)
class ItemIcon:
    unicode_char: str
    item: CustomItem | None
    # "hoverEvent": {"action": "show_text", "contents": ""}
    # "clickEvent": {"action": "change_page", "value": str(get_page_number(result_item))}
    # "clickEvent": {"action": "open_url", "value": str(get_page_number(result_item))}
    # "show_item": {"id": "minecraft:stone", "count": 1, "tag": {"display": {"Name": "Stone"}}}

    def get_json_data(self, datapack: "Datapack") -> dict[str, Any]:
        return_value = {
            "text": f"{self.unicode_char}{datapack.font_mapping['empty_1_x_1']}", "font": f"{datapack.namespace}:all_fonts",
            "color": "white", "underlined": False, "bold": False,
        }
        if self.item is not None:
            return_value["hoverEvent"] = {"action": "show_text", "contents": self.item.custom_name or self.item.base_item}
            return_value["clickEvent"] = {"action": "change_page", "value": "1"}
            # import json
            # return_value["hoverEvent"] = {"action": "show_item", "contents": {
            #     "id": self.item.base_item, "count": 1, "tag": json.dumps({"display": {"Name": self.item.custom_name or self.item.base_item}})
            # }}
        return return_value


# =======================================================================================================================================


@dataclass(frozen=True)
class CategoryIcon:
    unicode_char: str
    category_name: str

    def get_json_data(self, datapack: "Datapack") -> dict[str, Any]:
        return {
            "text": f"{self.unicode_char}{datapack.font_mapping['empty_1_x_1']}", "font": f"{datapack.namespace}:all_fonts",
            "color": "white", "underlined": False, "bold": False,
            "hoverEvent": {"action": "show_text", "contents": f"Go to the `{self.category_name}` category"},
        }


# =======================================================================================================================================


@dataclass
class GridPage:
    title: str
    icons: list[ItemIcon] | list[CategoryIcon]
    datapack: "Datapack"

    def __post_init__(self) -> None:
        elements = [{"text": self.title+"\n\n", "underlined": True, "bold": True}]
        groups_of_six = chunk_list(self.icons, ICONS_PER_ROW)
        for group_of_six in groups_of_six:
            elements.extend(self.make_row(self.datapack, group_of_six))
        for _ in range(ROWS_PER_PAGE-len(groups_of_six)):
            elements.extend(self.make_row(self.datapack, []))
        self.elements = elements

    def make_row(self, datapack: "Datapack", icons: list[ItemIcon], default_icon: str = "icon_base") -> list[dict[str, str | bool]]:
        """Takes a list of items to display only those (up to) ICONS_PER_ROW"""
        if len(icons) < ICONS_PER_ROW:
            icons += [ItemIcon(datapack.font_mapping[default_icon], None) for _ in range(ICONS_PER_ROW-len(icons))]
        return [
            generate_icon_row_spacing(datapack, ICON_ROW_INDENT),
            *[x.get_json_data(datapack) for x in icons],
            generate_backslashes(3)
        ]


# =======================================================================================================================================


class ReferenceBook:
    # /give @p written_book[written_book_content={"title": "abc", "author": "Title", "pages": ['[{"text": "Testing\\n"}, {"text": "Testing\\n"}, {text: "\\uE004\\uE004\\uE004\\uE006\\uE004\\uE006\\uE004\\uE006\\uE004\\uE006\\uE004\\uE006\\uE004\\uE006\\uE004", color: "white", font: "pypacks_testing:test_font_image"}]']}]

    def __init__(self, items: list[CustomItem]) -> None:
        self.items = items

    def generate_cover_page(self, datapack: "Datapack") -> list[dict[str, str | bool]]:
        logo_line = generate_icon_row_spacing(datapack, LOGO_HORIZONTAL_SPACER)
        logo_line["text"] += datapack.font_mapping["logo"]
        return [{"text": f"{datapack.name} Reference Book\n\n", "underlined": True}, logo_line] #  \\►
        # ► ▶  ➙ ➛ 	➜ ➝ ➞ ➟ ➠ ➡ ➢ ➣ ➤ ➥ ➦ ➨ ➩ ➪ ➫ ➬ ➭ ➮ ➯ ➱ ➲ ➳ ➴ ➵ ➶ ➷ ➸ ➹ ➺ ➻ ➼ ➽ ➾ 

    def generate_pages(self, datapack: "Datapack") -> list[list[dict[str, str | bool]]]:
        # Cover
        cover_page = self.generate_cover_page(datapack)

        # Categories
        category_page = GridPage("Categories", [
                CategoryIcon(datapack.font_mapping[f"{category.name.lower()}_category_icon"], category.name) for category in datapack.reference_book_categories
            ], datapack
        ).elements

        # Item page(s)
        item_icons = [ItemIcon(datapack.font_mapping[f"{item.item_id}_icon"], item) for item in datapack.custom_items]
        page = GridPage(f"Item list, page {'1'}", item_icons, datapack).elements

        return [cover_page, category_page, page]

    def generate_item(self, datapack: "Datapack") -> "CustomItem":
        pages = self.generate_pages(datapack)
        custom_data = CustomItemData(written_book_content=WrittenBookContent(f"{datapack.name} Reference Book", "PyPacks", pages))
        return CustomItem("minecraft:written_book", f"{datapack.name}_reference_book", additional_item_data=custom_data)

    def generate_give_command(self, datapack: "Datapack") -> str:
        return self.generate_item(datapack).generate_give_command(datapack)