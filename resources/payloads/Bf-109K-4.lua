local unitPayloads = {
	["name"] = "Bf-109K-4",
	["payloads"] = {
		[1] = {
			["name"] = "Fuel Tank",
			["pylons"] = {
				[1] = {
					["CLSID"] = "BF109K_4_FUEL_TANK",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 11, -- CAP
				[2] = 16, -- AFAC
				[3] = 18, -- Escort
			},
		},
		[2] = {
			["name"] = "SC250",
			["pylons"] = {
				[1] = {
					["CLSID"] = "SC_501_SC250",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 34, -- RunwayAttack
				[2] = 31, -- CAS
				[3] = 30, -- AntishipStrike
				[4] = 32, -- GroundAttack
			},
		},
		[3] = {
			["name"] = "SC500",
			["pylons"] = {
				[1] = {
					["CLSID"] = "SC_501_SC500",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 34, -- RunwayAttack
				[2] = 31, -- CAS
				[3] = 30, -- AntishipStrike
				[4] = 32, -- GroundAttack
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "Bf-109K-4",
}
return unitPayloads
