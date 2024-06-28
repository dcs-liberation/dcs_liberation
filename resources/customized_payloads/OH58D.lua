local unitPayloads = {
	["name"] = "OH58D",
	["payloads"] = {
		[1] = {
			["name"] = "Liberation CAS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "OH58D_AGM_114_R",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "OH58D_M3P_L500",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
		[2] = {
			["displayName"] = "Liberation DEAD",
			["name"] = "Liberation DEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "OH58D_AGM_114_R",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "OH58D_AGM_114_L",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
		[3] = {
			["displayName"] = "Liberation BAI",
			["name"] = "Liberation BAI",
			["pylons"] = {
				[1] = {
					["CLSID"] = "OH58D_AGM_114_R",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{M260_APKWS_M151}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
		[4] = {
			["displayName"] = "Liberation OCA/Aircraft",
			["name"] = "Liberation OCA/Aircraft",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{M260_APKWS_M151}",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "{M260_APKWS_M151}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
		[5] = {
			["displayName"] = "Liberation Escort",
			["name"] = "Liberation Escort",
			["pylons"] = {
				[1] = {
					["CLSID"] = "OH58D_AGM_114_R",
					["num"] = 5,
				},
				[2] = {
					["CLSID"] = "OH58D_FIM_92_L",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
	},
	["tasks"] = {
		[1] = 11,
		[2] = 31,
		[3] = 32,
		[4] = 16,
		[5] = 18,
		[6] = 35,
		[7] = 30,
		[8] = 17,
	},
	["unitType"] = "OH58D",
}
return unitPayloads
