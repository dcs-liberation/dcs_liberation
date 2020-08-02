local unitPayloads = {
	["name"] = "FW-190A8",
	["payloads"] = {
		[1] = {
			["name"] = "CAS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{WGr21}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{WGr21}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{SC_250_T1_L2}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[2] = {
			["name"] = "STRIKE",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{SD_500_A}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[3] = {
			["name"] = "CAP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "<CLEAN>",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[4] = {
			["name"] = "ANTISHIP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{SD_500_A}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{WGr21}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{WGr21}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "FW-190A8",
}
return unitPayloads
