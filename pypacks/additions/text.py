import json
from dataclasses import dataclass
from typing import Any

from pypacks.additions.constants import ColorType
from pypacks.utils import recursively_remove_nones_from_data


@dataclass
class Text:
    text: str
    color: ColorType | int = "white"
    bold: bool = False
    italic: bool = False
    underlined: bool = False
    strikethrough: bool = False
    obfuscated: bool = False
    font: str | None = None

    def to_dict(self) -> list[dict[str, Any]]:
        return [recursively_remove_nones_from_data({
            "text": self.text,
            "color": self.color if self.color != "white" else None,
            "bold": self.bold if self.bold else None,
            "italic": self.italic,  # WE DON'T WANT IT ITALICS
            "underlined": self.underlined if self.underlined else None,
            "strikethrough": self.strikethrough if self.strikethrough else None,
            "obfuscated": self.obfuscated if self.obfuscated else None,
            "font": self.font,
        })]
    
    @staticmethod
    def resolve_text(text: "str | Text | None") -> list[dict[str, str | bool]] | None:
        if text is None:
            return None
        if isinstance(text, Text):
            return Text.to_dict(text)
        return Text.to_dict(Text(text))

# @dataclass
# class TranslatableText(Text):
#     translate: str
#     with_: list[Text] = None

#     def to_dict(self) -> dict[str, Any]:
#         return recursively_remove_nones_from_data({
#             "translate": self.translate,
#             "with": [text.to_dict() for text in self.with_] if self.with_ else None,
#             **super().to_dict()
#         })
