local unitPayloads = {
	["name"] = "UH-1H",
	["payloads"] = {
		[1] = {
			["name"] = "M134 Minigun*2, XM158*2",
			["pylons"] = {
				[1] = {
					["CLSID"] = "M134_L",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "XM158_MK5",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "XM158_MK5",
					["num"] = 5,
				},
				[4] = {
					["CLSID"] = "M134_R",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 32,
				[2] = 31,
				[3] = 35,
				[4] = 16,
			},
		},
	},
	["unitType"] = "UH-1H",
}
return unitPayloads
