local unitPayloads = {
	["name"] = "AH-1W",
	["payloads"] = {
		[1] = {
			["name"] = "14xHYDRA-70 WP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "M260_HYDRA_WP",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "M260_HYDRA_WP",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
		[2] = {
			["name"] = "38xHYDRA-70 WP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{3DFB7321-AB0E-11d7-9897-000476191836}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{3DFB7321-AB0E-11d7-9897-000476191836}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
		[3] = {
			["name"] = "8xBGM-71, 14xHYDRA-70",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{3EA17AB0-A805-4D9E-8732-4CE00CB00F17}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "M260_HYDRA",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "M260_HYDRA",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{3EA17AB0-A805-4D9E-8732-4CE00CB00F17}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 18,
				[2] = 31,
				[3] = 32,
			},
		},
		[4] = {
			["name"] = "8xBGM-71, 14xHYDRA-70 WP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{3EA17AB0-A805-4D9E-8732-4CE00CB00F17}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "M260_HYDRA_WP",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "M260_HYDRA_WP",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{3EA17AB0-A805-4D9E-8732-4CE00CB00F17}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
		[5] = {
			["name"] = "8xBGM-71, 38xHYDRA-70 WP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{3EA17AB0-A805-4D9E-8732-4CE00CB00F17}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{3DFB7321-AB0E-11d7-9897-000476191836}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{3DFB7321-AB0E-11d7-9897-000476191836}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{3EA17AB0-A805-4D9E-8732-4CE00CB00F17}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
		[6] = {
			["name"] = "14xHYDRA-70",
			["pylons"] = {
				[1] = {
					["CLSID"] = "M260_HYDRA",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "M260_HYDRA",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 18,
				[2] = 31,
				[3] = 32,
			},
		},
		[7] = {
			["name"] = "38xHYDRA-70",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FD90A1DC-9147-49FA-BF56-CB83EF0BD32B}",
					["num"] = 2,
				},
				[2] = {
					["CLSID"] = "{FD90A1DC-9147-49FA-BF56-CB83EF0BD32B}",
					["num"] = 3,
				},
			},
			["tasks"] = {
				[1] = 18,
				[2] = 31,
				[3] = 32,
			},
		},
		[8] = {
			["name"] = "8xAGM-114",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{88D18A5E-99C8-4B04-B40B-1C02F2018B6E}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{88D18A5E-99C8-4B04-B40B-1C02F2018B6E}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 18,
				[2] = 31,
				[3] = 32,
			},
		},
		[9] = {
			["name"] = "28xHYDRA-70",
			["pylons"] = {
				[1] = {
					["CLSID"] = "M260_HYDRA",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "M260_HYDRA",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "M260_HYDRA",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "M260_HYDRA",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 18,
				[2] = 31,
				[3] = 32,
			},
		},
		[10] = {
			["name"] = "8xBGM-71, 38xHYDRA-70",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{3EA17AB0-A805-4D9E-8732-4CE00CB00F17}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{FD90A1DC-9147-49FA-BF56-CB83EF0BD32B}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{FD90A1DC-9147-49FA-BF56-CB83EF0BD32B}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{3EA17AB0-A805-4D9E-8732-4CE00CB00F17}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 18,
				[2] = 31,
				[3] = 32,
			},
		},
		[11] = {
			["name"] = "8xAGM-114, 38xHYDRA-70 WP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{88D18A5E-99C8-4B04-B40B-1C02F2018B6E}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{3DFB7321-AB0E-11d7-9897-000476191836}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{3DFB7321-AB0E-11d7-9897-000476191836}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{88D18A5E-99C8-4B04-B40B-1C02F2018B6E}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
		[12] = {
			["name"] = "8xBGM-71",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{3EA17AB0-A805-4D9E-8732-4CE00CB00F17}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{3EA17AB0-A805-4D9E-8732-4CE00CB00F17}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 18,
				[2] = 31,
				[3] = 32,
			},
		},
		[13] = {
			["name"] = "8xAGM-114, 14xHYDRA-70 WP",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{88D18A5E-99C8-4B04-B40B-1C02F2018B6E}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "M260_HYDRA_WP",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "M260_HYDRA_WP",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{88D18A5E-99C8-4B04-B40B-1C02F2018B6E}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 16,
			},
		},
		[14] = {
			["name"] = "76xHYDRA-70",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{FD90A1DC-9147-49FA-BF56-CB83EF0BD32B}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{FD90A1DC-9147-49FA-BF56-CB83EF0BD32B}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{FD90A1DC-9147-49FA-BF56-CB83EF0BD32B}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{FD90A1DC-9147-49FA-BF56-CB83EF0BD32B}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 18,
				[2] = 31,
				[3] = 32,
			},
		},
		[15] = {
			["name"] = "8xAGM-114, 38xHYDRA-70",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{88D18A5E-99C8-4B04-B40B-1C02F2018B6E}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "{FD90A1DC-9147-49FA-BF56-CB83EF0BD32B}",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "{FD90A1DC-9147-49FA-BF56-CB83EF0BD32B}",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{88D18A5E-99C8-4B04-B40B-1C02F2018B6E}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 18,
				[2] = 31,
				[3] = 32,
				[4] = 30,
			},
		},
		[16] = {
			["name"] = "8xAGM-114, 14xHYDRA-70",
			["pylons"] = {
				[1] = {
					["CLSID"] = "{88D18A5E-99C8-4B04-B40B-1C02F2018B6E}",
					["num"] = 1,
				},
				[2] = {
					["CLSID"] = "M260_HYDRA",
					["num"] = 2,
				},
				[3] = {
					["CLSID"] = "M260_HYDRA",
					["num"] = 3,
				},
				[4] = {
					["CLSID"] = "{88D18A5E-99C8-4B04-B40B-1C02F2018B6E}",
					["num"] = 4,
				},
			},
			["tasks"] = {
				[1] = 18,
				[2] = 31,
				[3] = 32,
			},
		},
	},
	["unitType"] = "AH-1W",
}
return unitPayloads
