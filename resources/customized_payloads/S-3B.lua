local unitPayloads = {
	["name"] = "S-3B",
	["payloads"] = {
		[1] = {
			["name"] = "SEAD",
			["pylons"] = {
										
			},
			["tasks"] = {
				[1] = 23,
			},
		},
		[2] = {
			["name"] = "ANTISHIP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{8B7CADF9-4954-46B3-8CFB-93F2F5B90B03}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{8B7CADF9-4954-46B3-8CFB-93F2F5B90B03}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 30,
			},
		},
		[3] = {
			["name"] = "CAP",
			["pylons"] = {

			},
			["tasks"] = {
				[1] = 33,
			},
		},
		[4] = {
			["name"] = "STRIKE",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{AF42E6DF-9A60-46D8-A9A0-1708B241AADB}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{AF42E6DF-9A60-46D8-A9A0-1708B241AADB}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 33,
			},
		},
		[5] = {
			["name"] = "CAS",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{444BA8AE-82A7-4345-842E-76154EFCCA46}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{444BA8AE-82A7-4345-842E-76154EFCCA46}",
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "{AB8B8299-F1CC-4359-89B5-2172E0CF4A5A}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{AB8B8299-F1CC-4359-89B5-2172E0CF4A5A}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 32,
			},
		},
	},
	["unitType"] = "S-3B",
}
return unitPayloads