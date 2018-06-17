local unitPayloads = {
	["name"] = "C-101EB",
	["payloads"] = {
		[1] = {
			["name"] = "Smoke System: White Smoke",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{SMOKE-SYSTEM-AVIOJET}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 17,
			},
		},
		[2] = {
			["name"] = "Smoke System: White Smoke+Red Colorant",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{SMOKE-RED-AVIOJET}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{SMOKE-SYSTEM-AVIOJET}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 17,
			},
		},
		[3] = {
			["name"] = "Smoke System: White Smoke+Yellow Colorant",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{SMOKE-YELLOW-AVIOJET}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{SMOKE-SYSTEM-AVIOJET}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 17,
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "C-101EB",
}
return unitPayloads
