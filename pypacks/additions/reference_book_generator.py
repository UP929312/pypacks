from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from pypacks.utils import format_written_book
from pypacks.additions.written_book_framework import (
    ElementPage, GridPage, GridPageManager, Icon, RowManager, FormattedWrittenBook, RightAlignedIcon, ICONS_PER_PAGE,
)
from pypacks.additions.text import Text, OnClickRunCommand, OnHoverShowItem, OnHoverShowTextRaw, OnClickChangePage, OnHoverShowText
from pypacks.resources.custom_recipe import SmithingTrimRecipe

if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.resources.custom_item import CustomItem
    from pypacks.resources.custom_dimension import CustomDimension
    from pypacks.additions.written_book_framework import Row, FilledRow

LOGO_HORIZONTAL_SPACER = 6


@dataclass
class GenericItemPage:
    title: str | Text | dict[str, Any]  # Can be a Text object or a string
    item: "CustomItem | CustomDimension"
    pack: "Pack" = field(repr=False)  # Cannot be just namespace due to .font_mappings
    back_button_page: int = field(repr=False)

    def generate_info_icon(self) -> "Icon":
        more_info_text = f"More info about {self.title}:\n\n{self.item.ref_book_config.description}"
        return Icon(
            self.pack.font_mapping["information_icon"],
            self.pack.namespace,
            right_padding=3,
            on_hover=OnHoverShowText(more_info_text),
        )

    def get_json_data(self) -> list[dict[str, Any] | list[dict[str, Any]]]:
        return [x.get_json_data() for x in self.generate_page()]

    def generate_main_icon(self) -> "Icon":
        raise NotImplementedError

    def generate_info_icons(self) -> list["Icon"]:
        return [self.generate_info_icon()]

    def generate_page(self) -> list["Text | Icon | RightAlignedIcon | Row | FilledRow"]:
        MORE_INFO_ICONS_PER_ROW = 5
        MORE_INFO_ICONS_TRAILING_NEW_LINES = 3
        more_info_icon_rows = RowManager(
            self.generate_info_icons(), MORE_INFO_ICONS_PER_ROW, self.pack.namespace, trailing_new_lines=MORE_INFO_ICONS_TRAILING_NEW_LINES,
            empty_icon=None,
        )
        title = Text.from_input(self.title)
        title.color = "black"
        return [
            title,
            Text("\n"*2),
            self.generate_main_icon(),
            Text("\n"*4),
            *more_info_icon_rows.rows,
            Text("\n"*(2-(len(more_info_icon_rows.rows)))),
            RightAlignedIcon(
                unicode_char=self.pack.font_mapping["satchel_icon"],
                font_namespace=self.pack.namespace,
                char_width=20,
                left_shift=3,
                on_click=OnClickChangePage(self.back_button_page),
                on_hover=OnHoverShowText("Go back to the categories page"),
            ),
        ]


@dataclass
class CustomItemPage(GenericItemPage):
    def generate_info_icons(self) -> list[Icon]:
        from pypacks.resources.custom_item import CustomItem
        assert isinstance(self.item, CustomItem)
        info_icons: list[Icon] = [self.generate_info_icon()]
        # ============================================================================================================
        if self.item.components.instrument is not None:
            play_sound_icon = Icon(
                unicode_char=self.pack.font_mapping["play_icon"],
                font_namespace=self.pack.namespace,
                right_padding=3,
                on_click=OnClickRunCommand(self.item.components.instrument.get_run_command(self.pack.namespace)),
                on_hover=OnHoverShowText(f"Play: {self.item.custom_name}"),
            )
            info_icons.append(play_sound_icon)
        # ============================================================================================================
        # Custom recipes where this item is the result
        recipe_results = [
            x for x in self.pack.custom_recipes
            if not isinstance(x, SmithingTrimRecipe)
            and (x.result.internal_name if isinstance(x.result, CustomItem) else x.result) == self.item.internal_name
        ]
        recipe_result_icons = [
            Icon(
                self.pack.font_mapping[f"{recipe.recipe_block_name}_icon"],
                font_namespace=self.pack.namespace,
                right_padding=3,
                on_hover=OnHoverShowTextRaw([
                    {"text": self.pack.font_mapping[f"custom_recipe_for_{recipe.internal_name}_icon"], "font": f"{self.pack.namespace}:all_fonts"},
                    {"text": "\n"*6, "font": "minecraft:default"},
                ]),
            )
            for recipe in recipe_results
            if self.pack.font_mapping.get(f"{recipe.recipe_block_name}_icon")
        ]
        info_icons.extend(recipe_result_icons)
        # ===================================
        # Custom Recipes where this item is used in the recipe
        recipe_used_in = [
            x for x in self.pack.custom_recipes
            if not isinstance(x, SmithingTrimRecipe)
            and any(ingredient.internal_name == self.item.internal_name if isinstance(ingredient, CustomItem) else False for ingredient in x.used_ingredients)
        ]
        recipe_used_in_icons = [
            Icon(
                self.pack.font_mapping[f"{recipe.recipe_block_name}_used_in_icon"],
                font_namespace=self.pack.namespace,
                right_padding=3,
                on_hover=OnHoverShowTextRaw([
                    {"text": self.pack.font_mapping[f"custom_recipe_for_{recipe.internal_name}_icon"], "font": f"{self.pack.namespace}:all_fonts"},
                    {"text": "\n"*6, "font": "minecraft:default"},
                ]),
            )
            for recipe in recipe_used_in
            if self.pack.font_mapping.get(f"{recipe.recipe_block_name}_used_in_icon")
        ]
        info_icons.extend(recipe_used_in_icons)
        # ============================================================================================================
        return info_icons

    def generate_main_icon(self) -> "Icon":
        from pypacks.resources.custom_item import CustomItem
        assert isinstance(self.item, CustomItem)
        return Icon(
            unicode_char=self.pack.font_mapping[f"{self.item.internal_name}_icon"],
            font_namespace=self.pack.namespace,
            on_click=OnClickRunCommand(f"/function {self.pack.namespace}:give/{self.item.internal_name}"),
            on_hover=OnHoverShowItem(self.item, self.pack.namespace),
        )


@dataclass
class DimensionPage(GenericItemPage):
    def generate_main_icon(self) -> "Icon":
        from pypacks.resources.custom_dimension import CustomDimension
        assert isinstance(self.item, CustomDimension)
        return Icon(
            unicode_char=self.pack.font_mapping.get(f"{self.item.internal_name}_icon") or self.pack.font_mapping["dimensions_icon"],
            font_namespace=self.pack.namespace,
            on_click=OnClickRunCommand(self.item.generate_teleport_command(self.pack.namespace)),
            on_hover=OnHoverShowText(f"Teleport to {self.item.internal_name.replace('_', ' ').title()}"),
        )


@dataclass
class ReferenceBook:
    items: list["CustomItem"]

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="function")

    def generate_cover_page(self, pack: "Pack") -> "ElementPage":
        title_starting_char_code = "➤".encode('unicode_escape').decode('ascii')
        page_content = " "*LOGO_HORIZONTAL_SPACER + pack.font_mapping["logo_256_x_256"]
        return ElementPage([
            Text(f"{title_starting_char_code} {pack.name} Reference Book\n\n\n", color="black"),  # underlined=True,
            Text(page_content, font=f"{pack.namespace}:all_fonts", underlined=False, color="white"),
        ])

    def _generate_category_to_page_number(self, pack: "Pack") -> dict[str, int]:
        category_to_page_number = {}
        current_page_number = 0
        for category in pack.reference_book_categories:
            category_to_page_number[category.name] = current_page_number
            this_categories_items_count = category.get_length(pack.custom_items, pack.custom_dimensions)
            current_page_number += (this_categories_items_count // (ICONS_PER_PAGE) + 1)
        return category_to_page_number

    def generate_pages(self, pack: "Pack") -> list["ElementPage | GridPage"]:
        # Page order is as follows:
        category_to_page_number = self._generate_category_to_page_number(pack)
        COVER_PAGE = 1
        # ==============================================================================================================================
        CATEGORIES_STARTING_PAGE = COVER_PAGE + 1
        CATEGORIES_FINISHING_PAGE = CATEGORIES_STARTING_PAGE + len(pack.reference_book_categories) // (ICONS_PER_PAGE)  # A page for each ICONS_PER_PAGE categories
        # ==============================================================================================================================
        CATEGORY_ITEMS_STARTING_PAGE = CATEGORIES_FINISHING_PAGE + 1  # One for each category
        CATEGORY_ITEMS_FINISHING_PAGE = CATEGORY_ITEMS_STARTING_PAGE + max(category_to_page_number.values())
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
                    unicode_char=pack.font_mapping[f"{category.internal_name}_category_icon"],
                    font_namespace=pack.namespace,
                    on_hover=OnHoverShowText(f"Go to the `{category.name}` category"),
                    on_click=OnClickChangePage(CATEGORY_ITEMS_STARTING_PAGE+category_to_page_number[category.name])
                )
                for category in pack.reference_book_categories
            ],
            empty_icon_unicode_char=pack.font_mapping["blank_icon"],
            font_namespace=pack.namespace,
        ).pages
        # ==============================================================================================================================
        # Item list pages
        category_items_page_managers: list[GridPageManager] = [
            (
                GridPageManager(
                    title=f"{category.name.title()} items",
                    icons=[
                        Icon(
                            unicode_char=pack.font_mapping[f"{item.internal_name}_icon"],
                            font_namespace=pack.namespace,
                            on_hover=OnHoverShowText(item.custom_name or item.base_item.removeprefix('minecraft:').title()),
                            on_click=OnClickChangePage(ITEM_PAGE_START+item_index),
                        )
                        for item_index, item in enumerate(pack.custom_items)
                        if item.ref_book_config.category.name == category.name and not item.ref_book_config.hidden
                    ],
                    empty_icon_unicode_char=pack.font_mapping["blank_icon"],
                    font_namespace=pack.namespace,
                )
                if category.category_type == "item" else
                GridPageManager(
                    title=f"{category.name.title()}",
                    icons=[
                        Icon(
                            unicode_char=pack.font_mapping["dimensions_icon"],  # pack.font_mapping.get(f"{dimension.internal_name}_category_icon") or
                            font_namespace=pack.namespace,
                            on_hover=OnHoverShowText(dimension.internal_name.replace("_", " ").title()),
                            on_click=OnClickChangePage(ITEM_PAGE_START+dimension_index),
                        )
                        for dimension_index, dimension in enumerate(pack.custom_dimensions[:20], start=len(pack.custom_items))  # TODO: 20 for now
                    ],
                    empty_icon_unicode_char=pack.font_mapping["blank_icon"],
                    font_namespace=pack.namespace,
                )
            )
            for category in pack.reference_book_categories
        ]
        # Flatten to a 1d list of pages
        category_items_pages = [x for y in category_items_page_managers for x in y.pages]
        # ==============================================================================================================================
        # Item pages
        item_pages: list[ElementPage] = [
            CustomItemPage(item.custom_name or item.base_item.removeprefix('minecraft:').title(), item, pack,
                           CATEGORY_ITEMS_STARTING_PAGE+category_to_page_number[item.ref_book_config.category.name])  # type: ignore[misc]
            for item in pack.custom_items
        ]
        dimension_pages: list[ElementPage] = [
            DimensionPage(dimension.internal_name.replace('_', ' ').title(), dimension, pack,
                          CATEGORY_ITEMS_STARTING_PAGE+category_to_page_number["Dimensions"])  # type: ignore[misc]
            for dimension in pack.custom_dimensions
        ]
        # ==============================================================================================================================
        # Blank page:
        blank_page = ElementPage([Text("This page is intentionally left blank")])
        # ==============================================================================================================================
        return [cover_page, *category_pages, *category_items_pages, *[*item_pages, *dimension_pages], blank_page]

    def generate_give_command(self, pack: "Pack") -> str:
        title = f"{pack.name} Reference Book" if len(f"{pack.name} Reference Book") <= 32 else "Reference book"
        return FormattedWrittenBook(
            pages=self.generate_pages(pack),
            title=title,
            author=pack.name,
        ).generate_give_command(pack.namespace)

    def create_datapack_files(self, pack: "Pack") -> None:
        from pypacks.resources.custom_mcfunction import MCFunction
        MCFunction("give_reference_book", ["# Give the book", format_written_book(self.generate_give_command(pack))]).create_datapack_files(pack)

# =======================================================================================================================================
