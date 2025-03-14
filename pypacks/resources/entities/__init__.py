from pypacks.resources.entities.entity_variant import GenericEntityVariant
from pypacks.resources.entities.cat_variant import CatVariant
from pypacks.resources.entities.chicken_variant import ChickenVariant
from pypacks.resources.entities.cow_variant import CowVariant
from pypacks.resources.entities.frog_variant import FrogVariant
from pypacks.resources.entities.pig_variant import PigVariant
from pypacks.resources.entities.wolf_variant import WolfVariant

EntityVariant = CatVariant | ChickenVariant | CowVariant | FrogVariant | PigVariant | WolfVariant
ALL_ENTITY_VARIANTS: list[type[EntityVariant]] = [CatVariant, ChickenVariant, CowVariant, FrogVariant, PigVariant, WolfVariant]

__all__ = ["ALL_ENTITY_VARIANTS", "GenericEntityVariant", "CatVariant", "ChickenVariant", "CowVariant", "FrogVariant", "PigVariant", "WolfVariant", "EntityVariant"]
