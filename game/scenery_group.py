from dcs.triggers import TriggerZone
from typing import Iterable


class SceneryGroup:
    def __init__(self, zone_def: TriggerZone, zones: Iterable[TriggerZone]) -> None:

        self.zone_def = zone_def
        self.zones = zones

    @property
    def blue(self) -> bool:
        return is_blue(zone_def)

    @staticmethod
    def make_scenery_groups(trigger_zones: Iterable[TriggerZone], blue: bool):

        zone_definitions = []
        white_zones = []

        scenery_groups = []

        for zone in trigger_zones:
            if blue:
                if is_blue(zone):
                    zone_definitions.append(zone)
            else:
                if is_red(zone):
                    zone_definitions.append(zone)
            if is_white(zone):
                white_zones.append

        for zone_def in zone_definitions:

            zone_def_radius = zone_def.radius
            zone_def_position = zone_def.position

            valid_white_zones = []

            for zone in white_zones:
                if zone.position.distance_to_point(zone_def_position) < zone_def_radius:
                    valid_white_zones.append(zone)
                    # todo remove found white_zone.  Don't need to search again.

            yield scenery_groups.append(SceneryGroup(zone_def, valid_white_zones))

    @staticmethod
    def is_blue(zone: TriggerZone) -> bool:
        return zone.color[1] == 0 and zone.color[2] == 0 and zone.color[3] == 1

    @staticmethod
    def is_red(zone: TriggerZone) -> bool:
        return zone.color[1] == 1 and zone.color[2] == 0 and zone.color[3] == 0

    @staticmethod
    def is_white(zone: TriggerZone) -> bool:
        return zone.color[1] == 1 and zone.color[2] == 1 and zone.color[3] == 1
