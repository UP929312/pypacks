from typing import TYPE_CHECKING

from pypacks.written_book_framework import FormattedWrittenBook, ElementPage, Icon

if TYPE_CHECKING:
    from pypacks.pack import Pack


class FontTestingBook:
    def generate_pages(self, pack: "Pack") -> list[ElementPage]:
        return [
            ElementPage(
                [
                    Icon(
                        pack.font_mapping[icon.name],
                        pack.namespace,
                        indent_unicode_char=pack.font_mapping["1_pixel_indent"],
                        include_formatting=False,
                    )
                ]
            )
            for icon in pack.custom_fonts[0].font_elements
        ]

    def generate_give_command(self, pack: "Pack") -> str:
        return FormattedWrittenBook(
            pages=self.generate_pages(pack),  # pyright: ignore
            title=f"{pack.name} Font Test Book",
            author="Pypacks",
        ).generate_give_command(pack.namespace)
# =======================================================================================================================================
