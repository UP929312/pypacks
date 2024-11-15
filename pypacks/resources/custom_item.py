from typing import TYPE_CHECKING, Any, Literal

from pypacks.utils import to_component_string, to_snbt
from pypacks.resources.item_components import CustomItemData

if TYPE_CHECKING:
    from pypacks.datapack import Datapack

MODEL_FILE = """{
    "parent": "minecraft:item/generated",
    "textures": {
        "layer0": "%s"
    }
}"""

ITEM_FILE = """{
    "model": {
        "type": "minecraft:model",
        "model": "%s"
    }
}"""

# Added data component use_remainder, which can have a single item stack as value. If present, will replace the item if its stack count has decreased after use.
# Added data component use_cooldown. If present, will apply a cooldown to all items of the same type when it has been used. It is an object with fields seconds (positive float) and cooldownGroup (resource location). Weird casing is a typo and is corrected in the next snapshot.

class CustomItem:
    def __init__(
            self, base_item: str, item_id: str, custom_name: str | None = None, lore: list[str] | None = None,
            max_stack_size: int = 64, rarity: Literal["common", "uncommon", "rare", "epic"] | None = None,
            texture_path: str | None = None, custom_data: dict[str, Any] = {},
            additional_item_data: "CustomItemData | None" = None, book_category: str = "miscellaneous",
        ) -> None:
        """Name is the name of the item, item_id is the name of the files, e.g. model, texture, etc."""
        self.base_item = base_item
        self.item_id = item_id
        self.custom_name = custom_name
        self.lore = lore or []
        self.max_stack_size = max_stack_size
        self.rarity = rarity
        assert self.lore == [], "Lore is not yet supported"
        self.texture_path = texture_path
        self.custom_data = custom_data
        assert custom_data == {}, "custom_data is not yet supported"
        self.additional_item_data = additional_item_data
        self.book_category = book_category
        assert 0 < max_stack_size < 100, "max_stack_size must be between 1 and 99"
        
        # Equippable = "ARMOR" | "HAND"

    def create_model_file(self, namespace: str) -> str:
        return MODEL_FILE % f"{namespace}:item/{self.item_id}"

    def create_item_file(self, namespace: str) -> str:
        return ITEM_FILE % f"{namespace}:item/{self.item_id}"

    def create_resource_pack_files(self, datapack: "Datapack") -> None:
        if self.texture_path is not None:
            with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/models/item/{self.item_id}.json", "w") as f:
                f.write(self.create_model_file(datapack.namespace))
            with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/items/{self.item_id}.json", "w") as f:
                f.write(self.create_item_file(datapack.namespace))
            with open(self.texture_path, "rb") as f:
                image_contents = f.read()
            with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/item/{self.item_id}.png", "wb") as f:
                f.write(image_contents)

    def generate_give_command(self, datapack: "Datapack", namespace: str) -> str:
        item_name = to_component_string({"item_name": to_snbt({"text": self.custom_name})}) if self.custom_name else None
        max_stack_size = to_component_string({"max_stack_size": self.max_stack_size}) if self.max_stack_size != 64 else None
        rarity = to_component_string({"rarity": self.rarity}) if self.rarity is not None else None
        item_model = to_component_string({"minecraft:item_model": f"{namespace}:{self.item_id}"}) if self.texture_path else None
        additional_item_data_string = to_component_string(self.additional_item_data.to_dict()) if self.additional_item_data else None
        # TODO: Figure out a way to not need to do this?
        if self.base_item in ["minecraft:written_book", "written_book"] and additional_item_data_string is not None:
            additional_item_data_string = additional_item_data_string.replace("\\\\", "\\").replace("\\n", "\\\\n")
        all_custom_data = ", ".join([x for x in (item_name, max_stack_size, rarity, item_model, additional_item_data_string) if x is not None])
        return f"give @p {self.base_item}[{all_custom_data}]"
