local unitPayloads = {
	["name"] = "B-52H",
	["payloads"] = {
		[1] = {
			["name"] = "SEAD",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{45447F82-01B5-4029-A572-9AAD28AF0275}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{8DCAF3A3-7FCF-41B8-BB88-58DEDA878EDE}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{45447F82-01B5-4029-A572-9AAD28AF0275}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 33,
			},
		},
		[2] = {
			["name"] = "ANTISHIP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{46ACDCF8-5451-4E26-BDDB-E78D5830E93C}",
					["num"] = 2,
				},
			},
			["tasks"] = {
				[1] = 30,
			},
		},
		[3] = {
			["name"] = "STRIKE",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{696CFFC4-0BDE-42A8-BE4B-0BE3D9DD723C}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{6C47D097-83FF-4FB2-9496-EAB36DDF0B05}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{696CFFC4-0BDE-42A8-BE4B-0BE3D9DD723C}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 32,
				[2] = 34,
			},
		},
		[4] = {
			["name"] = "CAP",
			["pylons"] = {
			},
			["tasks"] = {
			},
		},
		[5] = {
			["name"] = "CAS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{4CD2BB0F-5493-44EF-A927-9760350F7BA1}",
					["num"] = 3,
				},
				[2] = {
					["CLSID"] = "{4CD2BB0F-5493-44EF-A927-9760350F7BA1}",
					["num"] = 1,
				},
			},
			["tasks"] = {
			},
		},
	},
	["unitType"] = "B-52H",
}
return unitPayloads
