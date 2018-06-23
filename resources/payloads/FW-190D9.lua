local unitPayloads = {
	["name"] = "FW-190D9",
	["payloads"] = {
		[1] = {
			["name"] = "SC500",
			["pylons"] = {
				[1] = {
					["CLSID"] = "SC_501_SC500",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 34,
				[2] = 31,
				[3] = 30,
				[4] = 32,
			},
		},
		[2] = {
			["name"] = "Fuel Tank",
			["pylons"] = {
				[1] = {
					["CLSID"] = "FW109_FUEL_TANK",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 11,
				[2] = 16,
				[3] = 18,
			},
		},
		[3] = {
			["name"] = "R4M",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FW_190_R4M_RGHT_WING}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{FW_190_R4M_LEFT_WING}",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 11,
				[2] = 10,
				[3] = 32,
				[4] = 31,
			},
		},
		[4] = {
			["name"] = "BR 21",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{WGr21}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{WGr21}",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 11,
				[2] = 10,
				[3] = 32,
				[4] = 31,
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "FW-190D9",
}
return unitPayloads
