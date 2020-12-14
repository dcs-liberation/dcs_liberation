
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
		env.error(string.format("Cargo_Spawn: %s", result))
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
		env.error(string.format("Cargo_Initialize: %s", result))
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
				if (GT_DisplayName == "ATGM M1045 HMMWV TOW [7183lb]") then
					GT_Name = "M1045 HMMWV TOW"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "APC M1043 HMMWV Armament [7023lb]") then
					GT_Name = "M1043 HMMWV Armament"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "SAM Avenger M1097 [7200lb]") then
					GT_Name = "M1097 Avenger"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "APC Cobra [10912lb]") then
					GT_Name = "Cobra"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "APC M113 [21624lb]") then
					GT_Name = "M-113"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "Tanker M978 HEMTT [34000lb]") then
					GT_Name = "M978 HEMTT Tanker"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "HEMTT TFFT [34400lb]") then
					GT_Name = "HEMTT TFFT"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "SPG M1128 Stryker MGS [33036lb]") then
					GT_Name = "M1128 Stryker MGS"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "AAA Vulcan M163 [21666lb]") then
					GT_Name = "Vulcan"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "APC M1126 Stryker ICV [29542lb]") then
					GT_Name = "M1126 Stryker ICV"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "ATGM M1134 Stryker [30337lb]") then
					GT_Name = "M1134 Stryker ATGM"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "APC LAV-25 [22514lb]") then
					GT_Name = "LAV-25"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "M1025 HMMWV [6160lb]") then
					GT_Name = "Hummer"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "IFV M2A2 Bradley [34720lb]") then
					GT_Name = "M-2 Bradley"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
					if (GT_DisplayName == "IFV MCV-80 [34720lb]") then
					GT_Name = "MCV-80"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
					if (GT_DisplayName == "IFV BMP-1 [23232lb]") then
					GT_Name = "BMP-1"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "IFV BMP-2 [25168lb]") then
					GT_Name = "BMP-2"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "IFV BMP-3 [32912lb]") then
					GT_Name = "BMP-3"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "ARV BRDM-2 [12320lb]") then
					GT_Name = "BRDM-2"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "APC BTR-80 [23936lb]") then
					GT_Name = "BTR-80"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "SAM ROLAND ADS [34720lb]") then
					GT_Name = "Roland Radar"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "SAM ROLAND LN [34720b]") then
					GT_Name = "Roland ADS"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "SAM SA-13 STRELA [21624lb]") then
					GT_Name = "Strela-10M3"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "AAA ZSU-23-4 Shilka [32912lb]") then
					GT_Name = "ZSU-23-4 Shilka"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "SAM SA-19 Tunguska 2S6 [34720lb]") then
					GT_Name = "2S6 Tunguska"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "Transport UAZ-469 [3747lb]") then
					GT_Name = "UAZ-469"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "Armed speedboat [2000lb]") then
					GT_Name = "speedboat"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "AAA GEPARD [34720lb]") then
					GT_Name = "Gepard"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "SAM CHAPARRAL [21624lb]") then
					GT_Name = "M48 Chaparral"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "SAM LINEBACKER [34720lb]") then
					GT_Name = "M6 Linebacker"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "Transport URAL-375 [14815lb]") then
					GT_Name = "Ural-375"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "Transport M818 [16000lb]") then
					GT_Name = "M 818"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "IFV MARDER [34720lb]") then
					GT_Name = "Marder"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "Transport Tigr [15900lb]") then
					GT_Name = "Tigr_233036"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "IFV TPZ FUCH [33440lb]") then
					GT_Name = "TPZ"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "IFV BMD-1 [18040lb]") then
					GT_Name = "BMD-1"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "IFV BTR-D [18040lb]") then
					GT_Name = "BTR_D"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "EWR SBORKA [21624lb]") then
					GT_Name = "Dog Ear radar"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "ART 2S9 NONA [19140lb]") then
					GT_Name = "SAU 2-C9"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "ART GVOZDIKA [34720lb]") then
					GT_Name = "SAU Gvozdika"
					Cargo_Container_Enclosed = false
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
				if (GT_DisplayName == "APC MTLB [26000lb]") then
					GT_Name = "MTLB"
					Cargo_Container_Enclosed = true
					Hercules_Cargo.Cargo_Initialize(Cargo_Drop_Event.initiator, Cargo_Drop_Event.weapon, GT_Name, Cargo_Container_Enclosed)
				end
				---------------------------------------------------------------------------------------------------------------------------------
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



