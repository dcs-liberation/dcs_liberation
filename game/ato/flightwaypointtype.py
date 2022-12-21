from enum import IntEnum, unique


@unique
class FlightWaypointType(IntEnum):
    """Enumeration of waypoint types.

    The value of the enum has no meaning but should remain stable to prevent breaking
    save game compatibility.

    When adding a new waypoint type, you will also need to update:

    * waypointbuilder.py: Add a builder to simplify construction of the new waypoint
      type unless the new waypoint type will be a parameter to an existing builder
      method (such as how escort ingress waypoints work).
    * aircraftgenerator.py: Associate AI actions with the new waypoint type by subclassing
      PydcsWaypointBuilder and using it in PydcsWaypointBuilder.for_waypoint.
    """

    TAKEOFF = 0  # Take off point
    ASCEND_POINT = 1  # Ascension point after take off
    PATROL = 2  # Patrol point
    PATROL_TRACK = 3  # Patrol race track
    NAV = 4  # Nav point
    INGRESS_STRIKE = 5  # Ingress strike (For generator, means that this should have bombing on next TARGET_POINT points)
    INGRESS_SEAD = 6  # Ingress sead (For generator, means that this should attack groups on TARGET_GROUP_LOC points)
    INGRESS_CAS = 7  # Ingress cas (should start CAS task)
    CAS = 8  # Should do CAS there
    EGRESS = 9  # Should stop attack
    DESCENT_POINT = 10  # Should start descending to pattern alt
    LANDING_POINT = 11  # Should land there
    TARGET_POINT = 12  # A target building or static object, position
    TARGET_GROUP_LOC = 13  # A target group approximate location
    TARGET_SHIP = 14  # Unused.
    CUSTOM = 15  # User waypoint (no specific behaviour)
    JOIN = 16
    SPLIT = 17
    LOITER = 18
    INGRESS_ESCORT = 19
    INGRESS_DEAD = 20
    INGRESS_SWEEP = 21
    INGRESS_BAI = 22
    DIVERT = 23
    INGRESS_OCA_RUNWAY = 24
    INGRESS_OCA_AIRCRAFT = 25
    PICKUP_ZONE = 26  # Pickup Zone for cargo or troops
    DROPOFF_ZONE = 27  # Dropoff Zone for cargo or troops
    BULLSEYE = 28
    REFUEL = 29  # Should look for nearby tanker to refuel from.
    CARGO_STOP = 30  # Stopover landing point using the LandingReFuAr waypoint type
    INGRESS_AIR_ASSAULT = 31
    RECOVERY_TANKER = 32
