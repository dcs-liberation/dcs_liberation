local unitPayloads = {
	["name"] = "SA342Mistral",
	["payloads"] = {
		[1] = {
			["name"] = "Mistral x 4",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{MBDA_MistralD}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{MBDA_MistralG}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{MBDA_MistralD}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{MBDA_MistralG}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 18,
			},
		},
		[2] = {
			["name"] = "Mistral x 4, IR Deflector",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{MBDA_MistralD}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{MBDA_MistralG}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{MBDA_MistralD}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{MBDA_MistralG}",
					["num"] = 4,
				},
				[5] = {
					["CLSID"] = "{IR_Deflector}",
					["num"] = 6,
				},
			},
			["tasks"] = {
				[1] = 18,
			},
		},
		[3] = {
			["name"] = "Mistral x 4, IR Deflector, Sand Filter",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{MBDA_MistralD}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{MBDA_MistralG}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{MBDA_MistralD}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{MBDA_MistralG}",
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
				[1] = 18,
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "SA342Mistral",
}
return unitPayloads
