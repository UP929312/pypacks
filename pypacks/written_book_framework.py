from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

from pypacks.resources.item_components import CustomItemData, WrittenBookContent
from pypacks.resources.custom_recipe import *  # type: ignore
from pypacks.utils import chunk_list

if TYPE_CHECKING:
    from pypacks.datapack import Datapack
    from pypacks.resources.custom_item import CustomItem

ICONS_PER_ROW = 5
ROWS_PER_PAGE = 4
PIXELS_PER_WIDTH = 113

ICON_ROW_INDENT = 2

# \n has to be \\n
# \uE<x><x><x> has to be \\uE<x><x><x>
# https://github.com/Stoupy51/python_datapack/blob/main/src/python_datapack/manual/main.py
# https://minecraft.fandom.com/wiki/Raw_JSON_text_format#Java_Edition

# =======================================================================================================================================


@dataclass
class OnClickChangePage:
    page_to_change_to: int

    def get_json_data(self) -> dict[str, Any]:
        return {"clickEvent": {"action": "change_page", "value": str(self.page_to_change_to)}}


@dataclass
class OnClickRunCommand:
    command: str
    datapack: "Datapack"

    def get_json_data(self) -> dict[str, Any]:
        return {"clickEvent": {"action": "run_command", "value": self.command}}


@dataclass
class OnHoverShowText:
    text: str
    font: str = "minecraft:default"

    def get_json_data(self) -> dict[str, Any]:
        return {"hoverEvent": {"action": "show_text", "contents": {"text": self.text, "color": "white", "font": self.font}}}


@dataclass
class OnHoverShowItem:
    custom_item: "CustomItem"
    datapack_namespace: str

    def get_json_data(self) -> dict[str, Any]:\
        return {"hoverEvent": {"action": "show_item", "contents": {"id": self.custom_item.base_item, "components": self.custom_item.to_dict(self.datapack_namespace)}}}


# =======================================================================================================================================


@dataclass
class Row:
    elements: list["Text | Icon"]
    indent_unicode_char: str = ""
    font_namespace: str = ""

    def get_json_data(self) -> list[dict[str, Any]]:
        regular_icons = [x.get_json_data() for x in self.elements]
        initial_padding = {
            "text": (self.indent_unicode_char*ICON_ROW_INDENT), "color": "white",
            "underlined": False, "bold": False, "font": f"{self.font_namespace}:all_fonts"}
        return [initial_padding, *regular_icons]


@dataclass
class FilledRow:
    elements: list["Text | Icon"]
    indent_unicode_char: str = ""
    font_namespace: str = ""
    empty_icon_unicode_char: str | None = None
    row_length: int = 0

    def get_json_data(self) -> list[dict[str, Any]]:
        icons = [x for x in self.elements]
        if len(icons) < self.row_length and self.empty_icon_unicode_char is not None:
            icons += [Icon(self.empty_icon_unicode_char, self.font_namespace, self.indent_unicode_char)]*(self.row_length-len(self.elements))
        initial_padding = {
            "text": (self.indent_unicode_char*ICON_ROW_INDENT), "color": "white",
            "underlined": False, "bold": False, "font": f"{self.font_namespace}:all_fonts"
        }
        return [initial_padding, *[x.get_json_data() for x in icons]]


@dataclass
class RowManager:
    icons: list["Icon"]
    row_length: int = ICONS_PER_ROW
    indent_unicode_char: str = ""
    font_namespace: str = ""
    empty_icon_unicode_char: str | None = None
    # back_button_unicode_char: str | None = None

    def __post_init__(self) -> None:
        self.rows: list[Row | FilledRow] = []
        chunked_elements = chunk_list(self.icons, self.row_length)
        self.rows.extend([
            FilledRow(icon_group, self.indent_unicode_char, self.font_namespace, self.empty_icon_unicode_char, row_length=ICONS_PER_ROW)
            for icon_group in chunked_elements
        ])
        empty_icon = Icon(self.empty_icon_unicode_char, self.font_namespace, self.indent_unicode_char)  # type: ignore
        self.rows.extend([
            Row([empty_icon]*ICONS_PER_ROW, self.indent_unicode_char, self.font_namespace)
            if self.empty_icon_unicode_char
            else Row([])
            for _ in range(self.row_length-len(chunked_elements))
        ])
        # if self.back_button_unicode_char:
        #     self.rows[-1].elements[-1] = Icon(self.back_button_unicode_char, self.font_namespace, self.indent_unicode_char, on_click=OnClickChangePage(0), on_hover=OnHoverShowText("Go back"))

    def get_json_data(self) -> list[list[dict[str, Any]]]:
        return [x.get_json_data() for x in self.rows]


@dataclass
class GridPage:
    title: "Text"
    empty_icon_unicode_char: str | None
    indent_unicode_char: str
    font_namespace: str
    icons: list["Icon"]
    icons_per_row: int = ICONS_PER_ROW
    rows_per_page: int = ROWS_PER_PAGE
    back_button_unicode_char: str | None = None
    back_button_page: int | None = None

    def __post_init__(self) -> None:
        assert len(self.icons) < (
            (self.icons_per_row*self.rows_per_page)-1 if self.back_button_page is not None else (self.icons_per_row*self.rows_per_page)
        ), "Too many icons for the grid"
        self.elements: list["Row | FilledRow"] = [Row([self.title])]
        row_manager = RowManager(self.icons, ICONS_PER_ROW, self.indent_unicode_char, self.font_namespace, self.empty_icon_unicode_char,
                                 # self.back_button_unicode_char,
                                )
        self.elements.extend(row_manager.rows)

        # if self.back_button_page is not None and self.back_button_unicode_char is not None:
        #     self.elements[-1].back_button = Icon(self.back_button_unicode_char, self.font_namespace, self.indent_unicode_char,
        #                                          on_click=OnClickChangePage(self.back_button_page),
        #                                          on_hover=OnHoverShowText("Go back"))

    def get_json_data(self) -> list[dict[str, Any]]:
        # Make it one layer flatter
        # For each row, add some new lines after it
        return_carriage = Row([Text("\n\n\n")]).get_json_data()
        elements = (
            [self.elements[0].get_json_data()+Row([Text("\n\n")]).get_json_data()]+
            [x.get_json_data()+return_carriage for x in self.elements[1:]]
        )
        # For each row, extract the elements and flatten
        return [item for pair in elements for item in pair]


@dataclass
class ElementPage:
    elements: list["Text | Icon"]

    def get_json_data(self) -> list[dict[str, Any]]:
        return [x.get_json_data() for x in self.elements]


# =======================================================================================================================================


@dataclass
class Icon:
    unicode_char: str
    font_namespace: str
    indent_unicode_char: str
    on_hover: OnHoverShowText | OnHoverShowItem | None = None
    on_click: OnClickChangePage | OnClickRunCommand | None = None

    def get_json_data(self) -> dict[str, Any]:
        return_value = {"text": f"{self.unicode_char}{self.indent_unicode_char}", "color": "white", "underlined": False, "bold": False, "font": f"{self.font_namespace}:all_fonts"}
        if self.on_hover:
            return_value |= self.on_hover.get_json_data()
        if self.on_click:
            return_value |= self.on_click.get_json_data()
        return return_value


@dataclass
class Text:
    text: str
    underline: bool = False
    bold: bool = False
    font: str = "minecraft:default"
    # succeeding_new_lines: int = 0

    def get_json_data(self) -> dict[str, Any]:
        return {"text": self.text, "color": "white" if self.font != "minecraft:default" else "black",
                "underlined": self.underline, "bold": self.bold, "font": self.font}


@dataclass
class RightAlignedIcon:
    unicode_char: str
    indent_unicode_char: str
    char_width: int
    font_namespace: str
    left_shift: int = 0  # If you want to move it slightly left?
    on_hover: OnHoverShowText | None = None
    on_click: OnClickChangePage | None = None

    def get_json_data(self) -> dict[str, Any]:
        padding = (PIXELS_PER_WIDTH-self.char_width)-self.left_shift
        return_value = {"text": (self.indent_unicode_char*padding)+f"{self.unicode_char}", "color": "white",
                        "underlined": False, "bold": False, "font": f"{self.font_namespace}:all_fonts"}
        if self.on_hover:
            return_value |= self.on_hover.get_json_data()
        if self.on_click:
            return_value |= self.on_click.get_json_data()
        return return_value


# =======================================================================================================================================


@dataclass
class FormattedWrittenBook:
    pages: list[ElementPage | GridPage]
    title: str
    author: str

    def generate_give_command(self, datapack: "Datapack") -> str:
        from pypacks.resources.custom_item import CustomItem

        custom_item_data = CustomItemData(written_book_content=WrittenBookContent(self.title, self.author, [x.get_json_data() for x in self.pages]))
        custom_item = CustomItem("minecraft:written_book", self.title, additional_item_data=custom_item_data)
        return custom_item.generate_give_command(datapack)
