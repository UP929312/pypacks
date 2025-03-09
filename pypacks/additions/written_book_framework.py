from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

from pypacks.additions.item_components import Components, WrittenBookContent
from pypacks.additions.text import Text
from pypacks.utils import chunk_list

if TYPE_CHECKING:
    from pypacks.additions.text import OnClickRunCommand, OnHoverShowItem, OnHoverShowTextRaw, OnClickChangePage, OnHoverShowText

ICONS_PER_ROW = 5
ROWS_PER_PAGE = 4
PIXELS_PER_WIDTH = 113
NEWLINES_BETWEEN_GRID_ROWS = 3

ICON_ROW_INDENT = 2


# =======================================================================================================================================


@dataclass
class Row:
    elements: list["Text | Icon"]
    indent_unicode_char: str = field(repr=False, default="")
    font_namespace: str = field(repr=False, default="")

    def get_json_data(self) -> list[dict[str, Any]]:
        regular_icons = [x.get_json_data() for x in self.elements]
        initial_padding = Text(self.indent_unicode_char*ICON_ROW_INDENT, color="white", underlined=False,
                               bold=False, font=f"{self.font_namespace}:all_fonts").to_dict()
        return [initial_padding, *regular_icons]


@dataclass
class FilledRow:
    elements: list["Text | Icon"]
    indent_unicode_char: str = field(repr=False, default="")
    font_namespace: str = field(repr=False, default="")
    empty_icon_unicode_char: str | None = field(repr=False, default=None)
    row_length: int = field(default=0)

    def get_json_data(self) -> list[dict[str, Any]]:
        icons = list(self.elements)  # Shallow copy
        if len(icons) < self.row_length and self.empty_icon_unicode_char is not None:
            icons += [Icon(self.empty_icon_unicode_char, self.font_namespace, self.indent_unicode_char, include_formatting=False)]*(self.row_length-len(self.elements))
        initial_padding = (
            Text(self.indent_unicode_char*ICON_ROW_INDENT, color="white", underlined=False,
                 bold=False, font=f"{self.font_namespace}:all_fonts").to_dict()
        ) if self.indent_unicode_char else {}
        return [initial_padding, *[x.get_json_data() for x in icons]]


@dataclass
class RowManager:
    """Takes any amount of icons and returns a list of `Row`s"""
    icons: list["Icon"]
    row_length: int = ICONS_PER_ROW
    indent_unicode_char: str = field(repr=False, default="")
    font_namespace: str = field(repr=False, default="")
    empty_icon_unicode_char: str | None = field(repr=False, default=None)
    trailing_new_lines: int = 0
    # back_button_unicode_char: str | None = None

    def __post_init__(self) -> None:
        empty_icon: "Icon | Text" = Icon(self.empty_icon_unicode_char, self.font_namespace, self.indent_unicode_char)  # type: ignore
        if self.empty_icon_unicode_char is None:
            empty_icon = Text("")
        inline_added_icons = [empty_icon]*(self.row_length-(len(self.icons) % self.row_length))
        chunked_elements = chunk_list(self.icons+inline_added_icons, self.row_length)

        self.rows: list[Row | FilledRow] = [
            FilledRow(icon_group, self.indent_unicode_char, self.font_namespace, self.empty_icon_unicode_char, row_length=self.row_length)
            for icon_group in chunked_elements
        ]
        if self.empty_icon_unicode_char:
            self.rows.extend([
                Row([empty_icon]*self.row_length, self.indent_unicode_char, self.font_namespace)
                for _ in range(self.row_length-len(chunked_elements))
            ])
        # Add in the newlines
        for row in self.rows[:-1]:
            row.elements.append(Text("\n"*self.trailing_new_lines))

        # if self.back_button_unicode_char:
        #     self.rows[-1].elements[-1] = Icon(self.back_button_unicode_char, self.font_namespace, self.indent_unicode_char, on_click=OnClickChangePage(0), on_hover=OnHoverShowText("Go back"))


# =======================================================================================================================================


@dataclass
class GridPage:
    title: "Text"
    empty_icon_unicode_char: str | None = field(repr=False)
    indent_unicode_char: str = field(repr=False)
    font_namespace: str = field(repr=False)
    icons: list["Icon"]
    icons_per_row: int = ICONS_PER_ROW
    rows_per_page: int = ROWS_PER_PAGE
    # back_button_unicode_char: str | None = field(repr=False, default=None)
    # back_button_page: int | None = field(repr=False, default=None)

    def __post_init__(self) -> None:
        self.back_button_page = None  # TEMP
        limit = (self.icons_per_row*self.rows_per_page)-1 if self.back_button_page is not None else (self.icons_per_row*self.rows_per_page)
        assert len(self.icons) <= limit, f"Too many icons for the grid, received {len(self.icons)} but can only have {limit} icons"
        row_manager = RowManager(
            self.icons, self.icons_per_row, self.indent_unicode_char, self.font_namespace, self.empty_icon_unicode_char, trailing_new_lines=NEWLINES_BETWEEN_GRID_ROWS,
        )
        # if self.back_button_page is not None and self.back_button_unicode_char is not None:
        #     self.elements[-1].back_button = Icon(self.back_button_unicode_char, self.font_namespace, self.indent_unicode_char,
        #                                          on_click=OnClickChangePage(self.back_button_page),
        #                                          on_hover=OnHoverShowText("Go back"))
        self.elements = row_manager.rows

    def get_json_data(self) -> list[dict[str, Any]]:
        title = Row([self.title, Text("\n\n")])
        elements = [x.get_json_data() for x in [title]+self.elements]
        return elements  # type: ignore[return-value]


@dataclass
class ElementPage:
    elements: list["Text | Icon"]

    def get_json_data(self) -> list[dict[str, Any]]:
        return [x.get_json_data() for x in self.elements]


@dataclass
class GridPageManager:
    title: str
    empty_icon_unicode_char: str | None
    indent_unicode_char: str
    font_namespace: str
    icons: list["Icon"]
    icons_per_row: int = ICONS_PER_ROW
    rows_per_page: int = ROWS_PER_PAGE
    # UNUSED:
    back_button_unicode_char: str | None = None
    back_button_page: int | None = None

    def __post_init__(self) -> None:
        icons_per_page = self.icons_per_row*self.rows_per_page
        self.pages = [
            GridPage(
                Text(self.title + (f", page {i}" if len(self.icons)//icons_per_page != 0 else ""), underlined=True, color="black"),
                self.empty_icon_unicode_char,
                self.indent_unicode_char,
                self.font_namespace,
                icons=page_icons,  # Here's the magic
                icons_per_row=self.icons_per_row,
                rows_per_page=self.rows_per_page,
                # back_button_unicode_char=self.back_button_unicode_char,
                # back_button_page=self.back_button_page
            )
            for i, page_icons in enumerate(chunk_list(self.icons, self.icons_per_row*self.rows_per_page), 1)
        ]


# =======================================================================================================================================


@dataclass
class Icon:
    """Simply represents one icon in the written book, i.e. a unicode character, with optional formatting and click/hover events,
    as well as as some right spacing"""
    unicode_char: str
    font_namespace: str = field(repr=False)
    indent_unicode_char: str = field(repr=False)
    include_formatting: bool = field(repr=False, default=True)
    right_indentation: int = field(repr=False, default=1)
    on_hover: "OnHoverShowText | OnHoverShowTextRaw | OnHoverShowItem | None" = field(repr=False, default=None)
    on_click: "OnClickChangePage | OnClickRunCommand | None" = field(repr=False, default=None)

    def get_json_data(self) -> dict[str, Any]:
        text = Text(f"{self.unicode_char}{self.indent_unicode_char*self.right_indentation}", color="white", font=f"{self.font_namespace}:all_fonts")
        if self.include_formatting:
            text.bold = False
            text.underlined = False
            text.color = "white"
        if self.on_hover:
            text.on_hover = self.on_hover
        if self.on_click:
            text.on_click = self.on_click
        return text.to_dict()


@dataclass
class RightAlignedIcon:
    unicode_char: str
    indent_unicode_char: str
    char_width: int
    font_namespace: str
    left_shift: int = 0  # If you want to move it slightly left?
    on_hover: "OnHoverShowText | None" = field(repr=False, default=None)
    on_click: "OnClickChangePage | None" = field(repr=False, default=None)

    def get_json_data(self) -> dict[str, Any]:
        padding = (PIXELS_PER_WIDTH-self.char_width)-self.left_shift
        # This is slightly hacky, but we reverse them so the padding goes on the left
        self.unicode_char, self.indent_unicode_char = self.indent_unicode_char, self.unicode_char
        return Icon(
            self.unicode_char*padding, self.font_namespace, indent_unicode_char=self.indent_unicode_char,
            on_hover=self.on_hover, on_click=self.on_click
        ).get_json_data()


# =======================================================================================================================================

@dataclass
class FormattedWrittenBook:
    pages: list[ElementPage | GridPage]
    title: str
    author: str

    def generate_give_command(self, pack_namespace: str) -> str:
        from pypacks.resources.custom_item import CustomItem

        custom_item_data = Components(written_book_content=WrittenBookContent(self.title, self.author, [x.get_json_data() for x in self.pages]))
        custom_item = CustomItem("formatted_written_book", "minecraft:written_book", components=custom_item_data)
        return custom_item.generate_give_command(pack_namespace)
