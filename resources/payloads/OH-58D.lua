local unitPayloads = {
	["name"] = "OH-58D",
	["payloads"] = {
		[1] = {
			["name"] = "2xAGM-114, 7xHYDRA-70",
			["pylons"] = {
				[1] = {
					["CLSID"] = "AGM114x2_OH_58",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "M260_HYDRA",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 18,
				[2] = 31,
				[3] = 32,
			},
		},
		[2] = {
			["name"] = "4xAGM-114",
			["pylons"] = {
				[1] = {
					["CLSID"] = "AGM114x2_OH_58",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "AGM114x2_OH_58",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 18,
				[2] = 31,
				[3] = 32,
			},
		},
		[3] = {
			["name"] = "M-3, 7xHYDRA-70",
			["pylons"] = {
				[1] = {
					["CLSID"] = "oh-58-brauning",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "M260_HYDRA",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 18,
				[2] = 31,
				[3] = 32,
			},
		},
		[4] = {
			["name"] = "2xAGM-114, M-3",
			["pylons"] = {
				[1] = {
					["CLSID"] = "oh-58-brauning",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "AGM114x2_OH_58",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 18,
				[2] = 31,
				[3] = 32,
			},
		},
		[5] = {
			["name"] = "14xHYDRA-70",
			["pylons"] = {
				[1] = {
					["CLSID"] = "M260_HYDRA",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "M260_HYDRA",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 18,
				[2] = 31,
				[3] = 32,
			},
		},
		[6] = {
			["name"] = "14xHYDRA-70 WP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "M260_HYDRA_WP",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "M260_HYDRA_WP",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
	},
	["unitType"] = "OH-58D",
}
return unitPayloads
