--[[
    Combat Troop and Logistics Drop

    Allows Huey, Mi-8 and C130 to transport troops internally and Helicopters to transport Logistic / Vehicle units to the field via sling-loads
    without requiring external mods.

    Supports all of the original CTTS functionality such as AI auto troop load and unload as well as group spawning and preloading of troops into units.

    Supports deployment of Auto Lasing JTAC to the field

    See https://github.com/ciribob/DCS-CTLD for a user manual and the latest version

	Contributors:
	    - Steggles - https://github.com/Bob7heBuilder
	    - mvee - https://github.com/mvee
	    - jmontleon - https://github.com/jmontleon
	    - emilianomolina - https://github.com/emilianomolina
	    - davidp57 - https://github.com/veaf

      - Allow minimum distance from friendly logistics to be set
 ]]

ctld = {} -- DONT REMOVE!

--- Identifier. All output in DCS.log will start with this.
ctld.Id = "CTLD - "

--- Version.
ctld.Version = "20211113.01"

-- debug level, specific to this module
ctld.Debug = true
-- trace level, specific to this module
ctld.Trace = true

ctld.alreadyInitialized = false -- if true, ctld.initialize() will not run

-- ************************************************************************
-- *********************  USER CONFIGURATION ******************************
-- ************************************************************************
ctld.staticBugWorkaround = false --  DCS had a bug where destroying statics would cause a crash. If this happens again, set this to TRUE

ctld.disableAllSmoke = false -- if true, all smoke is diabled at pickup and drop off zones regardless of settings below. Leave false to respect settings below

ctld.hoverPickup = true --  if set to false you can load crates with the F10 menu instead of hovering... Only if not using real crates!

ctld.enableCrates = true -- if false, Helis will not be able to spawn or unpack crates so will be normal CTTS
ctld.slingLoad = false -- if false, crates can be used WITHOUT slingloading, by hovering above the crate, simulating slingloading but not the weight...
-- There are some bug with Sling-loading that can cause crashes, if these occur set slingLoad to false
-- to use the other method.
-- Set staticBugFix  to FALSE if use set ctld.slingLoad to TRUE

ctld.enableSmokeDrop = true -- if false, helis and c-130 will not be able to drop smoke

ctld.maxExtractDistance = 125 -- max distance from vehicle to troops to allow a group extraction
ctld.maximumDistanceLogistic = 200 -- max distance from vehicle to logistics to allow a loading or spawning operation
ctld.maximumSearchDistance = 4000 -- max distance for troops to search for enemy
ctld.maximumMoveDistance = 2000 -- max distance for troops to move from drop point if no enemy is nearby

ctld.minimumDeployDistance = 1000 -- minimum distance from a friendly pickup zone where you can deploy a crate

ctld.numberOfTroops = 10 -- default number of troops to load on a transport heli or C-130 
							-- also works as maximum size of group that'll fit into a helicopter unless overridden
ctld.enableFastRopeInsertion = true -- allows you to drop troops by fast rope
ctld.fastRopeMaximumHeight = 18.28 -- in meters which is 60 ft max fast rope (not rappell) safe height

ctld.vehiclesForTransportRED = { "BRDM-2", "BTR_D" } -- vehicles to load onto Il-76 - Alternatives {"Strela-1 9P31","BMP-1"}
ctld.vehiclesForTransportBLUE = { "M1045 HMMWV TOW", "M1043 HMMWV Armament" } -- vehicles to load onto c130 - Alternatives {"M1128 Stryker MGS","M1097 Avenger"}
ctld.vehiclesWeight = {
    ["BRDM-2"] = 7000,
    ["BTR_D"] = 8000,
    ["M1045 HMMWV TOW"] = 3220,
    ["M1043 HMMWV Armament"] = 2500
}

ctld.aaLaunchers = 3 -- controls how many launchers to add to the kub/buk when its spawned.
ctld.hawkLaunchers = 8 -- controls how many launchers to add to the hawk when its spawned.

ctld.spawnRPGWithCoalition = true --spawns a friendly RPG unit with Coalition forces
ctld.spawnStinger = false -- spawns a stinger / igla soldier with a group of 6 or more soldiers!

ctld.enabledFOBBuilding = true -- if true, you can load a crate INTO a C-130 than when unpacked creates a Forward Operating Base (FOB) which is a new place to spawn (crates) and carry crates from
-- In future i'd like it to be a FARP but so far that seems impossible...
-- You can also enable troop Pickup at FOBS

ctld.cratesRequiredForFOB = 3 -- The amount of crates required to build a FOB. Once built, helis can spawn crates at this outpost to be carried and deployed in another area.
-- The large crates can only be loaded and dropped by large aircraft, like the C-130 and listed in ctld.vehicleTransportEnabled
-- Small FOB crates can be moved by helicopter. The FOB will require ctld.cratesRequiredForFOB larges crates and small crates are 1/3 of a large fob crate
-- To build the FOB entirely out of small crates you will need ctld.cratesRequiredForFOB * 3

ctld.troopPickupAtFOB = true -- if true, troops can also be picked up at a created FOB

ctld.buildTimeFOB = 120 --time in seconds for the FOB to be built

ctld.crateWaitTime = 120 -- time in seconds to wait before you can spawn another crate

ctld.forceCrateToBeMoved = true -- a crate must be picked up at least once and moved before it can be unpacked. Helps to reduce crate spam

ctld.radioSound = "beacon.ogg" -- the name of the sound file to use for the FOB radio beacons. If this isnt added to the mission BEACONS WONT WORK!
ctld.radioSoundFC3 = "beaconsilent.ogg" -- name of the second silent radio file, used so FC3 aircraft dont hear ALL the beacon noises... :)

ctld.deployedBeaconBattery = 30 -- the battery on deployed beacons will last for this number minutes before needing to be re-deployed

ctld.enabledRadioBeaconDrop = true -- if its set to false then beacons cannot be dropped by units

ctld.allowRandomAiTeamPickups = false -- Allows the AI to randomize the loading of infantry teams (specified below) at pickup zones

-- Simulated Sling load configuration

ctld.minimumHoverHeight = 7.5 -- Lowest allowable height for crate hover
ctld.maximumHoverHeight = 12.0 -- Highest allowable height for crate hover
ctld.maxDistanceFromCrate = 5.5 -- Maximum distance from from crate for hover
ctld.hoverTime = 10 -- Time to hold hover above a crate for loading in seconds

-- end of Simulated Sling load configuration

-- AA SYSTEM CONFIG --
-- Sets a limit on the number of active AA systems that can be built for RED.
-- A system is counted as Active if its fully functional and has all parts
-- If a system is partially destroyed, it no longer counts towards the total
-- When this limit is hit, a player will still be able to get crates for an AA system, just unable
-- to unpack them

ctld.AASystemLimitRED = 20 -- Red side limit

ctld.AASystemLimitBLUE = 20 -- Blue side limit

--END AA SYSTEM CONFIG --

-- ***************** JTAC CONFIGURATION *****************

ctld.JTAC_LIMIT_RED = 10 -- max number of JTAC Crates for the RED Side
ctld.JTAC_LIMIT_BLUE = 10 -- max number of JTAC Crates for the BLUE Side

ctld.JTAC_dropEnabled = true -- allow JTAC Crate spawn from F10 menu

ctld.JTAC_maxDistance = 10000 -- How far a JTAC can "see" in meters (with Line of Sight)

ctld.JTAC_smokeOn_RED = true -- enables marking of target with smoke for RED forces
ctld.JTAC_smokeOn_BLUE = true -- enables marking of target with smoke for BLUE forces

ctld.JTAC_smokeColour_RED = 4 -- RED side smoke colour -- Green = 0 , Red = 1, White = 2, Orange = 3, Blue = 4
ctld.JTAC_smokeColour_BLUE = 1 -- BLUE side smoke colour -- Green = 0 , Red = 1, White = 2, Orange = 3, Blue = 4

ctld.JTAC_jtacStatusF10 = true -- enables F10 JTAC Status menu

ctld.JTAC_location = true -- shows location of target in JTAC message
ctld.location_DMS = false -- shows coordinates as Degrees Minutes Seconds instead of Degrees Decimal minutes

ctld.JTAC_lock = "all" -- "vehicle" OR "troop" OR "all" forces JTAC to only lock vehicles or troops or all ground units

-- ***************** Pickup, dropoff and waypoint zones *****************

-- Available colors (anything else like "none" disables smoke): "green", "red", "white", "orange", "blue", "none",

-- Use any of the predefined names or set your own ones

-- You can add number as a third option to limit the number of soldier or vehicle groups that can be loaded from a zone.
-- Dropping back a group at a limited zone will add one more to the limit

-- If a zone isn't ACTIVE then you can't pickup from that zone until the zone is activated by ctld.activatePickupZone
-- using the Mission editor

-- You can pickup from a SHIP by adding the SHIP UNIT NAME instead of a zone name

-- Side - Controls which side can load/unload troops at the zone

-- Flag Number - Optional last field. If set the current number of groups remaining can be obtained from the flag value

--pickupZones = { "Zone name or Ship Unit Name", "smoke color", "limit (-1 unlimited)", "ACTIVE (yes/no)", "side (0 = Both sides / 1 = Red / 2 = Blue )", flag number (optional) }
ctld.pickupZones = {
    { "pickzone1", "blue", -1, "yes", 0 },
    { "pickzone2", "red", -1, "yes", 0 },
    { "pickzone3", "none", -1, "yes", 0 },
    { "pickzone4", "none", -1, "yes", 0 },
    { "pickzone5", "none", -1, "yes", 0 },
    { "pickzone6", "none", -1, "yes", 0 },
    { "pickzone7", "none", -1, "yes", 0 },
    { "pickzone8", "none", -1, "yes", 0 },
    { "pickzone9", "none", 5, "yes", 1 }, -- limits pickup zone 9 to 5 groups of soldiers or vehicles, only red can pick up
    { "pickzone10", "none", 10, "yes", 2 },  -- limits pickup zone 10 to 10 groups of soldiers or vehicles, only blue can pick up

    { "pickzone11", "blue", 20, "no", 2 },  -- limits pickup zone 11 to 20 groups of soldiers or vehicles, only blue can pick up. Zone starts inactive!
    { "pickzone12", "red", 20, "no", 1 },  -- limits pickup zone 11 to 20 groups of soldiers or vehicles, only blue can pick up. Zone starts inactive!
    { "pickzone13", "none", -1, "yes", 0 },
    { "pickzone14", "none", -1, "yes", 0 },
    { "pickzone15", "none", -1, "yes", 0 },
    { "pickzone16", "none", -1, "yes", 0 },
    { "pickzone17", "none", -1, "yes", 0 },
    { "pickzone18", "none", -1, "yes", 0 },
    { "pickzone19", "none", 5, "yes", 0 },
    { "pickzone20", "none", 10, "yes", 0, 1000 }, -- optional extra flag number to store the current number of groups available in

    { "USA Carrier", "blue", 10, "yes", 0, 1001 }, -- instead of a Zone Name you can also use the UNIT NAME of a ship
}


-- dropOffZones = {"name","smoke colour",0,side 1 = Red or 2 = Blue or 0 = Both sides}
ctld.dropOffZones = {
    { "dropzone1", "green", 2 },
    { "dropzone2", "blue", 2 },
    { "dropzone3", "orange", 2 },
    { "dropzone4", "none", 2 },
    { "dropzone5", "none", 1 },
    { "dropzone6", "none", 1 },
    { "dropzone7", "none", 1 },
    { "dropzone8", "none", 1 },
    { "dropzone9", "none", 1 },
    { "dropzone10", "none", 1 },
}


--wpZones = { "Zone name", "smoke color",  "ACTIVE (yes/no)", "side (0 = Both sides / 1 = Red / 2 = Blue )", }
ctld.wpZones = {
    { "wpzone1", "green","yes", 2 },
    { "wpzone2", "blue","yes", 2 },
    { "wpzone3", "orange","yes", 2 },
    { "wpzone4", "none","yes", 2 },
    { "wpzone5", "none","yes", 2 },
    { "wpzone6", "none","yes", 1 },
    { "wpzone7", "none","yes", 1 },
    { "wpzone8", "none","yes", 1 },
    { "wpzone9", "none","yes", 1 },
    { "wpzone10", "none","no", 0 }, -- Both sides as its set to 0
}


-- ******************** Transports names **********************

-- Use any of the predefined names or set your own ones
ctld.transportPilotNames = {
    "helicargo1",
    "helicargo2",
    "helicargo3",
    "helicargo4",
    "helicargo5",
    "helicargo6",
    "helicargo7",
    "helicargo8",
    "helicargo9",
    "helicargo10",

    "helicargo11",
    "helicargo12",
    "helicargo13",
    "helicargo14",
    "helicargo15",
    "helicargo16",
    "helicargo17",
    "helicargo18",
    "helicargo19",
    "helicargo20",

    "helicargo21",
    "helicargo22",
    "helicargo23",
    "helicargo24",
    "helicargo25",

    "MEDEVAC #1",
    "MEDEVAC #2",
    "MEDEVAC #3",
    "MEDEVAC #4",
    "MEDEVAC #5",
    "MEDEVAC #6",
    "MEDEVAC #7",
    "MEDEVAC #8",
    "MEDEVAC #9",
    "MEDEVAC #10",
    "MEDEVAC #11",
    "MEDEVAC #12",
    "MEDEVAC #13",
    "MEDEVAC #14",
    "MEDEVAC #15",
    "MEDEVAC #16",

    "MEDEVAC RED #1",
    "MEDEVAC RED #2",
    "MEDEVAC RED #3",
    "MEDEVAC RED #4",
    "MEDEVAC RED #5",
    "MEDEVAC RED #6",
    "MEDEVAC RED #7",
    "MEDEVAC RED #8",
    "MEDEVAC RED #9",
    "MEDEVAC RED #10",
    "MEDEVAC RED #11",
    "MEDEVAC RED #12",
    "MEDEVAC RED #13",
    "MEDEVAC RED #14",
    "MEDEVAC RED #15",
    "MEDEVAC RED #16",
    "MEDEVAC RED #17",
    "MEDEVAC RED #18",
    "MEDEVAC RED #19",
    "MEDEVAC RED #20",
    "MEDEVAC RED #21",

    "MEDEVAC BLUE #1",
    "MEDEVAC BLUE #2",
    "MEDEVAC BLUE #3",
    "MEDEVAC BLUE #4",
    "MEDEVAC BLUE #5",
    "MEDEVAC BLUE #6",
    "MEDEVAC BLUE #7",
    "MEDEVAC BLUE #8",
    "MEDEVAC BLUE #9",
    "MEDEVAC BLUE #10",
    "MEDEVAC BLUE #11",
    "MEDEVAC BLUE #12",
    "MEDEVAC BLUE #13",
    "MEDEVAC BLUE #14",
    "MEDEVAC BLUE #15",
    "MEDEVAC BLUE #16",
    "MEDEVAC BLUE #17",
    "MEDEVAC BLUE #18",
    "MEDEVAC BLUE #19",
    "MEDEVAC BLUE #20",
    "MEDEVAC BLUE #21",

    -- *** AI transports names (different names only to ease identification in mission) ***

    -- Use any of the predefined names or set your own ones

    "transport1",
    "transport2",
    "transport3",
    "transport4",
    "transport5",
    "transport6",
    "transport7",
    "transport8",
    "transport9",
    "transport10",

    "transport11",
    "transport12",
    "transport13",
    "transport14",
    "transport15",
    "transport16",
    "transport17",
    "transport18",
    "transport19",
    "transport20",

    "transport21",
    "transport22",
    "transport23",
    "transport24",
    "transport25",
}

-- *************** Optional Extractable GROUPS *****************

-- Use any of the predefined names or set your own ones

ctld.extractableGroups = {
    "extract1",
    "extract2",
    "extract3",
    "extract4",
    "extract5",
    "extract6",
    "extract7",
    "extract8",
    "extract9",
    "extract10",

    "extract11",
    "extract12",
    "extract13",
    "extract14",
    "extract15",
    "extract16",
    "extract17",
    "extract18",
    "extract19",
    "extract20",

    "extract21",
    "extract22",
    "extract23",
    "extract24",
    "extract25",
}

-- ************** Logistics UNITS FOR CRATE SPAWNING ******************

-- Use any of the predefined names or set your own ones
-- When a logistic unit is destroyed, you will no longer be able to spawn crates

ctld.logisticUnits = {
    "logistic1",
    "logistic2",
    "logistic3",
    "logistic4",
    "logistic5",
    "logistic6",
    "logistic7",
    "logistic8",
    "logistic9",
    "logistic10",
}

-- ************** UNITS ABLE TO TRANSPORT VEHICLES ******************
-- Add the model name of the unit that you want to be able to transport and deploy vehicles
-- units db has all the names or you can extract a mission.miz file by making it a zip and looking
-- in the contained mission file
ctld.vehicleTransportEnabled = {
    "76MD", -- the il-76 mod doesnt use a normal - sign so il-76md wont match... !!!! GRR
    "Hercules",
}


-- ************** Maximum Units SETUP for UNITS ******************

-- Put the name of the Unit you want to limit group sizes too
-- i.e
-- ["UH-1H"] = 10,
--
-- Will limit UH1 to only transport groups with a size 10 or less
-- Make sure the unit name is exactly right or it wont work

ctld.unitLoadLimits = {

    -- Remove the -- below to turn on options
    -- ["SA342Mistral"] = 4,
    -- ["SA342L"] = 4,
    -- ["SA342M"] = 4,

}


-- ************** Allowable actions for UNIT TYPES ******************

-- Put the name of the Unit you want to limit actions for
-- NOTE - the unit must've been listed in the transportPilotNames list above
-- This can be used in conjunction with the options above for group sizes
-- By default you can load both crates and troops unless overriden below
-- i.e
-- ["UH-1H"] = {crates=true, troops=false},
--
-- Will limit UH1 to only transport CRATES but NOT TROOPS
--
-- ["SA342Mistral"] = {crates=fales, troops=true},
-- Will allow Mistral Gazelle to only transport crates, not troops

ctld.unitActions = {

    -- Remove the -- below to turn on options
    -- ["SA342Mistral"] = {crates=true, troops=true},
    -- ["SA342L"] = {crates=false, troops=true},
    -- ["SA342M"] = {crates=false, troops=true},

}

-- ************** WEIGHT CALCULATIONS FOR INFANTRY GROUPS ******************

-- Infantry groups weight is calculated based on the soldiers' roles, and the weight of their kit
-- Every soldier weights between 90% and 120% of ctld.SOLDIER_WEIGHT, and they all carry a backpack and their helmet (ctld.KIT_WEIGHT)
-- Standard grunts have a rifle and ammo (ctld.RIFLE_WEIGHT)
-- AA soldiers have a MANPAD tube (ctld.MANPAD_WEIGHT)
-- Anti-tank soldiers have a RPG and a rocket (ctld.RPG_WEIGHT)
-- Machine gunners have the squad MG and 200 bullets (ctld.MG_WEIGHT)
-- JTAC have the laser sight, radio and binoculars (ctld.JTAC_WEIGHT)
-- Mortar servants carry their tube and a few rounds (ctld.MORTAR_WEIGHT)

ctld.SOLDIER_WEIGHT = 80 -- kg, will be randomized between 90% and 120%
ctld.KIT_WEIGHT = 20 -- kg
ctld.RIFLE_WEIGHT = 5 -- kg
ctld.MANPAD_WEIGHT = 18 -- kg
ctld.RPG_WEIGHT = 7.6 -- kg
ctld.MG_WEIGHT = 10 -- kg
ctld.MORTAR_WEIGHT = 26 -- kg
ctld.JTAC_WEIGHT = 15 -- kg

-- ************** INFANTRY GROUPS FOR PICKUP ******************
-- Unit Types
-- inf is normal infantry
-- mg is M249
-- at is RPG-16
-- aa is Stinger or Igla
-- mortar is a 2B11 mortar unit
-- jtac is a JTAC soldier, which will use JTACAutoLase
-- You must add a name to the group for it to work
-- You can also add an optional coalition side to limit the group to one side
-- for the side - 2 is BLUE and 1 is RED
ctld.loadableGroups = {
    {name = "Standard Group", inf = 6, mg = 2, at = 2 }, -- will make a loadable group with 6 infantry, 2 MGs and 2 anti-tank for both coalitions
    {name = "Anti Air", inf = 2, aa = 3  },
    {name = "Anti Tank", inf = 2, at = 6  },
    {name = "Mortar Squad", mortar = 6 },
    {name = "JTAC Group", inf = 4, jtac = 1 }, -- will make a loadable group with 4 infantry and a JTAC soldier for both coalitions
    {name = "Single JTAC", jtac = 1 }, -- will make a loadable group witha single JTAC soldier for both coalitions
    -- {name = "Mortar Squad Red", inf = 2, mortar = 5, side =1 }, --would make a group loadable by RED only
}

-- ************** SPAWNABLE CRATES ******************
-- Weights must be unique as we use the weight to change the cargo to the correct unit
-- when we unpack
--
ctld.spawnableCrates = {
    -- name of the sub menu on F10 for spawning crates
    ["Ground Forces"] = {
        --crates you can spawn
        -- weight in KG
        -- Desc is the description on the F10 MENU
        -- unit is the model name of the unit to spawn
        -- cratesRequired - if set requires that many crates of the same type within 100m of each other in order build the unit
        -- side is optional but 2 is BLUE and 1 is RED
        -- dont use that option with the HAWK Crates
        { weight = 500, desc = "HMMWV - TOW", unit = "M1045 HMMWV TOW", side = 2 },
        { weight = 505, desc = "HMMWV - MG", unit = "M1043 HMMWV Armament", side = 2 },

        { weight = 510, desc = "BTR-D", unit = "BTR_D", side = 1 },
        { weight = 515, desc = "BRDM-2", unit = "BRDM-2", side = 1 },

        { weight = 520, desc = "HMMWV - JTAC", unit = "Hummer", side = 2, }, -- used as jtac and unarmed, not on the crate list if JTAC is disabled
        { weight = 525, desc = "SKP-11 - JTAC", unit = "SKP-11", side = 1, }, -- used as jtac and unarmed, not on the crate list if JTAC is disabled

        { weight = 100, desc = "2B11 Mortar", unit = "2B11 mortar" },

        { weight = 250, desc = "SPH 2S19 Msta", unit = "SAU Msta", side = 1, cratesRequired = 3 },
        { weight = 255, desc = "M-109", unit = "M-109", side = 2, cratesRequired = 3 },

        { weight = 252, desc = "Ural-375 Ammo Truck", unit = "Ural-375", side = 1, cratesRequired = 2 },
        { weight = 253, desc = "M-818 Ammo Truck", unit = "M 818", side = 2, cratesRequired = 2 },

        { weight = 800, desc = "FOB Crate - Small", unit = "FOB-SMALL" }, -- Builds a FOB! - requires 3 * ctld.cratesRequiredForFOB
    },
    ["AA short range"] = {
        { weight = 50, desc = "Stinger", unit = "Soldier stinger", side = 2 },
        { weight = 55, desc = "Igla", unit = "SA-18 Igla manpad", side = 1 },

        { weight = 405, desc = "Strela-1 9P31", unit = "Strela-1 9P31", side = 1, cratesRequired = 3 },
        { weight = 400, desc = "M1097 Avenger", unit = "M1097 Avenger", side = 2, cratesRequired = 3 },
    },
    ["AA mid range"] = {
        -- HAWK System
        { weight = 540, desc = "HAWK Launcher", unit = "Hawk ln", side = 2},
        { weight = 545, desc = "HAWK Search Radar", unit = "Hawk sr", side = 2 },
        { weight = 546, desc = "HAWK Track Radar", unit = "Hawk tr", side = 2 },
        { weight = 547, desc = "HAWK PCP", unit = "Hawk pcp" , side = 2 }, -- Remove this if on 1.2
	    { weight = 548, desc = "HAWK CWAR", unit = "Hawk cwar" , side = 2 }, -- Remove this if on 2.5	
        { weight = 549, desc = "HAWK Repair", unit = "HAWK Repair" , side = 2 },
        -- End of HAWK

        -- KUB SYSTEM
        { weight = 560, desc = "KUB Launcher", unit = "Kub 2P25 ln", side = 1},
        { weight = 565, desc = "KUB Radar", unit = "Kub 1S91 str", side = 1 },
        { weight = 570, desc = "KUB Repair", unit = "KUB Repair", side = 1},
        -- End of KUB

        -- BUK System
        --        { weight = 575, desc = "BUK Launcher", unit = "SA-11 Buk LN 9A310M1"},
        --        { weight = 580, desc = "BUK Search Radar", unit = "SA-11 Buk SR 9S18M1"},
        --        { weight = 585, desc = "BUK CC Radar", unit = "SA-11 Buk CC 9S470M1"},
        --        { weight = 590, desc = "BUK Repair", unit = "BUK Repair"},
        -- END of BUK
    },
    ["AA long range"] = {
        -- Patriot System
        { weight = 555, desc = "Patriot Launcher", unit = "Patriot ln", side = 2 },
        { weight = 556, desc = "Patriot Radar", unit = "Patriot str" , side = 2 },
        { weight = 557, desc = "Patriot ECS", unit = "Patriot ECS", side = 2 },
        -- { weight = 553, desc = "Patriot ICC", unit = "Patriot cp", side = 2 },
        -- { weight = 554, desc = "Patriot EPP", unit = "Patriot EPP", side = 2 },
        { weight = 558, desc = "Patriot AMG (optional)", unit = "Patriot AMG" , side = 2 },
        { weight = 559, desc = "Patriot Repair", unit = "Patriot Repair" , side = 2 },
        -- End of Patriot

        { weight = 595, desc = "Early Warning Radar", unit = "1L13 EWR", side = 1 }, -- cant be used by BLUE coalition
    },
}

--- 3D model that will be used to represent a loadable crate ; by default, a generator
ctld.spawnableCratesModel_load = {
    ["category"] = "Fortifications",
    ["shape_name"] = "GeneratorF",
    ["type"] = "GeneratorF"
}

--- 3D model that will be used to represent a slingable crate ; by default, a crate
ctld.spawnableCratesModel_sling = {
    ["category"] = "Cargos",
    ["shape_name"] = "bw_container_cargo",
    ["type"] = "container_cargo"
}

--[[ Placeholder for different type of cargo containers. Let's say pipes and trunks, fuel for FOB building
    ["shape_name"] = "ab-212_cargo",
    ["type"] = "uh1h_cargo" --new type for the container previously used

    ["shape_name"] = "ammo_box_cargo",
    ["type"] = "ammo_cargo",

    ["shape_name"] = "barrels_cargo",
    ["type"] = "barrels_cargo",

    ["shape_name"] = "bw_container_cargo",
    ["type"] = "container_cargo",

    ["shape_name"] = "f_bar_cargo",
    ["type"] = "f_bar_cargo",

    ["shape_name"] = "fueltank_cargo",
    ["type"] = "fueltank_cargo",

    ["shape_name"] = "iso_container_cargo",
    ["type"] = "iso_container",

    ["shape_name"] = "iso_container_small_cargo",
    ["type"] = "iso_container_small",

    ["shape_name"] = "oiltank_cargo",
    ["type"] = "oiltank_cargo",

    ["shape_name"] = "pipes_big_cargo",
    ["type"] = "pipes_big_cargo",

    ["shape_name"] = "pipes_small_cargo",
    ["type"] = "pipes_small_cargo",

    ["shape_name"] = "tetrapod_cargo",
    ["type"] = "tetrapod_cargo",

    ["shape_name"] = "trunks_long_cargo",
    ["type"] = "trunks_long_cargo",

    ["shape_name"] = "trunks_small_cargo",
    ["type"] = "trunks_small_cargo",
]]--

-- if the unit is on this list, it will be made into a JTAC when deployed
ctld.jtacUnitTypes = {
    "SKP", "Hummer" -- there are some wierd encoding issues so if you write SKP-11 it wont match as the - sign is encoded differently...
}


-- ***************************************************************
-- **************** Mission Editor Functions *********************
-- ***************************************************************


-----------------------------------------------------------------
-- Spawn group at a trigger and set them as extractable. Usage:
-- ctld.spawnGroupAtTrigger("groupside", number, "triggerName", radius)
-- Variables:
-- "groupSide" = "red" for Russia "blue" for USA
-- _number = number of groups to spawn OR Group description
-- "triggerName" = trigger name in mission editor between commas
-- _searchRadius = random distance for units to move from spawn zone (0 will leave troops at the spawn position - no search for enemy)
--
-- Example: ctld.spawnGroupAtTrigger("red", 2, "spawn1", 1000)
--
-- This example will spawn 2 groups of russians at the specified point
-- and they will search for enemy or move randomly withing 1000m
-- OR
--
-- ctld.spawnGroupAtTrigger("blue", {mg=1,at=2,aa=3,inf=4,mortar=5},"spawn2", 2000)
-- Spawns 1 machine gun, 2 anti tank, 3 anti air, 4 standard soldiers and 5 mortars
--
function ctld.spawnGroupAtTrigger(_groupSide, _number, _triggerName, _searchRadius)
    local _spawnTrigger = trigger.misc.getZone(_triggerName) -- trigger to use as reference position

    if _spawnTrigger == nil then
        trigger.action.outText("CTLD.lua ERROR: Cant find trigger called " .. _triggerName, 10)
        return
    end

    local _country
    if _groupSide == "red" then
        _groupSide = 1
        _country = 0
    else
        _groupSide = 2
        _country = 2
    end

    if _searchRadius < 0 then
        _searchRadius = 0
    end

    local _pos2 = { x = _spawnTrigger.point.x, y = _spawnTrigger.point.z }
    local _alt = land.getHeight(_pos2)
    local _pos3 = { x = _pos2.x, y = _alt, z = _pos2.y }

    local _groupDetails = ctld.generateTroopTypes(_groupSide, _number, _country)

    local _droppedTroops = ctld.spawnDroppedGroup(_pos3, _groupDetails, false, _searchRadius);

    if _groupSide == 1 then
        table.insert(ctld.droppedTroopsRED, _droppedTroops:getName())
    else
        table.insert(ctld.droppedTroopsBLUE, _droppedTroops:getName())
    end
end


-----------------------------------------------------------------
-- Spawn group at a Vec3 Point and set them as extractable. Usage:
-- ctld.spawnGroupAtPoint("groupside", number,Vec3 Point, radius)
-- Variables:
-- "groupSide" = "red" for Russia "blue" for USA
-- _number = number of groups to spawn OR Group Description
-- Vec3 Point = A vec3 point like {x=1,y=2,z=3}. Can be obtained from a unit like so: Unit.getName("Unit1"):getPoint()
-- _searchRadius = random distance for units to move from spawn zone (0 will leave troops at the spawn position - no search for enemy)
--
-- Example: ctld.spawnGroupAtPoint("red", 2, {x=1,y=2,z=3}, 1000)
--
-- This example will spawn 2 groups of russians at the specified point
-- and they will search for enemy or move randomly withing 1000m
-- OR
--
-- ctld.spawnGroupAtPoint("blue", {mg=1,at=2,aa=3,inf=4,mortar=5}, {x=1,y=2,z=3}, 2000)
-- Spawns 1 machine gun, 2 anti tank, 3 anti air, 4 standard soldiers and 5 mortars
function ctld.spawnGroupAtPoint(_groupSide, _number, _point, _searchRadius)

    local _country
    if _groupSide == "red" then
        _groupSide = 1
        _country = 0
    else
        _groupSide = 2
        _country = 2
    end

    if _searchRadius < 0 then
        _searchRadius = 0
    end

    local _groupDetails = ctld.generateTroopTypes(_groupSide, _number, _country)

    local _droppedTroops = ctld.spawnDroppedGroup(_point, _groupDetails, false, _searchRadius);

    if _groupSide == 1 then
        table.insert(ctld.droppedTroopsRED, _droppedTroops:getName())
    else
        table.insert(ctld.droppedTroopsBLUE, _droppedTroops:getName())
    end
end


-- Preloads a transport with troops or vehicles
-- replaces any troops currently on board
function ctld.preLoadTransport(_unitName, _number, _troops)

    local _unit = ctld.getTransportUnit(_unitName)

    if _unit ~= nil then

        -- will replace any units currently on board
        --        if not ctld.troopsOnboard(_unit,_troops)  then
        ctld.loadTroops(_unit, _troops, _number)
        --        end
    end
end


-- Continuously counts the number of crates in a zone and sets the value of the passed in flag
-- to the count amount
-- This means you can trigger actions based on the count and also trigger messages before the count is reached
-- Just pass in the zone name and flag number like so as a single (NOT Continuous) Trigger
-- This will now work for Mission Editor and Spawned Crates
-- e.g. ctld.cratesInZone("DropZone1", 5)
function ctld.cratesInZone(_zone, _flagNumber)
    local _triggerZone = trigger.misc.getZone(_zone) -- trigger to use as reference position

    if _triggerZone == nil then
        trigger.action.outText("CTLD.lua ERROR: Cant find zone called " .. _zone, 10)
        return
    end

    local _zonePos = mist.utils.zoneToVec3(_zone)

    --ignore side, if crate has been used its discounted from the count
    local _crateTables = { ctld.spawnedCratesRED, ctld.spawnedCratesBLUE, ctld.missionEditorCargoCrates }

    local _crateCount = 0

    for _, _crates in pairs(_crateTables) do

        for _crateName, _dontUse in pairs(_crates) do

            --get crate
            local _crate = ctld.getCrateObject(_crateName)

            --in air seems buggy with crates so if in air is true, get the height above ground and the speed magnitude
            if _crate ~= nil and _crate:getLife() > 0
                    and (ctld.inAir(_crate) == false) then

                local _dist = ctld.getDistance(_crate:getPoint(), _zonePos)

                if _dist <= _triggerZone.radius then
                    _crateCount = _crateCount + 1
                end
            end
        end
    end

    --set flag stuff
    trigger.action.setUserFlag(_flagNumber, _crateCount)

    -- env.info("FLAG ".._flagNumber.." crates ".._crateCount)

    --retrigger in 5 seconds
    timer.scheduleFunction(function(_args)

        ctld.cratesInZone(_args[1], _args[2])
    end, { _zone, _flagNumber }, timer.getTime() + 5)
end

-- Creates an extraction zone
-- any Soldiers (not vehicles) dropped at this zone by a helicopter will disappear
-- and be added to a running total of soldiers for a set flag number
-- The idea is you can then drop say 20 troops in a zone and trigger an action using the mission editor triggers
-- and the flag value
--
-- The ctld.createExtractZone function needs to be called once in a trigger action do script.
-- if you dont want smoke, pass -1 to the function.
--Green = 0 , Red = 1, White = 2, Orange = 3, Blue = 4, NO SMOKE = -1
--
-- e.g. ctld.createExtractZone("extractzone1", 2, -1) will create an extraction zone at trigger zone "extractzone1", store the number of troops dropped at
-- the zone in flag 2 and not have smoke
--
--
--
function ctld.createExtractZone(_zone, _flagNumber, _smoke)
    local _triggerZone = trigger.misc.getZone(_zone) -- trigger to use as reference position

    if _triggerZone == nil then
        trigger.action.outText("CTLD.lua ERROR: Cant find zone called " .. _zone, 10)
        return
    end

    local _pos2 = { x = _triggerZone.point.x, y = _triggerZone.point.z }
    local _alt = land.getHeight(_pos2)
    local _pos3 = { x = _pos2.x, y = _alt, z = _pos2.y }

    trigger.action.setUserFlag(_flagNumber, 0) --start at 0

    local _details = { point = _pos3, name = _zone, smoke = _smoke, flag = _flagNumber, radius = _triggerZone.radius}

    ctld.extractZones[_zone.."-".._flagNumber] =  _details

    if _smoke ~= nil and _smoke > -1 then

        local _smokeFunction

        _smokeFunction = function(_args)

            local _extractDetails = ctld.extractZones[_zone.."-".._flagNumber]
            -- check zone is still active
            if _extractDetails == nil then
                -- stop refreshing smoke, zone is done
                return
            end


            trigger.action.smoke(_args.point, _args.smoke)
            --refresh in 5 minutes
            timer.scheduleFunction(_smokeFunction, _args, timer.getTime() + 300)
        end

        --run local function
        _smokeFunction(_details)
    end
end


-- Removes an extraction zone
--
-- The smoke will take up to 5 minutes to disappear depending on the last time the smoke was activated
--
-- The ctld.removeExtractZone function needs to be called once in a trigger action do script.
--
-- e.g. ctld.removeExtractZone("extractzone1", 2) will remove an extraction zone at trigger zone "extractzone1"
-- that was setup with flag 2
--
--
--
function ctld.removeExtractZone(_zone,_flagNumber)

    local _extractDetails = ctld.extractZones[_zone.."-".._flagNumber]

    if _extractDetails ~= nil then
        --remove zone
        ctld.extractZones[_zone.."-".._flagNumber] = nil

    end
end

-- CONTINUOUS TRIGGER FUNCTION
-- This function will count the current number of extractable RED and BLUE
-- GROUPS in a zone and store the values in two flags
-- A group is only counted as being in a zone when the leader of that group
-- is in the zone
-- Use: ctld.countDroppedGroupsInZone("Zone Name", flagBlue, flagRed)
function ctld.countDroppedGroupsInZone(_zone, _blueFlag, _redFlag)

    local _triggerZone = trigger.misc.getZone(_zone) -- trigger to use as reference position

    if _triggerZone == nil then
        trigger.action.outText("CTLD.lua ERROR: Cant find zone called " .. _zone, 10)
        return
    end

    local _zonePos = mist.utils.zoneToVec3(_zone)

    local _redCount = 0;
    local _blueCount = 0;

    local _allGroups = {ctld.droppedTroopsRED,ctld.droppedTroopsBLUE,ctld.droppedVehiclesRED,ctld.droppedVehiclesBLUE}
    for _, _extractGroups in pairs(_allGroups) do
        for _,_groupName  in pairs(_extractGroups) do
            local _groupUnits = ctld.getGroup(_groupName)

            if #_groupUnits > 0 then
                local _zonePos = mist.utils.zoneToVec3(_zone)
                local _dist = ctld.getDistance(_groupUnits[1]:getPoint(), _zonePos)

                if _dist <= _triggerZone.radius then

                    if (_groupUnits[1]:getCoalition() == 1) then
                        _redCount = _redCount + 1;
                    else
                        _blueCount = _blueCount + 1;
                    end
                end
            end
        end
    end
    --set flag stuff
    trigger.action.setUserFlag(_blueFlag, _blueCount)
    trigger.action.setUserFlag(_redFlag, _redCount)

    --  env.info("Groups in zone ".._blueCount.." ".._redCount)

end

-- CONTINUOUS TRIGGER FUNCTION
-- This function will count the current number of extractable RED and BLUE
-- UNITS in a zone and store the values in two flags

-- Use: ctld.countDroppedUnitsInZone("Zone Name", flagBlue, flagRed)
function ctld.countDroppedUnitsInZone(_zone, _blueFlag, _redFlag)

    local _triggerZone = trigger.misc.getZone(_zone) -- trigger to use as reference position

    if _triggerZone == nil then
        trigger.action.outText("CTLD.lua ERROR: Cant find zone called " .. _zone, 10)
        return
    end

    local _zonePos = mist.utils.zoneToVec3(_zone)

    local _redCount = 0;
    local _blueCount = 0;

    local _allGroups = {ctld.droppedTroopsRED,ctld.droppedTroopsBLUE,ctld.droppedVehiclesRED,ctld.droppedVehiclesBLUE}

    for _, _extractGroups in pairs(_allGroups) do
        for _,_groupName  in pairs(_extractGroups) do
            local _groupUnits = ctld.getGroup(_groupName)

            if #_groupUnits > 0 then

                local _zonePos = mist.utils.zoneToVec3(_zone)
                for _,_unit in pairs(_groupUnits) do
                    local _dist = ctld.getDistance(_unit:getPoint(), _zonePos)

                    if _dist <= _triggerZone.radius then

                        if (_unit:getCoalition() == 1) then
                            _redCount = _redCount + 1;
                        else
                            _blueCount = _blueCount + 1;
                        end
                    end
                end
            end
        end
    end


    --set flag stuff
    trigger.action.setUserFlag(_blueFlag, _blueCount)
    trigger.action.setUserFlag(_redFlag, _redCount)

    --  env.info("Units in zone ".._blueCount.." ".._redCount)
end


-- Creates a radio beacon on a random UHF - VHF and HF/FM frequency for homing
-- This WILL NOT WORK if you dont add beacon.ogg and beaconsilent.ogg to the mission!!!
-- e.g. ctld.createRadioBeaconAtZone("beaconZone","red", 1440,"Waypoint 1") will create a beacon at trigger zone "beaconZone" for the Red side
-- that will last 1440 minutes (24 hours ) and named "Waypoint 1" in the list of radio beacons
--
-- e.g. ctld.createRadioBeaconAtZone("beaconZoneBlue","blue", 20) will create a beacon at trigger zone "beaconZoneBlue" for the Blue side
-- that will last 20 minutes
function ctld.createRadioBeaconAtZone(_zone, _coalition, _batteryLife, _name)
    local _triggerZone = trigger.misc.getZone(_zone) -- trigger to use as reference position

    if _triggerZone == nil then
        trigger.action.outText("CTLD.lua ERROR: Cant find zone called " .. _zone, 10)
        return
    end

    local _zonePos = mist.utils.zoneToVec3(_zone)

    ctld.beaconCount = ctld.beaconCount + 1

    if _name == nil or _name == "" then
        _name = "Beacon #" .. ctld.beaconCount
    end

    if _coalition == "red" then
        ctld.createRadioBeacon(_zonePos, 1, 0, _name, _batteryLife) --1440
    else
        ctld.createRadioBeacon(_zonePos, 2, 2, _name, _batteryLife) --1440
    end
end


-- Activates a pickup zone
-- Activates a pickup zone when called from a trigger
-- EG: ctld.activatePickupZone("pickzone3")
-- This is enable pickzone3 to be used as a pickup zone for the team set
function ctld.activatePickupZone(_zoneName)
    ctld.logDebug(string.format("ctld.activatePickupZone(_zoneName=%s)", ctld.p(_zoneName)))

    local _triggerZone = trigger.misc.getZone(_zoneName) -- trigger to use as reference position

    if _triggerZone == nil then
        local _ship = ctld.getTransportUnit(_triggerZone)

        if _ship then
            local _point = _ship:getPoint()
            _triggerZone = {}
            _triggerZone.point = _point
        end

    end

    if _triggerZone == nil  then
        trigger.action.outText("CTLD.lua ERROR: Cant find zone or ship called " .. _zoneName, 10)
    end

    for _, _zoneDetails in pairs(ctld.pickupZones) do

        if _zoneName == _zoneDetails[1] then

            --smoke could get messy if designer keeps calling this on an active zone, check its not active first
            if _zoneDetails[4] == 1 then
                -- they might have a continuous trigger so i've hidden the warning
                --trigger.action.outText("CTLD.lua ERROR: Pickup Zone already active: " .. _zoneName, 10)
                return
            end

            _zoneDetails[4] = 1 --activate zone

            if ctld.disableAllSmoke == true then --smoke disabled
            return
            end

            if _zoneDetails[2] >= 0 then

                -- Trigger smoke marker
                -- This will cause an overlapping smoke marker on next refreshsmoke call
                -- but will only happen once
                local _pos2 = { x = _triggerZone.point.x, y = _triggerZone.point.z }
                local _alt = land.getHeight(_pos2)
                local _pos3 = { x = _pos2.x, y = _alt, z = _pos2.y }

                trigger.action.smoke(_pos3, _zoneDetails[2])
            end
        end
    end
end


-- Deactivates a pickup zone
-- Deactivates a pickup zone when called from a trigger
-- EG: ctld.deactivatePickupZone("pickzone3")
-- This is disables pickzone3 and can no longer be used to as a pickup zone
-- These functions can be called by triggers, like if a set of buildings is used, you can trigger the zone to be 'not operational'
-- once they are destroyed
function ctld.deactivatePickupZone(_zoneName)

    local _triggerZone = trigger.misc.getZone(_zoneName) -- trigger to use as reference position

    if _triggerZone == nil then
        local _ship = ctld.getTransportUnit(_triggerZone)

        if _ship then
            local _point = _ship:getPoint()
            _triggerZone = {}
            _triggerZone.point = _point
        end

    end

    if _triggerZone == nil then
        trigger.action.outText("CTLD.lua ERROR: Cant find zone called " .. _zoneName, 10)
        return
    end

    for _, _zoneDetails in pairs(ctld.pickupZones) do

        if _zoneName == _zoneDetails[1] then

            -- i'd just ignore it if its already been deactivated
            --            if _zoneDetails[4] == 0 then --this really needed??
            --            trigger.action.outText("CTLD.lua ERROR: Pickup Zone already deactiveated: " .. _zoneName, 10)
            --            return
            --            end

            _zoneDetails[4] = 0 --deactivate zone
        end
    end
end

-- Change the remaining groups currently available for pickup at a zone
-- e.g. ctld.changeRemainingGroupsForPickupZone("pickup1", 5) -- adds 5 groups
-- ctld.changeRemainingGroupsForPickupZone("pickup1", -3) -- remove 3 groups
function ctld.changeRemainingGroupsForPickupZone(_zoneName, _amount)
    local _triggerZone = trigger.misc.getZone(_zoneName) -- trigger to use as reference position

    if _triggerZone == nil then
        local _ship = ctld.getTransportUnit(_triggerZone)

        if _ship then
            local _point = _ship:getPoint()
            _triggerZone = {}
            _triggerZone.point = _point
        end

    end

    if _triggerZone == nil  then
        trigger.action.outText("CTLD.lua ctld.changeRemainingGroupsForPickupZone ERROR: Cant find zone called " .. _zoneName, 10)
        return
    end

    for _, _zoneDetails in pairs(ctld.pickupZones) do

        if _zoneName == _zoneDetails[1] then
            ctld.updateZoneCounter(_zoneName, _amount)
        end
    end


end

-- Activates a Waypoint zone
-- Activates a Waypoint zone when called from a trigger
-- EG: ctld.activateWaypointZone("pickzone3")
-- This means that troops dropped within the radius of the zone will head to the center
-- of the zone instead of searching for troops
function ctld.activateWaypointZone(_zoneName)
    local _triggerZone = trigger.misc.getZone(_zoneName) -- trigger to use as reference position


    if _triggerZone == nil  then
        trigger.action.outText("CTLD.lua ERROR: Cant find zone  called " .. _zoneName, 10)

        return
    end

    for _, _zoneDetails in pairs(ctld.wpZones) do

        if _zoneName == _zoneDetails[1] then

            --smoke could get messy if designer keeps calling this on an active zone, check its not active first
            if _zoneDetails[3] == 1 then
                -- they might have a continuous trigger so i've hidden the warning
                --trigger.action.outText("CTLD.lua ERROR: Pickup Zone already active: " .. _zoneName, 10)
                return
            end

            _zoneDetails[3] = 1 --activate zone

            if ctld.disableAllSmoke == true then --smoke disabled
            return
            end

            if _zoneDetails[2] >= 0 then

                -- Trigger smoke marker
                -- This will cause an overlapping smoke marker on next refreshsmoke call
                -- but will only happen once
                local _pos2 = { x = _triggerZone.point.x, y = _triggerZone.point.z }
                local _alt = land.getHeight(_pos2)
                local _pos3 = { x = _pos2.x, y = _alt, z = _pos2.y }

                trigger.action.smoke(_pos3, _zoneDetails[2])
            end
        end
    end
end


-- Deactivates a Waypoint zone
-- Deactivates a Waypoint zone when called from a trigger
-- EG: ctld.deactivateWaypointZone("wpzone3")
-- This  disables wpzone3 so that troops dropped in this zone will search for troops as normal
-- These functions can be called by triggers
function ctld.deactivateWaypointZone(_zoneName)

    local _triggerZone = trigger.misc.getZone(_zoneName)

    if _triggerZone == nil then
        trigger.action.outText("CTLD.lua ERROR: Cant find zone called " .. _zoneName, 10)
        return
    end

    for _, _zoneDetails in pairs(ctld.pickupZones) do

        if _zoneName == _zoneDetails[1] then

            _zoneDetails[3] = 0 --deactivate zone
        end
    end
end

-- Continuous Trigger Function
-- Causes an AI unit with the specified name to unload troops / vehicles when
-- an enemy is detected within a specified distance
-- The enemy must have Line or Sight to the unit to be detected
function ctld.unloadInProximityToEnemy(_unitName,_distance)

    local _unit = ctld.getTransportUnit(_unitName)

    if _unit ~= nil and _unit:getPlayerName() == nil then

        -- no player name means AI!
        -- the findNearest visible enemy you'd want to modify as it'll find enemies quite far away
        -- limited by  ctld.JTAC_maxDistance
        local _nearestEnemy = ctld.findNearestVisibleEnemy(_unit,"all",_distance)

        if _nearestEnemy ~= nil then

            if ctld.troopsOnboard(_unit, true) then
                ctld.deployTroops(_unit, true)
                return true
            end

            if ctld.unitCanCarryVehicles(_unit) and ctld.troopsOnboard(_unit, false) then
                ctld.deployTroops(_unit, false)
                return true
            end
        end
    end

    return false

end



-- Unit will unload any units onboard if the unit is on the ground
-- when this function is called
function ctld.unloadTransport(_unitName)

    local _unit = ctld.getTransportUnit(_unitName)

    if _unit ~= nil  then

        if ctld.troopsOnboard(_unit, true) then
            ctld.unloadTroops({_unitName,true})
        end

        if ctld.unitCanCarryVehicles(_unit) and ctld.troopsOnboard(_unit, false) then
            ctld.unloadTroops({_unitName,false})
        end
    end

end

-- Loads Troops and Vehicles from a zone or picks up nearby troops or vehicles
function ctld.loadTransport(_unitName)

    local _unit = ctld.getTransportUnit(_unitName)

    if _unit ~= nil  then

        ctld.loadTroopsFromZone({ _unitName, true,"",true })

        if ctld.unitCanCarryVehicles(_unit)  then
            ctld.loadTroopsFromZone({ _unitName, false,"",true })
        end

    end

end

-- adds a callback that will be called for many actions ingame
function ctld.addCallback(_callback)

    table.insert(ctld.callbacks,_callback)

end

-- Spawns a sling loadable crate at a Trigger Zone
--
-- Weights can be found in the ctld.spawnableCrates list
-- e.g. ctld.spawnCrateAtZone("red", 500,"triggerzone1") -- spawn a humvee at triggerzone 1 for red side
-- e.g. ctld.spawnCrateAtZone("blue", 505,"triggerzone1") -- spawn a tow humvee at triggerzone1 for blue side
--
function ctld.spawnCrateAtZone(_side, _weight,_zone)
    local _spawnTrigger = trigger.misc.getZone(_zone) -- trigger to use as reference position

    if _spawnTrigger == nil then
        trigger.action.outText("CTLD.lua ERROR: Cant find zone called " .. _zone, 10)
        return
    end

    local _crateType = ctld.crateLookupTable[tostring(_weight)]

    if _crateType == nil then
        trigger.action.outText("CTLD.lua ERROR: Cant find crate with weight " .. _weight, 10)
        return
    end

    local _country
    if _side == "red" then
        _side = 1
        _country = 0
    else
        _side = 2
        _country = 2
    end

    local _pos2 = { x = _spawnTrigger.point.x, y = _spawnTrigger.point.z }
    local _alt = land.getHeight(_pos2)
    local _point = { x = _pos2.x, y = _alt, z = _pos2.y }

    local _unitId = ctld.getNextUnitId()

    local _name = string.format("%s #%i", _crateType.desc, _unitId)

    local _spawnedCrate = ctld.spawnCrateStatic(_country, _unitId, _point, _name, _crateType.weight,_side)

end

-- Spawns a sling loadable crate at a Point
--
-- Weights can be found in the ctld.spawnableCrates list
-- Points can be made by hand or obtained from a Unit position by Unit.getByName("PilotName"):getPoint()
-- e.g. ctld.spawnCrateAtZone("red", 500,{x=1,y=2,z=3}) -- spawn a humvee at triggerzone 1 for red side at a specified point
-- e.g. ctld.spawnCrateAtZone("blue", 505,{x=1,y=2,z=3}) -- spawn a tow humvee at triggerzone1 for blue side at a specified point
--
--
function ctld.spawnCrateAtPoint(_side, _weight,_point)


    local _crateType = ctld.crateLookupTable[tostring(_weight)]

    if _crateType == nil then
        trigger.action.outText("CTLD.lua ERROR: Cant find crate with weight " .. _weight, 10)
        return
    end

    local _country
    if _side == "red" then
        _side = 1
        _country = 0
    else
        _side = 2
        _country = 2
    end

    local _unitId = ctld.getNextUnitId()

    local _name = string.format("%s #%i", _crateType.desc, _unitId)

    local _spawnedCrate = ctld.spawnCrateStatic(_country, _unitId, _point, _name, _crateType.weight,_side)

end

-- ***************************************************************
-- **************** BE CAREFUL BELOW HERE ************************
-- ***************************************************************

--- Tells CTLD What multipart AA Systems there are and what parts they need
-- A New system added here also needs the launcher added
ctld.AASystemTemplate = {

    {
        name = "HAWK AA System",
        count = 4,
        parts = {
            {name = "Hawk ln", desc = "HAWK Launcher", launcher = true},
            {name = "Hawk tr", desc = "HAWK Track Radar"},
            {name = "Hawk sr", desc = "HAWK Search Radar"},
            {name = "Hawk pcp", desc = "HAWK PCP"},
	    {name = "Hawk cwar", desc = "HAWK CWAR"},
        },
        repair = "HAWK Repair",
    },
    {
        name = "Patriot AA System",
        count = 4,
        parts = {
            {name = "Patriot ln", desc = "Patriot Launcher", launcher = true},
            {name = "Patriot ECS", desc = "Patriot Control Unit"},
            {name = "Patriot str", desc = "Patriot Search and Track Radar"},
        },
        repair = "Patriot Repair",
    },
	{
        name = "BUK AA System",
        count = 3,
        parts = {
            {name = "SA-11 Buk LN 9A310M1", desc = "BUK Launcher" , launcher = true},
            {name = "SA-11 Buk CC 9S470M1", desc = "BUK CC Radar"},
            {name = "SA-11 Buk SR 9S18M1", desc = "BUK Search Radar"},
        },
        repair = "BUK Repair",
    },
    {
        name = "KUB AA System",
        count = 2,
        parts = {
            {name = "Kub 2P25 ln", desc = "KUB Launcher", launcher = true},
            {name = "Kub 1S91 str", desc = "KUB Radar"},
        },
        repair = "KUB Repair",
    },
}


ctld.crateWait = {}
ctld.crateMove = {}

---------------- INTERNAL FUNCTIONS ----------------
---
---
-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Utility methods
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- print an object for a debugging log
function ctld.p(o, level)
    local MAX_LEVEL = 20
    if level == nil then level = 0 end
    if level > MAX_LEVEL then
        ctld.logError("max depth reached in ctld.p : "..tostring(MAX_LEVEL))
        return ""
    end
    local text = ""
    if (type(o) == "table") then
        text = "\n"
        for key,value in pairs(o) do
            for i=0, level do
                text = text .. " "
            end
            text = text .. ".".. key.."="..ctld.p(value, level+1) .. "\n"
        end
    elseif (type(o) == "function") then
        text = "[function]"
    elseif (type(o) == "boolean") then
        if o == true then
            text = "[true]"
        else
            text = "[false]"
        end
    else
        if o == nil then
            text = "[nil]"
        else
            text = tostring(o)
        end
    end
    return text
end

function ctld.logError(message)
    env.info(" E - " .. ctld.Id .. message)
end

function ctld.logInfo(message)
    env.info(" I - " .. ctld.Id .. message)
end

function ctld.logDebug(message)
    if message and ctld.Debug then
        env.info(" D - " .. ctld.Id .. message)
    end
end

function ctld.logTrace(message)
    if message and ctld.Trace then
        env.info(" T - " .. ctld.Id .. message)
    end
end

ctld.nextUnitId = 1;
ctld.getNextUnitId = function()
    ctld.nextUnitId = ctld.nextUnitId + 1

    return ctld.nextUnitId
end

ctld.nextGroupId = 1;

ctld.getNextGroupId = function()
    ctld.nextGroupId = ctld.nextGroupId + 1

    return ctld.nextGroupId
end

function ctld.getTransportUnit(_unitName)

    if _unitName == nil then
        return nil
    end

    local _heli = Unit.getByName(_unitName)

    if _heli ~= nil and _heli:isActive() and _heli:getLife() > 0 then

        return _heli
    end

    return nil
end

function ctld.spawnCrateStatic(_country, _unitId, _point, _name, _weight,_side)

    local _crate
    local _spawnedCrate

    if ctld.staticBugWorkaround and ctld.slingLoad == false then
        local _groupId = ctld.getNextGroupId()
        local _groupName = "Crate Group #".._groupId

        local _group = {
            ["visible"] = false,
           -- ["groupId"] = _groupId,
            ["hidden"] = false,
            ["units"] = {},
            --        ["y"] = _positions[1].z,
            --        ["x"] = _positions[1].x,
            ["name"] = _groupName,
            ["task"] = {},
        }

        _group.units[1] = ctld.createUnit(_point.x , _point.z , 0, {type="UAZ-469",name=_name,unitId=_unitId})

        --switch to MIST
        _group.category = Group.Category.GROUND;
        _group.country = _country;

        local _spawnedGroup = Group.getByName(mist.dynAdd(_group).name)

        -- Turn off AI
        trigger.action.setGroupAIOff(_spawnedGroup)

        _spawnedCrate = Unit.getByName(_name)
    else

        if ctld.slingLoad then
            _crate = mist.utils.deepCopy(ctld.spawnableCratesModel_sling)
            _crate["canCargo"] = true
    	else
            _crate = mist.utils.deepCopy(ctld.spawnableCratesModel_load)
            _crate["canCargo"] = false
        end

        _crate["y"] = _point.z
        _crate["x"] = _point.x
        _crate["mass"] = _weight
        _crate["name"] = _name
        _crate["heading"] = 0
        _crate["country"] = _country

        ctld.logTrace(string.format("_crate=%s", ctld.p(_crate)))
        mist.dynAddStatic(_crate)

        _spawnedCrate = StaticObject.getByName(_crate["name"])
    end


    local _crateType = ctld.crateLookupTable[tostring(_weight)]

    if _side == 1 then
        ctld.spawnedCratesRED[_name] =_crateType
    else
        ctld.spawnedCratesBLUE[_name] = _crateType
    end

    return _spawnedCrate
end

function ctld.spawnFOBCrateStatic(_country, _unitId, _point, _name)

    local _crate = {
        ["category"] = "Fortifications",
        ["shape_name"] = "konteiner_red1",
        ["type"] = "Container red 1",
     --   ["unitId"] = _unitId,
        ["y"] = _point.z,
        ["x"] = _point.x,
        ["name"] = _name,
        ["canCargo"] = false,
        ["heading"] = 0,
    }

    _crate["country"] = _country

    mist.dynAddStatic(_crate)

    local _spawnedCrate = StaticObject.getByName(_crate["name"])
    --local _spawnedCrate = coalition.addStaticObject(_country, _crate)

    return _spawnedCrate
end


function ctld.spawnFOB(_country, _unitId, _point, _name)

    local _crate = {
        ["category"] = "Fortifications",
        ["type"] = "outpost",
      --  ["unitId"] = _unitId,
        ["y"] = _point.z,
        ["x"] = _point.x,
        ["name"] = _name,
        ["canCargo"] = false,
        ["heading"] = 0,
    }

    _crate["country"] = _country
    mist.dynAddStatic(_crate)
    local _spawnedCrate = StaticObject.getByName(_crate["name"])
    --local _spawnedCrate = coalition.addStaticObject(_country, _crate)

    local _id = ctld.getNextUnitId()
    local _tower = {
        ["type"] = "house2arm",
     --   ["unitId"] = _id,
        ["rate"] = 100,
        ["y"] = _point.z + -36.57142857,
        ["x"] = _point.x + 14.85714286,
        ["name"] = "FOB Watchtower #" .. _id,
        ["category"] = "Fortifications",
        ["canCargo"] = false,
        ["heading"] = 0,
    }
    --coalition.addStaticObject(_country, _tower)
    _tower["country"] = _country

    mist.dynAddStatic(_tower)

    return _spawnedCrate
end


function ctld.spawnCrate(_arguments)

    local _status, _err = pcall(function(_args)

        -- use the cargo weight to guess the type of unit as no way to add description :(

        local _crateType = ctld.crateLookupTable[tostring(_args[2])]
        local _heli = ctld.getTransportUnit(_args[1])

        if _crateType ~= nil and _heli ~= nil and ctld.inAir(_heli) == false then

            if ctld.inLogisticsZone(_heli) == false then

                ctld.displayMessageToGroup(_heli, "You are not close enough to friendly logistics to get a crate!", 10)

                return
            end

            if ctld.isJTACUnitType(_crateType.unit) then

                local _limitHit = false

                if _heli:getCoalition() == 1 then

                    if ctld.JTAC_LIMIT_RED == 0 then
                        _limitHit = true
                    else
                        ctld.JTAC_LIMIT_RED = ctld.JTAC_LIMIT_RED - 1
                    end
                else
                    if ctld.JTAC_LIMIT_BLUE == 0 then
                        _limitHit = true
                    else
                        ctld.JTAC_LIMIT_BLUE = ctld.JTAC_LIMIT_BLUE - 1
                    end
                end

                if _limitHit then
                    ctld.displayMessageToGroup(_heli, "No more JTAC Crates Left!", 10)
                    return
                end
            end

            local _position = _heli:getPosition()

            -- check crate spam
            if _heli:getPlayerName() ~= nil and ctld.crateWait[_heli:getPlayerName()] and  ctld.crateWait[_heli:getPlayerName()] > timer.getTime() then

                ctld.displayMessageToGroup(_heli,"Sorry you must wait "..(ctld.crateWait[_heli:getPlayerName()]  - timer.getTime()).. " seconds before you can get another crate", 20)
                return
            end

            if _heli:getPlayerName() ~= nil then
                ctld.crateWait[_heli:getPlayerName()] = timer.getTime() + ctld.crateWaitTime
            end
                --   trigger.action.outText("Spawn Crate".._args[1].." ".._args[2],10)

            local _heli = ctld.getTransportUnit(_args[1])

            local _point = ctld.getPointAt12Oclock(_heli, 30)

            local _unitId = ctld.getNextUnitId()

            local _side = _heli:getCoalition()

            local _name = string.format("%s #%i", _crateType.desc, _unitId)

            local _spawnedCrate = ctld.spawnCrateStatic(_heli:getCountry(), _unitId, _point, _name, _crateType.weight,_side)

            -- add to move table
            ctld.crateMove[_name] = _name

            ctld.displayMessageToGroup(_heli, string.format("A %s crate weighing %s kg has been brought out and is at your 12 o'clock ", _crateType.desc, _crateType.weight), 20)

        else
            env.info("Couldn't find crate item to spawn")
        end
    end, _arguments)

    if (not _status) then
        env.error(string.format("CTLD ERROR: %s", _err))
    end
end

function ctld.getPointAt12Oclock(_unit, _offset)

    local _position = _unit:getPosition()
    local _angle = math.atan2(_position.x.z, _position.x.x)
    local _xOffset = math.cos(_angle) * _offset
    local _yOffset = math.sin(_angle) * _offset

    local _point = _unit:getPoint()
    return { x = _point.x + _xOffset, z = _point.z + _yOffset, y = _point.y }
end

function ctld.troopsOnboard(_heli, _troops)

    if ctld.inTransitTroops[_heli:getName()] ~= nil then

        local _onboard = ctld.inTransitTroops[_heli:getName()]

        if _troops then

            if _onboard.troops ~= nil and _onboard.troops.units ~= nil and #_onboard.troops.units > 0 then
                return true
            else
                return false
            end
        else

            if _onboard.vehicles ~= nil and _onboard.vehicles.units ~= nil and #_onboard.vehicles.units > 0 then
                return true
            else
                return false
            end
        end

    else
        return false
    end
end

-- if its dropped by AI then there is no player name so return the type of unit
function ctld.getPlayerNameOrType(_heli)

    if _heli:getPlayerName() == nil then

        return _heli:getTypeName()
    else
        return _heli:getPlayerName()
    end
end

function ctld.inExtractZone(_heli)

    local _heliPoint = _heli:getPoint()

    for _, _zoneDetails in pairs(ctld.extractZones) do

        --get distance to center
        local _dist = ctld.getDistance(_heliPoint, _zoneDetails.point)

        if _dist <= _zoneDetails.radius then
            return _zoneDetails
        end
    end

    return false
end

-- safe to fast rope if speed is less than 0.5 Meters per second
function ctld.safeToFastRope(_heli)

    if ctld.enableFastRopeInsertion == false then
        return false
    end

    --landed or speed is less than 8 km/h and height is less than fast rope height
    if (ctld.inAir(_heli) == false or (ctld.heightDiff(_heli) <= ctld.fastRopeMaximumHeight + 3.0 and mist.vec.mag(_heli:getVelocity()) < 2.2)) then
        return true
    end
end

function ctld.metersToFeet(_meters)

    local _feet = _meters * 3.2808399

    return mist.utils.round(_feet)
end

function ctld.inAir(_heli)

    if _heli:inAir() == false then
        return false
    end

    -- less than 5 cm/s a second so landed
    -- BUT AI can hold a perfect hover so ignore AI
    if mist.vec.mag(_heli:getVelocity()) < 0.05 and _heli:getPlayerName() ~= nil then
        return false
    end
    return true
end

function ctld.deployTroops(_heli, _troops)

    local _onboard = ctld.inTransitTroops[_heli:getName()]

    -- deloy troops
    if _troops then
        if _onboard.troops ~= nil and #_onboard.troops.units > 0 then
            if ctld.inAir(_heli) == false or ctld.safeToFastRope(_heli) then

                -- check we're not in extract zone
                local _extractZone = ctld.inExtractZone(_heli)

                if _extractZone == false then

                    local _droppedTroops = ctld.spawnDroppedGroup(_heli:getPoint(), _onboard.troops, false)
                    ctld.logTrace(string.format("_onboard.troops=%s", ctld.p(_onboard.troops)))
                    if _onboard.troops.jtac or _droppedTroops:getName():lower():find("jtac") then
                        local _code = table.remove(ctld.jtacGeneratedLaserCodes, 1)
                        ctld.logTrace(string.format("_code=%s", ctld.p(_code)))
                        table.insert(ctld.jtacGeneratedLaserCodes, _code)
                        ctld.logTrace(string.format("_droppedTroops:getName()=%s", ctld.p(_droppedTroops:getName())))
                        ctld.JTACAutoLase(_droppedTroops:getName(), _code)
                    end

                    if _heli:getCoalition() == 1 then

                        table.insert(ctld.droppedTroopsRED, _droppedTroops:getName())
                    else

                        table.insert(ctld.droppedTroopsBLUE, _droppedTroops:getName())
                    end

                    ctld.inTransitTroops[_heli:getName()].troops = nil
                    ctld.adaptWeightToCargo(_heli:getName())

                    if ctld.inAir(_heli) then
                        trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " fast-ropped troops from " .. _heli:getTypeName() .. " into combat", 10)
                    else
                        trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " dropped troops from " .. _heli:getTypeName() .. " into combat", 10)
                    end

                    ctld.processCallback({unit = _heli, unloaded = _droppedTroops, action = "dropped_troops"})


                else
                    --extract zone!
                    local _droppedCount = trigger.misc.getUserFlag(_extractZone.flag)

                    _droppedCount = (#_onboard.troops.units) + _droppedCount

                    trigger.action.setUserFlag(_extractZone.flag, _droppedCount)

                    ctld.inTransitTroops[_heli:getName()].troops = nil
                    ctld.adaptWeightToCargo(_heli:getName())

                    if ctld.inAir(_heli) then
                        trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " troops fast-ropped from " .. _heli:getTypeName() .. " into " .. _extractZone.name, 10)
                    else
                        trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " troops dropped from " .. _heli:getTypeName() .. " into " .. _extractZone.name, 10)
                    end
                end
            else
                ctld.displayMessageToGroup(_heli, "Too high or too fast to drop troops into combat! Hover below " .. ctld.metersToFeet(ctld.fastRopeMaximumHeight) .. " feet or land.", 10)
            end
        end

    else
        if ctld.inAir(_heli) == false then
            if _onboard.vehicles ~= nil and #_onboard.vehicles.units > 0 then

                local _droppedVehicles = ctld.spawnDroppedGroup(_heli:getPoint(), _onboard.vehicles, true)

                if _heli:getCoalition() == 1 then

                    table.insert(ctld.droppedVehiclesRED, _droppedVehicles:getName())
                else

                    table.insert(ctld.droppedVehiclesBLUE, _droppedVehicles:getName())
                end

                ctld.inTransitTroops[_heli:getName()].vehicles = nil
                ctld.adaptWeightToCargo(_heli:getName())

                ctld.processCallback({unit = _heli, unloaded = _droppedVehicles, action = "dropped_vehicles"})

                trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " dropped vehicles from " .. _heli:getTypeName() .. " into combat", 10)
            end
        end
    end
end

function ctld.insertIntoTroopsArray(_troopType,_count,_troopArray,_troopName)

    for _i = 1, _count do
        local _unitId = ctld.getNextUnitId()
        table.insert(_troopArray, { type = _troopType, unitId = _unitId, name = string.format("Dropped %s #%i", _troopName or _troopType, _unitId) })
    end

    return _troopArray

end


function ctld.generateTroopTypes(_side, _countOrTemplate, _country)
    local _troops = {}
    local _weight = 0
    local _hasJTAC = false

    local function getSoldiersWeight(count, additionalWeight)
        local _weight = 0
        for i = 1, count do
            local _soldierWeight = math.random(90, 120) * ctld.SOLDIER_WEIGHT / 100
            ctld.logTrace(string.format("_soldierWeight=%s", ctld.p(_soldierWeight)))
            _weight = _weight + _soldierWeight + ctld.KIT_WEIGHT + additionalWeight
        end
        return _weight
    end

    if type(_countOrTemplate) == "table" then

        if _countOrTemplate.aa then
            ctld.logTrace(string.format("_countOrTemplate.aa=%s", ctld.p(_countOrTemplate.aa)))
            if _side == 2 then
                _troops = ctld.insertIntoTroopsArray("Soldier stinger",_countOrTemplate.aa,_troops)
            else
                _troops = ctld.insertIntoTroopsArray("SA-18 Igla manpad",_countOrTemplate.aa,_troops)
            end
            _weight = _weight + getSoldiersWeight(_countOrTemplate.aa, ctld.MANPAD_WEIGHT)
            ctld.logTrace(string.format("_weight=%s", ctld.p(_weight)))
        end

        if _countOrTemplate.inf then
            ctld.logTrace(string.format("_countOrTemplate.inf=%s", ctld.p(_countOrTemplate.inf)))
            if _side == 2 then
                _troops = ctld.insertIntoTroopsArray("Soldier M4",_countOrTemplate.inf,_troops)
            else
                _troops = ctld.insertIntoTroopsArray("Soldier AK",_countOrTemplate.inf,_troops)
            end
            _weight = _weight + getSoldiersWeight(_countOrTemplate.inf, ctld.RIFLE_WEIGHT)
            ctld.logTrace(string.format("_weight=%s", ctld.p(_weight)))
        end

        if _countOrTemplate.mg then
            ctld.logTrace(string.format("_countOrTemplate.mg=%s", ctld.p(_countOrTemplate.mg)))
            if _side == 2 then
                _troops = ctld.insertIntoTroopsArray("Soldier M249",_countOrTemplate.mg,_troops)
            else
                _troops = ctld.insertIntoTroopsArray("Paratrooper AKS-74",_countOrTemplate.mg,_troops)
            end
            _weight = _weight + getSoldiersWeight(_countOrTemplate.mg, ctld.MG_WEIGHT)
            ctld.logTrace(string.format("_weight=%s", ctld.p(_weight)))
        end

        if _countOrTemplate.at then
            ctld.logTrace(string.format("_countOrTemplate.at=%s", ctld.p(_countOrTemplate.at)))
            _troops = ctld.insertIntoTroopsArray("Paratrooper RPG-16",_countOrTemplate.at,_troops)
            _weight = _weight + getSoldiersWeight(_countOrTemplate.at, ctld.RPG_WEIGHT)
            ctld.logTrace(string.format("_weight=%s", ctld.p(_weight)))
        end

        if _countOrTemplate.mortar then
            ctld.logTrace(string.format("_countOrTemplate.mortar=%s", ctld.p(_countOrTemplate.mortar)))
            _troops = ctld.insertIntoTroopsArray("2B11 mortar",_countOrTemplate.mortar,_troops)
            _weight = _weight + getSoldiersWeight(_countOrTemplate.mortar, ctld.MORTAR_WEIGHT)
            ctld.logTrace(string.format("_weight=%s", ctld.p(_weight)))
        end

        if _countOrTemplate.jtac then
            ctld.logTrace(string.format("_countOrTemplate.jtac=%s", ctld.p(_countOrTemplate.jtac)))
            if _side == 2 then
                _troops = ctld.insertIntoTroopsArray("Soldier M4",_countOrTemplate.jtac,_troops, "JTAC")
            else
                _troops = ctld.insertIntoTroopsArray("Soldier AK",_countOrTemplate.jtac,_troops, "JTAC")
            end
            _hasJTAC = true
            _weight = _weight + getSoldiersWeight(_countOrTemplate.jtac, ctld.JTAC_WEIGHT + ctld.RIFLE_WEIGHT)
            ctld.logTrace(string.format("_weight=%s", ctld.p(_weight)))
        end

    else
        for _i = 1, _countOrTemplate do

            local _unitType = "Soldier AK"

            if _side == 2 then
                if _i <=2 then
                    _unitType = "Soldier M249"
                    _weight = _weight + getSoldiersWeight(1, ctld.MG_WEIGHT)
                    ctld.logTrace(string.format("_unitType=%s, _weight=%s", ctld.p(_unitType), ctld.p(_weight)))
                elseif ctld.spawnRPGWithCoalition and _i > 2 and _i <= 4 then
                    _unitType = "Paratrooper RPG-16"
                    _weight = _weight + getSoldiersWeight(1, ctld.RPG_WEIGHT)
                    ctld.logTrace(string.format("_unitType=%s, _weight=%s", ctld.p(_unitType), ctld.p(_weight)))
                elseif ctld.spawnStinger and _i > 4 and _i <= 5 then
                    _unitType = "Soldier stinger"
                    _weight = _weight + getSoldiersWeight(1, ctld.MANPAD_WEIGHT)
                    ctld.logTrace(string.format("_unitType=%s, _weight=%s", ctld.p(_unitType), ctld.p(_weight)))
                else
                    _unitType = "Soldier M4"
                    _weight = _weight + getSoldiersWeight(1, ctld.RIFLE_WEIGHT)
                    ctld.logTrace(string.format("_unitType=%s, _weight=%s", ctld.p(_unitType), ctld.p(_weight)))
                end
            else
                if _i <=2 then
                    _unitType = "Paratrooper AKS-74"
                    _weight = _weight + getSoldiersWeight(1, ctld.MG_WEIGHT)
                    ctld.logTrace(string.format("_unitType=%s, _weight=%s", ctld.p(_unitType), ctld.p(_weight)))
                elseif ctld.spawnRPGWithCoalition and _i > 2 and _i <= 4 then
                    _unitType = "Paratrooper RPG-16"
                    _weight = _weight + getSoldiersWeight(1, ctld.RPG_WEIGHT)
                    ctld.logTrace(string.format("_unitType=%s, _weight=%s", ctld.p(_unitType), ctld.p(_weight)))
                elseif ctld.spawnStinger and _i > 4 and _i <= 5 then
                    _unitType = "SA-18 Igla manpad"
                    _weight = _weight + getSoldiersWeight(1, ctld.MANPAD_WEIGHT)
                    ctld.logTrace(string.format("_unitType=%s, _weight=%s", ctld.p(_unitType), ctld.p(_weight)))
                else
                    _unitType = "Infantry AK"
                    _weight = _weight + getSoldiersWeight(1, ctld.RIFLE_WEIGHT)
                    ctld.logTrace(string.format("_unitType=%s, _weight=%s", ctld.p(_unitType), ctld.p(_weight)))
                end
            end

            local _unitId = ctld.getNextUnitId()

            _troops[_i] = { type = _unitType, unitId = _unitId, name = string.format("Dropped %s #%i", _unitType, _unitId) }
        end
    end

    local _groupId = ctld.getNextGroupId()
    local _groupName = "Dropped Group"
    if _hasJTAC then
        _groupName = "Dropped JTAC Group"
    end
    local _details = { units = _troops, groupId = _groupId, groupName = string.format("%s %i", _groupName, _groupId), side = _side, country = _country, weight = _weight, jtac = _hasJTAC }
    ctld.logTrace(string.format("total  weight=%s", ctld.p(_weight)))

    return _details
end

--Special F10 function for players for troops
function ctld.unloadExtractTroops(_args)

    local _heli = ctld.getTransportUnit(_args[1])

    if _heli == nil then
        return false
    end


    local _extract = nil
    if not ctld.inAir(_heli) then
        if _heli:getCoalition() == 1 then
            _extract = ctld.findNearestGroup(_heli, ctld.droppedTroopsRED)
        else
            _extract = ctld.findNearestGroup(_heli, ctld.droppedTroopsBLUE)
        end

    end

    if _extract ~= nil and not ctld.troopsOnboard(_heli, true) then
        -- search for nearest troops to pickup
        return ctld.extractTroops({_heli:getName(), true})
    else
        return ctld.unloadTroops({_heli:getName(),true,true})
    end


end

-- load troops onto vehicle
function ctld.loadTroops(_heli, _troops, _numberOrTemplate)

    -- load troops + vehicles if c130 or herc
    -- "M1045 HMMWV TOW"
    -- "M1043 HMMWV Armament"
    local _onboard = ctld.inTransitTroops[_heli:getName()]

    --number doesnt apply to vehicles
    if _numberOrTemplate == nil  or (type(_numberOrTemplate) ~= "table" and type(_numberOrTemplate) ~= "number")  then
        _numberOrTemplate = ctld.getTransportLimit(_heli:getTypeName())
    end

    if _onboard == nil then
        _onboard = { troops = {}, vehicles = {} }
    end

    local _list
    if _heli:getCoalition() == 1 then
        _list = ctld.vehiclesForTransportRED
    else
        _list = ctld.vehiclesForTransportBLUE
    end

    ctld.logTrace(string.format("_troops=%s", ctld.p(_troops)))
    if _troops then
        _onboard.troops = ctld.generateTroopTypes(_heli:getCoalition(), _numberOrTemplate, _heli:getCountry())
        ctld.logTrace(string.format("_onboard.troops=%s", ctld.p(_onboard.troops)))
        trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " loaded troops into " .. _heli:getTypeName(), 10)

        ctld.processCallback({unit = _heli, onboard = _onboard.troops, action = "load_troops"})
    else

        _onboard.vehicles = ctld.generateVehiclesForTransport(_heli:getCoalition(), _heli:getCountry())

        local _count = #_list

        ctld.processCallback({unit = _heli, onboard = _onboard.vehicles, action = "load_vehicles"})

        trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " loaded " .. _count .. " vehicles into " .. _heli:getTypeName(), 10)
    end

    ctld.inTransitTroops[_heli:getName()] = _onboard
    ctld.logTrace(string.format("ctld.inTransitTroops=%s", ctld.p(ctld.inTransitTroops[_heli:getName()])))
    ctld.adaptWeightToCargo(_heli:getName())
end

function ctld.generateVehiclesForTransport(_side, _country)

    local _vehicles = {}
    local _list
    if _side == 1 then
        _list = ctld.vehiclesForTransportRED
    else
        _list = ctld.vehiclesForTransportBLUE
    end


    for _i, _type in ipairs(_list) do

        local _unitId = ctld.getNextUnitId()
        local _weight = ctld.vehiclesWeight[_type] or 2500
        _vehicles[_i] = { type = _type, unitId = _unitId, name = string.format("Dropped %s #%i", _type, _unitId), weight = _weight }
    end


    local _groupId = ctld.getNextGroupId()
    local _details = { units = _vehicles, groupId = _groupId, groupName = string.format("Dropped Group %i", _groupId), side = _side, country = _country }

    return _details
end

function ctld.loadUnloadFOBCrate(_args)

    local _heli = ctld.getTransportUnit(_args[1])
    local _troops = _args[2]

    if _heli == nil then
        return
    end

    if ctld.inAir(_heli) == true then
        return
    end


    local _side = _heli:getCoalition()

    local _inZone = ctld.inLogisticsZone(_heli)
    local _crateOnboard = ctld.inTransitFOBCrates[_heli:getName()] ~= nil

    if _inZone == false and _crateOnboard == true then

        ctld.inTransitFOBCrates[_heli:getName()] = nil

        local _position = _heli:getPosition()

        --try to spawn at 6 oclock to us
        local _angle = math.atan2(_position.x.z, _position.x.x)
        local _xOffset = math.cos(_angle) * -60
        local _yOffset = math.sin(_angle) * -60

        local _point = _heli:getPoint()

        local _side = _heli:getCoalition()

        local _unitId = ctld.getNextUnitId()

        local _name = string.format("FOB Crate #%i", _unitId)

        local _spawnedCrate = ctld.spawnFOBCrateStatic(_heli:getCountry(), ctld.getNextUnitId(), { x = _point.x + _xOffset, z = _point.z + _yOffset }, _name)

        if _side == 1 then
            ctld.droppedFOBCratesRED[_name] = _name
        else
            ctld.droppedFOBCratesBLUE[_name] = _name
        end

        trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " delivered a FOB Crate", 10)

        ctld.displayMessageToGroup(_heli, "Delivered FOB Crate 60m at 6'oclock to you", 10)

    elseif _inZone == true and _crateOnboard == true then

        ctld.displayMessageToGroup(_heli, "FOB Crate dropped back to base", 10)

        ctld.inTransitFOBCrates[_heli:getName()] = nil

    elseif _inZone == true and _crateOnboard == false then
        ctld.displayMessageToGroup(_heli, "FOB Crate Loaded", 10)

        ctld.inTransitFOBCrates[_heli:getName()] = true

        trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " loaded a FOB Crate ready for delivery!", 10)

    else

        -- nearest Crate
        local _crates = ctld.getCratesAndDistance(_heli)
        local _nearestCrate = ctld.getClosestCrate(_heli, _crates, "FOB")

        if _nearestCrate ~= nil and _nearestCrate.dist < 150 then

            ctld.displayMessageToGroup(_heli, "FOB Crate Loaded", 10)
            ctld.inTransitFOBCrates[_heli:getName()] = true

            trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " loaded a FOB Crate ready for delivery!", 10)

            if _side == 1 then
                ctld.droppedFOBCratesRED[_nearestCrate.crateUnit:getName()] = nil
            else
                ctld.droppedFOBCratesBLUE[_nearestCrate.crateUnit:getName()] = nil
            end

            --remove
            _nearestCrate.crateUnit:destroy()

        else
            ctld.displayMessageToGroup(_heli, "There are no friendly logistic units nearby to load a FOB crate from!", 10)
        end
    end
end

function ctld.loadTroopsFromZone(_args)

    local _heli = ctld.getTransportUnit(_args[1])
    local _troops = _args[2]
    local _groupTemplate = _args[3] or ""
    local _allowExtract = _args[4]

    if _heli == nil then
        return false
    end

    local _zone = ctld.inPickupZone(_heli)

    if ctld.troopsOnboard(_heli, _troops) then

        if _troops then
            ctld.displayMessageToGroup(_heli, "You already have troops onboard.", 10)
        else
            ctld.displayMessageToGroup(_heli, "You already have vehicles onboard.", 10)
        end

        return false
    end

    local _extract

    if _allowExtract then
        -- first check for extractable troops regardless of if we're in a zone or not
        if _troops then
            if _heli:getCoalition() == 1 then
                _extract = ctld.findNearestGroup(_heli, ctld.droppedTroopsRED)
            else
                _extract = ctld.findNearestGroup(_heli, ctld.droppedTroopsBLUE)
            end
        else

            if _heli:getCoalition() == 1 then
                _extract = ctld.findNearestGroup(_heli, ctld.droppedVehiclesRED)
            else
                _extract = ctld.findNearestGroup(_heli, ctld.droppedVehiclesBLUE)
            end
        end
    end

    if _extract ~= nil then
        -- search for nearest troops to pickup
        return ctld.extractTroops({_heli:getName(), _troops})
    elseif _zone.inZone == true then

        if _zone.limit - 1 >= 0 then
            -- decrease zone counter by 1
            ctld.updateZoneCounter(_zone.index, -1)

            ctld.loadTroops(_heli, _troops,_groupTemplate)

            return true
        else
            ctld.displayMessageToGroup(_heli, "This area has no more reinforcements available!", 20)

            return false
        end

    else
        if _allowExtract then
            ctld.displayMessageToGroup(_heli, "You are not in a pickup zone and no one is nearby to extract", 10)
        else
            ctld.displayMessageToGroup(_heli, "You are not in a pickup zone", 10)
        end

        return false
    end
end



function ctld.unloadTroops(_args)

    local _heli = ctld.getTransportUnit(_args[1])
    local _troops = _args[2]

    if _heli == nil then
        return false
    end

    local _zone = ctld.inPickupZone(_heli)
    if not ctld.troopsOnboard(_heli, _troops)  then

        ctld.displayMessageToGroup(_heli, "No one to unload", 10)

        return false
    else

        -- troops must be onboard to get here
        if _zone.inZone == true then

            if _troops then
                ctld.displayMessageToGroup(_heli, "Dropped troops back to base", 20)

                ctld.processCallback({unit = _heli, unloaded = ctld.inTransitTroops[_heli:getName()].troops, action = "unload_troops_zone"})

                ctld.inTransitTroops[_heli:getName()].troops = nil

            else
                ctld.displayMessageToGroup(_heli, "Dropped vehicles back to base", 20)

                ctld.processCallback({unit = _heli, unloaded = ctld.inTransitTroops[_heli:getName()].vehicles, action = "unload_vehicles_zone"})

                ctld.inTransitTroops[_heli:getName()].vehicles = nil
            end

            ctld.adaptWeightToCargo(_heli:getName())

            -- increase zone counter by 1
            ctld.updateZoneCounter(_zone.index, 1)

            return true

        elseif ctld.troopsOnboard(_heli, _troops)  then

            return ctld.deployTroops(_heli, _troops)
        end
    end

end

function ctld.extractTroops(_args)

    local _heli = ctld.getTransportUnit(_args[1])
    local _troops = _args[2]

    if _heli == nil then
        return false
    end

    if ctld.inAir(_heli) then
        return false
    end

    if  ctld.troopsOnboard(_heli, _troops)  then
        if _troops then
            ctld.displayMessageToGroup(_heli, "You already have troops onboard.", 10)
        else
            ctld.displayMessageToGroup(_heli, "You already have vehicles onboard.", 10)
        end

        return false
    end

    local _onboard = ctld.inTransitTroops[_heli:getName()]

    if _onboard == nil then
        _onboard = { troops = nil, vehicles = nil }
    end

    local _extracted = false

    if _troops then

        local _extractTroops

        if _heli:getCoalition() == 1 then
            _extractTroops = ctld.findNearestGroup(_heli, ctld.droppedTroopsRED)
        else
            _extractTroops = ctld.findNearestGroup(_heli, ctld.droppedTroopsBLUE)
        end


        if _extractTroops ~= nil then

            local _limit = ctld.getTransportLimit(_heli:getTypeName())

            local _size =  #_extractTroops.group:getUnits()

            if _limit < #_extractTroops.group:getUnits() then

                ctld.displayMessageToGroup(_heli, "Sorry - The group of ".._size.." is too large to fit. \n\nLimit is ".._limit.." for ".._heli:getTypeName(), 20)

                return
            end

            _onboard.troops = _extractTroops.details
            _onboard.troops.weight = #_extractTroops.group:getUnits() * 130 -- default to 130kg per soldier

            if _extractTroops.group:getName():lower():find("jtac") then
                _onboard.troops.jtac = true
            end

            trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " extracted troops in " .. _heli:getTypeName() .. " from combat", 10)

            if _heli:getCoalition() == 1 then
                ctld.droppedTroopsRED[_extractTroops.group:getName()] = nil
            else
                ctld.droppedTroopsBLUE[_extractTroops.group:getName()] = nil
            end

            ctld.processCallback({unit = _heli, extracted = _extractTroops, action = "extract_troops"})

            --remove
            _extractTroops.group:destroy()

            _extracted = true
        else
            _onboard.troops = nil
            ctld.displayMessageToGroup(_heli, "No extractable troops nearby!", 20)
        end

    else

        local _extractVehicles


        if _heli:getCoalition() == 1 then

            _extractVehicles = ctld.findNearestGroup(_heli, ctld.droppedVehiclesRED)
        else

            _extractVehicles = ctld.findNearestGroup(_heli, ctld.droppedVehiclesBLUE)
        end

        if _extractVehicles ~= nil then
            _onboard.vehicles = _extractVehicles.details

            if _heli:getCoalition() == 1 then

                ctld.droppedVehiclesRED[_extractVehicles.group:getName()] = nil
            else

                ctld.droppedVehiclesBLUE[_extractVehicles.group:getName()] = nil
            end

            trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " extracted vehicles in " .. _heli:getTypeName() .. " from combat", 10)

            ctld.processCallback({unit = _heli, extracted = _extractVehicles, action = "extract_vehicles"})
            --remove
            _extractVehicles.group:destroy()
            _extracted = true

        else
            _onboard.vehicles = nil
            ctld.displayMessageToGroup(_heli, "No extractable vehicles nearby!", 20)
        end
    end

    ctld.inTransitTroops[_heli:getName()] = _onboard
    ctld.adaptWeightToCargo(_heli:getName())

    return _extracted
end


function ctld.checkTroopStatus(_args)
    local _unitName = _args[1]
    --list onboard troops, if c130
    local _heli = ctld.getTransportUnit(_unitName)

    if _heli == nil then
        return
    end

    local _, _message = ctld.getWeightOfCargo(_unitName)
    ctld.logTrace(string.format("_message=%s", ctld.p(_message)))
    if _message and _message ~= "" then
        ctld.displayMessageToGroup(_heli, _message, 10)
    end
end

-- Removes troops from transport when it dies
function ctld.checkTransportStatus()

    timer.scheduleFunction(ctld.checkTransportStatus, nil, timer.getTime() + 3)

    for _, _name in ipairs(ctld.transportPilotNames) do

        local _transUnit = ctld.getTransportUnit(_name)

        if _transUnit == nil then
            --env.info("CTLD Transport Unit Dead event")
            ctld.inTransitTroops[_name] = nil
            ctld.inTransitFOBCrates[_name] = nil
            ctld.inTransitSlingLoadCrates[_name] = nil
        end
    end
end

function ctld.adaptWeightToCargo(unitName)
    local _weight = ctld.getWeightOfCargo(unitName)
    trigger.action.setUnitInternalCargo(unitName, _weight)
end

function ctld.getWeightOfCargo(unitName)
    ctld.logDebug(string.format("ctld.getWeightOfCargo(%s)", ctld.p(unitName)))

    local FOB_CRATE_WEIGHT = 800
    local _weight = 0
    local _description = ""

    -- add troops weight
    if ctld.inTransitTroops[unitName] then
        ctld.logTrace("ctld.inTransitTroops = true")
        local _inTransit = ctld.inTransitTroops[unitName]
        if _inTransit then
            ctld.logTrace(string.format("_inTransit=%s", ctld.p(_inTransit)))
            local _troops = _inTransit.troops
            if _troops and _troops.units then
                ctld.logTrace(string.format("_troops.weight=%s", ctld.p(_troops.weight)))
                _description = _description .. string.format("%s troops onboard (%s kg)\n", #_troops.units, _troops.weight)
                _weight = _weight + _troops.weight
            end
            local _vehicles = _inTransit.vehicles
            if _vehicles and _vehicles.units then
                for _, _unit in pairs(_vehicles.units) do
                    _weight = _weight + _unit.weight
                end
                ctld.logTrace(string.format("_weight=%s", ctld.p(_weight)))
                _description = _description .. string.format("%s vehicles onboard (%s kg)\n", #_vehicles.units, _weight)
            end
        end
    end
    ctld.logTrace(string.format("with troops and vehicles : weight = %s", tostring(_weight)))

    -- add FOB crates weight
    if ctld.inTransitFOBCrates[unitName] then
        ctld.logTrace("ctld.inTransitFOBCrates = true")
        _weight = _weight + FOB_CRATE_WEIGHT
        _description = _description .. string.format("1 FOB Crate oboard (%s kg)\n", FOB_CRATE_WEIGHT)
    end
    ctld.logTrace(string.format("with FOB crates : weight = %s", tostring(_weight)))

    -- add simulated slingload crates weight
    local _crate = ctld.inTransitSlingLoadCrates[unitName]
    if _crate then
        ctld.logTrace(string.format("_crate=%s", ctld.p(_crate)))
        if _crate.simulatedSlingload then
            ctld.logTrace(string.format("_crate.weight=%s", ctld.p(_crate.weight)))
            _weight = _weight + _crate.weight
            _description = _description .. string.format("1 %s crate onboard (%s kg)\n", _crate.desc, _crate.weight)
        end
    end
    ctld.logTrace(string.format("with simulated slingload crates : weight = %s", tostring(_weight)))
    if _description ~= "" then
        _description = _description .. string.format("Total weight of cargo : %s kg\n", _weight)
    else
        _description = "No cargo."
    end
    ctld.logTrace(string.format("_description = %s", tostring(_description)))

    return _weight, _description
end

function ctld.checkHoverStatus()
    --ctld.logDebug(string.format("ctld.checkHoverStatus()"))
    timer.scheduleFunction(ctld.checkHoverStatus, nil, timer.getTime() + 1.0)

    local _status, _result = pcall(function()

        for _, _name in ipairs(ctld.transportPilotNames) do

            local _reset = true
            local _transUnit = ctld.getTransportUnit(_name)

            --only check transports that are hovering and not planes
            if _transUnit ~= nil and ctld.inTransitSlingLoadCrates[_name] == nil and ctld.inAir(_transUnit) and ctld.unitCanCarryVehicles(_transUnit) == false then

                --ctld.logTrace(string.format("%s - capable of slingloading", ctld.p(_name)))

                local _crates = ctld.getCratesAndDistance(_transUnit)
                --ctld.logTrace(string.format("_crates = %s", ctld.p(_crates)))

                for _, _crate in pairs(_crates) do
                    --ctld.logTrace(string.format("_crate = %s", ctld.p(_crate)))
                    if _crate.dist < ctld.maxDistanceFromCrate and _crate.details.unit ~= "FOB" then

                        --check height!
                        local _height = _transUnit:getPoint().y - _crate.crateUnit:getPoint().y
                        --env.info("HEIGHT " .. _name .. " " .. _height .. " " .. _transUnit:getPoint().y .. " " .. _crate.crateUnit:getPoint().y)
                        --  ctld.heightDiff(_transUnit)
                        --env.info("HEIGHT ABOVE GROUD ".._name.." ".._height.." ".._transUnit:getPoint().y.." ".._crate.crateUnit:getPoint().y)
                        --ctld.logTrace(string.format("_height = %s", ctld.p(_height)))

                        if _height > ctld.minimumHoverHeight and _height <= ctld.maximumHoverHeight then

                            local _time = ctld.hoverStatus[_transUnit:getName()]
                            --ctld.logTrace(string.format("_time = %s", ctld.p(_time)))

                            if _time == nil then
                                ctld.hoverStatus[_transUnit:getName()] = ctld.hoverTime
                                _time = ctld.hoverTime
                            else
                                _time = ctld.hoverStatus[_transUnit:getName()] - 1
                                ctld.hoverStatus[_transUnit:getName()] = _time
                            end

                            if _time > 0 then
                                ctld.displayMessageToGroup(_transUnit, "Hovering above " .. _crate.details.desc .. " crate. \n\nHold hover for " .. _time .. " seconds! \n\nIf the countdown stops you're too far away!", 10,true)
                            else
                                ctld.hoverStatus[_transUnit:getName()] = nil
                                ctld.displayMessageToGroup(_transUnit, "Loaded  " .. _crate.details.desc .. " crate!", 10,true)

                                --crates been moved once!
                                ctld.crateMove[_crate.crateUnit:getName()] = nil

                                if _transUnit:getCoalition() == 1 then
                                    ctld.spawnedCratesRED[_crate.crateUnit:getName()] = nil
                                else
                                    ctld.spawnedCratesBLUE[_crate.crateUnit:getName()] = nil
                                end

                                _crate.crateUnit:destroy()

                                local _copiedCrate = mist.utils.deepCopy(_crate.details)
                                _copiedCrate.simulatedSlingload = true
                                --ctld.logTrace(string.format("_copiedCrate = %s", ctld.p(_copiedCrate)))
                                ctld.inTransitSlingLoadCrates[_name] = _copiedCrate
                                ctld.adaptWeightToCargo(_name)
                            end

                            _reset = false

                            break
                        elseif _height <= ctld.minimumHoverHeight then
                            ctld.displayMessageToGroup(_transUnit, "Too low to hook " .. _crate.details.desc .. " crate.\n\nHold hover for " .. ctld.hoverTime .. " seconds", 5,true)
                            break
                        else
                            ctld.displayMessageToGroup(_transUnit, "Too high to hook " .. _crate.details.desc .. " crate.\n\nHold hover for " .. ctld.hoverTime .. " seconds", 5, true)
                            break
                        end
                    end
                end
            end

            if _reset then
                ctld.hoverStatus[_name] = nil
            end
        end
    end)

    if (not _status) then
        env.error(string.format("CTLD ERROR: %s", _result))
    end
end

function ctld.loadNearbyCrate(_name)
    local _transUnit = ctld.getTransportUnit(_name)

    if _transUnit ~= nil  then

        if ctld.inAir(_transUnit) then
            ctld.displayMessageToGroup(_transUnit, "You must land before you can load a crate!", 10,true)
            return
        end

        if ctld.inTransitSlingLoadCrates[_name] == nil then
            local _crates = ctld.getCratesAndDistance(_transUnit)

            for _, _crate in pairs(_crates) do

                if _crate.dist < 50.0 then
                    ctld.displayMessageToGroup(_transUnit, "Loaded  " .. _crate.details.desc .. " crate!", 10,true)

                    if _transUnit:getCoalition() == 1 then
                        ctld.spawnedCratesRED[_crate.crateUnit:getName()] = nil
                    else
                        ctld.spawnedCratesBLUE[_crate.crateUnit:getName()] = nil
                    end

                    ctld.crateMove[_crate.crateUnit:getName()] = nil

                    _crate.crateUnit:destroy()

                    local _copiedCrate = mist.utils.deepCopy(_crate.details)
                    _copiedCrate.simulatedSlingload = true
                    ctld.inTransitSlingLoadCrates[_name] = _copiedCrate
                    ctld.adaptWeightToCargo(_name)
                    return
                end
            end

            ctld.displayMessageToGroup(_transUnit, "No Crates within 50m to load!", 10,true)

        else
            -- crate onboard
            ctld.displayMessageToGroup(_transUnit, "You already have a "..ctld.inTransitSlingLoadCrates[_name].desc.." crate onboard!", 10,true)
        end
    end


end

--recreates beacons to make sure they work!
function ctld.refreshRadioBeacons()

    timer.scheduleFunction(ctld.refreshRadioBeacons, nil, timer.getTime() + 30)


    for _index, _beaconDetails in ipairs(ctld.deployedRadioBeacons) do

        --trigger.action.outTextForCoalition(_beaconDetails.coalition,_beaconDetails.text,10)
        if ctld.updateRadioBeacon(_beaconDetails) == false then

            --search used frequencies + remove, add back to unused

            for _i, _freq in ipairs(ctld.usedUHFFrequencies) do
                if _freq == _beaconDetails.uhf then

                    table.insert(ctld.freeUHFFrequencies, _freq)
                    table.remove(ctld.usedUHFFrequencies, _i)
                end
            end

            for _i, _freq in ipairs(ctld.usedVHFFrequencies) do
                if _freq == _beaconDetails.vhf then

                    table.insert(ctld.freeVHFFrequencies, _freq)
                    table.remove(ctld.usedVHFFrequencies, _i)
                end
            end

            for _i, _freq in ipairs(ctld.usedFMFrequencies) do
                if _freq == _beaconDetails.fm then

                    table.insert(ctld.freeFMFrequencies, _freq)
                    table.remove(ctld.usedFMFrequencies, _i)
                end
            end

            --clean up beacon table
            table.remove(ctld.deployedRadioBeacons, _index)
        end
    end
end

function ctld.getClockDirection(_heli, _crate)

    -- Source: Helicopter Script - Thanks!

    local _position = _crate:getPosition().p -- get position of crate
    local _playerPosition = _heli:getPosition().p -- get position of helicopter
    local _relativePosition = mist.vec.sub(_position, _playerPosition)

    local _playerHeading = mist.getHeading(_heli) -- the rest of the code determines the 'o'clock' bearing of the missile relative to the helicopter

    local _headingVector = { x = math.cos(_playerHeading), y = 0, z = math.sin(_playerHeading) }

    local _headingVectorPerpendicular = { x = math.cos(_playerHeading + math.pi / 2), y = 0, z = math.sin(_playerHeading + math.pi / 2) }

    local _forwardDistance = mist.vec.dp(_relativePosition, _headingVector)

    local _rightDistance = mist.vec.dp(_relativePosition, _headingVectorPerpendicular)

    local _angle = math.atan2(_rightDistance, _forwardDistance) * 180 / math.pi

    if _angle < 0 then
        _angle = 360 + _angle
    end
    _angle = math.floor(_angle * 12 / 360 + 0.5)
    if _angle == 0 then
        _angle = 12
    end

    return _angle
end


function ctld.getCompassBearing(_ref, _unitPos)

    _ref = mist.utils.makeVec3(_ref, 0) -- turn it into Vec3 if it is not already.
    _unitPos = mist.utils.makeVec3(_unitPos, 0) -- turn it into Vec3 if it is not already.

    local _vec = { x = _unitPos.x - _ref.x, y = _unitPos.y - _ref.y, z = _unitPos.z - _ref.z }

    local _dir = mist.utils.getDir(_vec, _ref)

    local _bearing = mist.utils.round(mist.utils.toDegree(_dir), 0)

    return _bearing
end

function ctld.listNearbyCrates(_args)

    local _message = ""

    local _heli = ctld.getTransportUnit(_args[1])

    if _heli == nil then

        return -- no heli!
    end

    local _crates = ctld.getCratesAndDistance(_heli)

    --sort
    local _sort = function( a,b ) return a.dist < b.dist end
    table.sort(_crates,_sort)

    for _, _crate in pairs(_crates) do

        if _crate.dist < 1000 and _crate.details.unit ~= "FOB" then
            _message = string.format("%s\n%s crate - kg %i - %i m - %d o'clock", _message, _crate.details.desc, _crate.details.weight, _crate.dist, ctld.getClockDirection(_heli, _crate.crateUnit))
        end
    end


    local _fobMsg = ""
    for _, _fobCrate in pairs(_crates) do

        if _fobCrate.dist < 1000 and _fobCrate.details.unit == "FOB" then
            _fobMsg = _fobMsg .. string.format("FOB Crate - %d m - %d o'clock\n", _fobCrate.dist, ctld.getClockDirection(_heli, _fobCrate.crateUnit))
        end
    end

    if _message ~= "" or _fobMsg ~= "" then

        local _txt = ""

        if _message ~= "" then
            _txt = "Nearby Crates:\n" .. _message
        end

        if _fobMsg ~= "" then

            if _message ~= "" then
                _txt = _txt .. "\n\n"
            end

            _txt = _txt .. "Nearby FOB Crates (Not Slingloadable):\n" .. _fobMsg
        end

        ctld.displayMessageToGroup(_heli, _txt, 20)

    else
        --no crates nearby

        local _txt = "No Nearby Crates"

        ctld.displayMessageToGroup(_heli, _txt, 20)
    end
end


function ctld.listFOBS(_args)

    local _msg = "FOB Positions:"

    local _heli = ctld.getTransportUnit(_args[1])

    if _heli == nil then

        return -- no heli!
    end

    -- get fob positions

    local _fobs = ctld.getSpawnedFobs(_heli)

    -- now check spawned fobs
    for _, _fob in ipairs(_fobs) do
        _msg = string.format("%s\nFOB @ %s", _msg, ctld.getFOBPositionString(_fob))
    end

    if _msg == "FOB Positions:" then
        ctld.displayMessageToGroup(_heli, "Sorry, there are no active FOBs!", 20)
    else
        ctld.displayMessageToGroup(_heli, _msg, 20)
    end
end

function ctld.getFOBPositionString(_fob)

    local _lat, _lon = coord.LOtoLL(_fob:getPosition().p)

    local _latLngStr = mist.tostringLL(_lat, _lon, 3, ctld.location_DMS)

    --   local _mgrsString = mist.tostringMGRS(coord.LLtoMGRS(coord.LOtoLL(_fob:getPosition().p)), 5)

    local _message = _latLngStr

    local _beaconInfo = ctld.fobBeacons[_fob:getName()]

    if _beaconInfo ~= nil then
        _message = string.format("%s - %.2f KHz ", _message, _beaconInfo.vhf / 1000)
        _message = string.format("%s - %.2f MHz ", _message, _beaconInfo.uhf / 1000000)
        _message = string.format("%s - %.2f MHz ", _message, _beaconInfo.fm / 1000000)
    end

    return _message
end


function ctld.displayMessageToGroup(_unit, _text, _time,_clear)

    local _groupId = ctld.getGroupId(_unit)
    if _groupId then
        if _clear == true then
            trigger.action.outTextForGroup(_groupId, _text, _time,_clear)
        else
            trigger.action.outTextForGroup(_groupId, _text, _time)
        end
    end
end

function ctld.heightDiff(_unit)

    local _point = _unit:getPoint()

    -- env.info("heightunit " .. _point.y)
    --env.info("heightland " .. land.getHeight({ x = _point.x, y = _point.z }))

    return _point.y - land.getHeight({ x = _point.x, y = _point.z })
end

--includes fob crates!
function ctld.getCratesAndDistance(_heli)

    local _crates = {}

    local _allCrates
    if _heli:getCoalition() == 1 then
        _allCrates = ctld.spawnedCratesRED
    else
        _allCrates = ctld.spawnedCratesBLUE
    end

    for _crateName, _details in pairs(_allCrates) do

        --get crate
        local _crate = ctld.getCrateObject(_crateName)

        --in air seems buggy with crates so if in air is true, get the height above ground and the speed magnitude
        if _crate ~= nil and _crate:getLife() > 0
                and (ctld.inAir(_crate) == false) then

            local _dist = ctld.getDistance(_crate:getPoint(), _heli:getPoint())

            local _crateDetails = { crateUnit = _crate, dist = _dist, details = _details }

            table.insert(_crates, _crateDetails)
        end
    end

    local _fobCrates
    if _heli:getCoalition() == 1 then
        _fobCrates = ctld.droppedFOBCratesRED
    else
        _fobCrates = ctld.droppedFOBCratesBLUE
    end

    for _crateName, _details in pairs(_fobCrates) do

        --get crate
        local _crate = ctld.getCrateObject(_crateName)

        if _crate ~= nil and _crate:getLife() > 0 then

            local _dist = ctld.getDistance(_crate:getPoint(), _heli:getPoint())

            local _crateDetails = { crateUnit = _crate, dist = _dist, details = { unit = "FOB" }, }

            table.insert(_crates, _crateDetails)
        end
    end

    return _crates
end


function ctld.getClosestCrate(_heli, _crates, _type)

    local _closetCrate = nil
    local _shortestDistance = -1
    local _distance = 0

    for _, _crate in pairs(_crates) do

        if (_crate.details.unit == _type or _type == nil) then
            _distance = _crate.dist

            if _distance ~= nil and (_shortestDistance == -1 or _distance < _shortestDistance) then
                _shortestDistance = _distance
                _closetCrate = _crate
            end
        end
    end

    return _closetCrate
end

function ctld.findNearestAASystem(_heli,_aaSystem)

    local _closestHawkGroup = nil
    local _shortestDistance = -1
    local _distance = 0

    for _groupName, _hawkDetails in pairs(ctld.completeAASystems) do

        local _hawkGroup = Group.getByName(_groupName)

        --  env.info(_groupName..": "..mist.utils.tableShow(_hawkDetails))
        if _hawkGroup ~= nil and _hawkGroup:getCoalition() == _heli:getCoalition() and _hawkDetails[1].system.name == _aaSystem.name then

            local _units = _hawkGroup:getUnits()

            for _, _leader in pairs(_units) do

                if _leader ~= nil and _leader:getLife() > 0 then

                    _distance = ctld.getDistance(_leader:getPoint(), _heli:getPoint())

                    if _distance ~= nil and (_shortestDistance == -1 or _distance < _shortestDistance) then
                        _shortestDistance = _distance
                        _closestHawkGroup = _hawkGroup
                    end

                    break
                end
            end
        end
    end

    if _closestHawkGroup ~= nil then

        return { group = _closestHawkGroup, dist = _shortestDistance }
    end
    return nil
end

function ctld.getCrateObject(_name)
    local _crate

    if ctld.staticBugWorkaround then
        _crate  = Unit.getByName(_name)
    else
        _crate = StaticObject.getByName(_name)
    end
    return _crate
end



function ctld.unpackCrates(_arguments)

    local _status, _err = pcall(function(_args)

        -- trigger.action.outText("Unpack Crates".._args[1],10)

        local _heli = ctld.getTransportUnit(_args[1])

        if _heli ~= nil and ctld.inAir(_heli) == false then

            local _crates = ctld.getCratesAndDistance(_heli)
            local _crate = ctld.getClosestCrate(_heli, _crates)


            if ctld.inLogisticsZone(_heli) == true  or  ctld.farEnoughFromLogisticZone(_heli) == false then

                ctld.displayMessageToGroup(_heli, "You can't unpack that here! Take it to where it's needed!", 20)

                return
            end



            if _crate ~= nil and _crate.dist < 750
                    and (_crate.details.unit == "FOB" or _crate.details.unit == "FOB-SMALL") then

                ctld.unpackFOBCrates(_crates, _heli)

                return

            elseif _crate ~= nil and _crate.dist < 200 then

                if ctld.forceCrateToBeMoved and ctld.crateMove[_crate.crateUnit:getName()] then
                    ctld.displayMessageToGroup(_heli,"Sorry you must move this crate before you unpack it!", 20)
                    return
                end


                local _aaTemplate = ctld.getAATemplate(_crate.details.unit)

                if _aaTemplate then

                    if _crate.details.unit == _aaTemplate.repair then
                        ctld.repairAASystem(_heli, _crate,_aaTemplate)
                    else
                        ctld.unpackAASystem(_heli, _crate, _crates,_aaTemplate)
                    end

                    return -- stop processing
                    -- is multi crate?
                elseif _crate.details.cratesRequired ~= nil and _crate.details.cratesRequired > 1 then
                    -- multicrate

                    ctld.unpackMultiCrate(_heli, _crate, _crates)

                    return

                else
                    -- single crate
                    local _cratePoint = _crate.crateUnit:getPoint()
                    local _crateName = _crate.crateUnit:getName()

                    -- ctld.spawnCrateStatic( _heli:getCoalition(),ctld.getNextUnitId(),{x=100,z=100},_crateName,100)

                    --remove crate
                  --  if ctld.slingLoad == false then
                        _crate.crateUnit:destroy()
                   -- end

                    local _spawnedGroups = ctld.spawnCrateGroup(_heli, { _cratePoint }, { _crate.details.unit })

                    if _heli:getCoalition() == 1 then
                        ctld.spawnedCratesRED[_crateName] = nil
                    else
                        ctld.spawnedCratesBLUE[_crateName] = nil
                    end

                    ctld.processCallback({unit = _heli, crate = _crate , spawnedGroup = _spawnedGroups, action = "unpack"})

                    if _crate.details.unit == "1L13 EWR" then
                        ctld.addEWRTask(_spawnedGroups)

                        --       env.info("Added EWR")
                    end


                    trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " successfully deployed " .. _crate.details.desc .. " to the field", 10)

                    if ctld.isJTACUnitType(_crate.details.unit) and ctld.JTAC_dropEnabled then

                        local _code = table.remove(ctld.jtacGeneratedLaserCodes, 1)
                        --put to the end
                        table.insert(ctld.jtacGeneratedLaserCodes, _code)

                        ctld.JTACAutoLase(_spawnedGroups:getName(), _code) --(_jtacGroupName, _laserCode, _smoke, _lock, _colour)
                    end
                end

            else

                ctld.displayMessageToGroup(_heli, "No friendly crates close enough to unpack", 20)
            end
        end
    end, _arguments)

    if (not _status) then
        env.error(string.format("CTLD ERROR: %s", _err))
    end
end


-- builds a fob!
function ctld.unpackFOBCrates(_crates, _heli)

    if ctld.inLogisticsZone(_heli) == true then

        ctld.displayMessageToGroup(_heli, "You can't unpack that here! Take it to where it's needed!", 20)

        return
    end

    -- unpack multi crate
    local _nearbyMultiCrates = {}

    local _bigFobCrates = 0
    local _smallFobCrates = 0
    local _totalCrates = 0

    for _, _nearbyCrate in pairs(_crates) do

        if _nearbyCrate.dist < 750  then

            if  _nearbyCrate.details.unit == "FOB" then
                _bigFobCrates = _bigFobCrates + 1
                table.insert(_nearbyMultiCrates, _nearbyCrate)
            elseif _nearbyCrate.details.unit == "FOB-SMALL" then
                _smallFobCrates = _smallFobCrates + 1
                table.insert(_nearbyMultiCrates, _nearbyCrate)
            end

            --catch divide by 0
            if _smallFobCrates > 0 then
                _totalCrates = _bigFobCrates + (_smallFobCrates/3.0)
            else
                _totalCrates = _bigFobCrates
            end

            if _totalCrates >= ctld.cratesRequiredForFOB then
                break
            end
        end
    end

    --- check crate count
    if _totalCrates >= ctld.cratesRequiredForFOB then

        -- destroy crates

        local _points = {}

        for _, _crate in pairs(_nearbyMultiCrates) do

            if _heli:getCoalition() == 1 then
                ctld.droppedFOBCratesRED[_crate.crateUnit:getName()] = nil
                ctld.spawnedCratesRED[_crate.crateUnit:getName()] = nil
            else
                ctld.droppedFOBCratesBLUE[_crate.crateUnit:getName()] = nil
                ctld.spawnedCratesBLUE[_crate.crateUnit:getName()] = nil
            end

            table.insert(_points, _crate.crateUnit:getPoint())

            --destroy
            _crate.crateUnit:destroy()
        end

        local _centroid = ctld.getCentroid(_points)

        timer.scheduleFunction(function(_args)

            local _unitId = ctld.getNextUnitId()
            local _name = "Deployed FOB #" .. _unitId

            local _fob = ctld.spawnFOB(_args[2], _unitId, _args[1], _name)

            --make it able to deploy crates
            table.insert(ctld.logisticUnits, _fob:getName())

            ctld.beaconCount = ctld.beaconCount + 1

            local _radioBeaconName = "FOB Beacon #" .. ctld.beaconCount

            local _radioBeaconDetails = ctld.createRadioBeacon(_args[1], _args[3], _args[2], _radioBeaconName, nil, true)

            ctld.fobBeacons[_name] = { vhf = _radioBeaconDetails.vhf, uhf = _radioBeaconDetails.uhf, fm = _radioBeaconDetails.fm }

            if ctld.troopPickupAtFOB == true then
                table.insert(ctld.builtFOBS, _fob:getName())

                trigger.action.outTextForCoalition(_args[3], "Finished building FOB! Crates and Troops can now be picked up.", 10)
            else
                trigger.action.outTextForCoalition(_args[3], "Finished building FOB! Crates can now be picked up.", 10)
            end
        end, { _centroid, _heli:getCountry(), _heli:getCoalition() }, timer.getTime() + ctld.buildTimeFOB)

        local _txt = string.format("%s started building FOB using %d FOB crates, it will be finished in %d seconds.\nPosition marked with smoke.", ctld.getPlayerNameOrType(_heli), _totalCrates, ctld.buildTimeFOB)

        ctld.processCallback({unit = _heli, position = _centroid, action = "fob"})

        trigger.action.smoke(_centroid, trigger.smokeColor.Green)

        trigger.action.outTextForCoalition(_heli:getCoalition(), _txt, 10)
    else
        local _txt = string.format("Cannot build FOB!\n\nIt requires %d Large FOB crates ( 3 small FOB crates equal 1 large FOB Crate) and there are the equivalent of %d large FOB crates nearby\n\nOr the crates are not within 750m of each other", ctld.cratesRequiredForFOB, _totalCrates)
        ctld.displayMessageToGroup(_heli, _txt, 20)
    end
end

--unloads the sling crate when the helicopter is on the ground or between 4.5 - 10 meters
function ctld.dropSlingCrate(_args)
    local _heli = ctld.getTransportUnit(_args[1])

    if _heli == nil then
        return -- no heli!
    end

    local _currentCrate = ctld.inTransitSlingLoadCrates[_heli:getName()]

    if _currentCrate == nil then
        if ctld.hoverPickup then
            ctld.displayMessageToGroup(_heli, "You are not currently transporting any crates. \n\nTo Pickup a crate, hover for "..ctld.hoverTime.." seconds above the crate", 10)
        else
            ctld.displayMessageToGroup(_heli, "You are not currently transporting any crates. \n\nTo Pickup a crate - land and use F10 Crate Commands to load one.", 10)
        end
    else

        local _heli = ctld.getTransportUnit(_args[1])

        local _point = _heli:getPoint()

        local _unitId = ctld.getNextUnitId()

        local _side = _heli:getCoalition()

        local _name = string.format("%s #%i", _currentCrate.desc, _unitId)


        local _heightDiff = ctld.heightDiff(_heli)

        if ctld.inAir(_heli) == false or _heightDiff <= 7.5 then
            ctld.displayMessageToGroup(_heli, _currentCrate.desc .. " crate has been safely unhooked and is at your 12 o'clock", 10)
            _point = ctld.getPointAt12Oclock(_heli, 30)
            --        elseif _heightDiff > 40.0 then
            --            ctld.inTransitSlingLoadCrates[_heli:getName()] = nil
            --            ctld.displayMessageToGroup(_heli, "You were too high! The crate has been destroyed", 10)
            --            return
        elseif _heightDiff > 7.5 and _heightDiff <= 40.0 then
            ctld.displayMessageToGroup(_heli, _currentCrate.desc .. " crate has been safely dropped below you", 10)
        else -- _heightDiff > 40.0
            ctld.inTransitSlingLoadCrates[_heli:getName()] = nil
            ctld.displayMessageToGroup(_heli, "You were too high! The crate has been destroyed", 10)
            return
        end


        --remove crate from cargo
        ctld.inTransitSlingLoadCrates[_heli:getName()] = nil
        ctld.adaptWeightToCargo(_heli:getName())
        local _spawnedCrate = ctld.spawnCrateStatic(_heli:getCountry(), _unitId, _point, _name, _currentCrate.weight,_side)
    end
end

--spawns a radio beacon made up of two units,
-- one for VHF and one for UHF
-- The units are set to to NOT engage
function ctld.createRadioBeacon(_point, _coalition, _country, _name, _batteryTime, _isFOB)

    local _uhfGroup = ctld.spawnRadioBeaconUnit(_point, _country, "UHF")
    local _vhfGroup = ctld.spawnRadioBeaconUnit(_point, _country, "VHF")
    local _fmGroup = ctld.spawnRadioBeaconUnit(_point, _country, "FM")

    local _freq = ctld.generateADFFrequencies()

    --create timeout
    local _battery

    if _batteryTime == nil then
        _battery = timer.getTime() + (ctld.deployedBeaconBattery * 60)
    else
        _battery = timer.getTime() + (_batteryTime * 60)
    end

    local _lat, _lon = coord.LOtoLL(_point)

    local _latLngStr = mist.tostringLL(_lat, _lon, 3, ctld.location_DMS)

    --local _mgrsString = mist.tostringMGRS(coord.LLtoMGRS(coord.LOtoLL(_point)), 5)

    local _message = _name

    if _isFOB then
        --  _message = "FOB " .. _message
        _battery = -1 --never run out of power!
    end

    _message = _message .. " - " .. _latLngStr

    --  env.info("GEN UHF: ".. _freq.uhf)
    --  env.info("GEN VHF: ".. _freq.vhf)

    _message = string.format("%s - %.2f KHz", _message, _freq.vhf / 1000)

    _message = string.format("%s - %.2f MHz", _message, _freq.uhf / 1000000)

    _message = string.format("%s - %.2f MHz ", _message, _freq.fm / 1000000)



    local _beaconDetails = {
        vhf = _freq.vhf,
        vhfGroup = _vhfGroup:getName(),
        uhf = _freq.uhf,
        uhfGroup = _uhfGroup:getName(),
        fm = _freq.fm,
        fmGroup = _fmGroup:getName(),
        text = _message,
        battery = _battery,
        coalition = _coalition,
    }
    ctld.updateRadioBeacon(_beaconDetails)

    table.insert(ctld.deployedRadioBeacons, _beaconDetails)

    return _beaconDetails
end

function ctld.generateADFFrequencies()

    if #ctld.freeUHFFrequencies <= 3 then
        ctld.freeUHFFrequencies = ctld.usedUHFFrequencies
        ctld.usedUHFFrequencies = {}
    end

    --remove frequency at RANDOM
    local _uhf = table.remove(ctld.freeUHFFrequencies, math.random(#ctld.freeUHFFrequencies))
    table.insert(ctld.usedUHFFrequencies, _uhf)


    if #ctld.freeVHFFrequencies <= 3 then
        ctld.freeVHFFrequencies = ctld.usedVHFFrequencies
        ctld.usedVHFFrequencies = {}
    end

    local _vhf = table.remove(ctld.freeVHFFrequencies, math.random(#ctld.freeVHFFrequencies))
    table.insert(ctld.usedVHFFrequencies, _vhf)

    if #ctld.freeFMFrequencies <= 3 then
        ctld.freeFMFrequencies = ctld.usedFMFrequencies
        ctld.usedFMFrequencies = {}
    end

    local _fm = table.remove(ctld.freeFMFrequencies, math.random(#ctld.freeFMFrequencies))
    table.insert(ctld.usedFMFrequencies, _fm)

    return { uhf = _uhf, vhf = _vhf, fm = _fm }
    --- return {uhf=_uhf,vhf=_vhf}
end



function ctld.spawnRadioBeaconUnit(_point, _country, _type)

    local _groupId = ctld.getNextGroupId()

    local _unitId = ctld.getNextUnitId()

    local _radioGroup = {
        ["visible"] = false,
       -- ["groupId"] = _groupId,
        ["hidden"] = false,
        ["units"] = {
            [1] = {
                ["y"] = _point.z,
                ["type"] = "TACAN_beacon",
                ["name"] = _type .. " Radio Beacon Unit #" .. _unitId,
             --   ["unitId"] = _unitId,
                ["heading"] = 0,
                ["playerCanDrive"] = true,
                ["skill"] = "Excellent",
                ["x"] = _point.x,
            }
        },
        --        ["y"] = _positions[1].z,
        --        ["x"] = _positions[1].x,
        ["name"] = _type .. " Radio Beacon Group #" .. _groupId,
        ["task"] = {},
        --added two fields below for MIST
        ["category"] = Group.Category.GROUND,
        ["country"] = _country
    }

    -- return coalition.addGroup(_country, Group.Category.GROUND, _radioGroup)
    return Group.getByName(mist.dynAdd(_radioGroup).name)
end

function ctld.updateRadioBeacon(_beaconDetails)

    local _vhfGroup = Group.getByName(_beaconDetails.vhfGroup)

    local _uhfGroup = Group.getByName(_beaconDetails.uhfGroup)

    local _fmGroup = Group.getByName(_beaconDetails.fmGroup)

    local _radioLoop = {}

    if _vhfGroup ~= nil and _vhfGroup:getUnits() ~= nil and #_vhfGroup:getUnits() == 1 then
        table.insert(_radioLoop, { group = _vhfGroup, freq = _beaconDetails.vhf, silent = false, mode = 0 })
    end

    if _uhfGroup ~= nil and _uhfGroup:getUnits() ~= nil and #_uhfGroup:getUnits() == 1 then
        table.insert(_radioLoop, { group = _uhfGroup, freq = _beaconDetails.uhf, silent = true, mode = 0 })
    end

    if _fmGroup ~= nil and _fmGroup:getUnits() ~= nil and #_fmGroup:getUnits() == 1 then
        table.insert(_radioLoop, { group = _fmGroup, freq = _beaconDetails.fm, silent = false, mode = 1 })
    end

    local _batLife = _beaconDetails.battery - timer.getTime()

    if (_batLife <= 0 and _beaconDetails.battery ~= -1) or #_radioLoop ~= 3 then
        -- ran out of batteries

        if _vhfGroup ~= nil then
            _vhfGroup:destroy()
        end
        if _uhfGroup ~= nil then
            _uhfGroup:destroy()
        end
        if _fmGroup ~= nil then
            _fmGroup:destroy()
        end

        return false
    end

    --fobs have unlimited battery life
    --    if _battery ~= -1 then
    --        _text = _text.." "..mist.utils.round(_batLife).." seconds of battery"
    --    end

    for _, _radio in pairs(_radioLoop) do

        local _groupController = _radio.group:getController()

        local _sound = ctld.radioSound
        if _radio.silent then
            _sound = ctld.radioSoundFC3
        end

        _sound = "l10n/DEFAULT/".._sound

        _groupController:setOption(AI.Option.Ground.id.ROE, AI.Option.Ground.val.ROE.WEAPON_HOLD)

        trigger.action.radioTransmission(_sound, _radio.group:getUnit(1):getPoint(), _radio.mode, false, _radio.freq, 1000)
        --This function doesnt actually stop transmitting when then sound is false. My hope is it will stop if a new beacon is created on the same
        -- frequency... OR they fix the bug where it wont stop.
        --        end

        --
    end

    return true

    --  trigger.action.radioTransmission(ctld.radioSound, _point, 1, true, _frequency, 1000)
end

function ctld.listRadioBeacons(_args)

    local _heli = ctld.getTransportUnit(_args[1])
    local _message = ""

    if _heli ~= nil then

        for _x, _details in pairs(ctld.deployedRadioBeacons) do

            if _details.coalition == _heli:getCoalition() then
                _message = _message .. _details.text .. "\n"
            end
        end

        if _message ~= "" then
            ctld.displayMessageToGroup(_heli, "Radio Beacons:\n" .. _message, 20)
        else
            ctld.displayMessageToGroup(_heli, "No Active Radio Beacons", 20)
        end
    end
end

function ctld.dropRadioBeacon(_args)

    local _heli = ctld.getTransportUnit(_args[1])
    local _message = ""

    if _heli ~= nil and ctld.inAir(_heli) == false then

        --deploy 50 m infront
        --try to spawn at 12 oclock to us
        local _point = ctld.getPointAt12Oclock(_heli, 50)

        ctld.beaconCount = ctld.beaconCount + 1
        local _name = "Beacon #" .. ctld.beaconCount

        local _radioBeaconDetails = ctld.createRadioBeacon(_point, _heli:getCoalition(), _heli:getCountry(), _name, nil, false)

        -- mark with flare?

        trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " deployed a Radio Beacon.\n\n" .. _radioBeaconDetails.text, 20)

    else
        ctld.displayMessageToGroup(_heli, "You need to land before you can deploy a Radio Beacon!", 20)
    end
end

--remove closet radio beacon
function ctld.removeRadioBeacon(_args)

    local _heli = ctld.getTransportUnit(_args[1])
    local _message = ""

    if _heli ~= nil and ctld.inAir(_heli) == false then

        -- mark with flare?

        local _closetBeacon = nil
        local _shortestDistance = -1
        local _distance = 0

        for _x, _details in pairs(ctld.deployedRadioBeacons) do

            if _details.coalition == _heli:getCoalition() then

                local _group = Group.getByName(_details.vhfGroup)

                if _group ~= nil and #_group:getUnits() == 1 then

                    _distance = ctld.getDistance(_heli:getPoint(), _group:getUnit(1):getPoint())
                    if _distance ~= nil and (_shortestDistance == -1 or _distance < _shortestDistance) then
                        _shortestDistance = _distance
                        _closetBeacon = _details
                    end
                end
            end
        end

        if _closetBeacon ~= nil and _shortestDistance then
            local _vhfGroup = Group.getByName(_closetBeacon.vhfGroup)

            local _uhfGroup = Group.getByName(_closetBeacon.uhfGroup)

            local _fmGroup = Group.getByName(_closetBeacon.fmGroup)

            if _vhfGroup ~= nil then
                _vhfGroup:destroy()
            end
            if _uhfGroup ~= nil then
                _uhfGroup:destroy()
            end
            if _fmGroup ~= nil then
                _fmGroup:destroy()
            end

            trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " removed a Radio Beacon.\n\n" .. _closetBeacon.text, 20)
        else
            ctld.displayMessageToGroup(_heli, "No Radio Beacons within 500m.", 20)
        end

    else
        ctld.displayMessageToGroup(_heli, "You need to land before remove a Radio Beacon", 20)
    end
end

-- gets the center of a bunch of points!
-- return proper DCS point with height
function ctld.getCentroid(_points)
    local _tx, _ty = 0, 0
    for _index, _point in ipairs(_points) do
        _tx = _tx + _point.x
        _ty = _ty + _point.z
    end

    local _npoints = #_points

    local _point = { x = _tx / _npoints, z = _ty / _npoints }

    _point.y = land.getHeight({ _point.x, _point.z })

    return _point
end

function ctld.getAATemplate(_unitName)

    for _,_system in pairs(ctld.AASystemTemplate) do

        if _system.repair == _unitName then
            return _system
        end

        for _,_part in pairs(_system.parts) do

            if _unitName == _part.name  then
                return _system
            end
        end
    end

    return nil

end

function ctld.getLauncherUnitFromAATemplate(_aaTemplate)
    for _,_part in pairs(_aaTemplate.parts) do

        if _part.launcher then
            return _part.name
        end
    end

    return nil
end

function ctld.rearmAASystem(_heli, _nearestCrate, _nearbyCrates, _aaSystemTemplate)

    -- are we adding to existing aa system?
    -- check to see if the crate is a launcher
    if ctld.getLauncherUnitFromAATemplate(_aaSystemTemplate) == _nearestCrate.details.unit then

        -- find nearest COMPLETE AA system
        local _nearestSystem = ctld.findNearestAASystem(_heli, _aaSystemTemplate)

        if _nearestSystem ~= nil and _nearestSystem.dist < 300 then

            local _uniqueTypes = {} -- stores each unique part of system
            local _types = {}
            local _points = {}

            local _units = _nearestSystem.group:getUnits()

            if _units ~= nil and #_units > 0 then

                for x = 1, #_units do
                    if _units[x]:getLife() > 0 then

                        --this allows us to count each type once
                        _uniqueTypes[_units[x]:getTypeName()] = _units[x]:getTypeName()

                        table.insert(_points, _units[x]:getPoint())
                        table.insert(_types, _units[x]:getTypeName())
                    end
                end
            end

            -- do we have the correct number of unique pieces and do we have enough points for all the pieces
            if ctld.countTableEntries(_uniqueTypes) == _aaSystemTemplate.count and #_points >= _aaSystemTemplate.count then

                -- rearm aa system
                -- destroy old group
                ctld.completeAASystems[_nearestSystem.group:getName()] = nil

                _nearestSystem.group:destroy()

                local _spawnedGroup = ctld.spawnCrateGroup(_heli, _points, _types)

                ctld.completeAASystems[_spawnedGroup:getName()] = ctld.getAASystemDetails(_spawnedGroup, _aaSystemTemplate)

                ctld.processCallback({unit = _heli, crate =  _nearestCrate , spawnedGroup = _spawnedGroup, action = "rearm"})

                trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " successfully rearmed a full ".._aaSystemTemplate.name.." in the field", 10)

                if _heli:getCoalition() == 1 then
                    ctld.spawnedCratesRED[_nearestCrate.crateUnit:getName()] = nil
                else
                    ctld.spawnedCratesBLUE[_nearestCrate.crateUnit:getName()] = nil
                end

                -- remove crate
           --     if ctld.slingLoad == false then
                    _nearestCrate.crateUnit:destroy()
              --  end

                return true -- all done so quit
            end
        end
    end

    return false
end

function ctld.getAASystemDetails(_hawkGroup,_aaSystemTemplate)

    local _units = _hawkGroup:getUnits()

    local _hawkDetails = {}

    for _, _unit in pairs(_units) do
        table.insert(_hawkDetails, { point = _unit:getPoint(), unit = _unit:getTypeName(), name = _unit:getName(), system =_aaSystemTemplate})
    end

    return _hawkDetails
end

function ctld.countTableEntries(_table)

    if _table == nil then
        return 0
    end


    local _count = 0

    for _key, _value in pairs(_table) do

        _count = _count + 1
    end

    return _count
end

function ctld.unpackAASystem(_heli, _nearestCrate, _nearbyCrates,_aaSystemTemplate)

    if ctld.rearmAASystem(_heli, _nearestCrate, _nearbyCrates,_aaSystemTemplate) then
        -- rearmed hawk
        return
    end

    -- are there all the pieces close enough together
    local _systemParts = {}

    --initialise list of parts
    for _,_part in pairs(_aaSystemTemplate.parts) do
        _systemParts[_part.name] = {name = _part.name,desc = _part.desc,found = false}
    end

    -- find all nearest crates and add them to the list if they're part of the AA System
    for _, _nearbyCrate in pairs(_nearbyCrates) do

        if _nearbyCrate.dist < 500 then

            if _systemParts[_nearbyCrate.details.unit] ~= nil and _systemParts[_nearbyCrate.details.unit].found == false  then
                local _foundPart = _systemParts[_nearbyCrate.details.unit]

                _foundPart.found = true
                _foundPart.crate = _nearbyCrate

                _systemParts[_nearbyCrate.details.unit] = _foundPart
            end
        end
    end

    local _count = 0
    local _txt = ""

    local _posArray = {}
    local _typeArray = {}
    for _name, _systemPart in pairs(_systemParts) do

        if _systemPart.found == false then
            _txt = _txt.."Missing ".._systemPart.desc.."\n"
        else

            local _launcherPart = ctld.getLauncherUnitFromAATemplate(_aaSystemTemplate)

            --handle multiple launchers from one crate
            if (_name == "Hawk ln" and ctld.hawkLaunchers > 1)
                    or (_launcherPart == _name and ctld.aaLaunchers  > 1) then

                --add multiple launcher
                local _launchers = ctld.aaLaunchers

                if _name == "Hawk ln" then
                    _launchers = ctld.hawkLaunchers
                end

                for _i = 1, _launchers do

                    -- spawn in a circle around the crate
                    local _angle = math.pi * 2 * (_i - 1) / _launchers
                    local _xOffset = math.cos(_angle) * 12
                    local _yOffset = math.sin(_angle) * 12

                    local _point = _systemPart.crate.crateUnit:getPoint()

                    _point = { x = _point.x + _xOffset, y = _point.y, z = _point.z + _yOffset }

                    table.insert(_posArray, _point)
                    table.insert(_typeArray, _name)
                end
            else
                table.insert(_posArray, _systemPart.crate.crateUnit:getPoint())
                table.insert(_typeArray, _name)
            end
        end
    end

    local _activeLaunchers = ctld.countCompleteAASystems(_heli)

    local _allowed = ctld.getAllowedAASystems(_heli)

    env.info("Active: ".._activeLaunchers.." Allowed: ".._allowed)

    if _activeLaunchers + 1 > _allowed then
        trigger.action.outTextForCoalition(_heli:getCoalition(), "Out of parts for AA Systems. Current limit is ".._allowed.." \n", 10)
        return
    end

    if _txt ~= ""  then
        ctld.displayMessageToGroup(_heli, "Cannot build ".._aaSystemTemplate.name.."\n" .. _txt .. "\n\nOr the crates are not close enough together", 20)
        return
    else

        -- destroy crates
        for _name, _systemPart in pairs(_systemParts) do

            if _heli:getCoalition() == 1 then
                ctld.spawnedCratesRED[_systemPart.crate.crateUnit:getName()] = nil
            else
                ctld.spawnedCratesBLUE[_systemPart.crate.crateUnit:getName()] = nil
            end

            --destroy
           -- if ctld.slingLoad == false then
                _systemPart.crate.crateUnit:destroy()
            --end
        end

        -- HAWK / BUK READY!
        local _spawnedGroup = ctld.spawnCrateGroup(_heli, _posArray, _typeArray)

        ctld.completeAASystems[_spawnedGroup:getName()] = ctld.getAASystemDetails(_spawnedGroup,_aaSystemTemplate)

        ctld.processCallback({unit = _heli, crate = _nearestCrate , spawnedGroup = _spawnedGroup, action = "unpack"})

        trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " successfully deployed a full ".._aaSystemTemplate.name.." to the field. \n\nAA Active System limit is: ".._allowed.."\nActive: "..(_activeLaunchers+1), 10)

    end
end

--count the number of captured cities, sets the amount of allowed AA Systems
function ctld.getAllowedAASystems(_heli)

    if _heli:getCoalition() == 1 then
        return ctld.AASystemLimitBLUE
    else
        return ctld.AASystemLimitRED
    end


end


function ctld.countCompleteAASystems(_heli)

    local _count = 0

    for _groupName, _hawkDetails in pairs(ctld.completeAASystems) do

        local _hawkGroup = Group.getByName(_groupName)

        --  env.info(_groupName..": "..mist.utils.tableShow(_hawkDetails))
        if _hawkGroup ~= nil and _hawkGroup:getCoalition() == _heli:getCoalition() then

            local _units = _hawkGroup:getUnits()

            if _units ~=nil and #_units > 0 then
                --get the system template
                local _aaSystemTemplate = _hawkDetails[1].system

                local _uniqueTypes = {} -- stores each unique part of system
                local _types = {}
                local _points = {}

                if _units ~= nil and #_units > 0 then

                    for x = 1, #_units do
                        if _units[x]:getLife() > 0 then

                            --this allows us to count each type once
                            _uniqueTypes[_units[x]:getTypeName()] = _units[x]:getTypeName()

                            table.insert(_points, _units[x]:getPoint())
                            table.insert(_types, _units[x]:getTypeName())
                        end
                    end
                end

                -- do we have the correct number of unique pieces and do we have enough points for all the pieces
                if ctld.countTableEntries(_uniqueTypes) == _aaSystemTemplate.count and #_points >= _aaSystemTemplate.count then
                    _count = _count +1
                end
            end
        end
    end

    return _count
end


function ctld.repairAASystem(_heli, _nearestCrate,_aaSystem)

    -- find nearest COMPLETE AA system
    local _nearestHawk = ctld.findNearestAASystem(_heli,_aaSystem)



    if _nearestHawk ~= nil and _nearestHawk.dist < 300 then

        local _oldHawk = ctld.completeAASystems[_nearestHawk.group:getName()]

        --spawn new one

        local _types = {}
        local _points = {}

        for _, _part in pairs(_oldHawk) do
            table.insert(_points, _part.point)
            table.insert(_types, _part.unit)
        end

        --remove old system
        ctld.completeAASystems[_nearestHawk.group:getName()] = nil
        _nearestHawk.group:destroy()

        local _spawnedGroup = ctld.spawnCrateGroup(_heli, _points, _types)

        ctld.completeAASystems[_spawnedGroup:getName()] = ctld.getAASystemDetails(_spawnedGroup,_aaSystem)

        ctld.processCallback({unit = _heli, crate = _nearestCrate , spawnedGroup = _spawnedGroup, action = "repair"})

        trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " successfully repaired a full ".._aaSystem.name.." in the field", 10)

        if _heli:getCoalition() == 1 then
            ctld.spawnedCratesRED[_nearestCrate.crateUnit:getName()] = nil
        else
            ctld.spawnedCratesBLUE[_nearestCrate.crateUnit:getName()] = nil
        end

        -- remove crate
       -- if ctld.slingLoad == false then
            _nearestCrate.crateUnit:destroy()
       -- end

    else
        ctld.displayMessageToGroup(_heli, "Cannot repair  ".._aaSystem.name..". No damaged ".._aaSystem.name.." within 300m", 10)
    end
end

function ctld.unpackMultiCrate(_heli, _nearestCrate, _nearbyCrates)

    -- unpack multi crate
    local _nearbyMultiCrates = {}

    for _, _nearbyCrate in pairs(_nearbyCrates) do

        if _nearbyCrate.dist < 300 then

            if _nearbyCrate.details.unit == _nearestCrate.details.unit then

                table.insert(_nearbyMultiCrates, _nearbyCrate)

                if #_nearbyMultiCrates == _nearestCrate.details.cratesRequired then
                    break
                end
            end
        end
    end

    --- check crate count
    if #_nearbyMultiCrates == _nearestCrate.details.cratesRequired then

        local _point = _nearestCrate.crateUnit:getPoint()

        -- destroy crates
        for _, _crate in pairs(_nearbyMultiCrates) do

            if _point == nil then
                _point = _crate.crateUnit:getPoint()
            end

            if _heli:getCoalition() == 1 then
                ctld.spawnedCratesRED[_crate.crateUnit:getName()] = nil
            else
                ctld.spawnedCratesBLUE[_crate.crateUnit:getName()] = nil
            end

            --destroy
         --   if ctld.slingLoad == false then
                _crate.crateUnit:destroy()
         --   end
        end


        local _spawnedGroup = ctld.spawnCrateGroup(_heli, { _point }, { _nearestCrate.details.unit })

        ctld.processCallback({unit = _heli, crate =  _nearestCrate , spawnedGroup = _spawnedGroup, action = "unpack"})

        local _txt = string.format("%s successfully deployed %s to the field using %d crates", ctld.getPlayerNameOrType(_heli), _nearestCrate.details.desc, #_nearbyMultiCrates)

        trigger.action.outTextForCoalition(_heli:getCoalition(), _txt, 10)

    else

        local _txt = string.format("Cannot build %s!\n\nIt requires %d crates and there are %d \n\nOr the crates are not within 300m of each other", _nearestCrate.details.desc, _nearestCrate.details.cratesRequired, #_nearbyMultiCrates)

        ctld.displayMessageToGroup(_heli, _txt, 20)
    end
end


function ctld.spawnCrateGroup(_heli, _positions, _types)

    local _id = ctld.getNextGroupId()

    local _groupName = _types[1] .. "  #" .. _id

    local _side = _heli:getCoalition()

    local _group = {
        ["visible"] = false,
       -- ["groupId"] = _id,
        ["hidden"] = false,
        ["units"] = {},
        --        ["y"] = _positions[1].z,
        --        ["x"] = _positions[1].x,
        ["name"] = _groupName,
        ["task"] = {},
    }

    if #_positions == 1 then

        local _unitId = ctld.getNextUnitId()
        local _details = { type = _types[1], unitId = _unitId, name = string.format("Unpacked %s #%i", _types[1], _unitId) }

        _group.units[1] = ctld.createUnit(_positions[1].x + 5, _positions[1].z + 5, 120, _details)

    else

        for _i, _pos in ipairs(_positions) do

            local _unitId = ctld.getNextUnitId()
            local _details = { type = _types[_i], unitId = _unitId, name = string.format("Unpacked %s #%i", _types[_i], _unitId) }

            _group.units[_i] = ctld.createUnit(_pos.x + 5, _pos.z + 5, 120, _details)
        end
    end

    --mist function
    _group.category = Group.Category.GROUND
    _group.country = _heli:getCountry()

    local _spawnedGroup = Group.getByName(mist.dynAdd(_group).name)

    return _spawnedGroup
end



-- spawn normal group
function ctld.spawnDroppedGroup(_point, _details, _spawnBehind, _maxSearch)

    local _groupName = _details.groupName

    local _group = {
        ["visible"] = false,
      --  ["groupId"] = _details.groupId,
        ["hidden"] = false,
        ["units"] = {},
        --        ["y"] = _positions[1].z,
        --        ["x"] = _positions[1].x,
        ["name"] = _groupName,
        ["task"] = {},
    }


    if _spawnBehind == false then

        -- spawn in circle around heli

        local _pos = _point

        for _i, _detail in ipairs(_details.units) do

            local _angle = math.pi * 2 * (_i - 1) / #_details.units
            local _xOffset = math.cos(_angle) * 30
            local _yOffset = math.sin(_angle) * 30

            _group.units[_i] = ctld.createUnit(_pos.x + _xOffset, _pos.z + _yOffset, _angle, _detail)
        end

    else

        local _pos = _point

        --try to spawn at 6 oclock to us
        local _angle = math.atan2(_pos.z, _pos.x)
        local _xOffset = math.cos(_angle) * -30
        local _yOffset = math.sin(_angle) * -30


        for _i, _detail in ipairs(_details.units) do
            _group.units[_i] = ctld.createUnit(_pos.x + (_xOffset + 10 * _i), _pos.z + (_yOffset + 10 * _i), _angle, _detail)
        end
    end

    --switch to MIST
    _group.category = Group.Category.GROUND;
    _group.country = _details.country;

    local _spawnedGroup = Group.getByName(mist.dynAdd(_group).name)

    --local _spawnedGroup = coalition.addGroup(_details.country, Group.Category.GROUND, _group)


    -- find nearest enemy and head there
    if _maxSearch == nil then
        _maxSearch = ctld.maximumSearchDistance
    end

    local _wpZone = ctld.inWaypointZone(_point,_spawnedGroup:getCoalition())

    if _wpZone.inZone then
        ctld.orderGroupToMoveToPoint(_spawnedGroup:getUnit(1), _wpZone.point)
        env.info("Heading to waypoint - In Zone ".._wpZone.name)
    else
        local _enemyPos = ctld.findNearestEnemy(_details.side, _point, _maxSearch)

        ctld.orderGroupToMoveToPoint(_spawnedGroup:getUnit(1), _enemyPos)
    end

    return _spawnedGroup
end

function ctld.findNearestEnemy(_side, _point, _searchDistance)

    local _closestEnemy = nil

    local _groups

    local _closestEnemyDist = _searchDistance

    local _heliPoint = _point

    if _side == 2 then
        _groups = coalition.getGroups(1, Group.Category.GROUND)
    else
        _groups = coalition.getGroups(2, Group.Category.GROUND)
    end

    for _, _group in pairs(_groups) do

        if _group ~= nil then
            local _units = _group:getUnits()

            if _units ~= nil and #_units > 0 then

                local _leader = nil

                -- find alive leader
                for x = 1, #_units do
                    if _units[x]:getLife() > 0 then
                        _leader = _units[x]
                        break
                    end
                end

                if _leader ~= nil then
                    local _leaderPos = _leader:getPoint()
                    local _dist = ctld.getDistance(_heliPoint, _leaderPos)
                    if _dist < _closestEnemyDist then
                        _closestEnemyDist = _dist
                        _closestEnemy = _leaderPos
                    end
                end
            end
        end
    end


    -- no enemy - move to random point
    if _closestEnemy ~= nil then

        -- env.info("found enemy")
        return _closestEnemy
    else

        local _x = _heliPoint.x + math.random(0, ctld.maximumMoveDistance) - math.random(0, ctld.maximumMoveDistance)
        local _z = _heliPoint.z + math.random(0, ctld.maximumMoveDistance) - math.random(0, ctld.maximumMoveDistance)
        local _y = _heliPoint.y + math.random(0, ctld.maximumMoveDistance) - math.random(0, ctld.maximumMoveDistance)

        return { x = _x, z = _z,y=_y }
    end
end

function ctld.findNearestGroup(_heli, _groups)

    local _closestGroupDetails = {}
    local _closestGroup = nil

    local _closestGroupDist = ctld.maxExtractDistance

    local _heliPoint = _heli:getPoint()

    for _, _groupName in pairs(_groups) do

        local _group = Group.getByName(_groupName)

        if _group ~= nil then
            local _units = _group:getUnits()

            if _units ~= nil and #_units > 0 then

                local _leader = nil

                local _groupDetails = { groupId = _group:getID(), groupName = _group:getName(), side = _group:getCoalition(), units = {} }

                -- find alive leader
                for x = 1, #_units do
                    if _units[x]:getLife() > 0 then

                        if _leader == nil then
                            _leader = _units[x]
                            -- set country based on leader
                            _groupDetails.country = _leader:getCountry()
                        end

                        local _unitDetails = { type = _units[x]:getTypeName(), unitId = _units[x]:getID(), name = _units[x]:getName() }

                        table.insert(_groupDetails.units, _unitDetails)
                    end
                end

                if _leader ~= nil then
                    local _leaderPos = _leader:getPoint()
                    local _dist = ctld.getDistance(_heliPoint, _leaderPos)
                    if _dist < _closestGroupDist then
                        _closestGroupDist = _dist
                        _closestGroupDetails = _groupDetails
                        _closestGroup = _group
                    end
                end
            end
        end
    end


    if _closestGroup ~= nil then

        return { group = _closestGroup, details = _closestGroupDetails }
    else

        return nil
    end
end


function ctld.createUnit(_x, _y, _angle, _details)

    local _newUnit = {
        ["y"] = _y,
        ["type"] = _details.type,
        ["name"] = _details.name,
      --  ["unitId"] = _details.unitId,
        ["heading"] = _angle,
        ["playerCanDrive"] = true,
        ["skill"] = "Excellent",
        ["x"] = _x,
    }

    return _newUnit
end

function ctld.addEWRTask(_group)

    -- delayed 2 second to work around bug
    timer.scheduleFunction(function(_ewrGroup)
        local _grp = ctld.getAliveGroup(_ewrGroup)

        if _grp ~= nil then
            local _controller = _grp:getController();
            local _EWR = {
                id = 'EWR',
                auto = true,
                params = {
                }
            }
            _controller:setTask(_EWR)
        end
    end
        , _group:getName(), timer.getTime() + 2)

end

function ctld.orderGroupToMoveToPoint(_leader, _destination)

    local _group = _leader:getGroup()

    local _path = {}
    table.insert(_path, mist.ground.buildWP(_leader:getPoint(), 'Off Road', 50))
    table.insert(_path, mist.ground.buildWP(_destination, 'Off Road', 50))

    local _mission = {
        id = 'Mission',
        params = {
            route = {
                points =_path
            },
        },
    }


    -- delayed 2 second to work around bug
    timer.scheduleFunction(function(_arg)
        local _grp = ctld.getAliveGroup(_arg[1])

        if _grp ~= nil then
            local _controller = _grp:getController();
            Controller.setOption(_controller, AI.Option.Ground.id.ALARM_STATE, AI.Option.Ground.val.ALARM_STATE.AUTO)
            Controller.setOption(_controller, AI.Option.Ground.id.ROE, AI.Option.Ground.val.ROE.OPEN_FIRE)
            _controller:setTask(_arg[2])
        end
    end
        , {_group:getName(), _mission}, timer.getTime() + 2)

end

-- are we in pickup zone
function ctld.inPickupZone(_heli)
    ctld.logDebug(string.format("ctld.inPickupZone(_heli=%s)", ctld.p(_heli)))

    if ctld.inAir(_heli) then
        return { inZone = false, limit = -1, index = -1 }
    end

    local _heliPoint = _heli:getPoint()

    for _i, _zoneDetails in pairs(ctld.pickupZones) do
        ctld.logTrace(string.format("_zoneDetails=%s", ctld.p(_zoneDetails)))

        local _triggerZone = trigger.misc.getZone(_zoneDetails[1])

        if _triggerZone == nil then
            local _ship = ctld.getTransportUnit(_zoneDetails[1])

            if _ship then
                local _point = _ship:getPoint()
                _triggerZone = {}
                _triggerZone.point = _point
                _triggerZone.radius = 200 -- should be big enough for ship
            end

        end

        if _triggerZone ~= nil then

            --get distance to center

            local _dist = ctld.getDistance(_heliPoint, _triggerZone.point)
            ctld.logTrace(string.format("_dist=%s", ctld.p(_dist)))
            if _dist <= _triggerZone.radius then
                local _heliCoalition = _heli:getCoalition()
                if _zoneDetails[4] == 1 and (_zoneDetails[5] == _heliCoalition or _zoneDetails[5] == 0) then
                    return { inZone = true, limit = _zoneDetails[3], index = _i }
                end
            end
        end
    end

    local _fobs = ctld.getSpawnedFobs(_heli)

    -- now check spawned fobs
    for _, _fob in ipairs(_fobs) do

        --get distance to center

        local _dist = ctld.getDistance(_heliPoint, _fob:getPoint())

        if _dist <= 150 then
            return { inZone = true, limit = 10000, index = -1 };
        end
    end



    return { inZone = false, limit = -1, index = -1 };
end

function ctld.getSpawnedFobs(_heli)

    local _fobs = {}

    for _, _fobName in ipairs(ctld.builtFOBS) do

        local _fob = StaticObject.getByName(_fobName)

        if _fob ~= nil and _fob:isExist() and _fob:getCoalition() == _heli:getCoalition() and _fob:getLife() > 0 then

            table.insert(_fobs, _fob)
        end
    end

    return _fobs
end

-- are we in a dropoff zone
function ctld.inDropoffZone(_heli)

    if ctld.inAir(_heli) then
        return false
    end

    local _heliPoint = _heli:getPoint()

    for _, _zoneDetails in pairs(ctld.dropOffZones) do

        local _triggerZone = trigger.misc.getZone(_zoneDetails[1])

        if _triggerZone ~= nil and (_zoneDetails[3] == _heli:getCoalition() or _zoneDetails[3]== 0) then

            --get distance to center

            local _dist = ctld.getDistance(_heliPoint, _triggerZone.point)

            if _dist <= _triggerZone.radius then
                return true
            end
        end
    end

    return false
end

-- are we in a waypoint zone
function ctld.inWaypointZone(_point,_coalition)

    for _, _zoneDetails in pairs(ctld.wpZones) do

        local _triggerZone = trigger.misc.getZone(_zoneDetails[1])

        --right coalition and active?
        if _triggerZone ~= nil and (_zoneDetails[4] == _coalition or _zoneDetails[4]== 0) and _zoneDetails[3] == 1 then

            --get distance to center

            local _dist = ctld.getDistance(_point, _triggerZone.point)

            if _dist <= _triggerZone.radius then
                return {inZone = true, point = _triggerZone.point, name = _zoneDetails[1]}
            end
        end
    end

    return {inZone = false}
end

-- are we near friendly logistics zone
function ctld.inLogisticsZone(_heli)

    if ctld.inAir(_heli) then
        return false
    end

    local _heliPoint = _heli:getPoint()

    for _, _name in pairs(ctld.logisticUnits) do

        local _logistic = StaticObject.getByName(_name)

        if _logistic ~= nil and _logistic:getCoalition() == _heli:getCoalition() then

            --get distance
            local _dist = ctld.getDistance(_heliPoint, _logistic:getPoint())

            if _dist <= ctld.maximumDistanceLogistic then
                return true
            end
        end
    end

    return false
end


-- are far enough from a friendly logistics zone
function ctld.farEnoughFromLogisticZone(_heli)

    if ctld.inAir(_heli) then
        return false
    end

    local _heliPoint = _heli:getPoint()

    local _farEnough = true

    for _, _name in pairs(ctld.logisticUnits) do

        local _logistic = StaticObject.getByName(_name)

        if _logistic ~= nil and _logistic:getCoalition() == _heli:getCoalition() then

            --get distance
            local _dist = ctld.getDistance(_heliPoint, _logistic:getPoint())
            -- env.info("DIST ".._dist)
            if _dist <= ctld.minimumDeployDistance then
                -- env.info("TOO CLOSE ".._dist)
                _farEnough = false
            end
        end
    end

    return _farEnough
end

function ctld.refreshSmoke()

    if ctld.disableAllSmoke == true then
        return
    end

    for _, _zoneGroup in pairs({ ctld.pickupZones, ctld.dropOffZones }) do

        for _, _zoneDetails in pairs(_zoneGroup) do

            local _triggerZone = trigger.misc.getZone(_zoneDetails[1])

            if _triggerZone == nil then
                local _ship = ctld.getTransportUnit(_triggerZone)

                if _ship then
                    local _point = _ship:getPoint()
                    _triggerZone = {}
                    _triggerZone.point = _point
                end

            end


            --only trigger if smoke is on AND zone is active
            if _triggerZone ~= nil and _zoneDetails[2] >= 0 and _zoneDetails[4] == 1 then

                -- Trigger smoke markers

                local _pos2 = { x = _triggerZone.point.x, y = _triggerZone.point.z }
                local _alt = land.getHeight(_pos2)
                local _pos3 = { x = _pos2.x, y = _alt, z = _pos2.y }

                trigger.action.smoke(_pos3, _zoneDetails[2])
            end
        end
    end

    --waypoint zones
    for _, _zoneDetails in pairs(ctld.wpZones) do

        local _triggerZone = trigger.misc.getZone(_zoneDetails[1])

        --only trigger if smoke is on AND zone is active
        if _triggerZone ~= nil and _zoneDetails[2] >= 0 and _zoneDetails[3] == 1 then

            -- Trigger smoke markers

            local _pos2 = { x = _triggerZone.point.x, y = _triggerZone.point.z }
            local _alt = land.getHeight(_pos2)
            local _pos3 = { x = _pos2.x, y = _alt, z = _pos2.y }

            trigger.action.smoke(_pos3, _zoneDetails[2])
        end
    end


    --refresh in 5 minutes
    timer.scheduleFunction(ctld.refreshSmoke, nil, timer.getTime() + 300)
end

function ctld.dropSmoke(_args)

    local _heli = ctld.getTransportUnit(_args[1])

    if _heli ~= nil then

        local _colour = ""

        if _args[2] == trigger.smokeColor.Red then

            _colour = "RED"
        elseif _args[2] == trigger.smokeColor.Blue then

            _colour = "BLUE"
        elseif _args[2] == trigger.smokeColor.Green then

            _colour = "GREEN"
        elseif _args[2] == trigger.smokeColor.Orange then

            _colour = "ORANGE"
        end

        local _point = _heli:getPoint()

        local _pos2 = { x = _point.x, y = _point.z }
        local _alt = land.getHeight(_pos2)
        local _pos3 = { x = _point.x, y = _alt, z = _point.z }

        trigger.action.smoke(_pos3, _args[2])

        trigger.action.outTextForCoalition(_heli:getCoalition(), ctld.getPlayerNameOrType(_heli) .. " dropped " .. _colour .. " smoke ", 10)
    end
end

function ctld.unitCanCarryVehicles(_unit)

    local _type = string.lower(_unit:getTypeName())

    for _, _name in ipairs(ctld.vehicleTransportEnabled) do
        local _nameLower = string.lower(_name)
        if string.match(_type, _nameLower) then
            return true
        end
    end

    return false
end

function ctld.isJTACUnitType(_type)

    _type = string.lower(_type)

    for _, _name in ipairs(ctld.jtacUnitTypes) do
        local _nameLower = string.lower(_name)
        if string.match(_type, _nameLower) then
            return true
        end
    end

    return false
end

function ctld.updateZoneCounter(_index, _diff)

    if ctld.pickupZones[_index] ~= nil then

        ctld.pickupZones[_index][3] = ctld.pickupZones[_index][3] + _diff

        if ctld.pickupZones[_index][3] < 0 then
            ctld.pickupZones[_index][3] = 0
        end

        if ctld.pickupZones[_index][6] ~= nil then
            trigger.action.setUserFlag(ctld.pickupZones[_index][6], ctld.pickupZones[_index][3])
        end
        --  env.info(ctld.pickupZones[_index][1].." = " ..ctld.pickupZones[_index][3])
    end
end

function ctld.processCallback(_callbackArgs)

    for _, _callback in pairs(ctld.callbacks) do

        local _status, _result = pcall(function()

            _callback(_callbackArgs)

        end)

        if (not _status) then
            env.error(string.format("CTLD Callback Error: %s", _result))
        end
    end
end


-- checks the status of all AI troop carriers and auto loads and unloads troops
-- as long as the troops are on the ground
function ctld.checkAIStatus()

    timer.scheduleFunction(ctld.checkAIStatus, nil, timer.getTime() + 2)


    for _, _unitName in pairs(ctld.transportPilotNames) do
        local status, error = pcall(function()

            local _unit = ctld.getTransportUnit(_unitName)

            -- no player name means AI!
            if _unit ~= nil and _unit:getPlayerName() == nil then
                local _zone = ctld.inPickupZone(_unit)
                --  env.error("Checking.. ".._unit:getName())
                if _zone.inZone == true and not ctld.troopsOnboard(_unit, true) then
                    --   env.error("in zone, loading.. ".._unit:getName())

                    if ctld.allowRandomAiTeamPickups == true then
                        -- Random troop pickup implementation
                        local _team = nil
                        if _unit:getCoalition() == 1 then
                            _team = math.floor((math.random(#ctld.redTeams * 100) / 100) + 1)
                            ctld.loadTroopsFromZone({ _unitName, true,ctld.loadableGroups[ctld.redTeams[_team]],true })
                        else
                            _team = math.floor((math.random(#ctld.blueTeams * 100) / 100) + 1)
                            ctld.loadTroopsFromZone({ _unitName, true,ctld.loadableGroups[ctld.blueTeams[_team]],true })
                        end
                    else
                        ctld.loadTroopsFromZone({ _unitName, true,"",true })
                    end

                elseif ctld.inDropoffZone(_unit) and ctld.troopsOnboard(_unit, true) then
                    --     env.error("in dropoff zone, unloading.. ".._unit:getName())
                    ctld.unloadTroops( { _unitName, true })
                end

                if ctld.unitCanCarryVehicles(_unit) then

                    if _zone.inZone == true and not ctld.troopsOnboard(_unit, false) then

                        ctld.loadTroopsFromZone({ _unitName, false,"",true })

                    elseif ctld.inDropoffZone(_unit) and ctld.troopsOnboard(_unit, false) then

                        ctld.unloadTroops( { _unitName, false })
                    end
                end
            end
        end)

        if (not status) then
            env.error(string.format("Error with ai status: %s", error), false)
        end
    end


end

function ctld.getTransportLimit(_unitType)

    if ctld.unitLoadLimits[_unitType] then

        return ctld.unitLoadLimits[_unitType]
    end

    return ctld.numberOfTroops

end

function ctld.getUnitActions(_unitType)

    if ctld.unitActions[_unitType] then
        return ctld.unitActions[_unitType]
    end

    return {crates=true,troops=true}

end

-- Adds menuitem to all heli units that are active
function ctld.addF10MenuOptions()
    -- Loop through all Heli units

    timer.scheduleFunction(ctld.addF10MenuOptions, nil, timer.getTime() + 10)

    for _, _unitName in pairs(ctld.transportPilotNames) do

        local status, error = pcall(function()

            local _unit = ctld.getTransportUnit(_unitName)

            if _unit ~= nil then

                local _groupId = ctld.getGroupId(_unit)

                if _groupId then

                    if ctld.addedTo[tostring(_groupId)] == nil then

                        local _rootPath = missionCommands.addSubMenuForGroup(_groupId, "CTLD")

                        local _unitActions = ctld.getUnitActions(_unit:getTypeName())
                        ctld.logTrace(string.format("_unitActions=%s", ctld.p(_unitActions)))

                        missionCommands.addCommandForGroup(_groupId, "Check Cargo", _rootPath, ctld.checkTroopStatus, { _unitName })

                        if _unitActions.troops then

                            local _troopCommandsPath = missionCommands.addSubMenuForGroup(_groupId, "Troop Transport", _rootPath)

                            missionCommands.addCommandForGroup(_groupId, "Unload / Extract Troops", _troopCommandsPath, ctld.unloadExtractTroops, { _unitName })


                            -- local _loadPath = missionCommands.addSubMenuForGroup(_groupId, "Load From Zone", _troopCommandsPath)
                            local _transportLimit = ctld.getTransportLimit(_unit:getTypeName())
                            ctld.logTrace(string.format("_transportLimit=%s", ctld.p(_transportLimit)))
                            for _,_loadGroup in pairs(ctld.loadableGroups) do
                                ctld.logTrace(string.format("_loadGroup=%s", ctld.p(_loadGroup)))
                                if not _loadGroup.side or _loadGroup.side == _unit:getCoalition() then

                                    -- check size & unit
                                    if _transportLimit >= _loadGroup.total then
                                        missionCommands.addCommandForGroup(_groupId, "Load ".._loadGroup.name, _troopCommandsPath, ctld.loadTroopsFromZone, { _unitName, true,_loadGroup,false })
                                    end
                                end
                            end

                            if ctld.unitCanCarryVehicles(_unit) then

                                local _vehicleCommandsPath = missionCommands.addSubMenuForGroup(_groupId, "Vehicle / FOB Transport", _rootPath)

                                missionCommands.addCommandForGroup(_groupId, "Unload Vehicles", _vehicleCommandsPath, ctld.unloadTroops, { _unitName, false })
                                missionCommands.addCommandForGroup(_groupId, "Load / Extract Vehicles", _vehicleCommandsPath, ctld.loadTroopsFromZone, { _unitName, false,"",true })

                                if ctld.enabledFOBBuilding and ctld.staticBugWorkaround == false then

                                    missionCommands.addCommandForGroup(_groupId, "Load / Unload FOB Crate", _vehicleCommandsPath, ctld.loadUnloadFOBCrate, { _unitName, false })
                                end
                                missionCommands.addCommandForGroup(_groupId, "Check Cargo", _vehicleCommandsPath, ctld.checkTroopStatus, { _unitName })
                            end

                        end


                        if ctld.enableCrates and _unitActions.crates then

                            if ctld.unitCanCarryVehicles(_unit) == false then

                                -- local _cratePath = missionCommands.addSubMenuForGroup(_groupId, "Spawn Crate", _rootPath)
                                -- add menu for spawning crates
                                for _subMenuName, _crates in pairs(ctld.spawnableCrates) do

                                    local _cratePath = missionCommands.addSubMenuForGroup(_groupId, _subMenuName, _rootPath)
                                    for _, _crate in pairs(_crates) do

                                        if ctld.isJTACUnitType(_crate.unit) == false
                                                or (ctld.isJTACUnitType(_crate.unit) == true and ctld.JTAC_dropEnabled) then
                                            if _crate.side == nil or (_crate.side == _unit:getCoalition()) then

                                                local _crateRadioMsg = _crate.desc

                                                --add in the number of crates required to build something
                                                if _crate.cratesRequired ~= nil and _crate.cratesRequired > 1 then
                                                    _crateRadioMsg = _crateRadioMsg.." (".._crate.cratesRequired..")"
                                                end

                                                missionCommands.addCommandForGroup(_groupId,_crateRadioMsg, _cratePath, ctld.spawnCrate, { _unitName, _crate.weight })
                                            end
                                        end
                                    end
                                end
                            end
                        end

                        if (ctld.enabledFOBBuilding or ctld.enableCrates) and _unitActions.crates then

                            local _crateCommands = missionCommands.addSubMenuForGroup(_groupId, "CTLD Commands", _rootPath)
                            if ctld.hoverPickup == false then
                                if  ctld.slingLoad == false then
                                    missionCommands.addCommandForGroup(_groupId, "Load Nearby Crate", _crateCommands, ctld.loadNearbyCrate,  _unitName )
                                end
                            end

                            missionCommands.addCommandForGroup(_groupId, "Unpack Any Crate", _crateCommands, ctld.unpackCrates, { _unitName })

                            if ctld.slingLoad == false then
                                missionCommands.addCommandForGroup(_groupId, "Drop Crate", _crateCommands, ctld.dropSlingCrate, { _unitName })
                            end

                            missionCommands.addCommandForGroup(_groupId, "List Nearby Crates", _crateCommands, ctld.listNearbyCrates, { _unitName })

                            if ctld.enabledFOBBuilding then
                                missionCommands.addCommandForGroup(_groupId, "List FOBs", _crateCommands, ctld.listFOBS, { _unitName })
                            end
                        end


                        if ctld.enableSmokeDrop then
                            local _smokeMenu = missionCommands.addSubMenuForGroup(_groupId, "Smoke Markers", _rootPath)
                            missionCommands.addCommandForGroup(_groupId, "Drop Red Smoke", _smokeMenu, ctld.dropSmoke, { _unitName, trigger.smokeColor.Red })
                            missionCommands.addCommandForGroup(_groupId, "Drop Blue Smoke", _smokeMenu, ctld.dropSmoke, { _unitName, trigger.smokeColor.Blue })
                            missionCommands.addCommandForGroup(_groupId, "Drop Orange Smoke", _smokeMenu, ctld.dropSmoke, { _unitName, trigger.smokeColor.Orange })
                            missionCommands.addCommandForGroup(_groupId, "Drop Green Smoke", _smokeMenu, ctld.dropSmoke, { _unitName, trigger.smokeColor.Green })
                        end

                        if ctld.enabledRadioBeaconDrop then
                            local _radioCommands = missionCommands.addSubMenuForGroup(_groupId, "Radio Beacons", _rootPath)
                            missionCommands.addCommandForGroup(_groupId, "List Beacons", _radioCommands, ctld.listRadioBeacons, { _unitName })
                            missionCommands.addCommandForGroup(_groupId, "Drop Beacon", _radioCommands, ctld.dropRadioBeacon, { _unitName })
                            missionCommands.addCommandForGroup(_groupId, "Remove Closet Beacon", _radioCommands, ctld.removeRadioBeacon, { _unitName })
                        elseif ctld.deployedRadioBeacons ~= {} then
                            local _radioCommands = missionCommands.addSubMenuForGroup(_groupId, "Radio Beacons", _rootPath)
                            missionCommands.addCommandForGroup(_groupId, "List Beacons", _radioCommands, ctld.listRadioBeacons, { _unitName })
                        end

                        ctld.addedTo[tostring(_groupId)] = true
                    end
                end
            else
                -- env.info(string.format("unit nil %s",_unitName))
            end
        end)

        if (not status) then
            env.error(string.format("Error adding f10 to transport: %s", error), false)
        end
    end

    local status, error = pcall(function()

        -- now do any player controlled aircraft that ARENT transport units
        if ctld.enabledRadioBeaconDrop then
            -- get all BLUE players
            ctld.addRadioListCommand(2)

            -- get all RED players
            ctld.addRadioListCommand(1)
        end


        if ctld.JTAC_jtacStatusF10 then
            -- get all BLUE players
            ctld.addJTACRadioCommand(2)

            -- get all RED players
            ctld.addJTACRadioCommand(1)
        end

    end)

    if (not status) then
        env.error(string.format("Error adding f10 to other players: %s", error), false)
    end


end

--add to all players that arent transport
function ctld.addRadioListCommand(_side)

    local _players = coalition.getPlayers(_side)

    if _players ~= nil then

        for _, _playerUnit in pairs(_players) do

            local _groupId = ctld.getGroupId(_playerUnit)

            if _groupId then

                if ctld.addedTo[tostring(_groupId)] == nil then
                    missionCommands.addCommandForGroup(_groupId, "List Radio Beacons", nil, ctld.listRadioBeacons, { _playerUnit:getName() })
                    ctld.addedTo[tostring(_groupId)] = true
                end
            end
        end
    end
end

function ctld.addJTACRadioCommand(_side)

    local _players = coalition.getPlayers(_side)

    if _players ~= nil then

        for _, _playerUnit in pairs(_players) do

            local _groupId = ctld.getGroupId(_playerUnit)

            if _groupId then
                --   env.info("adding command for "..index)
                if ctld.jtacRadioAdded[tostring(_groupId)] == nil then
                    -- env.info("about command for "..index)
                    missionCommands.addCommandForGroup(_groupId, "JTAC Status", nil, ctld.getJTACStatus, { _playerUnit:getName() })
                    ctld.jtacRadioAdded[tostring(_groupId)] = true
                    -- env.info("Added command for " .. index)
                end
            end


        end
    end
end

function ctld.getGroupId(_unit)

    local _unitDB =  mist.DBs.unitsById[tonumber(_unit:getID())]
    if _unitDB ~= nil and _unitDB.groupId then
        return _unitDB.groupId
    end

    return nil
end

--get distance in meters assuming a Flat world
function ctld.getDistance(_point1, _point2)

    local xUnit = _point1.x
    local yUnit = _point1.z
    local xZone = _point2.x
    local yZone = _point2.z

    local xDiff = xUnit - xZone
    local yDiff = yUnit - yZone

    return math.sqrt(xDiff * xDiff + yDiff * yDiff)
end


------------ JTAC -----------


ctld.jtacLaserPoints = {}
ctld.jtacIRPoints = {}
ctld.jtacSmokeMarks = {}
ctld.jtacUnits = {} -- list of JTAC units for f10 command
ctld.jtacStop = {} -- jtacs to tell to stop lasing
ctld.jtacCurrentTargets = {}
ctld.jtacRadioAdded = {} --keeps track of who's had the radio command added
ctld.jtacGeneratedLaserCodes = {} -- keeps track of generated codes, cycles when they run out
ctld.jtacLaserPointCodes = {}
ctld.jtacRadioData = {}

function ctld.JTACAutoLase(_jtacGroupName, _laserCode, _smoke, _lock, _colour, _radio)
    ctld.logDebug(string.format("ctld.JTACAutoLase(_jtacGroupName=%s, _laserCode=%s", ctld.p(_jtacGroupName), ctld.p(_laserCode)))

    local _radio = _radio
    if not _radio then
        _radio = {}
        if _laserCode then
            local _laserCode = tonumber(_laserCode)
            if _laserCode and _laserCode >= 1111 and _laserCode <= 1688 then
                local _laserB = math.floor((_laserCode - 1000)/100)
                local _laserCD = _laserCode - 1000 - _laserB*100
                local _frequency = tostring(30+_laserB+_laserCD*0.05)
                ctld.logTrace(string.format("_laserB=%s", ctld.p(_laserB)))
                ctld.logTrace(string.format("_laserCD=%s", ctld.p(_laserCD)))
                ctld.logTrace(string.format("_frequency=%s", ctld.p(_frequency)))
                _radio.freq = _frequency
                _radio.mod = "fm"
            end        
        end
    end

    if _radio and not _radio.name then
        _radio.name = _jtacGroupName
    end

    if ctld.jtacStop[_jtacGroupName] == true then
        ctld.jtacStop[_jtacGroupName] = nil -- allow it to be started again
        ctld.cleanupJTAC(_jtacGroupName)
        return
    end

    if _lock == nil then

        _lock = ctld.JTAC_lock
    end


    ctld.jtacLaserPointCodes[_jtacGroupName] = _laserCode
    ctld.jtacRadioData[_jtacGroupName] = _radio

    local _jtacGroup = ctld.getGroup(_jtacGroupName)
    local _jtacUnit

    if _jtacGroup == nil or #_jtacGroup == 0 then

        --check not in a heli
        if ctld.inTransitTroops then
            for _, _onboard in pairs(ctld.inTransitTroops) do
                if _onboard ~= nil then
                    if _onboard.troops ~= nil and _onboard.troops.groupName ~= nil and _onboard.troops.groupName == _jtacGroupName then

                        --jtac soldier being transported by heli
                        ctld.cleanupJTAC(_jtacGroupName)

                        env.info(_jtacGroupName .. ' in Transport - Waiting 10 seconds')
                        timer.scheduleFunction(ctld.timerJTACAutoLase, { _jtacGroupName, _laserCode, _smoke, _lock, _colour, _radio }, timer.getTime() + 10)
                        return
                    end

                    if _onboard.vehicles ~= nil and _onboard.vehicles.groupName ~= nil and _onboard.vehicles.groupName == _jtacGroupName then
                        --jtac vehicle being transported by heli
                        ctld.cleanupJTAC(_jtacGroupName)

                        env.info(_jtacGroupName .. ' in Transport - Waiting 10 seconds')
                        timer.scheduleFunction(ctld.timerJTACAutoLase, { _jtacGroupName, _laserCode, _smoke, _lock, _colour, _radio }, timer.getTime() + 10)
                        return
                    end
                end
            end
        end


        if ctld.jtacUnits[_jtacGroupName] ~= nil then
            ctld.notifyCoalition("JTAC Group " .. _jtacGroupName .. " KIA!", 10, ctld.jtacUnits[_jtacGroupName].side, _radio)
        end

        --remove from list
        ctld.jtacUnits[_jtacGroupName] = nil

        ctld.cleanupJTAC(_jtacGroupName)

        return
    else

        _jtacUnit = _jtacGroup[1]
        --add to list
        ctld.jtacUnits[_jtacGroupName] = { name = _jtacUnit:getName(), side = _jtacUnit:getCoalition(), radio = _radio }

        -- work out smoke colour
        if _colour == nil then

            if _jtacUnit:getCoalition() == 1 then
                _colour = ctld.JTAC_smokeColour_RED
            else
                _colour = ctld.JTAC_smokeColour_BLUE
            end
        end


        if _smoke == nil then

            if _jtacUnit:getCoalition() == 1 then
                _smoke = ctld.JTAC_smokeOn_RED
            else
                _smoke = ctld.JTAC_smokeOn_BLUE
            end
        end
    end


    -- search for current unit

    if _jtacUnit:isActive() == false then

        ctld.cleanupJTAC(_jtacGroupName)

        env.info(_jtacGroupName .. ' Not Active - Waiting 30 seconds')
        timer.scheduleFunction(ctld.timerJTACAutoLase, { _jtacGroupName, _laserCode, _smoke, _lock, _colour, _radio }, timer.getTime() + 30)

        return
    end

    local _enemyUnit = ctld.getCurrentUnit(_jtacUnit, _jtacGroupName)
    local targetDestroyed = false
    local targetLost = false

    if _enemyUnit == nil and ctld.jtacCurrentTargets[_jtacGroupName] ~= nil then

        local _tempUnitInfo = ctld.jtacCurrentTargets[_jtacGroupName]

        --      env.info("TEMP UNIT INFO: " .. tempUnitInfo.name .. " " .. tempUnitInfo.unitType)

        local _tempUnit = Unit.getByName(_tempUnitInfo.name)

        if _tempUnit ~= nil and _tempUnit:getLife() > 0 and _tempUnit:isActive() == true then
            targetLost = true
        else
            targetDestroyed = true
        end

        --remove from smoke list
        ctld.jtacSmokeMarks[_tempUnitInfo.name] = nil

    	-- JTAC Unit: resume his route ------------
	    trigger.action.groupContinueMoving(Group.getByName(_jtacGroupName)) 	

        -- remove from target list
        ctld.jtacCurrentTargets[_jtacGroupName] = nil

        --stop lasing
        ctld.cancelLase(_jtacGroupName)
    end


    if _enemyUnit == nil then
        _enemyUnit = ctld.findNearestVisibleEnemy(_jtacUnit, _lock)

        if _enemyUnit ~= nil then

            -- store current target for easy lookup
            ctld.jtacCurrentTargets[_jtacGroupName] = { name = _enemyUnit:getName(), unitType = _enemyUnit:getTypeName(), unitId = _enemyUnit:getID() }
            local action = ", lasing new target, "
            if targetLost then
                action = ", target lost " .. action
                targetLost = false
            elseif targetDestroyed then
                action = ", target destroyed " .. action
                targetDestroyed = false
            end

            local message = _jtacGroupName .. action .. _enemyUnit:getTypeName()
            local fullMessage = message .. '. CODE: ' .. _laserCode .. ". POSITION: " .. ctld.getPositionString(_enemyUnit)
            ctld.notifyCoalition(fullMessage, 10, _jtacUnit:getCoalition(), _radio, message)

	        -- JTAC Unit stop his route -----------------
	        trigger.action.groupStopMoving(Group.getByName(_jtacGroupName)) -- stop JTAC
            
            -- create smoke
            if _smoke == true then

                --create first smoke
                ctld.createSmokeMarker(_enemyUnit, _colour)
            end
        end
    end

    if _enemyUnit ~= nil then

        ctld.laseUnit(_enemyUnit, _jtacUnit, _jtacGroupName, _laserCode)

        --   env.info('Timer timerSparkleLase '..jtacGroupName.." "..laserCode.." "..enemyUnit:getName())
        timer.scheduleFunction(ctld.timerJTACAutoLase, { _jtacGroupName, _laserCode, _smoke, _lock, _colour, _radio }, timer.getTime() + 15)


        if _smoke == true then
            local _nextSmokeTime = ctld.jtacSmokeMarks[_enemyUnit:getName()]

            --recreate smoke marker after 5 mins
            if _nextSmokeTime ~= nil and _nextSmokeTime < timer.getTime() then

                ctld.createSmokeMarker(_enemyUnit, _colour)
            end
        end

    else
        -- env.info('LASE: No Enemies Nearby')

        -- stop lazing the old spot
        ctld.cancelLase(_jtacGroupName)
        --  env.info('Timer Slow timerSparkleLase '..jtacGroupName.." "..laserCode.." "..enemyUnit:getName())

        timer.scheduleFunction(ctld.timerJTACAutoLase, { _jtacGroupName, _laserCode, _smoke, _lock, _colour, _radio }, timer.getTime() + 5)
    end

    if targetLost then
        ctld.notifyCoalition(_jtacGroupName .. ", target lost.", 10, _jtacUnit:getCoalition(), _radio)
    elseif targetDestroyed then
        ctld.notifyCoalition(_jtacGroupName .. ", target destroyed.", 10, _jtacUnit:getCoalition(), _radio)
    end
end

function ctld.JTACAutoLaseStop(_jtacGroupName)
    ctld.jtacStop[_jtacGroupName] = true
end

-- used by the timer function
function ctld.timerJTACAutoLase(_args)

    ctld.JTACAutoLase(_args[1], _args[2], _args[3], _args[4], _args[5], _args[6])
end

function ctld.cleanupJTAC(_jtacGroupName)
    -- clear laser - just in case
    ctld.cancelLase(_jtacGroupName)

    -- Cleanup
    ctld.jtacUnits[_jtacGroupName] = nil

    ctld.jtacCurrentTargets[_jtacGroupName] = nil

    ctld.jtacRadioData[_jtacGroupName] = nil
end


--- send a message to the coalition
--- if _radio is set, the message will be read out loud via SRS
function ctld.notifyCoalition(_message, _displayFor, _side, _radio, _shortMessage)
    ctld.logDebug(string.format("ctld.notifyCoalition(_message=%s)", ctld.p(_message)))
    ctld.logTrace(string.format("_radio=%s", ctld.p(_radio)))

    local _shortMessage = _shortMessage
    if _shortMessage == nil then 
        _shortMessage = _message
    end
    
    if STTS and STTS.TextToSpeech and _radio and _radio.freq then
        local _freq = _radio.freq
        local _modulation = _radio.mod or "FM"
        local _volume = _radio.volume or "1.0"
        local _name = _radio.name or "JTAC"
        local _gender = _radio.gender or "male"
        local _culture = _radio.culture or "en-US"
        local _voice = _radio.voice
        local _googleTTS = _radio.googleTTS or false
        ctld.logTrace(string.format("calling STTS.TextToSpeech(%s)", ctld.p(_shortMessage)))
        ctld.logTrace(string.format("_freq=%s", ctld.p(_freq)))
        ctld.logTrace(string.format("_modulation=%s", ctld.p(_modulation)))
        ctld.logTrace(string.format("_volume=%s", ctld.p(_volume)))
        ctld.logTrace(string.format("_name=%s", ctld.p(_name)))
        ctld.logTrace(string.format("_gender=%s", ctld.p(_gender)))
        ctld.logTrace(string.format("_culture=%s", ctld.p(_culture)))
        ctld.logTrace(string.format("_voice=%s", ctld.p(_voice)))
        ctld.logTrace(string.format("_googleTTS=%s", ctld.p(_googleTTS)))
        STTS.TextToSpeech(_shortMessage, _freq, _modulation, _volume, _name, _side, nil, 1, _gender, _culture, _voice, _googleTTS)
    end

    trigger.action.outTextForCoalition(_side, _message, _displayFor)
    trigger.action.outSoundForCoalition(_side, "radiobeep.ogg")
end

function ctld.createSmokeMarker(_enemyUnit, _colour)

    --recreate in 5 mins
    ctld.jtacSmokeMarks[_enemyUnit:getName()] = timer.getTime() + 300.0

    -- move smoke 2 meters above target for ease
    local _enemyPoint = _enemyUnit:getPoint()
    trigger.action.smoke({ x = _enemyPoint.x, y = _enemyPoint.y + 2.0, z = _enemyPoint.z }, _colour)
end

function ctld.cancelLase(_jtacGroupName)

    --local index = "JTAC_"..jtacUnit:getID()

    local _tempLase = ctld.jtacLaserPoints[_jtacGroupName]

    if _tempLase ~= nil then
        Spot.destroy(_tempLase)
        ctld.jtacLaserPoints[_jtacGroupName] = nil

        --      env.info('Destroy laze  '..index)

        _tempLase = nil
    end

    local _tempIR = ctld.jtacIRPoints[_jtacGroupName]

    if _tempIR ~= nil then
        Spot.destroy(_tempIR)
        ctld.jtacIRPoints[_jtacGroupName] = nil

        --  env.info('Destroy laze  '..index)

        _tempIR = nil
    end
end

function ctld.laseUnit(_enemyUnit, _jtacUnit, _jtacGroupName, _laserCode)

    --cancelLase(jtacGroupName)

    local _spots = {}

    local _enemyVector = _enemyUnit:getPoint()
    local _enemyVectorUpdated = { x = _enemyVector.x, y = _enemyVector.y + 2.0, z = _enemyVector.z }

    local _oldLase = ctld.jtacLaserPoints[_jtacGroupName]
    local _oldIR = ctld.jtacIRPoints[_jtacGroupName]

    if _oldLase == nil or _oldIR == nil then

        -- create lase

        local _status, _result = pcall(function()
            _spots['irPoint'] = Spot.createInfraRed(_jtacUnit, { x = 0, y = 2.0, z = 0 }, _enemyVectorUpdated)
            _spots['laserPoint'] = Spot.createLaser(_jtacUnit, { x = 0, y = 2.0, z = 0 }, _enemyVectorUpdated, _laserCode)
            return _spots
        end)

        if not _status then
            env.error('ERROR: ' .. _result, false)
        else
            if _result.irPoint then

                --    env.info(jtacUnit:getName() .. ' placed IR Pointer on '..enemyUnit:getName())

                ctld.jtacIRPoints[_jtacGroupName] = _result.irPoint --store so we can remove after
            end
            if _result.laserPoint then

                --  env.info(jtacUnit:getName() .. ' is Lasing '..enemyUnit:getName()..'. CODE:'..laserCode)

                ctld.jtacLaserPoints[_jtacGroupName] = _result.laserPoint
            end
        end

    else

        -- update lase

        if _oldLase ~= nil then
            _oldLase:setPoint(_enemyVectorUpdated)
        end

        if _oldIR ~= nil then
            _oldIR:setPoint(_enemyVectorUpdated)
        end
    end
end

-- get currently selected unit and check they're still in range
function ctld.getCurrentUnit(_jtacUnit, _jtacGroupName)


    local _unit = nil

    if ctld.jtacCurrentTargets[_jtacGroupName] ~= nil then
        _unit = Unit.getByName(ctld.jtacCurrentTargets[_jtacGroupName].name)
    end

    local _tempPoint = nil
    local _tempDist = nil
    local _tempPosition = nil

    local _jtacPosition = _jtacUnit:getPosition()
    local _jtacPoint = _jtacUnit:getPoint()

    if _unit ~= nil and _unit:getLife() > 0 and _unit:isActive() == true then

        -- calc distance
        _tempPoint = _unit:getPoint()
        --   tempPosition = unit:getPosition()

        _tempDist = ctld.getDistance(_unit:getPoint(), _jtacUnit:getPoint())
        if _tempDist < ctld.JTAC_maxDistance then
            -- calc visible

            -- check slightly above the target as rounding errors can cause issues, plus the unit has some height anyways
            local _offsetEnemyPos = { x = _tempPoint.x, y = _tempPoint.y + 2.0, z = _tempPoint.z }
            local _offsetJTACPos = { x = _jtacPoint.x, y = _jtacPoint.y + 2.0, z = _jtacPoint.z }

            if land.isVisible(_offsetEnemyPos, _offsetJTACPos) then
                return _unit
            end
        end
    end
    return nil
end


-- Find nearest enemy to JTAC that isn't blocked by terrain
function ctld.findNearestVisibleEnemy(_jtacUnit, _targetType,_distance)

    --local startTime = os.clock()

    local _maxDistance = _distance or ctld.JTAC_maxDistance

    local _nearestDistance = _maxDistance

    local _jtacPoint = _jtacUnit:getPoint()
    local _coa =    _jtacUnit:getCoalition()

    local _offsetJTACPos = { x = _jtacPoint.x, y = _jtacPoint.y + 2.0, z = _jtacPoint.z }

    local _volume = {
        id = world.VolumeType.SPHERE,
        params = {
            point = _offsetJTACPos,
            radius = _maxDistance
        }
    }

    local _unitList = {}


    local _search = function(_unit, _coa)
        pcall(function()

            if _unit ~= nil
                    and _unit:getLife() > 0
                    and _unit:isActive()
                    and _unit:getCoalition() ~= _coa
                    and not _unit:inAir()
                    and not ctld.alreadyTarget(_jtacUnit,_unit) then

                local _tempPoint = _unit:getPoint()
                local _offsetEnemyPos = { x = _tempPoint.x, y = _tempPoint.y + 2.0, z = _tempPoint.z }

                if land.isVisible(_offsetJTACPos,_offsetEnemyPos ) then

                    local _dist = ctld.getDistance(_offsetJTACPos, _offsetEnemyPos)

                    if _dist < _maxDistance then
                        table.insert(_unitList,{unit=_unit, dist=_dist})

                    end
                end
            end
        end)

        return true
    end

    world.searchObjects(Object.Category.UNIT, _volume, _search, _coa)

    --log.info(string.format("JTAC Search elapsed time: %.4f\n", os.clock() - startTime))

    -- generate list order by distance & visible

    -- first check
    -- hpriority
    -- priority
    -- vehicle
    -- unit

    local _sort = function( a,b ) return a.dist < b.dist end
    table.sort(_unitList,_sort)
    -- sort list

    -- check for hpriority
    for _, _enemyUnit in ipairs(_unitList) do
        local _enemyName = _enemyUnit.unit:getName()

        if string.match(_enemyName, "hpriority") then
            return _enemyUnit.unit
        end
    end

    for _, _enemyUnit in ipairs(_unitList) do
        local _enemyName = _enemyUnit.unit:getName()

        if string.match(_enemyName, "priority") then
            return _enemyUnit.unit
        end
    end

    local result = nil
    for _, _enemyUnit in ipairs(_unitList) do
        local _enemyName = _enemyUnit.unit:getName()
        --log.info(string.format("CTLD - checking _enemyName=%s", _enemyName))

        -- check for air defenses
        --log.info(string.format("CTLD - _enemyUnit.unit:getDesc()[attributes]=%s", ctld.p(_enemyUnit.unit:getDesc()["attributes"])))
        local airdefense = (_enemyUnit.unit:getDesc()["attributes"]["Air Defence"] ~= nil)
        --log.info(string.format("CTLD - airdefense=%s", tostring(airdefense)))

        if (_targetType == "vehicle" and ctld.isVehicle(_enemyUnit.unit)) or _targetType == "all" then
            if airdefense then
                return _enemyUnit.unit
            else
                result = _enemyUnit.unit
            end

        elseif (_targetType == "troop" and ctld.isInfantry(_enemyUnit.unit)) or _targetType == "all" then
            if airdefense then
                return _enemyUnit.unit
            else
                result = _enemyUnit.unit
            end
        end
    end

    return result

end


function ctld.listNearbyEnemies(_jtacUnit)

    local _maxDistance =  ctld.JTAC_maxDistance

    local _jtacPoint = _jtacUnit:getPoint()
    local _coa =    _jtacUnit:getCoalition()

    local _offsetJTACPos = { x = _jtacPoint.x, y = _jtacPoint.y + 2.0, z = _jtacPoint.z }

    local _volume = {
        id = world.VolumeType.SPHERE,
        params = {
            point = _offsetJTACPos,
            radius = _maxDistance
        }
    }
    local _enemies = nil

    local _search = function(_unit, _coa)
        pcall(function()

            if _unit ~= nil
                    and _unit:getLife() > 0
                    and _unit:isActive()
                    and _unit:getCoalition() ~= _coa
                    and not _unit:inAir() then

                local _tempPoint = _unit:getPoint()
                local _offsetEnemyPos = { x = _tempPoint.x, y = _tempPoint.y + 2.0, z = _tempPoint.z }

                if land.isVisible(_offsetJTACPos,_offsetEnemyPos ) then

                    if not _enemies then
                        _enemies = {}
                    end

                    _enemies[_unit:getTypeName()] = _unit:getTypeName()

                end
            end
        end)

        return true
    end

    world.searchObjects(Object.Category.UNIT, _volume, _search, _coa)

    return _enemies
end

-- tests whether the unit is targeted by another JTAC
function ctld.alreadyTarget(_jtacUnit, _enemyUnit)

    for _, _jtacTarget in pairs(ctld.jtacCurrentTargets) do

        if _jtacTarget.unitId == _enemyUnit:getID() then
            -- env.info("ALREADY TARGET")
            return true
        end
    end

    return false
end


-- Returns only alive units from group but the group / unit may not be active

function ctld.getGroup(groupName)

    local _groupUnits = Group.getByName(groupName)

    local _filteredUnits = {} --contains alive units
    local _x = 1

    if _groupUnits ~= nil and _groupUnits:isExist() then

        _groupUnits = _groupUnits:getUnits()

        if _groupUnits ~= nil and #_groupUnits > 0 then
            for _x = 1, #_groupUnits do
                if _groupUnits[_x]:getLife() > 0  then -- removed and _groupUnits[_x]:isExist() as isExist doesnt work on single units!
                table.insert(_filteredUnits, _groupUnits[_x])
                end
            end
        end
    end

    return _filteredUnits
end

function ctld.getAliveGroup(_groupName)

    local _group = Group.getByName(_groupName)

    if _group and _group:isExist() == true and #_group:getUnits() > 0 then
        return _group
    end

    return nil
end

-- gets the JTAC status and displays to coalition units
function ctld.getJTACStatus(_args)

    --returns the status of all JTAC units

    local _playerUnit = ctld.getTransportUnit(_args[1])

    if _playerUnit == nil then
        return
    end

    local _side = _playerUnit:getCoalition()

    local _jtacGroupName = nil
    local _jtacUnit = nil

    local _message = "JTAC STATUS: \n\n"

    for _jtacGroupName, _jtacDetails in pairs(ctld.jtacUnits) do

        --look up units
        _jtacUnit = Unit.getByName(_jtacDetails.name)

        if _jtacUnit ~= nil and _jtacUnit:getLife() > 0 and _jtacUnit:isActive() == true and _jtacUnit:getCoalition() == _side then

            local _enemyUnit = ctld.getCurrentUnit(_jtacUnit, _jtacGroupName)

            local _laserCode = ctld.jtacLaserPointCodes[_jtacGroupName]

            local _start = _jtacGroupName
            if (_jtacDetails.radio) then
                _start = _start .. ", available on ".._jtacDetails.radio.freq.." ".._jtacDetails.radio.mod ..","
            end

            if _laserCode == nil then
                _laserCode = "UNKNOWN"
            end

            if _enemyUnit ~= nil and _enemyUnit:getLife() > 0 and _enemyUnit:isActive() == true then
                _message = _message .. "" .. _start .. " targeting " .. _enemyUnit:getTypeName() .. " CODE: " .. _laserCode .. ctld.getPositionString(_enemyUnit) .. "\n"

                local _list = ctld.listNearbyEnemies(_jtacUnit)

                if _list then
                    _message = _message.."Visual On: "

                    for _,_type in pairs(_list) do
                        _message = _message.._type.." "
                    end
                    _message = _message.."\n"
                end

            else
                _message = _message .. "" .. _start .. " searching for targets" .. ctld.getPositionString(_jtacUnit) .. "\n"
            end
        end
    end

    if _message == "JTAC STATUS: \n\n" then
        _message = "No Active JTACs"
    end


    ctld.notifyCoalition(_message, 10, _side)
end



function ctld.isInfantry(_unit)

    local _typeName = _unit:getTypeName()

    --type coerce tostring
    _typeName = string.lower(_typeName .. "")

    local _soldierType = { "infantry", "paratrooper", "stinger", "manpad", "mortar" }

    for _key, _value in pairs(_soldierType) do
        if string.match(_typeName, _value) then
            return true
        end
    end

    return false
end

-- assume anything that isnt soldier is vehicle
function ctld.isVehicle(_unit)

    if ctld.isInfantry(_unit) then
        return false
    end

    return true
end

-- The entered value can range from 1111 - 1788,
-- -- but the first digit of the series must be a 1 or 2
-- -- and the last three digits must be between 1 and 8.
--  The range used to be bugged so its not 1 - 8 but 0 - 7.
-- function below will use the range 1-7 just incase
function ctld.generateLaserCode()

    ctld.jtacGeneratedLaserCodes = {}

    -- generate list of laser codes
    local _code = 1111

    local _count = 1

    while _code < 1777 and _count < 30 do

        while true do

            _code = _code + 1

            if not ctld.containsDigit(_code, 8)
                    and not ctld.containsDigit(_code, 9)
                    and not ctld.containsDigit(_code, 0) then

                table.insert(ctld.jtacGeneratedLaserCodes, _code)

                --env.info(_code.." Code")
                break
            end
        end
        _count = _count + 1
    end
end

function ctld.containsDigit(_number, _numberToFind)

    local _thisNumber = _number
    local _thisDigit = 0

    while _thisNumber ~= 0 do

        _thisDigit = _thisNumber % 10
        _thisNumber = math.floor(_thisNumber / 10)

        if _thisDigit == _numberToFind then
            return true
        end
    end

    return false
end

-- 200 - 400 in 10KHz
-- 400 - 850 in 10 KHz
-- 850 - 1250 in 50 KHz
function ctld.generateVHFrequencies()

    --ignore list
    --list of all frequencies in KHZ that could conflict with
    -- 191 - 1290 KHz, beacon range
    local _skipFrequencies = {
        745, --Astrahan
        381,
        384,
        300.50,
        312.5,
        1175,
        342,
        735,
        300.50,
        353.00,
        440,
        795,
        525,
        520,
        690,
        625,
        291.5,
        300.50,
        435,
        309.50,
        920,
        1065,
        274,
        312.50,
        580,
        602,
        297.50,
        750,
        485,
        950,
        214,
        1025, 730, 995, 455, 307, 670, 329, 395, 770,
        380, 705, 300.5, 507, 740, 1030, 515,
        330, 309.5,
        348, 462, 905, 352, 1210, 942, 435,
        324,
        320, 420, 311, 389, 396, 862, 680, 297.5,
        920, 662,
        866, 907, 309.5, 822, 515, 470, 342, 1182, 309.5, 720, 528,
        337, 312.5, 830, 740, 309.5, 641, 312, 722, 682, 1050,
        1116, 935, 1000, 430, 577,
        326 -- Nevada
    }

    ctld.freeVHFFrequencies = {}
    local _start = 200000

    -- first range
    while _start < 400000 do

        -- skip existing NDB frequencies
        local _found = false
        for _, value in pairs(_skipFrequencies) do
            if value * 1000 == _start then
                _found = true
                break
            end
        end


        if _found == false then
            table.insert(ctld.freeVHFFrequencies, _start)
        end

        _start = _start + 10000
    end

    _start = 400000
    -- second range
    while _start < 850000 do

        -- skip existing NDB frequencies
        local _found = false
        for _, value in pairs(_skipFrequencies) do
            if value * 1000 == _start then
                _found = true
                break
            end
        end

        if _found == false then
            table.insert(ctld.freeVHFFrequencies, _start)
        end


        _start = _start + 10000
    end

    _start = 850000
    -- third range
    while _start <= 1250000 do

        -- skip existing NDB frequencies
        local _found = false
        for _, value in pairs(_skipFrequencies) do
            if value * 1000 == _start then
                _found = true
                break
            end
        end

        if _found == false then
            table.insert(ctld.freeVHFFrequencies, _start)
        end

        _start = _start + 50000
    end
end

-- 220 - 399 MHZ, increments of 0.5MHZ
function ctld.generateUHFrequencies()

    ctld.freeUHFFrequencies = {}
    local _start = 220000000

    while _start < 399000000 do
        table.insert(ctld.freeUHFFrequencies, _start)
        _start = _start + 500000
    end
end


-- 220 - 399 MHZ, increments of 0.5MHZ
--    -- first digit 3-7MHz
--    -- second digit 0-5KHz
--    -- third digit 0-9
--    -- fourth digit 0 or 5
--    -- times by 10000
--
function ctld.generateFMFrequencies()

    ctld.freeFMFrequencies = {}
    local _start = 220000000

    while _start < 399000000 do

        _start = _start + 500000
    end

    for _first = 3, 7 do
        for _second = 0, 5 do
            for _third = 0, 9 do
                local _frequency = ((100 * _first) + (10 * _second) + _third) * 100000 --extra 0 because we didnt bother with 4th digit
                table.insert(ctld.freeFMFrequencies, _frequency)
            end
        end
    end
end

function ctld.getPositionString(_unit)

    if ctld.JTAC_location == false then
        return ""
    end

    local _lat, _lon = coord.LOtoLL(_unit:getPosition().p)

    local _latLngStr = mist.tostringLL(_lat, _lon, 3, ctld.location_DMS)

    local _mgrsString = mist.tostringMGRS(coord.LLtoMGRS(coord.LOtoLL(_unit:getPosition().p)), 5)

    return " @ " .. _latLngStr .. " - MGRS " .. _mgrsString
end


-- ***************** SETUP SCRIPT ****************
function ctld.initialize(force)
    ctld.logInfo(string.format("Initializing version %s", ctld.Version))
    ctld.logTrace(string.format("ctld.alreadyInitialized=%s", ctld.p(ctld.alreadyInitialized)))
    ctld.logTrace(string.format("force=%s", ctld.p(force)))

    if ctld.alreadyInitialized and not force then
        ctld.logInfo(string.format("Bypassing initialization because ctld.alreadyInitialized = true"))
        return
    end

    assert(mist ~= nil, "\n\n** HEY MISSION-DESIGNER! **\n\nMiST has not been loaded!\n\nMake sure MiST 3.6 or higher is running\n*before* running this script!\n")

    ctld.addedTo = {}
    ctld.spawnedCratesRED = {} -- use to store crates that have been spawned
    ctld.spawnedCratesBLUE = {} -- use to store crates that have been spawned

    ctld.droppedTroopsRED = {} -- stores dropped troop groups
    ctld.droppedTroopsBLUE = {} -- stores dropped troop groups

    ctld.droppedVehiclesRED = {} -- stores vehicle groups for c-130 / hercules
    ctld.droppedVehiclesBLUE = {} -- stores vehicle groups for c-130 / hercules

    ctld.inTransitTroops = {}

    ctld.inTransitFOBCrates = {}

    ctld.inTransitSlingLoadCrates = {} -- stores crates that are being transported by helicopters for alternative to real slingload

    ctld.droppedFOBCratesRED = {}
    ctld.droppedFOBCratesBLUE = {}

    ctld.builtFOBS = {} -- stores fully built fobs

    ctld.completeAASystems = {} -- stores complete spawned groups from multiple crates

    ctld.fobBeacons = {} -- stores FOB radio beacon details, refreshed every 60 seconds

    ctld.deployedRadioBeacons = {} -- stores details of deployed radio beacons

    ctld.beaconCount = 1

    ctld.usedUHFFrequencies = {}
    ctld.usedVHFFrequencies = {}
    ctld.usedFMFrequencies = {}

    ctld.freeUHFFrequencies = {}
    ctld.freeVHFFrequencies = {}
    ctld.freeFMFrequencies = {}

    --used to lookup what the crate will contain
    ctld.crateLookupTable = {}

    ctld.extractZones = {} -- stored extract zones

    ctld.missionEditorCargoCrates = {} --crates added by mission editor for triggering cratesinzone
    ctld.hoverStatus = {} -- tracks status of a helis hover above a crate

    ctld.callbacks = {} -- function callback


    -- Remove intransit troops when heli / cargo plane dies
    --ctld.eventHandler = {}
    --function ctld.eventHandler:onEvent(_event)
    --
    --    if _event == nil or _event.initiator == nil then
    --        env.info("CTLD null event")
    --    elseif _event.id == 9 then
    --        -- Pilot dead
    --        ctld.inTransitTroops[_event.initiator:getName()] = nil
    --
    --    elseif world.event.S_EVENT_EJECTION == _event.id or _event.id == 8 then
    --        -- env.info("Event unit - Pilot Ejected or Unit Dead")
    --        ctld.inTransitTroops[_event.initiator:getName()] = nil
    --
    --        -- env.info(_event.initiator:getName())
    --    end
    --
    --end

    -- create crate lookup table
    for _subMenuName, _crates in pairs(ctld.spawnableCrates) do

        for _, _crate in pairs(_crates) do
            -- convert number to string otherwise we'll have a pointless giant
            -- table. String means 'hashmap' so it will only contain the right number of elements
            ctld.crateLookupTable[tostring(_crate.weight)] = _crate
        end
    end


    --sort out pickup zones
    for _, _zone in pairs(ctld.pickupZones) do

        local _zoneName = _zone[1]
        local _zoneColor = _zone[2]
        local _zoneActive = _zone[4]

        if _zoneColor == "green" then
            _zone[2] = trigger.smokeColor.Green
        elseif _zoneColor == "red" then
            _zone[2] = trigger.smokeColor.Red
        elseif _zoneColor == "white" then
            _zone[2] = trigger.smokeColor.White
        elseif _zoneColor == "orange" then
            _zone[2] = trigger.smokeColor.Orange
        elseif _zoneColor == "blue" then
            _zone[2] = trigger.smokeColor.Blue
        else
            _zone[2] = -1 -- no smoke colour
        end

        -- add in counter for troops or units
        if _zone[3] == -1 then
            _zone[3] = 10000;
        end

        -- change active to 1 / 0
        if _zoneActive == "yes" then
            _zone[4] = 1
        else
            _zone[4] = 0
        end
    end

    --sort out dropoff zones
    for _, _zone in pairs(ctld.dropOffZones) do

        local _zoneColor = _zone[2]

        if _zoneColor == "green" then
            _zone[2] = trigger.smokeColor.Green
        elseif _zoneColor == "red" then
            _zone[2] = trigger.smokeColor.Red
        elseif _zoneColor == "white" then
            _zone[2] = trigger.smokeColor.White
        elseif _zoneColor == "orange" then
            _zone[2] = trigger.smokeColor.Orange
        elseif _zoneColor == "blue" then
            _zone[2] = trigger.smokeColor.Blue
        else
            _zone[2] = -1 -- no smoke colour
        end

        --mark as active for refresh smoke logic to work
        _zone[4] = 1
    end

    --sort out waypoint zones
    for _, _zone in pairs(ctld.wpZones) do

        local _zoneColor = _zone[2]

        if _zoneColor == "green" then
            _zone[2] = trigger.smokeColor.Green
        elseif _zoneColor == "red" then
            _zone[2] = trigger.smokeColor.Red
        elseif _zoneColor == "white" then
            _zone[2] = trigger.smokeColor.White
        elseif _zoneColor == "orange" then
            _zone[2] = trigger.smokeColor.Orange
        elseif _zoneColor == "blue" then
            _zone[2] = trigger.smokeColor.Blue
        else
            _zone[2] = -1 -- no smoke colour
        end

        --mark as active for refresh smoke logic to work
        -- change active to 1 / 0
        if  _zone[3] == "yes" then
            _zone[3] = 1
        else
            _zone[3] = 0
        end
    end

    -- Sort out extractable groups
    for _, _groupName in pairs(ctld.extractableGroups) do

        local _group = Group.getByName(_groupName)

        if _group ~= nil then

            if _group:getCoalition() == 1 then
                table.insert(ctld.droppedTroopsRED, _group:getName())
            else
                table.insert(ctld.droppedTroopsBLUE, _group:getName())
            end
        end
    end


    -- Seperate troop teams into red and blue for random AI pickups
    if ctld.allowRandomAiTeamPickups == true then
        ctld.redTeams = {}
        ctld.blueTeams = {}
        for _,_loadGroup in pairs(ctld.loadableGroups) do
            if not _loadGroup.side then
                table.insert(ctld.redTeams, _)
                table.insert(ctld.blueTeams, _)
            elseif _loadGroup.side == 1 then
                table.insert(ctld.redTeams, _)
            elseif _loadGroup.side == 2 then
                table.insert(ctld.blueTeams, _)
            end
        end
    end

    -- add total count

    for _,_loadGroup in pairs(ctld.loadableGroups) do

        _loadGroup.total = 0
        if _loadGroup.aa then
            _loadGroup.total = _loadGroup.aa + _loadGroup.total
        end

        if _loadGroup.inf then
            _loadGroup.total = _loadGroup.inf + _loadGroup.total
        end


        if _loadGroup.mg then
            _loadGroup.total = _loadGroup.mg + _loadGroup.total
        end

        if _loadGroup.at then
            _loadGroup.total = _loadGroup.at + _loadGroup.total
        end

        if _loadGroup.mortar then
            _loadGroup.total = _loadGroup.mortar + _loadGroup.total
        end

    end


    -- Scheduled functions (run cyclically) -- but hold execution for a second so we can override parts

    timer.scheduleFunction(ctld.checkAIStatus, nil, timer.getTime() + 1)
    timer.scheduleFunction(ctld.checkTransportStatus, nil, timer.getTime() + 5)

    timer.scheduleFunction(function()

        timer.scheduleFunction(ctld.refreshRadioBeacons, nil, timer.getTime() + 5)
        timer.scheduleFunction(ctld.refreshSmoke, nil, timer.getTime() + 5)
        timer.scheduleFunction(ctld.addF10MenuOptions, nil, timer.getTime() + 5)

        if ctld.enableCrates == true and ctld.slingLoad == false and ctld.hoverPickup == true then
            timer.scheduleFunction(ctld.checkHoverStatus, nil, timer.getTime() + 1)
        end

    end,nil, timer.getTime()+1 )

    --event handler for deaths
    --world.addEventHandler(ctld.eventHandler)

    --env.info("CTLD event handler added")

    env.info("Generating Laser Codes")
    ctld.generateLaserCode()
    env.info("Generated Laser Codes")



    env.info("Generating UHF Frequencies")
    ctld.generateUHFrequencies()
    env.info("Generated  UHF Frequencies")

    env.info("Generating VHF Frequencies")
    ctld.generateVHFrequencies()
    env.info("Generated VHF Frequencies")


    env.info("Generating FM Frequencies")
    ctld.generateFMFrequencies()
    env.info("Generated FM Frequencies")

    -- Search for crates
    -- Crates are NOT returned by coalition.getStaticObjects() for some reason
    -- Search for crates in the mission editor instead
    env.info("Searching for Crates")
    for _coalitionName, _coalitionData in pairs(env.mission.coalition) do

        if (_coalitionName == 'red' or _coalitionName == 'blue')
                and type(_coalitionData) == 'table' then
            if _coalitionData.country then --there is a country table
            for _, _countryData in pairs(_coalitionData.country) do

                if type(_countryData) == 'table' then
                    for _objectTypeName, _objectTypeData in pairs(_countryData) do
                        if _objectTypeName == "static" then

                            if ((type(_objectTypeData) == 'table')
                                    and _objectTypeData.group
                                    and (type(_objectTypeData.group) == 'table')
                                    and (#_objectTypeData.group > 0)) then

                                for _groupId, _group in pairs(_objectTypeData.group) do
                                    if _group and _group.units and type(_group.units) == 'table' then
                                        for _unitNum, _unit in pairs(_group.units) do
                                            if _unit.canCargo == true then
                                                local _cargoName = env.getValueDictByKey(_unit.name)
                                                ctld.missionEditorCargoCrates[_cargoName] = _cargoName
                                                env.info("Crate Found: " .. _unit.name.." - Unit: ".._cargoName)
                                            end
                                        end
                                    end
                                end
                            end
                        end
                    end
                end
            end
            end
        end
    end
    env.info("END search for crates")

    -- don't initialize more than once
    ctld.alreadyInitialized = true

    env.info("CTLD READY")
end


-- initialize the random number generator to make it almost random
math.random(); math.random(); math.random()

--- Enable/Disable error boxes displayed on screen.
env.setErrorMessageBoxEnabled(false)

-- initialize CTLD in 2 seconds, so other scripts have a chance to modify the configuration before initialization
ctld.logInfo(string.format("Loading version %s in 2 seconds", ctld.Version))
timer.scheduleFunction(ctld.initialize, nil, timer.getTime() + 2)

--DEBUG FUNCTION
--        for key, value in pairs(getmetatable(_spawnedCrate)) do
--            env.info(tostring(key))
--            env.info(tostring(value))
--        end
