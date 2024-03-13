from game.campaignloader.controlpointconfig import ControlPointConfig


def test_from_empty_data() -> None:
    config = ControlPointConfig.from_data({})
    assert not config.ferry_only


def test_from_data() -> None:
    config = ControlPointConfig.from_data(
        {
            "ferry_only": True,
        }
    )
    assert config.ferry_only


def iter_from_data() -> None:
    data = dict(
        ControlPointConfig.iter_from_data(
            {
                0: {},
                "named": {"ferry_only": True},
            }
        )
    )
    assert data == {
        0: ControlPointConfig(ferry_only=False),
        "named": ControlPointConfig(ferry_only=True),
    }
