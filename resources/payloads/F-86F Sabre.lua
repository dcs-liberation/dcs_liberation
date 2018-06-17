local unitPayloads = {
	["name"] = "F-86F Sabre",
	["payloads"] = {
		[1] = {
			["name"] = "120gal Fuel*2",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{PTB_120_F86F35}",
					["num"] = 4,
				},
				[2] = {
					["CLSID"] = "{PTB_120_F86F35}",
					["num"] = 7,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[2] = {
			["name"] = "200gal Fuel*2",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{PTB_200_F86F35}",
					["num"] = 10,
				},
				[2] = {
					["CLSID"] = "{PTB_200_F86F35}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[3] = {
			["name"] = "120gal Fuel*2, 200gal Fuel*2",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{PTB_200_F86F35}",
					["num"] = 10,
				},
				[2] = {
					["CLSID"] = "{PTB_120_F86F35}",
					["num"] = 7,
				},
				[3] = {
					["CLSID"] = "{PTB_120_F86F35}",
					["num"] = 4,
				},
				[4] = {
					["CLSID"] = "{PTB_200_F86F35}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 11,
			},
		},
		[4] = {
			["name"] = "GAR-8*2",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{GAR-8}",
					["num"] = 6,
				},
				[2] = {
					["CLSID"] = "{GAR-8}",
					["num"] = 5,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 18,
				[4] = 19,
			},
		},
		[5] = {
			["name"] = "120gal Fuel*2, GAR-8*2",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{PTB_120_F86F35}",
					["num"] = 7,
				},
				[2] = {
					["CLSID"] = "{GAR-8}",
					["num"] = 6,
				},
				[3] = {
					["CLSID"] = "{GAR-8}",
					["num"] = 5,
				},
				[4] = {
					["CLSID"] = "{PTB_120_F86F35}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 10,
				[2] = 11,
				[3] = 18,
				[4] = 19,
			},
		},
		[6] = {
			["name"] = "HVAR*16",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{HVARx2}",
					["num"] = 10,
				},
				[2] = {
					["CLSID"] = "{HVARx2}",
					["num"] = 9,
				},
				[3] = {
					["CLSID"] = "{HVARx2}",
					["num"] = 8,
				},
				[4] = {
					["CLSID"] = "{HVARx2}",
					["num"] = 7,
				},
				[5] = {
					["CLSID"] = "{HVARx2}",
					["num"] = 4,
				},
				[6] = {
					["CLSID"] = "{HVARx2}",
					["num"] = 3,
				},
				[7] = {
					["CLSID"] = "{HVARx2}",
					["num"] = 2,
				},
				[8] = {
					["CLSID"] = "{HVARx2}",
					["num"] = 1,
				},
			},
			["tasks"] = {
				[1] = 32,
				[2] = 31,
				[3] = 30,
			},
		},
		[7] = {
			["name"] = "200gal Fuel*2, HVARx2*4",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{PTB_200_F86F35}",
					["num"] = 10,
				},
				[2] = {
					["CLSID"] = "{PTB_200_F86F35}",
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "{HVARx2}",
					["num"] = 8,
				},
				[4] = {
					["CLSID"] = "{HVARx2}",
					["num"] = 7,
				},
				[5] = {
					["CLSID"] = "{HVARx2}",
					["num"] = 4,
				},
				[6] = {
					["CLSID"] = "{HVARx2}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 31,
				[2] = 32,
			},
		},
		[8] = {
			["name"] = "AN-M64*2",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{F86ANM64}",
					["num"] = 7,
				},
				[2] = {
					["CLSID"] = "{F86ANM64}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 31,
				[2] = 32,
				[3] = 30,
			},
		},
		[9] = {
			["name"] = "200gal Fuel*2, AN-M64*2",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{PTB_200_F86F35}",
					["num"] = 10,
				},
				[2] = {
					["CLSID"] = "{PTB_200_F86F35}",
					["num"] = 1,
				},
				[3] = {
					["CLSID"] = "{F86ANM64}",
					["num"] = 7,
				},
				[4] = {
					["CLSID"] = "{F86ANM64}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 31,
				[2] = 32,
			},
		},
		[10] = {
			["name"] = "M117*2",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{00F5DAC4-0466-4122-998F-B1A298E34113}",
					["num"] = 7,
				},
				[2] = {
					["CLSID"] = "{00F5DAC4-0466-4122-998F-B1A298E34113}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 31,
				[2] = 32,
				[3] = 30,
			},
		},
	},
	["tasks"] = {
	},
	["unitType"] = "F-86F Sabre",
}
return unitPayloads
