from pathlib import Path


MAJOR_VERSION = 6
MINOR_VERSION = 1
MICRO_VERSION = 1
VERSION_NUMBER = ".".join(str(v) for v in (MAJOR_VERSION, MINOR_VERSION, MICRO_VERSION))


def _optional_build_id_component(path: Path) -> str | None:
    if path.exists():
        return path.read_text().strip()
    return None


BUILD_NUMBER = _optional_build_id_component(Path("resources/buildnumber"))
GIT_SHA = _optional_build_id_component(Path("resources/gitsha"))


def _build_version_string() -> str:
    components = [VERSION_NUMBER]
    if BUILD_NUMBER is not None:
        components.append(BUILD_NUMBER)
    if GIT_SHA is not None:
        components.append(GIT_SHA)
    if not Path("resources/final").exists():
        components.append("preview")

    return "-".join(components)


#: Current version of Liberation.
VERSION = _build_version_string()

#: The latest version of the campaign format. Increment this version whenever all
#: existing campaigns should be flagged as incompatible in the UI. We will still attempt
#: to load old campaigns, but this provides a warning to the user that the campaign may
#: not work correctly.
#:
#: There is no verification that the campaign author updated their campaign correctly
#: this is just a UI hint.
#:
#: Version history:
#:
#: Version 0
#: * Unknown compatibility.
#:
#: Version 1
#: * Compatible with Liberation 2.5.
#:
#: Version 2
#: * Front line endpoints now define convoy origin/destination waypoints. They should be
#:   placed on or near roads.
#: * Factories (Workshop_A) define factory objectives. Only control points with
#:   factories will be able to recruit ground units, so they should exist in sufficient
#:   number and be protected by IADS.
#:
#: Version 3
#: * Bulker Handy Winds define shipping lanes. They should be placed in port areas that
#:   are navigable by ships and have a route to another port area. DCS ships *will not*
#:   avoid driving into islands, so ensure that their waypoints plot a navigable route.
#:
#: Version 4
#: * TriggerZones define map based building targets.  White TriggerZones created by right
#:   clicking an object and using "assign as..." define the buildings within an objective.
#:   Blue circular TriggerZones created normally must surround groups of one or more
#:   white TriggerZones to define an objective.  If a white TriggerZone is not surrounded
#:   by a blue circular TriggerZone, campaign creation will fail.  Blue circular
#:   TriggerZones must also have their first property's value field define the type of
#:   objective (a valid value for a building TGO category, from `game.db.PRICES`).
#:
#: Version 4.1
#: * All objective types may now be set as required generation (similar to the required
#:   IADS generation). This includes:
#:     * SHORADS
#:     * Armor groups
#:     * Strike targets
#:     * Offshore strike targets
#:     * Ships
#:     * Missile sites
#:     * Coastal defenses
#:
#:   See the unit lists in MizCampaignLoader in conflicttheater.py for unit types.
#:
#: Version 4.2
#: * Adds support for AAA objectives. Place with any of the following units (either red
#:   or blue):
#:     * Flak18,
#:     * Vulcan,
#:     * ZSU_23_4_Shilka,
#:
#: Version 5.0
#: * Ammunition Depots objective locations are now predetermined using the "Ammunition
#    Depot" Warehouse object, and through trigger zone based scenery objects.
#:     * The number of alive Ammunition Depot objective buildings connected to a control
#:       point directly influences how many ground units can be supported on the front
#:       line.
#:     * The number of supported ground units at any control point is artificially
#:       capped at 50, even if the number of alive Ammunition Depot objectives can
#:       support more.
#:
#: Version 6.0
#: * Random objective generation no is longer supported. Fixed objective locations were
#:   added in 4.1.
#:
#: Version 6.1
#: * Support for new Syrian airfields in DCS 2.7.2.7910.1 (Cyprus update).
#:
#: Version 7.0
#: * DCS 2.7.2.7910.1 (Cyprus update) changed the IDs of scenery strike targets. Any
#:   mission using map buildings as strike targets must check and potentially recreate
#:   all those objectives. This definitely affects all Syria campaigns, other maps are
#:   not yet verified.
#:
#: Version 7.1
#: * Support for Mariana Islands terrain
#:
#: Version 8.0
#: * DCS 2.7.4.9632 changed scenery target IDs. Any mission using map buildings as
#:   strike targets must check and potentially recreate all those objectives.
#:
#: Version 8.1
#: * You can now add "Invisible FARP" static to FOB to add helicopter slots
#:
#: Version 9.0
#: * Campaign files now define the initial squadron layouts. See
#:   https://github.com/dcs-liberation/dcs_liberation/wiki/Custom-Campaigns.
#: * CV and LHA control points now get their names from the group name in the campaign
#:   miz.
#:
#: Version 9.1
#: * Campaign files can optionally define a start date with
#:   `recommended_start_date: YYYY-MM-DD`.
#:
#: Version 9.2
#: * Squadrons defined in campaign files can optionally setup squadrons' name,
#:   nickname and/or generated female pilot name percentage
#:
#: Version 10.0
#: * The new introduced layout system extends the mission generation so that a
#:   campaign designer can now define the heading of the ground objects which will be
#:   also used later in mission generation to orient the group accordingly.
#:   This removes the randomization of the orientation from the generation.
#:   Most campaigns will not need any updates and will work out of the box.
#:   If the campaign designer sets the heading to 0 then we will automatically change
#:   the orientation of the generated TGO to head towards the conflict if it is
#:   required by the TGO to work properly. Values other than 0 will prevent the
#:   automatic orientation.
#:
#: Version 10.1
#: * Campaign designers can now define the recommended economy settings:
#:   `recommended_player_money: 2000`.
#:   `recommended_enemy_money: 2000`.
#:   `recommended_player_income_multiplier: 1.0`.
#:   `recommended_enemy_income_multiplier: 1.0`.
#:
#: Version 10.2
#: * Campaign files can optionally define the iads configuration
#:   It is possible to define if the campaign supports advanced iads
#:
#: Version 10.3
#: * Campaign files can optionally include a start time in their recommended_start_date
#:   field. For example, `recommended_start_date: 2022-08-31 13:30:00` will have the
#:   first turn start at 13:30. If omitted, or if only a date is given, the mission will
#:   start at a random hour in the middle of the day as before.
#:
#: Version 10.4
#: * Support for the Falklands.
#:
#: Version 10.5
#: * Support for scenery objectives defined by quad zones.
CAMPAIGN_FORMAT_VERSION = (10, 5)
