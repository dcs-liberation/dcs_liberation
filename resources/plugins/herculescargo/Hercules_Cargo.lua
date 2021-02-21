
-- Hercules Cargo Drop Events by Anubis Yinepu

-- This script will only work for the Herculus mod by Anubis
-- Payloads carried by pylons 11, 12 and 13 need to be declared in the Herculus_Loadout.lua file
-- Except for Ammo pallets, this script will spawn whatever payload gets launched from pylons 11, 12 and 13
-- Pylons 11, 12 and 13 are moveable within the Herculus cargobay area
-- Ammo pallets can only be jettisoned from these pylons with no benefit to DCS world
-- To benefit DCS world, Ammo pallets need to be off/on loaded using DCS arming and refueling window
-- Cargo_Container_Enclosed = true: Cargo enclosed in container with parachute, need to be dropped from 100m (300ft) or more, except when parked on ground
-- Cargo_Container_Enclosed = false: Open cargo with no parachute, need to be dropped from 10m (30ft) or less

Hercules_Cargo = {}
Hercules_Cargo.Hercules_Cargo_Drop_Events = {}
local GT_DisplayName = ""
local GT_Name = ""
local Cargo_Drop_initiator = ""
local Cargo_Container_Enclosed = false
local SoldierGroup = false
local ParatrooperCount = 1
local ParatrooperGroupSpawnInit = false
local ParatrooperGroupSpawn = false

local Herc_j = 0
local Herc_Cargo = {}
Herc_Cargo.Cargo_Drop_Direction = 0
Herc_Cargo.Cargo_Contents = ""
Herc_Cargo.Cargo_Type_name = ""
Herc_Cargo.Cargo_over_water = false
Herc_Cargo.Container_Enclosed = false
Herc_Cargo.offload_cargo = false
Herc_Cargo.all_cargo_survive_to_the_ground = false
Herc_Cargo.all_cargo_gets_destroyed = false
Herc_Cargo.destroy_cargo_dropped_without_parachute = false
Herc_Cargo.scheduleFunctionID = 0

local CargoHeading = 0
local Cargo_Drop_Position = {}

local SoldierUnitID = 12000
local SoldierGroupID = 12000
local GroupSpacing = 0
--added by wrench
Hercules_Cargo.types = {
	["ATGM M1045 HMMWV TOW Air [7183lb]"] = {['name'] = "M1045 HMMWV TOW", ['container'] = true},
	["ATGM M1045 HMMWV TOW Skid [7073lb]"] = {['name'] = "M1045 HMMWV TOW", ['container'] = false},
	["APC M1043 HMMWV Armament Air [7023lb]"] = {['name'] = "M1043 HMMWV Armament", ['container'] = true},
	["APC M1043 HMMWV Armament Skid [6912lb]"] = {['name'] = "M1043 HMMWV Armament", ['container'] = false},
	["SAM Avenger M1097 Air [7200lb]"] = {['name'] = "M1097 Avenger", ['container'] = true},
	["SAM Avenger M1097 Skid [7090lb]"] = {['name'] = "M1097 Avenger", ['container'] = false},
	["APC Cobra Air [10912lb]"] = {['name'] = "Cobra", ['container'] = true},
	["APC Cobra Skid [10802lb]"] = {['name'] = "Cobra", ['container'] = false},
	["APC M113 Air [21624lb]"] = {['name'] = "M-113", ['container'] = true},
	["APC M113 Skid [21494lb]"] = {['name'] = "M-113", ['container'] = false},
	["Tanker M978 HEMTT [34000lb]"] = {['name'] = "M978 HEMTT Tanker", ['container'] = false},
	["HEMTT TFFT [34400lb]"] = {['name'] = "HEMTT TFFT", ['container'] = false},
	["SPG M1128 Stryker MGS [33036lb]"] = {['name'] = "M1128 Stryker MGS", ['container'] = false},
	["AAA Vulcan M163 Air [21666lb]"] = {['name'] = "Vulcan", ['container'] = true},
	["AAA Vulcan M163 Skid [21577lb]"] = {['name'] = "Vulcan", ['container'] = false},
	["APC M1126 Stryker ICV [29542lb]"] = {['name'] = "M1126 Stryker ICV", ['container'] = false},
	["ATGM M1134 Stryker [30337lb]"] = {['name'] = "M1134 Stryker ATGM", ['container'] = false},
	["APC LAV-25 Air [22520lb]"] = {['name'] = "LAV-25", ['container'] = true},
	["APC LAV-25 Skid [22514lb]"] = {['name'] = "LAV-25", ['container'] = false},
	["M1025 HMMWV Air [6160lb]"] = {['name'] = "Hummer", ['container'] = true},
	["M1025 HMMWV Skid [6050lb]"] = {['name'] = "Hummer", ['container'] = false},
	["IFV M2A2 Bradley [34720lb]"] = {['name'] = "M-2 Bradley", ['container'] = false},
	["IFV MCV-80 [34720lb]"] = {['name'] = "MCV-80", ['container'] = false},
	["IFV BMP-1 [23232lb]"] = {['name'] = "BMP-1", ['container'] = false},
	["IFV BMP-2 [25168lb]"] = {['name'] = "BMP-2", ['container'] = false},
	["IFV BMP-3 [32912lb]"] = {['name'] = "BMP-3", ['container'] = false},
	["ARV BRDM-2 Air [12320lb]"] = {['name'] = "BRDM-2", ['container'] = true},
	["ARV BRDM-2 Skid [12210lb]"] = {['name'] = "BRDM-2", ['container'] = false},
	["APC BTR-80 Air [23936lb]"] = {['name'] = "BTR-80", ['container'] = true},
	["APC BTR-80 Skid [23826lb]"] = {['name'] = "BTR-80", ['container'] = false},
	["APC BTR-82A Air [24998lb]"] = {['name'] = "BTR-82A", ['container'] = true},
	["APC BTR-82A Skid [24888lb]"] = {['name'] = "BTR-82A", ['container'] = false},
	["SAM ROLAND ADS [34720lb]"] = {['name'] = "Roland Radar", ['container'] = false},
	["SAM ROLAND LN [34720b]"] = {['name'] = "Roland ADS", ['container'] = false},
	["SAM SA-13 STRELA [21624lb]"] = {['name'] = "Strela-10M3", ['container'] = false},
	["AAA ZSU-23-4 Shilka [32912lb]"] = {['name'] = "ZSU-23-4 Shilka", ['container'] = false},
	["SAM SA-19 Tunguska 2S6 [34720lb]"] = {['name'] = "2S6 Tunguska", ['container'] = false},
	["Transport UAZ-469 Air [3747lb]"] = {['name'] = "UAZ-469", ['container'] = true},
	["Transport UAZ-469 Skid [3630lb]"] = {['name'] = "UAZ-469", ['container'] = false},
	["AAA GEPARD [34720lb]"] = {['name'] = "Gepard", ['container'] = false},
	["SAM CHAPARRAL Air [21624lb]"] = {['name'] = "M48 Chaparral", ['container'] = true},
	["SAM CHAPARRAL Skid [21516lb]"] = {['name'] = "M48 Chaparral", ['container'] = false},
	["SAM LINEBACKER [34720lb]"] = {['name'] = "M6 Linebacker", ['container'] = false},
	["Transport URAL-375 [14815lb]"] = {['name'] = "Ural-375", ['container'] = false},
	["Transport M818 [16000lb]"] = {['name'] = "M 818", ['container'] = false},
	["IFV MARDER [34720lb]"] = {['name'] = "Marder", ['container'] = false},
	["Transport Tigr Air [15900lb]"] = {['name'] = "Tigr_233036", ['container'] = true},
	["Transport Tigr Skid [15730lb]"] = {['name'] = "Tigr_233036", ['container'] = false},
	["IFV TPZ FUCH [33440lb]"] = {['name'] = "TPZ", ['container'] = false},
	["IFV BMD-1 Air [18040lb]"] = {['name'] = "BMD-1", ['container'] = true},
	["IFV BMD-1 Skid [17930lb]"] = {['name'] = "BMD-1", ['container'] = false},
	["IFV BTR-D Air [18040lb]"] = {['name'] = "BTR_D", ['container'] = true},
	["IFV BTR-D Skid [17930lb]"] = {['name'] = "BTR_D", ['container'] = false},
	["EWR SBORKA Air [21624lb]"] = {['name'] = "Dog Ear radar", ['container'] = true},
	["EWR SBORKA Skid [21624lb]"] = {['name'] = "Dog Ear radar", ['container'] = false},
	["ART 2S9 NONA Air [19140lb]"] = {['name'] = "SAU 2-C9", ['container'] = true},
	["ART 2S9 NONA Skid [19030lb]"] = {['name'] = "SAU 2-C9", ['container'] = false},
	["ART GVOZDIKA [34720lb]"] = {['name'] = "SAU Gvozdika", ['container'] = false},
	["APC MTLB Air [26400lb]"] = {['name'] = "MTLB", ['container'] = true},
	["APC MTLB Skid [26290lb]"] = {['name'] = "MTLB", ['container'] = false},
	--["Generic Crate [20000lb]"] = {['name'] =  "Hercules_Container_Parachute", ['container'] = true}
}
function Hercules_Cargo.Soldier_SpawnGroup(Cargo_Drop_Position, Cargo_Type_name, CargoHeading, Cargo_Country, GroupSpacing)
	SoldierUnitID = SoldierUnitID + 30
	SoldierGroupID = SoldierGroupID + 1
	local Herc_Soldier_Spawn = 
	{
		["visible"] = false,
		["tasks"] = 
		{
		}, -- end of ["tasks"]
		["uncontrollable"] = false,
		["task"] = "Ground Nothing",
		["taskSelected"] = true,
		["groupId"] = SoldierGroupID,
		["hidden"] = false,
		["units"] = 
		{
			[1] = 
			{
				["type"] = Cargo_Type_name,
				["transportable"] = 
				{
					["randomTransportable"] = true,
				}, -- end of ["transportable"]
				["unitId"] = SoldierUnitID + 1,
				["skill"] = "Excellent",
				["y"] = Cargo_Drop_Position.z + 0.5 + GroupSpacing,
				["x"] = Cargo_Drop_Position.x + 0.5 + GroupSpacing,
				["name"] = "Soldier Unit "..SoldierUnitID,
				["heading"] = CargoHeading,
				["playerCanDrive"] = false,
			}, -- end of [1]
			[2] = 
			{
				["type"] = Cargo_Type_name,
				["transportable"] = 
				{
					["randomTransportable"] = true,
				}, -- end of ["transportable"]
				["unitId"] = SoldierUnitID + 1,
				["skill"] = "Excellent",
				["y"] = Cargo_Drop_Position.z + 1.0 + GroupSpacing,
				["x"] = Cargo_Drop_Position.x + 1.0 + GroupSpacing,
				["name"] = "Soldier Unit "..SoldierUnitID,
				["heading"] = CargoHeading,
				["playerCanDrive"] = false,
			}, -- end of [2]
			[3] = 
			{
				["type"] = Cargo_Type_name,
				["transportable"] = 
				{
					["randomTransportable"] = true,
				}, -- end of ["transportable"]
				["unitId"] = SoldierUnitID + 1,
				["skill"] = "Excellent",
				["y"] = Cargo_Drop_Position.z + 1.5 + GroupSpacing,
				["x"] = Cargo_Drop_Position.x + 1.0 + GroupSpacing,
				["name"] = "Soldier Unit "..SoldierUnitID,
				["heading"] = CargoHeading,
				["playerCanDrive"] = false,
			}, -- end of [3]
			[4] = 
			{
				["type"] = Cargo_Type_name,
				["transportable"] = 
				{
					["randomTransportable"] = true,
				}, -- end of ["transportable"]
				["unitId"] = SoldierUnitID + 1,
				["skill"] = "Excellent",
				["y"] = Cargo_Drop_Position.z + 2.0 + GroupSpacing,
				["x"] = Cargo_Drop_Position.x + 2.0 + GroupSpacing,
				["name"] = "Soldier Unit "..SoldierUnitID,
				["heading"] = CargoHeading,
				["playerCanDrive"] = false,
			}, -- end of [4]
			[5] = 
			{
				["type"] = Cargo_Type_name,
				["transportable"] = 
				{
					["randomTransportable"] = true,
				}, -- end of ["transportable"]
				["unitId"] = SoldierUnitID + 1,
				["skill"] = "Excellent",
				["y"] = Cargo_Drop_Position.z + 2.5 + GroupSpacing,
				["x"] = Cargo_Drop_Position.x + 2.5 + GroupSpacing,
				["name"] = "Soldier Unit "..SoldierUnitID,
				["heading"] = CargoHeading,
				["playerCanDrive"] = false,
			}, -- end of [5]
			[6] = 
			{
				["type"] = Cargo_Type_name,
				["transportable"] = 
				{
					["randomTransportable"] = true,
				}, -- end of ["transportable"]
				["unitId"] = SoldierUnitID + 1,
				["skill"] = "Excellent",
				["y"] = Cargo_Drop_Position.z + 3.0 + GroupSpacing,
				["x"] = Cargo_Drop_Position.x + 3.0 + GroupSpacing,
				["name"] = "Soldier Unit "..SoldierUnitID,
				["heading"] = CargoHeading,
				["playerCanDrive"] = false,
			}, -- end of [6]
			[7] = 
			{
				["type"] = "Soldier M249",
				["transportable"] = 
				{
					["randomTransportable"] = true,
				}, -- end of ["transportable"]
				["unitId"] = SoldierUnitID + 1,
				["skill"] = "Excellent",
				["y"] = Cargo_Drop_Position.z + 3.5 + GroupSpacing,
				["x"] = Cargo_Drop_Position.x + 3.5 + GroupSpacing,
				["name"] = "Soldier Unit "..SoldierUnitID,
				["heading"] = CargoHeading,
				["playerCanDrive"] = false,
			}, -- end of [7]
			[8] = 
			{
				["type"] = "Soldier M249",
				["transportable"] = 
				{
					["randomTransportable"] = true,
				}, -- end of ["transportable"]
				["unitId"] = SoldierUnitID + 1,
				["skill"] = "Excellent",
				["y"] = Cargo_Drop_Position.z + 4.0 + GroupSpacing,
				["x"] = Cargo_Drop_Position.x + 4.0 + GroupSpacing,
				["name"] = "Soldier Unit "..SoldierUnitID,
				["heading"] = CargoHeading,
				["playerCanDrive"] = false,
			}, -- end of [8]
			[9] = 
			{
				["type"] = Cargo_Type_name,
				["transportable"] = 
				{
					["randomTransportable"] = true,
				}, -- end of ["transportable"]
				["unitId"] = SoldierUnitID + 1,
				["skill"] = "Excellent",
				["y"] = Cargo_Drop_Position.z + 4.5 + GroupSpacing,
				["x"] = Cargo_Drop_Position.x + 4.5 + GroupSpacing,
				["name"] = "Soldier Unit "..SoldierUnitID,
				["heading"] = CargoHeading,
				["playerCanDrive"] = false,
			}, -- end of [9]
			[10] = 
			{
				["type"] = "Paratrooper RPG-16",
				["transportable"] = 
				{
					["randomTransportable"] = true,
				}, -- end of ["transportable"]
				["unitId"] = SoldierUnitID + 1,
				["skill"] = "Excellent",
				["y"] = Cargo_Drop_Position.z + 5.0 + GroupSpacing,
				["x"] = Cargo_Drop_Position.x + 5.0 + GroupSpacing,
				["name"] = "Soldier Unit "..SoldierUnitID,
				["heading"] = CargoHeading,
				["playerCanDrive"] = false,
			}, -- end of [10]
		}, -- end of ["units"]
		["y"] = Cargo_Drop_Position.z,
		["x"] = Cargo_Drop_Position.x,
		["name"] = "Soldier_Group_"..SoldierGroupID,
		["start_time"] = 0,
	}
	coalition.addGroup(Cargo_Country, Group.Category.GROUND, Herc_Soldier_Spawn)
end

local CargoUnitID = 10000
local CargoGroupID = 10000
local CargoStaticGroupID = 11000

function Hercules_Cargo.Cargo_SpawnGroup(Cargo_Drop_Position, Cargo_Type_name, CargoHeading, Cargo_Country)
	CargoUnitID = CargoUnitID + 1
	CargoGroupID = CargoGroupID + 1
	local Herc_Cargo_Spawn = 
	{
		["visible"] = false,
		["tasks"] = 
		{
		}, -- end of ["tasks"]
		["uncontrollable"] = false,
		["task"] = "Ground Nothing",
		["groupId"] = CargoGroupID,
		["hidden"] = false,
		["units"] = 
		{
			[1] = 
			{
				["type"] = Cargo_Type_name,
				["transportable"] = 
				{
					["randomTransportable"] = false,
				}, -- end of ["transportable"]
				["unitId"] = CargoUnitID,
				["skill"] = "Excellent",
				["y"] = Cargo_Drop_Position.z,
				["x"] = Cargo_Drop_Position.x,
				["name"] = "Cargo Unit "..CargoUnitID,
				["heading"] = CargoHeading,
				["playerCanDrive"] = true,
			}, -- end of [1]
		}, -- end of ["units"]
		["y"] = Cargo_Drop_Position.z,
		["x"] = Cargo_Drop_Position.x,
		["name"] = "Cargo Group "..CargoUnitID,
		["start_time"] = 0,
	}
	coalition.addGroup(Cargo_Country, Group.Category.GROUND, Herc_Cargo_Spawn)
end

function Hercules_Cargo.Cargo_SpawnStatic(Cargo_Drop_Position, Cargo_Type_name, CargoHeading, dead, Cargo_Country)
	CargoStaticGroupID = CargoStaticGroupID + 1
	local Herc_CargoObject_Spawn = 
	{
		["type"] = Cargo_Type_name,
		["y"] = Cargo_Drop_Position.z,
		["x"] = Cargo_Drop_Position.x,
		["name"] = "Cargo Static Group "..CargoStaticGroupID,
		["heading"] = CargoHeading,
		["dead"] = dead,
	}
	coalition.addStaticObject(Cargo_Country, Herc_CargoObject_Spawn)
end

function Hercules_Cargo.Cargo_SpawnObjects(Cargo_Drop_Direction, Cargo_Content_position, Cargo_Type_name, Cargo_over_water, Container_Enclosed, ParatrooperGroupSpawn, offload_cargo, all_cargo_survive_to_the_ground, all_cargo_gets_destroyed, destroy_cargo_dropped_without_parachute, Cargo_Country)
	if offload_cargo == true then
		------------------------------------------------------------------------------
		if CargoHeading >= 3.14 then
			CargoHeading = 0
			Cargo_Drop_Position = {["x"] = Cargo_Content_position.x - (30.0 * math.cos(Cargo_Drop_Direction - 1.0)),
								   ["z"] = Cargo_Content_position.z - (30.0 * math.sin(Cargo_Drop_Direction - 1.0))}
		else
			if CargoHeading >= 1.57 then
				CargoHeading = 3.14
				Cargo_Drop_Position = {["x"] = Cargo_Content_position.x - (20.0 * math.cos(Cargo_Drop_Direction + 0.5)),
									   ["z"] = Cargo_Content_position.z - (20.0 * math.sin(Cargo_Drop_Direction + 0.5))}
			else
				if CargoHeading >= 0 then
					CargoHeading = 1.57
					Cargo_Drop_Position = {["x"] = Cargo_Content_position.x - (10.0 * math.cos(Cargo_Drop_Direction + 1.5)),
										   ["z"] = Cargo_Content_position.z - (10.0 * math.sin(Cargo_Drop_Direction + 1.5))}
				end
			end
		end
		------------------------------------------------------------------------------
		if ParatrooperGroupSpawn == true then
			Hercules_Cargo.Soldier_SpawnGroup(Cargo_Drop_Position, Cargo_Type_name, CargoHeading, Cargo_Country, 0)
			Hercules_Cargo.Soldier_SpawnGroup(Cargo_Drop_Position, Cargo_Type_name, CargoHeading, Cargo_Country, 5)
			Hercules_Cargo.Soldier_SpawnGroup(Cargo_Drop_Position, Cargo_Type_name, CargoHeading, Cargo_Country, 10)
		else
			Hercules_Cargo.Cargo_SpawnGroup(Cargo_Drop_Position, Cargo_Type_name, CargoHeading, Cargo_Country, 0)
		end
	else
		------------------------------------------------------------------------------
		CargoHeading = 0
		Cargo_Drop_Position = {["x"] = Cargo_Content_position.x - (20.0 * math.cos(Cargo_Drop_Direction)),
							   ["z"] = Cargo_Content_position.z - (20.0 * math.cos(Cargo_Drop_Direction))}
		------------------------------------------------------------------------------
		if all_cargo_gets_destroyed == true or Cargo_over_water == true then
			if Container_Enclosed == true then
				Hercules_Cargo.Cargo_SpawnStatic(Cargo_Drop_Position, Cargo_Type_name, CargoHeading, true, Cargo_Country)
				if ParatrooperGroupSpawn == false then
					Hercules_Cargo.Cargo_SpawnStatic(Cargo_Drop_Position, "Hercules_Container_Parachute_Static", CargoHeading, true, Cargo_Country)
				end
			else
				Hercules_Cargo.Cargo_SpawnStatic(Cargo_Drop_Position, Cargo_Type_name, CargoHeading, true, Cargo_Country)
			end
		else
			------------------------------------------------------------------------------
			if all_cargo_survive_to_the_ground == true then
				if ParatrooperGroupSpawn == true then
					Hercules_Cargo.Cargo_SpawnStatic(Cargo_Drop_Position, Cargo_Type_name, CargoHeading, true, Cargo_Country)
				else
					Hercules_Cargo.Cargo_SpawnGroup(Cargo_Drop_Position, Cargo_Type_name, CargoHeading, Cargo_Country)
				end
				if Container_Enclosed == true then
					if ParatrooperGroupSpawn == false then
						Hercules_Cargo.Cargo_SpawnStatic({["z"] = Cargo_Drop_Position.z + 10.0,["x"] = Cargo_Drop_Position.x + 10.0}, "Hercules_Container_Parachute_Static", CargoHeading, false, Cargo_Country)
					end
				end
			end
			------------------------------------------------------------------------------
			if destroy_cargo_dropped_without_parachute == true then
				if Container_Enclosed == true then
					if ParatrooperGroupSpawn == true then
						Hercules_Cargo.Soldier_SpawnGroup(Cargo_Drop_Position, Cargo_Type_name, CargoHeading, Cargo_Country, 0)
					else
						Hercules_Cargo.Cargo_SpawnGroup(Cargo_Drop_Position, Cargo_Type_name, CargoHeading, Cargo_Country)
						Hercules_Cargo.Cargo_SpawnStatic({["z"] = Cargo_Drop_Position.z + 10.0,["x"] = Cargo_Drop_Position.x + 10.0}, "Hercules_Container_Parachute_Static", CargoHeading, false, Cargo_Country)
					end
				else
					Hercules_Cargo.Cargo_SpawnStatic(Cargo_Drop_Position, Cargo_Type_name, CargoHeading, true, Cargo_Country)
				end
			end
			------------------------------------------------------------------------------
		end
	end
end

function Hercules_Cargo.Calculate_Object_Height_AGL(object)
	return object:getPosition().p.y - land.getHeight({x = object:getPosition().p.x, y = object:getPosition().p.z})
end

function Hercules_Cargo.Check_SurfaceType(object)
   -- LAND,--1 SHALLOW_WATER,--2 WATER,--3 ROAD,--4 RUNWAY--5
	return land.getSurfaceType({x = object:getPosition().p.x, y = object:getPosition().p.z})
end

function Hercules_Cargo.Cargo_Track(Arg, time)
	local status, result = pcall(
		function()
		local next = next
		if next(Arg[1].Cargo_Contents) ~= nil then
			if Hercules_Cargo.Calculate_Object_Height_AGL(Arg[1].Cargo_Contents) < 5.0 then--pallet less than 5m above ground before spawning
				if Hercules_Cargo.Check_SurfaceType(Arg[1].Cargo_Contents) == 2 or Hercules_Cargo.Check_SurfaceType(Arg[1].Cargo_Contents) == 3 then
					Arg[1].Cargo_over_water = true--pallets gets destroyed in water
				end
				Arg[1].Cargo_Contents:destroy()--remove pallet+parachute before hitting ground and replace with Cargo_SpawnContents
				Hercules_Cargo.Cargo_SpawnObjects(Arg[1].Cargo_Drop_Direction, Object.getPoint(Arg[1].Cargo_Contents), Arg[1].Cargo_Type_name, Arg[1].Cargo_over_water, Arg[1].Container_Enclosed, Arg[1].ParatrooperGroupSpawn, Arg[1].offload_cargo, Arg[1].all_cargo_survive_to_the_ground, Arg[1].all_cargo_gets_destroyed, Arg[1].destroy_cargo_dropped_without_parachute, Arg[1].Cargo_Country)
				timer.removeFunction(Arg[1].scheduleFunctionID)
				Arg[1] = {}
			end
			return time + 0.1
		end
	end) -- pcall
	if not status then
		-- env.error(string.format("Cargo_Spawn: %s", result))
	else
		return result
	end
end

function Hercules_Cargo.Calculate_Cargo_Drop_initiator_NorthCorrection(point)	--correction needed for true north
	if not point.z then --Vec2; convert to Vec3
		point.z = point.y
		point.y = 0
	end
	local lat, lon = coord.LOtoLL(point)
	local north_posit = coord.LLtoLO(lat + 1, lon)
	return math.atan2(north_posit.z - point.z, north_posit.x - point.x)
end

function Hercules_Cargo.Calculate_Cargo_Drop_initiator_Heading(Cargo_Drop_initiator)
	local Heading = math.atan2(Cargo_Drop_initiator:getPosition().x.z, Cargo_Drop_initiator:getPosition().x.x)
	Heading = Heading + Hercules_Cargo.Calculate_Cargo_Drop_initiator_NorthCorrection(Cargo_Drop_initiator:getPosition().p)
	if Heading < 0 then
		Heading = Heading + (2 * math.pi)-- put heading in range of 0 to 2*pi
	end
	return Heading + 0.06 -- rad
end

function Hercules_Cargo.Cargo_Initialize(initiator, Cargo_Contents, Cargo_Type_name, Container_Enclosed)
	local status, result = pcall(
		function()
		Cargo_Drop_initiator = Unit.getByName(initiator:getName())
		local next = next
		if next(Cargo_Drop_initiator) ~= nil then
			if ParatrooperGroupSpawnInit == true then
				if (ParatrooperCount == 1 or ParatrooperCount == 2 or ParatrooperCount == 3) then
					Herc_j = Herc_j + 1
					Herc_Cargo[Herc_j] = {}
					Herc_Cargo[Herc_j].Cargo_Drop_Direction = Hercules_Cargo.Calculate_Cargo_Drop_initiator_Heading(Cargo_Drop_initiator)
					Herc_Cargo[Herc_j].Cargo_Contents = Cargo_Contents
					Herc_Cargo[Herc_j].Cargo_Type_name = Cargo_Type_name
					Herc_Cargo[Herc_j].Container_Enclosed = Container_Enclosed
					Herc_Cargo[Herc_j].ParatrooperGroupSpawn = ParatrooperGroupSpawnInit
					Herc_Cargo[Herc_j].Cargo_Country = initiator:getCountry()
				------------------------------------------------------------------------------
					if Hercules_Cargo.Calculate_Object_Height_AGL(Cargo_Drop_initiator) < 5.0 then--aircraft on ground
						Herc_Cargo[Herc_j].offload_cargo = true
						ParatrooperCount = 0
						ParatrooperGroupSpawnInit = false
					else
				------------------------------------------------------------------------------
						if Hercules_Cargo.Calculate_Object_Height_AGL(Cargo_Drop_initiator) < 10.0 then--aircraft less than 10m above ground
							Herc_Cargo[Herc_j].all_cargo_survive_to_the_ground = true
						else
				------------------------------------------------------------------------------
							if Hercules_Cargo.Calculate_Object_Height_AGL(Cargo_Drop_initiator) < 100.0 then--aircraft more than 10m but less than 100m above ground
								Herc_Cargo[Herc_j].all_cargo_gets_destroyed = true
							else
				------------------------------------------------------------------------------
								Herc_Cargo[Herc_j].destroy_cargo_dropped_without_parachute = true--aircraft more than 100m above ground
							end
						end
					end
				------------------------------------------------------------------------------
					Herc_Cargo[Herc_j].scheduleFunctionID = timer.scheduleFunction(Hercules_Cargo.Cargo_Track, {Herc_Cargo[Herc_j]}, timer.getTime() + 0.1)
					ParatrooperCount = ParatrooperCount + 1.0
				else
					if (ParatrooperCount == 30) then
						ParatrooperGroupSpawnInit = false
						ParatrooperCount = 1
					else
						ParatrooperCount = ParatrooperCount + 1.0
					end
				end
			else
				Herc_j = Herc_j + 1
				Herc_Cargo[Herc_j] = {}
				Herc_Cargo[Herc_j].Cargo_Drop_Direction = Hercules_Cargo.Calculate_Cargo_Drop_initiator_Heading(Cargo_Drop_initiator)
				Herc_Cargo[Herc_j].Cargo_Contents = Cargo_Contents
				Herc_Cargo[Herc_j].Cargo_Type_name = Cargo_Type_name
				Herc_Cargo[Herc_j].Container_Enclosed = Container_Enclosed
				Herc_Cargo[Herc_j].ParatrooperGroupSpawn = ParatrooperGroupSpawnInit
				Herc_Cargo[Herc_j].Cargo_Country = initiator:getCountry()
			------------------------------------------------------------------------------
				if Hercules_Cargo.Calculate_Object_Height_AGL(Cargo_Drop_initiator) < 5.0 then--aircraft on ground
					Herc_Cargo[Herc_j].offload_cargo = true
				else
			------------------------------------------------------------------------------
					if Hercules_Cargo.Calculate_Object_Height_AGL(Cargo_Drop_initiator) < 10.0 then--aircraft less than 10m above ground
						Herc_Cargo[Herc_j].all_cargo_survive_to_the_ground = true
					else
			------------------------------------------------------------------------------
						if Hercules_Cargo.Calculate_Object_Height_AGL(Cargo_Drop_initiator) < 100.0 then--aircraft more than 10m but less than 100m above ground
							Herc_Cargo[Herc_j].all_cargo_gets_destroyed = true
						else
			------------------------------------------------------------------------------
							Herc_Cargo[Herc_j].destroy_cargo_dropped_without_parachute = true--aircraft more than 100m above ground
						end
					end
				end
			------------------------------------------------------------------------------
				Herc_Cargo[Herc_j].scheduleFunctionID = timer.scheduleFunction(Hercules_Cargo.Cargo_Track, {Herc_Cargo[Herc_j]}, timer.getTime() + 0.1)
			end
		end
	end) -- pcall
	if not status then
		-- env.error(string.format("Cargo_Initialize: %s", result))
	else
		return result
	end
end

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	-- EventHandlers
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
function Hercules_Cargo.Hercules_Cargo_Drop_Events:onEvent(Cargo_Drop_Event)
	if Cargo_Drop_Event.id == world.event.S_EVENT_SHOT then
		GT_DisplayName = Weapon.getDesc(Cargo_Drop_Event.weapon).typeName:sub(15, -1)--Remove "weapons.bombs." from string
		 -- trigger.action.outTextForCoalition(coalition.side.BLUE, string.format("Cargo_Drop_Event: %s", Weapon.getDesc(Cargo_Drop_Event.weapon).typeName), 10)
		 -- trigger.action.outTextForCoalition(coalition.side.RED, string.format("Cargo_Drop_Event: %s", Weapon.getDesc(Cargo_Drop_Event.weapon).typeName), 10)
			 ---------------------------------------------------------------------------------------------------------------------------------
			if (GT_DisplayName == "Squad 30 x Soldier [7950lb]") then
				GT_Name = "Soldier M4 GRG"
				SoldierGroup = true
				ParatrooperGroupSpawnInit = true
				Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, SoldierGroup)
			end
			 ---------------------------------------------------------------------------------------------------------------------------------
			if Hercules_Cargo.types[GT_DisplayName] then
				local GT_Name = Hercules_Cargo.types[GT_DisplayName]['name']
				local Cargo_Container_Enclosed = Hercules_Cargo.types[GT_DisplayName]['container']
				Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
			end
end
end
world.addEventHandler(Hercules_Cargo.Hercules_Cargo_Drop_Events)

-- trigger.action.outTextForCoalition(coalition.side.BLUE, string.format("Cargo_Drop_Event.weapon: %s", Weapon.getDesc(Cargo_Drop_Event.weapon).typeName), 10)
-- trigger.action.outTextForCoalition(coalition.side.BLUE, tostring('Calculate_Object_Height_AGL: ' .. aaaaa), 10)
-- trigger.action.outTextForCoalition(coalition.side.BLUE, string.format("Speed: %.2f", Calculate_Object_Speed(Cargo_Drop_initiator)), 10)
-- trigger.action.outTextForCoalition(coalition.side.BLUE, string.format("Russian Interceptor Patrol scrambled from Nalchik"), 10)

-- function basicSerialize(var)
	-- if var == nil then
		-- return "\"\""
	-- else
		-- if ((type(var) == 'number') or
				-- (type(var) == 'boolean') or
				-- (type(var) == 'function') or
				-- (type(var) == 'table') or
				-- (type(var) == 'userdata') ) then
			-- return tostring(var)
		-- else
			-- if type(var) == 'string' then
				-- var = string.format('%q', var)
				-- return var
			-- end
		-- end
	-- end
-- end
	
-- function tableShow(tbl, loc, indent, tableshow_tbls) --based on serialize_slmod, this is a _G serialization
	-- tableshow_tbls = tableshow_tbls or {} --create table of tables
	-- loc = loc or ""
	-- indent = indent or ""
	-- if type(tbl) == 'table' then --function only works for tables!
		-- tableshow_tbls[tbl] = loc
		-- local tbl_str = {}
		-- tbl_str[#tbl_str + 1] = indent .. '{\n'
		-- for ind,val in pairs(tbl) do -- serialize its fields
			-- if type(ind) == "number" then
				-- tbl_str[#tbl_str + 1] = indent
				-- tbl_str[#tbl_str + 1] = loc .. '['
				-- tbl_str[#tbl_str + 1] = tostring(ind)
				-- tbl_str[#tbl_str + 1] = '] = '
			-- else
				-- tbl_str[#tbl_str + 1] = indent
				-- tbl_str[#tbl_str + 1] = loc .. '['
				-- tbl_str[#tbl_str + 1] = basicSerialize(ind)
				-- tbl_str[#tbl_str + 1] = '] = '
			-- end
			-- if ((type(val) == 'number') or (type(val) == 'boolean')) then
				-- tbl_str[#tbl_str + 1] = tostring(val)
				-- tbl_str[#tbl_str + 1] = ',\n'
			-- elseif type(val) == 'string' then
				-- tbl_str[#tbl_str + 1] = basicSerialize(val)
				-- tbl_str[#tbl_str + 1] = ',\n'
			-- elseif type(val) == 'nil' then -- won't ever happen, right?
				-- tbl_str[#tbl_str + 1] = 'nil,\n'
			-- elseif type(val) == 'table' then
				-- if tableshow_tbls[val] then
					-- tbl_str[#tbl_str + 1] = tostring(val) .. ' already defined: ' .. tableshow_tbls[val] .. ',\n'
				-- else
					-- tableshow_tbls[val] = loc ..	'[' .. basicSerialize(ind) .. ']'
					-- tbl_str[#tbl_str + 1] = tostring(val) .. ' '
					-- tbl_str[#tbl_str + 1] = tableShow(val,	loc .. '[' .. basicSerialize(ind).. ']', indent .. '		', tableshow_tbls)
					-- tbl_str[#tbl_str + 1] = ',\n'
				-- end
			-- elseif type(val) == 'function' then
				-- if debug and debug.getinfo then
					-- local fcnname = tostring(val)
					-- local info = debug.getinfo(val, "S")
					-- if info.what == "C" then
						-- tbl_str[#tbl_str + 1] = string.format('%q', fcnname .. ', C function') .. ',\n'
					-- else
						-- if (string.sub(info.source, 1, 2) == [[./]]) then
							-- tbl_str[#tbl_str + 1] = string.format('%q', fcnname .. ', defined in (' .. info.linedefined .. '-' .. info.lastlinedefined .. ')' .. info.source) ..',\n'
						-- else
							-- tbl_str[#tbl_str + 1] = string.format('%q', fcnname .. ', defined in (' .. info.linedefined .. '-' .. info.lastlinedefined .. ')') ..',\n'
						-- end
					-- end
				-- else
					-- tbl_str[#tbl_str + 1] = 'a function,\n'
				-- end
			-- else
				-- tbl_str[#tbl_str + 1] = 'unable to serialize value type ' .. basicSerialize(type(val)) .. ' at index ' .. tostring(ind)
			-- end
		-- end
		-- tbl_str[#tbl_str + 1] = indent .. '}'
		-- return table.concat(tbl_str)
	-- end
-- end




-- function F10CargoDrop(GroupId, Unitname)
	-- local rootPath = missionCommands.addSubMenuForGroup(GroupId, "Cargo Drop")
	-- missionCommands.addCommandForGroup(GroupId, "Drop direction", rootPath, CruiseMissilesMessage, {GroupId, Unitname})
	-- missionCommands.addCommandForGroup(GroupId, "Drop distance", rootPath, ForwardConvoy, nil)
	-- local measurementsSetPath = missionCommands.addSubMenuForGroup(GroupId,"Set measurement units",rootPath)
	-- missionCommands.addCommandForGroup(GroupId, "Set to Imperial (feet, knts)",measurementsSetPath,setMeasurements,{GroupId, "imperial"})
	-- missionCommands.addCommandForGroup(GroupId, "Set to Metric (meters, km/h)",measurementsSetPath,setMeasurements,{GroupId, "metric"})
-- end

-- function Calculate_Object_Speed(object)
	-- return math.sqrt(object:getVelocity().x^2 + object:getVelocity().y^2 + object:getVelocity().z^2) * 3600 / 1852 -- knts
-- end

-- function vecDotProduct(vec1, vec2)
	-- return vec1.x*vec2.x + vec1.y*vec2.y + vec1.z*vec2.z
-- end

-- function Calculate_Aircraft_ForwardVelocity(Drop_initiator)
	-- return vecDotProduct(Drop_initiator:getPosition().x, Drop_initiator:getVelocity())
-- end



