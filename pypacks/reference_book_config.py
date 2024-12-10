from dataclasses import dataclass
from pathlib import Path

from pypacks.image_generation.ref_book_icon_gen import add_centered_overlay
from pypacks.utils import PYPACKS_ROOT

@dataclass
class RefBookCategory:
    internal_name: str
    name: str
    image_path: str | Path
    icon_image_bytes: bytes = None  # type: ignore  # DON'T SET THIS MANUALLY

    @staticmethod
    def get_unique_categories(categories: list["RefBookCategory"]) -> list["RefBookCategory"]:
        reference_book_categories: list["RefBookCategory"] = []
        for category in categories:
            if category.name not in [x.name for x in reference_book_categories]:
                with open(category.image_path, "rb") as file:
                    category.icon_image_bytes = add_centered_overlay(image_bytes=file.read())
                reference_book_categories.append(category)
        return reference_book_categories


@dataclass
class RefBookConfig:
    category: RefBookCategory = None  #type: ignore[assignment] # Set in post_init, never None
    description: str = "No description provided for this item"
    hidden: bool = False
    wiki_link: str | None = None

    def __post_init__(self) -> None:
        assert self.wiki_link is None
        if self.category is None:
            self.category = MISC_REF_BOOK_CATEGORY

MISC_REF_BOOK_CATEGORY = RefBookCategory("misc", "Misc", Path(PYPACKS_ROOT)/"assets"/"images"/"reference_book_icons"/"miscellaneous_icon.png")
PAINTING_REF_BOOK_CATEGORY = RefBookCategory("paintings", "Paintings", Path(PYPACKS_ROOT)/"assets"/"images"/"reference_book_icons"/"painting.png")
CUSTOM_BLOCKS_REF_BOOK_CATEGORY = RefBookCategory("custom_blocks", "Custom Block", Path(PYPACKS_ROOT)/"assets"/"images"/"reference_book_icons"/"custom_block_icon.png")

MISC_REF_BOOK_CONFIG = RefBookConfig(category=MISC_REF_BOOK_CATEGORY, description="No description provided for this item")
PAINTING_REF_BOOK_CONFIG = RefBookConfig(category=PAINTING_REF_BOOK_CATEGORY, description="A custom painting, added by this pack!")
CUSTOM_BLOCKS_REF_BOOK_CONFIG = RefBookConfig(category=CUSTOM_BLOCKS_REF_BOOK_CATEGORY, description="A custom block, added by this pack!")
