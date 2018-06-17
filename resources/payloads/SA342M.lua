local unitPayloads = {
	["name"] = "SA342M",
	["payloads"] = {
		[1] = {
			["name"] = "HOT3x4",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HOT3D}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{HOT3G}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{HOT3D}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{HOT3G}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[2] = {
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
		[3] = {
			["name"] = "Hot3x4, FAS, IR Deflector",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HOT3D}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{HOT3G}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{HOT3D}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{HOT3G}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{FAS}",
					["num"] = 5,
				},
				[6] = {
					["CLSID"] = "{IR_Deflector}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[4] = {
			["name"] = "HOT3x2",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HOT3D}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{HOT3G}",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[5] = {
			["name"] = "Hot3x4, IR Deflector",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HOT3D}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{HOT3G}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{HOT3D}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{HOT3G}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{IR_Deflector}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
		[6] = {
			["name"] = "Hot3x2, IR Deflector",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HOT3D}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{HOT3G}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{IR_Deflector}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 31,
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "SA342M",
}
return unitPayloads
