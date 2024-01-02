import pytest

from game.dcs.datalinkconfig import DatalinkConfig


def test_from_data_no_data() -> None:
    assert DatalinkConfig.from_data({}) is None


def test_from_data_bad_data() -> None:
    with pytest.raises(KeyError):
        DatalinkConfig.from_data(
            {
                "datalink": {
                    "max_team_members": 4,
                }
            }
        )
    with pytest.raises(KeyError):
        DatalinkConfig.from_data(
            {
                "datalink": {
                    "max_donors": 4,
                }
            }
        )
    with pytest.raises(ValueError):
        DatalinkConfig.from_data(
            {
                "datalink": {
                    "max_team_members": 4,
                    "max_donors": "a",
                }
            }
        )
    with pytest.raises(ValueError):
        DatalinkConfig.from_data(
            {
                "datalink": {
                    "max_team_members": "a",
                    "max_donors": 4,
                }
            }
        )


def test_from_data() -> None:
    assert DatalinkConfig.from_data(
        {
            "datalink": {
                "max_team_members": 4,
                "max_donors": 8,
            }
        }
    ) == DatalinkConfig(max_team_members=4, max_donors=8)
