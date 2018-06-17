local unitPayloads = {
	["name"] = "SA342L",
	["payloads"] = {
		[1] = {
			["name"] = "M621, 8xSNEB68 EAP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{LAU_SNEB68G}",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[2] = {
			["name"] = "M621, 8xSNEB68 EAP, IR Deflector",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{LAU_SNEB68G}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{IR_Deflector}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[3] = {
			["name"] = "M621, 8xSNEB68 EAP, IR Deflector, Sand Filter",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{LAU_SNEB68G}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{IR_Deflector}",
					["num"] = 6,
				},
				[3] = {
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
	["unitType"] = "SA342L",
}
return unitPayloads
