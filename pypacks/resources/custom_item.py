import json
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal

from pypacks.additions.reference_book_config import MISC_REF_BOOK_CONFIG
from pypacks.additions.item_components import Components, AttributeModifier, Consumable, Food, TooltipDisplay
from pypacks.additions.raycasting import Raycast
from pypacks.additions.text import Text
from pypacks.resources.custom_advancement import CustomAdvancement, Criteria
from pypacks.resources.custom_model import CustomItemTexture, SlabModel
from pypacks.resources.custom_mcfunction import MCFunction
from pypacks.resources.custom_model import CustomItemRenderDefinition
from pypacks.image_manipulation.built_in_resolving import resolve_default_item_image
from pypacks.utils import recursively_remove_nones_from_data

from pypacks.scripts.repos.all_items import MinecraftItem

if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.additions.reference_book_config import RefBookConfig


@dataclass
class CustomItem:
    internal_name: str  # Internal name of the item
    base_item: MinecraftItem  # What item to base it on
    custom_name: str | Text | dict[str, Any] | None = None  # Display name of the item
    lore: list[str] = field(repr=False, default_factory=list)  # Lore of the item
    max_stack_size: int = field(repr=False, default=64)  # Max stack size of the item (1-99)
    rarity: Literal["common", "uncommon", "rare", "epic"] | None = field(repr=False, default=None)
    texture_path: str | None = field(repr=False, default=None)
    item_model: "str | CustomItemRenderDefinition | None" = field(repr=False, default=None)
    custom_data: dict[str, Any] = field(repr=False, default_factory=dict)
    on_right_click: "str | MCFunction | Raycast | None" = field(repr=False, default=None)  # Command/Function/Raycast to call when the item is right clicked
    on_item_drop: "str | MCFunction | None" = field(repr=False, default=None)  # Command/Function to call when the item is dropped
    components: "Components" = field(repr=False, default_factory=lambda: Components())
    ref_book_config: "RefBookConfig" = field(repr=False, default_factory=lambda: MISC_REF_BOOK_CONFIG)

    is_block: bool = field(init=False, repr=False, hash=False, default=False)
    datapack_subdirectory_name: None = field(init=False, repr=False, hash=False, default=None)

    def __post_init__(self) -> None:
        assert not (self.texture_path and self.item_model), "You can't have both a texture path and an item model!"
        if self.on_right_click:
            self.add_right_click_components()
        if self.on_item_drop:
            self.custom_data["on_drop_command"] = self.on_item_drop

        # TODO: Rework this, instead, just make a custom item model here instead...
        # from pypacks.resources.custom_model import CustomItemRenderDefinition, ModelItemModel
        # custom_item_model = CustomItemRenderDefinition(self.internal_name, ModelItemModel(self.texture_path), self.base_item)
        self.path_to_item_texture = self.texture_path if self.texture_path is not None else resolve_default_item_image(self.base_item)
        self.custom_item_texture = CustomItemTexture(self.internal_name, self.path_to_item_texture) if self.texture_path is not None else None

        self.use_right_click_cooldown = getattr(getattr(self.components, "cooldown", None), "seconds", None)
        Components.verify_compatible_components(self)

    def __str__(self) -> "str":
        return self.base_item  # This is used so we can cast CustomItem | str to string and always get a minecraft item

    def __hash__(self) -> int:
        return hash(self.internal_name)

    def create_resource_pack_files(self, pack: "Pack") -> None:
        from pypacks.resources.custom_model import CustomTexture
        # If it has a custom texture, create it, but not if it's a block (that gets done by the custom block code)
        if self.custom_item_texture is not None and not self.is_block:
            self.custom_item_texture.create_resource_pack_files(pack)
        if self.item_model is not None and isinstance(self.item_model, (SlabModel, CustomItemRenderDefinition)):
            self.item_model.create_resource_pack_files(pack)
        if self.components and self.components.equippable is not None and isinstance(self.components.equippable.camera_overlay, CustomTexture):
            self.components.equippable.camera_overlay.create_resource_pack_files(pack)

    def create_datapack_files(self, pack: "Pack") -> None:
        # Create the give command for use in books
        MCFunction(self.internal_name, [self.generate_give_command(pack.namespace)], ["give"]).create_datapack_files(pack)
        # If they pass in a temporary raycast or MCFunction, create them like normal
        if isinstance(self.on_right_click, (Raycast, MCFunction)):
            self.on_right_click.create_datapack_files(pack)
        if isinstance(self.on_item_drop, (Raycast, MCFunction)):
            self.on_item_drop.create_datapack_files(pack)

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        # TODO: Clean this up
        if self.item_model:
            item_model: str | None = self.item_model.get_reference(pack_namespace) if isinstance(self.item_model, (SlabModel, CustomItemRenderDefinition)) else self.item_model
        else:
            item_model = self.custom_item_texture.get_reference(pack_namespace) if self.custom_item_texture is not None else self.texture_path
        if isinstance(self.on_item_drop, MCFunction):  # TODO: Somehow improve this?
            self.custom_data["on_drop_command"] = self.on_item_drop.get_run_command(pack_namespace)
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "custom_name": Text.make_white_and_remove_italics(self.custom_name) if self.custom_name is not None else None,
            "lore": [Text.remove_italics(line) for line in self.lore] if self.lore else None,
            "max_stack_size": self.max_stack_size if self.max_stack_size != 64 else None,
            "rarity": self.rarity,
            "item_model": item_model,
            "custom_data": self.custom_data if self.custom_data else None,
            **self.components.to_dict(pack_namespace),
        })

    @classmethod
    def from_dict(cls, internal_name: str, base_item: MinecraftItem, data: dict[str, Any]) -> "CustomItem":
        return cls(
            internal_name,
            base_item,
            custom_name=data.get("custom_name"),
            lore=data.get("lore", []),
            max_stack_size=data.get("max_stack_size", 64),
            rarity=data.get("rarity"),
            texture_path=None,  # data.get("texture_path"),  # TODO: Look more into this
            item_model=data.get("item_model"),
            custom_data=data.get("custom_data", {}),
            on_right_click=None,  # TODO: Look more into this, maybe only support pypacks on_right_click?
            on_item_drop=None,  # TODO: Look more into this
            components=Components.from_dict(data),
            ref_book_config=MISC_REF_BOOK_CONFIG,
        )

    @staticmethod
    def to_component_string(obj: dict[str, Any]) -> str:
        replacee, replacer = "\\\\", "\\"
        return ", ".join([f"{key}={json.dumps(recursively_remove_nones_from_data(val)).replace(replacee, replacer)}" for key, val in obj.items() if val is not None])

    def generate_give_command(self, pack_namespace: str) -> str:
        return f"give @p {self.base_item}[{self.to_component_string(self.to_dict(pack_namespace))}]"

    # =============================================
    # Right click

    def add_right_click_components(self) -> None:
        """Adds the consuamble and food components to the item (so we can detect right clicks)"""
        if self.components.consumable is not None or self.components.food is not None:
            raise ValueError("You can't have both on_right_click and consumable/food!")
        if (
            self.components.attribute_modifiers is not None and
            any(x for x in self.components.attribute_modifiers if x.attribute_type == "block_interaction_range") is None
        ):
            raise ValueError("You can't have both on_right_click and block_interaction_range!")
        self.components.consumable = Consumable(consume_seconds=1_000_000, animation="none", consuming_sound=None, has_consume_particles=False)
        self.components.food = Food(nutrition=0, saturation=0, can_always_eat=True)
        self.custom_data |= {f"custom_right_click_for_{self.internal_name}": True}  # self.on_right_click.get_run_command()
        # Make sure we can't interact with blocks (e.g. place blocks or spawn eggs)
        self.components.attribute_modifiers.append(AttributeModifier(attribute_type="block_interaction_range", slot="mainhand", amount=-1000, operation="add_value"))
        if self.components.tooltip_display is None:
            self.components.tooltip_display = TooltipDisplay(hide_tooltip=False, hidden_components=[])
        self.components.tooltip_display.hidden_components.append("minecraft:attribute_modifiers")

    def generate_right_click_advancement(self, pack_namespace: str) -> "CustomAdvancement":
        criteria = Criteria(f"eating_{self.internal_name}", "minecraft:using_item", {
            "item": {
                "predicates": {  # We use predicates instead of components because components require exact match, predicates require minimum match
                    "minecraft:custom_data": {f"custom_right_click_for_{self.internal_name}": True},
                },
            }
        })
        eating_advancement = CustomAdvancement(
            f"custom_right_click_for_{self.internal_name}", [criteria],
            hidden=True, rewarded_function=f"{pack_namespace}:right_click/{self.internal_name}"
        )
        return eating_advancement

    def create_right_click_revoke_advancement_function(self, pack_namespace: str) -> MCFunction:
        revoke_and_call_mcfunction = MCFunction(
            self.internal_name, [
                f"advancement revoke @s only {self.generate_right_click_advancement(pack_namespace).get_reference(pack_namespace)}",
            ], ["right_click"]
        )
        run_code = self.on_right_click.get_run_command(pack_namespace) if isinstance(self.on_right_click, (MCFunction, Raycast)) else self.on_right_click
        if self.use_right_click_cooldown is not None:
            action_bar_command = f'title @s actionbar {{"text": "Cooldown: ", "color": "red", "extra": [{{"score": {{"name": "@s", "objective": "{self.internal_name}_cooldown"}}}}, {{"text": " ticks"}}]}}'
            revoke_and_call_mcfunction.commands.extend([
                f"execute as @a[scores={{{self.internal_name}_cooldown=1..}}] run {action_bar_command}",
                f"execute as @s[scores={{{self.internal_name}_cooldown=0}}] run {run_code}",
                f"execute as @a[scores={{{self.internal_name}_cooldown=0}}] run scoreboard players set @s {self.internal_name}_cooldown {int(self.use_right_click_cooldown*20)}",
            ])
        else:
            revoke_and_call_mcfunction.commands.append(run_code)  # type: ignore[arg-type]

        return revoke_and_call_mcfunction

    # ======
    # Drop logic

    @staticmethod
    def generate_on_drop_execute_loop(pack_namespace: str) -> tuple[MCFunction, MCFunction]:
        # Inspired by https://far.ddns.me/?share=SZQhBwxiLH
        # 1. Clear the storage
        # 2. Create an empty Compound (dict) in the storage, command
        # 3. Set the command to the on_drop_command
        # 4. Call the function that will run the command (which is a namespaced {command: <command>})
        # The key of the compound is the macro name, the value is the value of the compound.
        apply_and_execute = MCFunction("apply_and_execute", [
            f"tag @s add {pack_namespace}_processed_drop",
            f"data remove storage {pack_namespace}:drop_command command",
            "data modify storage pypacks_testing:drop_command command set value {\"command\": \"\"}",
            "data modify storage pypacks_testing:drop_command command.command set from entity @s Item.components.\"minecraft:custom_data\".on_drop_command",
            # Need to apply the tag
            f"execute as @s run function {pack_namespace}:utils/run_macro_function with storage {pack_namespace}:drop_command command",
            ], ["on_drop"],
        )
        drop_detection = MCFunction("drop_detection", [
            f"execute as @e[type=item, tag=!{pack_namespace}_processed_drop] run {apply_and_execute.get_run_command(pack_namespace)}",
            ], ["on_drop"],
        )
        return apply_and_execute, drop_detection
