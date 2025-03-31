from dataclasses import dataclass, field
from typing import Literal, Any, TYPE_CHECKING

from pypacks.resources.base_resource import BaseResource
from pypacks.utils import recursively_remove_nones_from_data

if TYPE_CHECKING:
    from pypacks.resources.custom_mcfunction import MCFunction
    from pypacks.resources.custom_loot_tables import CustomLootTable
    from pypacks.resources.custom_recipe import Recipe

TriggerType = Literal[
    # https://minecraft.wiki/w/Advancement_definition#List_of_triggers
    "minecraft:allay_drop_item_on_block", "minecraft:any_block_use", "minecraft:avoid_vibration", "minecraft:bee_nest_destroyed",
    "minecraft:bred_animals", "minecraft:brewed_potion", "minecraft:changed_dimension", "minecraft:channeled_lightning",
    "minecraft:construct_beacon", "minecraft:consume_item", "minecraft:crafter_recipe_crafted", "minecraft:cured_zombie_villager",
    "minecraft:default_block_use", "minecraft:effects_changed", "minecraft:enchanted_item", "minecraft:enter_block",
    "minecraft:entity_hurt_player", "minecraft:entity_killed_player", "minecraft:fall_after_explosion", "minecraft:fall_from_height",
    "minecraft:filled_bucket", "minecraft:fishing_rod_hooked", "minecraft:hero_of_the_village", "minecraft:impossible",
    "minecraft:inventory_changed", "minecraft:item_durability_changed", "minecraft:item_used_on_block",
    "minecraft:kill_mob_near_sculk_catalyst", "minecraft:killed_by_arrow", "minecraft:levitation", "minecraft:lightning_strike",
    "minecraft:location", "minecraft:nether_travel", "minecraft:placed_block", "minecraft:player_generates_container_loot",
    "minecraft:player_hurt_entity", "minecraft:player_interacted_with_entity", "minecraft:player_killed_entity", "minecraft:recipe_crafted",
    "minecraft:recipe_unlocked", "minecraft:ride_entity_in_lava", "minecraft:shot_crossbow", "minecraft:slept_in_bed",
    "minecraft:slide_down_block", "minecraft:started_riding", "minecraft:summoned_entity", "minecraft:tame_animal", "minecraft:target_hit",
    "minecraft:thrown_item_picked_up_by_entity", "minecraft:thrown_item_picked_up_by_player", "minecraft:tick", "minecraft:used_ender_eye",
    "minecraft:used_totem", "minecraft:using_item", "minecraft:villager_trade"
]


@dataclass
class Criteria:
    """A requirement for an advancement."""
    name: str
    trigger: TriggerType
    conditions: dict[str, Any]  # TODO: Type this ):

    def to_dict(self) -> dict[str, Any]:
        return {
            "trigger": self.trigger,
            "conditions": self.conditions if self.conditions else None,
        }

    @classmethod
    def from_dict(cls, name: str, data: dict[str, Any]) -> "Criteria":
        return cls(
            name=name,
            trigger=data["trigger"],
            conditions=data.get("conditions", {}),
        )


@dataclass
class CustomAdvancement(BaseResource):
    """Rewarded loot is the reference to a LootTable"""
    # https://minecraft.wiki/w/Advancement_definition
    internal_name: str
    criteria: list[Criteria]
    rewarded_loot_tables: list["str | CustomLootTable"] = field(repr=False, default_factory=list)  # The resource location of a loot table.
    rewarded_recipes: list["str | Recipe"] = field(repr=False, default_factory=list)  # The resource location of a recipe.
    rewarded_experience: int = field(repr=False, default=0)  # To give an amount of experience. Defaults to 0.
    rewarded_function: "str | MCFunction | None" = field(default=None)  # To run a function. Function tags are not allowed.
    hidden: bool = False

    title: str = "Unknown"
    description: str = "Unknown"
    parent: str | None = None
    icon_item: str = "minecraft:target"
    frame: Literal["task", "challenge", "goal"] = "task"
    root_background: str = "minecraft:textures/gui/advancements/backgrounds/adventure.png"
    show_toast: bool = True
    announce_to_chat: bool = False
    send_telemetry_event: bool = False

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="advancement")

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        from pypacks.resources.custom_mcfunction import MCFunction
        return recursively_remove_nones_from_data({  # type: ignore[no-any-return]
            "parent": self.parent,
            "display": {
                "icon": {"id": self.icon_item},
                "title": self.title,  # {"text": self.title},
                "description": self.description,  # {"text": self.description},
                "frame": self.frame if self.frame != "task" else None,
                "background": "minecraft:textures/gui/advancements/backgrounds/adventure.png",
                "show_toast": False if not self.show_toast else None,
                "announce_to_chat": False if not self.announce_to_chat else None,
            } if not self.hidden else None,
            "criteria": {
                criteriom.name: criteriom.to_dict() for criteriom in self.criteria
            },
            "requirements": [[x.name] for x in self.criteria],
            "rewards": {
                "experience": self.rewarded_experience or None,
                "recipes": [x.get_reference(pack_namespace) if isinstance(x, Recipe) else x for x in self.rewarded_recipes] or None,
                "loot": [x.get_reference(pack_namespace) if isinstance(x, CustomLootTable) else x for x in self.rewarded_loot_tables] or None,
                "function": self.rewarded_function.get_reference(pack_namespace) if isinstance(self.rewarded_function, MCFunction) else self.rewarded_function,
            },
            "sends_telemetry_event": True if self.send_telemetry_event else None,
        })

    @classmethod
    def from_dict(cls, internal_name: str, data: dict[str, Any]) -> "CustomAdvancement":
        return cls(
            internal_name,
            criteria=[Criteria.from_dict(key, value) for key, value in data["criteria"].items()],
            rewarded_loot_tables=data.get("rewarded_loot") or [],
            rewarded_recipes=data.get("rewarded_recipes") or [],
            rewarded_experience=data.get("rewarded_experience", 0),
            rewarded_function=data.get("rewarded_function"),
            hidden=data.get("hidden", False),
            title=data.get("title", "Unknown"),
            description=data.get("description", "Unknown"),
            parent=data.get("parent"),
            icon_item=data.get("icon_item", "minecraft:target"),
            frame=data.get("frame", "task"),
            root_background=data.get("root_background", "minecraft:textures/gui/advancements/backgrounds/adventure.png"),
            show_toast=data.get("show_toast", True),
            announce_to_chat=data.get("announce_to_chat", False),
            send_telemetry_event=data.get("send_telemetry_event", False),
        )

    def generate_grant_command(self) -> str:
        return f"advancement grant @s only {self.internal_name}"

    def generate_revoke_command(self) -> str:
        return f"advancement revoke @s only {self.internal_name}"

    __repr__ = BaseResource.__repr__
