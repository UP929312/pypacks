import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from pypacks.pack import Pack


@dataclass
class CustomDamageType:
    """Custom damage types can be applied only by using the /damage command."""
    # https://minecraft.wiki/w/Damage_type
    internal_name: str
    message_id: str  # E.g. fallingStalactite
    exhaustion: float = 0.0  # The amount of hunger exhaustion caused by this damage type.
    scaling: Literal["never", "always", "when_caused_by_living_non_player"] = "never"  # Whether this damage type scales with difficulty.
    effects: Literal["hurt", "thorns", "drowning", "burning", "poking", "freezing"] | None = None  # Optional field controlling how incoming damage is shown to the player.
    death_message_type: Literal["default", "fall_variants", "intentional_game_design"] | None = None  # Optional field that controls the kind of death messages to use.

    datapack_subdirectory_name: str = field(init=False, repr=False, default="damage_type")

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        data = {
            "message_id": f"{pack_namespace}:{self.message_id}",
            "exhaustion": self.exhaustion,
            "scaling": self.scaling,
        }
        if self.effects is not None:
            data["effects"] = self.effects
        if self.death_message_type is not None:
            data["death_message_type"] = self.death_message_type
        return data

    def create_datapack_files(self, pack: "Pack") -> None:
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)

    def generate_damage_command(self, pack_namespace: str, amount: float) -> str:
        return f"damage @p 5 {pack_namespace}:{self.internal_name} {amount}"
