import json
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from pypacks.image_manipulation.ref_book_icon_gen import add_centered_overlay
from pypacks.reference_book_config import MISC_REF_BOOK_CONFIG
from pypacks.resources.item_components import Consumable, Food, CustomItemData
from pypacks.resources.mcfunction import MCFunction
from pypacks.utils import to_component_string, colour_codes_to_json_format, resolve_default_item_image, recusively_remove_nones_from_dict

if TYPE_CHECKING:
    from pypacks.datapack import Datapack
    from pypacks.reference_book_config import RefBookConfig


@dataclass
class CustomItem:
    base_item: str  # What item to base it on
    internal_name: str  # Internal name of the item
    custom_name: str | None = None  # Display name of the item
    lore: list[str] = field(repr=False, default_factory=list)  # Lore of the item
    max_stack_size: int = field(repr=False, default=64)  # Max stack size of the item (1-99)
    rarity: Literal["common", "uncommon", "rare", "epic"] | None = field(repr=False, default=None)
    texture_path: str | None = field(repr=False, default=None)
    custom_data: dict[str, Any] = field(repr=False, default_factory=dict)  # Is populated in post_init if it's none
    on_right_click: str | None = None  # Function to call when the item is right clicked
    additional_item_data: "CustomItemData | None" = field(repr=False, default=None)
    ref_book_config: "RefBookConfig" = field(repr=False, default=MISC_REF_BOOK_CONFIG)

    is_block: bool = field(init=False, repr=False, default=False)
    datapack_subdirectory_name: None = field(init=False, repr=False, default=None)

    def __post_init__(self) -> None:
        if self.on_right_click and self.additional_item_data is not None and (
            self.additional_item_data.consumable is not None or self.additional_item_data.food is not None
        ):
            raise ValueError("You can't have both on_right_click and consumable/food!")
        self.custom_data |= {"pypacks_custom_item": self.internal_name}

        if self.on_right_click:
            self.add_right_click_functionality()

        path: str | Path = self.texture_path if self.texture_path is not None else resolve_default_item_image(self.base_item)
        with open(path, mode="rb") as file:
            self.icon_image_bytes = add_centered_overlay(image_bytes=file.read())

        self.use_right_click_cooldown = getattr(getattr(self.additional_item_data, "cooldown", None), "seconds", None)
        
        if self.additional_item_data is not None:
            for value in self.additional_item_data.__dict__.values():
                if hasattr(value, "allowed_items"):
                    assert self.base_item.removeprefix("minecraft:") in value.allowed_items, f"{value.__class__.__name__} can only be used with {' and '.join(value.allowed_items)}, not {self.base_item}"

    def __str__(self) -> "str":
        return self.base_item  # This is used so we can cast CustomItem | str to string and always get a minecraft item

    def add_right_click_functionality(self) -> None:
        """Adds the consuamble and food components to the item (so we can detect right clicks)"""
        consumable = Consumable(consume_seconds=1_000_000, animation="none", sound=None, has_consume_particles=False)
        food = Food(nutrition=0, saturation=0, can_always_eat=True)
        tag = {f"custom_right_click_for_{self.internal_name}": True}
        if self.additional_item_data:
            self.additional_item_data.consumable = consumable
            self.additional_item_data.food = food
        else:
            self.additional_item_data = CustomItemData(consumable=consumable, food=food)
        self.custom_data |= tag

    def create_resource_pack_files(self, datapack: "Datapack") -> None:
        # The resource pack requires 3 things:
        # 1. The model definition/config (in items/<internal_name>.json)
        # 2. The model components, including textures, parent, etc. (in models/item/<internal_name>.json)
        # 3. The texture itself (in textures/item/<internal_name>.png)

        if self.texture_path is not None:
            os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"models"/"item", exist_ok=True)
            os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"items", exist_ok=True)
            os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"textures"/"item", exist_ok=True)
            os.makedirs(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"textures"/"font", exist_ok=True)

            layers = {("all" if self.is_block else "layer0"): f"{datapack.namespace}:item/{self.internal_name}"}
            parent = "minecraft:block/cube_all" if self.is_block else "minecraft:item/generated"
            with open(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"models"/"item"/f"{self.internal_name}.json", "w") as file:
                json.dump({"parent": parent, "textures": layers}, file, indent=4)

            with open(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"items"/f"{self.internal_name}.json", "w") as file:
                json.dump({"model": {"type": "minecraft:model", "model": f"{datapack.namespace}:item/{self.internal_name}"}}, file, indent=4)

            shutil.copyfile(self.texture_path, Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"textures"/"item"/f"{self.internal_name}.png")

        # Create the icons for the custom items
        with open(Path(datapack.resource_pack_path)/"assets"/datapack.namespace/"textures"/"font"/f"{self.internal_name}_icon.png", "wb") as file:
            file.write(self.icon_image_bytes)

    def create_datapack_files(self, datapack: "Datapack") -> None:
        # Create the give command for use in books
        with open(Path(datapack.datapack_output_path)/"data"/datapack.namespace/"function"/"give"/f"{self.internal_name}.mcfunction", "w") as file:
            file.write(self.generate_give_command(datapack))

    def create_right_click_revoke_advancement_function(self, datapack: "Datapack") -> MCFunction:
        revoke_and_call_mcfunction = MCFunction(
            self.internal_name, [
                f"advancement revoke @s only {datapack.namespace}:custom_right_click_for_{self.internal_name}",
            ], ["right_click"]
        )
        if self.use_right_click_cooldown is not None:
            action_bar_command = f'title @s actionbar {{"text": "Cooldown: ", "color": "red", "extra": [{{"score": {{"name": "@s", "objective": "{self.internal_name}_cooldown"}}}}, {{"text": " ticks"}}]}}'
            revoke_and_call_mcfunction.commands.extend([
                f"execute as @a[scores={{{self.internal_name}_cooldown=1..}}] run {action_bar_command}",
                f"execute as @s[scores={{{self.internal_name}_cooldown=0}}] run {self.on_right_click}",
                f"execute as @a[scores={{{self.internal_name}_cooldown=0}}] run scoreboard players set @s {self.internal_name}_cooldown {self.use_right_click_cooldown*20}",
            ])
        else:
            revoke_and_call_mcfunction.commands.append(self.on_right_click)  # type: ignore[arg-type]

        return revoke_and_call_mcfunction

    def to_dict(self, datapack_namespace: str) -> dict[str, Any]:
        return recusively_remove_nones_from_dict({
            "custom_name": colour_codes_to_json_format(self.custom_name, auto_unitalicise=True) if self.custom_name is not None else None,
            "lore": [colour_codes_to_json_format(line) for line in self.lore] if self.lore else None,
            "max_stack_size": self.max_stack_size if self.max_stack_size != 64 else None,
            "rarity": self.rarity,
            "item_model": f"{datapack_namespace}:{self.internal_name}" if self.texture_path else None,
            "custom_data": self.custom_data,
            # "additional_item_data": self.additional_item_data.to_dict() if self.additional_item_data else None,
        })

    def generate_give_command(self, datapack: "Datapack") -> str:
        components = ", ".join([
            to_component_string({key: value})
            for key, value in self.to_dict(datapack.namespace).items()
        ])
        additional_item_data_string = (
            to_component_string(self.additional_item_data.to_dict(datapack))  # Also strips None
            if self.additional_item_data else None
        )
        # TODO: Figure out a way to not have to do this?
        if self.base_item.removeprefix("minecraft:") in ["writable_book", "written_book"] and additional_item_data_string is not None:
            additional_item_data_string = additional_item_data_string.replace("\\\\", "\\").replace("\\n", "\\\\n")
        return f"give @p {self.base_item}[{components}{', ' if components and additional_item_data_string else ''}{additional_item_data_string if additional_item_data_string else ''}]"
