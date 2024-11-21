import json
from typing import Literal, Any, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from pypacks.datapack import Datapack

TriggerType = Literal["minecraft:allay_drop_item_on_block", "minecraft:any_block_use", "minecraft:avoid_vibration", "minecraft:bee_nest_destroyed", "minecraft:bred_animals", "minecraft:brewed_potion", "minecraft:changed_dimension", "minecraft:channeled_lightning", "minecraft:construct_beacon", "minecraft:consume_item", "minecraft:crafter_recipe_crafted", "minecraft:cured_zombie_villager", "minecraft:default_block_use", "minecraft:effects_changed", "minecraft:enchanted_item", "minecraft:enter_block", "minecraft:entity_hurt_player", "minecraft:entity_killed_player", "minecraft:fall_after_explosion", "minecraft:fall_from_height", "minecraft:filled_bucket", "minecraft:fishing_rod_hooked", "minecraft:hero_of_the_village", "minecraft:impossible", "minecraft:inventory_changed", "minecraft:item_durability_changed", "minecraft:item_used_on_block", "minecraft:kill_mob_near_sculk_catalyst", "minecraft:killed_by_crossbow", "minecraft:levitation", "minecraft:lightning_strike", "minecraft:location", "minecraft:nether_travel", "minecraft:placed_block", "minecraft:player_generates_container_loot", "minecraft:player_hurt_entity", "minecraft:player_interacted_with_entity", "minecraft:player_killed_entity", "minecraft:recipe_crafted", "minecraft:recipe_unlocked", "minecraft:ride_entity_in_lava", "minecraft:shot_crossbow", "minecraft:slept_in_bed", "minecraft:slide_down_block", "minecraft:started_riding", "minecraft:summoned_entity", "minecraft:tame_animal", "minecraft:target_hit", "minecraft:thrown_item_picked_up_by_entity", "minecraft:thrown_item_picked_up_by_player", "minecraft:tick", "minecraft:used_ender_eye", "minecraft:used_totem", "minecraft:using_item", "minecraft:villager_trade"]

@dataclass
class CustomAdvancement:
    name: str
    parent: str
    frame: Literal["task", "challenge", "goal"]
    root_background: str | None = None
    show_toast: bool = True
    announce_to_chat: bool = False
    hidden: bool = False
    criteria: Any = None
    requirements: Any = None
    rewards: Any = None
    send_telemetry_event: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "parent": "minecraft:adventure/shoot_arrow",
            "criteria": {
                "bullseye": {
                    "conditions": {
                        "projectile": [
                        {
                            "condition": "minecraft:entity_properties",
                            "entity": "this",
                            "predicate": {
                                "distance": {
                                    "horizontal": {
                                    "min": 30.0
                                    }
                                }
                            }
                        }
                    ],
                    "signal_strength": 15
                },
                "trigger": "minecraft:target_hit"
            }
        },
        "display": {
            "description": {
                "translate": "advancements.adventure.bullseye.description"
            },
            "frame": "challenge",
            "icon": {
                "count": 1,
                "id": "minecraft:target"
            },
            "title": {
                "translate": "advancements.adventure.bullseye.title"
            }
        },
        "requirements": [
            [
                "bullseye"
            ]
        ],
        "rewards": {
            "experience": 50
        },
        "sends_telemetry_event": self.send_telemetry_event,
    }

    def create_json_file(self, datapack: "Datapack") -> None:
        with open(f"{datapack.datapack_output_path}/data/{datapack.namespace}/advancements/{self.name}.json", "w") as f:
            json.dump(self.to_dict(), f, indent=4)