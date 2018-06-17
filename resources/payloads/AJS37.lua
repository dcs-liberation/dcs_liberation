local unitPayloads = {
	["name"] = "AJS37",
	["payloads"] = {
		[1] = {
			["name"] = "Battlefield Air Interdiction: RB-75*4, RB-24J*2, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{RB75}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{RB75}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{RB75}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{RB75}",
					["num"] = 6,
				},
				[5] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 1,
				},
				[6] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 7,
				},
				[7] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[2] = {
			["name"] = "Anti-ship: RB-04E*2, RB-74*2, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{Rb04}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{Rb04}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{Robot74}",
					["num"] = 3,
				},
				[5] = {
					["CLSID"] = "{Robot74}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 30,
			},
		},
		[3] = {
			["name"] = "Anti-ship (Heavy Mav): RB-75T*4, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{RB75T}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{RB75T}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{RB75T}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{RB75T}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 30,
			},
		},
		[4] = {
			["name"] = "Hard Target (Countermeasures): RB-05, XT, KB, U22",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{Robot05}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "{Robot05}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{U22}",
					["num"] = 6,
				},
				[5] = {
					["CLSID"] = "{KB}",
					["num"] = 2,
				},
				[6] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 7,
				},
				[7] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[5] = {
			["name"] = "Hard Target (MAV): RB-75T*2, RB-74*2, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{RB75T}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{RB75T}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{Robot74}",
					["num"] = 6,
				},
				[5] = {
					["CLSID"] = "{Robot74}",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[6] = {
			["name"] = "Ferry Flight: XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[7] = {
			["name"] = "CAS (75 GUN): RB-75*2, AKAN",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{RB75}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{RB75}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{AKAN}",
					["num"] = 6,
				},
				[4] = {
					["CLSID"] = "{AKAN}",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[8] = {
			["name"] = "CAP: RB-74*4, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{Robot74}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{Robot74}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{Robot74}",
					["num"] = 6,
				},
				[4] = {
					["CLSID"] = "{Robot74}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[9] = {
			["name"] = "Countermeasures Escort: U/22A, KB",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{U22A}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{KB}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{Robot74}",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{Robot74}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[10] = {
			["name"] = "Strike: BK90 (MJ1)*2, RB-74*2, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{BK90MJ1}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{BK90MJ1}",
					["num"] = 6,
				},
				[3] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{Robot74}",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{Robot74}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[11] = {
			["name"] = "CAS: AKAN, RB-05A",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{Robot05}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{Robot05}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{AKAN}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{AKAN}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[12] = {
			["name"] = "CAP (6 AAM): RB-74*4, RB-24J*2, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{Robot74}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{Robot74}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{Robot74}",
					["num"] = 6,
				},
				[4] = {
					["CLSID"] = "{Robot74}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[6] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 7,
				},
				[7] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[13] = {
			["name"] = "Rocket Half Load HE: ARAK HE*2, RB-74*2, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{ARAKM70BHE}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{ARAKM70BHE}",
					["num"] = 5,
				},
				[3] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{Robot74}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{Robot74}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[14] = {
			["name"] = "CAP / Intecept: RB-05A*2, RB-74*2, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{Robot05}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{Robot05}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{Robot74}",
					["num"] = 6,
				},
				[4] = {
					["CLSID"] = "{Robot74}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[15] = {
			["name"] = "Bombs Low-drag: SB71LD*16, RB-24J*2, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{M71BOMB}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{M71BOMB}",
					["num"] = 6,
				},
				[3] = {
					["CLSID"] = "{M71BOMB}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{M71BOMB}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[6] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 7,
				},
				[7] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[16] = {
			["name"] = "SEAD: RB-75T*2, U22/A, KB, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{RB75T}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{RB75T}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{KB}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{U22}",
					["num"] = 6,
				},
				[5] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[17] = {
			["name"] = "Anti-Ship (Modern): RB-15F*2, RB-74*2, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{Rb15}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{Rb15}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{Robot74}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{Robot74}",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 30,
			},
		},
		[18] = {
			["name"] = "New Payload",
			["pylons"] = {
			},
			["tasks"] = {
			},
		},
		[19] = {
			["name"] = "CAP (AJ37): RB-24J*2",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 6,
				},
				[4] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[20] = {
			["name"] = "ECM Escort Anti-ship: RB-04E, KB, RB-74*2, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{KB}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{Rb04}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{Robot74}",
					["num"] = 3,
				},
				[5] = {
					["CLSID"] = "{Robot74}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 30,
			},
		},
		[21] = {
			["name"] = "Bombs High-drag: SB71HD*16, XT, RB-24J",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{M71BOMBD}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{M71BOMBD}",
					["num"] = 5,
				},
				[3] = {
					["CLSID"] = "{M71BOMBD}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{M71BOMBD}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[6] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 7,
				},
				[7] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[22] = {
			["name"] = "Anti-ship (Light Mav): RB-75*4, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{RB75}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{RB75}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{RB75}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{RB75}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 30,
			},
		},
		[23] = {
			["name"] = "Rocket Full Load HE:  ARAK HE*4, RB-24J, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{ARAKM70BHE}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{ARAKM70BHE}",
					["num"] = 5,
				},
				[3] = {
					["CLSID"] = "{ARAKM70BHE}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{ARAKM70BHE}",
					["num"] = 6,
				},
				[5] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[6] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 7,
				},
				[7] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[24] = {
			["name"] = "Illumination: LYSB*8, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{LYSBOMB}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{LYSBOMB}",
					["num"] = 5,
				},
				[3] = {
					["CLSID"] = "{LYSBOMB}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{LYSBOMB}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[25] = {
			["name"] = "Anti-ship (RB05): RB-05A*2, RB-74*2, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{Robot05}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{Robot05}",
					["num"] = 5,
				},
				[4] = {
					["CLSID"] = "{Robot74}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{Robot74}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 30,
			},
		},
		[26] = {
			["name"] = "CAP (Gun): AKAN*2, RB-74*2, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{Robot74}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{Robot74}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{AKAN}",
					["num"] = 6,
				},
				[4] = {
					["CLSID"] = "{AKAN}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[27] = {
			["name"] = "Hard Target: RB-05A*2, RB-74*2, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{Robot05}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{Robot05}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{Robot74}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{Robot74}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[28] = {
			["name"] = "RB-05*2, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{Robot05}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{Robot05}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
		[29] = {
			["name"] = "CAS: ARAK M70 HE*4, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{ARAKM70BHE}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{ARAKM70BHE}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{ARAKM70BHE}",
					["num"] = 5,
				},
				[5] = {
					["CLSID"] = "{ARAKM70BHE}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[30] = {
			["name"] = "Runway Strike: SB71HD*16, RB-24J, XT",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{VIGGEN_X-TANK}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{M71BOMBD}",
					["num"] = 3,
				},
				[3] = {
					["CLSID"] = "{M71BOMBD}",
					["num"] = 5,
				},
				[4] = {
					["CLSID"] = "{M71BOMBD}",
					["num"] = 2,
				},
				[5] = {
					["CLSID"] = "{M71BOMBD}",
					["num"] = 6,
				},
				[6] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 1,
				},
				[7] = {
					["CLSID"] = "{Robot24J}",
					["num"] = 7,
				},
			},
			["tasks"] = {
				[1] = 34,
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "AJS37",
}
return unitPayloads
