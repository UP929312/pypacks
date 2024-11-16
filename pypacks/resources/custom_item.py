import json
import shutil
from typing import TYPE_CHECKING, Any, Literal

from pypacks.utils import PYPACKS_ROOT, to_component_string, to_snbt
from pypacks.image_generation import add_icon_to_base

if TYPE_CHECKING:
    from pypacks.resources.item_components import CustomItemData
    from pypacks.book_generator import ReferenceBookCategory
    from pypacks.datapack import Datapack


class CustomItem:
    def __init__(
            self, base_item: str, item_id: str, custom_name: str | None = None, lore: list[str] | None = None,
            max_stack_size: int = 64, rarity: Literal["common", "uncommon", "rare", "epic"] | None = None,
            texture_path: str | None = None, custom_data: dict[str, Any] = {},
            additional_item_data: "CustomItemData | None" = None, book_category: "ReferenceBookCategory | None" = None,
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

        from pypacks.book_generator import ReferenceBookCategory  # Circular imports
        self.book_category = book_category or ReferenceBookCategory("Miscellaneous", f"{PYPACKS_ROOT}/assets/images/miscellaneous_icon.png")
        assert 0 < max_stack_size < 100, "max_stack_size must be between 1 and 99"

        if self.texture_path is None:
            with open(f"{PYPACKS_ROOT}/assets/minecraft/item/{self.base_item.removeprefix('minecraft:')}.png", "rb") as f:
                self.icon_image_bytes = add_icon_to_base(image_bytes=f.read())
        else:
            self.icon_image_bytes = add_icon_to_base(image_path=self.texture_path) 

    def create_resource_pack_files(self, datapack: "Datapack") -> None:
        if self.texture_path is not None:
            with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/models/item/{self.item_id}.json", "w") as f:
                json.dump({"parent": "minecraft:item/generated", "textures": {"layer0": f"{datapack.namespace}:item/{self.item_id}"}}, f, indent=4)
            with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/items/{self.item_id}.json", "w") as f:
                json.dump({"model": {"type": "minecraft:model", "model": f"{datapack.namespace}:item/{self.item_id}"}}, f, indent=4)
            shutil.copyfile(self.texture_path, f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/item/{self.item_id}.png")

        # Create the icons for the custom items
        with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/font/{self.item_id}_icon.png", "wb") as file:
            file.write(self.icon_image_bytes)

    def generate_give_command(self, datapack: "Datapack") -> str:
        item_name = to_component_string({"item_name": to_snbt({"text": self.custom_name})}) if self.custom_name else None
        max_stack_size = to_component_string({"max_stack_size": self.max_stack_size}) if self.max_stack_size != 64 else None
        rarity = to_component_string({"rarity": self.rarity}) if self.rarity is not None else None
        item_model = to_component_string({"minecraft:item_model": f"{datapack.namespace}:{self.item_id}"}) if self.texture_path else None
        additional_item_data_string = to_component_string(self.additional_item_data.to_dict()) if self.additional_item_data else None
        # TODO: Figure out a way to not need to do this?
        if self.base_item in ["minecraft:written_book", "written_book"] and additional_item_data_string is not None:
            additional_item_data_string = additional_item_data_string.replace("\\\\", "\\").replace("\\n", "\\\\n")
        all_custom_data = ", ".join([x for x in (item_name, max_stack_size, rarity, item_model, additional_item_data_string) if x is not None])
        return f"give @p {self.base_item}[{all_custom_data}]"
