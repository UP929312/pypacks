import json
import shutil
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal

from pypacks.utils import to_component_string, colour_codes_to_json_format, resolve_default_item_image, recusively_remove_nones_from_dict
from pypacks.resources.item_components import Consumable, Food, CustomItemData
from pypacks.image_generation import add_icon_to_base

if TYPE_CHECKING:
    from pypacks.book_generator import ReferenceBookCategory
    from pypacks.datapack import Datapack


@dataclass
class CustomItem:
    base_item: str  # What item to base it on
    internal_name: str  # Internal name of the item
    custom_name: str | None = None  # Display name of the item
    lore: list[str] = field(default_factory=list)  # Lore of the item
    max_stack_size: int = 64  # Max stack size of the item (1-99)
    rarity: Literal["common", "uncommon", "rare", "epic"] | None = None
    texture_path: str | None = None
    custom_data: dict[str, Any] = field(default_factory=dict)  # type: ignore[abc]   # Is populated in post_init if it's none
    on_right_click: str | None = None  # Function to call when the item is right clicked
    additional_item_data: "CustomItemData | None" = None
    reference_book_description: str | None = None
    book_category: "ReferenceBookCategory" = None  # type: ignore[abc]  # This is set in post_init

    is_block: bool = field(init=False, default=False)
    datapack_subdirectory_name: None = field(init=False, default=None)

    def __post_init__(self) -> None:
        if self.on_right_click and self.additional_item_data is not None and (
            self.additional_item_data.consumable is not None or self.additional_item_data.food is not None
        ):
            raise ValueError("You can't have both on_right_click and consumable/food!")

        from pypacks.book_generator import MISCELLANOUS_REF_BOOK_CATEGORY  # Circular imports
        if self.book_category is None:
            self.book_category = MISCELLANOUS_REF_BOOK_CATEGORY

        self.custom_data |= {"pypacks_custom_item": self.internal_name}

        if self.on_right_click:
            self.add_right_click_functionality()

        if self.texture_path is None:
            path = resolve_default_item_image(self.base_item)
            with open(path, "rb") as file:
                self.icon_image_bytes = add_icon_to_base(image_bytes=file.read())
        else:
            self.icon_image_bytes = add_icon_to_base(image_path=self.texture_path)

    def add_right_click_functionality(self) -> None:
        """Adds the consuamble and food components to the item (so we can detect right clicks)"""
        consumable = Consumable(consume_seconds=1_000_000, animation="none", sound=None, has_consume_particles=False)
        food = Food(nutrition=0, saturation=0, can_always_eat=True)
        # cooldown = Cooldown(5, f"custom_right_click_for_{self.internal_name}")
        tag = {f"custom_right_click_for_{self.internal_name}": True}
        if self.additional_item_data:
            self.additional_item_data.consumable = consumable
            self.additional_item_data.food = food
            # if self.additional_item_data.cooldown is None:
            #     self.additional_item_data.cooldown = cooldown
        else:
            self.additional_item_data = CustomItemData(consumable=consumable, food=food)  # , cooldown=cooldown
        self.custom_data |= tag

    def to_components_dict(self, datapack: "Datapack") -> dict[str, Any]:
        """Used for the results key in a recipe, DEPRECATED"""  # TODO: Remove this
        return self.to_dict(datapack)

    def create_resource_pack_files(self, datapack: "Datapack") -> None:
        # The resource pack requires 3 things:
        # 1. The model definition/config (in items/<internal_name>.json)
        # 2. The model components, including textures, parent, etc. (in models/item/<internal_name>.json)
        # 3. The texture itself (in textures/item/<internal_name>.png)

        if self.texture_path is not None:
            layers = {("all" if self.is_block else "layer0"): f"{datapack.namespace}:item/{self.internal_name}"}
            parent = "minecraft:block/cube_all" if self.is_block else "minecraft:item/generated" 
            with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/models/item/{self.internal_name}.json", "w") as file:
                json.dump({"parent": parent, "textures": layers}, file, indent=4)

            with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/items/{self.internal_name}.json", "w") as file:
                json.dump({"model": {"type": "minecraft:model", "model": f"{datapack.namespace}:item/{self.internal_name}"}}, file, indent=4)

            shutil.copyfile(self.texture_path, f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/item/{self.internal_name}.png")

        # Create the icons for the custom items
        with open(f"{datapack.resource_pack_path}/assets/{datapack.namespace}/textures/font/{self.internal_name}_icon.png", "wb") as file:
            file.write(self.icon_image_bytes)

    def create_datapack_files(self, datapack: "Datapack") -> None:
        # Create the give command for use in books
        with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/function/give/{self.internal_name}.mcfunction", "w") as file:
            file.write(self.generate_give_command(datapack))

        if self.on_right_click is not None:
            with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/function/right_click/{self.internal_name}.mcfunction", "w") as file:
                file.write(f"advancement revoke @s only {datapack.namespace}:custom_right_click_for_{self.internal_name}\n{self.on_right_click}")

    def to_dict(self, datapack: "Datapack") -> dict[str, Any]:
        return recusively_remove_nones_from_dict({
            "custom_name": colour_codes_to_json_format(self.custom_name, auto_unitalicise=True) if self.custom_name is not None else None,  # type: ignore
            "lore": [colour_codes_to_json_format(line) for line in self.lore] if self.lore else None,
            "max_stack_size": self.max_stack_size if self.max_stack_size != 64 else None,
            "rarity": self.rarity,
            "item_model": f"{datapack.namespace}:{self.internal_name}" if self.texture_path else None,
            "custom_data": self.custom_data,
            # "additional_item_data": self.additional_item_data.to_dict() if self.additional_item_data else None,
        })

    def generate_give_command(self, datapack: "Datapack") -> str:
        components = ", ".join([
            to_component_string({key: value})
            for key, value in self.to_dict(datapack).items()
        ])
        additional_item_data_string = to_component_string(self.additional_item_data.to_dict()) if self.additional_item_data else None  # Also strips None
        # TODO: Figure out a way to not have to do this?
        if self.base_item in ["minecraft:written_book", "written_book"] and additional_item_data_string is not None:
            additional_item_data_string = additional_item_data_string.replace("\\\\", "\\").replace("\\n", "\\\\n")
        return f"give @p {self.base_item}[{components}{', ' if components and additional_item_data_string else ''}{additional_item_data_string if additional_item_data_string else ''}]"
