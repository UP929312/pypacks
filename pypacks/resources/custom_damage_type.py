import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from pypacks.pack import Pack
    from pypacks.resources.custom_language import LanguageCode, CustomLanguage


@dataclass
class DamageTypeTranslation:
    """
    Used to generate all 3 cases of the translation file for a damage type.
    "death.attack.electricity": "%s was electrocuted",
    "death.attack.electricity.item": "%s was electrocuted by %s using %s",
    "death.attack.electricity.player": "%s was electrocuted whilst trying to escape %s",
    """
    language_code: "LanguageCode"
    no_item_or_player: str = "%s was killed"
    with_item_and_by_player: str = "%s was killed by %s using %s"
    by_player_no_item: str = "%s was killed whilst trying to escape %s"

    def to_custom_language(self, pack_namespace: str, internal_name: str) -> "CustomLanguage":
        from pypacks.resources.custom_language import CustomLanguage
        return CustomLanguage(
            self.language_code,
            {
                f"death.attack.{pack_namespace}:{internal_name}": self.no_item_or_player,
                f"death.attack.{pack_namespace}:{internal_name}.item": self.with_item_and_by_player,
                f"death.attack.{pack_namespace}:{internal_name}.player": self.by_player_no_item,
            },
        )


@dataclass
class CustomDamageType:
    """Custom damage types can be applied only by using the /damage command."""
    # https://minecraft.wiki/w/Damage_type
    internal_name: str
    translations: "list[DamageTypeTranslation] | None" = None  # The translation for this damage type.
    exhaustion: float = 0.0  # The amount of hunger exhaustion caused by this damage type.
    scaling: Literal["never", "always", "when_caused_by_living_non_player"] = "never"  # Whether this damage type scales with difficulty.
    effects: Literal["hurt", "thorns", "drowning", "burning", "poking", "freezing"] | None = None  # Optional field controlling how incoming damage is shown to the player.
    death_message_type: Literal["default", "fall_variants", "intentional_game_design"] | None = None  # Optional field that controls the kind of death messages to use.

    datapack_subdirectory_name: str = field(init=False, repr=False, hash=False, default="damage_type")

    def __post_init__(self) -> None:
        language_codes = [translation.language_code for translation in self.translations] if self.translations is not None else []
        assert self.translations is not None and len(set(language_codes)) == len(language_codes), "Each translation must have a unique language code."

    def to_dict(self, pack_namespace: str) -> dict[str, Any]:
        data = {
            "message_id": f"{pack_namespace}:{self.internal_name}",
            "exhaustion": self.exhaustion,
            "scaling": self.scaling,
        }
        if self.effects is not None:
            data["effects"] = self.effects
        if self.death_message_type is not None:
            data["death_message_type"] = self.death_message_type
        return data

    def get_translation_commands(self, pack_namespace: str) -> str:
        return f"tellraw @a [{{\"translate\":\"death.attack.{pack_namespace}:{self.internal_name}\", \"with\": [\"Player\"]}}, {{\"text\": \"\\n\"}}, {{\"translate\":\"death.attack.{pack_namespace}:{self.internal_name}.item\", \"with\": [\"Victim\", \"Attacker\", \"Item\"]}}, {{\"text\": \"\\n\"}}, {{\"translate\":\"death.attack.{pack_namespace}:{self.internal_name}.player\", \"with\": [\"Victim\", \"Attacker\"]}}]"

    def create_datapack_files(self, pack: "Pack") -> None:
        with open(Path(pack.datapack_output_path)/"data"/pack.namespace/self.__class__.datapack_subdirectory_name/f"{self.internal_name}.json", "w") as file:
            json.dump(self.to_dict(pack.namespace), file, indent=4)

    def generate_damage_command(self, pack_namespace: str, amount: int = 1) -> str:
        return f"damage @p {amount} {pack_namespace}:{self.internal_name}"
