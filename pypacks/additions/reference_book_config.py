from dataclasses import dataclass, field
from pathlib import Path

from pypacks.utils import IMAGES_PATH


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


MISC_REF_BOOK_CATEGORY = RefBookCategory("misc", "Misc", IMAGES_PATH/"reference_book_icons"/"miscellaneous_icon.png")
PAINTING_REF_BOOK_CATEGORY = RefBookCategory("paintings", "Paintings", IMAGES_PATH/"reference_book_icons"/"painting.png")
CUSTOM_BLOCKS_REF_BOOK_CATEGORY = RefBookCategory("custom_blocks", "Custom Block", IMAGES_PATH/"reference_book_icons"/"custom_block_icon.png")
DEV_ITEMS_REF_BOOK_CATEGORY = RefBookCategory("dev_items", "Dev Items", IMAGES_PATH/"reference_book_icons"/"dev_items_icon.png")


@dataclass
class RefBookConfig:
    category: "RefBookCategory" = field(default_factory=lambda: MISC_REF_BOOK_CATEGORY)
    description: str = "No description provided for this item"
    hidden: bool = field(kw_only=True, default=False)
    # wiki_link: str | None = field(kw_only=True, default=None)

    # def __post_init__(self) -> None:
    #     assert self.wiki_link is None


MISC_REF_BOOK_CONFIG = RefBookConfig(category=MISC_REF_BOOK_CATEGORY, description="No description provided for this item")
PAINTING_REF_BOOK_CONFIG = RefBookConfig(category=PAINTING_REF_BOOK_CATEGORY, description="A custom painting, added by this pack!")
CUSTOM_BLOCKS_REF_BOOK_CONFIG = RefBookConfig(category=CUSTOM_BLOCKS_REF_BOOK_CATEGORY, description="A custom block, added by this pack!")
DEV_ITEMS_REF_BOOK_CONFIG = RefBookConfig(category=DEV_ITEMS_REF_BOOK_CATEGORY, description="A dev item, added by this pack!")
HIDDEN_REF_BOOK_CONFIG = RefBookConfig(hidden=True)
