import copy
import typing

from dcs import (
    action,
    countries,
    helicopters,
    planes,
    ships,
    statics,
    triggers,
    unittype,
    vehicles,
)
from dcs.country import Country
from dcs.mapping import Point, Vector2
from dcs.mission import Mission
from dcs.terrain.caucasus import Caucasus
from dcs.translation import String, Translation


def add_units(
    unit_class: str,
    unit_map: dict[str, unittype.UnitType],
    origin: Point,
    spacing: Vector2 = Vector2(0, 1000),
    country_name="USA",
):
    position = copy.deepcopy(origin)
    country = mission.country(country_name)
    for unit_name in unit_map.keys():
        unit_type = unit_map[unit_name]
        position += spacing
        yield {
            "name": unit_class + "," + unit_name,
            "_type": unit_type,
            "position": position,
            "country": country,
        }
        position = copy.deepcopy(position)


def handle_flying_unit(unit: dict, altitude: int):
    unit["altitude"] = altitude
    unit["aircraft_type"] = unit["_type"]
    unit.pop("_type")


def setup_export_trigger(mission, output_filename, script_file="export.lua"):
    trigger_rule = triggers.TriggerStart(comment="Run export script")
    script = f"""
local output_file = io.open({output_filename}, 'w')
for i, group in pairs(coalition.getGroups(2)) do
 for j, unit in pairs(group:getUnits()) do
  output_file:write(group:getName(), ',', unit:getLife(), '\\n')
 end
end
for i, static_object in pairs(coalition.getStaticObjects(2)) do
 output_file:write(static_object:getName(), ',', static_object:getLife(), '\\n')
end
output_file:close()
            """
    translation = Translation(mission)
    script_string = String(_id=script, translation=translation)
    script_string.set(script)
    trigger_rule.add_action(action.DoScript(script_string))
    print(script_string.str())
    mission.triggerrules.triggers.append(trigger_rule)


if __name__ == "__main__":
    mission = Mission(terrain=Caucasus())
    mission.filename = "C://Users//zhexu//Saved Games//DCS//Missions//sample.miz"

    # Add ships
    for unit in add_units(
        "ship", ships.ship_map, origin=Point(-200000, -300000, Caucasus)
    ):
        mission.ship_group(**unit)

    # Add statics
    for unit in add_units(
        "static", statics.fortification_map, origin=Point(-500000, -300000, Caucasus)
    ):
        mission.static_group(**unit)
    for unit in add_units(
        "static", statics.warehouse_map, origin=Point(-501000, -300000, Caucasus)
    ):
        mission.static_group(**unit)

    # Add vehicles
    for unit in add_units(
        "vehicle", vehicles.vehicle_map, origin=Point(-502000, -300000, Caucasus)
    ):
        mission.vehicle_group(**unit)

    # Add helicopters
    for unit in add_units(
        "helicopter",
        helicopters.helicopter_map,
        origin=Point(-210000, -300000, Caucasus),
    ):
        handle_flying_unit(unit, altitude=5000)
        mission.flight_group_inflight(**unit)

    # Add planes
    for unit in add_units(
        "plane", planes.plane_map, origin=Point(-190000, -300000, Caucasus)
    ):
        if unit["name"].split(",")[1] in ["Mirage-F1JA"]:  # skip problematic units
            continue
        handle_flying_unit(unit, altitude=10000)
        mission.flight_group_inflight(**unit)

    setup_export_trigger(mission, output_filename="""'D://pydcs//out.csv'""")

    mission.save()
