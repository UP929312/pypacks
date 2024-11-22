import json
from typing import Literal, Any, TYPE_CHECKING
from dataclasses import dataclass

from pypacks.utils import recusively_remove_nones_from_dict

if TYPE_CHECKING:
    from pypacks.datapack import Datapack
    from pypacks.resources.custom_item import CustomItem

TriggerType = Literal["minecraft:allay_drop_item_on_block", "minecraft:any_block_use", "minecraft:avoid_vibration", "minecraft:bee_nest_destroyed", "minecraft:bred_animals", "minecraft:brewed_potion", "minecraft:changed_dimension", "minecraft:channeled_lightning", "minecraft:construct_beacon", "minecraft:consume_item", "minecraft:crafter_recipe_crafted", "minecraft:cured_zombie_villager", "minecraft:default_block_use", "minecraft:effects_changed", "minecraft:enchanted_item", "minecraft:enter_block", "minecraft:entity_hurt_player", "minecraft:entity_killed_player", "minecraft:fall_after_explosion", "minecraft:fall_from_height", "minecraft:filled_bucket", "minecraft:fishing_rod_hooked", "minecraft:hero_of_the_village", "minecraft:impossible", "minecraft:inventory_changed", "minecraft:item_durability_changed", "minecraft:item_used_on_block", "minecraft:kill_mob_near_sculk_catalyst", "minecraft:killed_by_crossbow", "minecraft:levitation", "minecraft:lightning_strike", "minecraft:location", "minecraft:nether_travel", "minecraft:placed_block", "minecraft:player_generates_container_loot", "minecraft:player_hurt_entity", "minecraft:player_interacted_with_entity", "minecraft:player_killed_entity", "minecraft:recipe_crafted", "minecraft:recipe_unlocked", "minecraft:ride_entity_in_lava", "minecraft:shot_crossbow", "minecraft:slept_in_bed", "minecraft:slide_down_block", "minecraft:started_riding", "minecraft:summoned_entity", "minecraft:tame_animal", "minecraft:target_hit", "minecraft:thrown_item_picked_up_by_entity", "minecraft:thrown_item_picked_up_by_player", "minecraft:tick", "minecraft:used_ender_eye", "minecraft:used_totem", "minecraft:using_item", "minecraft:villager_trade"]

@dataclass
class Criteria:
    """A requirement for an advancement."""
    name: str
    trigger: TriggerType
    conditions: dict[str, Any]


@dataclass
class CustomAdvancement:
    """Rewarded loot is a """
    name: str
    title: str
    description: str
    criteria: list[Criteria]
    rewarded_loot: str | None = None  # The resource location of a loot table.
    rewarded_recipes: str | None = None  # The resource location of a recipe.
    rewarded_experience: int | None = None  # To give an amount of experience. Defaults to 0.
    rewarded_function: str | None = None  # To run a function. Function tags are not allowed.

    parent: str | None = None
    icon_item: str = "minecraft:target"
    frame: Literal["task", "challenge", "goal"] = "task"
    root_background: str = "minecraft:textures/gui/advancements/backgrounds/adventure.png"
    show_toast: bool = True
    announce_to_chat: bool = False
    hidden: bool = False
    send_telemetry_event: bool = False

    def to_dict(self) -> dict[str, Any]:
        return recusively_remove_nones_from_dict({
            "parent": self.parent,
            "display": {
                "icon": {"id": self.icon_item},
                "title": self.title,  # {"text": self.title},
                "description": self.description,  # {"text": self.description},
                "frame": self.frame if self.frame != "task" else None,
                "background": "minecraft:textures/gui/advancements/backgrounds/adventure.png",
                "show_toast": False if not self.show_toast else None,
                "announce_to_chat": False if not self.announce_to_chat else None,
                "hidden": True if self.hidden else None,
            },
            "criteria": {
                x.name: {"trigger": x.trigger, "conditions": x.conditions}
                for x in self.criteria
            },
            "requirements": [
                [x.name for x in self.criteria],
            ],
            "rewards": {
                "experience": self.rewarded_experience,
                "recipes": self.rewarded_recipes,
                "loot": self.rewarded_loot,
                "function": self.rewarded_function,
            },
            "sends_telemetry_event": True if self.send_telemetry_event else None,
        })

    def create_json_file(self, datapack: "Datapack") -> None:
        with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/advancement/{self.name}.json", "w") as f:
            json.dump(self.to_dict(), f, indent=4)


    @staticmethod
    def generate_right_click_functionality(item: "CustomItem", datapack: "Datapack") -> "CustomAdvancement":
        criteria = Criteria(f"eating_{item.item_id}", "minecraft:using_item", {
            "item": {
                "components": {
                    "minecraft:custom_data": {f"custom_right_click_for_{item.item_id}": True},
                    # Don't need any of this anymore, used to work for 1 item but 2 broke it
                    # "minecraft:food": {
                    #     "nutrition": 0,
                    #     "saturation": 0,
                    #     "can_always_eat": True,
                    #     "eat_seconds": 1_000_000,  # Doesn't seem to work... hence the custom_data
                    # }
                }
            }
        })
        eating_advancement = CustomAdvancement(
            f"custom_right_click_for_{item.item_id}", f"Ignore me {item.item_id}", "Nothing to see here", [criteria],
            hidden=True, rewarded_function=f"{datapack.namespace}:right_click/{item.item_id}"
        )
        return eating_advancement
