from dataclasses import dataclass, field
from typing import Any, TYPE_CHECKING

from pypacks.additions.item_components import Components, WrittenBookContent
from pypacks.additions.text import Text
from pypacks.utils import chunk_list

if TYPE_CHECKING:
    from pypacks.additions.text import OnClickRunCommand, OnClickChangePage, OnClickCopyToClipboard, OnHoverShowItem, OnHoverShowTextRaw, OnHoverShowText

ICONS_PER_ROW = 5
ROWS_PER_PAGE = 4
ICONS_PER_PAGE = ICONS_PER_ROW*ROWS_PER_PAGE
PIXELS_PER_WIDTH = 113
NEWLINES_BETWEEN_GRID_ROWS = 3

ICON_ROW_INDENT = 2


# =======================================================================================================================================


@dataclass
class Row:
    row_elements: list["Text | Icon"]
    indentation_spaces: int = 0
    trailing_new_lines: int = 0
    font_namespace: str = field(repr=False, default="")

    def get_json_data(self) -> list[dict[str, Any]]:
        regular_icons = [x.get_json_data() for x in self.row_elements]
        initial_padding = Text(" "*self.indentation_spaces, color="white", underlined=False, bold=False, font=f"{self.font_namespace}:all_fonts").to_dict()
        if self.indentation_spaces:
            regular_icons = [initial_padding, *regular_icons]
        if self.trailing_new_lines:
            regular_icons.append(Text("\n"*self.trailing_new_lines).to_dict())
        return regular_icons


@dataclass
class FilledRow:
    """Similar to a Row, but if it's not full, it fills the rest with empty icons"""
    row_elements: list["Text | Icon"]
    empty_icon: "Icon" = field(repr=False)
    indentation_spaces: int = 0
    trailing_new_lines: int = 0
    row_length: int = field(default=0)
    font_namespace: str = field(repr=False, default="")

    def get_json_data(self) -> list[dict[str, Any]]:
        icons = list(self.row_elements)  # Shallow copy
        required_blanks = self.row_length-len(icons)
        return Row(
            row_elements=icons+([self.empty_icon]*required_blanks), indentation_spaces=self.indentation_spaces,
            trailing_new_lines=self.trailing_new_lines, font_namespace=self.font_namespace
        ).get_json_data()


@dataclass
class RowManager:
    """Takes any amount of icons and returns a list of `Row`s, with each row containing `row_length` icons (splits x items in n rows)"""
    icons: list["Icon"]
    row_length: int = ICONS_PER_ROW
    font_namespace: str = field(repr=False, default="")
    empty_icon: "Icon | None" = field(repr=False, default=None)
    trailing_new_lines: int = 0

    def __post_init__(self) -> None:
        self.rows: list[Row | FilledRow] = [
            (
                FilledRow(row_elements=icon_group, trailing_new_lines=self.trailing_new_lines,
                          empty_icon=self.empty_icon, row_length=self.row_length, font_namespace=self.font_namespace)
                #
                if self.empty_icon is not None else
                #
                Row(row_elements=icon_group, trailing_new_lines=self.trailing_new_lines, font_namespace=self.font_namespace)
            )
            for icon_group in chunk_list(self.icons, self.row_length)  # Splits up the icons into groups
        ]


# =======================================================================================================================================


@dataclass
class GridPage:
    """Takes a title and between 1 and <20> icons, splits them up into rows and fills the rest with empty icons"""
    title: "Text"
    empty_icon_unicode_char: str = field(repr=False)
    font_namespace: str = field(repr=False)
    icons: list["Icon"]
    icons_per_row: int = ICONS_PER_ROW
    rows_per_page: int = ROWS_PER_PAGE

    def __post_init__(self) -> None:
        limit = self.icons_per_row*self.rows_per_page
        assert len(self.icons) <= limit, f"Too many icons for the grid, received {len(self.icons)} but can only have {limit} icons"
        #
        empty_icon = Icon(self.empty_icon_unicode_char, self.font_namespace)
        row_manager = RowManager(
            icons=self.icons, row_length=self.icons_per_row, font_namespace=self.font_namespace,
            empty_icon=empty_icon, trailing_new_lines=NEWLINES_BETWEEN_GRID_ROWS,
        )
        if len(row_manager.rows) < self.rows_per_page:
            row_manager.rows.extend(
                [
                    FilledRow([], empty_icon=empty_icon, row_length=self.icons_per_row, trailing_new_lines=NEWLINES_BETWEEN_GRID_ROWS)
                ] * (self.rows_per_page-len(row_manager.rows))
            )
        self.elements = row_manager.rows

    def get_json_data(self) -> list[Any]:
        # Force the title to be black and not underlined (and add \n\n)
        self.title.update_attributes(text=self.title.text+"\n\n", color="black", underlined=False)
        return [x.get_json_data() for x in [self.title]+self.elements]


@dataclass
class ElementPage:
    elements: list["Text | Icon"]

    def get_json_data(self) -> list[dict[str, Any]]:
        return [x.get_json_data() for x in self.elements]


@dataclass
class GridPageManager:
    title: str
    empty_icon_unicode_char: str
    font_namespace: str
    icons: list["Icon"]
    icons_per_row: int = ICONS_PER_ROW
    rows_per_page: int = ROWS_PER_PAGE

    def __post_init__(self) -> None:
        icons_per_page = self.icons_per_row*self.rows_per_page
        self.pages = [
            GridPage(
                Text(self.title + (f", page {i}" if len(self.icons)//icons_per_page != 0 else ""), underlined=True, color="black"),
                empty_icon_unicode_char=self.empty_icon_unicode_char,
                font_namespace=self.font_namespace,
                icons=page_icons,  # Here's the magic
                icons_per_row=self.icons_per_row,
                rows_per_page=self.rows_per_page,
            )
            for i, page_icons in enumerate(chunk_list(self.icons, self.icons_per_row*self.rows_per_page), 1)
        ]


# =======================================================================================================================================


@dataclass
class Icon:
    """Simply represents one icon in the written book, i.e. a unicode character, with optional formatting and click/hover events,
    as well as as some left-right spacing"""
    unicode_char: str
    font_namespace: str = field(repr=False)
    left_padding: int = field(repr=False, default=0)
    right_padding: int = field(repr=False, default=1)
    on_hover: "OnHoverShowText | OnHoverShowTextRaw | OnHoverShowItem | None" = field(repr=False, default=None)
    on_click: "OnClickChangePage | OnClickRunCommand | OnClickCopyToClipboard | None" = field(repr=False, default=None)

    def get_json_data(self) -> dict[str, Any]:
        return [  # type: ignore[return-value]
            Text(' '*self.left_padding, font=f"{self.font_namespace}:all_fonts", bold=False, underlined=False).to_dict(),
            Text(
                self.unicode_char, color="white", font=f"{self.font_namespace}:all_fonts",
                bold=False, underlined=False, on_hover=self.on_hover, on_click=self.on_click
            ).to_dict(),
            Text(' '*self.right_padding, font=f"{self.font_namespace}:all_fonts", bold=False, underlined=False).to_dict(),
        ]


@dataclass
class RightAlignedIcon:
    unicode_char: str
    font_namespace: str
    char_width: int = 1
    left_shift: int = 0  # To slightly shift it back left
    on_hover: "OnHoverShowText | None" = field(repr=False, default=None)
    on_click: "OnClickChangePage | None" = field(repr=False, default=None)

    def get_json_data(self) -> dict[str, Any]:
        return Icon(
            self.unicode_char, self.font_namespace,
            left_padding=PIXELS_PER_WIDTH-self.char_width-self.left_shift, right_padding=0,
            on_hover=self.on_hover, on_click=self.on_click,
        ).get_json_data()


# =======================================================================================================================================

@dataclass
class FormattedWrittenBook:
    pages: list["ElementPage | GridPage"]
    title: str
    author: str

    def generate_give_command(self, pack_namespace: str) -> str:
        from pypacks.resources.custom_item import CustomItem

        custom_item_data = Components(written_book_content=WrittenBookContent(self.title, self.author, [x.get_json_data() for x in self.pages]))
        custom_item = CustomItem("formatted_written_book", "minecraft:written_book", components=custom_item_data)
        return custom_item.generate_give_command(pack_namespace)
