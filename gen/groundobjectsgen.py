import logging
import random
from typing import Dict, Iterator

from dcs import Mission
from dcs.statics import fortification_map, warehouse_map
from dcs.task import (
    ActivateBeaconCommand,
    ActivateICLSCommand,
    EPLRS,
    OptAlarmState,
)
from dcs.unit import Ship, Vehicle
from dcs.unitgroup import StaticGroup

from game import db
from game.data.building_data import FORTIFICATION_UNITS, FORTIFICATION_UNITS_ID
from game.db import unit_type_from_name
from .conflictgen import Conflict
from .radios import RadioRegistry
from .runways import RunwayData
from .tacan import TacanBand, TacanRegistry

FARP_FRONTLINE_DISTANCE = 10000
AA_CP_MIN_DISTANCE = 40000


class GroundObjectsGenerator:
    FARP_CAPACITY = 4

    def __init__(self, mission: Mission, conflict: Conflict, game,
                 radio_registry: RadioRegistry, tacan_registry: TacanRegistry):
        self.m = mission
        self.conflict = conflict
        self.game = game
        self.radio_registry = radio_registry
        self.tacan_registry = tacan_registry
        self.icls_alloc = iter(range(1, 21))
        self.runways: Dict[str, RunwayData] = {}

    def generate_farps(self, number_of_units=1) -> Iterator[StaticGroup]:
        if self.conflict.is_vector:
            center = self.conflict.center
            heading = self.conflict.heading - 90
        else:
            center, heading = self.conflict.frontline_position(self.conflict.theater, self.conflict.from_cp, self.conflict.to_cp)
            heading -= 90

        initial_position = center.point_from_heading(heading, FARP_FRONTLINE_DISTANCE)
        position = self.conflict.find_ground_position(initial_position, heading)
        if not position:
            position = initial_position

        for i, _ in enumerate(range(0, number_of_units, self.FARP_CAPACITY)):
            position = position.point_from_heading(0, i * 275)

            yield self.m.farp(
                country=self.m.country(self.game.player_country),
                name="FARP",
                position=position,
            )

    def generate(self):

        for cp in self.game.theater.controlpoints:

            if cp.captured:
                country = self.game.player_country
            else:
                country = self.game.enemy_country
            side = self.m.country(country)

            for ground_object in cp.ground_objects:
                if ground_object.dcs_identifier == "AA":

                    if self.game.position_culled(ground_object.position):
                        continue

                    for g in ground_object.groups:
                        if len(g.units) > 0:
                            utype = unit_type_from_name(g.units[0].type)

                            if not ground_object.sea_object:
                                vg = self.m.vehicle_group(side, g.name, utype, position=g.position, heading=g.units[0].heading)
                                vg.units[0].name = self.m.string(g.units[0].name)
                                vg.units[0].player_can_drive = True
                                for i, u in enumerate(g.units):
                                    if i > 0:
                                        vehicle = Vehicle(self.m.next_unit_id(), self.m.string(u.name), u.type)
                                        vehicle.position.x = u.position.x
                                        vehicle.position.y = u.position.y
                                        vehicle.heading = u.heading
                                        vehicle.player_can_drive = True
                                        vg.add_unit(vehicle)

                                if hasattr(utype, 'eplrs'):
                                    if utype.eplrs:
                                        vg.points[0].tasks.append(EPLRS(vg.id))
                            else:
                                vg = self.m.ship_group(side, g.name, utype, position=g.position,
                                                          heading=g.units[0].heading)
                                vg.units[0].name = self.m.string(g.units[0].name)
                                for i, u in enumerate(g.units):
                                    utype = unit_type_from_name(u.type)
                                    if i > 0:
                                        ship = Ship(self.m.next_unit_id(), self.m.string(u.name), utype)
                                        ship.position.x = u.position.x
                                        ship.position.y = u.position.y
                                        ship.heading = u.heading
                                        vg.add_unit(ship)

                            if self.game.settings.perf_red_alert_state:
                                vg.points[0].tasks.append(OptAlarmState(2))
                            else:
                                vg.points[0].tasks.append(OptAlarmState(1))


                elif ground_object.dcs_identifier in ["CARRIER", "LHA"]:
                    for g in ground_object.groups:
                        if len(g.units) > 0:

                            utype = unit_type_from_name(g.units[0].type)
                            if ground_object.dcs_identifier == "CARRIER" and self.game.settings.supercarrier == True:
                                utype = db.upgrade_to_supercarrier(utype, cp.name)

                            sg = self.m.ship_group(side, g.name, utype, position=g.position, heading=g.units[0].heading)
                            atc_channel = self.radio_registry.alloc_uhf()
                            sg.set_frequency(atc_channel.hertz)
                            sg.units[0].name = self.m.string(g.units[0].name)

                            for i, u in enumerate(g.units):
                                if i > 0:
                                    ship = Ship(self.m.next_unit_id(), self.m.string(u.name), unit_type_from_name(u.type))
                                    ship.position.x = u.position.x
                                    ship.position.y = u.position.y
                                    ship.heading = u.heading
                                    # TODO: Verify.
                                    ship.set_frequency(atc_channel.hertz)
                                    sg.add_unit(ship)

                            # Find carrier direction (In the wind)
                            found_carrier_destination = False
                            attempt = 0
                            brc = self.m.weather.wind_at_ground.direction + 180
                            while not found_carrier_destination and attempt < 5:
                                point = sg.points[0].position.point_from_heading(brc, 100000-attempt*20000)
                                if self.game.theater.is_in_sea(point):
                                    found_carrier_destination = True
                                    sg.add_waypoint(point)
                                else:
                                    attempt = attempt + 1

                            # Set UP TACAN and ICLS
                            tacan = self.tacan_registry.alloc_for_band(TacanBand.X)
                            icls_channel = next(self.icls_alloc)
                            # TODO: Assign these properly.
                            if ground_object.dcs_identifier == "CARRIER":
                                tacan_callsign = random.choice([
                                    "STE",
                                    "CVN",
                                    "CVH",
                                    "CCV",
                                    "ACC",
                                    "ARC",
                                    "GER",
                                    "ABR",
                                    "LIN",
                                    "TRU",
                                ])
                            else:
                                tacan_callsign = random.choice([
                                    "LHD",
                                    "LHA",
                                    "LHB",
                                    "LHC",
                                    "LHD",
                                    "LDS",
                                ])
                            sg.points[0].tasks.append(ActivateBeaconCommand(
                                channel=tacan.number,
                                modechannel=tacan.band.value,
                                callsign=tacan_callsign,
                                unit_id=sg.units[0].id,
                                aa=False
                            ))
                            sg.points[0].tasks.append(ActivateICLSCommand(
                                icls_channel,
                                unit_id=sg.units[0].id
                            ))
                            # TODO: Make unit name usable.
                            # This relies on one control point mapping exactly
                            # to one LHA, carrier, or other usable "runway".
                            # This isn't wholly true, since the DD escorts of
                            # the carrier group are valid for helicopters, but
                            # they aren't exposed as such to the game. Should
                            # clean this up so that's possible. We can't use the
                            # unit name since it's an arbitrary ID.
                            self.runways[cp.name] = RunwayData(
                                cp.name,
                                brc,
                                "N/A",
                                atc=atc_channel,
                                tacan=tacan,
                                tacan_callsign=tacan_callsign,
                                icls=icls_channel,
                            )

                else:

                    if self.game.position_culled(ground_object.position):
                        continue

                    static_type = None
                    if ground_object.dcs_identifier in warehouse_map:
                        static_type = warehouse_map[ground_object.dcs_identifier]
                    elif ground_object.dcs_identifier in fortification_map:
                        static_type = fortification_map[ground_object.dcs_identifier]
                    elif ground_object.dcs_identifier in FORTIFICATION_UNITS_ID:
                        for f in FORTIFICATION_UNITS:
                            if f.id == ground_object.dcs_identifier:
                                unit_type = f
                                break
                    else:
                        print("Didn't find {} in static _map(s)!".format(ground_object.dcs_identifier))
                        continue

                    if static_type is None:
                        if not ground_object.is_dead:
                            group = self.m.vehicle_group(
                                country=side,
                                name=ground_object.string_identifier,
                                _type=unit_type,
                                position=ground_object.position,
                                heading=ground_object.heading,
                            )
                            logging.info("generated {}object identifier {} with mission id {}".format(
                                "dead " if ground_object.is_dead else "", group.name, group.id))
                    else:
                        group = self.m.static_group(
                            country=side,
                            name=ground_object.string_identifier,
                            _type=static_type,
                            position=ground_object.position,
                            heading=ground_object.heading,
                            dead=ground_object.is_dead,
                        )

                        logging.info("generated {}object identifier {} with mission id {}".format("dead " if ground_object.is_dead else "", group.name, group.id))