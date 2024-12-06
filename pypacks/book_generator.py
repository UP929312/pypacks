from dataclasses import dataclass
from typing import TYPE_CHECKING

from pypacks.written_book_framework import (
    ElementPage, GridPage, Icon, OnClickChangePage, OnHoverShowText, Text, FormattedWrittenBook, RightAlignedIcon,
    OnClickRunCommand, OnHoverShowItem,
)
from pypacks.utils import PYPACKS_ROOT, remove_colour_codes
from pypacks.resources.custom_recipe import *

if TYPE_CHECKING:
    from pypacks.datapack import Datapack
    from pypacks.resources.custom_item import CustomItem

LOGO_HORIZONTAL_SPACER = 6

@dataclass
class ReferenceBookCategory:
    name: str
    image_path: str
    icon_image_bytes: bytes | None = None  # DON'T SET THIS MANUALLY

    def __post_init__(self) -> None:
        assert " " not in self.name, "Category name cannot contain spaces"

@dataclass
class ItemPage:
    item: "CustomItem"
    datapack: "Datapack"
    back_button_page: int
    
    def generate_info_icons(self) -> list[Icon]:
        from pypacks.resources.custom_item import CustomItem

        non_smithing_trim_recipes = [x for x in self.datapack.custom_recipes if not isinstance(x, SmithingTrimRecipe)]
        recipes = [x for x in non_smithing_trim_recipes if (
            x.result.internal_name if isinstance(x.result, CustomItem) else x.result
        ) == self.item.internal_name]
        recipe_to_font_icon = {
            ShapelessCraftingRecipe: self.datapack.font_mapping["crafting_table_icon"],
            ShapedCraftingRecipe: self.datapack.font_mapping["crafting_table_icon"],
            CraftingTransmuteRecipe: self.datapack.font_mapping["crafting_table_transmute_icon"],
            FurnaceRecipe: self.datapack.font_mapping["furnace_icon"],
            StonecutterRecipe: self.datapack.font_mapping["stonecutter_icon"],
            BlastFurnaceRecipe: self.datapack.font_mapping["furnace_icon"],
            SmokerRecipe: self.datapack.font_mapping["furnace_icon"],
            StonecutterRecipe: self.datapack.font_mapping["stonecutter_icon"],
            CampfireRecipe: self.datapack.font_mapping["campfire_icon"],
            SmithingTransformRecipe: self.datapack.font_mapping["smithing_table_icon"],
            SmithingTrimRecipe: self.datapack.font_mapping["smithing_table_icon"],
        }
        recipe_icons = [
            Icon(recipe_to_font_icon[type(recipe)],
                 self.datapack.namespace,
                 self.datapack.font_mapping["empty_1_x_1"],
                 on_hover=OnHoverShowText(self.datapack.font_mapping[f"custom_recipe_for_{recipe.internal_name}_icon"], font=f"{self.datapack.namespace}:all_fonts"),
            )
            for recipe in recipes if type(recipe) in recipe_to_font_icon
        ]
        # more_info_icon = MoreInfoIcon(self.datapack.font_mapping["information_icon"], item=self.item)
        #   return [more_info_icon, *recipe_icons]
        return recipe_icons

    def get_json_data(self) -> list[dict[str, Any]]:
        return [x.get_json_data() for x in self.generate_page()]

    def generate_page(self) -> list[Text | Icon | RightAlignedIcon]:
        give_item_icon = Icon(
            self.datapack.font_mapping[f"{self.item.internal_name}_icon"],
            font_namespace=self.datapack.namespace,
            indent_unicode_char=self.datapack.font_mapping["empty_1_x_1"],
            on_click=OnClickRunCommand(f"/function {self.datapack.namespace}:give/{self.item.internal_name}", self.datapack),
            on_hover=OnHoverShowItem(self.item, self.datapack.namespace),
        )
        more_info_text = f"More info about {remove_colour_codes(self.item.custom_name or self.item.base_item)}:\n\n"
        more_info_text += self.item.reference_book_description if self.item.reference_book_description else "No description available"

        return [
            Text(f"{remove_colour_codes(self.item.custom_name or self.item.base_item)}", underline=True, bold=True),
            Text("\n"*2),
            give_item_icon,
            Text("\n"*4),
            # Get all the ways to craft it, info, etc
            Icon(self.datapack.font_mapping["information_icon"], self.datapack.namespace, self.datapack.font_mapping["empty_1_x_1"], on_hover=OnHoverShowText(more_info_text)),
            *self.generate_info_icons(),
            Text("\n"*4),
            RightAlignedIcon(
                self.datapack.font_mapping["satchel_icon"],
                self.datapack.font_mapping["empty_1_x_1"],
                20,
                font_namespace=self.datapack.namespace,
                left_shift=3,
                on_click=OnClickChangePage(self.back_button_page),
                on_hover=OnHoverShowText("Go back to the categories page"),
            ),
        ]


@dataclass
class ReferenceBook:
    items: list["CustomItem"]
    
    def generate_cover_page(self, datapack: "Datapack") -> "ElementPage":
        return ElementPage([
            Text(f"{datapack.name} Reference Book\n\n\n", underline=True),
            Text(datapack.font_mapping['empty_1_x_1']*LOGO_HORIZONTAL_SPACER, font=f"{datapack.namespace}:all_fonts"),  # SPACER
            Text(datapack.font_mapping["logo_256_x_256"], font=f"{datapack.namespace}:all_fonts")
        ])

    def generate_pages(self, datapack: "Datapack") -> list["ElementPage | GridPage"]:
        # Page order is as follows:
        COVER_PAGE = 1
        CATEGORIES_PAGE = 2
        CATEGORY_ITEMS_PAGE = 3  # 3+   One for each category
        ITEM_PAGE  = CATEGORY_ITEMS_PAGE+len(datapack.reference_book_categories)  # After we have all the categories, start adding the individual items
        BLANK_PAGE = CATEGORY_ITEMS_PAGE*len(datapack.reference_book_categories)+len(datapack.custom_items)+1

        # Cover (1)
        cover_page = self.generate_cover_page(datapack)

        # Categories (2)
        category_page: GridPage = GridPage(
            Text("Categories", underline=True),
            datapack.font_mapping["blank_icon"],
            datapack.font_mapping["empty_1_x_1"],
            datapack.namespace,
            [
                Icon(datapack.font_mapping[f"{category.name.lower()}_category_icon"],
                     datapack.namespace,
                     indent_unicode_char=datapack.font_mapping["empty_1_x_1"],
                     on_hover=OnHoverShowText(f"Go to the `{category.name}` category"),
                     on_click=OnClickChangePage(CATEGORY_ITEMS_PAGE+i)
                )
                for i, category in enumerate(datapack.reference_book_categories)
            ],
            back_button_unicode_char=datapack.font_mapping["satchel_icon"],
        )

        category_items_pages: list[GridPage] = []
        # Item list page(s) (3+)
        for category in datapack.reference_book_categories:
            # This shows lists of items per category, the button takes you to the individual item page, which comes after all
            # The cover & category pages, so it's index is CATEGORIES_PAGE + item_index
            icon_list_page = GridPage(
                Text(f"{category.name.title()} items", underline=True),
                empty_icon_unicode_char=datapack.font_mapping["blank_icon"],
                indent_unicode_char=datapack.font_mapping["empty_1_x_1"],
                font_namespace=datapack.namespace,
                icons=[
                    Icon(
                        datapack.font_mapping[f"{item.internal_name}_icon"],
                        datapack.namespace,
                        indent_unicode_char=datapack.font_mapping["empty_1_x_1"],
                        on_hover=OnHoverShowText(remove_colour_codes(item.custom_name or item.base_item)),
                        on_click=OnClickChangePage(ITEM_PAGE+item_index),
                    )
                    for item_index, item in enumerate(datapack.custom_items) if item.book_category.name == category.name
                ],
                back_button_page=CATEGORIES_PAGE,
                back_button_unicode_char=datapack.font_mapping["satchel_icon"],
            )
            category_items_pages.append(icon_list_page)

        # Item page(s) (x+)
        item_pages = []
        for item in datapack.custom_items:
            category_page_index = CATEGORY_ITEMS_PAGE+[x.name for x in datapack.reference_book_categories].index(item.book_category.name)

            item_page: ElementPage = ItemPage(item, datapack, category_page_index)  # type: ignore
            item_pages.append(item_page)

        # Blank page:
        blank_page = ElementPage([Text("This page is intentionally left blank")])

        all_pages: list[ElementPage | GridPage] = [cover_page, category_page, *category_items_pages, *item_pages, blank_page]

        return all_pages

    def generate_give_command(self, datapack: "Datapack") -> str:
        return FormattedWrittenBook(
            pages=self.generate_pages(datapack),
            title=f"{datapack.name} Reference Book",
            author="Pypacks",
        ).generate_give_command(datapack)
# =======================================================================================================================================

# https://github.com/misode/misode.github.io/blob/master/public/images/crafting_table.png
MISCELLANOUS_REF_BOOK_CATEGORY = ReferenceBookCategory("Misc", f"{PYPACKS_ROOT}/assets/images/reference_book_icons/miscellaneous_icon.png")  # TODO: os.pathlib.join
PAINTING_REF_BOOK_CATEGORY = ReferenceBookCategory("Paintings", f"{PYPACKS_ROOT}/assets/images/reference_book_icons/painting.png")  # TODO: os.pathlib.join
