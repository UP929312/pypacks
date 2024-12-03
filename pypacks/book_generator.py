from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

from pypacks.resources.item_components import CustomItemData, WrittenBookContent
from pypacks.resources.custom_recipe import SmithingTrimRecipe
from pypacks.utils import PYPACKS_ROOT, chunk_list, remove_colour_codes

if TYPE_CHECKING:
    from pypacks.datapack import Datapack
    from pypacks.resources.custom_item import CustomItem
    from pypacks.resources.custom_recipe import Recipe

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
    return {"text": f"{datapack.font_mapping['empty_1_x_1']}"*pixels,
            "color": "white", "underlined": False, "bold": False, "font": f"{datapack.namespace}:all_fonts"}

def generate_backslashes(n: int) -> dict[str, Any]:
    return {"text": "\n"*n, "color": "white", "underlined": False, "bold": False, "font": "minecraft:default"}

# =======================================================================================================================================

@dataclass
class ReferenceBookCategory:
    name: str
    image_path: str
    icon_image_bytes: bytes | None = None  # DON'T SET THIS MANUALLY

    def __post_init__(self) -> None:
        assert " " not in self.name, "Category name cannot contain spaces"


@dataclass
class GenericIcon:
    unicode_char: str
    hover_text: str | None = None
    go_to_page: int | None = None

    def get_json_data(self, datapack: "Datapack") -> dict[str, Any]:
        return_value = self.generate_icon(self.unicode_char, datapack)
        if self.hover_text is not None:
            return_value |= {"hoverEvent": {"action": "show_text", "contents": self.hover_text}}
        if self.go_to_page is not None:
            return_value |= {"clickEvent": {"action": "change_page", "value": str(self.go_to_page)}}
        return return_value
        # import json
        # return_value["hoverEvent"] = {"action": "show_item", "contents": {
        #     "id": self.item.base_item, "count": 1, "tag": json.dumps({"display": {"Name": self.item.custom_name or self.item.base_item}})
        # }}
    
    @staticmethod
    def generate_icon(unicode_char: str, datapack: "Datapack") -> dict[str, Any]:
        return {"text": f"{unicode_char}{datapack.font_mapping['empty_1_x_1']}", "font": f"{datapack.namespace}:all_fonts",
                "color": "white", "underlined": False, "bold": False}


@dataclass
class MoreInfoIcon(GenericIcon):
    item: "CustomItem" = None  # type: ignore[assignment]

    def get_json_data(self, datapack: "Datapack") -> dict[str, Any]:
        hover_content = f"More info about {remove_colour_codes(self.item.custom_name or self.item.base_item)}:\n\n"
        hover_content += self.item.reference_book_description if self.item.reference_book_description else "No description available"
        hover_data = {"hoverEvent": {"action": "show_text", "contents": hover_content}}
        data = super().get_json_data(datapack) | hover_data
        return data
        # https://www.planetminecraft.com/blog/showing-hover-event-items-in-written-books/


@dataclass
class RecipeIcon(GenericIcon):
    recipe: "Recipe" = None  # type: ignore[assignment]

    def get_json_data(self, datapack: "Datapack") -> dict[str, Any]:
        # hover_content = f"Recipe for {remove_colour_codes(self.recipe.result.custom_name or self.recipe.result.base_item)}:\n\n"
        hover_content = ""
        hover_data = {"hoverEvent": {"action": "show_text", "contents": hover_content}}
        data = super().get_json_data(datapack) | hover_data
        return data

# =======================================================================================================================================


@dataclass
class ItemPage:
    item: "CustomItem"
    datapack: "Datapack"
    back_button_page: int

    def get_title(self) -> dict[str, Any]:
        return {
            "text": f"{remove_colour_codes(self.item.custom_name or self.item.base_item)}", "underlined": True, "bold": True,
            "hoverEvent": {"action": "show_item", "contents": {
                "id": self.item.base_item, "components": self.item.to_dict(self.datapack),
            }},
            "clickEvent": {"action": "run_command", "value": f"/function {self.datapack.namespace}:give/{self.item.internal_name}"},
        }

    def generate_page(self) -> list[dict[str, Any]]:
        from pypacks.resources.custom_item import CustomItem

        title: dict[str, Any] = self.get_title()
        # Get all the ways to craft it
        non_smithing_trim_recipes = [x for x in self.datapack.custom_recipes if not isinstance(x, SmithingTrimRecipe)]
        recipes = [x for x in non_smithing_trim_recipes if (
            x.result.internal_name if isinstance(x.result, CustomItem) else x.result  # type: ignore[attr-defined]
        ) == self.item.internal_name]
        # obtain_methods = [RecipeIcon(self.datapack.font_mapping["crafting_icon"], recipe=x) for x in recipes]
        obtain_methods = False
        obtain_method_data = [{"text": f"Found recipe!", "underlined": False, "bold": False}] if obtain_methods else [{"text": f"No recipe found!", "underlined": False, "bold": False}]
        
        give_item_icon = GenericIcon(self.datapack.font_mapping[f"{self.item.internal_name}_icon"])
        more_info_icon = MoreInfoIcon(self.datapack.font_mapping["more_info_icon"], item=self.item)

        return [
            title,
            generate_backslashes(2),
            give_item_icon.get_json_data(self.datapack),
            generate_backslashes(2),
            *obtain_method_data,
            generate_backslashes(2),
            generate_icon_row_spacing(self.datapack, 2), more_info_icon.get_json_data(self.datapack),
            generate_backslashes(3),
            generate_icon_row_spacing(self.datapack, 90), RedirectButton(self.datapack.font_mapping["satchel_icon"], "Go to the categories page", self.back_button_page).get_json_data(self.datapack),
        ]


# =======================================================================================================================================


@dataclass
class RedirectButton(GenericIcon):
    """A generic redirect button that can be used to go to a different page"""
    # "hoverEvent": {"action": "show_text", "contents": ""}
    # "clickEvent": {"action": "change_page", "value": str(get_page_number(result_item))}
    # "clickEvent": {"action": "open_url", "value": str(get_page_number(result_item))}
    # "show_item": {"id": "minecraft:stone", "count": 1, "tag": {"display": {"Name": "Stone"}}}


# =======================================================================================================================================


@dataclass
class GridPage:
    title: str
    icons: list[RedirectButton]
    datapack: "Datapack"
    back_button_page: int | None = None

    def __post_init__(self) -> None:
        elements: list[dict[str, Any]] = [{"text": self.title+"\n\n", "underlined": True, "bold": True}]
        groups_of_six = chunk_list(self.icons, ICONS_PER_ROW)
        for i, group_of_six in enumerate(groups_of_six):
            elements.extend(self.make_row(self.datapack, group_of_six, row_index=i))
        for i in range(ROWS_PER_PAGE-len(groups_of_six)):
            elements.extend(self.make_row(self.datapack, [], row_index=len(groups_of_six)+i))
        self.elements = elements

    def make_row(self, datapack: "Datapack", icons: list[RedirectButton], row_index: int, default_icon: str = "icon_base") -> list[dict[str, str | bool]]:
        """Takes a list of items to display only those (up to) ICONS_PER_ROW"""
        if len(icons) < ICONS_PER_ROW:
            icons += [RedirectButton(datapack.font_mapping[default_icon], "", None) for _ in range(ICONS_PER_ROW-len(icons))]
        if self.back_button_page is not None and row_index == ROWS_PER_PAGE-1:
            GO_TO_CATEGORIES_BUTTON = RedirectButton(datapack.font_mapping["satchel_icon"], "Go to the categories page", self.back_button_page)
            icons[-1] = GO_TO_CATEGORIES_BUTTON
        return [
            generate_icon_row_spacing(datapack, ICON_ROW_INDENT),
            *[x.get_json_data(datapack) for x in icons],
            generate_backslashes(3)
        ]


# =======================================================================================================================================


class ReferenceBook:
    # /give @p written_book[written_book_content={"title": "abc", "author": "Title", "pages": ['[{"text": "Testing\\n"}, {"text": "Testing\\n"}, {text: "\\uE004\\uE004\\uE004\\uE006\\uE004\\uE006\\uE004\\uE006\\uE004\\uE006\\uE004\\uE006\\uE004\\uE006\\uE004", color: "white", font: "pypacks_testing:test_font_image"}]']}]

    def __init__(self, items: list["CustomItem"]) -> None:
        self.items = items

    def generate_cover_page(self, datapack: "Datapack") -> list[dict[str, str | bool]]:
        logo_line = generate_icon_row_spacing(datapack, LOGO_HORIZONTAL_SPACER)
        logo_line["text"] += datapack.font_mapping["logo_256_x_256"] # "logo"
        return [{"text": f"{datapack.name} Reference Book\n\n", "underlined": True}, logo_line]
        # ► ▶  ➙ ➛ 	➜ ➝ ➞ ➟ ➠ ➡ ➢ ➣ ➤ ➥ ➦ ➨ ➩ ➪ ➫ ➬ ➭ ➮ ➯ ➱ ➲ ➳ ➴ ➵ ➶ ➷ ➸ ➹ ➺ ➻ ➼ ➽ ➾

    def generate_pages(self, datapack: "Datapack") -> list[list[dict[str, str | bool]]]:
        # Page order is as follows:
        COVER_PAGE = 1
        CATEGORIES_PAGE = 2
        CATEGORY_ITEMS_PAGE = 3  # 3+   One for each category
        ITEM_PAGE  = CATEGORY_ITEMS_PAGE+len(datapack.reference_book_categories)  # After we have all the categories, start adding the individual items
        BLANK_PAGE = CATEGORY_ITEMS_PAGE*len(datapack.reference_book_categories)+len(datapack.custom_items)+1
        
        # Cover (1)
        cover_page = self.generate_cover_page(datapack)

        # Categories (2)
        category_page = GridPage("Categories", [
                RedirectButton(datapack.font_mapping[f"{category.name.lower()}_category_icon"], f"Go to the `{category.name}` category", CATEGORIES_PAGE)
                for category in datapack.reference_book_categories
            ], datapack, back_button_page=None,
        ).elements

        category_items_pages = []
        # Item list page(s) (3+)
        for category_index, category in enumerate(datapack.reference_book_categories):
            # This shows lists of items per category, the button takes you to the individual item page, which comes after all
            # The cover & category pages, so it's index is CATEGORIES_PAGE + item_index
            item_list_icons = [
                RedirectButton(
                    datapack.font_mapping[f"{item.internal_name}_icon"],
                    remove_colour_codes(item.custom_name or item.base_item),  #colour_codes_to_json_format(item.custom_name or item.base_item)
                    ITEM_PAGE+item_index,
                )
                for item_index, item in enumerate(datapack.custom_items) if item.book_category.name == category.name
            ]
            icon_list_page = GridPage(f"{category.name.title()} items", item_list_icons, datapack, back_button_page=CATEGORIES_PAGE+category_index).elements
            category_items_pages.append(icon_list_page)

        # Item page(s) (x+)
        item_pages = []
        for item in datapack.custom_items:
            category_page_index = CATEGORY_ITEMS_PAGE+[x.name for x in datapack.reference_book_categories].index(item.book_category.name)

            item_page = ItemPage(item, datapack, category_page_index).generate_page()
            item_pages.append(item_page)

        # Blank page:
        blank_page = [{"text": "This page is intentionally left blank", "underlined": False, "bold": False}]

        return [cover_page, category_page, *category_items_pages, *item_pages, blank_page]  # type: ignore[list-item]

    def generate_give_command(self, datapack: "Datapack") -> str:
        from pypacks.resources.custom_item import CustomItem

        pages = self.generate_pages(datapack)
        custom_item_data = CustomItemData(written_book_content=WrittenBookContent(f"{datapack.name} Reference Book", "PyPacks", pages))
        custom_item = CustomItem("minecraft:written_book", f"{datapack.name}_reference_book", additional_item_data=custom_item_data)
        return custom_item.generate_give_command(datapack)

# =======================================================================================================================================

# https://github.com/misode/misode.github.io/blob/master/public/images/crafting_table.png
MISCELLANOUS_REF_BOOK_CATEGORY = ReferenceBookCategory("Misc", f"{PYPACKS_ROOT}/assets/images/reference_book_icons/miscellaneous_icon.png")  # TODO: os.pathlib.join
PAINTING_REF_BOOK_CATEGORY = ReferenceBookCategory("Paintings", f"{PYPACKS_ROOT}/assets/images/reference_book_icons/miscellaneous_icon.png")  # TODO: os.pathlib.join