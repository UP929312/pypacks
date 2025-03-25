class ConfiguredFeature:  # TODO: Type me
    feature_type: str
    # https://minecraft.wiki/w/Configured_feature


class PlacementModifier:  # TODO: Type me
    pass


class PlacedFeature:  # TODO: Type me
    feature: "str | ConfiguredFeature"
    placement: "PlacementModifier"
    # https://minecraft.wiki/w/Placed_feature
