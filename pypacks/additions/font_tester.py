from typing import TYPE_CHECKING

from pypacks.additions.written_book_framework import FormattedWrittenBook, ElementPage, Icon

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
        title = f"{pack.name} Font Test Book" if len(f"{pack.name} Reference Book") <= 32 else "Font Test Book"
        return FormattedWrittenBook(
            pages=self.generate_pages(pack),  # type: ignore[arg-type]
            title=title,
            author=pack.name,
        ).generate_give_command(pack.namespace)

    def create_datapack_files(self, pack: "Pack") -> None:
        from pypacks.resources.custom_mcfunction import MCFunction
        MCFunction("give_font_tester", ["# Give the font tester book", self.generate_give_command(pack)]).create_datapack_files(pack)

# =======================================================================================================================================
