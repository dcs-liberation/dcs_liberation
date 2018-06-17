local unitPayloads = {
	["name"] = "MiG-21Bis",
	["payloads"] = {
		[1] = {
			["name"] = "Patrol, long range",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{PTB_800_MIG21}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{R-3R}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{R-3R}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{R-3S}",
					["num"] = 1,
				},
				[5] = {
					["CLSID"] = "{R-3S}",
					["num"] = 5,
				},
				[6] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[2] = {
			["name"] = "Patrol, medium range",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{PTB_800_MIG21}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{R-3R}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{R-3R}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{R-60 2L}",
					["num"] = 1,
				},
				[5] = {
					["CLSID"] = "{R-60 2R}",
					["num"] = 5,
				},
				[6] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[3] = {
			["name"] = "Patrol, short range",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{PTB_490C_MIG21}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{R-3R}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{R-3R}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{R-60 2L}",
					["num"] = 1,
				},
				[5] = {
					["CLSID"] = "{R-60 2R}",
					["num"] = 5,
				},
				[6] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[4] = {
			["name"] = "Hard targets, BOMBS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{PTB_800_MIG21}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 1,
				},
				[6] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[5] = {
			["name"] = "Unknown or mixed targets, BOMBS + ROCKETS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{PTB_800_MIG21}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{UB-32_S5M}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{UB-32_S5M}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 1,
				},
				[6] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[6] = {
			["name"] = "Soft targets, CLUSTERS + ROCKETS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{PTB_800_MIG21}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{UB-32_S5M}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{UB-32_S5M}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{4203753F-8198-4E85-9924-6F8FF679F9FF}",
					["num"] = 1,
				},
				[6] = {
					["CLSID"] = "{4203753F-8198-4E85-9924-6F8FF679F9FF}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[7] = {
			["name"] = "Soft targets, CLUSTERS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{PTB_800_MIG21}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{08164777-5E9C-4B08-B48E-5AA7AFB246E2}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{08164777-5E9C-4B08-B48E-5AA7AFB246E2}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{4203753F-8198-4E85-9924-6F8FF679F9FF}",
					["num"] = 1,
				},
				[6] = {
					["CLSID"] = "{4203753F-8198-4E85-9924-6F8FF679F9FF}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[8] = {
			["name"] = "Soft targets, scattered",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
				[2] = {
					--["CLSID"] = "{05544F1A-C39C-466b-BC37-5BD1D52E57BB}",
					["CLSID"] = "{UPK-23-250 MiG-21}",
					["num"] = 2,
				},
				[3] = {
					--["CLSID"] = "{05544F1A-C39C-466b-BC37-5BD1D52E57BB}",
					["CLSID"] = "{UPK-23-250 MiG-21}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{PTB_800_MIG21}",
					["num"] = 3,
				},
				[5] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 1,
				},
				[6] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[9] = {
			["name"] = "Few big targets, GROM + BOMBS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{Kh-66_Grom}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{PTB_800_MIG21}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{Kh-66_Grom}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 5,
				},
				[6] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[10] = {
			["name"] = "Very hard target, PENETRATION",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{PTB_800_MIG21}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{35B698AC-9FEF-4EC4-AD29-484A0085F62B}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{35B698AC-9FEF-4EC4-AD29-484A0085F62B}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
				[5] = {
					["CLSID"] = "{FB3CE165-BF07-4979-887C-92B87F13276B}",
					["num"] = 1,
				},
				[6] = {
					["CLSID"] = "{FB3CE165-BF07-4979-887C-92B87F13276B}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[11] = {
			["name"] = "Aerial attack, hard targets, CLUSTERS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{4203753F-8198-4E85-9924-6F8FF679F9FF}",
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "{4203753F-8198-4E85-9924-6F8FF679F9FF}",
					["num"] = 5,
				},
				[4] = {
					["CLSID"] = "{4203753F-8198-4E85-9924-6F8FF679F9FF}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{4203753F-8198-4E85-9924-6F8FF679F9FF}",
					["num"] = 4,
				},
				[6] = {
					["CLSID"] = "{PTB_800_MIG21}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[12] = {
			["name"] = "Hard targets, ROCKETS, PENETRATION",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{PTB_800_MIG21}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{S-24A}",
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "{S-24A}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{S-24A}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{S-24A}",
					["num"] = 5,
				},
				[6] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[13] = {
			["name"] = "Soft targets, ROCKETS, BLAST-FRAGMENTS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{PTB_800_MIG21}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{S-24B}",
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "{S-24B}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{S-24B}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{S-24B}",
					["num"] = 5,
				},
				[6] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[14] = {
			["name"] = "Long range, MIX",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{PTB_490C_MIG21}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
				[3] = {
					["CLSID"] = "{R-3R}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{R-3S}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{PTB_490_MIG21}",
					["num"] = 1,
				},
				[6] = {
					["CLSID"] = "{PTB_490_MIG21}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 10,
			},
		},
		[15] = {
			["name"] = "Long range, RADAR GUIDED MISSILES",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{PTB_490C_MIG21}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
				[3] = {
					["CLSID"] = "{R-3R}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{R-3R}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{PTB_490_MIG21}",
					["num"] = 5,
				},
				[6] = {
					["CLSID"] = "{PTB_490_MIG21}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 10,
			},
		},
		[16] = {
			["name"] = "Long range, INFRA RED MISSILES",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{PTB_490C_MIG21}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
				[3] = {
					["CLSID"] = "{R-3S}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{R-3S}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{PTB_490_MIG21}",
					["num"] = 1,
				},
				[6] = {
					["CLSID"] = "{PTB_490_MIG21}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 10,
			},
		},
		[17] = {
			["name"] = "Escort",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{PTB_800_MIG21}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
				[3] = {
					["CLSID"] = "{R-3R}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{R-3R}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{R-3S}",
					["num"] = 1,
				},
				[6] = {
					["CLSID"] = "{R-3S}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 18,
			},
		},
		[18] = {
			["name"] = "Escort, JAMMER",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{SPS-141-100}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{R-3R}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{R-3S}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{PTB_490_MIG21}",
					["num"] = 1,
				},
				[5] = {
					["CLSID"] = "{PTB_490_MIG21}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 18,
			},
		},
		[19] = {
			["name"] = "Night, ILLUMINATOR",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{PTB_800_MIG21}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{0511E528-EA28-4caf-A212-00D1408DF10A}",
					["num"] = 1,
				},
				[4] = {
					["CLSID"] = "{0511E528-EA28-4caf-A212-00D1408DF10A}",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{0511E528-EA28-4caf-A212-00D1408DF10A}",
					["num"] = 2,
				},
				[6] = {
					["CLSID"] = "{0511E528-EA28-4caf-A212-00D1408DF10A}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[20] = {
			["name"] = "Long range, JAMMER",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{SPS-141-100}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{R-3R}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{R-3S}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{PTB_490_MIG21}",
					["num"] = 1,
				},
				[5] = {
					["CLSID"] = "{PTB_490_MIG21}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 10,
			},
		},
		[21] = {
			["name"] = "Soft targets, UPK + ROCKETS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{PTB_800_MIG21}",
					["num"] = 3,
				},
				[3] = {
					--["CLSID"] = "{05544F1A-C39C-466b-BC37-5BD1D52E57BB}",
					["CLSID"] = "{UPK-23-250 MiG-21}",
					["num"] = 2,
				},
				[4] = {
					--["CLSID"] = "{05544F1A-C39C-466b-BC37-5BD1D52E57BB}",
					["CLSID"] = "{UPK-23-250 MiG-21}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{UB-16_S5M}",
					["num"] = 1,
				},
				[6] = {
					["CLSID"] = "{UB-16_S5M}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[22] = {
			["name"] = "Soft targets, UPK + CLUSTERS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{4203753F-8198-4E85-9924-6F8FF679F9FF}",
					["num"] = 1,
				},
				[2] = {
					--["CLSID"] = "{05544F1A-C39C-466b-BC37-5BD1D52E57BB}",
					["CLSID"] = "{UPK-23-250 MiG-21}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{PTB_800_MIG21}",
					["num"] = 3,
				},
				[4] = {
					--["CLSID"] = "{05544F1A-C39C-466b-BC37-5BD1D52E57BB}",
					["CLSID"] = "{UPK-23-250 MiG-21}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{4203753F-8198-4E85-9924-6F8FF679F9FF}",
					["num"] = 5,
				},
				[6] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[23] = {
			["name"] = "Patrol, JAMMER",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{R-3R}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{R-3S}",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "{SPS-141-100}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{PTB_490_MIG21}",
					["num"] = 1,
				},
				[5] = {
					["CLSID"] = "{PTB_490_MIG21}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[24] = {
			["name"] = "NUCLEAR A",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{RN-24}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
				[3] = {
					["CLSID"] = "{PTB_490_MIG21}",
					["num"] = 5,
				},
				[4] = {
					["CLSID"] = "{PTB_490_MIG21}",
					["num"] = 1,
				},
				[5] = {
					["CLSID"] = "{R-3S}",
					["num"] = 4,
				},
				[6] = {
					["CLSID"] = "{R-3R}",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[25] = {
			["name"] = "NUCLEAR B",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{RN-28}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
				[3] = {
					["CLSID"] = "{PTB_490_MIG21}",
					["num"] = 5,
				},
				[4] = {
					["CLSID"] = "{PTB_490_MIG21}",
					["num"] = 1,
				},
				[5] = {
					["CLSID"] = "{R-3S}",
					["num"] = 4,
				},
				[6] = {
					["CLSID"] = "{R-3R}",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[26] = {
			["name"] = "Short range",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{PTB_800_MIG21}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{R-3R}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{R-3R}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{R-3S}",
					["num"] = 1,
				},
				[5] = {
					["CLSID"] = "{R-3S}",
					["num"] = 5,
				},
				[6] = {
					["CLSID"] = "{ASO-2}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 10,
			},
		},
		[27] = {
			["name"] = "AEROBATIC",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{SMOKE_WHITE}",
					["num"] = 7,
				},
			},
			["tasks"] = {
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "MiG-21Bis",
}
return unitPayloads
