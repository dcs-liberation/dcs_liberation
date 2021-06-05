from pathlib import Path


def _build_version_string() -> str:
    components = ["4.0"]
    build_number_path = Path("resources/buildnumber")
    if build_number_path.exists():
        with build_number_path.open("r") as build_number_file:
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
#:     * AAA_8_8cm_Flak_18,
#:     * SPAAA_Vulcan_M163,
#:     * SPAAA_ZSU_23_4_Shilka_Gun_Dish,
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
CAMPAIGN_FORMAT_VERSION = (6, 0)
