from pathlib import Path


MAJOR_VERSION = 6
MINOR_VERSION = 0
MICRO_VERSION = 0


def _build_version_string() -> str:
    components = [
        ".".join(str(v) for v in (MAJOR_VERSION, MINOR_VERSION, MICRO_VERSION))
    ]
    build_number_path = Path("resources/buildnumber")
    if build_number_path.exists():
        with build_number_path.open("r", encoding="utf-8") as build_number_file:
            components.append(build_number_file.readline())

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
CAMPAIGN_FORMAT_VERSION = (9, 2)
