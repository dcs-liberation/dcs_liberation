-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- DCS World units database
-- By zip (2018)
--
-- Load the script:
-- ----------------
-- 1.) Download the script and save it anywhere on your hard drive.
-- 2.) Open your mission in the mission editor.
-- 3.) Add a new trigger:
--     * TYPE   "4 MISSION START"
--     * ACTION "DO SCRIPT FILE"
--     * OPEN --> Browse to the location where you saved the script and click OK.
--
-------------------------------------------------------------------------------------------------------------------------------------------------------------

dcsUnits = {}

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Global settings. Stores the root VEAF constants
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Identifier. All output in DCS.log will start with this.
dcsUnits.Id = "DCSUNITS - "

--- Version.
dcsUnits.Version = "2020.06.06"

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Do not change anything below unless you know what you are doing!
-------------------------------------------------------------------------------------------------------------------------------------------------------------

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Utility methods
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function dcsUnits.logInfo(message)
    if message then
        veaf.logInfo(dcsUnits.Id .. message)
    end
end

function dcsUnits.logDebug(message)
    if message then
        veaf.logDebug(dcsUnits.Id .. message)
    end
end

function dcsUnits.logTrace(message)
    if message then
        veaf.logTrace(dcsUnits.Id .. message)
    end
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Raw DCS units database
-------------------------------------------------------------------------------------------------------------------------------------------------------------

dcsUnits.DcsUnitsDatabase =
{
    [1] = 
    {
        ["type"] = "flak18",
        ["name"] = "AAA 8,8cm Flak 18",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "AAA 8,8cm Flak 18",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [1]
    [2] = 
    {
        ["type"] = "flak36",
        ["name"] = "AAA 8,8cm Flak 36",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "AAA 8,8cm Flak 36",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [2]
    [3] = 
    {
        ["type"] = "flak37",
        ["name"] = "AAA 8,8cm Flak 37",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "AAA 8,8cm Flak 37",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [3]
    [4] = 
    {
        ["type"] = "flak41",
        ["name"] = "AAA 8,8cm Flak 41",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "AAA 8,8cm Flak 41",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [4]
    [5] = 
    {
        ["type"] = "bofors40",
        ["name"] = "AAA Bofors 40mm",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "AAA Bofors 40mm",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [5]
    [6] = 
    {
        ["type"] = "flak30",
        ["name"] = "AAA Flak 38",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "AAA Flak 38",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [6]
    [7] = 
    {
        ["type"] = "flak38",
        ["name"] = "AAA Flak-Vierling 38",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "AAA Flak-Vierling 38",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [7]
    [8] = 
    {
        ["type"] = "KDO_Mod40",
        ["name"] = "AAA Kdo.G.40",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "AAA Kdo.G.40",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [8]
    [9] = 
    {
        ["type"] = "Vulcan",
        ["name"] = "AAA Vulcan M163",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "AAA Vulcan M163",
        ["aliases"] = 
        {
            [1] = "M163 Vulcan",
        }, -- end of ["aliases"]
    }, -- end of [9]
    [10] = 
    {
        ["type"] = "ZU-23 Emplacement Closed",
        ["name"] = "AAA ZU-23 Closed",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "AAA ZU-23 Closed",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [10]
    [11] = 
    {
        ["type"] = "ZU-23 Emplacement",
        ["name"] = "AAA ZU-23 Emplacement",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "AAA ZU-23 Emplacement",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [11]
    [12] = 
    {
        ["type"] = "ZU-23 Insurgent",
        ["name"] = "AAA ZU-23 Insurgent",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "AAA ZU-23 Insurgent",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [12]
    [13] = 
    {
        ["type"] = "ZU-23 Closed Insurgent",
        ["name"] = "AAA ZU-23 Insurgent Closed",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "AAA ZU-23 Insurgent Closed",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [13]
    [14] = 
    {
        ["type"] = "Ural-375 ZU-23 Insurgent",
        ["name"] = "AAA ZU-23 Insurgent on Ural-375",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "AAA ZU-23 Insurgent on Ural-375",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [14]
    [15] = 
    {
        ["type"] = "Ural-375 ZU-23",
        ["name"] = "AAA ZU-23 on Ural-375",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "AAA ZU-23 on Ural-375",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [15]
    [16] = 
    {
        ["type"] = "Dog Ear radar",
        ["name"] = "CP 9S80M1 Sborka",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "CP 9S80M1 Sborka",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [16]
    [17] = 
    {
        ["type"] = "1L13 EWR",
        ["name"] = "EWR 1L13",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "EWR 1L13",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [17]
    [18] = 
    {
        ["type"] = "55G6 EWR",
        ["name"] = "EWR 55G6",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "EWR 55G6",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [18]
    [19] = 
    {
        ["type"] = "Flakscheinwerfer_37",
        ["name"] = "Flak Searchlight 37",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "Flak Searchlight 37",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [19]
    [20] = 
    {
        ["type"] = "HQ-7_LN_SP",
        ["name"] = "HQ-7 Self-Propelled LN",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "HQ-7 Self-Propelled LN",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [20]
    [21] = 
    {
        ["type"] = "HQ-7_STR_SP",
        ["name"] = "HQ-7 Self-Propelled STR",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "HQ-7 Self-Propelled STR",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [21]
    [22] = 
    {
        ["type"] = "Maschinensatz_33",
        ["name"] = "Maschinensatz_33",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "Maschinensatz_33",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [22]
    [23] = 
    {
        ["type"] = "rapier_fsa_blindfire_radar",
        ["name"] = "Rapier FSA Blindfire Tracker",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "Rapier FSA Blindfire Tracker",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [23]
    [24] = 
    {
        ["type"] = "rapier_fsa_launcher",
        ["name"] = "Rapier FSA Launcher",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "Rapier FSA Launcher",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [24]
    [25] = 
    {
        ["type"] = "rapier_fsa_optical_tracker_unit",
        ["name"] = "Rapier FSA Optical Tracker",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "Rapier FSA Optical Tracker",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [25]
    [26] = 
    {
        ["type"] = "M1097 Avenger",
        ["name"] = "SAM Avenger M1097",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM Avenger M1097",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [26]
    [27] = 
    {
        ["type"] = "M48 Chaparral",
        ["name"] = "SAM Chaparral M48",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM Chaparral M48",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [27]
    [28] = 
    {
        ["type"] = "Hawk cwar",
        ["name"] = "SAM Hawk CWAR AN/MPQ-55",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM Hawk CWAR AN/MPQ-55",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [28]
    [29] = 
    {
        ["type"] = "Hawk ln",
        ["name"] = "SAM Hawk LN M192",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM Hawk LN M192",
        ["aliases"] = 
        {
            [1] = "Hawk M192 LN",
        }, -- end of ["aliases"]
    }, -- end of [29]
    [30] = 
    {
        ["type"] = "Hawk pcp",
        ["name"] = "SAM Hawk PCP",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM Hawk PCP",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [30]
    [31] = 
    {
        ["type"] = "Hawk sr",
        ["name"] = "SAM Hawk SR AN/MPQ-50",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM Hawk SR AN/MPQ-50",
        ["aliases"] = 
        {
            [1] = "Hawk AN/MPQ-50 SR",
        }, -- end of ["aliases"]
    }, -- end of [31]
    [32] = 
    {
        ["type"] = "Hawk tr",
        ["name"] = "SAM Hawk TR AN/MPQ-46",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM Hawk TR AN/MPQ-46",
        ["aliases"] = 
        {
            [1] = "Hawk AN/MPQ-46 TR",
        }, -- end of ["aliases"]
    }, -- end of [32]
    [33] = 
    {
        ["type"] = "M6 Linebacker",
        ["name"] = "SAM Linebacker M6",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM Linebacker M6",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [33]
    [34] = 
    {
        ["type"] = "Patriot AMG",
        ["name"] = "SAM Patriot AMG AN/MRC-137",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM Patriot AMG AN/MRC-137",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [34]
    [35] = 
    {
        ["type"] = "Patriot ECS",
        ["name"] = "SAM Patriot ECS AN/MSQ-104",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM Patriot ECS AN/MSQ-104",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [35]
    [36] = 
    {
        ["type"] = "Patriot EPP",
        ["name"] = "SAM Patriot EPP-III",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM Patriot EPP-III",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [36]
    [37] = 
    {
        ["type"] = "Patriot cp",
        ["name"] = "SAM Patriot ICC",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM Patriot ICC",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [37]
    [38] = 
    {
        ["type"] = "Patriot ln",
        ["name"] = "SAM Patriot LN M901",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM Patriot LN M901",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [38]
    [39] = 
    {
        ["type"] = "Patriot str",
        ["name"] = "SAM Patriot STR AN/MPQ-53",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM Patriot STR AN/MPQ-53",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [39]
    [40] = 
    {
        ["type"] = "Roland ADS",
        ["name"] = "SAM Roland ADS",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM Roland ADS",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [40]
    [41] = 
    {
        ["type"] = "Roland Radar",
        ["name"] = "SAM Roland EWR",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM Roland EWR",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [41]
    [42] = 
    {
        ["type"] = "S-300PS 54K6 cp",
        ["name"] = "SAM SA-10 S-300PS CP 54K6",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-10 S-300PS CP 54K6",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [42]
    [43] = 
    {
        ["type"] = "S-300PS 5P85C ln",
        ["name"] = "SAM SA-10 S-300PS LN 5P85C",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-10 S-300PS LN 5P85C",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [43]
    [44] = 
    {
        ["type"] = "S-300PS 5P85D ln",
        ["name"] = "SAM SA-10 S-300PS LN 5P85D",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-10 S-300PS LN 5P85D",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [44]
    [45] = 
    {
        ["type"] = "S-300PS 40B6MD sr",
        ["name"] = "SAM SA-10 S-300PS SR 5N66M",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-10 S-300PS SR 5N66M",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [45]
    [46] = 
    {
        ["type"] = "S-300PS 64H6E sr",
        ["name"] = "SAM SA-10 S-300PS SR 64H6E",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-10 S-300PS SR 64H6E",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [46]
    [47] = 
    {
        ["type"] = "S-300PS 40B6M tr",
        ["name"] = "SAM SA-10 S-300PS TR 30N6",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-10 S-300PS TR 30N6",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [47]
    [48] = 
    {
        ["type"] = "SA-11 Buk CC 9S470M1",
        ["name"] = "SAM SA-11 Buk CC 9S470M1",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-11 Buk CC 9S470M1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [48]
    [49] = 
    {
        ["type"] = "SA-11 Buk LN 9A310M1",
        ["name"] = "SAM SA-11 Buk LN 9A310M1",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-11 Buk LN 9A310M1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [49]
    [50] = 
    {
        ["type"] = "SA-11 Buk SR 9S18M1",
        ["name"] = "SAM SA-11 Buk SR 9S18M1",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-11 Buk SR 9S18M1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [50]
    [51] = 
    {
        ["type"] = "Strela-10M3",
        ["name"] = "SAM SA-13 Strela-10M3 9A35M3",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-13 Strela-10M3 9A35M3",
        ["aliases"] = 
        {
            [1] = "SA-13 Strela-10M3 9A35M3",
        }, -- end of ["aliases"]
    }, -- end of [51]
    [52] = 
    {
        ["type"] = "Tor 9A331",
        ["name"] = "SAM SA-15 Tor 9A331",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-15 Tor 9A331",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [52]
    [53] = 
    {
        ["type"] = "SA-18 Igla comm",
        ["name"] = "SAM SA-18 Igla comm",
        ["category"] = "Air Defence",
        ["infantry"] = true,
        ["vehicle"] = true,
        ["description"] = "SAM SA-18 Igla comm",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [53]
    [54] = 
    {
        ["type"] = "SA-18 Igla manpad",
        ["name"] = "SAM SA-18 Igla MANPADS",
        ["category"] = "Air Defence",
        ["infantry"] = true,
        ["vehicle"] = true,
        ["description"] = "SAM SA-18 Igla MANPADS",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [54]
    [55] = 
    {
        ["type"] = "Igla manpad INS",
        ["name"] = "SAM SA-18 Igla MANPADS",
        ["category"] = "Air Defence",
        ["infantry"] = true,
        ["vehicle"] = true,
        ["description"] = "SAM SA-18 Igla MANPADS",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [55]
    [56] = 
    {
        ["type"] = "SA-18 Igla-S comm",
        ["name"] = "SAM SA-18 Igla-S comm",
        ["category"] = "Air Defence",
        ["infantry"] = true,
        ["vehicle"] = true,
        ["description"] = "SAM SA-18 Igla-S comm",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [56]
    [57] = 
    {
        ["type"] = "SA-18 Igla-S manpad",
        ["name"] = "SAM SA-18 Igla-S MANPADS",
        ["category"] = "Air Defence",
        ["infantry"] = true,
        ["vehicle"] = true,
        ["description"] = "SAM SA-18 Igla-S MANPADS",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [57]
    [58] = 
    {
        ["type"] = "2S6 Tunguska",
        ["name"] = "SAM SA-19 Tunguska 2S6",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-19 Tunguska 2S6",
        ["aliases"] = 
        {
            [1] = "SA-19 Tunguska 2S6",
        }, -- end of ["aliases"]
    }, -- end of [58]
    [59] = 
    {
        ["type"] = "S_75M_Volhov",
        ["name"] = "SAM SA-2 LN SM-90",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-2 LN SM-90",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [59]
    [60] = 
    {
        ["type"] = "SNR_75V",
        ["name"] = "SAM SA-2 TR SNR-75 Fan Song",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-2 TR SNR-75 Fan Song",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [60]
    [61] = 
    {
        ["type"] = "5p73 s-125 ln",
        ["name"] = "SAM SA-3 S-125 LN 5P73",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-3 S-125 LN 5P73",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [61]
    [62] = 
    {
        ["type"] = "snr s-125 tr",
        ["name"] = "SAM SA-3 S-125 TR SNR",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-3 S-125 TR SNR",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [62]
    [63] = 
    {
        ["type"] = "Kub 2P25 ln",
        ["name"] = "SAM SA-6 Kub LN 2P25",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-6 Kub LN 2P25",
        ["aliases"] = 
        {
            [1] = "SA-6 Kub LN 2P25",
        }, -- end of ["aliases"]
    }, -- end of [63]
    [64] = 
    {
        ["type"] = "Kub 1S91 str",
        ["name"] = "SAM SA-6 Kub STR 9S91",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-6 Kub STR 9S91",
        ["aliases"] = 
        {
            [1] = "SA-6 Kub STR 9S91",
        }, -- end of ["aliases"]
    }, -- end of [64]
    [65] = 
    {
        ["type"] = "Osa 9A33 ln",
        ["name"] = "SAM SA-8 Osa 9A33",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-8 Osa 9A33",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [65]
    [66] = 
    {
        ["type"] = "SA-8 Osa LD 9T217",
        ["name"] = "SAM SA-8 Osa LD 9T217",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-8 Osa LD 9T217",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [66]
    [67] = 
    {
        ["type"] = "Strela-1 9P31",
        ["name"] = "SAM SA-9 Strela-1 9P31",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SA-9 Strela-1 9P31",
        ["aliases"] = 
        {
            [1] = "SA-9 Strela-1 9P31",
        }, -- end of ["aliases"]
    }, -- end of [67]
    [68] = 
    {
        ["type"] = "p-19 s-125 sr",
        ["name"] = "SAM SR P-19",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SAM SR P-19",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [68]
    [69] = 
    {
        ["type"] = "Stinger comm",
        ["name"] = "SAM Stinger comm",
        ["category"] = "Air Defence",
        ["infantry"] = true,
        ["vehicle"] = true,
        ["description"] = "SAM Stinger comm",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [69]
    [70] = 
    {
        ["type"] = "Stinger comm dsr",
        ["name"] = "SAM Stinger comm dsr",
        ["category"] = "Air Defence",
        ["infantry"] = true,
        ["vehicle"] = true,
        ["description"] = "SAM Stinger comm dsr",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [70]
    [71] = 
    {
        ["type"] = "Gepard",
        ["name"] = "SPAAA Gepard",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SPAAA Gepard",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [71]
    [72] = 
    {
        ["type"] = "ZSU-23-4 Shilka",
        ["name"] = "SPAAA ZSU-23-4 Shilka",
        ["category"] = "Air Defence",
        ["vehicle"] = true,
        ["description"] = "SPAAA ZSU-23-4 Shilka",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [72]
    [73] = 
    {
        ["type"] = "Soldier stinger",
        ["name"] = "Stinger MANPADS",
        ["category"] = "Air Defence",
        ["infantry"] = true,
        ["vehicle"] = true,
        ["description"] = "Stinger MANPADS",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [73]
    [74] = 
    {
        ["type"] = "AAV7",
        ["name"] = "APC AAV-7",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "APC AAV-7",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [74]
    [75] = 
    {
        ["type"] = "BTR-80",
        ["name"] = "APC BTR-80",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "APC BTR-80",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [75]
    [76] = 
    {
        ["type"] = "Cobra",
        ["name"] = "APC Cobra",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "APC Cobra",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [76]
    [77] = 
    {
        ["type"] = "M1043 HMMWV Armament",
        ["name"] = "APC M1043 HMMWV Armament",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "APC M1043 HMMWV Armament",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [77]
    [78] = 
    {
        ["type"] = "M1126 Stryker ICV",
        ["name"] = "APC M1126 Stryker ICV",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "APC M1126 Stryker ICV",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [78]
    [79] = 
    {
        ["type"] = "M-113",
        ["name"] = "APC M113",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "APC M113",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [79]
    [80] = 
    {
        ["type"] = "M2A1_halftrack",
        ["name"] = "APC M2A1",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "APC M2A1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [80]
    [81] = 
    {
        ["type"] = "MTLB",
        ["name"] = "APC MTLB",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "APC MTLB",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [81]
    [82] = 
    {
        ["type"] = "Sd_Kfz_251",
        ["name"] = "APC Sd.Kfz.251",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "APC Sd.Kfz.251",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [82]
    [83] = 
    {
        ["type"] = "BRDM-2",
        ["name"] = "ARV BRDM-2",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "ARV BRDM-2",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [83]
    [84] = 
    {
        ["type"] = "BTR_D",
        ["name"] = "ARV BTR-RD",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "ARV BTR-RD",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [84]
    [85] = 
    {
        ["type"] = "M1045 HMMWV TOW",
        ["name"] = "ATGM M1045 HMMWV TOW",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "ATGM M1045 HMMWV TOW",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [85]
    [86] = 
    {
        ["type"] = "M1134 Stryker ATGM",
        ["name"] = "ATGM M1134 Stryker",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "ATGM M1134 Stryker",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [86]
    [87] = 
    {
        ["type"] = "Cromwell_IV",
        ["name"] = "CT Cromwell IV",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "CT Cromwell IV",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [87]
    [88] = 
    {
        ["type"] = "Grad_FDDM",
        ["name"] = "FDDM Grad",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "FDDM Grad",
        ["aliases"] = 
        {
            [1] = "Boman",
        }, -- end of ["aliases"]
    }, -- end of [88]
    [89] = 
    {
        ["type"] = "Churchill_VII",
        ["name"] = "HIT Churchill_VII",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "HIT Churchill_VII",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [89]
    [90] = 
    {
        ["type"] = "Tiger_II_H",
        ["name"] = "HT Pz.Kpfw.VI Ausf. B 'Tiger II'",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "HT Pz.Kpfw.VI Ausf. B 'Tiger II'",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [90]
    [91] = 
    {
        ["type"] = "Tiger_I",
        ["name"] = "HT Pz.Kpfw.VI Tiger I",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "HT Pz.Kpfw.VI Tiger I",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [91]
    [92] = 
    {
        ["type"] = "BMD-1",
        ["name"] = "IFV BMD-1",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "IFV BMD-1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [92]
    [93] = 
    {
        ["type"] = "BMP-1",
        ["name"] = "IFV BMP-1",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "IFV BMP-1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [93]
    [94] = 
    {
        ["type"] = "BMP-2",
        ["name"] = "IFV BMP-2",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "IFV BMP-2",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [94]
    [95] = 
    {
        ["type"] = "BMP-3",
        ["name"] = "IFV BMP-3",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "IFV BMP-3",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [95]
    [96] = 
    {
        ["type"] = "LAV-25",
        ["name"] = "IFV LAV-25",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "IFV LAV-25",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [96]
    [97] = 
    {
        ["type"] = "M-2 Bradley",
        ["name"] = "IFV M2A2 Bradley",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "IFV M2A2 Bradley",
        ["aliases"] = 
        {
            [1] = "M2A2 Bradley",
        }, -- end of ["aliases"]
    }, -- end of [97]
    [98] = 
    {
        ["type"] = "Marder",
        ["name"] = "IFV Marder",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "IFV Marder",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [98]
    [99] = 
    {
        ["type"] = "MCV-80",
        ["name"] = "IFV MCV-80",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "IFV MCV-80",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [99]
    [100] = 
    {
        ["type"] = "Sd_Kfz_234_2_Puma",
        ["name"] = "IFV Sd.Kfz.234/2 Puma",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "IFV Sd.Kfz.234/2 Puma",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [100]
    [101] = 
    {
        ["type"] = "M8_Greyhound",
        ["name"] = "LAC M8 Greyhound",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "LAC M8 Greyhound",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [101]
    [102] = 
    {
        ["type"] = "M30_CC",
        ["name"] = "M30 Cargo Carrier",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "M30 Cargo Carrier",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [102]
    [103] = 
    {
        ["type"] = "Challenger2",
        ["name"] = "MBT Challenger II",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "MBT Challenger II",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [103]
    [104] = 
    {
        ["type"] = "Leclerc",
        ["name"] = "MBT Leclerc",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "MBT Leclerc",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [104]
    [105] = 
    {
        ["type"] = "Leopard1A3",
        ["name"] = "MBT Leopard 1A3",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "MBT Leopard 1A3",
        ["aliases"] = 
        {
            [1] = "LEO1A3",
        }, -- end of ["aliases"]
    }, -- end of [105]
    [106] = 
    {
        ["type"] = "Leopard-2",
        ["name"] = "MBT Leopard-2",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "MBT Leopard-2",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [106]
    [107] = 
    {
        ["type"] = "M-1 Abrams",
        ["name"] = "MBT M1A2 Abrams",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "MBT M1A2 Abrams",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [107]
    [108] = 
    {
        ["type"] = "M-60",
        ["name"] = "MBT M60A3 Patton",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "MBT M60A3 Patton",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [108]
    [109] = 
    {
        ["type"] = "Merkava_Mk4",
        ["name"] = "MBT Merkava Mk. 4",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "MBT Merkava Mk. 4",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [109]
    [110] = 
    {
        ["type"] = "T-55",
        ["name"] = "MBT T-55",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "MBT T-55",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [110]
    [111] = 
    {
        ["type"] = "T-72B",
        ["name"] = "MBT T-72B",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "MBT T-72B",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [111]
    [112] = 
    {
        ["type"] = "T-80UD",
        ["name"] = "MBT T-80U",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "MBT T-80U",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [112]
    [113] = 
    {
        ["type"] = "T-90",
        ["name"] = "MBT T-90",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "MBT T-90",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [113]
    [114] = 
    {
        ["type"] = "M4_Sherman",
        ["name"] = "MT M4 Sherman",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "MT M4 Sherman",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [114]
    [115] = 
    {
        ["type"] = "M4A4_Sherman_FF",
        ["name"] = "MT M4A4 Sherman Firefly",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "MT M4A4 Sherman Firefly",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [115]
    [116] = 
    {
        ["type"] = "Pz_IV_H",
        ["name"] = "MT Pz.Kpfw.IV Ausf.H",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "MT Pz.Kpfw.IV Ausf.H",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [116]
    [117] = 
    {
        ["type"] = "Pz_V_Panther_G",
        ["name"] = "MT Pz.Kpfw.V Panther Ausf.G",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "MT Pz.Kpfw.V Panther Ausf.G",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [117]
    [118] = 
    {
        ["type"] = "Elefant_SdKfz_184",
        ["name"] = "Sd.Kfz.184 Elefant",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "Sd.Kfz.184 Elefant",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [118]
    [119] = 
    {
        ["type"] = "M1128 Stryker MGS",
        ["name"] = "SPG M1128 Stryker MGS",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "SPG M1128 Stryker MGS",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [119]
    [120] = 
    {
        ["type"] = "Centaur_IV",
        ["name"] = "ST Centaur IV",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "ST Centaur IV",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [120]
    [121] = 
    {
        ["type"] = "Stug_III",
        ["name"] = "StuG III Ausf. G",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "StuG III Ausf. G",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [121]
    [122] = 
    {
        ["type"] = "Stug_IV",
        ["name"] = "StuG IV",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "StuG IV",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [122]
    [123] = 
    {
        ["type"] = "Jagdpanther_G1",
        ["name"] = "TD Jagdpanther G1",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "TD Jagdpanther G1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [123]
    [124] = 
    {
        ["type"] = "JagdPz_IV",
        ["name"] = "TD Jagdpanzer IV",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "TD Jagdpanzer IV",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [124]
    [125] = 
    {
        ["type"] = "M10_GMC",
        ["name"] = "TD M10 GMC",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "TD M10 GMC",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [125]
    [126] = 
    {
        ["type"] = "TPZ",
        ["name"] = "TPz Fuchs",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "TPz Fuchs",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [126]
    [127] = 
    {
        ["type"] = "ZBD04A",
        ["name"] = "ZBD-04A",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "ZBD-04A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [127]
    [128] = 
    {
        ["type"] = "ZTZ96B",
        ["name"] = "ZTZ-96B",
        ["category"] = "Armor",
        ["vehicle"] = true,
        ["description"] = "ZTZ-96B",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [128]
    [129] = 
    {
        ["type"] = "2B11 mortar",
        ["name"] = "2B11 mortar",
        ["category"] = "Artillery",
        ["vehicle"] = true,
        ["description"] = "2B11 mortar",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [129]
    [130] = 
    {
        ["type"] = "M12_GMC",
        ["name"] = "M12 GMC",
        ["category"] = "Artillery",
        ["vehicle"] = true,
        ["description"] = "M12 GMC",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [130]
    [131] = 
    {
        ["type"] = "Smerch",
        ["name"] = "MLRS 9A52 Smerch",
        ["category"] = "Artillery",
        ["vehicle"] = true,
        ["description"] = "MLRS 9A52 Smerch",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [131]
    [132] = 
    {
        ["type"] = "Uragan_BM-27",
        ["name"] = "MLRS 9K57 Uragan BM-27",
        ["category"] = "Artillery",
        ["vehicle"] = true,
        ["description"] = "MLRS 9K57 Uragan BM-27",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [132]
    [133] = 
    {
        ["type"] = "Grad-URAL",
        ["name"] = "MLRS BM-21 Grad",
        ["category"] = "Artillery",
        ["vehicle"] = true,
        ["description"] = "MLRS BM-21 Grad",
        ["aliases"] = 
        {
            [1] = "MLRS BM-21 Grad",
        }, -- end of ["aliases"]
    }, -- end of [133]
    [134] = 
    {
        ["type"] = "MLRS FDDM",
        ["name"] = "MLRS FDDM",
        ["category"] = "Artillery",
        ["vehicle"] = true,
        ["description"] = "MLRS FDDM",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [134]
    [135] = 
    {
        ["type"] = "MLRS",
        ["name"] = "MLRS M270",
        ["category"] = "Artillery",
        ["vehicle"] = true,
        ["description"] = "MLRS M270",
        ["aliases"] = 
        {
            [1] = "M270 MLRS",
        }, -- end of ["aliases"]
    }, -- end of [135]
    [136] = 
    {
        ["type"] = "SpGH_Dana",
        ["name"] = "SpGH Dana",
        ["category"] = "Artillery",
        ["vehicle"] = true,
        ["description"] = "SpGH Dana",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [136]
    [137] = 
    {
        ["type"] = "SAU Gvozdika",
        ["name"] = "SPH 2S1 Gvozdika",
        ["category"] = "Artillery",
        ["vehicle"] = true,
        ["description"] = "SPH 2S1 Gvozdika",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [137]
    [138] = 
    {
        ["type"] = "SAU Msta",
        ["name"] = "SPH 2S19 Msta",
        ["category"] = "Artillery",
        ["vehicle"] = true,
        ["description"] = "SPH 2S19 Msta",
        ["aliases"] = 
        {
            [1] = "2S19 Msta",
        }, -- end of ["aliases"]
    }, -- end of [138]
    [139] = 
    {
        ["type"] = "SAU Akatsia",
        ["name"] = "SPH 2S3 Akatsia",
        ["category"] = "Artillery",
        ["vehicle"] = true,
        ["description"] = "SPH 2S3 Akatsia",
        ["aliases"] = 
        {
            [1] = "2S3 Akatsia",
        }, -- end of ["aliases"]
    }, -- end of [139]
    [140] = 
    {
        ["type"] = "SAU 2-C9",
        ["name"] = "SPH 2S9 Nona",
        ["category"] = "Artillery",
        ["vehicle"] = true,
        ["description"] = "SPH 2S9 Nona",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [140]
    [141] = 
    {
        ["type"] = "M-109",
        ["name"] = "SPH M109 Paladin",
        ["category"] = "Artillery",
        ["vehicle"] = true,
        ["description"] = "SPH M109 Paladin",
        ["aliases"] = 
        {
            [1] = "M109",
        }, -- end of ["aliases"]
    }, -- end of [141]
    [142] = 
    {
        ["type"] = "SturmPzIV",
        ["name"] = "Sturmpanzer IV Brummbär",
        ["category"] = "Artillery",
        ["vehicle"] = true,
        ["description"] = "Sturmpanzer IV Brummbär",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [142]
    [143] = 
    {
        ["type"] = "ammo_cargo",
        ["name"] = "Ammo",
        ["category"] = "Cargo",
        ["description"] = "Ammo",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [143]
    [144] = 
    {
        ["type"] = "barrels_cargo",
        ["name"] = "Barrels",
        ["category"] = "Cargo",
        ["description"] = "Barrels",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [144]
    [145] = 
    {
        ["type"] = "container_cargo",
        ["name"] = "Container",
        ["category"] = "Cargo",
        ["description"] = "Container",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [145]
    [146] = 
    {
        ["type"] = "f_bar_cargo",
        ["name"] = "F-shape barrier",
        ["category"] = "Cargo",
        ["description"] = "F-shape barrier",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [146]
    [147] = 
    {
        ["type"] = "fueltank_cargo",
        ["name"] = "Fueltank",
        ["category"] = "Cargo",
        ["description"] = "Fueltank",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [147]
    [148] = 
    {
        ["type"] = "iso_container",
        ["name"] = "ISO container",
        ["category"] = "Cargo",
        ["description"] = "ISO container",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [148]
    [149] = 
    {
        ["type"] = "iso_container_small",
        ["name"] = "ISO container small",
        ["category"] = "Cargo",
        ["description"] = "ISO container small",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [149]
    [150] = 
    {
        ["type"] = "m117_cargo",
        ["name"] = "M117 bombs",
        ["category"] = "Cargo",
        ["description"] = "M117 bombs",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [150]
    [151] = 
    {
        ["type"] = "oiltank_cargo",
        ["name"] = "Oiltank",
        ["category"] = "Cargo",
        ["description"] = "Oiltank",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [151]
    [152] = 
    {
        ["type"] = "pipes_big_cargo",
        ["name"] = "Pipes big",
        ["category"] = "Cargo",
        ["description"] = "Pipes big",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [152]
    [153] = 
    {
        ["type"] = "pipes_small_cargo",
        ["name"] = "Pipes small",
        ["category"] = "Cargo",
        ["description"] = "Pipes small",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [153]
    [154] = 
    {
        ["type"] = "tetrapod_cargo",
        ["name"] = "Tetrapod",
        ["category"] = "Cargo",
        ["description"] = "Tetrapod",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [154]
    [155] = 
    {
        ["type"] = "trunks_long_cargo",
        ["name"] = "Trunks long",
        ["category"] = "Cargo",
        ["description"] = "Trunks long",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [155]
    [156] = 
    {
        ["type"] = "trunks_small_cargo",
        ["name"] = "Trunks short",
        ["category"] = "Cargo",
        ["description"] = "Trunks short",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [156]
    [157] = 
    {
        ["type"] = "uh1h_cargo",
        ["name"] = "UH-1H cargo",
        ["category"] = "Cargo",
        ["description"] = "UH-1H cargo",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [157]
    [158] = 
    {
        ["type"] = "Boxcartrinity",
        ["name"] = "Boxcartrinity",
        ["category"] = "Carriage",
        ["vehicle"] = true,
        ["description"] = "Boxcartrinity",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [158]
    [159] = 
    {
        ["type"] = "Coach a tank blue",
        ["name"] = "Coach a tank blue",
        ["category"] = "Carriage",
        ["vehicle"] = true,
        ["description"] = "Coach a tank blue",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [159]
    [160] = 
    {
        ["type"] = "Coach a tank yellow",
        ["name"] = "Coach a tank yellow",
        ["category"] = "Carriage",
        ["vehicle"] = true,
        ["description"] = "Coach a tank yellow",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [160]
    [161] = 
    {
        ["type"] = "Coach a platform",
        ["name"] = "Coach flatbed",
        ["category"] = "Carriage",
        ["vehicle"] = true,
        ["description"] = "Coach flatbed",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [161]
    [162] = 
    {
        ["type"] = "Coach cargo",
        ["name"] = "Coach for cargo",
        ["category"] = "Carriage",
        ["vehicle"] = true,
        ["description"] = "Coach for cargo",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [162]
    [163] = 
    {
        ["type"] = "Coach cargo open",
        ["name"] = "Coach for open cargo",
        ["category"] = "Carriage",
        ["vehicle"] = true,
        ["description"] = "Coach for open cargo",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [163]
    [164] = 
    {
        ["type"] = "Coach a passenger",
        ["name"] = "Coach for passengers",
        ["category"] = "Carriage",
        ["vehicle"] = true,
        ["description"] = "Coach for passengers",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [164]
    [165] = 
    {
        ["type"] = "DR_50Ton_Flat_Wagon",
        ["name"] = "DR 50-ton flat wagon",
        ["category"] = "Carriage",
        ["vehicle"] = true,
        ["description"] = "DR 50-ton flat wagon",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [165]
    [166] = 
    {
        ["type"] = "German_covered_wagon_G10",
        ["name"] = "German covered wagon G10",
        ["category"] = "Carriage",
        ["vehicle"] = true,
        ["description"] = "German covered wagon G10",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [166]
    [167] = 
    {
        ["type"] = "German_tank_wagon",
        ["name"] = "German tank wagon",
        ["category"] = "Carriage",
        ["vehicle"] = true,
        ["description"] = "German tank wagon",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [167]
    [168] = 
    {
        ["type"] = "Tankcartrinity",
        ["name"] = "Tankcartrinity",
        ["category"] = "Carriage",
        ["vehicle"] = true,
        ["description"] = "Tankcartrinity",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [168]
    [169] = 
    {
        ["type"] = "Wellcarnsc",
        ["name"] = "Wellcarnsc",
        ["category"] = "Carriage",
        ["vehicle"] = true,
        ["description"] = "Wellcarnsc",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [169]
    [170] = 
    {
        ["type"] = "Airshow_Cone",
        ["name"] = "Airshow cone",
        ["category"] = "Fortification",
        ["description"] = "Airshow cone",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [170]
    [171] = 
    {
        ["type"] = "Airshow_Crowd",
        ["name"] = "Airshow Crowd",
        ["category"] = "Fortification",
        ["description"] = "Airshow Crowd",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [171]
    [172] = 
    {
        ["type"] = "houseA_arm",
        ["name"] = "Armed house",
        ["category"] = "Fortification",
        ["description"] = "Armed house",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [172]
    [173] = 
    {
        ["type"] = "Barracks 2",
        ["name"] = "Barracks 2",
        ["category"] = "Fortification",
        ["description"] = "Barracks 2",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [173]
    [174] = 
    {
        ["type"] = "house1arm",
        ["name"] = "Barracks armed",
        ["category"] = "Fortification",
        ["description"] = "Barracks armed",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [174]
    [175] = 
    {
        ["type"] = "Belgian gate",
        ["name"] = "Belgian gate",
        ["category"] = "Fortification",
        ["description"] = "Belgian gate",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [175]
    [176] = 
    {
        ["type"] = "Boiler-house A",
        ["name"] = "Boiler-house A",
        ["category"] = "Fortification",
        ["description"] = "Boiler-house A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [176]
    [177] = 
    {
        ["type"] = "Sandbox",
        ["name"] = "Bunker 1",
        ["category"] = "Fortification",
        ["description"] = "Bunker 1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [177]
    [178] = 
    {
        ["type"] = "Bunker",
        ["name"] = "Bunker 2",
        ["category"] = "Fortification",
        ["description"] = "Bunker 2",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [178]
    [179] = 
    {
        ["type"] = "SK_C_28_naval_gun",
        ["name"] = "Bunker with SK C/28 15cm naval gun",
        ["category"] = "Fortification",
        ["vehicle"] = true,
        ["description"] = "Bunker with SK C/28 15cm naval gun",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [179]
    [180] = 
    {
        ["type"] = "Cafe",
        ["name"] = "Cafe",
        ["category"] = "Fortification",
        ["description"] = "Cafe",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [180]
    [181] = 
    {
        ["type"] = "Chemical tank A",
        ["name"] = "Chemical tank A",
        ["category"] = "Fortification",
        ["description"] = "Chemical tank A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [181]
    [182] = 
    {
        ["type"] = ".Command Center",
        ["name"] = "Command Center",
        ["category"] = "Fortification",
        ["description"] = "Command Center",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [182]
    [183] = 
    {
        ["type"] = "Comms tower M",
        ["name"] = "Comms tower M",
        ["category"] = "Fortification",
        ["description"] = "Comms tower M",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [183]
    [184] = 
    {
        ["type"] = "Concertina wire",
        ["name"] = "Concertina wire",
        ["category"] = "Fortification",
        ["description"] = "Concertina wire",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [184]
    [185] = 
    {
        ["type"] = "Container brown",
        ["name"] = "Container brown",
        ["category"] = "Fortification",
        ["description"] = "Container brown",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [185]
    [186] = 
    {
        ["type"] = "Container red 1",
        ["name"] = "Container red 1",
        ["category"] = "Fortification",
        ["description"] = "Container red 1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [186]
    [187] = 
    {
        ["type"] = "Container red 2",
        ["name"] = "Container red 2",
        ["category"] = "Fortification",
        ["description"] = "Container red 2",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [187]
    [188] = 
    {
        ["type"] = "Container red 3",
        ["name"] = "Container red 3",
        ["category"] = "Fortification",
        ["description"] = "Container red 3",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [188]
    [189] = 
    {
        ["type"] = "Container white",
        ["name"] = "Container white",
        ["category"] = "Fortification",
        ["description"] = "Container white",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [189]
    [190] = 
    {
        ["type"] = "Czech hedgehogs 1",
        ["name"] = "Czech hedgehogs 1",
        ["category"] = "Fortification",
        ["description"] = "Czech hedgehogs 1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [190]
    [191] = 
    {
        ["type"] = "Czech hedgehogs 2",
        ["name"] = "Czech hedgehogs 2",
        ["category"] = "Fortification",
        ["description"] = "Czech hedgehogs 2",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [191]
    [192] = 
    {
        ["type"] = "Dragonteeth 1",
        ["name"] = "Dragonteeth 1",
        ["category"] = "Fortification",
        ["description"] = "Dragonteeth 1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [192]
    [193] = 
    {
        ["type"] = "Dragonteeth 2",
        ["name"] = "Dragonteeth 2",
        ["category"] = "Fortification",
        ["description"] = "Dragonteeth 2",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [193]
    [194] = 
    {
        ["type"] = "Dragonteeth 3",
        ["name"] = "Dragonteeth 3",
        ["category"] = "Fortification",
        ["description"] = "Dragonteeth 3",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [194]
    [195] = 
    {
        ["type"] = "Dragonteeth 4",
        ["name"] = "Dragonteeth 4",
        ["category"] = "Fortification",
        ["description"] = "Dragonteeth 4",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [195]
    [196] = 
    {
        ["type"] = "Dragonteeth 5",
        ["name"] = "Dragonteeth 5",
        ["category"] = "Fortification",
        ["description"] = "Dragonteeth 5",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [196]
    [197] = 
    {
        ["type"] = "Electric power box",
        ["name"] = "Electric power box",
        ["category"] = "Fortification",
        ["description"] = "Electric power box",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [197]
    [198] = 
    {
        ["type"] = "Farm A",
        ["name"] = "Farm A",
        ["category"] = "Fortification",
        ["description"] = "Farm A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [198]
    [199] = 
    {
        ["type"] = "Farm B",
        ["name"] = "Farm B",
        ["category"] = "Fortification",
        ["description"] = "Farm B",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [199]
    [200] = 
    {
        ["type"] = "FARP Ammo Dump Coating",
        ["name"] = "FARP Ammo Storage",
        ["category"] = "Fortification",
        ["description"] = "FARP Ammo Storage",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [200]
    [201] = 
    {
        ["type"] = "FARP CP Blindage",
        ["name"] = "FARP Command Post",
        ["category"] = "Fortification",
        ["description"] = "FARP Command Post",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [201]
    [202] = 
    {
        ["type"] = "FARP Fuel Depot",
        ["name"] = "FARP Fuel Depot",
        ["category"] = "Fortification",
        ["description"] = "FARP Fuel Depot",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [202]
    [203] = 
    {
        ["type"] = "FARP Tent",
        ["name"] = "FARP Tent",
        ["category"] = "Fortification",
        ["description"] = "FARP Tent",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [203]
    [204] = 
    {
        ["type"] = "fire_control",
        ["name"] = "Fire control bunker",
        ["category"] = "Fortification",
        ["description"] = "Fire control bunker",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [204]
    [205] = 
    {
        ["type"] = "Fire Control Bunker",
        ["name"] = "Fire control bunker",
        ["category"] = "Fortification",
        ["description"] = "Fire control bunker",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [205]
    [206] = 
    {
        ["type"] = "Fuel tank",
        ["name"] = "Fuel tank",
        ["category"] = "Fortification",
        ["description"] = "Fuel tank",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [206]
    [207] = 
    {
        ["type"] = "Garage A",
        ["name"] = "Garage A",
        ["category"] = "Fortification",
        ["description"] = "Garage A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [207]
    [208] = 
    {
        ["type"] = "Garage B",
        ["name"] = "Garage B",
        ["category"] = "Fortification",
        ["description"] = "Garage B",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [208]
    [209] = 
    {
        ["type"] = "Garage small A",
        ["name"] = "Garage small A",
        ["category"] = "Fortification",
        ["description"] = "Garage small A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [209]
    [210] = 
    {
        ["type"] = "Garage small B",
        ["name"] = "Garage small B",
        ["category"] = "Fortification",
        ["description"] = "Garage small B",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [210]
    [211] = 
    {
        ["type"] = "GeneratorF",
        ["name"] = "GeneratorF",
        ["category"] = "Fortification",
        ["description"] = "GeneratorF",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [211]
    [212] = 
    {
        ["type"] = "Hangar A",
        ["name"] = "Hangar A",
        ["category"] = "Fortification",
        ["description"] = "Hangar A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [212]
    [213] = 
    {
        ["type"] = "Hangar B",
        ["name"] = "Hangar B",
        ["category"] = "Fortification",
        ["description"] = "Hangar B",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [213]
    [214] = 
    {
        ["type"] = "Haystack 1",
        ["name"] = "Haystack 1",
        ["category"] = "Fortification",
        ["description"] = "Haystack 1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [214]
    [215] = 
    {
        ["type"] = "Haystack 2",
        ["name"] = "Haystack 2",
        ["category"] = "Fortification",
        ["description"] = "Haystack 2",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [215]
    [216] = 
    {
        ["type"] = "Haystack 3",
        ["name"] = "Haystack 3",
        ["category"] = "Fortification",
        ["description"] = "Haystack 3",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [216]
    [217] = 
    {
        ["type"] = "Haystack 4",
        ["name"] = "Haystack 4",
        ["category"] = "Fortification",
        ["description"] = "Haystack 4",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [217]
    [218] = 
    {
        ["type"] = "Hemmkurvenhindernis",
        ["name"] = "Hemmkurvenhindernis",
        ["category"] = "Fortification",
        ["description"] = "Hemmkurvenhindernis",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [218]
    [219] = 
    {
        ["type"] = "Landmine",
        ["name"] = "Landmine",
        ["category"] = "Fortification",
        ["description"] = "Landmine",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [219]
    [220] = 
    {
        ["type"] = "Log posts 1",
        ["name"] = "Log posts 1",
        ["category"] = "Fortification",
        ["description"] = "Log posts 1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [220]
    [221] = 
    {
        ["type"] = "Log posts 2",
        ["name"] = "Log posts 2",
        ["category"] = "Fortification",
        ["description"] = "Log posts 2",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [221]
    [222] = 
    {
        ["type"] = "Log posts 3",
        ["name"] = "Log posts 3",
        ["category"] = "Fortification",
        ["description"] = "Log posts 3",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [222]
    [223] = 
    {
        ["type"] = "Log ramps 1",
        ["name"] = "Log ramps 1",
        ["category"] = "Fortification",
        ["description"] = "Log ramps 1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [223]
    [224] = 
    {
        ["type"] = "Log ramps 2",
        ["name"] = "Log ramps 2",
        ["category"] = "Fortification",
        ["description"] = "Log ramps 2",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [224]
    [225] = 
    {
        ["type"] = "Log ramps 3",
        ["name"] = "Log ramps 3",
        ["category"] = "Fortification",
        ["description"] = "Log ramps 3",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [225]
    [226] = 
    {
        ["type"] = "Red_Flag",
        ["name"] = "Mark Flag Red",
        ["category"] = "Fortification",
        ["description"] = "Mark Flag Red",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [226]
    [227] = 
    {
        ["type"] = "White_Flag",
        ["name"] = "Mark Flag White",
        ["category"] = "Fortification",
        ["description"] = "Mark Flag White",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [227]
    [228] = 
    {
        ["type"] = "Black_Tyre",
        ["name"] = "Mark Tyre Black",
        ["category"] = "Fortification",
        ["description"] = "Mark Tyre Black",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [228]
    [229] = 
    {
        ["type"] = "White_Tyre",
        ["name"] = "Mark Tyre White",
        ["category"] = "Fortification",
        ["description"] = "Mark Tyre White",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [229]
    [230] = 
    {
        ["type"] = "Black_Tyre_RF",
        ["name"] = "Mark Tyre with Red Flag",
        ["category"] = "Fortification",
        ["description"] = "Mark Tyre with Red Flag",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [230]
    [231] = 
    {
        ["type"] = "Black_Tyre_WF",
        ["name"] = "Mark Tyre with White Flag",
        ["category"] = "Fortification",
        ["description"] = "Mark Tyre with White Flag",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [231]
    [232] = 
    {
        ["type"] = "Military staff",
        ["name"] = "Military staff",
        ["category"] = "Fortification",
        ["description"] = "Military staff",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [232]
    [233] = 
    {
        ["type"] = "Oil derrick",
        ["name"] = "Oil derrick",
        ["category"] = "Fortification",
        ["description"] = "Oil derrick",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [233]
    [234] = 
    {
        ["type"] = "Oil platform",
        ["name"] = "Oil platform",
        ["category"] = "Fortification",
        ["description"] = "Oil platform",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [234]
    [235] = 
    {
        ["type"] = "outpost",
        ["name"] = "Outpost",
        ["category"] = "Fortification",
        ["description"] = "Outpost",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [235]
    [236] = 
    {
        ["type"] = "Pump station",
        ["name"] = "Pump station",
        ["category"] = "Fortification",
        ["description"] = "Pump station",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [236]
    [237] = 
    {
        ["type"] = "Railway crossing A",
        ["name"] = "Railway crossing A",
        ["category"] = "Fortification",
        ["description"] = "Railway crossing A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [237]
    [238] = 
    {
        ["type"] = "Railway crossing B",
        ["name"] = "Railway crossing B",
        ["category"] = "Fortification",
        ["description"] = "Railway crossing B",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [238]
    [239] = 
    {
        ["type"] = "Railway station",
        ["name"] = "Railway station",
        ["category"] = "Fortification",
        ["description"] = "Railway station",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [239]
    [240] = 
    {
        ["type"] = "Repair workshop",
        ["name"] = "Repair workshop",
        ["category"] = "Fortification",
        ["description"] = "Repair workshop",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [240]
    [241] = 
    {
        ["type"] = "Restaurant 1",
        ["name"] = "Restaurant 1",
        ["category"] = "Fortification",
        ["description"] = "Restaurant 1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [241]
    [242] = 
    {
        ["type"] = "outpost_road",
        ["name"] = "Road outpost",
        ["category"] = "Fortification",
        ["description"] = "Road outpost",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [242]
    [243] = 
    {
        ["type"] = "Shelter",
        ["name"] = "Shelter",
        ["category"] = "Fortification",
        ["description"] = "Shelter",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [243]
    [244] = 
    {
        ["type"] = "Shelter B",
        ["name"] = "Shelter B",
        ["category"] = "Fortification",
        ["description"] = "Shelter B",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [244]
    [245] = 
    {
        ["type"] = "Shop",
        ["name"] = "Shop",
        ["category"] = "Fortification",
        ["description"] = "Shop",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [245]
    [246] = 
    {
        ["type"] = "Siegfried Line",
        ["name"] = "Siegfried line",
        ["category"] = "Fortification",
        ["description"] = "Siegfried line",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [246]
    [247] = 
    {
        ["type"] = "Small house 1A",
        ["name"] = "Small house 1A",
        ["category"] = "Fortification",
        ["description"] = "Small house 1A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [247]
    [248] = 
    {
        ["type"] = "Small house 1A area",
        ["name"] = "Small house 1A area",
        ["category"] = "Fortification",
        ["description"] = "Small house 1A area",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [248]
    [249] = 
    {
        ["type"] = "Small house 1B",
        ["name"] = "Small house 1B",
        ["category"] = "Fortification",
        ["description"] = "Small house 1B",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [249]
    [250] = 
    {
        ["type"] = "Small house 1B area",
        ["name"] = "Small house 1B area",
        ["category"] = "Fortification",
        ["description"] = "Small house 1B area",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [250]
    [251] = 
    {
        ["type"] = "Small house 1C area",
        ["name"] = "Small house 1C area",
        ["category"] = "Fortification",
        ["description"] = "Small house 1C area",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [251]
    [252] = 
    {
        ["type"] = "Small house 2C",
        ["name"] = "Small house 2C",
        ["category"] = "Fortification",
        ["description"] = "Small house 2C",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [252]
    [253] = 
    {
        ["type"] = "Small werehouse 1",
        ["name"] = "Small warehouse 1",
        ["category"] = "Fortification",
        ["description"] = "Small warehouse 1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [253]
    [254] = 
    {
        ["type"] = "Small werehouse 2",
        ["name"] = "Small warehouse 2",
        ["category"] = "Fortification",
        ["description"] = "Small warehouse 2",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [254]
    [255] = 
    {
        ["type"] = "Small werehouse 3",
        ["name"] = "Small warehouse 3",
        ["category"] = "Fortification",
        ["description"] = "Small warehouse 3",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [255]
    [256] = 
    {
        ["type"] = "Small werehouse 4",
        ["name"] = "Small warehouse 4",
        ["category"] = "Fortification",
        ["description"] = "Small warehouse 4",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [256]
    [257] = 
    {
        ["type"] = "Subsidiary structure 1",
        ["name"] = "Subsidiary structure 1",
        ["category"] = "Fortification",
        ["description"] = "Subsidiary structure 1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [257]
    [258] = 
    {
        ["type"] = "Subsidiary structure 2",
        ["name"] = "Subsidiary structure 2",
        ["category"] = "Fortification",
        ["description"] = "Subsidiary structure 2",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [258]
    [259] = 
    {
        ["type"] = "Subsidiary structure 3",
        ["name"] = "Subsidiary structure 3",
        ["category"] = "Fortification",
        ["description"] = "Subsidiary structure 3",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [259]
    [260] = 
    {
        ["type"] = "Subsidiary structure A",
        ["name"] = "Subsidiary structure A",
        ["category"] = "Fortification",
        ["description"] = "Subsidiary structure A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [260]
    [261] = 
    {
        ["type"] = "Subsidiary structure B",
        ["name"] = "Subsidiary structure B",
        ["category"] = "Fortification",
        ["description"] = "Subsidiary structure B",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [261]
    [262] = 
    {
        ["type"] = "Subsidiary structure C",
        ["name"] = "Subsidiary structure C",
        ["category"] = "Fortification",
        ["description"] = "Subsidiary structure C",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [262]
    [263] = 
    {
        ["type"] = "Subsidiary structure D",
        ["name"] = "Subsidiary structure D",
        ["category"] = "Fortification",
        ["description"] = "Subsidiary structure D",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [263]
    [264] = 
    {
        ["type"] = "Subsidiary structure E",
        ["name"] = "Subsidiary structure E",
        ["category"] = "Fortification",
        ["description"] = "Subsidiary structure E",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [264]
    [265] = 
    {
        ["type"] = "Subsidiary structure F",
        ["name"] = "Subsidiary structure F",
        ["category"] = "Fortification",
        ["description"] = "Subsidiary structure F",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [265]
    [266] = 
    {
        ["type"] = "Subsidiary structure G",
        ["name"] = "Subsidiary structure G",
        ["category"] = "Fortification",
        ["description"] = "Subsidiary structure G",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [266]
    [267] = 
    {
        ["type"] = "Supermarket A",
        ["name"] = "Supermarket A",
        ["category"] = "Fortification",
        ["description"] = "Supermarket A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [267]
    [268] = 
    {
        ["type"] = "TACAN_beacon",
        ["name"] = "TACAN Beacon (Man Portable) TTS 3030",
        ["category"] = "Fortification",
        ["description"] = "TACAN Beacon (Man Portable) TTS 3030",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [268]
    [269] = 
    {
        ["type"] = "Tech combine",
        ["name"] = "Tech combine",
        ["category"] = "Fortification",
        ["description"] = "Tech combine",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [269]
    [270] = 
    {
        ["type"] = "Tech hangar A",
        ["name"] = "Tech hangar A",
        ["category"] = "Fortification",
        ["description"] = "Tech hangar A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [270]
    [271] = 
    {
        ["type"] = "Tetrahydra",
        ["name"] = "Tetrahydra",
        ["category"] = "Fortification",
        ["description"] = "Tetrahydra",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [271]
    [272] = 
    {
        ["type"] = "TV tower",
        ["name"] = "TV tower",
        ["category"] = "Fortification",
        ["description"] = "TV tower",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [272]
    [273] = 
    {
        ["type"] = "house2arm",
        ["name"] = "Watch tower armed",
        ["category"] = "Fortification",
        ["description"] = "Watch tower armed",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [273]
    [274] = 
    {
        ["type"] = "Water tower A",
        ["name"] = "Water tower A",
        ["category"] = "Fortification",
        ["description"] = "Water tower A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [274]
    [275] = 
    {
        ["type"] = "WC",
        ["name"] = "WC",
        ["category"] = "Fortification",
        ["description"] = "WC",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [275]
    [276] = 
    {
        ["type"] = "Windsock",
        ["name"] = "Windsock",
        ["category"] = "Fortification",
        ["description"] = "Windsock",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [276]
    [277] = 
    {
        ["type"] = "Workshop A",
        ["name"] = "Workshop A",
        ["category"] = "Fortification",
        ["description"] = "Workshop A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [277]
    [278] = 
    {
        ["type"] = "Bridge",
        ["name"] = "Bridge",
        ["category"] = "GroundObject",
        ["description"] = "Bridge",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [278]
    [279] = 
    {
        ["type"] = "Building",
        ["name"] = "Building",
        ["category"] = "GroundObject",
        ["description"] = "Building",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [279]
    [280] = 
    {
        ["type"] = "Train",
        ["name"] = "Train",
        ["category"] = "GroundObject",
        ["description"] = "Train",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [280]
    [281] = 
    {
        ["type"] = "Transport",
        ["name"] = "Transport",
        ["category"] = "GroundObject",
        ["description"] = "Transport",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [281]
    [282] = 
    {
        ["air"] = true,
        ["type"] = "AH-1W",
        ["name"] = "AH-1W",
        ["category"] = "Helicopter",
        ["description"] = "AH-1W",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [282]
    [283] = 
    {
        ["air"] = true,
        ["type"] = "AH-64A",
        ["name"] = "AH-64A",
        ["category"] = "Helicopter",
        ["description"] = "AH-64A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [283]
    [284] = 
    {
        ["air"] = true,
        ["type"] = "AH-64D",
        ["name"] = "AH-64D",
        ["category"] = "Helicopter",
        ["description"] = "AH-64D",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [284]
    [285] = 
    {
        ["air"] = true,
        ["type"] = "CH-47D",
        ["name"] = "CH-47D",
        ["category"] = "Helicopter",
        ["description"] = "CH-47D",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [285]
    [286] = 
    {
        ["air"] = true,
        ["type"] = "CH-53E",
        ["name"] = "CH-53E",
        ["category"] = "Helicopter",
        ["description"] = "CH-53E",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [286]
    [287] = 
    {
        ["air"] = true,
        ["type"] = "Ka-27",
        ["name"] = "Ka-27",
        ["category"] = "Helicopter",
        ["description"] = "Ka-27",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [287]
    [288] = 
    {
        ["air"] = true,
        ["type"] = "Ka-50",
        ["name"] = "Ka-50",
        ["category"] = "Helicopter",
        ["description"] = "Ka-50",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [288]
    [289] = 
    {
        ["air"] = true,
        ["type"] = "Ka-52",
        ["name"] = "Ka-52",
        ["category"] = "Helicopter",
        ["description"] = "Ka-52",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [289]
    [290] = 
    {
        ["air"] = true,
        ["type"] = "Mi-24V",
        ["name"] = "Mi-24V",
        ["category"] = "Helicopter",
        ["description"] = "Mi-24V",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [290]
    [291] = 
    {
        ["air"] = true,
        ["type"] = "Mi-26",
        ["name"] = "Mi-26",
        ["category"] = "Helicopter",
        ["description"] = "Mi-26",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [291]
    [292] = 
    {
        ["air"] = true,
        ["type"] = "Mi-28N",
        ["name"] = "Mi-28N",
        ["category"] = "Helicopter",
        ["description"] = "Mi-28N",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [292]
    [293] = 
    {
        ["air"] = true,
        ["type"] = "Mi-8MT",
        ["name"] = "Mi-8MTV2",
        ["category"] = "Helicopter",
        ["description"] = "Mi-8MTV2",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [293]
    [294] = 
    {
        ["air"] = true,
        ["type"] = "OH-58D",
        ["name"] = "OH-58D",
        ["category"] = "Helicopter",
        ["description"] = "OH-58D",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [294]
    [295] = 
    {
        ["air"] = true,
        ["type"] = "SA342L",
        ["name"] = "SA342L",
        ["category"] = "Helicopter",
        ["description"] = "SA342L",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [295]
    [296] = 
    {
        ["air"] = true,
        ["type"] = "SA342M",
        ["name"] = "SA342M",
        ["category"] = "Helicopter",
        ["description"] = "SA342M",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [296]
    [297] = 
    {
        ["air"] = true,
        ["type"] = "SA342Minigun",
        ["name"] = "SA342Minigun",
        ["category"] = "Helicopter",
        ["description"] = "SA342Minigun",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [297]
    [298] = 
    {
        ["air"] = true,
        ["type"] = "SA342Mistral",
        ["name"] = "SA342Mistral",
        ["category"] = "Helicopter",
        ["description"] = "SA342Mistral",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [298]
    [299] = 
    {
        ["air"] = true,
        ["type"] = "SH-3W",
        ["name"] = "SH-3W",
        ["category"] = "Helicopter",
        ["description"] = "SH-3W",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [299]
    [300] = 
    {
        ["air"] = true,
        ["type"] = "SH-60B",
        ["name"] = "SH-60B",
        ["category"] = "Helicopter",
        ["description"] = "SH-60B",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [300]
    [301] = 
    {
        ["air"] = true,
        ["type"] = "UH-1H",
        ["name"] = "UH-1H",
        ["category"] = "Helicopter",
        ["description"] = "UH-1H",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [301]
    [302] = 
    {
        ["air"] = true,
        ["type"] = "UH-60A",
        ["name"] = "UH-60A",
        ["category"] = "Helicopter",
        ["description"] = "UH-60A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [302]
    [303] = 
    {
        ["type"] = "Soldier M4 GRG",
        ["name"] = "Georgian soldier with M4",
        ["category"] = "Infantry",
        ["infantry"] = true,
        ["description"] = "Georgian soldier with M4",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [303]
    [304] = 
    {
        ["type"] = "soldier_wwii_us",
        ["name"] = "Infantry M1 Garand",
        ["category"] = "Infantry",
        ["infantry"] = true,
        ["description"] = "Infantry M1 Garand",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [304]
    [305] = 
    {
        ["type"] = "Soldier M4",
        ["name"] = "Infantry M4",
        ["category"] = "Infantry",
        ["infantry"] = true,
        ["description"] = "Infantry M4",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [305]
    [306] = 
    {
        ["type"] = "soldier_mauser98",
        ["name"] = "Infantry Mauser 98",
        ["category"] = "Infantry",
        ["infantry"] = true,
        ["description"] = "Infantry Mauser 98",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [306]
    [307] = 
    {
        ["type"] = "soldier_wwii_br_01",
        ["name"] = "Infantry SMLE No.4 Mk-1",
        ["category"] = "Infantry",
        ["infantry"] = true,
        ["description"] = "Infantry SMLE No.4 Mk-1",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [307]
    [308] = 
    {
        ["type"] = "Infantry AK Ins",
        ["name"] = "Infantry Soldier Insurgents",
        ["category"] = "Infantry",
        ["infantry"] = true,
        ["description"] = "Infantry Soldier Insurgents",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [308]
    [309] = 
    {
        ["type"] = "Infantry AK",
        ["name"] = "Infantry Soldier Rus",
        ["category"] = "Infantry",
        ["infantry"] = true,
        ["description"] = "Infantry Soldier Rus",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [309]
    [310] = 
    {
        ["type"] = "Paratrooper AKS-74",
        ["name"] = "Paratrooper AKS",
        ["category"] = "Infantry",
        ["infantry"] = true,
        ["description"] = "Paratrooper AKS",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [310]
    [311] = 
    {
        ["type"] = "Paratrooper RPG-16",
        ["name"] = "Paratrooper RPG-16",
        ["category"] = "Infantry",
        ["infantry"] = true,
        ["description"] = "Paratrooper RPG-16",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [311]
    [312] = 
    {
        ["type"] = "Soldier AK",
        ["name"] = "Soldier AK",
        ["category"] = "Infantry",
        ["infantry"] = true,
        ["description"] = "Soldier AK",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [312]
    [313] = 
    {
        ["type"] = "Soldier M249",
        ["name"] = "Soldier M249",
        ["category"] = "Infantry",
        ["infantry"] = true,
        ["description"] = "Soldier M249",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [313]
    [314] = 
    {
        ["type"] = "Soldier RPG",
        ["name"] = "Soldier RPG",
        ["category"] = "Infantry",
        ["infantry"] = true,
        ["description"] = "Soldier RPG",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [314]
    [315] = 
    {
        ["type"] = "DRG_Class_86",
        ["name"] = "DRG Class 86",
        ["category"] = "Locomotive",
        ["vehicle"] = true,
        ["description"] = "DRG Class 86",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [315]
    [316] = 
    {
        ["type"] = "Electric locomotive",
        ["name"] = "Electric locomotive VL80",
        ["category"] = "Locomotive",
        ["vehicle"] = true,
        ["description"] = "Electric locomotive VL80",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [316]
    [317] = 
    {
        ["type"] = "ES44AH",
        ["name"] = "ES44AH",
        ["category"] = "Locomotive",
        ["vehicle"] = true,
        ["description"] = "ES44AH",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [317]
    [318] = 
    {
        ["type"] = "Locomotive",
        ["name"] = "Locomotive CHME3T",
        ["category"] = "Locomotive",
        ["vehicle"] = true,
        ["description"] = "Locomotive CHME3T",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [318]
    [319] = 
    {
        ["type"] = "Silkworm_SR",
        ["name"] = "Silkworm Radar",
        ["category"] = "MissilesSS",
        ["vehicle"] = true,
        ["description"] = "Silkworm Radar",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [319]
    [320] = 
    {
        ["type"] = "Scud_B",
        ["name"] = "SRBM SS-1C Scud-B 9K72 LN 9P117M",
        ["category"] = "MissilesSS",
        ["vehicle"] = true,
        ["description"] = "SRBM SS-1C Scud-B 9K72 LN 9P117M",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [320]
    [321] = 
    {
        ["type"] = "hy_launcher",
        ["name"] = "SS-N-2 Silkworm",
        ["category"] = "MissilesSS",
        ["vehicle"] = true,
        ["description"] = "SS-N-2 Silkworm",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [321]
    [322] = 
    {
        ["type"] = "v1_launcher",
        ["name"] = "V-1 ramp",
        ["category"] = "MissilesSS",
        ["vehicle"] = true,
        ["description"] = "V-1 ramp",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [322]
    [323] = 
    {
        ["air"] = true,
        ["type"] = "A-10A",
        ["name"] = "A-10A",
        ["category"] = "Plane",
        ["description"] = "A-10A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [323]
    [324] = 
    {
        ["air"] = true,
        ["type"] = "A-10C",
        ["name"] = "A-10C",
        ["category"] = "Plane",
        ["description"] = "A-10C",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [324]
    [325] = 
    {
        ["air"] = true,
        ["type"] = "A-20G",
        ["name"] = "A-20G",
        ["category"] = "Plane",
        ["description"] = "A-20G",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [325]
    [326] = 
    {
        ["air"] = true,
        ["type"] = "A-50",
        ["name"] = "A-50",
        ["category"] = "Plane",
        ["description"] = "A-50",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [326]
    [327] = 
    {
        ["air"] = true,
        ["type"] = "AJS37",
        ["name"] = "AJS37",
        ["category"] = "Plane",
        ["description"] = "AJS37",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [327]
    [328] = 
    {
        ["air"] = true,
        ["type"] = "An-26B",
        ["name"] = "An-26B",
        ["category"] = "Plane",
        ["description"] = "An-26B",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [328]
    [329] = 
    {
        ["air"] = true,
        ["type"] = "An-30M",
        ["name"] = "An-30M",
        ["category"] = "Plane",
        ["description"] = "An-30M",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [329]
    [330] = 
    {
        ["air"] = true,
        ["type"] = "AV8BNA",
        ["name"] = "AV-8B N/A",
        ["category"] = "Plane",
        ["description"] = "AV-8B N/A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [330]
    [331] = 
    {
        ["air"] = true,
        ["type"] = "B-17G",
        ["name"] = "B-17G",
        ["category"] = "Plane",
        ["description"] = "B-17G",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [331]
    [332] = 
    {
        ["air"] = true,
        ["type"] = "B-1B",
        ["name"] = "B-1B",
        ["category"] = "Plane",
        ["description"] = "B-1B",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [332]
    [333] = 
    {
        ["air"] = true,
        ["type"] = "B-52H",
        ["name"] = "B-52H",
        ["category"] = "Plane",
        ["description"] = "B-52H",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [333]
    [334] = 
    {
        ["air"] = true,
        ["type"] = "Bf-109K-4",
        ["name"] = "Bf 109 K-4",
        ["category"] = "Plane",
        ["description"] = "Bf 109 K-4",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [334]
    [335] = 
    {
        ["air"] = true,
        ["type"] = "C-101CC",
        ["name"] = "C-101CC",
        ["category"] = "Plane",
        ["description"] = "C-101CC",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [335]
    [336] = 
    {
        ["air"] = true,
        ["type"] = "C-101EB",
        ["name"] = "C-101EB",
        ["category"] = "Plane",
        ["description"] = "C-101EB",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [336]
    [337] = 
    {
        ["air"] = true,
        ["type"] = "C-130",
        ["name"] = "C-130",
        ["category"] = "Plane",
        ["description"] = "C-130",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [337]
    [338] = 
    {
        ["air"] = true,
        ["type"] = "C-17A",
        ["name"] = "C-17A",
        ["category"] = "Plane",
        ["description"] = "C-17A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [338]
    [339] = 
    {
        ["air"] = true,
        ["type"] = "Christen Eagle II",
        ["name"] = "Christen Eagle II",
        ["category"] = "Plane",
        ["description"] = "Christen Eagle II",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [339]
    [340] = 
    {
        ["air"] = true,
        ["type"] = "E-2C",
        ["name"] = "E-2D",
        ["category"] = "Plane",
        ["description"] = "E-2D",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [340]
    [341] = 
    {
        ["air"] = true,
        ["type"] = "E-3A",
        ["name"] = "E-3A",
        ["category"] = "Plane",
        ["description"] = "E-3A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [341]
    [342] = 
    {
        ["air"] = true,
        ["type"] = "F-111F",
        ["name"] = "F-111F",
        ["category"] = "Plane",
        ["description"] = "F-111F",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [342]
    [343] = 
    {
        ["air"] = true,
        ["type"] = "F-117A",
        ["name"] = "F-117A",
        ["category"] = "Plane",
        ["description"] = "F-117A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [343]
    [344] = 
    {
        ["air"] = true,
        ["type"] = "F-14A",
        ["name"] = "F-14A",
        ["category"] = "Plane",
        ["description"] = "F-14A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [344]
    [345] = 
    {
        ["air"] = true,
        ["type"] = "F-14B",
        ["name"] = "F-14B",
        ["category"] = "Plane",
        ["description"] = "F-14B",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [345]
    [346] = 
    {
        ["air"] = true,
        ["type"] = "F-15C",
        ["name"] = "F-15C",
        ["category"] = "Plane",
        ["description"] = "F-15C",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [346]
    [347] = 
    {
        ["air"] = true,
        ["type"] = "F-15E",
        ["name"] = "F-15E",
        ["category"] = "Plane",
        ["description"] = "F-15E",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [347]
    [348] = 
    {
        ["air"] = true,
        ["type"] = "F-16A",
        ["name"] = "F-16A",
        ["category"] = "Plane",
        ["description"] = "F-16A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [348]
    [349] = 
    {
        ["air"] = true,
        ["type"] = "F-16A MLU",
        ["name"] = "F-16A MLU",
        ["category"] = "Plane",
        ["description"] = "F-16A MLU",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [349]
    [350] = 
    {
        ["air"] = true,
        ["type"] = "F-16C bl.50",
        ["name"] = "F-16C bl.50",
        ["category"] = "Plane",
        ["description"] = "F-16C bl.50",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [350]
    [351] = 
    {
        ["air"] = true,
        ["type"] = "F-16C bl.52d",
        ["name"] = "F-16C bl.52d",
        ["category"] = "Plane",
        ["description"] = "F-16C bl.52d",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [351]
    [352] = 
    {
        ["air"] = true,
        ["type"] = "F-16C_50",
        ["name"] = "F-16CM bl.50",
        ["category"] = "Plane",
        ["description"] = "F-16CM bl.50",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [352]
    [353] = 
    {
        ["air"] = true,
        ["type"] = "F-4E",
        ["name"] = "F-4E",
        ["category"] = "Plane",
        ["description"] = "F-4E",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [353]
    [354] = 
    {
        ["air"] = true,
        ["type"] = "F-5E",
        ["name"] = "F-5E",
        ["category"] = "Plane",
        ["description"] = "F-5E",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [354]
    [355] = 
    {
        ["air"] = true,
        ["type"] = "F-5E-3",
        ["name"] = "F-5E-3",
        ["category"] = "Plane",
        ["description"] = "F-5E-3",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [355]
    [356] = 
    {
        ["air"] = true,
        ["type"] = "F-86F Sabre",
        ["name"] = "F-86F",
        ["category"] = "Plane",
        ["description"] = "F-86F",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [356]
    [357] = 
    {
        ["air"] = true,
        ["type"] = "F/A-18A",
        ["name"] = "F/A-18A",
        ["category"] = "Plane",
        ["description"] = "F/A-18A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [357]
    [358] = 
    {
        ["air"] = true,
        ["type"] = "F/A-18C",
        ["name"] = "F/A-18C",
        ["category"] = "Plane",
        ["description"] = "F/A-18C",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [358]
    [359] = 
    {
        ["air"] = true,
        ["type"] = "FA-18C_hornet",
        ["name"] = "F/A-18C Lot 20",
        ["category"] = "Plane",
        ["description"] = "F/A-18C Lot 20",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [359]
    [360] = 
    {
        ["air"] = true,
        ["type"] = "FW-190A8",
        ["name"] = "Fw 190 A-8",
        ["category"] = "Plane",
        ["description"] = "Fw 190 A-8",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [360]
    [361] = 
    {
        ["air"] = true,
        ["type"] = "FW-190D9",
        ["name"] = "Fw 190 D-9",
        ["category"] = "Plane",
        ["description"] = "Fw 190 D-9",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [361]
    [362] = 
    {
        ["air"] = true,
        ["type"] = "Hawk",
        ["name"] = "Hawk",
        ["category"] = "Plane",
        ["description"] = "Hawk",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [362]
    [363] = 
    {
        ["air"] = true,
        ["type"] = "I-16",
        ["name"] = "I-16",
        ["category"] = "Plane",
        ["description"] = "I-16",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [363]
    [364] = 
    {
        ["air"] = true,
        ["type"] = "IL-76MD",
        ["name"] = "IL-76MD",
        ["category"] = "Plane",
        ["description"] = "IL-76MD",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [364]
    [365] = 
    {
        ["air"] = true,
        ["type"] = "IL-78M",
        ["name"] = "IL-78M",
        ["category"] = "Plane",
        ["description"] = "IL-78M",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [365]
    [366] = 
    {
        ["air"] = true,
        ["type"] = "J-11A",
        ["name"] = "J-11A",
        ["category"] = "Plane",
        ["description"] = "J-11A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [366]
    [367] = 
    {
        ["air"] = true,
        ["type"] = "JF-17",
        ["name"] = "JF-17",
        ["category"] = "Plane",
        ["description"] = "JF-17",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [367]
    [368] = 
    {
        ["air"] = true,
        ["type"] = "Ju-88A4",
        ["name"] = "Ju 88 A-4",
        ["category"] = "Plane",
        ["description"] = "Ju 88 A-4",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [368]
    [369] = 
    {
        ["air"] = true,
        ["type"] = "KC130",
        ["name"] = "KC-130",
        ["category"] = "Plane",
        ["description"] = "KC-130",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [369]
    [370] = 
    {
        ["air"] = true,
        ["type"] = "KC-135",
        ["name"] = "KC-135",
        ["category"] = "Plane",
        ["description"] = "KC-135",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [370]
    [371] = 
    {
        ["air"] = true,
        ["type"] = "KC135MPRS",
        ["name"] = "KC-135MPRS",
        ["category"] = "Plane",
        ["description"] = "KC-135MPRS",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [371]
    [372] = 
    {
        ["air"] = true,
        ["type"] = "KJ-2000",
        ["name"] = "KJ-2000",
        ["category"] = "Plane",
        ["description"] = "KJ-2000",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [372]
    [373] = 
    {
        ["air"] = true,
        ["type"] = "L-39C",
        ["name"] = "L-39C",
        ["category"] = "Plane",
        ["description"] = "L-39C",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [373]
    [374] = 
    {
        ["air"] = true,
        ["type"] = "L-39ZA",
        ["name"] = "L-39ZA",
        ["category"] = "Plane",
        ["description"] = "L-39ZA",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [374]
    [375] = 
    {
        ["air"] = true,
        ["type"] = "M-2000C",
        ["name"] = "M-2000C",
        ["category"] = "Plane",
        ["description"] = "M-2000C",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [375]
    [376] = 
    {
        ["air"] = true,
        ["type"] = "MiG-15bis",
        ["name"] = "MiG-15bis",
        ["category"] = "Plane",
        ["description"] = "MiG-15bis",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [376]
    [377] = 
    {
        ["air"] = true,
        ["type"] = "MiG-19P",
        ["name"] = "MiG-19P",
        ["category"] = "Plane",
        ["description"] = "MiG-19P",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [377]
    [378] = 
    {
        ["air"] = true,
        ["type"] = "MiG-21Bis",
        ["name"] = "MiG-21Bis",
        ["category"] = "Plane",
        ["description"] = "MiG-21Bis",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [378]
    [379] = 
    {
        ["air"] = true,
        ["type"] = "MiG-23MLD",
        ["name"] = "MiG-23MLD",
        ["category"] = "Plane",
        ["description"] = "MiG-23MLD",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [379]
    [380] = 
    {
        ["air"] = true,
        ["type"] = "MiG-25PD",
        ["name"] = "MiG-25PD",
        ["category"] = "Plane",
        ["description"] = "MiG-25PD",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [380]
    [381] = 
    {
        ["air"] = true,
        ["type"] = "MiG-25RBT",
        ["name"] = "MiG-25RBT",
        ["category"] = "Plane",
        ["description"] = "MiG-25RBT",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [381]
    [382] = 
    {
        ["air"] = true,
        ["type"] = "MiG-27K",
        ["name"] = "MiG-27K",
        ["category"] = "Plane",
        ["description"] = "MiG-27K",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [382]
    [383] = 
    {
        ["air"] = true,
        ["type"] = "MiG-29A",
        ["name"] = "MiG-29A",
        ["category"] = "Plane",
        ["description"] = "MiG-29A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [383]
    [384] = 
    {
        ["air"] = true,
        ["type"] = "MiG-29G",
        ["name"] = "MiG-29G",
        ["category"] = "Plane",
        ["description"] = "MiG-29G",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [384]
    [385] = 
    {
        ["air"] = true,
        ["type"] = "MiG-29K",
        ["name"] = "MiG-29K",
        ["category"] = "Plane",
        ["description"] = "MiG-29K",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [385]
    [386] = 
    {
        ["air"] = true,
        ["type"] = "MiG-29S",
        ["name"] = "MiG-29S",
        ["category"] = "Plane",
        ["description"] = "MiG-29S",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [386]
    [387] = 
    {
        ["air"] = true,
        ["type"] = "MiG-31",
        ["name"] = "MiG-31",
        ["category"] = "Plane",
        ["description"] = "MiG-31",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [387]
    [388] = 
    {
        ["air"] = true,
        ["type"] = "Mirage 2000-5",
        ["name"] = "Mirage 2000-5",
        ["category"] = "Plane",
        ["description"] = "Mirage 2000-5",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [388]
    [389] = 
    {
        ["air"] = true,
        ["type"] = "RQ-1A Predator",
        ["name"] = "MQ-1A Predator",
        ["category"] = "Plane",
        ["description"] = "MQ-1A Predator",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [389]
    [390] = 
    {
        ["air"] = true,
        ["type"] = "MQ-9 Reaper",
        ["name"] = "MQ-9 Reaper",
        ["category"] = "Plane",
        ["description"] = "MQ-9 Reaper",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [390]
    [391] = 
    {
        ["air"] = true,
        ["type"] = "P-47D-30",
        ["name"] = "P-47D-30",
        ["category"] = "Plane",
        ["description"] = "P-47D-30",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [391]
    [392] = 
    {
        ["air"] = true,
        ["type"] = "P-51D",
        ["name"] = "P-51D-25-NA",
        ["category"] = "Plane",
        ["description"] = "P-51D-25-NA",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [392]
    [393] = 
    {
        ["air"] = true,
        ["type"] = "P-51D-30-NA",
        ["name"] = "P-51D-30-NA",
        ["category"] = "Plane",
        ["description"] = "P-51D-30-NA",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [393]
    [394] = 
    {
        ["air"] = true,
        ["type"] = "S-3B",
        ["name"] = "S-3B",
        ["category"] = "Plane",
        ["description"] = "S-3B",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [394]
    [395] = 
    {
        ["air"] = true,
        ["type"] = "S-3B Tanker",
        ["name"] = "S-3B Tanker",
        ["category"] = "Plane",
        ["description"] = "S-3B Tanker",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [395]
    [396] = 
    {
        ["air"] = true,
        ["type"] = "SpitfireLFMkIX",
        ["name"] = "Spitfire LF Mk. IX",
        ["category"] = "Plane",
        ["description"] = "Spitfire LF Mk. IX",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [396]
    [397] = 
    {
        ["air"] = true,
        ["type"] = "SpitfireLFMkIXCW",
        ["name"] = "Spitfire LF Mk. IX CW",
        ["category"] = "Plane",
        ["description"] = "Spitfire LF Mk. IX CW",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [397]
    [398] = 
    {
        ["air"] = true,
        ["type"] = "Su-17M4",
        ["name"] = "Su-17M4",
        ["category"] = "Plane",
        ["description"] = "Su-17M4",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [398]
    [399] = 
    {
        ["air"] = true,
        ["type"] = "Su-24M",
        ["name"] = "Su-24M",
        ["category"] = "Plane",
        ["description"] = "Su-24M",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [399]
    [400] = 
    {
        ["air"] = true,
        ["type"] = "Su-24MR",
        ["name"] = "Su-24MR",
        ["category"] = "Plane",
        ["description"] = "Su-24MR",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [400]
    [401] = 
    {
        ["air"] = true,
        ["type"] = "Su-25",
        ["name"] = "Su-25",
        ["category"] = "Plane",
        ["description"] = "Su-25",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [401]
    [402] = 
    {
        ["air"] = true,
        ["type"] = "Su-25T",
        ["name"] = "Su-25T",
        ["category"] = "Plane",
        ["description"] = "Su-25T",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [402]
    [403] = 
    {
        ["air"] = true,
        ["type"] = "Su-25TM",
        ["name"] = "Su-25TM",
        ["category"] = "Plane",
        ["description"] = "Su-25TM",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [403]
    [404] = 
    {
        ["air"] = true,
        ["type"] = "Su-27",
        ["name"] = "Su-27",
        ["category"] = "Plane",
        ["description"] = "Su-27",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [404]
    [405] = 
    {
        ["air"] = true,
        ["type"] = "Su-30",
        ["name"] = "Su-30",
        ["category"] = "Plane",
        ["description"] = "Su-30",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [405]
    [406] = 
    {
        ["air"] = true,
        ["type"] = "Su-33",
        ["name"] = "Su-33",
        ["category"] = "Plane",
        ["description"] = "Su-33",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [406]
    [407] = 
    {
        ["air"] = true,
        ["type"] = "Su-34",
        ["name"] = "Su-34",
        ["category"] = "Plane",
        ["description"] = "Su-34",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [407]
    [408] = 
    {
        ["air"] = true,
        ["type"] = "TF-51D",
        ["name"] = "TF-51D",
        ["category"] = "Plane",
        ["description"] = "TF-51D",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [408]
    [409] = 
    {
        ["air"] = true,
        ["type"] = "Tornado GR4",
        ["name"] = "Tornado GR4",
        ["category"] = "Plane",
        ["description"] = "Tornado GR4",
        ["aliases"] = 
        {
            [1] = "Tornado GR3",
        }, -- end of ["aliases"]
    }, -- end of [409]
    [410] = 
    {
        ["air"] = true,
        ["type"] = "Tornado IDS",
        ["name"] = "Tornado IDS",
        ["category"] = "Plane",
        ["description"] = "Tornado IDS",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [410]
    [411] = 
    {
        ["air"] = true,
        ["type"] = "Tu-142",
        ["name"] = "Tu-142",
        ["category"] = "Plane",
        ["description"] = "Tu-142",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [411]
    [412] = 
    {
        ["air"] = true,
        ["type"] = "Tu-160",
        ["name"] = "Tu-160",
        ["category"] = "Plane",
        ["description"] = "Tu-160",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [412]
    [413] = 
    {
        ["air"] = true,
        ["type"] = "Tu-22M3",
        ["name"] = "Tu-22M3",
        ["category"] = "Plane",
        ["description"] = "Tu-22M3",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [413]
    [414] = 
    {
        ["air"] = true,
        ["type"] = "Tu-95MS",
        ["name"] = "Tu-95MS",
        ["category"] = "Plane",
        ["description"] = "Tu-95MS",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [414]
    [415] = 
    {
        ["air"] = true,
        ["type"] = "Yak-40",
        ["name"] = "Yak-40",
        ["category"] = "Plane",
        ["description"] = "Yak-40",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [415]
    [416] = 
    {
        ["air"] = true,
        ["type"] = "Yak-52",
        ["name"] = "Yak-52",
        ["category"] = "Plane",
        ["description"] = "Yak-52",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [416]
    [417] = 
    {
        ["type"] = "speedboat",
        ["name"] = "Armed speedboat",
        ["category"] = "Ship",
        ["description"] = "Armed speedboat",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [417]
    [418] = 
    {
        ["type"] = "Dry-cargo ship-1",
        ["name"] = "Bulk cargo ship Yakushev",
        ["category"] = "Ship",
        ["description"] = "Bulk cargo ship Yakushev",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [418]
    [419] = 
    {
        ["type"] = "MOSCOW",
        ["name"] = "CG 1164 Moskva",
        ["category"] = "Ship",
        ["description"] = "CG 1164 Moskva",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [419]
    [420] = 
    {
        ["type"] = "PIOTR",
        ["name"] = "CGN 1144.2 Pyotr Velikiy",
        ["category"] = "Ship",
        ["description"] = "CGN 1144.2 Pyotr Velikiy",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [420]
    [421] = 
    {
        ["type"] = "ZWEZDNY",
        ["name"] = "Civil boat Zvezdny",
        ["category"] = "Ship",
        ["description"] = "Civil boat Zvezdny",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [421]
    [422] = 
    {
        ["type"] = "KUZNECOW",
        ["name"] = "CV 1143.5 Admiral Kuznetsov",
        ["category"] = "Ship",
        ["description"] = "CV 1143.5 Admiral Kuznetsov",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [422]
    [423] = 
    {
        ["type"] = "CV_1143_5",
        ["name"] = "CV 1143.5 Admiral Kuznetsov(2017)",
        ["category"] = "Ship",
        ["description"] = "CV 1143.5 Admiral Kuznetsov(2017)",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [423]
    [424] = 
    {
        ["type"] = "VINSON",
        ["name"] = "CVN-70 Carl Vinson",
        ["category"] = "Ship",
        ["description"] = "CVN-70 Carl Vinson",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [424]
    [425] = 
    {
        ["type"] = "CVN_71",
        ["name"] = "CVN-71 Theodore Roosevelt",
        ["category"] = "Ship",
        ["description"] = "CVN-71 Theodore Roosevelt",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [425]
    [426] = 
    {
        ["type"] = "CVN_72",
        ["name"] = "CVN-72 Abraham Lincoln",
        ["category"] = "Ship",
        ["description"] = "CVN-72 Abraham Lincoln",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [426]
    [427] = 
    {
        ["type"] = "CVN_73",
        ["name"] = "CVN-73 George Washington",
        ["category"] = "Ship",
        ["description"] = "CVN-73 George Washington",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [427]
    [428] = 
    {
        ["type"] = "Stennis",
        ["name"] = "CVN-74 John C. Stennis",
        ["category"] = "Ship",
        ["description"] = "CVN-74 John C. Stennis",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [428]
    [429] = 
    {
        ["type"] = "Dry-cargo ship-2",
        ["name"] = "Dry cargo ship Ivanov",
        ["category"] = "Ship",
        ["description"] = "Dry cargo ship Ivanov",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [429]
    [430] = 
    {
        ["type"] = "REZKY",
        ["name"] = "FF 1135M Rezky",
        ["category"] = "Ship",
        ["description"] = "FF 1135M Rezky",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [430]
    [431] = 
    {
        ["type"] = "NEUSTRASH",
        ["name"] = "FFG 11540 Neustrashimy",
        ["category"] = "Ship",
        ["description"] = "FFG 11540 Neustrashimy",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [431]
    [432] = 
    {
        ["type"] = "ALBATROS",
        ["name"] = "FFL 1124.4 Grisha",
        ["category"] = "Ship",
        ["description"] = "FFL 1124.4 Grisha",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [432]
    [433] = 
    {
        ["type"] = "MOLNIYA",
        ["name"] = "FSG 1241.1MP Molniya",
        ["category"] = "Ship",
        ["description"] = "FSG 1241.1MP Molniya",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [433]
    [434] = 
    {
        ["type"] = "Higgins_boat",
        ["name"] = "LCVP (Higgins boat)",
        ["category"] = "Ship",
        ["description"] = "LCVP (Higgins boat)",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [434]
    [435] = 
    {
        ["type"] = "LHA_Tarawa",
        ["name"] = "LHA-1 Tarawa",
        ["category"] = "Ship",
        ["description"] = "LHA-1 Tarawa",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [435]
    [436] = 
    {
        ["type"] = "USS_Samuel_Chase",
        ["name"] = "LS Samuel Chase",
        ["category"] = "Ship",
        ["description"] = "LS Samuel Chase",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [436]
    [437] = 
    {
        ["type"] = "LST_Mk2",
        ["name"] = "LST Mk.II",
        ["category"] = "Ship",
        ["description"] = "LST Mk.II",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [437]
    [438] = 
    {
        ["type"] = "PERRY",
        ["name"] = "Oliver Hazzard Perry class",
        ["category"] = "Ship",
        ["description"] = "Oliver Hazzard Perry class",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [438]
    [439] = 
    {
        ["type"] = "Schnellboot_type_S130",
        ["name"] = "Schnellboot type S130",
        ["category"] = "Ship",
        ["description"] = "Schnellboot type S130",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [439]
    [440] = 
    {
        ["type"] = "SOM",
        ["name"] = "SSK 641B",
        ["category"] = "Ship",
        ["description"] = "SSK 641B",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [440]
    [441] = 
    {
        ["type"] = "KILO",
        ["name"] = "SSK 877",
        ["category"] = "Ship",
        ["description"] = "SSK 877",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [441]
    [442] = 
    {
        ["type"] = "ELNYA",
        ["name"] = "Tanker Elnya 160",
        ["category"] = "Ship",
        ["description"] = "Tanker Elnya 160",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [442]
    [443] = 
    {
        ["type"] = "TICONDEROG",
        ["name"] = "Ticonderoga class",
        ["category"] = "Ship",
        ["description"] = "Ticonderoga class",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [443]
    [444] = 
    {
        ["type"] = "052B",
        ["name"] = "Type 052B Destroyer",
        ["category"] = "Ship",
        ["description"] = "Type 052B Destroyer",
        ["vehicle"] = true,
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [444]
    [445] = 
    {
        ["type"] = "052C",
        ["name"] = "Type 052C Destroyer",
        ["category"] = "Ship",
        ["description"] = "Type 052C Destroyer",
        ["vehicle"] = true,
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [445]
    [446] = 
    {
        ["type"] = "054A",
        ["name"] = "Type 054A Frigate",
        ["category"] = "Ship",
        ["description"] = "Type 054A Frigate",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [446]
    [447] = 
    {
        ["type"] = "Type 093",
        ["name"] = "Type 093",
        ["category"] = "Ship",
        ["description"] = "Type 093",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [447]
    [448] = 
    {
        ["type"] = "Uboat_VIIC",
        ["name"] = "Uboat VIIC U-flak",
        ["category"] = "Ship",
        ["description"] = "Uboat VIIC U-flak",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [448]
    [449] = 
    {
        ["type"] = "USS_Arleigh_Burke_IIa",
        ["name"] = "USS Arleigh Burke IIa",
        ["category"] = "Ship",
        ["description"] = "USS Arleigh Burke IIa",
        ["naval"] = true,
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [449]
    [450] = 
    {
        ["type"] = "Hummer",
        ["name"] = "APC M1025 HMMWV",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "APC M1025 HMMWV",
        ["aliases"] = 
        {
            [1] = "M1025 HMMWV",
        }, -- end of ["aliases"]
    }, -- end of [450]
    [451] = 
    {
        ["type"] = "Tigr_233036",
        ["name"] = "APC Tigr 233036",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "APC Tigr 233036",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [451]
    [452] = 
    {
        ["type"] = "Bedford_MWD",
        ["name"] = "Bedford MWD",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Bedford MWD",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [452]
    [453] = 
    {
        ["type"] = "Blitz_36-6700A",
        ["name"] = "Blitz 3.6-6700A",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Blitz 3.6-6700A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [453]
    [454] = 
    {
        ["type"] = "CCKW_353",
        ["name"] = "CCKW 353",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "CCKW 353",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [454]
    [455] = 
    {
        ["type"] = "Predator GCS",
        ["name"] = "CP Predator GCS",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "CP Predator GCS",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [455]
    [456] = 
    {
        ["type"] = "Predator TrojanSpirit",
        ["name"] = "CP Predator TrojanSpirit",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "CP Predator TrojanSpirit",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [456]
    [457] = 
    {
        ["type"] = "SKP-11",
        ["name"] = "CP SKP-11 ATC Mobile Command Post",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "CP SKP-11 ATC Mobile Command Post",
        ["aliases"] = 
        {
            [1] = "SKP-11 Mobile Command Post",
        }, -- end of ["aliases"]
    }, -- end of [457]
    [458] = 
    {
        ["type"] = "Ural-375 PBU",
        ["name"] = "CP Ural-375 PBU",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "CP Ural-375 PBU",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [458]
    [459] = 
    {
        ["type"] = "ATMZ-5",
        ["name"] = "Fuel Truck ATMZ-5",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Fuel Truck ATMZ-5",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [459]
    [460] = 
    {
        ["type"] = "ATZ-10",
        ["name"] = "Fuel Truck ATZ-10",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Fuel Truck ATZ-10",
        ["aliases"] = 
        {
            [1] = "ATZ-10 Fuel Truck",
        }, -- end of ["aliases"]
    }, -- end of [460]
    [461] = 
    {
        ["type"] = "Ural-4320 APA-5D",
        ["name"] = "GPU APA-5D on Ural-4320",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "GPU APA-5D on Ural-4320",
        ["aliases"] = 
        {
            [1] = "Ural-4320 APA-5D Ground Power Unit",
        }, -- end of ["aliases"]
    }, -- end of [461]
    [462] = 
    {
        ["type"] = "ZiL-131 APA-80",
        ["name"] = "GPU APA-80 on ZiL-131",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "GPU APA-80 on ZiL-131",
        ["aliases"] = 
        {
            [1] = "ZiL-131 APA-80 Ground Power Unit",
        }, -- end of ["aliases"]
    }, -- end of [462]
    [463] = 
    {
        ["type"] = "HEMTT TFFT",
        ["name"] = "HEMTT TFFT",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "HEMTT TFFT",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [463]
    [464] = 
    {
        ["type"] = "Horch_901_typ_40_kfz_21",
        ["name"] = "Horch 901 typ 40",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Horch 901 typ 40",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [464]
    [465] = 
    {
        ["type"] = "Kubelwagen_82",
        ["name"] = "Kübelwagen 82",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Kübelwagen 82",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [465]
    [466] = 
    {
        ["type"] = "Land_Rover_101_FC",
        ["name"] = "Land Rover 101 FC",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Land Rover 101 FC",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [466]
    [467] = 
    {
        ["type"] = "Land_Rover_109_S3",
        ["name"] = "Land Rover 109 S3",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Land Rover 109 S3",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [467]
    [468] = 
    {
        ["type"] = "Sd_Kfz_2",
        ["name"] = "Sd.Kfz.2",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Sd.Kfz.2",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [468]
    [469] = 
    {
        ["type"] = "Sd_Kfz_7",
        ["name"] = "Sd.Kfz.7",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Sd.Kfz.7",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [469]
    [470] = 
    {
        ["type"] = "Suidae",
        ["name"] = "Suidae",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Suidae",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [470]
    [471] = 
    {
        ["type"] = "M978 HEMTT Tanker",
        ["name"] = "Tanker M978 HEMTT",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Tanker M978 HEMTT",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [471]
    [472] = 
    {
        ["type"] = "Ural ATsP-6",
        ["name"] = "Transport fire-engine Ural ATsP-6",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport fire-engine Ural ATsP-6",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [472]
    [473] = 
    {
        ["type"] = "GAZ-3307",
        ["name"] = "Transport GAZ-3307",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport GAZ-3307",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [473]
    [474] = 
    {
        ["type"] = "GAZ-3308",
        ["name"] = "Transport GAZ-3308",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport GAZ-3308",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [474]
    [475] = 
    {
        ["type"] = "GAZ-66",
        ["name"] = "Transport GAZ-66",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport GAZ-66",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [475]
    [476] = 
    {
        ["type"] = "IKARUS Bus",
        ["name"] = "Transport IKARUS-280",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport IKARUS-280",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [476]
    [477] = 
    {
        ["type"] = "KAMAZ Truck",
        ["name"] = "Transport KAMAZ-43101",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport KAMAZ-43101",
        ["aliases"] = 
        {
            [1] = "KAMAZ-43101",
        }, -- end of ["aliases"]
    }, -- end of [477]
    [478] = 
    {
        ["type"] = "KrAZ6322",
        ["name"] = "Transport KrAZ-6322",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport KrAZ-6322",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [478]
    [479] = 
    {
        ["type"] = "LAZ Bus",
        ["name"] = "Transport LAZ-695",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport LAZ-695",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [479]
    [480] = 
    {
        ["type"] = "M 818",
        ["name"] = "Transport M818",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport M818",
        ["aliases"] = 
        {
            [1] = "M818",
        }, -- end of ["aliases"]
    }, -- end of [480]
    [481] = 
    {
        ["type"] = "MAZ-6303",
        ["name"] = "Transport MAZ-6303",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport MAZ-6303",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [481]
    [482] = 
    {
        ["type"] = "UAZ-469",
        ["name"] = "Transport UAZ-469",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport UAZ-469",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [482]
    [483] = 
    {
        ["type"] = "Ural-375",
        ["name"] = "Transport Ural-375",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport Ural-375",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [483]
    [484] = 
    {
        ["type"] = "Ural-4320-31",
        ["name"] = "Transport Ural-4320-31 Armored",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport Ural-4320-31 Armored",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [484]
    [485] = 
    {
        ["type"] = "Ural-4320T",
        ["name"] = "Transport Ural-4320T",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport Ural-4320T",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [485]
    [486] = 
    {
        ["type"] = "VAZ Car",
        ["name"] = "Transport VAZ-2109",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport VAZ-2109",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [486]
    [487] = 
    {
        ["type"] = "ZIL-131 KUNG",
        ["name"] = "Transport ZIL-131 KUNG",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport ZIL-131 KUNG",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [487]
    [488] = 
    {
        ["type"] = "ZIL-4331",
        ["name"] = "Transport ZIL-4331",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport ZIL-4331",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [488]
    [489] = 
    {
        ["type"] = "Trolley bus",
        ["name"] = "Transport ZIU-9",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Transport ZIU-9",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [489]
    [490] = 
    {
        ["type"] = "warning_board_a",
        ["name"] = "Warning Board A",
        ["category"] = "Unarmed",
        ["description"] = "Warning Board A",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [490]
    [491] = 
    {
        ["type"] = "Willys_MB",
        ["name"] = "Willys MB",
        ["category"] = "Unarmed",
        ["vehicle"] = true,
        ["description"] = "Willys MB",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [491]
    [492] = 
    {
        ["type"] = ".Ammunition depot",
        ["name"] = "Ammunition depot",
        ["category"] = "Warehouse",
        ["description"] = "Ammunition depot",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [492]
    [493] = 
    {
        ["type"] = "Tank",
        ["name"] = "Tank",
        ["category"] = "Warehouse",
        ["description"] = "Tank",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [493]
    [494] = 
    {
        ["type"] = "Tank 2",
        ["name"] = "Tank 2",
        ["category"] = "Warehouse",
        ["description"] = "Tank 2",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [494]
    [495] = 
    {
        ["type"] = "Tank 3",
        ["name"] = "Tank 3",
        ["category"] = "Warehouse",
        ["description"] = "Tank 3",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    }, -- end of [495]
    [496] = 
    {
        ["type"] = "Warehouse",
        ["name"] = "Warehouse",
        ["category"] = "Warehouse",
        ["description"] = "Warehouse",
        ["aliases"] = 
        {
        }, -- end of ["aliases"]
    } -- end of [496]
}

-- appending custom cargoes
function dcsUnits.addCargoUnit( name, displayName, shape, shapeDstr, life, canExplode, rate, mass, attribute, minMass, maxMass, topdown_view)
    local res = {}
    res.desc = {}
    
    res.desc.typeName = name
    res.desc.displayName = displayName
    res.desc.attributes = {}
    res.desc.attributes.Cargos = true
    res.desc.minMass = minMass
    res.desc.maxMass = maxMass
    res.desc.category = 'Cargo'

    dcsUnits.logDebug("Adding custom cargo "..displayName)
    dcsUnits.DcsUnitsDatabase[name] = res
end

dcsUnits.logInfo(string.format("Loading version %s", dcsUnits.Version))

-- dcsUnits.addCargoUnit( "jeep_cargo", "jeep_cargo", "jeep_cargo", "jeep_cargo",10,false, 100, 1200,  {"Cargos"}, 100, 4000 );
-- dcsUnits.addCargoUnit( "bambi_bucket", "bambi_bucket", "bambi_bucket","bambi_bucket",5,false, 1000, 1500,  {"Cargos"}, 1000, 2000 );
-- dcsUnits.addCargoUnit( "zu23_cargo", "zu23_cargo", "zu23_cargo","zu23_cargo",15,false, 100, 1500,  {"Cargos"}, 1000, 2000 ); --zu23_cargo
-- dcsUnits.addCargoUnit( "blu82_cargo", "blu82_cargo", "blu82_cargo","blu82_cargo",10,true,100, 2400,{"Cargos"},800,5000); --blu82_cargo
-- dcsUnits.addCargoUnit( "generator_cargo", "generator_cargo", "generator_cargo","generator_cargo",10,false, 100, 1500,  {"Cargos"}, 1000, 2000 ); --generator_cargo
-- dcsUnits.addCargoUnit( "Tschechenigel_cargo", "Tschechenigel_cargo", "reiter_cargo","reiter_cargo",20,false, 100, 1000,  {"Cargos"}, 100, 10000 ); --reiter_cargo
-- dcsUnits.addCargoUnit( "sandbag", "sandbag", "sandbag","sandbag", 100, 1000,  {"Cargos"},10,false, 100, 10000 ); --sandbag
-- dcsUnits.addCargoUnit( "booth_container", "booth_container", "booth_container","booth_container",10,false, 100, 3200,  {"Cargos"}, 2200, 10000 );--booth_container
-- dcsUnits.addCargoUnit( "antenne", "antenne", "antenne","antenne",10,false, 100, 3200,  {"Cargos"}, 2200, 10000 );--antenne
-- dcsUnits.addCargoUnit( "mast", "mast", "mast","mast",10,false, 100, 3200,  {"Cargos"}, 2200, 10000 );--mast
-- dcsUnits.addCargoUnit( "uh1_weapons", "uh1_weapons", "uh1_weapons","uh1_weapons",10,false, 100, 1000,  {"Cargos"}, 100, 10000 );--uh1_weapons
-- dcsUnits.addCargoUnit( "panzergranaten", "panzergranaten", "panzergranaten","panzergranaten",10,false, 100, 1500,  {"Cargos"}, 1000, 2000 );--panzergranaten
-- dcsUnits.addCargoUnit( "pz2000_shell", "pz2000_shell", "pz2000_shell","pz2000_shell",10,false, 100, 1500,  {"Cargos"}, 1000, 2000 );--pz2000_shell
-- dcsUnits.addCargoUnit( "sandbag_box", "sandbag_box", "sandbag_box","sandbag_box",10,false, 100, 1500,  {"Cargos"}, 1000, 2000 );--sandbag_box
-- dcsUnits.addCargoUnit( "fir_tree", "fir_tree", "fir_tree","fir_tree",100, 1000,  {"Cargos"},10,false, 100, 10000 );--fir_tree
-- dcsUnits.addCargoUnit( "hmvee_cargo", "hmvee_cargo", "hmvee_cargo","hmvee_cargo",10,false, 100, 3200,  {"Cargos"}, 2200, 10000 );--hmvee_cargo
-- dcsUnits.addCargoUnit( "eurotainer", "eurotainer", "eurotainer","eurotainer",10,false,100, 2400,{"Cargos"},800,5000);--eurotainer
-- dcsUnits.addCargoUnit( "MK6", "MK6", "MK6","MK6",10,true,100, 2400,{"Cargos"},800,5000);--MK6
-- dcsUnits.addCargoUnit( "concrete_pipe_duo", "concrete_pipe_duo", "concrete_pipe_duo","concrete_pipe_duo",10,false,100, 823,  {"Cargos"}, 823, 823 );--concrete_pipe_duo
-- dcsUnits.addCargoUnit( "concrete_pipe", "concrete_pipe", "concrete_pipe","concrete_pipe",10,false,100, 823,  {"Cargos"}, 823, 823 );--concrete_pipe
-- dcsUnits.addCargoUnit( "gaz66_cargo", "gaz66_cargo", "gaz66_cargo","gaz66_cargo",15,false, 100, 3200,  {"Cargos"}, 2200, 10000 );--gaz66_cargo
-- dcsUnits.addCargoUnit( "uaz_cargo", "uaz_cargo", "uaz_cargo","uaz_cargo",15,false, 100, 3200,  {"Cargos"}, 2200, 10000 );--uaz_cargo
-- dcsUnits.addCargoUnit( "stretcher_body", "stretcher_body", "stretcher_body","stretcher_body",5,false,100, 1000,  {"Cargos"}, 100, 10000 );--stretcher_body
-- dcsUnits.addCargoUnit( "stretcher_empty", "stretcher_empty", "stretcher_empty","stretcher_empty",10,false,100, 1000,  {"Cargos"}, 100, 10000 );--stretcher_empty
-- dcsUnits.addCargoUnit( "san_container", "san_container", "san_container","san_container",15,false, 100, 3200,  {"Cargos"}, 2200, 10000 );--san_container
-- dcsUnits.addCargoUnit( "biwak_cargo", "biwak_cargo", "biwak_cargo","biwak_cargo", 15,false,100, 3200,  {"Cargos"}, 2200, 10000 );--biwak_cargo
-- dcsUnits.addCargoUnit( "wolf_cargo", "wolf_cargo", "wolf_cargo","wolf_cargo",15,false, 100, 3200,  {"Cargos"}, 2200, 10000 );--wolf_cargo
-- dcsUnits.addCargoUnit( "biwak_timber", "biwak_timber", "biwak_timber","biwak_timber",15,false, 100, 480,  {"Cargos"}, 100, 480);--biwak_timber
-- dcsUnits.addCargoUnit( "biwak_metal", "biwak_metal", "biwak_metal","biwak_metal",15,false, 100, 480,  {"Cargos"}, 100, 480);--biwak_metal


