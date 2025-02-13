from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from pypacks.written_book_framework import (
    ElementPage, GridPage, GridPageManager, Icon, OnClickChangePage, OnHoverShowText, RowManager, Text, FormattedWrittenBook, RightAlignedIcon,
    OnClickRunCommand, OnHoverShowItem, OnHoverShowTextRaw,
    ICONS_PER_ROW, ROWS_PER_PAGE,
)
from pypacks.utils import remove_colour_codes
from pypacks.resources.custom_recipe import *  # noqa: F403

if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.resources.custom_item import CustomItem
    from pypacks.written_book_framework import Row, FilledRow

LOGO_HORIZONTAL_SPACER = 6


@dataclass
class ItemPage:
    item: "CustomItem"
    pack: "Pack" = field(repr=False)  # Cannot be just namespace due to .font_mappings
    back_button_page: int = field(repr=False)

    def generate_info_icons(self) -> list[Icon]:
        from pypacks.resources.custom_item import CustomItem
        info_icons: list[Icon] = []
        # ============================================================================================================
        # More info button
        more_info_text = f"More info about {remove_colour_codes(self.item.custom_name or self.item.base_item.removeprefix('minecraft:').title())}:\n\n{self.item.ref_book_config.description}"
        more_info_button = Icon(
            self.pack.font_mapping["information_icon"],
            self.pack.namespace,
            self.pack.font_mapping["1_pixel_indent"],
            right_indentation=3,
            on_hover=OnHoverShowText(more_info_text),
        )
        info_icons.append(more_info_button)
        # ============================================================================================================
        if self.item.components.instrument is not None:
            play_sound_icon = Icon(
                    self.pack.font_mapping["play_icon"],
                    self.pack.namespace,
                    self.pack.font_mapping["1_pixel_indent"],
                    right_indentation=3,
                    on_click=OnClickRunCommand(self.item.components.instrument.get_run_command(self.pack.namespace)),
                    on_hover=OnHoverShowText(f"Play: {self.item.custom_name}"),
            )
            info_icons.append(play_sound_icon)
        # ============================================================================================================
        recipes = [
            x for x in self.pack.custom_recipes
            if not isinstance(x, SmithingTrimRecipe)
            and (x.result.internal_name if isinstance(x.result, CustomItem) else x.result) == self.item.internal_name
        ]
        recipe_icons = [
            Icon(
                self.pack.font_mapping[f"{recipe.recipe_block_name}_icon"],
                self.pack.namespace,
                self.pack.font_mapping["1_pixel_indent"],
                right_indentation=3,
                on_hover=OnHoverShowTextRaw([
                    {"text": self.pack.font_mapping[f"custom_recipe_for_{recipe.internal_name}_icon"], "font": f"{self.pack.namespace}:all_fonts"},
                    {"text": "\n"*6, "font": "minecraft:default"},
                ]),
            )
            for recipe in recipes
            if self.pack.font_mapping.get(f"{recipe.recipe_block_name}_icon")
        ]
        info_icons.extend(recipe_icons)
        # ============================================================================================================
        return info_icons

    def get_json_data(self) -> list[dict[str, Any] | list[dict[str, Any]]]:
        return [x.get_json_data() for x in self.generate_page()]

    def generate_page(self) -> list["Text | Icon | RightAlignedIcon | Row | FilledRow"]:
        give_item_icon = Icon(
            self.pack.font_mapping[f"{self.item.internal_name}_icon"],
            font_namespace=self.pack.namespace,
            indent_unicode_char=self.pack.font_mapping["1_pixel_indent"],
            on_click=OnClickRunCommand(f"/function {self.pack.namespace}:give/{self.item.internal_name}"),
            on_hover=OnHoverShowItem(self.item, self.pack.namespace),
        )
        MORE_INFO_ICONS_PER_ROW = 5
        MORE_INFO_ICONS_TRAILING_NEW_LINES = 3
        more_info_icon_rows = RowManager(self.generate_info_icons(), MORE_INFO_ICONS_PER_ROW, self.pack.font_mapping["1_pixel_indent"],
                                         self.pack.namespace, trailing_new_lines=MORE_INFO_ICONS_TRAILING_NEW_LINES).rows
        return [
            Text(f"{remove_colour_codes(self.item.custom_name or self.item.base_item.removeprefix('minecraft:').title())}", underline=True, bold=True, text_color="black"),
            Text("\n"*2),
            give_item_icon,
            Text("\n"*4),
            *more_info_icon_rows,
            Text("\n"*(4-(len(more_info_icon_rows)))),
            RightAlignedIcon(
                self.pack.font_mapping["satchel_icon"],
                self.pack.font_mapping["1_pixel_indent"],
                20,
                font_namespace=self.pack.namespace,
                left_shift=3,
                on_click=OnClickChangePage(self.back_button_page),
                on_hover=OnHoverShowText("Go back to the categories page"),
            ),
        ]


@dataclass
class ReferenceBook:
    items: list["CustomItem"]

    def generate_cover_page(self, pack: "Pack") -> "ElementPage":
        title_starting_char_code = "➤".encode('unicode_escape').decode('ascii')
        return ElementPage([
            Text(f"{title_starting_char_code} {pack.name} Reference Book\n\n\n", underline=True, text_color="black"),
            Text(pack.font_mapping['1_pixel_indent']*LOGO_HORIZONTAL_SPACER, font=f"{pack.namespace}:all_fonts", text_color="white"),  # SPACER
            Text(pack.font_mapping["logo_256_x_256"], font=f"{pack.namespace}:all_fonts", text_color="white")
        ])

    def _generate_category_to_page_number(self, pack: "Pack") -> dict[str, int]:
        category_to_page_number = {}
        current_page_number = 0
        for category in pack.reference_book_categories:
            category_to_page_number[category.name] = current_page_number
            current_page_number += (
                len([x for x in pack.custom_items if x.ref_book_config.category.name == category.name and not x.ref_book_config.hidden]) // (ICONS_PER_ROW*ROWS_PER_PAGE) + 1
            )
        return category_to_page_number

    def generate_pages(self, pack: "Pack") -> list["ElementPage | GridPage"]:
        # Page order is as follows:
        COVER_PAGE = 1
        # ==============================================================================================================================
        CATEGORIES_STARTING_PAGE = COVER_PAGE + 1
        CATEGORIES_FINISHING_PAGE = CATEGORIES_STARTING_PAGE + len(pack.reference_book_categories) // (ICONS_PER_ROW*ROWS_PER_PAGE)
        # ==============================================================================================================================
        CATEGORY_ITEMS_STARTING_PAGE = CATEGORIES_FINISHING_PAGE + 1  # One for each category
        CATEGORY_ITEMS_FINISHING_PAGE = CATEGORY_ITEMS_STARTING_PAGE + max(self._generate_category_to_page_number(pack).values())
        # ==============================================================================================================================
        ITEM_PAGE_START = CATEGORY_ITEMS_FINISHING_PAGE + 1  # After we have all the categories, start adding the individual items
        # ==============================================================================================================================
        # BLANK_PAGE = ITEM_PAGE_START*len(pack.custom_items) + 1  # Just a blank page at the end
        # ==============================================================================================================================
        # Cover (1)
        cover_page = self.generate_cover_page(pack)  # Has to be pack
        # ==============================================================================================================================
        # Categories (2)
        category_pages: list[GridPage] = GridPageManager(
            title="Categories",
            icons=[
                Icon(
                    pack.font_mapping[f"{category.internal_name}_category_icon"],
                    pack.namespace,
                    indent_unicode_char=pack.font_mapping["1_pixel_indent"],
                    on_hover=OnHoverShowText(f"Go to the `{category.name}` category"),
                    on_click=OnClickChangePage(CATEGORY_ITEMS_STARTING_PAGE+i)
                )
                for i, category in enumerate(pack.reference_book_categories)
            ],
            empty_icon_unicode_char=pack.font_mapping["blank_icon"],
            indent_unicode_char=pack.font_mapping["1_pixel_indent"],
            font_namespace=pack.namespace,
        ).pages

        # ==============================================================================================================================
        # Item list pages
        category_items_page_managers: list[GridPageManager] = [
            GridPageManager(
                title=f"{category.name.title()} items",
                icons=[
                    Icon(
                        pack.font_mapping[f"{item.internal_name}_icon"],
                        pack.namespace,
                        indent_unicode_char=pack.font_mapping["1_pixel_indent"],
                        on_hover=OnHoverShowText(remove_colour_codes(item.custom_name or item.base_item.removeprefix('minecraft:').title())),
                        on_click=OnClickChangePage(ITEM_PAGE_START+item_index),
                    )
                    for item_index, item in enumerate(pack.custom_items)
                    if item.ref_book_config.category.name == category.name and not item.ref_book_config.hidden
                ],
                empty_icon_unicode_char=pack.font_mapping["blank_icon"],
                indent_unicode_char=pack.font_mapping["1_pixel_indent"],
                font_namespace=pack.namespace,
                # back_button_unicode_char=pack.font_mapping["satchel_icon"],
                # back_button_page=CATEGORIES_STARTING_PAGE,
            )
            for category in pack.reference_book_categories
        ]
        # Flatten to a 1d list of pages
        category_items_pages = [x for y in category_items_page_managers for x in y.pages]

        # ==============================================================================================================================
        # Item pages
        item_pages: list[ElementPage] = []
        for item in pack.custom_items:
            category_page_index = CATEGORY_ITEMS_STARTING_PAGE + self._generate_category_to_page_number(pack)[item.ref_book_config.category.name]
            item_page = ItemPage(item, pack, category_page_index)
            item_pages.append(item_page)  # type: ignore

        # ==============================================================================================================================
        # Blank page:
        blank_page = ElementPage([Text("This page is intentionally left blank")])
        # ==============================================================================================================================
        return [cover_page, *category_pages, *category_items_pages, *item_pages, blank_page]

    def generate_give_command(self, pack: "Pack") -> str:
        return FormattedWrittenBook(
            pages=self.generate_pages(pack),
            title=f"{pack.name} Reference Book",
            author="Pypacks",
        ).generate_give_command(pack.namespace)
# =======================================================================================================================================
