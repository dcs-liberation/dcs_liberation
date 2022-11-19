from typing import Any, Optional

from dcs import Mission
from dcs.statics import Fortification
from dcs.unitgroup import FlyingGroup

from game.ato import Flight
from game.ato.flightplans.airassault import AirAssaultFlightPlan
from game.ato.flightwaypointtype import FlightWaypointType
from game.missiongenerator.missiondata import CargoInfo, LogisticsInfo
from game.settings.settings import Settings
from game.transfers import TransferOrder

ZONE_RADIUS = 300
CRATE_ZONE_RADIUS = 50


class LogisticsGenerator:
    def __init__(
        self,
        flight: Flight,
        group: FlyingGroup[Any],
        mission: Mission,
        settings: Settings,
        transfer: Optional[TransferOrder] = None,
    ) -> None:
        self.flight = flight
        self.group = group
        self.transfer = transfer
        self.mission = mission
        self.settings = settings

    def generate_logistics(self) -> LogisticsInfo:
        # Add Logisitcs info for the flight
        logistics_info = LogisticsInfo(
            pilot_names=[u.name for u in self.group.units],
            transport=self.flight.squadron.aircraft,
            blue=self.flight.blue,
            preload=self.flight.state.in_flight,
        )

        if isinstance(self.flight.flight_plan, AirAssaultFlightPlan):
            # Preload fixed wing as they do not have a pickup zone
            logistics_info.preload = logistics_info.preload or not self.flight.is_helo
            # Create the Waypoint Zone used by CTLD
            target_zone = f"{self.group.name}TARGET_ZONE"
            self.mission.triggers.add_triggerzone(
                self.flight.flight_plan.layout.target.position,
                self.flight.flight_plan.ctld_target_zone_radius.meters,
                False,
                target_zone,
            )
            logistics_info.target_zone = target_zone

        pickup_point = None
        for waypoint in self.flight.points:
            if (
                waypoint.waypoint_type
                not in [
                    FlightWaypointType.PICKUP_ZONE,
                    FlightWaypointType.DROPOFF_ZONE,
                ]
                or waypoint.only_for_player
                and not self.flight.client_count
            ):
                continue
            # Create Pickup and DropOff zone
            zone_name = f"{self.group.name}{waypoint.waypoint_type.name}"
            self.mission.triggers.add_triggerzone(
                waypoint.position, ZONE_RADIUS, False, zone_name
            )
            if waypoint.waypoint_type == FlightWaypointType.PICKUP_ZONE:
                pickup_point = waypoint.position
                logistics_info.pickup_zone = zone_name
            else:
                logistics_info.drop_off_zone = zone_name

        if self.transfer and self.flight.client_count > 0 and pickup_point is not None:
            # Add spawnable crates for client airlifts
            crate_location = pickup_point.random_point_within(
                ZONE_RADIUS - CRATE_ZONE_RADIUS, CRATE_ZONE_RADIUS
            )
            crate_zone = f"{self.group.name}crate_spawn"
            self.mission.triggers.add_triggerzone(
                crate_location, CRATE_ZONE_RADIUS, False, crate_zone
            )
            logistics_info.cargo = [
                CargoInfo(cargo_unit_type.dcs_id, crate_zone, amount)
                for cargo_unit_type, amount in self.transfer.units.items()
            ]

        if pickup_point is not None and self.settings.plugin_option(
            "ctld.logisticunit"
        ):
            # Spawn logisticsunit at pickup zones
            country = self.mission.country(self.flight.country)
            logistic_unit = self.mission.static_group(
                country,
                f"{self.group.name}logistic",
                Fortification.FARP_Ammo_Dump_Coating,
                pickup_point,
            )
            logistics_info.logistic_unit = logistic_unit.units[0].name

        return logistics_info
