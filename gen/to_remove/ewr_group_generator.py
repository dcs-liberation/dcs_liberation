from gen.to_remove.ewrs import (
    BigBirdGenerator,
    BoxSpringGenerator,
    DogEarGenerator,
    FlatFaceGenerator,
    HawkEwrGenerator,
    PatriotEwrGenerator,
    RolandEwrGenerator,
    SnowDriftGenerator,
    StraightFlushGenerator,
    TallRackGenerator,
    TinShieldGenerator,
)

EWR_MAP = {
    "BoxSpringGenerator": BoxSpringGenerator,
    "TallRackGenerator": TallRackGenerator,
    "DogEarGenerator": DogEarGenerator,
    "RolandEwrGenerator": RolandEwrGenerator,
    "FlatFaceGenerator": FlatFaceGenerator,
    "PatriotEwrGenerator": PatriotEwrGenerator,
    "BigBirdGenerator": BigBirdGenerator,
    "SnowDriftGenerator": SnowDriftGenerator,
    "StraightFlushGenerator": StraightFlushGenerator,
    "HawkEwrGenerator": HawkEwrGenerator,
    "TinShieldGenerator": TinShieldGenerator,
}
