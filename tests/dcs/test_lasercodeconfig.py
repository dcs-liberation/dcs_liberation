from game.dcs.lasercodeconfig import (
    SinglePropertyLaserCodeConfig,
    MultiplePropertyLaserCodeConfig,
    LaserCodeConfig,
)


def test_singlepropertylasercodeproperty() -> None:
    config = SinglePropertyLaserCodeConfig("code", 3)
    assert list(config.iter_prop_ids()) == ["code"]
    assert config.property_dict_for_code(1688) == {"code": 688}
    assert config.property_dict_for_code(1000) == {"code": 0}
    assert config.property_dict_for_code(1234) == {"code": 234}
    assert config.property_dict_for_code(1) == {"code": 1}


def test_multiplepropertylasercodeproperty() -> None:
    config = MultiplePropertyLaserCodeConfig(
        [
            ("digit0", 0),
            ("digit1", 1),
            ("digit2", 2),
        ],
    )
    assert list(config.iter_prop_ids()) == ["digit0", "digit1", "digit2"]
    assert config.property_dict_for_code(1688) == {
        "digit0": 8,
        "digit1": 8,
        "digit2": 6,
    }
    assert config.property_dict_for_code(1000) == {
        "digit0": 0,
        "digit1": 0,
        "digit2": 0,
    }
    assert config.property_dict_for_code(1234) == {
        "digit0": 4,
        "digit1": 3,
        "digit2": 2,
    }
    assert config.property_dict_for_code(1) == {"digit0": 1, "digit1": 0, "digit2": 0}


def test_lasercodeconfig_from_yaml() -> None:
    config = LaserCodeConfig.from_yaml(
        {"pylon": 0, "property": {"id": "code", "digits": 3}}
    )
    assert config.property_dict_for_code(1688) == {"code": 688}

    config = LaserCodeConfig.from_yaml(
        {
            "pylon": 1,
            "properties": [
                {"id": "digit0", "digit": 0},
                {"id": "digit1", "digit": 1},
                {"id": "digit2", "digit": 2},
            ],
        }
    )
    assert config.property_dict_for_code(1688) == {
        "digit0": 8,
        "digit1": 8,
        "digit2": 6,
    }
