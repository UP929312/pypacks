from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal

from pypacks.additions.reference_book_config import MISC_REF_BOOK_CONFIG
from pypacks.additions.item_components import Consumable, Food, Components
from pypacks.resources.custom_model import CustomTexture
from pypacks.resources.custom_mcfunction import MCFunction
from pypacks.resources.custom_model import CustomItemModelDefinition
from pypacks.image_manipulation.built_in_resolving import resolve_default_item_image
from pypacks.utils import to_component_string, colour_codes_to_json_format, recursively_remove_nones_from_data

from pypacks.scripts.repos.all_items import MinecraftItem

if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.additions.reference_book_config import RefBookConfig


@dataclass
class CustomItem:
    internal_name: str  # Internal name of the item
    base_item: MinecraftItem  # What item to base it on
    custom_name: str | None = None  # Display name of the item
    lore: list[str] = field(repr=False, default_factory=list)  # Lore of the item
    max_stack_size: int = field(repr=False, default=64)  # Max stack size of the item (1-99)
    rarity: Literal["common", "uncommon", "rare", "epic"] | None = field(repr=False, default=None)
    texture_path: str | None = field(repr=False, default=None)
    item_model: "str | CustomItemModelDefinition | None" = field(repr=False, default=None)
    custom_data: dict[str, Any] = field(repr=False, default_factory=dict)  # Is populated in post_init if it's none
    on_right_click: "str | MCFunction | None" = None  # Function to call when the item is right clicked
    components: "Components" = field(repr=False, default_factory=lambda: Components())
    ref_book_config: "RefBookConfig" = field(repr=False, default=MISC_REF_BOOK_CONFIG)

    is_block: bool = field(init=False, repr=False, default=False)
    datapack_subdirectory_name: None = field(init=False, repr=False, default=None)

    def __post_init__(self) -> None:
        assert not (self.texture_path and self.item_model), "You can't have both a texture path and an item model!"
        if self.on_right_click:
            if self.components.consumable is not None or self.components.food is not None:
                raise ValueError("You can't have both on_right_click and consumable/food!")
            self.add_right_click_functionality()

        # TODO: Rework this, instead, just make a custom item model here instead...
        path: str | Path = self.texture_path if self.texture_path is not None else resolve_default_item_image(self.base_item)
        # from pypacks.resources.custom_model import ModelItemModel
        # custom_item_model = CustomItemModelDefinition(self.internal_name, ModelItemModel(path), self.base_item)
        with open(path, mode="rb") as file:
            self.image_bytes = file.read()

        self.use_right_click_cooldown = getattr(getattr(self.components, "cooldown", None), "seconds", None)

        if self.components is not None:
            for value in self.components.__dict__.values():
                if hasattr(value, "allowed_items"):
                    assert self.base_item.removeprefix("minecraft:") in value.allowed_items, (
                        f"{value.__class__.__name__} can only be used with {' and '.join(value.allowed_items)}, not {self.base_item}"
                    )

    def __str__(self) -> "str":
        return self.base_item  # This is used so we can cast CustomItem | str to string and always get a minecraft item

    def __hash__(self) -> int:
        return hash(self.internal_name)

    def add_right_click_functionality(self) -> None:
        """Adds the consuamble and food components to the item (so we can detect right clicks)"""
        self.components.consumable = Consumable(consume_seconds=1_000_000, animation="none", consuming_sound=None, has_consume_particles=False)
        self.components.food = Food(nutrition=0, saturation=0, can_always_eat=True)
        self.custom_data |= {f"custom_right_click_for_{self.internal_name}": True}

    def create_resource_pack_files(self, pack: "Pack") -> None:
        # If it has a custom texture, create it, but not if it's a block (that gets done by the custom block code)
        if self.texture_path is not None and not self.is_block:
            CustomTexture(self.internal_name, self.image_bytes).create_resource_pack_files(pack)
        # TODO: Should this exist here? I mean, it's a sub_item creating more resources, but maybe that's fine?
        if self.item_model is not None and isinstance(self.item_model, CustomItemModelDefinition):
            self.item_model.create_resource_pack_files(pack)

    def create_datapack_files(self, pack: "Pack") -> None:
        # Create the give command for use in books
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/"function"/"give"/f"{self.internal_name}.mcfunction", "w") as file:
            file.write(self.generate_give_command(pack.namespace))

    def create_right_click_revoke_advancement_function(self, pack_namespace: str) -> MCFunction:
        revoke_and_call_mcfunction = MCFunction(
            self.internal_name, [
                f"advancement revoke @s only {pack_namespace}:custom_right_click_for_{self.internal_name}",
            ], ["right_click"]
        )
        run_code = f"function {self.on_right_click.get_reference(pack_namespace)}" if isinstance(self.on_right_click, MCFunction) else self.on_right_click
        if self.use_right_click_cooldown is not None:
            action_bar_command = f'title @s actionbar {{"text": "Cooldown: ", "color": "red", "extra": [{{"score": {{"name": "@s", "objective": "{self.internal_name}_cooldown"}}}}, {{"text": " ticks"}}]}}'
            revoke_and_call_mcfunction.commands.extend([
                f"execute as @a[scores={{{self.internal_name}_cooldown=1..}}] run {action_bar_command}",
                f"execute as @s[scores={{{self.internal_name}_cooldown=0}}] run {run_code}",
                f"execute as @a[scores={{{self.internal_name}_cooldown=0}}] run scoreboard players set @s {self.internal_name}_cooldown {self.use_right_click_cooldown*20}",
            ])
        else:
            revoke_and_call_mcfunction.commands.append(run_code)  # type: ignore[arg-type]

        return revoke_and_call_mcfunction

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        # TODO: Clean this up
        if self.item_model:
            item_model: str | None = self.item_model.get_reference(pack_namespace) if isinstance(self.item_model, CustomItemModelDefinition) else self.item_model
        else:
            item_model = f"{pack_namespace}:{self.internal_name}" if self.texture_path is not None else self.texture_path
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "custom_name": colour_codes_to_json_format(self.custom_name, auto_unitalicise=True, make_white=False) if self.custom_name is not None else None,
            "lore": [colour_codes_to_json_format(line) for line in self.lore] if self.lore else None,
            "max_stack_size": self.max_stack_size if self.max_stack_size != 64 else None,
            "rarity": self.rarity,
            "item_model": item_model,
            "custom_data": self.custom_data if self.custom_data else None,
            **self.components.to_dict(pack_namespace),
        })

    def generate_give_command(self, pack_namespace: str) -> str:
        return f"give @p {self.base_item}[{to_component_string(self.to_dict(pack_namespace))}]"
