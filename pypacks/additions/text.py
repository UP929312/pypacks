from dataclasses import dataclass
from typing import Any, TYPE_CHECKING

from pypacks.utils import recursively_remove_nones_from_data

if TYPE_CHECKING:
    from pypacks.additions.constants import ColorType
    from pypacks.resources.custom_item import CustomItem



@dataclass
class Text:
    """Represents a text component in Minecraft. This is used in many places, such as in written books, item names, etc.
    Click events only work in chat messages and written books,
    Hover events work everywhere.
    """
    text: str
    color: "ColorType | int | None" = "white"
    bold: bool = False
    italic: bool = False
    underlined: bool = False
    strikethrough: bool = False
    obfuscated: bool = False
    on_click: "OnClickChangePage | OnClickRunCommand | None" = None
    on_hover: "OnHoverShowText | OnHoverShowTextRaw | OnHoverShowItem | None" = None
    font: str = "minecraft:default"

    def to_dict(self) -> dict[str, Any]:
        return recursively_remove_nones_from_data({  # type: ignore[abc]
            "text": self.text,
            "color": self.color,
            "bold": self.bold if self.bold else None,
            "italic": self.italic,  # WE DON'T WANT ITALICS
            "underlined": self.underlined if self.underlined else None,
            "strikethrough": self.strikethrough if self.strikethrough else None,
            "obfuscated": self.obfuscated if self.obfuscated else None,
            **(self.on_click.to_dict() if self.on_click else {}),
            **(self.on_hover.to_dict() if self.on_hover else {}),
            "font": self.font,
        })

    get_json_data = to_dict

    @classmethod
    def from_input(cls, data: "Text | dict[str, Any] | str") -> "Text":
        if isinstance(data, Text):
            return data
        if isinstance(data, dict):
            return cls(**data)
        return cls(data)
    
    @staticmethod
    def make_white_and_remove_italics(text: "str | Text | dict[str, Any]") -> str | dict[str, Any]:
        text_obj = Text.from_input(text)
        text_obj.color = "white"
        text_obj.italic = False
        return text_obj.to_dict()

    @staticmethod
    def remove_italics(text: "str | Text | dict[str, Any]") -> str | dict[str, Any]:
        text = Text.from_input(text)
        text.italic = False
        return text.to_dict()


# =======================================================================================================================================

@dataclass
class OnClickChangePage:
    page_to_change_to: int

    def to_dict(self) -> dict[str, Any]:
        return {"click_event": {"action": "change_page", "page": self.page_to_change_to}}


@dataclass
class OnClickRunCommand:
    command: str

    # def __post_init__(self) -> None:
    #     if self.command.startswith("/"):
    #         print("Warning: Command should not start with a /")

    def to_dict(self) -> dict[str, Any]:
        return {"click_event": {"action": "run_command", "command": self.command}}


@dataclass
class OnClickOpenURL:
    url: str

    def to_dict(self) -> dict[str, Any]:
        return {"click_event": {"action": "open_url", "url": self.url}}


@dataclass
class OnHoverShowText:
    text: "str | Text | dict[str, Any]"
    font: str = "minecraft:default"

    def to_dict(self) -> dict[str, Any]:
        return {"hover_event": {"action": "show_text", "value": self.text, "font": self.font}}


@dataclass
class OnHoverShowTextRaw:
    text: dict[str, Any] | list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {"hover_event": {"action": "show_text", "value": self.text}}


@dataclass
class OnHoverShowItem:
    custom_item: "CustomItem"
    pack_namespace: str

    def to_dict(self) -> dict[str, Any]:
        return {"hover_event": {"action": "show_item", "id": self.custom_item.base_item, "components": self.custom_item.to_dict(self.pack_namespace)}}


# =======================================================================================================================================


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
