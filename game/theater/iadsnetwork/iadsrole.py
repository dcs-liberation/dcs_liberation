from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from game.data.groups import GroupTask

from game.utils import Distance


class IadsRole(Enum):
    #: A radar SAM that should be controlled by Skynet.
    SAM = "Sam"

    #: A radar SAM that should be controlled and used as an EWR by Skynet.
    SAM_AS_EWR = "SamAsEwr"

    #: An air defense unit that should be used as point defense by Skynet.
    POINT_DEFENSE = "PD"

    #: An ewr unit that should provide information to the Skynet IADS.
    EWR = "Ewr"

    #: IADS Elements which allow the advanced functions of Skynet.
    CONNECTION_NODE = "ConnectionNode"
    POWER_SOURCE = "PowerSource"
    COMMAND_CENTER = "CommandCenter"

    #: All other types of groups that might be present in a SAM TGO. This includes
    #: SHORADS, AAA, supply trucks, etc. Anything that shouldn't be controlled by Skynet
    #: should use this role.
    NO_BEHAVIOR = "NoBehavior"

    @classmethod
    def for_task(cls, task: GroupTask) -> IadsRole:
        if task == GroupTask.COMMS:
            return cls.CONNECTION_NODE
        elif task == GroupTask.POWER:
            return cls.POWER_SOURCE
        elif task == GroupTask.COMMAND_CENTER:
            return cls.COMMAND_CENTER
        elif task == GroupTask.POINT_DEFENSE:
            return cls.POINT_DEFENSE
        elif task == GroupTask.LORAD:
            return cls.SAM_AS_EWR
        elif task == GroupTask.MERAD:
            return cls.SAM
        elif task in [
            GroupTask.EARLY_WARNING_RADAR,
            GroupTask.NAVY,
            GroupTask.AIRCRAFT_CARRIER,
            GroupTask.HELICOPTER_CARRIER,
        ]:
            return cls.EWR
        return cls.NO_BEHAVIOR

    @classmethod
    def for_category(cls, category: str) -> IadsRole:
        if category == "comms":
            return cls.CONNECTION_NODE
        elif category == "power":
            return cls.POWER_SOURCE
        elif category == "commandcenter":
            return cls.COMMAND_CENTER
        return cls.NO_BEHAVIOR

    @property
    def connection_range(self) -> Distance:
        if self == IadsRole.CONNECTION_NODE:
            return Distance(27780)  # 15nm
        elif self == IadsRole.POWER_SOURCE:
            return Distance(64820)  # 35nm
        return Distance(0)

    @property
    def participate(self) -> bool:
        # Returns true if the Role participates in the skynet
        # This will exclude NoBehaviour and PD for the time beeing
        return self not in [
            IadsRole.NO_BEHAVIOR,
            IadsRole.POINT_DEFENSE,
        ]

    @property
    def is_primary_node(self) -> bool:
        return self in [
            IadsRole.SAM,
            IadsRole.SAM_AS_EWR,
            IadsRole.EWR,
            IadsRole.COMMAND_CENTER,
        ]

    @property
    def is_secondary_node(self) -> bool:
        return self in [IadsRole.CONNECTION_NODE, IadsRole.POWER_SOURCE]
