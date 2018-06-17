local unitPayloads = {
	["name"] = "SA342Minigun",
	["payloads"] = {
		[1] = {
			["name"] = "IR Deflector",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{IR_Deflector}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[2] = {
			["name"] = "IR Deflector, Sand Filter",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{IR_Deflector}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{FAS}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "SA342Minigun",
}
return unitPayloads
