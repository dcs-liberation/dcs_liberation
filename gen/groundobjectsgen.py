import logging

from game import db
from .conflictgen import *
from .naming import *

from dcs.mission import *
from dcs.statics import *

FARP_FRONTLINE_DISTANCE = 10000
AA_CP_MIN_DISTANCE = 40000


class GroundObjectsGenerator:
    FARP_CAPACITY = 4

    def __init__(self, mission: Mission, conflict: Conflict, game):
        self.m = mission
        self.conflict = conflict
        self.game = game

    def generate_farps(self, number_of_units=1) -> typing.Collection[StaticGroup]:
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
        side = self.m.country(self.game.enemy_country)

        cp = None  # type: ControlPoint
        if self.conflict.attackers_side.name == self.game.player_country:
            cp = self.conflict.to_cp
        else:
            cp = self.conflict.from_cp

        consumed_farps = set()

        for ground_object in cp.ground_objects:
            if ground_object.dcs_identifier == "AA":

                if ground_object.is_dead:
                    continue

                unit_type = random.choice(self.game.commision_unit_types(cp, AirDefence))
                assert unit_type is not None, "Cannot find unit type for GroundObject defense ({})!".format(cp)

                group = self.m.aaa_vehicle_group(
                    country=side,
                    name=ground_object.string_identifier,
                    _type=unit_type,
                    position=ground_object.position,
                    heading=ground_object.heading,
                )

                logging.info("generated defense object identifier {} with mission id {}".format(group.name, group.id))
            else:
                if ground_object.dcs_identifier in warehouse_map:
                    static_type = warehouse_map[ground_object.dcs_identifier]
                else:
                    static_type = fortification_map[ground_object.dcs_identifier]

                if not static_type:
                    print("Didn't find {} in static _map(s)!".format(ground_object.dcs_identifier))
                    continue

                if ground_object.group_id not in consumed_farps:
                    consumed_farps.add(ground_object.group_id)
                    if random.randint(0, 100) > 50:
                        farp_aa(
                            self.m,
                            side,
                            ground_object.string_identifier,
                            ground_object.position,
                        )

                group = self.m.static_group(
                    country=side,
                    name=ground_object.string_identifier,
                    _type=static_type,
                    position=ground_object.position,
                    heading=ground_object.heading,
                    dead=ground_object.is_dead,
                )

                logging.info("generated {}object identifier {} with mission id {}".format("dead " if ground_object.is_dead else "", group.name, group.id))


def farp_aa(mission_obj, country, name, position: mapping.Point):
    """
    Add AAA to a FARP :)
    :param mission_obj:
    :param country:
    :param name:
    :param position:
    :return:
    """
    vg = unitgroup.VehicleGroup(mission_obj.next_group_id(), mission_obj.string(name))

    units = [
        AirDefence.SPAAA_ZSU_23_4_Shilka,
        AirDefence.AAA_ZU_23_Closed,
        AirDefence.AAA_ZU_23_Emplacement,
        AirDefence.AAA_ZU_23_on_Ural_375,
        AirDefence.AAA_ZU_23_Insurgent_Closed,
        AirDefence.AAA_ZU_23_Insurgent_on_Ural_375,
        Armor.MBT_T_55,
        Armor.IFV_BMP_3,
    ]

    v = mission_obj.vehicle(name + "_AAA", random.choice(units))
    v.position.x = position.x - random.randint(5, 30)
    v.position.y = position.y - random.randint(5, 30)
    v.heading = random.randint(0, 359)
    vg.add_unit(v)

    wp = vg.add_waypoint(vg.units[0].position, PointAction.OffRoad, 0)
    wp.ETA_locked = True

    country.add_vehicle_group(vg)
    return vg

