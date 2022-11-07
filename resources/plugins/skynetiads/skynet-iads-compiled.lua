env.info("--- SKYNET VERSION: 3.0.1 | BUILD TIME: 06.11.2022 1728Z ---")
do
--this file contains the required units per sam type
samTypesDB = {
	['S-200'] = {
        ['type'] = 'complex',
        ['searchRadar'] = {
            ['RLS_19J6'] = {
                ['name'] = {
                    ['NATO'] = 'Tin Shield',
                },
			}, 
			['p-19 s-125 sr'] = {
				['name'] = {
					['NATO'] = 'Flat Face',
				},
			},	
		},
        ['EWR P-37 BAR LOCK'] = {
            ['Name'] = {
              ['NATO'] = "Bar lock",
            },   
        },
        ['trackingRadar'] = {
            ['RPC_5N62V'] = {
            },
        },
        ['launchers'] = {
            ['S-200_Launcher'] = {
            },
        },
        ['name'] = {
            ['NATO'] = 'SA-5 Gammon',
        },
        ['harm_detection_chance'] = 60
    },
	['S-300'] = {
		['type'] = 'complex',
		['searchRadar'] = {
			['S-300PS 40B6MD sr'] = {
				['name'] = {
					['NATO'] = 'Clam Shell',
				},
			},
			['S-300PS 64H6E sr'] = {
				['name'] = {
					['NATO'] = 'Big Bird',
				},
			},
		},
		['trackingRadar'] = {
			['S-300PS 40B6M tr'] = {
			},
		},
		['launchers'] = {
			['S-300PS 5P85D ln'] = {
			},
			['S-300PS 5P85C ln'] = {
			},
		},
		['misc'] = {
			['S-300PS 54K6 cp'] = {
				['required'] = true,
			},
		},
		['name'] = {
			['NATO'] = 'SA-10 Grumble',
		},
		['harm_detection_chance'] = 90,
		['can_engage_harm'] = true
	},
	['Buk'] = {
		['type'] = 'complex',
		['searchRadar'] = {
			['SA-11 Buk SR 9S18M1'] = {
				['name'] = {
					['NATO'] = 'Snow Drift',
				},
			},
		},
		['launchers'] = {
			['SA-11 Buk LN 9A310M1'] = {
			},
		},
		['misc'] = {
			['SA-11 Buk CC 9S470M1'] = {
				['required'] = true,
			},
		},
		['name'] = {
			['NATO'] = 'SA-11 Gadfly',
		},
		['harm_detection_chance'] = 70
	},
	['S-125'] = {
		['type'] = 'complex',
		['searchRadar'] = {
			['p-19 s-125 sr'] = {
				['name'] = {
					['NATO'] = 'Flat Face',
				},
			},	
		},
		['trackingRadar'] = {
			['snr s-125 tr'] = {
			},
		},
		['launchers'] = {
			['5p73 s-125 ln'] = {
			},
		},
		['name'] = {
			['NATO'] = 'SA-3 Goa',
		},
		['harm_detection_chance'] = 30
	},
    ['S-75'] = {
		['type'] = 'complex',
		['searchRadar'] = {
			['p-19 s-125 sr'] = {
				['name'] = {
					['NATO'] = 'Flat Face',
				},
			},
		},
		['trackingRadar'] = {
			['SNR_75V'] = {
			},
		},
		['launchers'] = {
			['S_75M_Volhov'] = {
			},
		},
		['name'] = {
			['NATO'] = 'SA-2 Guideline',
		},
		['harm_detection_chance'] = 30
	},
	['Kub'] = {
		['type'] = 'complex',
		['searchRadar'] = {
			['Kub 1S91 str'] = {
				['name'] = {
					['NATO'] = 'Straight Flush',
				},
			},
		},
		['launchers'] = {
			['Kub 2P25 ln'] = {
			},
		},
		['name'] = {
			['NATO'] = 'SA-6 Gainful',
		},
		['harm_detection_chance'] = 40
	},
	['Patriot'] = {
		['type'] = 'complex',
		['searchRadar'] = {
			['Patriot str'] = {
				['name'] = {
					['NATO'] = 'Patriot str',
				},
			},
		},
		['launchers'] = {
			['Patriot ln'] = {
			},
		},
		['misc'] = {
			['Patriot cp'] = {
				['required'] = false,
			},
			['Patriot EPP']  = {
				['required'] = false,
			},
			['Patriot ECS']  = {
				['required'] = true,
			},
			['Patriot AMG']  = {
				['required'] = false,
			},
		},
		['name'] = {
			['NATO'] = 'Patriot',
		},
		['harm_detection_chance'] = 90,
		['can_engage_harm'] = true
	},
	['Hawk'] = {
		['type'] = 'complex',
		['searchRadar'] = {
			['Hawk sr'] = {
				['name'] = {
					['NATO'] = 'Hawk str',
				},
			},
		},
		['trackingRadar'] = {
			['Hawk tr'] = {
			},
		},
		['launchers'] = {
			['Hawk ln'] = {
			},
		},

		['name'] = {
			['NATO'] = 'Hawk',
		},
		['harm_detection_chance'] = 40

	},	
	['Roland ADS'] = {
		['type'] = 'single',
		['searchRadar'] = {
			['Roland ADS'] = {
			},
		},
		['launchers'] = {
			['Roland ADS'] = {
			},
		},

		['name'] = {
			['NATO'] = 'Roland ADS',
		},
		['harm_detection_chance'] = 60
	},	
	['NASAMS'] = {
		['type'] = 'complex',
		['searchRadar'] = {
			['NASAMS_Radar_MPQ64F1'] = {
			},
		},
		['launchers'] = {
			['NASAMS_LN_B'] = {		
			},
			['NASAMS_LN_C'] = {		
			},
		},
		
		['name'] = {
			['NATO'] = 'NASAMS',
		},
		['misc'] = {
			['NASAMS_Command_Post'] = {
				['required'] = false,
			},
		},
		['can_engage_harm'] = true,
		['harm_detection_chance'] = 90
	},	
	['2S6 Tunguska'] = {
		['type'] = 'single',
		['searchRadar'] = {
			['2S6 Tunguska'] = {
			},
		},
		['launchers'] = {
			['2S6 Tunguska'] = {
			},
		},
		['name'] = {
			['NATO'] = 'SA-19 Grison',
		},
	},		
	['Osa'] = {
		['type'] = 'single',
		['searchRadar'] = {
			['Osa 9A33 ln'] = {
			},
		},
		['launchers'] = {
			['Osa 9A33 ln'] = {
			
			},
		},
		['name'] = {
			['NATO'] = 'SA-8 Gecko',
		},
		['harm_detection_chance'] = 20
	},	
	['Strela-10M3'] = {
		['type'] = 'single',
		['searchRadar'] = {
			['Strela-10M3'] = {
				['trackingRadar'] = true,
			},
		},
		['launchers'] = {
			['Strela-10M3'] = {
			},
		},
		['name'] = {
			['NATO'] = 'SA-13 Gopher',
		},
	},	
	['Strela-1 9P31'] = {
		['type'] = 'single',
		['searchRadar'] = {
			['Strela-1 9P31'] = {
			},
		},
		['launchers'] = {
			['Strela-1 9P31'] = {
			},
		},
		['name'] = {
			['NATO'] = 'SA-9 Gaskin',
		},
		['harm_detection_chance'] = 20
	},
	['Tor'] = {
		['type'] = 'single',
		['searchRadar'] = {
			['Tor 9A331'] = {
			},
		},
		['launchers'] = {
			['Tor 9A331'] = {
			},
		},
		['name'] = {
			['NATO'] = 'SA-15 Gauntlet',
		},
		['harm_detection_chance'] = 90,
		['can_engage_harm'] = true
		
	},
	['Gepard'] = {
		['type'] = 'single',
		['searchRadar'] = {
			['Gepard'] = {
			},
		},
		['launchers'] = {
			['Gepard'] = {
			},
		},
		['name'] = {
			['NATO'] = 'Gepard',
		},
		['harm_detection_chance'] = 10
	},		
    ['Rapier'] = {
        ['searchRadar'] = {
            ['rapier_fsa_blindfire_radar'] = {
            },
        },
        ['launchers'] = {
        	['rapier_fsa_launcher'] = {
				['trackingRadar'] = true,
			},
        },
        ['misc'] = {
            ['rapier_fsa_optical_tracker_unit'] = {
                ['required'] = true,
            },
        },
        ['name'] = {
			['NATO'] = 'Rapier',
		},
		['harm_detection_chance'] = 10
    },	
	['ZSU-23-4 Shilka'] = {
		['type'] = 'single',
		['searchRadar'] = {
			['ZSU-23-4 Shilka'] = {
			},
		},
		['launchers'] = {
			['ZSU-23-4 Shilka'] = {
			},
		},
		['name'] = {
			['NATO'] = 'Zues',
		},
		['harm_detection_chance'] = 10
	},
	['HQ-7'] = {
		['searchRadar'] = {
			['HQ-7_STR_SP'] = {
				['name'] = {
					['NATO'] = 'CSA-4',
				},
			},
		},
		['launchers'] = {
			['HQ-7_LN_SP'] = {
			},
		},
		['name'] = {
			['NATO'] = 'CSA-4',
		},
		['harm_detection_chance'] = 30
	},
--- Start of EW radars:
	['1L13 EWR'] = {
		['type'] = 'ewr',
		['searchRadar'] = {
			['1L13 EWR'] = {
				['name'] = {
					['NATO'] = 'Box Spring',
				},
			},
		},
		['harm_detection_chance'] = 60
	},
	['55G6 EWR'] = {
		['type'] = 'ewr',
		['searchRadar'] = {
			['55G6 EWR'] = {
				['name'] = {
					['NATO'] = 'Tall Rack',
				},
			},
		},
		['harm_detection_chance'] = 60
	},
	['Dog Ear'] = {
		['type'] = 'ewr',
		['searchRadar'] = {
			['Dog Ear radar'] = {
				['name'] = {
					['NATO'] = 'Dog Ear',
				},
			},
		},
		['harm_detection_chance'] = 20
	},
	['Roland Radar'] = {
		['type'] = 'ewr',
		['searchRadar'] = {
			['Roland Radar'] = {
				['name'] = {
					['NATO'] = 'Roland EWR',
				},
			},
		},

		['harm_detection_chance'] = 60
	},	
}
end
do
-- this file contains the definitions for the HightDigitSAMSs: https://github.com/Auranis/HighDigitSAMs

--EW radars used in multiple SAM systems:

s300PMU164N6Esr = {
	['name'] = {
		['NATO'] = 'Big Bird',
	},
}

s300PMU140B6MDsr = {
	['name'] = {
		['NATO'] = 'Clam Shell',
	},
}

--[[ units in SA-10 group Gargoyle:
2020-12-10 18:27:27.050 INFO    SCRIPTING: S-300PMU1 54K6 cp
2020-12-10 18:27:27.050 INFO    SCRIPTING: S-300PMU1 5P85CE ln
2020-12-10 18:27:27.050 INFO    SCRIPTING: S-300PMU1 5P85DE ln
2020-12-10 18:27:27.050 INFO    SCRIPTING: S-300PMU1 40B6MD sr
2020-12-10 18:27:27.050 INFO    SCRIPTING: S-300PMU1 64N6E sr
2020-12-10 18:27:27.050 INFO    SCRIPTING: S-300PMU1 40B6M tr
2020-12-10 18:27:27.050 INFO    SCRIPTING: S-300PMU1 30N6E tr
--]]
samTypesDB['S-300PMU1'] = {
	['type'] = 'complex',
	['searchRadar'] = {
		['S-300PMU1 40B6MD sr'] = s300PMU140B6MDsr,
		['S-300PMU1 64N6E sr'] = s300PMU164N6Esr,
		
		['S-300PS 40B6MD sr'] = {
			['name'] = {
				['NATO'] = '',
			},
		},
		['S-300PS 64H6E sr'] = {
			['name'] = {
				['NATO'] = '',
			},
		},
	},
	['trackingRadar'] = {
		['S-300PMU1 40B6M tr'] = {
			['name'] = {
				['NATO'] = 'Grave Stone',
			},
		},
		['S-300PMU1 30N6E tr'] = {
			['name'] = {
				['NATO'] = 'Flap Lid',
			},

		},
		['S-300PS 40B6M tr'] = {
			['name'] = {
				['NATO'] = '',
			},
		},
	},
	['misc'] = {
		['S-300PMU1 54K6 cp'] = {
			['required'] = true,
		},
	},
	['launchers'] = {
		['S-300PMU1 5P85CE ln'] = {
		},
		['S-300PMU1 5P85DE ln'] = {
		},
	},
	['name']  = {
		['NATO'] = 'SA-20A Gargoyle'
	},
	['harm_detection_chance'] = 90,
	['can_engage_harm'] = true
}	

--[[ Units in the SA-23 Group:
2020-12-11 16:40:52.072 INFO    SCRIPTING: S-300VM 9A82ME ln
2020-12-11 16:40:52.072 INFO    SCRIPTING: S-300VM 9A83ME ln
2020-12-11 16:40:52.072 INFO    SCRIPTING: S-300VM 9S15M2 sr
2020-12-11 16:40:52.072 INFO    SCRIPTING: S-300VM 9S19M2 sr
2020-12-11 16:40:52.072 INFO    SCRIPTING: S-300VM 9S32ME tr
2020-12-11 16:40:52.072 INFO    SCRIPTING: S-300VM 9S457ME cp

]]--
samTypesDB['S-300VM'] = {
	['type'] = 'complex',
	['searchRadar'] = {
		['S-300VM 9S15M2 sr'] = {
			['name'] = {
				['NATO'] = 'Bill Board-C',
			},
		},
		['S-300VM 9S19M2 sr'] = {
			['name'] = {
				['NATO'] = 'High Screen-B',
			},
		},
	},
	['trackingRadar'] = {
		['S-300VM 9S32ME tr'] = {
		},
	},
	['misc'] = {
		['S-300VM 9S457ME cp'] = {
			['required'] = true,
		},
	},
	['launchers'] = {
		['S-300VM 9A82ME ln'] = {
		},
		['S-300VM 9A83ME ln'] = {
		},
	},
	['name']  = {
		['NATO'] = 'SA-23 Antey-2500'
	},
	['harm_detection_chance'] = 90,
	['can_engage_harm'] = true
}	

--[[ Units in the SA-10B Group:
2021-01-01 20:39:14.413 INFO    SCRIPTING: S-300PS SA-10B 40B6MD MAST sr
2021-01-01 20:39:14.413 INFO    SCRIPTING: S-300PS SA-10B 54K6 cp
2021-01-01 20:39:14.413 INFO    SCRIPTING: S-300PS 5P85SE_mod ln
2021-01-01 20:39:14.413 INFO    SCRIPTING: S-300PS 5P85SU_mod ln
2021-01-01 20:39:14.413 INFO    SCRIPTING: S-300PS 64H6E TRAILER sr
2021-01-01 20:39:14.413 INFO    SCRIPTING: S-300PS 30N6 TRAILER tr
2021-01-01 20:39:14.413 INFO    SCRIPTING: S-300PS SA-10B 40B6M MAST tr
--]]
samTypesDB['S-300PS'] = {
	['type'] = 'complex',
	['searchRadar'] = {
		['S-300PS SA-10B 40B6MD MAST sr'] = {
			['name'] = {
				['NATO'] = 'Clam Shell',
			},
		},
		['S-300PS 64H6E TRAILER sr'] = {
		},
	},
	['trackingRadar'] = {
		['S-300PS 30N6 TRAILER tr'] = {
		},
		['S-300PS SA-10B 40B6M MAST tr'] = {
		},
		['S-300PS 40B6M tr'] = {
		},
		['S-300PMU1 40B6M tr'] = {
		},	
		['S-300PMU1 30N6E tr'] = {
		},		
	},
	['misc'] = {
		['S-300PS SA-10B 54K6 cp'] = {
			['required'] = true,
		},
	},
	['launchers'] = {
		['S-300PS 5P85SE_mod ln'] = {
		},
		['S-300PS 5P85SU_mod ln'] = {
		},
	},
	['name']  = {
		['NATO'] = 'SA-10B Grumble'
	},
	['harm_detection_chance'] = 90,
	['can_engage_harm'] = true
}

--[[ Extra launchers for the in game SA-10C and HighDigitSAMs SA-10B, SA-20B
2021-01-01 21:04:19.908 INFO    SCRIPTING: S-300PS 5P85DE ln
2021-01-01 21:04:19.908 INFO    SCRIPTING: S-300PS 5P85CE ln
--]]

local s300launchers = samTypesDB['S-300']['launchers']
s300launchers['S-300PS 5P85DE ln'] = {}
s300launchers['S-300PS 5P85CE ln'] = {}

local s300launchers = samTypesDB['S-300PS']['launchers']
s300launchers['S-300PS 5P85DE ln'] = {}
s300launchers['S-300PS 5P85CE ln'] = {}

local s300launchers = samTypesDB['S-300PMU1']['launchers']
s300launchers['S-300PS 5P85DE ln'] = {}
s300launchers['S-300PS 5P85CE ln'] = {}

--[[
New launcher for the SA-11 complex, will identify as SA-17
SA-17 Buk M1-2 LN 9A310M1-2
 --]]
samTypesDB['Buk-M2'] = {
	['type'] = 'complex',
	['searchRadar'] = {
		['SA-11 Buk SR 9S18M1'] = {
			['name'] = {
				['NATO'] = 'Snow Drift',
			},
		},
	},
	['launchers'] = {
		['SA-17 Buk M1-2 LN 9A310M1-2'] = {
		},
	},
	['misc'] = {
		['SA-11 Buk CC 9S470M1'] = {
			['required'] = true,
		},
	},
	['name'] = {
		['NATO'] = 'SA-17 Grizzly',
	},
	['harm_detection_chance'] = 90
}

--[[
New launcher for the SA-2 complex: S_75M_Volhov_V759
--]]
local s75launchers = samTypesDB['S-75']['launchers']
s75launchers['S_75M_Volhov_V759'] = {}

--[[
New launcher for the SA-3 complex:
--]]
local s125launchers = samTypesDB['S-125']['launchers']
s125launchers['5p73 V-601P ln'] = {}

--[[
New launcher for the SA-2 complex: HQ_2_Guideline_LN
--]]
local s125launchers = samTypesDB['S-75']['launchers']
s125launchers['HQ_2_Guideline_LN'] = {}

--[[
SA-12 Gladiator / Giant:
2021-03-19 21:24:22.620 INFO    SCRIPTING: S-300V 9S15 sr
2021-03-19 21:24:22.620 INFO    SCRIPTING: S-300V 9S19 sr
2021-03-19 21:24:22.620 INFO    SCRIPTING: S-300V 9S32 tr
2021-03-19 21:24:22.620 INFO    SCRIPTING: S-300V 9S457 cp
2021-03-19 21:24:22.620 INFO    SCRIPTING: S-300V 9A83 ln
2021-03-19 21:24:22.620 INFO    SCRIPTING: S-300V 9A82 ln
--]]
samTypesDB['S-300V'] = {
	['type'] = 'complex',
	['searchRadar'] = {
		['S-300V 9S15 sr'] = {
			['name'] = {
				['NATO'] = 'Bill Board',
			},
		},
		['S-300V 9S19 sr'] = {
			['name'] = {
				['NATO'] = 'High Screen',
			},
		},
	},
	['trackingRadar'] = {
		['S-300V 9S32 tr'] = {
			['NATO'] = 'Grill Pan',
			},
	},
	['misc'] = {
		['S-300V 9S457 cp'] = {
			['required'] = true,
		},
	},
	['launchers'] = {
		['S-300V 9A83 ln'] = {
		},
		['S-300V 9A82 ln'] = {
		},
	},
	['name']  = {
		['NATO'] = 'SA-12 Gladiator/Giant'
	},
	['harm_detection_chance'] = 90,
	['can_engage_harm'] = true
}

--[[
SA-20B Gargoyle B:

2021-03-25 19:15:02.135 INFO    SCRIPTING: S-300PMU2 64H6E2 sr
2021-03-25 19:15:02.135 INFO    SCRIPTING: S-300PMU2 92H6E tr
2021-03-25 19:15:02.135 INFO    SCRIPTING: S-300PMU2 5P85SE2 ln
2021-03-25 19:15:02.135 INFO    SCRIPTING: S-300PMU2 54K6E2 cp
--]]

samTypesDB['S-300PMU2'] = {
	['type'] = 'complex',
	['searchRadar'] = {
		['S-300PMU2 64H6E2 sr'] = {
			['name'] = {
				['NATO'] = '',
			},
		},
		['S-300PMU1 40B6MD sr'] = s300PMU140B6MDsr,
		['S-300PMU1 64N6E sr'] = s300PMU164N6Esr,
		
		['S-300PS 40B6MD sr'] = {
			['name'] = {
				['NATO'] = '',
			},
		},		
		['S-300PS 64H6E sr'] = {
			['name'] = {
				['NATO'] = '',
			},
		},
	},
	['trackingRadar'] = {
		['S-300PMU2 92H6E tr'] = {
		},
		['S-300PS 40B6M tr'] = {
		},
		['S-300PMU1 40B6M tr'] = {
		},
		['S-300PMU1 30N6E tr'] = {
		},
	},
	['misc'] = {
		['S-300PMU2 54K6E2 cp'] = {
			['required'] = true,
		},
	},
	['launchers'] = {
		['S-300PMU2 5P85SE2 ln'] = {
		},
	},
	['name']  = {
		['NATO'] = 'SA-20B Gargoyle B'
	},
	['harm_detection_chance'] = 90,
	['can_engage_harm'] = true
}

--[[

--]]
end



do

SkynetIADSLogger = {}
SkynetIADSLogger.__index = SkynetIADSLogger

function SkynetIADSLogger:create(iads)
	local logger = {}
	setmetatable(logger, SkynetIADSLogger)
	logger.debugOutput = {}
	logger.debugOutput.IADSStatus = false
	logger.debugOutput.samWentDark = false
	logger.debugOutput.contacts = false
	logger.debugOutput.radarWentLive = false
	logger.debugOutput.jammerProbability = false
	logger.debugOutput.addedEWRadar = false
	logger.debugOutput.addedSAMSite = false
	logger.debugOutput.warnings = true
	logger.debugOutput.harmDefence = false
	logger.debugOutput.samSiteStatusEnvOutput = false
	logger.debugOutput.earlyWarningRadarStatusEnvOutput = false
	logger.debugOutput.commandCenterStatusEnvOutput = false
	logger.iads = iads
	return logger
end

function SkynetIADSLogger:getDebugSettings()
	return self.debugOutput
end

function SkynetIADSLogger:printOutput(output, typeWarning)
	if typeWarning == true and self:getDebugSettings().warnings or typeWarning == nil then
		if typeWarning == true then
			output = "WARNING: "..output
		end
		trigger.action.outText(output, 4)
	end
end

function SkynetIADSLogger:printOutputToLog(output)
	env.info("SKYNET: "..output, 4)
end

function SkynetIADSLogger:printEarlyWarningRadarStatus()
	local ewRadars = self.iads:getEarlyWarningRadars()
	self:printOutputToLog("------------------------------------------ EW RADAR STATUS: "..self.iads:getCoalitionString().." -------------------------------")
	for i = 1, #ewRadars do
		local ewRadar = ewRadars[i]
		local numConnectionNodes = #ewRadar:getConnectionNodes()
		local numPowerSources = #ewRadar:getPowerSources()
		local isActive = ewRadar:isActive()
		local connectionNodes = ewRadar:getConnectionNodes()
		local firstRadar = nil
		local radars = ewRadar:getRadars()
		
		--get the first existing radar to prevent issues in calculating the distance later on:
		for i = 1, #radars do
			if radars[i]:isExist() then
				firstRadar = radars[i]
				break
			end
		
		end
		local numDamagedConnectionNodes = 0
		
		
		for j = 1, #connectionNodes do
			local connectionNode = connectionNodes[j]
			if connectionNode:isExist() == false then
				numDamagedConnectionNodes = numDamagedConnectionNodes + 1
			end
		end
		local intactConnectionNodes = numConnectionNodes - numDamagedConnectionNodes
		
		local powerSources = ewRadar:getPowerSources()
		local numDamagedPowerSources = 0
		for j = 1, #powerSources do
			local powerSource = powerSources[j]
			if powerSource:isExist() == false then
				numDamagedPowerSources = numDamagedPowerSources + 1
			end
		end
		local intactPowerSources = numPowerSources - numDamagedPowerSources 
		
		local detectedTargets = ewRadar:getDetectedTargets()
		local samSitesInCoveredArea = ewRadar:getChildRadars()
		
		local unitName = "DESTROYED"
		
		if ewRadar:getDCSRepresentation():isExist() then
			unitName = ewRadar:getDCSName()
		end
		
		self:printOutputToLog("UNIT: "..unitName.." | TYPE: "..ewRadar:getNatoName())
		self:printOutputToLog("ACTIVE: "..tostring(isActive).."| DETECTED TARGETS: "..#detectedTargets.." | DEFENDING HARM: "..tostring(ewRadar:isDefendingHARM()))
		if numConnectionNodes > 0 then
			self:printOutputToLog("CONNECTION NODES: "..numConnectionNodes.." | DAMAGED: "..numDamagedConnectionNodes.." | INTACT: "..intactConnectionNodes)
		else
			self:printOutputToLog("NO CONNECTION NODES SET")
		end
		if numPowerSources > 0 then
			self:printOutputToLog("POWER SOURCES : "..numPowerSources.." | DAMAGED:"..numDamagedPowerSources.." | INTACT: "..intactPowerSources)
		else
			self:printOutputToLog("NO POWER SOURCES SET")
		end
		
		self:printOutputToLog("SAM SITES IN COVERED AREA: "..#samSitesInCoveredArea)
		for j = 1, #samSitesInCoveredArea do
			local samSiteCovered = samSitesInCoveredArea[j]
			self:printOutputToLog(samSiteCovered:getDCSName())
		end
		
		for j = 1, #detectedTargets do
			local contact = detectedTargets[j]
			if firstRadar ~= nil and firstRadar:isExist() then
				local distance = mist.utils.round(mist.utils.metersToNM(ewRadar:getDistanceInMetersToContact(firstRadar:getDCSRepresentation(), contact:getPosition().p)), 2)
				self:printOutputToLog("CONTACT: "..contact:getName().." | TYPE: "..contact:getTypeName().." | DISTANCE NM: "..distance)
			end
		end
		
		self:printOutputToLog("---------------------------------------------------")
		
	end

end

function SkynetIADSLogger:getMetaInfo(abstractElementSupport)
	local info = {}
	info.numSources = #abstractElementSupport
	info.numDamagedSources = 0
	info.numIntactSources = 0
	for j = 1, #abstractElementSupport do
		local source = abstractElementSupport[j]
		if source:isExist() == false then
			info.numDamagedSources = info.numDamagedSources + 1
		end
	end
	info.numIntactSources = info.numSources - info.numDamagedSources
	return info
end

function SkynetIADSLogger:printSAMSiteStatus()
	local samSites = self.iads:getSAMSites()
	
	self:printOutputToLog("------------------------------------------ SAM STATUS: "..self.iads:getCoalitionString().." -------------------------------")
	for i = 1, #samSites do
		local samSite = samSites[i]
		local numConnectionNodes = #samSite:getConnectionNodes()
		local numPowerSources = #samSite:getPowerSources()
		local isAutonomous = samSite:getAutonomousState()
		local isActive = samSite:isActive()
		
		local connectionNodes = samSite:getConnectionNodes()
		local firstRadar = samSite:getRadars()[1]
		local numDamagedConnectionNodes = 0
		for j = 1, #connectionNodes do
			local connectionNode = connectionNodes[j]
			if connectionNode:isExist() == false then
				numDamagedConnectionNodes = numDamagedConnectionNodes + 1
			end
		end
		local intactConnectionNodes = numConnectionNodes - numDamagedConnectionNodes
		
		local powerSources = samSite:getPowerSources()
		local numDamagedPowerSources = 0
		for j = 1, #powerSources do
			local powerSource = powerSources[j]
			if powerSource:isExist() == false then
				numDamagedPowerSources = numDamagedPowerSources + 1
			end
		end
		local intactPowerSources = numPowerSources - numDamagedPowerSources 
		
		local detectedTargets = samSite:getDetectedTargets()
		
		local samSitesInCoveredArea = samSite:getChildRadars()
		
		local engageAirWeapons = samSite:getCanEngageAirWeapons()
		
		local engageHARMS = samSite:getCanEngageHARM()
		
		local hasAmmo = samSite:hasRemainingAmmo()
		
		self:printOutputToLog("GROUP: "..samSite:getDCSName().." | TYPE: "..samSite:getNatoName())
		self:printOutputToLog("ACTIVE: "..tostring(isActive).." | AUTONOMOUS: "..tostring(isAutonomous).." | IS ACTING AS EW: "..tostring(samSite:getActAsEW()).." | CAN ENGAGE AIR WEAPONS : "..tostring(engageAirWeapons).." | CAN ENGAGE HARMS : "..tostring(engageHARMS).." | HAS AMMO: "..tostring(hasAmmo).." | DETECTED TARGETS: "..#detectedTargets.." | DEFENDING HARM: "..tostring(samSite:isDefendingHARM()).." | MISSILES IN FLIGHT: "..tostring(samSite:getNumberOfMissilesInFlight()))
		
		if numConnectionNodes > 0 then
			self:printOutputToLog("CONNECTION NODES: "..numConnectionNodes.." | DAMAGED: "..numDamagedConnectionNodes.." | INTACT: "..intactConnectionNodes)
		else
			self:printOutputToLog("NO CONNECTION NODES SET")
		end
		if numPowerSources > 0 then
			self:printOutputToLog("POWER SOURCES : "..numPowerSources.." | DAMAGED:"..numDamagedPowerSources.." | INTACT: "..intactPowerSources)
		else
			self:printOutputToLog("NO POWER SOURCES SET")
		end
		
		self:printOutputToLog("SAM SITES IN COVERED AREA: "..#samSitesInCoveredArea)
		for j = 1, #samSitesInCoveredArea do
			local samSiteCovered = samSitesInCoveredArea[j]
			self:printOutputToLog(samSiteCovered:getDCSName())
		end
		
		for j = 1, #detectedTargets do
			local contact = detectedTargets[j]
			if firstRadar ~= nil and firstRadar:isExist() then
				local distance = mist.utils.round(mist.utils.metersToNM(samSite:getDistanceInMetersToContact(firstRadar:getDCSRepresentation(), contact:getPosition().p)), 2)
				self:printOutputToLog("CONTACT: "..contact:getName().." | TYPE: "..contact:getTypeName().." | DISTANCE NM: "..distance)
			end
		end
		
		self:printOutputToLog("---------------------------------------------------")
	end
end

function SkynetIADSLogger:printCommandCenterStatus()
	local commandCenters = self.iads:getCommandCenters()
	self:printOutputToLog("------------------------------------------ COMMAND CENTER STATUS: "..self.iads:getCoalitionString().." -------------------------------")
	
	for i = 1, #commandCenters do
		local commandCenter = commandCenters[i]
		local numConnectionNodes = #commandCenter:getConnectionNodes()
		local powerSourceInfo = self:getMetaInfo(commandCenter:getPowerSources())
		local connectionNodeInfo = self:getMetaInfo(commandCenter:getConnectionNodes())
		self:printOutputToLog("GROUP: "..commandCenter:getDCSName().." | TYPE: "..commandCenter:getNatoName())
		if connectionNodeInfo.numSources > 0 then
			self:printOutputToLog("CONNECTION NODES: "..connectionNodeInfo.numSources.." | DAMAGED: "..connectionNodeInfo.numDamagedSources.." | INTACT: "..connectionNodeInfo.numIntactSources)
		else
			self:printOutputToLog("NO CONNECTION NODES SET")
		end
		if powerSourceInfo.numSources > 0 then
			self:printOutputToLog("POWER SOURCES : "..powerSourceInfo.numSources.." | DAMAGED: "..powerSourceInfo.numDamagedSources.." | INTACT: "..powerSourceInfo.numIntactSources)
		else
			self:printOutputToLog("NO POWER SOURCES SET")
		end
		self:printOutputToLog("---------------------------------------------------")
	end
end

function SkynetIADSLogger:printSystemStatus()	

	if self:getDebugSettings().IADSStatus or self:getDebugSettings().contacts then
		local coalitionStr = self.iads:getCoalitionString()
		self:printOutput("---- IADS: "..coalitionStr.." ------")
	end
	
	if self:getDebugSettings().IADSStatus then

		local commandCenters = self.iads:getCommandCenters()
		local numComCenters = #commandCenters
		local numDestroyedComCenters = 0
		local numComCentersNoPower = 0
		local numComCentersNoConnectionNode = 0
		local numIntactComCenters = 0
		for i = 1, #commandCenters do
			local commandCenter = commandCenters[i]
			if commandCenter:hasWorkingPowerSource() == false then
				numComCentersNoPower = numComCentersNoPower + 1
			end
			if commandCenter:hasActiveConnectionNode() == false then
				numComCentersNoConnectionNode = numComCentersNoConnectionNode + 1
			end
			if commandCenter:isDestroyed() == false then
				numIntactComCenters = numIntactComCenters + 1
			end
		end
		
		numDestroyedComCenters = numComCenters - numIntactComCenters
		
		
		self:printOutput("COMMAND CENTERS: "..numComCenters.." | Destroyed: "..numDestroyedComCenters.." | NoPowr: "..numComCentersNoPower.." | NoCon: "..numComCentersNoConnectionNode)
	
		local ewNoPower = 0
		local earlyWarningRadars = self.iads:getEarlyWarningRadars()
		local ewTotal = #earlyWarningRadars
		local ewNoConnectionNode = 0
		local ewActive = 0
		local ewRadarsInactive = 0

		for i = 1, #earlyWarningRadars do
			local ewRadar = earlyWarningRadars[i]
			if ewRadar:hasWorkingPowerSource() == false then
				ewNoPower = ewNoPower + 1
			end
			if ewRadar:hasActiveConnectionNode() == false then
				ewNoConnectionNode = ewNoConnectionNode + 1
			end
			if ewRadar:isActive() then
				ewActive = ewActive + 1
			end
		end
		
		ewRadarsInactive = ewTotal - ewActive	
		local numEWRadarsDestroyed = #self.iads:getDestroyedEarlyWarningRadars()
		self:printOutput("EW: "..ewTotal.." | On: "..ewActive.." | Off: "..ewRadarsInactive.." | Destroyed: "..numEWRadarsDestroyed.." | NoPowr: "..ewNoPower.." | NoCon: "..ewNoConnectionNode)
		
		local samSitesInactive = 0
		local samSitesActive = 0
		local samSites = self.iads:getSAMSites()
		local samSitesTotal = #samSites
		local samSitesNoPower = 0
		local samSitesNoConnectionNode = 0
		local samSitesOutOfAmmo = 0
		local samSiteAutonomous = 0
		local samSiteRadarDestroyed = 0
		for i = 1, #samSites do
			local samSite = samSites[i]
			if samSite:hasWorkingPowerSource() == false then
				samSitesNoPower = samSitesNoPower + 1
			end
			if samSite:hasActiveConnectionNode() == false then
				samSitesNoConnectionNode = samSitesNoConnectionNode + 1
			end
			if samSite:isActive() then
				samSitesActive = samSitesActive + 1
			end
			if samSite:hasRemainingAmmo() == false then
				samSitesOutOfAmmo = samSitesOutOfAmmo + 1
			end
			if samSite:getAutonomousState() == true then
				samSiteAutonomous = samSiteAutonomous + 1
			end
			if samSite:hasWorkingRadar() == false then
				samSiteRadarDestroyed = samSiteRadarDestroyed + 1
			end
		end
		
		samSitesInactive = samSitesTotal - samSitesActive
		self:printOutput("SAM: "..samSitesTotal.." | On: "..samSitesActive.." | Off: "..samSitesInactive.." | Autonm: "..samSiteAutonomous.." | Raddest: "..samSiteRadarDestroyed.." | NoPowr: "..samSitesNoPower.." | NoCon: "..samSitesNoConnectionNode.." | NoAmmo: "..samSitesOutOfAmmo)
	end
	
	if self:getDebugSettings().contacts then
		local contacts = self.iads:getContacts()
		if contacts then
			for i = 1, #contacts do
				local contact = contacts[i]
					self:printOutput("CONTACT: "..contact:getName().." | TYPE: "..contact:getTypeName().." | GS: "..tostring(contact:getGroundSpeedInKnots()).." | LAST SEEN: "..contact:getAge())
			end
		end
	end
	
	if self:getDebugSettings().commandCenterStatusEnvOutput then
		self:printCommandCenterStatus()
	end

	if self:getDebugSettings().earlyWarningRadarStatusEnvOutput then
		self:printEarlyWarningRadarStatus()
	end
	
	if self:getDebugSettings().samSiteStatusEnvOutput then
		self:printSAMSiteStatus()
	end

end

end
do

SkynetIADS = {}
SkynetIADS.__index = SkynetIADS

SkynetIADS.database = samTypesDB

function SkynetIADS:create(name)
	local iads = {}
	setmetatable(iads, SkynetIADS)
	iads.radioMenu = nil
	iads.earlyWarningRadars = {}
	iads.samSites = {}
	iads.commandCenters = {}
	iads.ewRadarScanMistTaskID = nil
	iads.coalition = nil
	iads.contacts = {}
	iads.maxTargetAge = 32
	iads.name = name
	iads.harmDetection = SkynetIADSHARMDetection:create(iads)
	iads.logger = SkynetIADSLogger:create(iads)
	if iads.name == nil then
		iads.name = ""
	end
	iads.contactUpdateInterval = 5
	return iads
end

function SkynetIADS:setUpdateInterval(interval)
	self.contactUpdateInterval = interval
end

function SkynetIADS:setCoalition(item)
	if item then
		local coalitionID = item:getCoalition()
		if self.coalitionID == nil then
			self.coalitionID = coalitionID
		end
		if self.coalitionID ~= coalitionID then
			self:printOutputToLog("element: "..item:getName().." has a different coalition than the IADS", true)
		end
	end
end

function SkynetIADS:addJammer(jammer)
	table.insert(self.jammers, jammer)
end

function SkynetIADS:getCoalition()
	return self.coalitionID
end

function SkynetIADS:getDestroyedEarlyWarningRadars()
	local destroyedSites = {}
	for i = 1, #self.earlyWarningRadars do
		local ewSite = self.earlyWarningRadars[i]
		if ewSite:isDestroyed() then
			table.insert(destroyedSites, ewSite)
		end
	end
	return destroyedSites
end

function SkynetIADS:getUsableAbstractRadarElemtentsOfTable(abstractRadarTable)
	local usable = {}
	for i = 1, #abstractRadarTable do
		local abstractRadarElement = abstractRadarTable[i]
		if abstractRadarElement:hasActiveConnectionNode() and abstractRadarElement:hasWorkingPowerSource() and abstractRadarElement:isDestroyed() == false then
			table.insert(usable, abstractRadarElement)
		end
	end
	return usable
end

function SkynetIADS:getUsableEarlyWarningRadars()
	return self:getUsableAbstractRadarElemtentsOfTable(self.earlyWarningRadars)
end

function SkynetIADS:createTableDelegator(units) 
	local sites = SkynetIADSTableDelegator:create()
	for i = 1, #units do
		local site = units[i]
		table.insert(sites, site)
	end
	return sites
end

function SkynetIADS:addEarlyWarningRadarsByPrefix(prefix)
	self:deactivateEarlyWarningRadars()
	self.earlyWarningRadars = {}
	for unitName, unit in pairs(mist.DBs.unitsByName) do
		local pos = self:findSubString(unitName, prefix)
		--somehow the MIST unit db contains StaticObject, we check to see we only add Units
		local unit = Unit.getByName(unitName)
		if pos and pos == 1 and unit then
			self:addEarlyWarningRadar(unitName)
		end
	end
	return self:createTableDelegator(self.earlyWarningRadars)
end

function SkynetIADS:addEarlyWarningRadar(earlyWarningRadarUnitName)
	local earlyWarningRadarUnit = Unit.getByName(earlyWarningRadarUnitName)
	if earlyWarningRadarUnit == nil then
		self:printOutputToLog("you have added an EW Radar that does not exist, check name of Unit in Setup and Mission editor: "..earlyWarningRadarUnitName, true)
		return
	end
	self:setCoalition(earlyWarningRadarUnit)
	local ewRadar = nil
	local category = earlyWarningRadarUnit:getDesc().category
	if category == Unit.Category.AIRPLANE or category == Unit.Category.SHIP then
		ewRadar = SkynetIADSAWACSRadar:create(earlyWarningRadarUnit, self)
	else
		ewRadar = SkynetIADSEWRadar:create(earlyWarningRadarUnit, self)
	end
	ewRadar:setupElements()
	ewRadar:setCachedTargetsMaxAge(self:getCachedTargetsMaxAge())	
	-- for performance improvement, if iads is not scanning no update coverage update needs to be done, will be executed once when iads activates
	if self.ewRadarScanMistTaskID ~= nil then
		self:buildRadarCoverageForEarlyWarningRadar(ewRadar)
	end
	ewRadar:setActAsEW(true)
	ewRadar:setToCorrectAutonomousState()
	ewRadar:goLive()
	table.insert(self.earlyWarningRadars, ewRadar)
	if self:getDebugSettings().addedEWRadar then
			self:printOutputToLog("ADDED: "..ewRadar:getDescription())
	end
	return ewRadar
end

function SkynetIADS:getCachedTargetsMaxAge()
	return self.contactUpdateInterval
end

function SkynetIADS:getEarlyWarningRadars()
	return self:createTableDelegator(self.earlyWarningRadars)
end

function SkynetIADS:getEarlyWarningRadarByUnitName(unitName)
	for i = 1, #self.earlyWarningRadars do
		local ewRadar = self.earlyWarningRadars[i]
		if ewRadar:getDCSName() == unitName then
			return ewRadar
		end
	end
end

function SkynetIADS:findSubString(haystack, needle)
	return string.find(haystack, needle, 1, true)
end

function SkynetIADS:addSAMSitesByPrefix(prefix)
	self:deativateSAMSites()
	self.samSites = {}
	for groupName, groupData in pairs(mist.DBs.groupsByName) do
		local pos = self:findSubString(groupName, prefix)
		if pos and pos == 1 then
			--mist returns groups, units and, StaticObjects
			local dcsObject = Group.getByName(groupName)
			if dcsObject then
				self:addSAMSite(groupName)
			end
		end
	end
	return self:createTableDelegator(self.samSites)
end

function SkynetIADS:getSAMSitesByPrefix(prefix)
	local returnSams = {}
	for i = 1, #self.samSites do
		local samSite = self.samSites[i]
		local groupName = samSite:getDCSName()
		local pos = self:findSubString(groupName, prefix)
		if pos and pos == 1 then
			table.insert(returnSams, samSite)
		end
	end
	return self:createTableDelegator(returnSams)
end

function SkynetIADS:addSAMSite(samSiteName)
	local samSiteDCS = Group.getByName(samSiteName)
	if samSiteDCS == nil then
		self:printOutputToLog("you have added an SAM Site that does not exist, check name of Group in Setup and Mission editor: "..tostring(samSiteName), true)
		return
	end
	self:setCoalition(samSiteDCS)
	local samSite = SkynetIADSSamSite:create(samSiteDCS, self)
	samSite:setupElements()
	samSite:setCanEngageAirWeapons(true)
	samSite:goLive()
	samSite:setCachedTargetsMaxAge(self:getCachedTargetsMaxAge())
	if samSite:getNatoName() == "UNKNOWN" then
		self:printOutputToLog("you have added an SAM site that Skynet IADS can not handle: "..samSite:getDCSName(), true)
		samSite:cleanUp()
	else
		samSite:goDark()
		table.insert(self.samSites, samSite)
		if self:getDebugSettings().addedSAMSite then
			self:printOutputToLog("ADDED: "..samSite:getDescription())
		end
		-- for performance improvement, if iads is not scanning no update coverage update needs to be done, will be executed once when iads activates
		if self.ewRadarScanMistTaskID ~= nil then
			self:buildRadarCoverageForSAMSite(samSite)
		end
		return samSite
	end 
end

function SkynetIADS:getUsableSAMSites()
	return self:getUsableAbstractRadarElemtentsOfTable(self.samSites)
end

function SkynetIADS:getDestroyedSAMSites()
	local destroyedSites = {}
	for i = 1, #self.samSites do
		local samSite = self.samSites[i]
		if samSite:isDestroyed() then
			table.insert(destroyedSites, samSite)
		end
	end
	return destroyedSites
end

function SkynetIADS:getSAMSites()
	return self:createTableDelegator(self.samSites)
end

function SkynetIADS:getActiveSAMSites()
	local activeSAMSites = {}
	for i = 1, #self.samSites do
		if self.samSites[i]:isActive() then
			table.insert(activeSAMSites, self.samSites[i])
		end
	end
	return activeSAMSites
end

function SkynetIADS:getSAMSiteByGroupName(groupName)
	for i = 1, #self.samSites do
		local samSite = self.samSites[i]
		if samSite:getDCSName() == groupName then
			return samSite
		end
	end
end

function SkynetIADS:getSAMSitesByNatoName(natoName)
	local selectedSAMSites = SkynetIADSTableDelegator:create()
	for i = 1, #self.samSites do
		local samSite = self.samSites[i]
		if samSite:getNatoName() == natoName then
			table.insert(selectedSAMSites, samSite)
		end
	end
	return selectedSAMSites
end

function SkynetIADS:addCommandCenter(commandCenter)
	self:setCoalition(commandCenter)
	local comCenter = SkynetIADSCommandCenter:create(commandCenter, self)
	table.insert(self.commandCenters, comCenter)
	-- when IADS is active the radars will be added to the new command center. If it not active this will happen when radar coverage is built
	if self.ewRadarScanMistTaskID ~= nil then
		self:addRadarsToCommandCenters()
	end
	return comCenter
end

function SkynetIADS:isCommandCenterUsable()
	if #self:getCommandCenters() == 0 then
		return true
	end
	local usableComCenters = self:getUsableAbstractRadarElemtentsOfTable(self:getCommandCenters())
	return (#usableComCenters > 0)
end

function SkynetIADS:getCommandCenters()
	return self.commandCenters
end


function SkynetIADS.evaluateContacts(self)

	local ewRadars = self:getUsableEarlyWarningRadars()
	local samSites = self:getUsableSAMSites()
	
	--will add SAM Sites acting as EW Rardars to the ewRadars array:
	for i = 1, #samSites do
		local samSite = samSites[i]
		--We inform SAM sites that a target update is about to happen. If they have no targets in range after the cycle they go dark
		samSite:targetCycleUpdateStart()
		if samSite:getActAsEW() then
			table.insert(ewRadars, samSite)
		end
		--if the sam site is not in ew mode and active we grab the detected targets right here
		if samSite:isActive() and samSite:getActAsEW() == false then
			local contacts = samSite:getDetectedTargets()
			for j = 1, #contacts do
				local contact = contacts[j]
				self:mergeContact(contact)
			end
		end
	end

	local samSitesToTrigger = {}
	
	for i = 1, #ewRadars do
		local ewRadar = ewRadars[i]
		--call go live in case ewRadar had to shut down (HARM attack)
		ewRadar:goLive()
		-- if an awacs has traveled more than a predeterminded distance we update the autonomous state of the SAMs
		if getmetatable(ewRadar) == SkynetIADSAWACSRadar and ewRadar:isUpdateOfAutonomousStateOfSAMSitesRequired() then
			self:buildRadarCoverageForEarlyWarningRadar(ewRadar)
		end
		local ewContacts = ewRadar:getDetectedTargets()
		if #ewContacts > 0 then
			local samSitesUnderCoverage = ewRadar:getUsableChildRadars()
			for j = 1, #samSitesUnderCoverage do
				local samSiteUnterCoverage = samSitesUnderCoverage[j]
				-- only if a SAM site is not active we add it to the hash of SAM sites to be iterated later on
				if samSiteUnterCoverage:isActive() == false then
					--we add them to a hash to make sure each SAM site is in the collection only once, reducing the number of loops we conduct later on
					samSitesToTrigger[samSiteUnterCoverage:getDCSName()] = samSiteUnterCoverage
				end
			end
			for j = 1, #ewContacts do
				local contact = ewContacts[j]
				self:mergeContact(contact)
			end
		end
	end

	self:cleanAgedTargets()
	
	for samName, samToTrigger in pairs(samSitesToTrigger) do
		for j = 1, #self.contacts do
			local contact = self.contacts[j]
			-- the DCS Radar only returns enemy aircraft, if that should change a coalition check will be required
			-- currently every type of object in the air is handed of to the SAM site, including missiles
			local description = contact:getDesc()
			local category = description.category
			if category and category ~= Unit.Category.GROUND_UNIT and category ~= Unit.Category.SHIP and category ~= Unit.Category.STRUCTURE then
				samToTrigger:informOfContact(contact)
			end
		end
	end
	
	for i = 1, #samSites do
		local samSite = samSites[i]
		samSite:targetCycleUpdateEnd()
	end
	
	self.harmDetection:setContacts(self:getContacts())
	self.harmDetection:evaluateContacts()
	
	self.logger:printSystemStatus()
end

function SkynetIADS:cleanAgedTargets()
	local contactsToKeep = {}
	for i = 1, #self.contacts do
		local contact = self.contacts[i]
		if contact:getAge() < self.maxTargetAge then
			table.insert(contactsToKeep, contact)
		end
	end
	self.contacts = contactsToKeep
end

--TODO unit test this method:
function SkynetIADS:getAbstracRadarElements()
	local abstractRadarElements = {}
	local ewRadars = self:getEarlyWarningRadars()
	local samSites = self:getSAMSites()
	
	for i = 1, #ewRadars do
		local ewRadar = ewRadars[i]
		table.insert(abstractRadarElements, ewRadar)
	end
	
	for i = 1, #samSites do
		local samSite = samSites[i]
		table.insert(abstractRadarElements, samSite)
	end
	return abstractRadarElements
end


function SkynetIADS:addRadarsToCommandCenters()

	--we clear any existing radars that may have been added earlier
	local comCenters = self:getCommandCenters()
	for i = 1, #comCenters do
		local comCenter = comCenters[i]
		comCenter:clearChildRadars()
	end	
	
	-- then we add child radars to the command centers
	local abstractRadarElements = self:getAbstracRadarElements()
		for i = 1, #abstractRadarElements do
			local abstractRadar = abstractRadarElements[i]
			self:addSingleRadarToCommandCenters(abstractRadar)
		end
end

function SkynetIADS:addSingleRadarToCommandCenters(abstractRadarElement)
	local comCenters = self:getCommandCenters()
	for i = 1, #comCenters do
		local comCenter = comCenters[i]
		comCenter:addChildRadar(abstractRadarElement)
	end	
end

-- this method rebuilds the radar coverage of the IADS, a complete rebuild is only required the first time the IADS is activated
-- during runtime it is sufficient to call buildRadarCoverageForSAMSite or buildRadarCoverageForEarlyWarningRadar method that just updates the IADS for one unit, this saves script execution time
function SkynetIADS:buildRadarCoverage()	
	
	--to build the basic radar coverage we use all SAM sites. Checks if SAM site has power or a connection node is done when using the SAM site later on
	local samSites = self:getSAMSites()
	
	--first we clear all child and parent radars that may have been added previously
	for i = 1, #samSites do
		local samSite = samSites[i]
		samSite:clearChildRadars()
		samSite:clearParentRadars()
	end
	
	local ewRadars = self:getEarlyWarningRadars()
	
	for i = 1, #ewRadars do
		local ewRadar = ewRadars[i]
		ewRadar:clearChildRadars()
	end	
	
	--then we rebuild the radar coverage
	local abstractRadarElements = self:getAbstracRadarElements()
	for i = 1, #abstractRadarElements do
		local abstract = abstractRadarElements[i]
		self:buildRadarCoverageForAbstractRadarElement(abstract)
	end
	
	self:addRadarsToCommandCenters()
	
	--we call this once on all sam sites, to make sure autonomous sites go live when IADS activates
	for i = 1, #samSites do
		local samSite = samSites[i]
		samSite:informChildrenOfStateChange()
	end

end

function SkynetIADS:buildRadarCoverageForAbstractRadarElement(abstractRadarElement)
	local abstractRadarElements = self:getAbstracRadarElements()
	for i = 1, #abstractRadarElements do
		local aElementToCompare = abstractRadarElements[i]
		if aElementToCompare ~= abstractRadarElement then
			if abstractRadarElement:isInRadarDetectionRangeOf(aElementToCompare) then
				self:buildRadarAssociation(aElementToCompare, abstractRadarElement)
			end
			if aElementToCompare:isInRadarDetectionRangeOf(abstractRadarElement) then
				self:buildRadarAssociation(abstractRadarElement, aElementToCompare)
			end
		end
	end
end

function SkynetIADS:buildRadarAssociation(parent, child)
	--chilren should only be SAM sites not EW radars
	if ( getmetatable(child) == SkynetIADSSamSite ) then
		parent:addChildRadar(child)
	end
	--Only SAM Sites should have parent Radars, not EW Radars
	if ( getmetatable(child) == SkynetIADSSamSite ) then
		child:addParentRadar(parent)
	end
end

function SkynetIADS:buildRadarCoverageForSAMSite(samSite)
	self:buildRadarCoverageForAbstractRadarElement(samSite)
	self:addSingleRadarToCommandCenters(samSite)
end

function SkynetIADS:buildRadarCoverageForEarlyWarningRadar(ewRadar)
	self:buildRadarCoverageForAbstractRadarElement(ewRadar)
	self:addSingleRadarToCommandCenters(ewRadar)
end

function SkynetIADS:mergeContact(contact)
	local existingContact = false
	for i = 1, #self.contacts do
		local iadsContact = self.contacts[i]
		if iadsContact:getName() == contact:getName() then
			iadsContact:refresh()
			--these contacts are used in the logger we set a kown harm state of a contact coming from a SAM site. So the logger will show them als HARMs
			contact:setHARMState(iadsContact:getHARMState())
			local radars = contact:getAbstractRadarElementsDetected()
			for j = 1, #radars do
				local radar = radars[j]
				iadsContact:addAbstractRadarElementDetected(radar)
			end
			existingContact = true
		end
	end
	if existingContact == false then
		table.insert(self.contacts, contact)
	end
end


function SkynetIADS:getContacts()
	return self.contacts
end

function SkynetIADS:getDebugSettings()
	return self.logger.debugOutput
end

function SkynetIADS:printOutput(output, typeWarning)
	self.logger:printOutput(output, typeWarning)
end

function SkynetIADS:printOutputToLog(output)
	self.logger:printOutputToLog(output)
end

-- will start going through the Early Warning Radars and SAM sites to check what targets they have detected
function SkynetIADS.activate(self)
	mist.removeFunction(self.ewRadarScanMistTaskID)
	self.ewRadarScanMistTaskID = mist.scheduleFunction(SkynetIADS.evaluateContacts, {self}, 1, self.contactUpdateInterval)
	self:buildRadarCoverage()
end

function SkynetIADS:setupSAMSitesAndThenActivate(setupTime)
	self:activate()
	self.iads:printOutputToLog("DEPRECATED: setupSAMSitesAndThenActivate, no longer needed since using enableEmission instead of AI on / off allows for the Ground units to setup with their radars turned off")
end

function SkynetIADS:deactivate()
	mist.removeFunction(self.ewRadarScanMistTaskID)
	mist.removeFunction(self.samSetupMistTaskID)
	self:deativateSAMSites()
	self:deactivateEarlyWarningRadars()
	self:deactivateCommandCenters()
end

function SkynetIADS:deactivateCommandCenters()
	for i = 1, #self.commandCenters do
		local comCenter = self.commandCenters[i]
		comCenter:cleanUp()
	end
end

function SkynetIADS:deativateSAMSites()
	for i = 1, #self.samSites do
		local samSite = self.samSites[i]
		samSite:cleanUp()
	end
end

function SkynetIADS:deactivateEarlyWarningRadars()
	for i = 1, #self.earlyWarningRadars do
		local ewRadar = self.earlyWarningRadars[i]
		ewRadar:cleanUp()
	end
end	

function SkynetIADS:addRadioMenu()
	self.radioMenu = missionCommands.addSubMenu('SKYNET IADS '..self:getCoalitionString())
	local displayIADSStatus = missionCommands.addCommand('show IADS Status', self.radioMenu, SkynetIADS.updateDisplay, {self = self, value = true, option = 'IADSStatus'})
	local displayIADSStatus = missionCommands.addCommand('hide IADS Status', self.radioMenu, SkynetIADS.updateDisplay, {self = self, value = false, option = 'IADSStatus'})
	local displayIADSStatus = missionCommands.addCommand('show contacts', self.radioMenu, SkynetIADS.updateDisplay, {self = self, value = true, option = 'contacts'})
	local displayIADSStatus = missionCommands.addCommand('hide contacts', self.radioMenu, SkynetIADS.updateDisplay, {self = self, value = false, option = 'contacts'})
end

function SkynetIADS:removeRadioMenu()
	missionCommands.removeItem(self.radioMenu)
end

function SkynetIADS.updateDisplay(params)
	local option = params.option
	local self = params.self
	local value = params.value
	if option == 'IADSStatus' then
		self:getDebugSettings()[option] = value
	elseif option == 'contacts' then
		self:getDebugSettings()[option] = value
	end
end

function SkynetIADS:getCoalitionString()
	local coalitionStr = "RED"
	if self.coalitionID == coalition.side.BLUE then
		coalitionStr = "BLUE"
	elseif self.coalitionID == coalition.side.NEUTRAL then
		coalitionStr = "NEUTRAL"
	end
		
	if self.name then
		coalitionStr = "COALITION: "..coalitionStr.." | NAME: "..self.name
	end
	
	return coalitionStr
end

function SkynetIADS:getMooseConnector()
	if self.mooseConnector == nil then
		self.mooseConnector = SkynetMooseA2ADispatcherConnector:create(self)
	end
	return self.mooseConnector
end

function SkynetIADS:addMooseSetGroup(mooseSetGroup)
	self:getMooseConnector():addMooseSetGroup(mooseSetGroup)
end

end
do

SkynetMooseA2ADispatcherConnector = {}

function SkynetMooseA2ADispatcherConnector:create(iads)
	local instance = {}
	setmetatable(instance, self)
	self.__index = self
	instance.iadsCollection = {}
	instance.mooseGroups = {}
	instance.ewRadarGroupNames = {}
	instance.samSiteGroupNames = {}
	table.insert(instance.iadsCollection, iads)
	return instance
end

function SkynetMooseA2ADispatcherConnector:addIADS(iads)
	table.insert(self.iadsCollection, iads)
end

function SkynetMooseA2ADispatcherConnector:addMooseSetGroup(mooseSetGroup)
	table.insert(self.mooseGroups, mooseSetGroup)
	self:update()
end

function SkynetMooseA2ADispatcherConnector:getEarlyWarningRadarGroupNames()
	self.ewRadarGroupNames = {}
	for i = 1, #self.iadsCollection do
		local ewRadars = self.iadsCollection[i]:getUsableEarlyWarningRadars()
		for j = 1, #ewRadars do
			local ewRadar = ewRadars[j]
			table.insert(self.ewRadarGroupNames, ewRadar:getDCSRepresentation():getGroup():getName())
		end
	end
	return self.ewRadarGroupNames
end

function SkynetMooseA2ADispatcherConnector:getSAMSiteGroupNames()
	self.samSiteGroupNames = {}
	for i = 1, #self.iadsCollection do
		local samSites = self.iadsCollection[i]:getUsableSAMSites()
		for j = 1, #samSites do
			local samSite = samSites[j]
			table.insert(self.samSiteGroupNames, samSite:getDCSName())
		end
	end
	return self.samSiteGroupNames
end

function SkynetMooseA2ADispatcherConnector:update()
	
	--mooseGroup elements are type of:
	--https://flightcontrol-master.github.io/MOOSE_DOCS_DEVELOP/Documentation/Core.Set.html##(SET_GROUP)
	
	--remove previously set group names:
	for i = 1, #self.mooseGroups do
		local mooseGroup = self.mooseGroups[i]
		mooseGroup:RemoveGroupsByName(self.ewRadarGroupNames)
		mooseGroup:RemoveGroupsByName(self.samSiteGroupNames)
	end
	
	--add group names of IADS radars that are currently usable by the IADS:
	for i = 1, #self.mooseGroups do
		local mooseGroup = self.mooseGroups[i]
		mooseGroup:AddGroupsByName(self:getEarlyWarningRadarGroupNames())
		mooseGroup:AddGroupsByName(self:getSAMSiteGroupNames())
	end
end

end
do


SkynetIADSTableDelegator = {}

function SkynetIADSTableDelegator:create()
	local instance = {}
	local forwarder = {}
	forwarder.__index = function(tbl, name)
		tbl[name] = function(self, ...)
				for i = 1, #self do
					self[i][name](self[i], ...)
				end
				return self
			end
		return tbl[name]
	end
	setmetatable(instance, forwarder)
	instance.__index = forwarder
	return instance
end

end
do

SkynetIADSAbstractDCSObjectWrapper = {}

function SkynetIADSAbstractDCSObjectWrapper:create(dcsRepresentation)
	local instance = {}
	setmetatable(instance, self)
	self.__index = self
	instance.dcsName = ""
	instance.typeName = ""
	instance:setDCSRepresentation(dcsRepresentation)
	if getmetatable(dcsRepresentation) ~= Group then
		instance.typeName = dcsRepresentation:getTypeName()
	end
	return instance
end

function SkynetIADSAbstractDCSObjectWrapper:setDCSRepresentation(representation)
	self.dcsRepresentation = representation
	if self.dcsRepresentation then
		self.dcsName = self:getDCSRepresentation():getName()
	end
end

function SkynetIADSAbstractDCSObjectWrapper:getDCSRepresentation()
	return self.dcsRepresentation
end

function SkynetIADSAbstractDCSObjectWrapper:getName()
	return self.dcsName
end

function SkynetIADSAbstractDCSObjectWrapper:getTypeName()
	return self.typeName
end

function SkynetIADSAbstractDCSObjectWrapper:getPosition()
	return self.dcsRepresentation:getPosition()
end

function SkynetIADSAbstractDCSObjectWrapper:isExist()
	if self.dcsRepresentation then
		return self.dcsRepresentation:isExist()
	else
		return false
	end
end

function SkynetIADSAbstractDCSObjectWrapper:insertToTableIfNotAlreadyAdded(tbl, object)
	local isAdded = false
	for i = 1, #tbl do
		local child = tbl[i]
		if child == object then
			isAdded = true
		end
	end
	if isAdded == false then
		table.insert(tbl, object)
	end
	return not isAdded
end

-- helper code for class inheritance
function inheritsFrom( baseClass )

    local new_class = {}
    local class_mt = { __index = new_class }

    function new_class:create()
        local newinst = {}
        setmetatable( newinst, class_mt )
        return newinst
    end

    if nil ~= baseClass then
        setmetatable( new_class, { __index = baseClass } )
    end

    -- Implementation of additional OO properties starts here --

    -- Return the class object of the instance
    function new_class:class()
        return new_class
    end

    -- Return the super class object of the instance
    function new_class:superClass()
        return baseClass
    end

    -- Return true if the caller is an instance of theClass
    function new_class:isa( theClass )
        local b_isa = false

        local cur_class = new_class

        while ( nil ~= cur_class ) and ( false == b_isa ) do
            if cur_class == theClass then
                b_isa = true
            else
                cur_class = cur_class:superClass()
            end
        end

        return b_isa
    end

    return new_class
end


end

do

SkynetIADSAbstractElement = {}
SkynetIADSAbstractElement = inheritsFrom(SkynetIADSAbstractDCSObjectWrapper)

function SkynetIADSAbstractElement:create(dcsRepresentation, iads)
	local instance = self:superClass():create(dcsRepresentation)
	setmetatable(instance, self)
	self.__index = self
	instance.connectionNodes = {}
	instance.powerSources = {}
	instance.iads = iads
	instance.natoName = "UNKNOWN"
	world.addEventHandler(instance)
	return instance
end

function SkynetIADSAbstractElement:removeEventHandlers()
	world.removeEventHandler(self)
end

function SkynetIADSAbstractElement:cleanUp()
	self:removeEventHandlers()
end

function SkynetIADSAbstractElement:isDestroyed()
	return self:getDCSRepresentation():isExist() == false
end

function SkynetIADSAbstractElement:addPowerSource(powerSource)
	table.insert(self.powerSources, powerSource)
	self:informChildrenOfStateChange()
	return self
end

function SkynetIADSAbstractElement:getPowerSources()
	return self.powerSources
end

function SkynetIADSAbstractElement:addConnectionNode(connectionNode)
	table.insert(self.connectionNodes, connectionNode)
	self:informChildrenOfStateChange()
	return self
end

function SkynetIADSAbstractElement:getConnectionNodes()
	return self.connectionNodes
end

function SkynetIADSAbstractElement:hasActiveConnectionNode()
	local connectionNode = self:genericCheckOneObjectIsAlive(self.connectionNodes)
	if connectionNode == false and self.iads:getDebugSettings().samNoConnection then
		self.iads:printOutput(self:getDescription().." no connection to Command Center")
	end
	return connectionNode
end

function SkynetIADSAbstractElement:hasWorkingPowerSource()
	local power = self:genericCheckOneObjectIsAlive(self.powerSources)
	if power == false and self.iads:getDebugSettings().hasNoPower then
		self.iads:printOutput(self:getDescription().." has no power")
	end
	return power
end

function SkynetIADSAbstractElement:getDCSName()
	return self.dcsName
end

-- generic function to theck if power plants, command centers, connection nodes are still alive
function SkynetIADSAbstractElement:genericCheckOneObjectIsAlive(objects)
	local isAlive = (#objects == 0)
	for i = 1, #objects do
		local object = objects[i]
		--if we find one object that is not fully destroyed we assume the IADS is still working
		if object:isExist() then
			isAlive = true
			break
		end
	end
	return isAlive
end

function SkynetIADSAbstractElement:getNatoName()
	return self.natoName
end

function SkynetIADSAbstractElement:getDescription()
	return "IADS ELEMENT: "..self:getDCSName().." | Type: "..tostring(self:getNatoName())
end

function SkynetIADSAbstractElement:onEvent(event)
	--if a unit is destroyed we check to see if its a power plant powering the unit or a connection node
	if event.id == world.event.S_EVENT_DEAD then
		if self:hasWorkingPowerSource() == false or self:isDestroyed() then
			self:goDark()
			self:informChildrenOfStateChange()
		end
		if self:hasActiveConnectionNode() == false then
			self:informChildrenOfStateChange()
		end
	end
	if event.id == world.event.S_EVENT_SHOT then
		self:weaponFired(event)
	end
end

--placeholder method, can be implemented by subclasses
function SkynetIADSAbstractElement:weaponFired(event)
	
end

--placeholder method, can be implemented by subclasses
function SkynetIADSAbstractElement:goDark()
	
end

--placeholder method, can be implemented by subclasses
function SkynetIADSAbstractElement:goAutonomous()

end

--placeholder method, can be implemented by subclasses
function SkynetIADSAbstractElement:setToCorrectAutonomousState()

end

--placeholder method, can be implemented by subclasses
function SkynetIADSAbstractElement:informChildrenOfStateChange()
	
end

end
do

SkynetIADSAbstractRadarElement = {}
SkynetIADSAbstractRadarElement = inheritsFrom(SkynetIADSAbstractElement)

SkynetIADSAbstractRadarElement.AUTONOMOUS_STATE_DCS_AI = 1
SkynetIADSAbstractRadarElement.AUTONOMOUS_STATE_DARK = 2

SkynetIADSAbstractRadarElement.GO_LIVE_WHEN_IN_KILL_ZONE = 1
SkynetIADSAbstractRadarElement.GO_LIVE_WHEN_IN_SEARCH_RANGE = 2

SkynetIADSAbstractRadarElement.HARM_TO_SAM_ASPECT = 15
SkynetIADSAbstractRadarElement.HARM_LOOKAHEAD_NM = 20

function SkynetIADSAbstractRadarElement:create(dcsElementWithRadar, iads)
	local instance = self:superClass():create(dcsElementWithRadar, iads)
	setmetatable(instance, self)
	self.__index = self
	instance.aiState = false
	instance.harmScanID = nil
	instance.harmSilenceID = nil
	instance.lastJammerUpdate = 0
	instance.objectsIdentifiedAsHarms = {}
	instance.objectsIdentifiedAsHarmsMaxTargetAge = 60
	instance.launchers = {}
	instance.trackingRadars = {}
	instance.searchRadars = {}
	instance.parentRadars = {}
	instance.childRadars = {}
	instance.missilesInFlight = {}
	instance.pointDefences = {}
	instance.harmDecoys = {}
	instance.autonomousBehaviour = SkynetIADSAbstractRadarElement.AUTONOMOUS_STATE_DCS_AI
	instance.goLiveRange = SkynetIADSAbstractRadarElement.GO_LIVE_WHEN_IN_KILL_ZONE
	instance.isAutonomous = true
	instance.harmDetectionChance = 0
	instance.minHarmShutdownTime = 0
	instance.maxHarmShutDownTime = 0
	instance.minHarmPresetShutdownTime = 30
	instance.maxHarmPresetShutdownTime = 180
	instance.harmShutdownTime = 0
	instance.firingRangePercent = 100
	instance.actAsEW = false
	instance.cachedTargets = {}
	instance.cachedTargetsMaxAge = 1
	instance.cachedTargetsCurrentAge = 0
	instance.goLiveTime = 0
	instance.engageAirWeapons = false
	instance.isAPointDefence = false
	instance.canEngageHARM = false
	instance.dataBaseSupportedTypesCanEngageHARM = false
	-- 5 seconds seems to be a good value for the sam site to find the target with its organic radar
	instance.noCacheActiveForSecondsAfterGoLive = 5
	return instance
end

--TODO: this method could be updated to only return Radar weapons fired, this way a SAM firing an IR weapon could go dark faster in the goDark() method
function SkynetIADSAbstractRadarElement:weaponFired(event)
	if event.id == world.event.S_EVENT_SHOT then
		local weapon = event.weapon
		local launcherFired = event.initiator
		for i = 1, #self.launchers do
			local launcher = self.launchers[i]
			if launcher:getDCSRepresentation() == launcherFired then
				table.insert(self.missilesInFlight, weapon)
			end
		end
	end
end

function SkynetIADSAbstractRadarElement:setCachedTargetsMaxAge(maxAge)
	self.cachedTargetsMaxAge = maxAge
end

function SkynetIADSAbstractRadarElement:cleanUp()
	for i = 1, #self.pointDefences do
		local pointDefence = self.pointDefences[i]
		pointDefence:cleanUp()
	end
	mist.removeFunction(self.harmScanID)
	mist.removeFunction(self.harmSilenceID)
	--call method from super class
	self:removeEventHandlers()
end

function SkynetIADSAbstractRadarElement:setIsAPointDefence(state)
	if (state == true or state == false) then
		self.isAPointDefence = state
	end
end

function SkynetIADSAbstractRadarElement:getIsAPointDefence()
	return self.isAPointDefence
end

function SkynetIADSAbstractRadarElement:addPointDefence(pointDefence)
	table.insert(self.pointDefences, pointDefence)
	pointDefence:setIsAPointDefence(true)
	return self
end

function SkynetIADSAbstractRadarElement:getPointDefences()
	return self.pointDefences
end

function SkynetIADSAbstractRadarElement:addHARMDecoy(harmDecoy)
	table.insert(self.harmDecoys, harmDecoy)
end

function SkynetIADSAbstractRadarElement:addParentRadar(parentRadar)
	self:insertToTableIfNotAlreadyAdded(self.parentRadars, parentRadar)
	self:informChildrenOfStateChange()
end

function SkynetIADSAbstractRadarElement:getParentRadars()
	return self.parentRadars
end

function SkynetIADSAbstractRadarElement:clearParentRadars()
	self.parentRadars = {}
end

function SkynetIADSAbstractRadarElement:addChildRadar(childRadar)
	self:insertToTableIfNotAlreadyAdded(self.childRadars, childRadar)
end

function SkynetIADSAbstractRadarElement:getChildRadars()
	return self.childRadars
end

function SkynetIADSAbstractRadarElement:clearChildRadars()
	self.childRadars = {}
end

--TODO: unit test this method
function SkynetIADSAbstractRadarElement:getUsableChildRadars()
	local usableRadars = {}
	for i = 1, #self.childRadars do
		local childRadar = self.childRadars[i]
		if childRadar:hasWorkingPowerSource() and childRadar:hasActiveConnectionNode() then
			table.insert(usableRadars, childRadar)
		end
	end	
	return usableRadars
end

function SkynetIADSAbstractRadarElement:informChildrenOfStateChange()
	self:setToCorrectAutonomousState()
	local children = self:getChildRadars()
	for i = 1, #children do
		local childRadar = children[i]
		childRadar:setToCorrectAutonomousState()
	end
	self.iads:getMooseConnector():update()
end

function SkynetIADSAbstractRadarElement:setToCorrectAutonomousState()
	local parents = self:getParentRadars()
	for i = 1, #parents do
		local parent = parents[i]
		--of one parent exists that still is connected to the IADS, the SAM site does not have to go autonomous
		--instead of isDestroyed() write method, hasWorkingSearchRadars()
		if self:hasActiveConnectionNode() and self.iads:isCommandCenterUsable() and parent:hasWorkingPowerSource() and parent:hasActiveConnectionNode() and parent:getActAsEW() == true and parent:isDestroyed() == false then
			self:resetAutonomousState()
			return
		end
	end
	self:goAutonomous()
end


function SkynetIADSAbstractRadarElement:setAutonomousBehaviour(mode)
	if mode ~= nil then
		self.autonomousBehaviour = mode
	end
	return self
end

function SkynetIADSAbstractRadarElement:getAutonomousBehaviour()
	return self.autonomousBehaviour
end

function SkynetIADSAbstractRadarElement:resetAutonomousState()
	self.isAutonomous = false
	self:goDark()
end

function SkynetIADSAbstractRadarElement:goAutonomous()
	self.isAutonomous = true
	if self.autonomousBehaviour == SkynetIADSAbstractRadarElement.AUTONOMOUS_STATE_DARK then
		self:goDark()
	else
		self:goLive()
	end
end

function SkynetIADSAbstractRadarElement:getAutonomousState()
	return self.isAutonomous
end

function SkynetIADSAbstractRadarElement:pointDefencesHaveRemainingAmmo(minNumberOfMissiles)
	local remainingMissiles = 0
	for i = 1, #self.pointDefences do
		local pointDefence = self.pointDefences[i]
		remainingMissiles = remainingMissiles + pointDefence:getRemainingNumberOfMissiles()
	end
	return self:hasRequiredNumberOfMissiles(minNumberOfMissiles, remainingMissiles)
end

function SkynetIADSAbstractRadarElement:hasRequiredNumberOfMissiles(minNumberOfMissiles, remainingMissiles)
	local returnValue = false
	if ( remainingMissiles > 0 and remainingMissiles >= minNumberOfMissiles ) then
		returnValue = true
	end
	return returnValue
end

function SkynetIADSAbstractRadarElement:hasRemainingAmmoToEngageMissiles(minNumberOfMissiles)
	local remainingMissiles = self:getRemainingNumberOfMissiles()
	return self:hasRequiredNumberOfMissiles(minNumberOfMissiles, remainingMissiles)
end

-- this method needs to be refactored so that it works for ew radars that don't have launchers, or that it is only called by sam sites
function SkynetIADSAbstractRadarElement:hasEnoughLaunchersToEngageMissiles(minNumberOfLaunchers)
	local launchers = self:getLaunchers()
	if(launchers ~= nil) then
	 launchers = #self:getLaunchers()
	else 
		launchers = 0
	end
	return self:hasRequiredNumberOfMissiles(minNumberOfLaunchers, launchers)
end

function SkynetIADSAbstractRadarElement:pointDefencesHaveEnoughLaunchers(minNumberOfLaunchers)
	local numOfLaunchers = 0
	for i = 1, #self.pointDefences do
		local pointDefence = self.pointDefences[i]
		numOfLaunchers = numOfLaunchers + #pointDefence:getLaunchers()	
	end
	return self:hasRequiredNumberOfMissiles(minNumberOfLaunchers, numOfLaunchers)
end

function SkynetIADSAbstractRadarElement:setIgnoreHARMSWhilePointDefencesHaveAmmo(state)
	self.iads:printOutputToLog("DEPRECATED: setIgnoreHARMSWhilePointDefencesHaveAmmo SAM Site will stay live automaticall as long as itself or it's point defences can defend against a HARM")
	return self
end

function SkynetIADSAbstractRadarElement:hasMissilesInFlight()
	return #self.missilesInFlight > 0
end

function SkynetIADSAbstractRadarElement:getNumberOfMissilesInFlight()
	return #self.missilesInFlight
end

-- DCS does not send an event, when a missile is destroyed, so this method needs to be polled so that the missiles in flight are current, polling is done in the HARM Search call: evaluateIfTargetsContainHARMs
function SkynetIADSAbstractRadarElement:updateMissilesInFlight()
	local missilesInFlight = {}
	for i = 1, #self.missilesInFlight do
		local missile = self.missilesInFlight[i]
		if missile:isExist() then
			table.insert(missilesInFlight, missile)
		end
	end
	self.missilesInFlight = missilesInFlight
	self:goDarkIfOutOfAmmo()
end

function SkynetIADSAbstractRadarElement:goDarkIfOutOfAmmo()
	if self:hasRemainingAmmo() == false and self:getActAsEW() == false then
		self:goDark()
	end
end

function SkynetIADSAbstractRadarElement:getActAsEW()
	return self.actAsEW
end	

function SkynetIADSAbstractRadarElement:setActAsEW(ewState)
	if ewState == true or ewState == false then
		local stateChange = false
		if ewState ~= self.actAsEW then
			stateChange = true
		end
		self.actAsEW = ewState
		if stateChange then
			self:informChildrenOfStateChange()
		end
	end
	if self.actAsEW == true then
		self:goLive()
	else
		self:goDark()
	end
	return self
end

function SkynetIADSAbstractRadarElement:getUnitsToAnalyse()
	local units = {}
	table.insert(units, self:getDCSRepresentation())
	if getmetatable(self:getDCSRepresentation()) == Group then
		units = self:getDCSRepresentation():getUnits()
	end
	return units
end

function SkynetIADSAbstractRadarElement:getRemainingNumberOfMissiles()
	local remainingNumberOfMissiles = 0
	for i = 1, #self.launchers do
		local launcher = self.launchers[i]
		remainingNumberOfMissiles = remainingNumberOfMissiles + launcher:getRemainingNumberOfMissiles()
	end
	return remainingNumberOfMissiles
end

function SkynetIADSAbstractRadarElement:getInitialNumberOfMissiles()
	local initalNumberOfMissiles = 0
	for i = 1, #self.launchers do
		local launcher = self.launchers[i]
		initalNumberOfMissiles = launcher:getInitialNumberOfMissiles() + initalNumberOfMissiles
	end
	return initalNumberOfMissiles
end

function SkynetIADSAbstractRadarElement:getRemainingNumberOfShells()
	local remainingNumberOfShells = 0
	for i = 1, #self.launchers do
		local launcher = self.launchers[i]
		remainingNumberOfShells = remainingNumberOfShells + launcher:getRemainingNumberOfShells()
	end
	return remainingNumberOfShells
end

function SkynetIADSAbstractRadarElement:getInitialNumberOfShells()
	local initialNumberOfShells = 0
	for i = 1, #self.launchers do
		local launcher = self.launchers[i]
		initialNumberOfShells = initialNumberOfShells + launcher:getInitialNumberOfShells()
	end
	return initialNumberOfShells
end

function SkynetIADSAbstractRadarElement:hasRemainingAmmo()
	--the launcher check is due to ew radars they have no launcher and no ammo and therefore are never out of ammo
	return ( #self.launchers == 0 ) or ((self:getRemainingNumberOfMissiles() > 0 ) or ( self:getRemainingNumberOfShells() > 0 ) )
end

function SkynetIADSAbstractRadarElement:getHARMDetectionChance()
	return self.harmDetectionChance
end

function SkynetIADSAbstractRadarElement:setHARMDetectionChance(chance)
	if chance and chance >= 0 and chance <= 100 then
		self.harmDetectionChance = chance
	end
	return self
end

function SkynetIADSAbstractRadarElement:setupElements()
	local numUnits = #self:getUnitsToAnalyse()
	for typeName, dataType in pairs(SkynetIADS.database) do
		local hasSearchRadar = false
		local hasTrackingRadar = false
		local hasLauncher = false
		self.searchRadars = {}
		self.trackingRadars = {}
		self.launchers = {}
		for entry, unitData in pairs(dataType) do
			if entry == 'searchRadar' then
				self:analyseAndAddUnit(SkynetIADSSAMSearchRadar, self.searchRadars, unitData)
				hasSearchRadar = true
			end
			if entry == 'launchers' then
				self:analyseAndAddUnit(SkynetIADSSAMLauncher, self.launchers, unitData)
				hasLauncher = true
			end
			if entry == 'trackingRadar' then
				self:analyseAndAddUnit(SkynetIADSSAMTrackingRadar, self.trackingRadars, unitData)
				hasTrackingRadar = true
			end
		end
		
		--this check ensures a unit or group has all required elements for the specific sam or ew type:
		if (hasLauncher and hasSearchRadar and hasTrackingRadar and #self.launchers > 0 and #self.searchRadars > 0  and #self.trackingRadars > 0 ) 
			or (hasSearchRadar and hasLauncher and #self.searchRadars > 0 and #self.launchers > 0) then
			self:setHARMDetectionChance(dataType['harm_detection_chance'])
			self.dataBaseSupportedTypesCanEngageHARM = dataType['can_engage_harm'] 
			self:setCanEngageHARM(self.dataBaseSupportedTypesCanEngageHARM)
			local natoName = dataType['name']['NATO']
			self:buildNatoName(natoName)
			break
		end	
	end
end

function SkynetIADSAbstractRadarElement:setCanEngageHARM(canEngage)
	if canEngage == true or canEngage == false then
		self.canEngageHARM = canEngage
		if ( canEngage == true and self:getCanEngageAirWeapons() == false ) then
			self:setCanEngageAirWeapons(true)
		end
	end
	return self
end

function SkynetIADSAbstractRadarElement:getCanEngageHARM()
	return self.canEngageHARM
end

function SkynetIADSAbstractRadarElement:setCanEngageAirWeapons(engageAirWeapons)
	if self:isDestroyed() == false then
		local controller = self:getDCSRepresentation():getController()
		if ( engageAirWeapons == true ) then
			controller:setOption(AI.Option.Ground.id.ENGAGE_AIR_WEAPONS, true)
			--its important that we set var to true here, to prevent recursion in setCanEngageHARM
			self.engageAirWeapons = true
			--we set the original value we got when loading info about the SAM site
			self:setCanEngageHARM(self.dataBaseSupportedTypesCanEngageHARM)
		else
			controller:setOption(AI.Option.Ground.id.ENGAGE_AIR_WEAPONS, false)
			self:setCanEngageHARM(false)
			self.engageAirWeapons = false
		end
	end
	return self
end

function SkynetIADSAbstractRadarElement:getCanEngageAirWeapons()
	return self.engageAirWeapons
end

function SkynetIADSAbstractRadarElement:buildNatoName(natoName)
	--we shorten the SA-XX names and don't return their code names eg goa, gainful..
	local pos = natoName:find(" ")
	local prefix = natoName:sub(1, 2)
	if string.lower(prefix) == 'sa' and pos ~= nil then
		self.natoName = natoName:sub(1, (pos-1))
	else
		self.natoName = natoName
	end
end

function SkynetIADSAbstractRadarElement:analyseAndAddUnit(class, tableToAdd, unitData)
	local units = self:getUnitsToAnalyse()
	for i = 1, #units do
		local unit = units[i]
		self:buildSingleUnit(unit, class, tableToAdd, unitData)
	end
end

function SkynetIADSAbstractRadarElement:buildSingleUnit(unit, class, tableToAdd, unitData)
	local unitTypeName = unit:getTypeName()
	for unitName, unitPerformanceData in pairs(unitData) do
		if unitName == unitTypeName then
			samElement = class:create(unit)
			samElement:setupRangeData()
			table.insert(tableToAdd, samElement)
		end
	end
end

function SkynetIADSAbstractRadarElement:getController()
	local dcsRepresentation = self:getDCSRepresentation()
	if dcsRepresentation:isExist() then
		return dcsRepresentation:getController()
	else
		return nil
	end
end

function SkynetIADSAbstractRadarElement:getLaunchers()
	return self.launchers
end

function SkynetIADSAbstractRadarElement:getSearchRadars()
	return self.searchRadars
end

function SkynetIADSAbstractRadarElement:getTrackingRadars()
	return self.trackingRadars
end

function SkynetIADSAbstractRadarElement:getRadars()
	local radarUnits = {}	
	for i = 1, #self.searchRadars do
		table.insert(radarUnits, self.searchRadars[i])
	end	
	for i = 1, #self.trackingRadars do
		table.insert(radarUnits, self.trackingRadars[i])
	end
	return radarUnits
end

function SkynetIADSAbstractRadarElement:setGoLiveRangeInPercent(percent)
	if percent ~= nil then
		self.firingRangePercent = percent	
		for i = 1, #self.launchers do
			local launcher = self.launchers[i]
			launcher:setFiringRangePercent(self.firingRangePercent)
		end
		for i = 1, #self.searchRadars do
			local radar = self.searchRadars[i]
			radar:setFiringRangePercent(self.firingRangePercent)
		end
	end
	return self
end

function SkynetIADSAbstractRadarElement:getGoLiveRangeInPercent()
	return self.firingRangePercent
end

function SkynetIADSAbstractRadarElement:setEngagementZone(engagementZone)
	if engagementZone == SkynetIADSAbstractRadarElement.GO_LIVE_WHEN_IN_KILL_ZONE then
		self.goLiveRange = engagementZone
	elseif engagementZone == SkynetIADSAbstractRadarElement.GO_LIVE_WHEN_IN_SEARCH_RANGE then
		self.goLiveRange = engagementZone
	end
	return self
end

function SkynetIADSAbstractRadarElement:getEngagementZone()
	return self.goLiveRange
end

function SkynetIADSAbstractRadarElement:goLive()
	if ( self.aiState == false and self:hasWorkingPowerSource() and self.harmSilenceID == nil) 
	and (self:hasRemainingAmmo() == true  )
	then
		if self:isDestroyed() == false then
			local  cont = self:getController()
			cont:setOption(AI.Option.Ground.id.ALARM_STATE, AI.Option.Ground.val.ALARM_STATE.RED)	
			cont:setOption(AI.Option.Air.id.ROE, AI.Option.Air.val.ROE.WEAPON_FREE)
			self:getDCSRepresentation():enableEmission(true)
			self.goLiveTime = timer.getTime()
			self.aiState = true
		end
		self:pointDefencesStopActingAsEW()
		if  self.iads:getDebugSettings().radarWentLive then
			self.iads:printOutputToLog("GOING LIVE: "..self:getDescription())
		end
		self:scanForHarms()
	end
end

function SkynetIADSAbstractRadarElement:pointDefencesStopActingAsEW()
	for i = 1, #self.pointDefences do
		local pointDefence = self.pointDefences[i]
		pointDefence:setActAsEW(false)
	end
end


function SkynetIADSAbstractRadarElement:goDark()
	if (self:hasWorkingPowerSource() == false) or ( self.aiState == true ) 
	and (self.harmSilenceID ~= nil or ( self.harmSilenceID == nil and #self:getDetectedTargets() == 0 and self:hasMissilesInFlight() == false) or ( self.harmSilenceID == nil and #self:getDetectedTargets() > 0 and self:hasMissilesInFlight() == false and self:hasRemainingAmmo() == false ) )	
	then
		if self:isDestroyed() == false then
			self:getDCSRepresentation():enableEmission(false)
		end
		-- point defence will only go live if the Radar Emitting site it is protecting goes dark and this is due to a it defending against a HARM
		if (self.harmSilenceID ~= nil) then
			self:pointDefencesGoLive()
		end
		self.aiState = false
		self:stopScanningForHARMs()
		if self.iads:getDebugSettings().radarWentDark then
			self.iads:printOutputToLog("GOING DARK: "..self:getDescription())
		end
	end
end

function SkynetIADSAbstractRadarElement:pointDefencesGoLive()
	local setActive = false
	for i = 1, #self.pointDefences do
		local pointDefence = self.pointDefences[i]
		if ( pointDefence:getActAsEW() == false ) then
			setActive = true
			pointDefence:setActAsEW(true)
		end
	end
	return setActive
end

function SkynetIADSAbstractRadarElement:isActive()
	return self.aiState
end

function SkynetIADSAbstractRadarElement:isTargetInRange(target)

	local isSearchRadarInRange = false
	local isTrackingRadarInRange = false
	local isLauncherInRange = false
	
	local isSearchRadarInRange = ( #self.searchRadars == 0 )
	for i = 1, #self.searchRadars do
		local searchRadar = self.searchRadars[i]
		if searchRadar:isInRange(target) then
			isSearchRadarInRange = true
			break
		end
	end
	
	if self.goLiveRange == SkynetIADSAbstractRadarElement.GO_LIVE_WHEN_IN_KILL_ZONE then
		
		isLauncherInRange = ( #self.launchers == 0 )
		for i = 1, #self.launchers do
			local launcher = self.launchers[i]
			if launcher:isInRange(target) then
				isLauncherInRange = true
				break
			end
		end
		
		isTrackingRadarInRange = ( #self.trackingRadars == 0 )
		for i = 1, #self.trackingRadars do
			local trackingRadar = self.trackingRadars[i]
			if trackingRadar:isInRange(target) then
				isTrackingRadarInRange = true
				break
			end
		end
	else
		isLauncherInRange = true
		isTrackingRadarInRange = true
	end
	return  (isSearchRadarInRange and isTrackingRadarInRange and isLauncherInRange )
end

function SkynetIADSAbstractRadarElement:isInRadarDetectionRangeOf(abstractRadarElement)
	local radars = self:getRadars()
	local abstractRadarElementRadars = abstractRadarElement:getRadars()
	for i = 1, #radars do
		local radar = radars[i]
		for j = 1, #abstractRadarElementRadars do
			local abstractRadarElementRadar = abstractRadarElementRadars[j]
			if  abstractRadarElementRadar:isExist() and radar:isExist() then
				local distance = self:getDistanceToUnit(radar:getDCSRepresentation():getPosition().p, abstractRadarElementRadar:getDCSRepresentation():getPosition().p)	
				if abstractRadarElementRadar:getMaxRangeFindingTarget() >= distance then
					return true
				end
			end
		end
	end
	return false
end

function SkynetIADSAbstractRadarElement:getDistanceToUnit(unitPosA, unitPosB)
	return mist.utils.round(mist.utils.get2DDist(unitPosA, unitPosB, 0))
end

function SkynetIADSAbstractRadarElement:hasWorkingRadar()
	local radars = self:getRadars()
	for i = 1, #radars do
		local radar = radars[i]
		if radar:isRadarWorking() == true then
			return true
		end
	end
	return false
end

function SkynetIADSAbstractRadarElement:jam(successProbability)
		if self:isDestroyed() == false then
			local controller = self:getController()
			local probability = math.random(1, 100)
			if self.iads:getDebugSettings().jammerProbability then
				self.iads:printOutputToLog("JAMMER: "..self:getDescription()..": Probability: "..successProbability)
			end
			if successProbability > probability then
				controller:setOption(AI.Option.Air.id.ROE, AI.Option.Air.val.ROE.WEAPON_HOLD)
				if self.iads:getDebugSettings().jammerProbability then
					self.iads:printOutputToLog("JAMMER: "..self:getDescription()..": jammed, setting to weapon hold")
				end
			else
				controller:setOption(AI.Option.Air.id.ROE, AI.Option.Air.val.ROE.WEAPON_FREE)
				if self.iads:getDebugSettings().jammerProbability then
					self.iads:printOutputToLog("JAMMER: "..self:getDescription()..": jammed, setting to weapon free")
				end
			end
			self.lastJammerUpdate = timer:getTime()
		end
end

function SkynetIADSAbstractRadarElement:scanForHarms()
	self:stopScanningForHARMs()
	self.harmScanID = mist.scheduleFunction(SkynetIADSAbstractRadarElement.evaluateIfTargetsContainHARMs, {self}, 1, 2)
end

function SkynetIADSAbstractRadarElement:isScanningForHARMs()
	return self.harmScanID ~= nil
end

function SkynetIADSAbstractRadarElement:isDefendingHARM()
	return self.harmSilenceID ~= nil
end

function SkynetIADSAbstractRadarElement:stopScanningForHARMs()
	mist.removeFunction(self.harmScanID)
	self.harmScanID = nil
end

function SkynetIADSAbstractRadarElement:goSilentToEvadeHARM(timeToImpact)
	self:finishHarmDefence(self)
	if ( timeToImpact == nil ) then
		timeToImpact = 0
	end
	
	self.minHarmShutdownTime = self:calculateMinimalShutdownTimeInSeconds(timeToImpact)
	self.maxHarmShutDownTime = self:calculateMaximalShutdownTimeInSeconds(self.minHarmShutdownTime)
	
	self.harmShutdownTime = self:calculateHARMShutdownTime()
	if self.iads:getDebugSettings().harmDefence then
		self.iads:printOutputToLog("HARM DEFENCE SHUTTING DOWN: "..self:getDCSName().." | FOR: "..self.harmShutdownTime.." seconds | TTI: "..timeToImpact)
	end
	self.harmSilenceID = mist.scheduleFunction(SkynetIADSAbstractRadarElement.finishHarmDefence, {self}, timer.getTime() + self.harmShutdownTime, 1)
	self:goDark()
end

function SkynetIADSAbstractRadarElement:getHARMShutdownTime()
	return self.harmShutdownTime
end

function SkynetIADSAbstractRadarElement:calculateHARMShutdownTime()
	local shutDownTime = math.random(self.minHarmShutdownTime, self.maxHarmShutDownTime)
	return shutDownTime
end

function SkynetIADSAbstractRadarElement.finishHarmDefence(self)
	mist.removeFunction(self.harmSilenceID)
	self.harmSilenceID = nil
	self.harmShutdownTime = 0
	
	if ( self:getAutonomousState() == true ) then
		self:goAutonomous()
	end	
end

function SkynetIADSAbstractRadarElement:getDetectedTargets()
	if ( timer.getTime() - self.cachedTargetsCurrentAge > self.cachedTargetsMaxAge ) or ( timer.getTime() - self.goLiveTime < self.noCacheActiveForSecondsAfterGoLive ) then
		self.cachedTargets = {}
		self.cachedTargetsCurrentAge = timer.getTime()
		if self:hasWorkingPowerSource() and self:isDestroyed() == false then
			local targets = self:getController():getDetectedTargets(Controller.Detection.RADAR)
			for i = 1, #targets do
				local target = targets[i]
				-- there are cases when a destroyed object is still visible as a target to the radar, don't add it, will cause errors everywhere the dcs object is accessed
				if target.object then
					local iadsTarget = SkynetIADSContact:create(target, self)
					iadsTarget:refresh()
					if self:isTargetInRange(iadsTarget) then
						table.insert(self.cachedTargets, iadsTarget)
					end
				end
			end
		end
	end
	return self.cachedTargets
end

function SkynetIADSAbstractRadarElement:getSecondsToImpact(distanceNM, speedKT)
	local tti = 0
	if speedKT > 0 then
		tti = mist.utils.round((distanceNM / speedKT) * 3600, 0)
		if tti < 0 then
			tti = 0
		end
	end
	return tti
end

function SkynetIADSAbstractRadarElement:getDistanceInMetersToContact(radarUnit, point)
	return mist.utils.round(mist.utils.get3DDist(radarUnit:getPosition().p, point), 0)
end

function SkynetIADSAbstractRadarElement:calculateMinimalShutdownTimeInSeconds(timeToImpact)
	return timeToImpact + self.minHarmPresetShutdownTime
end

function SkynetIADSAbstractRadarElement:calculateMaximalShutdownTimeInSeconds(minShutdownTime)	
	return minShutdownTime + mist.random(1, self.maxHarmPresetShutdownTime)
end

function SkynetIADSAbstractRadarElement:calculateImpactPoint(target, distanceInMeters)
	-- distance needs to be incremented by a certain value for ip calculation to work, check why presumably due to rounding errors in the previous distance calculation
	return land.getIP(target:getPosition().p, target:getPosition().x, distanceInMeters + 50)
end

function SkynetIADSAbstractRadarElement:shallReactToHARM()
	return self.harmDetectionChance >=  math.random(1, 100)
end

-- will only check for missiles, if DCS ads AAA than can engage HARMs then this code must be updated:
function SkynetIADSAbstractRadarElement:shallIgnoreHARMShutdown()
	local numOfHarms = self:getNumberOfObjectsItentifiedAsHARMS()
	--[[
	self.iads:printOutputToLog("Self enough launchers: "..tostring(self:hasEnoughLaunchersToEngageMissiles(numOfHarms)))
	self.iads:printOutputToLog("Self enough missiles: "..tostring(self:hasRemainingAmmoToEngageMissiles(numOfHarms)))
	self.iads:printOutputToLog("PD enough missiles: "..tostring(self:pointDefencesHaveRemainingAmmo(numOfHarms)))
	self.iads:printOutputToLog("PD enough launchers: "..tostring(self:pointDefencesHaveEnoughLaunchers(numOfHarms)))
	--]]
	return ( ((self:hasEnoughLaunchersToEngageMissiles(numOfHarms) and self:hasRemainingAmmoToEngageMissiles(numOfHarms) and self:getCanEngageHARM()) or (self:pointDefencesHaveRemainingAmmo(numOfHarms) and self:pointDefencesHaveEnoughLaunchers(numOfHarms))))
end

function SkynetIADSAbstractRadarElement:informOfHARM(harmContact)
	local radars = self:getRadars()
		for j = 1, #radars do
			local radar = radars[j]
			local distanceNM =  mist.utils.metersToNM(self:getDistanceInMetersToContact(radar, harmContact:getPosition().p))
			local harmToSAMHeading = mist.utils.toDegree(mist.utils.getHeadingPoints(harmContact:getPosition().p, radar:getPosition().p))
			local harmToSAMAspect = self:calculateAspectInDegrees(harmContact:getMagneticHeading(), harmToSAMHeading)
			local speedKT = harmContact:getGroundSpeedInKnots(0)
			local secondsToImpact = self:getSecondsToImpact(distanceNM, speedKT)
			--TODO: use tti instead of distanceNM?
			-- when iterating through the radars, store shortest tti and work with that value??
			if ( harmToSAMAspect < SkynetIADSAbstractRadarElement.HARM_TO_SAM_ASPECT and distanceNM < SkynetIADSAbstractRadarElement.HARM_LOOKAHEAD_NM ) then
				self:addObjectIdentifiedAsHARM(harmContact)
				if ( #self:getPointDefences() > 0 and self:pointDefencesGoLive() == true and self.iads:getDebugSettings().harmDefence ) then
						self.iads:printOutputToLog("POINT DEFENCES GOING LIVE FOR: "..self:getDCSName().." | TTI: "..secondsToImpact)
				end
				--self.iads:printOutputToLog("Ignore HARM shutdown: "..tostring(self:shallIgnoreHARMShutdown()))
				if ( self:getIsAPointDefence() == false and ( self:isDefendingHARM() == false or ( self:getHARMShutdownTime() < secondsToImpact ) ) and self:shallIgnoreHARMShutdown() == false) then
					self:goSilentToEvadeHARM(secondsToImpact)
					break
				end
			end
		end
end

function SkynetIADSAbstractElement:addObjectIdentifiedAsHARM(harmContact)
	self:insertToTableIfNotAlreadyAdded(self.objectsIdentifiedAsHarms, harmContact)
end

function SkynetIADSAbstractRadarElement:calculateAspectInDegrees(harmHeading, harmToSAMHeading)
		local aspect = harmHeading - harmToSAMHeading
		if ( aspect < 0 ) then
			aspect = -1 * aspect
		end
		if aspect > 180 then
			aspect = 360 - aspect
		end
		return mist.utils.round(aspect)
end

function SkynetIADSAbstractRadarElement:getNumberOfObjectsItentifiedAsHARMS()
	return #self.objectsIdentifiedAsHarms
end

function SkynetIADSAbstractRadarElement:cleanUpOldObjectsIdentifiedAsHARMS()
	local newHARMS = {}
	for i = 1, #self.objectsIdentifiedAsHarms do
		local harmContact = self.objectsIdentifiedAsHarms[i]
		if harmContact:getAge() < self.objectsIdentifiedAsHarmsMaxTargetAge then
			table.insert(newHARMS, harmContact)
		end
	end
	--stop point defences acting as ew (always on), will occur if activated via evaluateIfTargetsContainHARMs()
	--if in this iteration all harms where cleared we turn of the point defence. But in any other cases we dont turn of point defences, that interferes with other parts of the iads
	-- when setting up the iads (letting pds go to read state)
	if (#newHARMS == 0 and self:getNumberOfObjectsItentifiedAsHARMS() > 0 ) then
		self:pointDefencesStopActingAsEW()
	end
	self.objectsIdentifiedAsHarms = newHARMS
end


function SkynetIADSAbstractRadarElement.evaluateIfTargetsContainHARMs(self)

	--if an emitter dies the SAM site being jammed will revert back to normal operation:
	if self.lastJammerUpdate > 0 and ( timer:getTime() - self.lastJammerUpdate ) > 10 then
		self:jam(0)
		self.lastJammerUpdate = 0
	end
	
	--we use the regular interval of this method to update to other states: 
	self:updateMissilesInFlight()	
	self:cleanUpOldObjectsIdentifiedAsHARMS()
end

end
do
--this class is currently used for AWACS and Ships, at a latter date a separate class for ships could be created, currently not needed
SkynetIADSAWACSRadar = {}
SkynetIADSAWACSRadar = inheritsFrom(SkynetIADSAbstractRadarElement)

function SkynetIADSAWACSRadar:create(radarUnit, iads)
	local instance = self:superClass():create(radarUnit, iads)
	setmetatable(instance, self)
	self.__index = self
	instance.lastUpdatePosition = nil
	instance.natoName = radarUnit:getTypeName()
	return instance
end

function SkynetIADSAWACSRadar:setupElements()
	local unit = self:getDCSRepresentation()
	local radar = SkynetIADSSAMSearchRadar:create(unit)
	radar:setupRangeData()
	table.insert(self.searchRadars, radar)
end


-- AWACs will not scan for HARMS
function SkynetIADSAWACSRadar:scanForHarms()
	
end

function SkynetIADSAWACSRadar:getMaxAllowedMovementForAutonomousUpdateInNM()
	--local radarRange = mist.utils.metersToNM(self.searchRadars[1]:getMaxRangeFindingTarget())
	--return mist.utils.round(radarRange / 10)
	--fixed to 10 nm miles to better fit small SAM sites
	return 10
end

function SkynetIADSAWACSRadar:isUpdateOfAutonomousStateOfSAMSitesRequired()
	local isUpdateRequired = self:getDistanceTraveledSinceLastUpdate() > self:getMaxAllowedMovementForAutonomousUpdateInNM()
	if isUpdateRequired then
		self.lastUpdatePosition = nil
	end
	return isUpdateRequired
end

function SkynetIADSAWACSRadar:getDistanceTraveledSinceLastUpdate()
	local currentPosition = nil
	if self.lastUpdatePosition == nil and self:getDCSRepresentation():isExist() then
		self.lastUpdatePosition = self:getDCSRepresentation():getPosition().p
	end
	if self:getDCSRepresentation():isExist() then
		currentPosition = self:getDCSRepresentation():getPosition().p
	end
	return mist.utils.round(mist.utils.metersToNM(self:getDistanceToUnit(self.lastUpdatePosition, currentPosition)))
end

end

do
SkynetIADSCommandCenter = {}
SkynetIADSCommandCenter = inheritsFrom(SkynetIADSAbstractRadarElement)

function SkynetIADSCommandCenter:create(commandCenter, iads)
	local instance = self:superClass():create(commandCenter, iads)
	setmetatable(instance, self)
	self.__index = self
	instance.natoName = "COMMAND CENTER"
	return instance
end

function SkynetIADSCommandCenter:goDark()

end

function SkynetIADSCommandCenter:goLive()

end

end
do

SkynetIADSContact = {}
SkynetIADSContact = inheritsFrom(SkynetIADSAbstractDCSObjectWrapper)

SkynetIADSContact.CLIMB = "CLIMB"
SkynetIADSContact.DESCEND = "DESCEND"

SkynetIADSContact.HARM = "HARM"
SkynetIADSContact.NOT_HARM = "NOT_HARM"
SkynetIADSContact.HARM_UNKNOWN = "HARM_UNKNOWN"

function SkynetIADSContact:create(dcsRadarTarget, abstractRadarElementDetected)
	local instance = self:superClass():create(dcsRadarTarget.object)
	setmetatable(instance, self)
	self.__index = self
	instance.abstractRadarElementsDetected = {}
	table.insert(instance.abstractRadarElementsDetected, abstractRadarElementDetected)
	instance.firstContactTime = timer.getAbsTime()
	instance.lastTimeSeen = 0
	instance.dcsRadarTarget = dcsRadarTarget
	instance.position = instance:getDCSRepresentation():getPosition()
	instance.numOfTimesRefreshed = 0
	instance.speed = 0
	instance.harmState = SkynetIADSContact.HARM_UNKNOWN
	instance.simpleAltitudeProfile = {}
	return instance
end

function SkynetIADSContact:setHARMState(state)
	self.harmState = state
end

function SkynetIADSContact:getHARMState()
	return self.harmState
end

function SkynetIADSContact:isIdentifiedAsHARM()
	return self.harmState == SkynetIADSContact.HARM
end

function SkynetIADSContact:isHARMStateUnknown()
	return self.harmState == SkynetIADSContact.HARM_UNKNOWN
end

function SkynetIADSContact:getMagneticHeading()
	if ( self:isExist() ) then
		return mist.utils.round(mist.utils.toDegree(mist.getHeading(self:getDCSRepresentation())))
	else
		return -1
	end
end

function SkynetIADSContact:getAbstractRadarElementsDetected()
	return self.abstractRadarElementsDetected
end

function SkynetIADSContact:addAbstractRadarElementDetected(radar)
	self:insertToTableIfNotAlreadyAdded(self.abstractRadarElementsDetected, radar)
end

function SkynetIADSContact:isTypeKnown()
	return self.dcsRadarTarget.type
end

function SkynetIADSContact:isDistanceKnown()
	return self.dcsRadarTarget.distance
end

function SkynetIADSContact:getTypeName()
	if self:isIdentifiedAsHARM() then
		return SkynetIADSContact.HARM
	end
	local category = self:getDCSRepresentation():getCategory()
	if category == Object.Category.UNIT then
		return self.typeName
	end
	return "UNKNOWN"
end

function SkynetIADSContact:getPosition()
	return self.position
end

function SkynetIADSContact:getGroundSpeedInKnots(decimals)
	if decimals == nil then
		decimals = 2
	end
	return mist.utils.round(self.speed, decimals)
end

function SkynetIADSContact:getHeightInFeetMSL()
	if self:isExist() then
		return mist.utils.round(mist.utils.metersToFeet(self:getDCSRepresentation():getPosition().p.y), 0)
	else
		return 0
	end
end

function SkynetIADSContact:getDesc()
	if self:isExist() then
		return self:getDCSRepresentation():getDesc()
	else
		return {}
	end
end

function SkynetIADSContact:getNumberOfTimesHitByRadar()
	return self.numOfTimesRefreshed
end

function SkynetIADSContact:refresh()
	if self:isExist() then
		local timeDelta = (timer.getAbsTime() - self.lastTimeSeen)
		if timeDelta > 0 then
			self.numOfTimesRefreshed = self.numOfTimesRefreshed + 1
			local distance = mist.utils.metersToNM(mist.utils.get2DDist(self.position.p, self:getDCSRepresentation():getPosition().p))
			local hours = timeDelta / 3600
			self.speed = (distance / hours)
			self:updateSimpleAltitudeProfile()
			self.position = self:getDCSRepresentation():getPosition()
		end 
	end
	self.lastTimeSeen = timer.getAbsTime()
end

function SkynetIADSContact:updateSimpleAltitudeProfile()
	local currentAltitude = self:getDCSRepresentation():getPosition().p.y
	
	local previousPath = ""
	if #self.simpleAltitudeProfile > 0 then
		previousPath = self.simpleAltitudeProfile[#self.simpleAltitudeProfile]
	end
	
	if self.position.p.y > currentAltitude and previousPath ~= SkynetIADSContact.DESCEND then
		table.insert(self.simpleAltitudeProfile, SkynetIADSContact.DESCEND)
	elseif self.position.p.y < currentAltitude and previousPath ~= SkynetIADSContact.CLIMB then
		table.insert(self.simpleAltitudeProfile, SkynetIADSContact.CLIMB)
	end
end

function SkynetIADSContact:getSimpleAltitudeProfile()
	return self.simpleAltitudeProfile
end

function SkynetIADSContact:getAge()
	return mist.utils.round(timer.getAbsTime() - self.lastTimeSeen)
end

end

do

SkynetIADSEWRadar = {}
SkynetIADSEWRadar = inheritsFrom(SkynetIADSAbstractRadarElement)

function SkynetIADSEWRadar:create(radarUnit, iads)
	local instance = self:superClass():create(radarUnit, iads)
	setmetatable(instance, self)
	self.__index = self
	instance.autonomousBehaviour = SkynetIADSAbstractRadarElement.AUTONOMOUS_STATE_DARK
	return instance
end

function SkynetIADSEWRadar:setupElements()
	local unit = self:getDCSRepresentation()
	local unitType = unit:getTypeName()
	for typeName, dataType in pairs(SkynetIADS.database) do
		for entry, unitData in pairs(dataType) do
			if entry == 'searchRadar' then
				--buildSingleUnit checks to make sure the EW radar is defined in the Skynet database. If it is not, self.searchRadars will be 0 so no ew radar will be added
				self:buildSingleUnit(unit, SkynetIADSSAMSearchRadar, self.searchRadars, unitData)
				if #self.searchRadars > 0 then
					local harmDetection = dataType['harm_detection_chance']
					self:setHARMDetectionChance(harmDetection)
					if unitData[unitType]['name'] then
						local natoName = unitData[unitType]['name']['NATO']
						self:buildNatoName(natoName)
					end
					return
				end
			end
		end
	end
end

--an Early Warning Radar has simplified check to determine if its autonomous or not
function SkynetIADSEWRadar:setToCorrectAutonomousState()
	if self:hasActiveConnectionNode() and self:hasWorkingPowerSource() and self.iads:isCommandCenterUsable() then
		self:resetAutonomousState()
		self:goLive()
	end
	if self:hasActiveConnectionNode() == false or self.iads:isCommandCenterUsable() == false then
		self:goAutonomous()
	end
end

end
do

SkynetIADSJammer = {}
SkynetIADSJammer.__index = SkynetIADSJammer

function SkynetIADSJammer:create(emitter, iads)
	local jammer = {}
	setmetatable(jammer, SkynetIADSJammer)
	jammer.radioMenu = nil
	jammer.emitter = emitter
	jammer.jammerTaskID = nil
	jammer.iads = {iads}
	jammer.maximumEffectiveDistanceNM = 200
	--jammer probability settings are stored here, visualisation, see: https://docs.google.com/spreadsheets/d/16rnaU49ZpOczPEsdGJ6nfD0SLPxYLEYKmmo4i2Vfoe0/edit#gid=0
	jammer.jammerTable = {
		['SA-2'] = {
			['function'] = function(distanceNauticalMiles) return ( 1.4 ^ distanceNauticalMiles ) + 90 end,
			['canjam'] = true,
		},
		['SA-3'] = {
			['function'] = function(distanceNauticalMiles) return ( 1.4 ^ distanceNauticalMiles ) + 80 end,
			['canjam'] = true,
		},
		['SA-6'] = {
			['function'] = function(distanceNauticalMiles) return ( 1.4 ^ distanceNauticalMiles ) + 23 end,
			['canjam'] = true,
		},
		['SA-8'] = {
			['function'] = function(distanceNauticalMiles) return ( 1.35 ^ distanceNauticalMiles ) + 30 end,
			['canjam'] = true,
		},
		['SA-10'] = {
			['function'] = function(distanceNauticalMiles) return ( 1.07 ^ (distanceNauticalMiles / 1.13) ) + 5 end,
			['canjam'] = true,
		},
		['SA-11'] = {
			['function'] = function(distanceNauticalMiles) return ( 1.25 ^ distanceNauticalMiles ) + 15 end,
			['canjam'] = true,
		},
		['SA-15'] = {
			['function'] = function(distanceNauticalMiles) return ( 1.15 ^ distanceNauticalMiles ) + 5 end,
			['canjam'] = true,
		},
	}
	return jammer
end

function SkynetIADSJammer:masterArmOn()
	self:masterArmSafe()
	self.jammerTaskID = mist.scheduleFunction(SkynetIADSJammer.runCycle, {self}, 1, 10)
end

function SkynetIADSJammer:addFunction(natoName, jammerFunction)
	self.jammerTable[natoName] = {
		['function'] = jammerFunction,
		['canjam'] = true
	}
end

function SkynetIADSJammer:setMaximumEffectiveDistance(distance)
	self.maximumEffectiveDistanceNM = distance
end

function SkynetIADSJammer:disableFor(natoName)
	self.jammerTable[natoName]['canjam'] = false
end

function SkynetIADSJammer:isKnownRadarEmitter(natoName)
	local isActive = false
	for unitName, unit in pairs(self.jammerTable) do
		if unitName == natoName and unit['canjam'] == true then
			isActive = true
		end
	end
	return isActive
end

function SkynetIADSJammer:addIADS(iads)
	table.insert(self.iads, iads)
end

function SkynetIADSJammer:getSuccessProbability(distanceNauticalMiles, natoName)
	local probability = 0
	local jammerSettings = self.jammerTable[natoName]
	if jammerSettings ~= nil then
		probability = jammerSettings['function'](distanceNauticalMiles)
	end
	return probability
end

function SkynetIADSJammer:getDistanceNMToRadarUnit(radarUnit)
	return mist.utils.metersToNM(mist.utils.get3DDist(self.emitter:getPosition().p, radarUnit:getPosition().p))
end

function SkynetIADSJammer.runCycle(self)

	if self.emitter:isExist() == false then
		self:masterArmSafe()
		return
	end

	for i = 1, #self.iads do
		local iads = self.iads[i]
		local samSites = iads:getActiveSAMSites()	
		for j = 1, #samSites do
			local samSite = samSites[j]
			local radars = samSite:getRadars()
			local hasLOS = false
			local distance = 0
			local natoName = samSite:getNatoName()
			for l = 1, #radars do
				local radar = radars[l]
				distance = self:getDistanceNMToRadarUnit(radar)
				-- I try to emulate the system as it would work in real life, so a jammer can only jam a SAM site if has line of sight to at least one radar in the group
				if self:isKnownRadarEmitter(natoName) and self:hasLineOfSightToRadar(radar) and distance <= self.maximumEffectiveDistanceNM then
					if iads:getDebugSettings().jammerProbability then
						iads:printOutput("JAMMER: Distance: "..distance)
					end
					samSite:jam(self:getSuccessProbability(distance, natoName))
				end
			end
		end
	end
end

function SkynetIADSJammer:hasLineOfSightToRadar(radar)
	local radarPos = radar:getPosition().p
	--lift the radar 30 meters off the ground, some 3d models are dug in to the ground, creating issues in calculating LOS
	radarPos.y = radarPos.y + 30
	return land.isVisible(radarPos, self.emitter:getPosition().p) 
end

function SkynetIADSJammer:masterArmSafe()
	mist.removeFunction(self.jammerTaskID)
end

--TODO: Remove Menu when emitter dies:
function SkynetIADSJammer:addRadioMenu()
	self.radioMenu = missionCommands.addSubMenu('Jammer: '..self.emitter:getName())
	missionCommands.addCommand('Master Arm On', self.radioMenu, SkynetIADSJammer.updateMasterArm, {self = self, option = 'masterArmOn'})
	missionCommands.addCommand('Master Arm Safe', self.radioMenu, SkynetIADSJammer.updateMasterArm, {self = self, option = 'masterArmSafe'})
end

function SkynetIADSJammer.updateMasterArm(params)
	local option = params.option
	local self = params.self
	if option == 'masterArmOn' then
		self:masterArmOn()
	elseif option == 'masterArmSafe' then
		self:masterArmSafe()
	end
end

function SkynetIADSJammer:removeRadioMenu()
	missionCommands.removeItem(self.radioMenu)
end

end
do

SkynetIADSSAMSearchRadar = {}
SkynetIADSSAMSearchRadar = inheritsFrom(SkynetIADSAbstractDCSObjectWrapper)

function SkynetIADSSAMSearchRadar:create(unit)
	local instance = self:superClass():create(unit)
	setmetatable(instance, self)
	self.__index = self
	instance.firingRangePercent = 100
	instance.maximumRange = 0
	instance.initialNumberOfMissiles = 0
	instance.remainingNumberOfMissiles = 0
	instance.initialNumberOfShells = 0
	instance.remainingNumberOfShells = 0
	instance.triedSensors = 0
	return instance
end

--override in subclasses to match different datastructure of getSensors()
function SkynetIADSSAMSearchRadar:setupRangeData()
	if self:isExist() then
		local data = self:getDCSRepresentation():getSensors()
		if data == nil then
			--this is to prevent infinite calls between launcher and search radar
			self.triedSensors = self.triedSensors + 1
			--the SA-13 does not have any sensor data, but is has launcher data, so we use the stuff from the launcher for the radar range.
			SkynetIADSSAMLauncher.setupRangeData(self)
			return
		end
		for i = 1, #data do
			local subEntries = data[i]
			for j = 1, #subEntries do
				local sensorInformation = subEntries[j]
				-- some sam sites have  IR and passive EWR detection, we are just interested in the radar data
				-- investigate if upperHemisphere and headOn is ok, I guess it will work for most detection cases
				if sensorInformation.type == Unit.SensorType.RADAR and sensorInformation['detectionDistanceAir'] then
					local upperHemisphere = sensorInformation['detectionDistanceAir']['upperHemisphere']['headOn']
					local lowerHemisphere = sensorInformation['detectionDistanceAir']['lowerHemisphere']['headOn']
					self.maximumRange = upperHemisphere
					if lowerHemisphere > upperHemisphere then
						self.maximumRange = lowerHemisphere
					end
				end
			end
		end
	end
end

function SkynetIADSSAMSearchRadar:getMaxRangeFindingTarget()
	return self.maximumRange
end

function SkynetIADSSAMSearchRadar:isRadarWorking()
	-- the ammo check is for the SA-13 which does not return any sensor data:
	return (self:isExist() == true and ( self:getDCSRepresentation():getSensors() ~= nil or self:getDCSRepresentation():getAmmo() ~= nil ) )
end

function SkynetIADSSAMSearchRadar:setFiringRangePercent(percent)
	self.firingRangePercent = percent
end

function SkynetIADSSAMSearchRadar:getDistance(target)
	return mist.utils.get2DDist(target:getPosition().p, self:getDCSRepresentation():getPosition().p)
end

function SkynetIADSSAMSearchRadar:getHeight(target)
	local radarElevation = self:getDCSRepresentation():getPosition().p.y
	local targetElevation = target:getPosition().p.y
	return math.abs(targetElevation - radarElevation)
end

function SkynetIADSSAMSearchRadar:isInHorizontalRange(target)
	return (self:getMaxRangeFindingTarget() / 100 * self.firingRangePercent) >= self:getDistance(target)
end

function SkynetIADSSAMSearchRadar:isInRange(target)
	if self:isExist() == false then
		return false
	end
	return self:isInHorizontalRange(target)
end

end

do

SkynetIADSSamSite = {}
SkynetIADSSamSite = inheritsFrom(SkynetIADSAbstractRadarElement)

function SkynetIADSSamSite:create(samGroup, iads)
	local sam = self:superClass():create(samGroup, iads)
	setmetatable(sam, self)
	self.__index = self
	sam.targetsInRange = false
	sam.goLiveConstraints = {}
	return sam
end

function SkynetIADSSamSite:addGoLiveConstraint(constraintName, constraint)
	self.goLiveConstraints[constraintName] = constraint
end

function SkynetIADSAbstractRadarElement:areGoLiveConstraintsSatisfied(contact)
	for constraintName, constraint in pairs(self.goLiveConstraints) do
		if ( constraint(contact) ~= true ) then
			return false
		end
	end
	return true
end

function SkynetIADSSamSite:isDestroyed()
	local isDestroyed = true
	for i = 1, #self.launchers do
		local launcher = self.launchers[i]
		if launcher:isExist() == true then
			isDestroyed = false
		end
	end
	local radars = self:getRadars()
	for i = 1, #radars do
		local radar = radars[i]
		if radar:isExist() == true then
			isDestroyed = false
		end
	end	
	return isDestroyed
end

function SkynetIADSSamSite:targetCycleUpdateStart()
	self.targetsInRange = false
end

function SkynetIADSSamSite:targetCycleUpdateEnd()
	if self.targetsInRange == false and self.actAsEW == false and self:getAutonomousState() == false and self:getAutonomousBehaviour() == SkynetIADSAbstractRadarElement.AUTONOMOUS_STATE_DCS_AI then
		self:goDark()
	end
end

function SkynetIADSSamSite:informOfContact(contact)
	-- we make sure isTargetInRange (expensive call) is only triggered if no previous calls to this method resulted in targets in range
	if ( self.targetsInRange == false and self:areGoLiveConstraintsSatisfied(contact) == true and self:isTargetInRange(contact) and ( contact:isIdentifiedAsHARM() == false or ( contact:isIdentifiedAsHARM() == true and self:getCanEngageHARM() == true ) ) ) then
		self:goLive()
		self.targetsInRange = true
	end
end

end
do

SkynetIADSSAMTrackingRadar = {}
SkynetIADSSAMTrackingRadar = inheritsFrom(SkynetIADSSAMSearchRadar)

function SkynetIADSSAMTrackingRadar:create(unit)
	local instance = self:superClass():create(unit)
	setmetatable(instance, self)
	self.__index = self
	return instance
end

end
do

SkynetIADSSAMLauncher = {}
SkynetIADSSAMLauncher = inheritsFrom(SkynetIADSSAMSearchRadar)

function SkynetIADSSAMLauncher:create(unit)
	local instance = self:superClass():create(unit)
	setmetatable(instance, self)
	self.__index = self
	instance.maximumFiringAltitude = 0
	return instance
end

function SkynetIADSSAMLauncher:setupRangeData()
	self.remainingNumberOfMissiles = 0
	self.remainingNumberOfShells = 0
	if self:isExist() then
		local data = self:getDCSRepresentation():getAmmo()
		local initialNumberOfMissiles = 0
		local initialNumberOfShells = 0
		--data becomes nil, when all missiles are fired
		if data then
			for i = 1, #data do
				local ammo = data[i]		
				--we ignore checks on radar guidance types, since we are not interested in how exactly the missile is guided by the SAM site.
				if ammo.desc.category == Weapon.Category.MISSILE then
					--TODO: see what the difference is between Max and Min values, SA-3 has higher Min value than Max?, most likely it has to do with the box parameters supplied by launcher
					--to simplyfy we just use the larger value, sam sites need a few seconds of tracking time to fire, by that time contact has most likely closed in on the SAM site.
					local altMin = ammo.desc.rangeMaxAltMin
					local altMax = ammo.desc.rangeMaxAltMax
					self.maximumRange = altMin
					if altMin < altMax then
						self.maximumRange = altMax
					end
					self.maximumFiringAltitude = ammo.desc.altMax
					self.remainingNumberOfMissiles = self.remainingNumberOfMissiles + ammo.count
					initialNumberOfMissiles = self.remainingNumberOfMissiles
				end
				if ammo.desc.category == Weapon.Category.SHELL then
					self.remainingNumberOfShells = self.remainingNumberOfShells + ammo.count
					initialNumberOfShells = self.remainingNumberOfShells
				end
				--if no distance was detected we run the code for the search radar. This happens when all in one units are passed like the shilka
				if self.maximumRange == 0 then
					--this is to prevent infinite calls between launcher and search radar
					if self.triedSensors <= 2 then
						SkynetIADSSAMSearchRadar.setupRangeData(self)
					end
				end
			end
			-- conditions here are because setupRangeData() is called multiple times in the code to update ammo status, we set initial values only the first time the method is called
			if self.initialNumberOfMissiles == 0 then
				self.initialNumberOfMissiles = initialNumberOfMissiles
			end
			if self.initialNumberOfShells == 0 then
				self.initialNumberOfShells = initialNumberOfShells
			end
		end
	end
end

function SkynetIADSSAMLauncher:getInitialNumberOfShells()
	return self.initialNumberOfShells
end

function SkynetIADSSAMLauncher:getRemainingNumberOfShells()
	self:setupRangeData()
	return self.remainingNumberOfShells
end

function SkynetIADSSAMLauncher:getInitialNumberOfMissiles()
	return self.initialNumberOfMissiles
end

function SkynetIADSSAMLauncher:getRemainingNumberOfMissiles()
	self:setupRangeData()
	return self.remainingNumberOfMissiles
end

function SkynetIADSSAMLauncher:getRange()
	return self.maximumRange
end

function SkynetIADSSAMLauncher:getMaximumFiringAltitude()
	return self.maximumFiringAltitude
end

function SkynetIADSSAMLauncher:isWithinFiringHeight(target)
	-- if no max firing height is set (radar quided AAA) then we use the vertical range, bit of a hack but probably ok for AAA
	if self:getMaximumFiringAltitude() > 0 then
		return self:getMaximumFiringAltitude() >= self:getHeight(target) 
	else
		return self:getRange() >= self:getHeight(target)
	end
end

function SkynetIADSSAMLauncher:isInRange(target)
	if self:isExist() == false then
		return false
	end
	return self:isWithinFiringHeight(target) and self:isInHorizontalRange(target)
end

end

--[[
SA-2 Launcher:
    {
        count=1,
        desc={
            Nmax=17,
            RCS=0.39669999480247,
            _origin="",
            altMax=25000,
            altMin=100,
            box={
                max={x=4.7303376197815, y=0.84564626216888, z=0.84564626216888},
                min={x=-5.8387970924377, y=-0.84564626216888, z=-0.84564626216888}
            },
            category=1,
            displayName="SA2V755",
            fuseDist=20,
            guidance=4,
            life=2,
            missileCategory=2,
            rangeMaxAltMax=30000,
            rangeMaxAltMin=40000,
            rangeMin=7000,
            typeName="SA2V755",
            warhead={caliber=500, explosiveMass=196, mass=196, type=1}
        }
    }
}
--]]
do

SkynetIADSHARMDetection = {}
SkynetIADSHARMDetection.__index = SkynetIADSHARMDetection

SkynetIADSHARMDetection.HARM_THRESHOLD_SPEED_KTS = 800

function SkynetIADSHARMDetection:create(iads)
	local harmDetection = {}
	setmetatable(harmDetection, self)
	harmDetection.contacts = {}
	harmDetection.iads = iads
	harmDetection.contactRadarsEvaluated = {}
	return harmDetection
end

function SkynetIADSHARMDetection:setContacts(contacts)
	self.contacts = contacts
end

function SkynetIADSHARMDetection:evaluateContacts()
	self:cleanAgedContacts()
	for i = 1, #self.contacts do
		local contact = self.contacts[i]	
		local groundSpeed  = contact:getGroundSpeedInKnots(0)
		--if a contact has only been hit by a radar once it's speed is 0
		if groundSpeed == 0 then
			return
		end
		local simpleAltitudeProfile = contact:getSimpleAltitudeProfile()
		local newRadarsToEvaluate = self:getNewRadarsThatHaveDetectedContact(contact)
		--self.iads:printOutputToLog(contact:getName().." new Radars to evaluate: "..#newRadarsToEvaluate)
		--self.iads:printOutputToLog(contact:getName().." ground speed: "..groundSpeed)
		if ( #newRadarsToEvaluate > 0 and contact:isIdentifiedAsHARM() == false and ( groundSpeed > SkynetIADSHARMDetection.HARM_THRESHOLD_SPEED_KTS and #simpleAltitudeProfile <= 2 ) ) then
			local detectionProbability = self:getDetectionProbability(newRadarsToEvaluate)
			--self.iads:printOutputToLog("DETECTION PROB: "..detectionProbability)
			if ( self:shallReactToHARM(detectionProbability) ) then
				contact:setHARMState(SkynetIADSContact.HARM)
				if (self.iads:getDebugSettings().harmDefence ) then
					self.iads:printOutputToLog("HARM IDENTIFIED: "..contact:getTypeName().." | DETECTION PROBABILITY WAS: "..detectionProbability.."%")
				end
			else
				contact:setHARMState(SkynetIADSContact.NOT_HARM)
				if (self.iads:getDebugSettings().harmDefence ) then
					self.iads:printOutputToLog("HARM NOT IDENTIFIED: "..contact:getTypeName().." | DETECTION PROBABILITY WAS: "..detectionProbability.."%")
				end
			end
		end
		
		if ( #simpleAltitudeProfile > 2 and contact:isIdentifiedAsHARM() ) then
			contact:setHARMState(SkynetIADSContact.HARM_UNKNOWN)
			if (self.iads:getDebugSettings().harmDefence ) then
				self.iads:printOutputToLog("CORRECTING HARM STATE: CONTACT IS NOT A HARM: "..contact:getName())
			end
		end
		
		if ( contact:isIdentifiedAsHARM() ) then
			self:informRadarsOfHARM(contact)
		end
	end
end

function SkynetIADSHARMDetection:cleanAgedContacts()
	local activeContactRadars = {}
	for contact, radars in pairs (self.contactRadarsEvaluated) do
		if contact:getAge() < 32 then
			activeContactRadars[contact] = radars
		end
	end
	self.contactRadarsEvaluated = activeContactRadars
end

function SkynetIADSHARMDetection:getNewRadarsThatHaveDetectedContact(contact)
	local newRadars = contact:getAbstractRadarElementsDetected()
	local radars = self.contactRadarsEvaluated[contact]
	if radars then
		newRadars = {}
		local contactRadars = contact:getAbstractRadarElementsDetected()
		for i = 1, #contactRadars do
			local contactRadar = contactRadars[i]
			local newRadar = self:isElementInTable(radars, contactRadar)
			if newRadar ~= nil then
				table.insert(newRadars, newRadar)
			end
		end
	end
	self.contactRadarsEvaluated[contact] = contact:getAbstractRadarElementsDetected()
	return newRadars
end

function SkynetIADSHARMDetection:isElementInTable(tbl, element)
	for i = 1, #tbl do
		tblElement = tbl[i]
		if tblElement == element then
			return nil
		end
	end
	return element
end

function SkynetIADSHARMDetection:informRadarsOfHARM(contact)
	local samSites = self.iads:getUsableSAMSites()
	self:updateRadarsOfSites(samSites, contact)
	
	local ewRadars = self.iads:getUsableEarlyWarningRadars()
	self:updateRadarsOfSites(ewRadars, contact)
end

function SkynetIADSHARMDetection:updateRadarsOfSites(sites, contact)
	for i = 1, #sites do
		local site = sites[i]
		site:informOfHARM(contact)
	end
end

function SkynetIADSHARMDetection:shallReactToHARM(chance)
	return chance >=  math.random(1, 100)
end

function SkynetIADSHARMDetection:getDetectionProbability(radars)
	local detectionChance = 0
	local missChance = 100
	local detection = 0
	for i = 1, #radars do
		detection = radars[i]:getHARMDetectionChance()
		if ( detectionChance == 0 ) then
			detectionChance = detection
		else
			detectionChance = detectionChance + (detection * (missChance / 100))
		end	
		missChance = 100 - detection
	end
	return detectionChance
end

end


