-- registerTask("Nothing",15);
-- registerTask("SEAD",29);
-- registerTask("AntishipStrike",30);
-- registerTask("AWACS",14);
-- registerTask("CAS",31);
-- registerTask("CAP",11);
-- registerTask("Escort",18);
-- registerTask("FighterSweep",19);
-- registerTask("GAI",20);
-- registerTask("GroundAttack",32);
-- registerTask("Intercept",10);
-- registerTask("AFAC",16);
-- registerTask("RunwayAttack",34);
-- registerTask("Transport",35);
local unitPayloads = {
	["name"] = "J-11A",
	["payloads"] = {
		[1] = {
			["name"] = "FAB-100x36,R-73x2,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
				[2] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[4] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{F99BEC1A-869D-4AC7-9730-FBA0E3B1F5FC}",
					["num"] = 8,
				},
				[6] = {
					["CLSID"] = "{F99BEC1A-869D-4AC7-9730-FBA0E3B1F5FC}",
					["num"] = 3,
				},
				[7] = {
					["CLSID"] = "{F99BEC1A-869D-4AC7-9730-FBA0E3B1F5FC}",
					["num"] = 7,
				},
				[8] = {
					["CLSID"] = "{F99BEC1A-869D-4AC7-9730-FBA0E3B1F5FC}",
					["num"] = 4,
				},
				[9] = {
					["CLSID"] = "{F99BEC1A-869D-4AC7-9730-FBA0E3B1F5FC}",
					["num"] = 5,
				},
				[10] = {
					["CLSID"] = "{F99BEC1A-869D-4AC7-9730-FBA0E3B1F5FC}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[2] = {
			["name"] = "FAB-250x8,R-73x2,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{FAB_250_DUAL_L}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 6,
				},
				[6] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 7,
				},
				[7] = {
					["CLSID"] = "{FAB_250_DUAL_R}",
					["num"] = 8,
				},
				[8] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[9] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
				[10] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[3] = {
			["name"] = "FAB-500x8,R-73x2,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{FAB_500_DUAL_L}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{37DCC01E-9E02-432F-B61D-10C166CA2798}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{37DCC01E-9E02-432F-B61D-10C166CA2798}",
					["num"] = 7,
				},
				[5] = {
					["CLSID"] = "{FAB_500_DUAL_R}",
					["num"] = 8,
				},
				[6] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[7] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
				[8] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
				[9] = {
					["CLSID"] = "{37DCC01E-9E02-432F-B61D-10C166CA2798}",
					["num"] = 5,
				},
				[10] = {
					["CLSID"] = "{37DCC01E-9E02-432F-B61D-10C166CA2798}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[4] = {
			["name"] = "S-8KOMx80,FAB-250x4,R-73x2,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{B8M1_20_S8KOM_DUAL_L}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 6,
				},
				[5] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 7,
				},
				[6] = {
					["CLSID"] = "{B8M1_20_S8KOM_DUAL_R}",
					["num"] = 8,
				},
				[7] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[8] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
				[9] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
				[10] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[5] = {
			["name"] = "S-13x20,FAB-250x4,R-73x2,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
				[2] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[4] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{B13_5_S13OF_DUAL_R}",
					["num"] = 8,
				},
				[6] = {
					["CLSID"] = "{B13_5_S13OF_DUAL_L}",
					["num"] = 3,
				},
				[7] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 7,
				},
				[8] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 6,
				},
				[9] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 5,
				},
				[10] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[6] = {
			["name"] = "S-25x4,FAB-500x4,R-73x2,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
				[2] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[4] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{S25_DUAL_R}",
					["num"] = 8,
				},
				[6] = {
					["CLSID"] = "{S25_DUAL_L}",
					["num"] = 3,
				},
				[7] = {
					["CLSID"] = "{37DCC01E-9E02-432F-B61D-10C166CA2798}",
					["num"] = 7,
				},
				[8] = {
					["CLSID"] = "{37DCC01E-9E02-432F-B61D-10C166CA2798}",
					["num"] = 6,
				},
				[9] = {
					["CLSID"] = "{37DCC01E-9E02-432F-B61D-10C166CA2798}",
					["num"] = 5,
				},
				[10] = {
					["CLSID"] = "{37DCC01E-9E02-432F-B61D-10C166CA2798}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 32,
				[2] = 30
			},
		},
		[7] = {
			["name"] = "R-27ERx4,R-27ETx2,R-73x2,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{B79C379A-9E87-4E50-A1EE-7F7E29C2E87A}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 6,
				},
				[6] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 7,
				},
				[7] = {
					["CLSID"] = "{B79C379A-9E87-4E50-A1EE-7F7E29C2E87A}",
					["num"] = 8,
				},
				[8] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[9] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
				[10] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 18,
				[4] = 19,
			},
		},
		[8] = {
			["name"] = "R-77x6,R-73x2,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[2] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 8,
				},
				[4] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 7,
				},
				[5] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 6,
				},
				[6] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 5,
				},
				[7] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 4,
				},
				[8] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 3,
				},
				[9] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
				[10] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 18,
				[4] = 19,
			},
		},
		[9] = {
			["name"] = "R-27ERx6,R-73x2,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 6,
				},
				[6] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 7,
				},
				[7] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 8,
				},
				[8] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[9] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
				[10] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 18,
				[4] = 19,
			},
		},
		[10] = {
			["name"] = "R-77x4,R-27ETx2,R-73x2,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[2] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{B79C379A-9E87-4E50-A1EE-7F7E29C2E87A}",
					["num"] = 8,
				},
				[4] = {
					["CLSID"] = "{B79C379A-9E87-4E50-A1EE-7F7E29C2E87A}",
					["num"] = 3,
				},
				[5] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 7,
				},
				[6] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 4,
				},
				[7] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
				[8] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
				[9] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 6,
				},
				[10] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 18,
				[4] = 19,
			},
		},
		[11] = {
			["name"] = "R-77x4,R-27ERx2,R-73x2,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[2] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 6,
				},
				[4] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
				[6] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
				[7] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 7,
				},
				[8] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 4,
				},
				[9] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 3,
				},
				[10] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 8,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 18,
				[4] = 19,
			},
		},
		[12] = {
			["name"] = "BetAB-500ShPx6,R-73x2,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{BD289E34-DF84-4C5E-9220-4B14C346E79D}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{BD289E34-DF84-4C5E-9220-4B14C346E79D}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{BD289E34-DF84-4C5E-9220-4B14C346E79D}",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{BD289E34-DF84-4C5E-9220-4B14C346E79D}",
					["num"] = 6,
				},
				[6] = {
					["CLSID"] = "{BD289E34-DF84-4C5E-9220-4B14C346E79D}",
					["num"] = 7,
				},
				[7] = {
					["CLSID"] = "{BD289E34-DF84-4C5E-9220-4B14C346E79D}",
					["num"] = 8,
				},
				[8] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[9] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
				[10] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
			},
			["tasks"] = {
				[1] = 34,
			},
		},
		[13] = {
			["name"] = "R-73x4,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 8,
				},
				[4] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[5] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
				[6] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 18,
				[4] = 19,
			},
		},
		[14] = {
			["name"] = "R-77x2,R-27ETx2,R-73x2,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[2] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 7,
				},
				[4] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{B79C379A-9E87-4E50-A1EE-7F7E29C2E87A}",
					["num"] = 8,
				},
				[6] = {
					["CLSID"] = "{B79C379A-9E87-4E50-A1EE-7F7E29C2E87A}",
					["num"] = 3,
				},
				[7] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
				[8] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 18,
				[4] = 19,
			},
		},
		[15] = {
			["name"] = "R-77x6,R-73x4",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[2] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 7,
				},
				[4] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 8,
				},
				[6] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 3,
				},
				[7] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 1,
				},
				[8] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 10,
				},
				[9] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 6,
				},
				[10] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 18,
				[4] = 19,
			},
		},
		[16] = {
			["name"] = "R-77x2,R-27ETx2,R-27ERx2,R-73x2,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[2] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{B79C379A-9E87-4E50-A1EE-7F7E29C2E87A}",
					["num"] = 8,
				},
				[4] = {
					["CLSID"] = "{B79C379A-9E87-4E50-A1EE-7F7E29C2E87A}",
					["num"] = 3,
				},
				[5] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 7,
				},
				[6] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 4,
				},
				[7] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
				[8] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
				[9] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 6,
				},
				[10] = {
					["CLSID"] = "{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 18,
				[4] = 19,
			},
		},
		[17] = {
			["name"] = "R-27ETx2,R-27ERx4,R-73x2,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[2] = {
					["CLSID"] = "{B79C379A-9E87-4E50-A1EE-7F7E29C2E87A}",
					["num"] = 8,
				},
				[3] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 7,
				},
				[4] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 6,
				},
				[5] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 5,
				},
				[6] = {
					["CLSID"] = "{E8069896-8435-4B90-95C0-01A03AE6E400}",
					["num"] = 4,
				},
				[7] = {
					["CLSID"] = "{B79C379A-9E87-4E50-A1EE-7F7E29C2E87A}",
					["num"] = 3,
				},
				[8] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[9] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
				[10] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 18,
				[4] = 19,
			},
		},
		[18] = {
			["name"] = "S-8TsMx80,FAB-250x4,R-73x2,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{B8M1_20_S8TsM_DUAL_L}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 6,
				},
				[5] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 7,
				},
				[6] = {
					["CLSID"] = "{B8M1_20_S8TsM_DUAL_R}",
					["num"] = 8,
				},
				[7] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[8] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
				[9] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
				[10] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[19] = {
			["name"] = "S-8OFP2x80,FAB-250x4,R-73x2,ECM",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{B8M1_20_S8OFP2_DUAL_L}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 6,
				},
				[5] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 7,
				},
				[6] = {
					["CLSID"] = "{B8M1_20_S8OFP2_DUAL_R}",
					["num"] = 8,
				},
				[7] = {
					["CLSID"] = "{FBC29BFE-3D24-4C64-B81D-941239D12249}",
					["num"] = 9,
				},
				[8] = {
					["CLSID"] = "{RKL609_R}",
					["num"] = 10,
				},
				[9] = {
					["CLSID"] = "{RKL609_L}",
					["num"] = 1,
				},
				[10] = {
					["CLSID"] = "{3C612111-C7AD-476E-8A8E-2485812F4E5C}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "J-11A",
}
return unitPayloads
