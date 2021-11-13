from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING

from dcs import Mission
from dcs.action import DoScript, DoScriptFile
from dcs.translation import String
from dcs.triggers import TriggerStart

from game.ato import FlightType
from game.plugins import LuaPluginManager
from game.theater import TheaterGroundObject

from .aircraft.flightdata import FlightData
from .airsupport import AirSupport

if TYPE_CHECKING:
    from game import Game


class LuaGenerator:
    def __init__(
        self,
        game: Game,
        mission: Mission,
        air_support: AirSupport,
        flights: list[FlightData],
    ) -> None:
        self.game = game
        self.mission = mission
        self.air_support = air_support
        self.flights = flights
        self.plugin_scripts: list[str] = []

    def generate(self) -> None:
        self.generate_plugin_data()
        self.inject_plugins()

    def generate_plugin_data(self) -> None:
        #  TODO: Refactor this
        lua_data = {
            "AircraftCarriers": {},
            "Tankers": {},
            "AWACs": {},
            "JTACs": {},
            "TargetPoints": {},
            "RedAA": {},
            "BlueAA": {},
        }  # type: ignore

        for i, tanker in enumerate(self.air_support.tankers):
            lua_data["Tankers"][i] = {
                "dcsGroupName": tanker.group_name,
                "callsign": tanker.callsign,
                "variant": tanker.variant,
                "radio": tanker.freq.mhz,
                "tacan": str(tanker.tacan.number) + tanker.tacan.band.name,
            }

        for i, awacs in enumerate(self.air_support.awacs):
            lua_data["AWACs"][i] = {
                "dcsGroupName": awacs.group_name,
                "callsign": awacs.callsign,
                "radio": awacs.freq.mhz,
            }

        for i, jtac in enumerate(self.air_support.jtacs):
            lua_data["JTACs"][i] = {
                "dcsGroupName": jtac.group_name,
                "callsign": jtac.callsign,
                "zone": jtac.region,
                "dcsUnit": jtac.unit_name,
                "laserCode": jtac.code,
                "radio": jtac.freq.mhz,
            }
        flight_count = 0
        for flight in self.flights:
            if flight.friendly and flight.flight_type in [
                FlightType.ANTISHIP,
                FlightType.DEAD,
                FlightType.SEAD,
                FlightType.STRIKE,
            ]:
                flight_type = str(flight.flight_type)
                flight_target = flight.package.target
                if flight_target:
                    flight_target_name = None
                    flight_target_type = None
                    if isinstance(flight_target, TheaterGroundObject):
                        flight_target_name = flight_target.obj_name
                        flight_target_type = (
                            flight_type + f" TGT ({flight_target.category})"
                        )
                    elif hasattr(flight_target, "name"):
                        flight_target_name = flight_target.name
                        flight_target_type = flight_type + " TGT (Airbase)"
                    lua_data["TargetPoints"][flight_count] = {
                        "name": flight_target_name,
                        "type": flight_target_type,
                        "position": {
                            "x": flight_target.position.x,
                            "y": flight_target.position.y,
                        },
                    }
                    flight_count += 1

        for cp in self.game.theater.controlpoints:
            for ground_object in cp.ground_objects:
                if ground_object.might_have_aa and not ground_object.is_dead:
                    for g in ground_object.groups:
                        threat_range = ground_object.threat_range(g)

                        if not threat_range:
                            continue

                        faction = "BlueAA" if cp.captured else "RedAA"

                        lua_data[faction][g.name] = {
                            "name": ground_object.name,
                            "range": threat_range.meters,
                            "position": {
                                "x": ground_object.position.x,
                                "y": ground_object.position.y,
                            },
                        }

        # set a LUA table with data from Liberation that we want to set
        # at the moment it contains Liberation's install path, and an overridable
        # definition for the JTACAutoLase function later, we'll add data about the units
        # and points having been generated, in order to facilitate the configuration of
        # the plugin lua scripts
        state_location = "[[" + os.path.abspath(".") + "]]"
        lua = (
            """
            -- setting configuration table
            env.info("DCSLiberation|: setting configuration table")

            -- all data in this table is overridable.
            dcsLiberation = {}

            -- the base location for state.json; if non-existent, it'll be replaced with
            -- LIBERATION_EXPORT_DIR, TEMP, or DCS working directory
            dcsLiberation.installPath="""
            + state_location
            + """

        """
        )
        # Process the tankers
        lua += """

        -- list the tankers generated by Liberation
        dcsLiberation.Tankers = {
        """
        for key in lua_data["Tankers"]:
            data = lua_data["Tankers"][key]
            dcs_group_name = data["dcsGroupName"]
            callsign = data["callsign"]
            variant = data["variant"]
            tacan = data["tacan"]
            radio = data["radio"]
            lua += (
                f"    {{dcsGroupName='{dcs_group_name}', callsign='{callsign}', "
                f"variant='{variant}', tacan='{tacan}', radio='{radio}' }}, \n"
            )
        lua += "}"

        # Process the AWACSes
        lua += """

        -- list the AWACs generated by Liberation
        dcsLiberation.AWACs = {
        """
        for key in lua_data["AWACs"]:
            data = lua_data["AWACs"][key]
            dcs_group_name = data["dcsGroupName"]
            callsign = data["callsign"]
            radio = data["radio"]
            lua += (
                f"    {{dcsGroupName='{dcs_group_name}', callsign='{callsign}', "
                f"radio='{radio}' }}, \n"
            )
        lua += "}"

        # Process the JTACs
        lua += """

        -- list the JTACs generated by Liberation
        dcsLiberation.JTACs = {
        """
        for key in lua_data["JTACs"]:
            data = lua_data["JTACs"][key]
            dcs_group_name = data["dcsGroupName"]
            callsign = data["callsign"]
            zone = data["zone"]
            laser_code = data["laserCode"]
            dcs_unit = data["dcsUnit"]
            radio = data["radio"]
            lua += (
                f"    {{dcsGroupName='{dcs_group_name}', callsign='{callsign}', "
                f"zone={repr(zone)}, laserCode='{laser_code}', dcsUnit='{dcs_unit}', "
                f"radio='{radio}' }}, \n"
            )
        lua += "}"

        # Process the Target Points
        lua += """

        -- list the target points generated by Liberation
        dcsLiberation.TargetPoints = {
        """
        for key in lua_data["TargetPoints"]:
            data = lua_data["TargetPoints"][key]
            name = data["name"]
            point_type = data["type"]
            position_x = data["position"]["x"]
            position_y = data["position"]["y"]
            lua += (
                f"    {{name='{name}', pointType='{point_type}', "
                f"positionX='{position_x}', positionY='{position_y}' }}, \n"
            )
        lua += "}"

        lua += """

        -- list the airbases generated by Liberation
        -- dcsLiberation.Airbases = {}

        -- list the aircraft carriers generated by Liberation
        -- dcsLiberation.Carriers = {}

        -- list the Red AA generated by Liberation
        dcsLiberation.RedAA = {
        """
        for key in lua_data["RedAA"]:
            data = lua_data["RedAA"][key]
            name = data["name"]
            radius = data["range"]
            position_x = data["position"]["x"]
            position_y = data["position"]["y"]
            lua += (
                f"    {{dcsGroupName='{key}', name='{name}', range='{radius}', "
                f"positionX='{position_x}', positionY='{position_y}' }}, \n"
            )
        lua += "}"

        lua += """

        -- list the Blue AA generated by Liberation
        dcsLiberation.BlueAA = {
        """
        for key in lua_data["BlueAA"]:
            data = lua_data["BlueAA"][key]
            name = data["name"]
            radius = data["range"]
            position_x = data["position"]["x"]
            position_y = data["position"]["y"]
            lua += (
                f"    {{dcsGroupName='{key}', name='{name}', range='{radius}', "
                f"positionX='{position_x}', positionY='{position_y}' }}, \n"
            )
        lua += "}"

        lua += """

        """

        trigger = TriggerStart(comment="Set DCS Liberation data")
        trigger.add_action(DoScript(String(lua)))
        self.mission.triggerrules.triggers.append(trigger)

    def inject_lua_trigger(self, contents: str, comment: str) -> None:
        trigger = TriggerStart(comment=comment)
        trigger.add_action(DoScript(String(contents)))
        self.mission.triggerrules.triggers.append(trigger)

    def bypass_plugin_script(self, mnemonic: str) -> None:
        self.plugin_scripts.append(mnemonic)

    def inject_plugin_script(
        self, plugin_mnemonic: str, script: str, script_mnemonic: str
    ) -> None:
        if script_mnemonic in self.plugin_scripts:
            logging.debug(f"Skipping already loaded {script} for {plugin_mnemonic}")
            return

        self.plugin_scripts.append(script_mnemonic)

        plugin_path = Path("./resources/plugins", plugin_mnemonic)

        script_path = Path(plugin_path, script)
        if not script_path.exists():
            logging.error(f"Cannot find {script_path} for plugin {plugin_mnemonic}")
            return

        trigger = TriggerStart(comment=f"Load {script_mnemonic}")
        filename = script_path.resolve()
        fileref = self.mission.map_resource.add_resource_file(filename)
        trigger.add_action(DoScriptFile(fileref))
        self.mission.triggerrules.triggers.append(trigger)

    def inject_plugins(self) -> None:
        for plugin in LuaPluginManager.plugins():
            if plugin.enabled:
                plugin.inject_scripts(self)
                plugin.inject_configuration(self)
