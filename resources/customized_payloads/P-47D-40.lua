local unitPayloads = {
	["name"] = "P-47D-40",
	["payloads"] = {
		[1] = {
			["name"] = "CAP",
			["pylons"] = {
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[2] = {
			["name"] = "CAS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{P47_5_HVARS_ON_LEFT_WING_RAILS}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{P47_5_HVARS_ON_RIGHT_WING_RAILS}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[3] = {
			["name"] = "SEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{P47_5_HVARS_ON_LEFT_WING_RAILS}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{P47_5_HVARS_ON_RIGHT_WING_RAILS}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[4] = {
			["name"] = "STRIKE",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{AN-M64}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{AN-M64}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{AN-M64}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[5] = {
			["name"] = "ANTISHIP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{P47_5_HVARS_ON_RIGHT_WING_RAILS}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{P47_5_HVARS_ON_LEFT_WING_RAILS}",
					["num"] = 4,
				},
				[3] = {
					["CLSID"] = "{AN-M64}",
					["num"] = 1,
				},
			},
			["tasks"] = {
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "P-47D-40",
}
return unitPayloads
