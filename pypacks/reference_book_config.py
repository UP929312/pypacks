from dataclasses import dataclass, field
from pathlib import Path

from pypacks.utils import PYPACKS_ROOT


@dataclass
class RefBookCategory:
    internal_name: str
    name: str
    image_path: str | Path

    @staticmethod
    def get_unique_categories(categories: list["RefBookCategory"]) -> list["RefBookCategory"]:
        # Get all the categories by removing duplicates via name
        reference_book_categories = list({category.name: category for category in categories}.values())
        assert len(reference_book_categories) <= 20, "There can only be 20 reference book categories!"
        return reference_book_categories


MISC_REF_BOOK_CATEGORY = RefBookCategory("misc", "Misc", Path(PYPACKS_ROOT)/"assets"/"images"/"reference_book_icons"/"miscellaneous_icon.png")
PAINTING_REF_BOOK_CATEGORY = RefBookCategory("paintings", "Paintings", Path(PYPACKS_ROOT)/"assets"/"images"/"reference_book_icons"/"painting.png")
CUSTOM_BLOCKS_REF_BOOK_CATEGORY = RefBookCategory("custom_blocks", "Custom Block", Path(PYPACKS_ROOT)/"assets"/"images"/"reference_book_icons"/"custom_block_icon.png")


@dataclass
class RefBookConfig:
    category: "RefBookCategory" = MISC_REF_BOOK_CATEGORY
    description: str = "No description provided for this item"
    hidden: bool = field(kw_only=True, default=False)
    wiki_link: str | None = field(kw_only=True, default=None)

    def __post_init__(self) -> None:
        assert self.wiki_link is None


MISC_REF_BOOK_CONFIG = RefBookConfig(category=MISC_REF_BOOK_CATEGORY, description="No description provided for this item")
PAINTING_REF_BOOK_CONFIG = RefBookConfig(category=PAINTING_REF_BOOK_CATEGORY, description="A custom painting, added by this pack!")
CUSTOM_BLOCKS_REF_BOOK_CONFIG = RefBookConfig(category=CUSTOM_BLOCKS_REF_BOOK_CATEGORY, description="A custom block, added by this pack!")
