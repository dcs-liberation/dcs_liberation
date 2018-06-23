local unitPayloads = {
	["name"] = "P-51D",
	["payloads"] = {
		[1] = {
			["name"] = "Fuel75*2",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{DT75GAL}",
					["num"] = 7,
				},
				[2] = {
					["CLSID"] = "{DT75GAL}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 11,
				[2] = 19,
				[3] = 16,
			},
		},
		[2] = {
			["name"] = "HVAR*6,Fuel75*2",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HVAR}",
					["num"] = 10,
				},
				[2] = {
					["CLSID"] = "{HVAR}",
					["num"] = 9,
				},
				[3] = {
					["CLSID"] = "{HVAR}",
					["num"] = 8,
				},
				[4] = {
					["CLSID"] = "{DT75GAL}",
					["num"] = 7,
				},
				[5] = {
					["CLSID"] = "{DT75GAL}",
					["num"] = 4,
				},
				[6] = {
					["CLSID"] = "{HVAR}",
					["num"] = 3,
				},
				[7] = {
					["CLSID"] = "{HVAR}",
					["num"] = 2,
				},
				[8] = {
					["CLSID"] = "{HVAR}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
		[3] = {
			["name"] = "HVAR*6,M64*2",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HVAR}",
					["num"] = 10,
				},
				[2] = {
					["CLSID"] = "{HVAR}",
					["num"] = 9,
				},
				[3] = {
					["CLSID"] = "{HVAR}",
					["num"] = 8,
				},
				[4] = {
					["CLSID"] = "{AN-M64}",
					["num"] = 7,
				},
				[5] = {
					["CLSID"] = "{AN-M64}",
					["num"] = 4,
				},
				[6] = {
					["CLSID"] = "{HVAR}",
					["num"] = 3,
				},
				[7] = {
					["CLSID"] = "{HVAR}",
					["num"] = 2,
				},
				[8] = {
					["CLSID"] = "{HVAR}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 31,
				[2] = 32,
				[3] = 30,
			},
		},
		[4] = {
			["name"] = "HVAR*6",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HVAR}",
					["num"] = 10,
				},
				[2] = {
					["CLSID"] = "{HVAR}",
					["num"] = 9,
				},
				[3] = {
					["CLSID"] = "{HVAR}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{HVAR}",
					["num"] = 1,
				},
				[5] = {
					["CLSID"] = "{HVAR}",
					["num"] = 8,
				},
				[6] = {
					["CLSID"] = "{HVAR}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 31,
				[2] = 32,
				[3] = 30,
				[4] = 16,
			},
		},
		[5] = {
			["name"] = "M64*2",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{AN-M64}",
					["num"] = 7,
				},
				[2] = {
					["CLSID"] = "{AN-M64}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 32,
				[2] = 30,
				[3] = 31,
				[4] = 34,
			},
		},
		[6] = {
			["name"] = "HVAR*10",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HVAR}",
					["num"] = 10,
				},
				[2] = {
					["CLSID"] = "{HVAR}",
					["num"] = 9,
				},
				[3] = {
					["CLSID"] = "{HVAR}",
					["num"] = 8,
				},
				[4] = {
					["CLSID"] = "{HVAR}",
					["num"] = 7,
				},
				[5] = {
					["CLSID"] = "{HVAR}",
					["num"] = 6,
				},
				[6] = {
					["CLSID"] = "{HVAR}",
					["num"] = 5,
				},
				[7] = {
					["CLSID"] = "{HVAR}",
					["num"] = 4,
				},
				[8] = {
					["CLSID"] = "{HVAR}",
					["num"] = 3,
				},
				[9] = {
					["CLSID"] = "{HVAR}",
					["num"] = 2,
				},
				[10] = {
					["CLSID"] = "{HVAR}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 31,
				[2] = 32,
				[3] = 34,
				[4] = 30,
			},
		},
		[7] = {
			["name"] = "Smokes",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HVAR_SMOKE_GENERATOR}",
					["num"] = 10,
				},
				[2] = {
					["CLSID"] = "{HVAR_SMOKE_GENERATOR}",
					["num"] = 1,
				},
			},
			["tasks"] = {
			},
		},
	},
	["unitType"] = "P-51D",
}
return unitPayloads
