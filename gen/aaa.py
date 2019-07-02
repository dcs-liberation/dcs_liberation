import random
import math
from .conflictgen import *
from .naming import *

from dcs.mission import *

DISTANCE_FACTOR = 0.5, 1
EXTRA_AA_MIN_DISTANCE = 50000
EXTRA_AA_MAX_DISTANCE = 150000
EXTRA_AA_POSITION_FROM_CP = 550


def num_sam_dead(sam_type, destroyed_count):
    """
    Given a type and count of SAM units, determine if enough units were destroyed to warrant the
     loss of a site
    :param sam_type:
        inidivudal unit name in SAM site which was destroyed
    :param destroyed_count:
        count of that unit type which was destroyed *in the sortie*
    :return:
        INT: number of sites lost
    """
    sam_threshold = {
        AirDefence.SAM_SR_P_19: 1,
        AirDefence.SAM_SA_3_S_125_TR_SNR: 1,
        AirDefence.SAM_SA_6_Kub_STR_9S91: 1,
        AirDefence.SAM_SA_10_S_300PS_SR_5N66M: 1,
        AirDefence.SAM_SA_10_S_300PS_TR_30N6: 1,
        AirDefence.SAM_SA_10_S_300PS_CP_54K6: 1,
        AirDefence.SAM_SA_10_S_300PS_SR_64H6E: 1,
        AirDefence.SAM_SA_3_S_125_LN_5P73: 4,
        AirDefence.SAM_SA_6_Kub_LN_2P25: 6,
        AirDefence.SAM_SA_10_S_300PS_LN_5P85C: 8,
    }

    return int(destroyed_count / sam_threshold[sam_type])


def determine_positions(position, heading, num_units, launcher_distance, coverage=90):
    """
    Given a position on the map, array a group of units in a circle a uniform distance from the unit
    :param position:
        position of the center unit
    :param heading:
        the direction the units should be arranged toward if coverage is not 360
    :param num_units:
        number of units to play on the circle
    :param launcher_distance:
        distance the units should be from the center unit
    :param coverage:
        0-360
    :return:
        list of tuples representing each unit location
            [(pos_x, pos_y, heading), ...]
    """
    if coverage == 360:
        # one of the positions is shared :'(
        outer_offset = coverage / num_units
    else:
        outer_offset = coverage / (num_units - 1)

    positions = []

    if num_units % 2 == 0:
        current_offset = heading - ((coverage / (num_units - 1)) / 2)
    else:
        current_offset = heading
    current_offset -= outer_offset * (math.ceil(num_units / 2) - 1)
    for x in range(1, num_units + 1):
        positions.append((
            position.x + launcher_distance * math.cos(math.radians(current_offset)),
            position.y + launcher_distance * math.sin(math.radians(current_offset)),
            current_offset,
        ))
        current_offset += outer_offset
    return positions


def aaa_vehicle_group(self, country, name, _type: unittype.VehicleType, position: mapping.Point,
                  heading=0, group_size=1,
                  formation=unitgroup.VehicleGroup.Formation.Line,
                  move_formation: PointAction=PointAction.OffRoad):
    """
    Override the default vehicle group so that our group can contain a mix of units (which is required for advanced
        SAM sites)
    For further docstrings, see the built-in function
    """
    vg = unitgroup.VehicleGroup(self.next_group_id(), self.string(name))

    for i in range(1, group_size + 1):
        heading = randint(0, 359)
        if _type == AirDefence.SAM_SA_3_S_125_LN_5P73:
            # 4 launchers (180 degrees all facing the same direction), 1 SR, 1 TR
            num_launchers = 4
            # search radar
            v = self.vehicle(
                name + " Unit #{nr}-sr".format(nr=i),
                AirDefence.SAM_SR_P_19,
            )
            v.position.x = position.x
            v.position.y = position.y + (i - 1) * 20
            v.heading = heading
            vg.add_unit(v)
            # track radar
            v = self.vehicle(
                name + " Unit #{nr}-tr".format(nr=i),
                AirDefence.SAM_SA_3_S_125_TR_SNR,
            )

            center_x = position.x + randint(20, 40)
            center_y = position.y + (i - 1) * 20

            v.position.x = center_x
            v.position.y = center_y
            v.heading = heading
            vg.add_unit(v)
            plop_positions = determine_positions(
                position,
                heading,
                num_launchers,
                launcher_distance=100,
                coverage=180,
            )
            for x in range(0, num_launchers):
                v = self.vehicle(
                    name + " Unit #{nr}-{x}".format(nr=i, x=x),
                    AirDefence.SAM_SA_3_S_125_LN_5P73,
                )

                v.position.x = plop_positions[x][0]
                v.position.y = plop_positions[x][1]
                v.heading = plop_positions[x][2]
                vg.add_unit(v)

        elif _type == AirDefence.SAM_SA_6_Kub_LN_2P25:
            # 6 launchers (360 degree coverage)
            # 1 S/TR
            # search/track radar
            num_launchers = 6
            v = self.vehicle(
                name + " Unit #{nr}-str".format(nr=i),
                AirDefence.SAM_SA_6_Kub_STR_9S91,
            )
            v.position.x = position.x
            v.position.y = position.y + (i - 1) * 20
            v.heading = heading
            vg.add_unit(v)

            plop_positions = determine_positions(
                position,
                heading,
                num_launchers,
                launcher_distance=100,
                coverage=360,
            )
            for x in range(0, num_launchers):
                v = self.vehicle(
                    name + " Unit #{nr}-{x}".format(nr=i, x=x),
                    AirDefence.SAM_SA_6_Kub_LN_2P25,
                )

                v.position.x = plop_positions[x][0]
                v.position.y = plop_positions[x][1]
                v.heading = plop_positions[x][2]
                vg.add_unit(v)
        elif _type == AirDefence.SAM_SA_10_S_300PS_LN_5P85C:
            # 8 launchers - 4 directions, two in each direction
            # 1 SR (offset)
            # 1 TR (center)
            # search radar
            num_launchers = 8
            v = self.vehicle(
                name + " Unit #{nr}-sr".format(nr=i),
                AirDefence.SAM_SA_10_S_300PS_SR_5N66M,
            )
            v.position.x = position.x
            v.position.y = position.y + (i - 1) * 20
            v.heading = heading
            vg.add_unit(v)
            # track radar
            v = self.vehicle(
                name + " Unit #{nr}-tr".format(nr=i),
                AirDefence.SAM_SA_10_S_300PS_TR_30N6,
            )

            center_x = position.x + randint(20, 40)
            center_y = position.y + (i - 1) * 20

            v.position.x = center_x
            v.position.y = center_y
            v.heading = heading
            vg.add_unit(v)
            # command center
            v = self.vehicle(
                name + " Unit #{nr}-c".format(nr=i),
                AirDefence.SAM_SA_10_S_300PS_CP_54K6,
            )

            center_x = position.x + randint(40, 60)
            center_y = position.y + (i - 1) * 20

            v.position.x = center_x
            v.position.y = center_y
            v.heading = heading
            vg.add_unit(v)

            plop_positions = determine_positions(
                position,
                heading,
                num_launchers,
                launcher_distance=150,
                coverage=360,
            )
            for x in range(0, num_launchers):
                v = self.vehicle(
                    name + " Unit #{nr}-{x}".format(nr=i, x=x),
                    AirDefence.SAM_SA_10_S_300PS_LN_5P85C,
                )

                v.position.x = plop_positions[x][0]
                v.position.y = plop_positions[x][1]
                v.heading = plop_positions[x][2]
                vg.add_unit(v)

        elif _type == AirDefence.SAM_SA_10_S_300PS_CP_54K6:
            # 8 launchers - 4 directions, two in each direction
            # 1 SR (offset)
            # 1 TR (center)
            # search radar
            num_launchers = 8
            v = self.vehicle(
                name + " Unit #{nr}-sr".format(nr=i),
                AirDefence.SAM_SA_10_S_300PS_SR_64H6E,
            )
            v.position.x = position.x
            v.position.y = position.y + (i - 1) * 20
            v.heading = heading
            vg.add_unit(v)
            # track radar
            v = self.vehicle(
                name + " Unit #{nr}-tr".format(nr=i),
                AirDefence.SAM_SA_10_S_300PS_TR_30N6,
            )

            center_x = position.x + randint(20, 40)
            center_y = position.y + (i - 1) * 20

            v.position.x = center_x
            v.position.y = center_y
            v.heading = heading
            vg.add_unit(v)
            # command center
            v = self.vehicle(
                name + " Unit #{nr}-c".format(nr=i),
                AirDefence.SAM_SA_10_S_300PS_CP_54K6,
            )

            center_x = position.x + randint(40, 60)
            center_y = position.y + (i - 1) * 20

            v.position.x = center_x
            v.position.y = center_y
            v.heading = heading
            vg.add_unit(v)

            plop_positions = determine_positions(
                position,
                heading,
                num_units=num_launchers,
                launcher_distance=150,
                coverage=360,
            )
            for x in range(0, num_launchers):
                v = self.vehicle(
                    name + " Unit #{nr}-{x}".format(nr=i, x=x),
                    AirDefence.SAM_SA_10_S_300PS_LN_5P85D,
                )

                v.position.x = plop_positions[x][0]
                v.position.y = plop_positions[x][1]
                v.heading = plop_positions[x][2]
                vg.add_unit(v)
        else:
            v = self.vehicle(name + " Unit #{nr}-sam".format(nr=i), _type)
            v.position.x = position.x
            v.position.y = position.y + (i - 1) * 20
            v.heading = heading
            vg.add_unit(v)

    wp = vg.add_waypoint(vg.units[0].position, move_formation, 0)
    wp.ETA_locked = True
    if _type.eplrs:
        wp.tasks.append(task.EPLRS(self.next_eplrs("vehicle")))

    country.add_vehicle_group(vg)
    return vg


class AAConflictGenerator:
    def __init__(self, mission: Mission, conflict: Conflict):
        self.m = mission
        self.conflict = conflict

    def generate_at_defenders_location(self, units: db.AirDefenseDict):
        for unit_type, count in units.items():
            for _ in range(count):
                self.m.vehicle_group(
                    country=self.conflict.defenders_side,
                    name=namegen.next_unit_name(self.conflict.defenders_side, unit_type),
                    _type=unit_type,
                    position=self.conflict.ground_defenders_location.random_point_within(100, 100),
                    group_size=1)

    def generate(self, units: db.AirDefenseDict):
        for type, count in units.items():
            for _, radial in zip(range(count), self.conflict.radials):
                distance = randint(self.conflict.size * DISTANCE_FACTOR[0] + 9000, self.conflict.size * DISTANCE_FACTOR[1] + 14000)
                p = self.conflict.position.point_from_heading(random.choice(self.conflict.radials), distance)

                self.m.aaa_vehicle_group(
                        country=self.conflict.defenders_side,
                        name=namegen.next_unit_name(self.conflict.defenders_side, type),
                        _type=type,
                        position=p,
                        group_size=1)


class ExtraAAConflictGenerator:
    def __init__(self, mission: Mission, conflict: Conflict, game, player_name: Country, enemy_name: Country):
        self.mission = mission
        self.game = game
        self.conflict = conflict
        self.player_name = player_name
        self.enemy_name = enemy_name

    def generate(self):
        from theater.conflicttheater import ControlPoint

        for cp in self.game.theater.controlpoints:
            if cp.is_global:
                continue

            if cp.position.distance_to_point(self.conflict.position) < EXTRA_AA_MIN_DISTANCE:
                continue

            if cp.position.distance_to_point(self.conflict.from_cp.position) < EXTRA_AA_MIN_DISTANCE:
                continue

            if cp.position.distance_to_point(self.conflict.to_cp.position) < EXTRA_AA_MIN_DISTANCE:
                continue

            if cp.position.distance_to_point(self.conflict.position) > EXTRA_AA_MAX_DISTANCE:
                continue

            country_name = cp.captured and self.player_name or self.enemy_name
            position = cp.position.point_from_heading(0, EXTRA_AA_POSITION_FROM_CP)

            self.mission.vehicle_group(
                country=self.mission.country(country_name),
                name=namegen.next_basedefense_name(),
                _type=db.EXTRA_AA[country_name],
                position=position,
                group_size=1
            )

