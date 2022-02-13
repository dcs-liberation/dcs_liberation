local unitPayloads =
{
	["name"] = "UH-60L",
	["payloads"] =
	{
		[1] =
		{
			["name"] = "Liberation Ferry",
			["pylons"] =
			{
				[1] =
				{
					["CLSID"] = "{UH60_FUEL_TANK_230}",
					["num"] = 1,
				},
				[2] =
				{
					["CLSID"] = "{UH60_FUEL_TANK_230}",
					["num"] = 2,
				},
				[3] =
				{
					["CLSID"] = "{UH60_FUEL_TANK_230}",
					["num"] = 3,
				},
				[4] =
				{
					["CLSID"] = "{UH60_FUEL_TANK_230}",
					["num"] = 4,
				},
			},
			["tasks"] =
			{
				[1] = 35,
				[2] = 17,
			},
		},
	},
	["tasks"] = {},
	["unitType"] = "UH-60L",
}
return unitPayloads
