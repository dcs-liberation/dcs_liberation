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
				[1] = {
					["CLSID"] = "{UH60_FUEL_TANK_230}",
					["num"] = 7,
				},
				[2] = {
					["CLSID"] = "{UH60_FUEL_TANK_230}",
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "{UH60_FUEL_TANK_230}",
					["num"] = 2,
				},
				[4] = {
					["CLSID"] = "{UH60_FUEL_TANK_230}",
					["num"] = 6,
				},
				[5] = {
					["CLSID"] = "{UH60_SEAT_GUNNER_L}",
					["num"] = 3,
				},
				[6] = {
					["CLSID"] = "{UH60_SEAT_CARGO_ALL}",
					["num"] = 4,
				},
				[7] = {
					["CLSID"] = "{UH60_SEAT_GUNNER_R}",
					["num"] = 5,
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
