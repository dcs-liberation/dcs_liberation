--[[--
MIST Mission Scripting Tools.
## Description:
MIssion Scripting Tools (MIST) is a collection of Lua functions
and databases that is intended to be a supplement to the standard
Lua functions included in the simulator scripting engine.

MIST functions and databases provide ready-made solutions to many common
scripting tasks and challenges, enabling easier scripting and saving
mission scripters time. The table mist.flagFuncs contains a set of
Lua functions (that are similar to Slmod functions) that do not
require detailed Lua knowledge to use.

However, the majority of MIST does require knowledge of the Lua language,
and, if you are going to utilize these components of MIST, it is necessary
that you read the Simulator Scripting Engine guide on the official ED wiki.

## Links:

ED Forum Thread: <http://forums.eagle.ru/showthread.php?t=98616>

##Github:

Development <https://github.com/mrSkortch/MissionScriptingTools>

Official Releases <https://github.com/mrSkortch/MissionScriptingTools/tree/master>

@script MIST
@author Speed
@author Grimes
@author lukrop
]]
mist = {}

-- don't change these
mist.majorVersion = 4
mist.minorVersion = 4
mist.build = 90

-- forward declaration of log shorthand
local log

local mistSettings = {
	errorPopup = false, -- errors printed by mist logger will create popup warning you
	warnPopup = false,
	infoPopup = false,
	logLevel = 'warn',
}

do -- the main scope
	local coroutines = {}

	local tempSpawnedUnits = {} -- birth events added here
	local tempSpawnedGroups = {}
	local tempSpawnGroupsCounter = 0
	
	local mistAddedObjects = {} -- mist.dynAdd unit data added here
	local mistAddedGroups = {} -- mist.dynAdd groupdata added here
	local writeGroups = {}
	local lastUpdateTime = 0

	local updateAliveUnitsCounter = 0
	local updateTenthSecond = 0
	
	local mistGpId = 7000
	local mistUnitId = 7000
	local mistDynAddIndex = {[' air '] = 0, [' hel '] = 0, [' gnd '] = 0, [' bld '] = 0, [' static '] = 0, [' shp '] = 0}

	local scheduledTasks = {}
	local taskId = 0
	local idNum = 0

	mist.nextGroupId = 1
	mist.nextUnitId = 1

	local dbLog
	
	local function initDBs() -- mist.DBs scope
		mist.DBs = {}

		mist.DBs.missionData = {}
		if env.mission then

			mist.DBs.missionData.startTime = env.mission.start_time
			mist.DBs.missionData.theatre = env.mission.theatre
			mist.DBs.missionData.version = env.mission.version
			mist.DBs.missionData.files = {}
			if type(env.mission.resourceCounter) == 'table' then
				for fIndex, fData in pairs (env.mission.resourceCounter) do
					mist.DBs.missionData.files[#mist.DBs.missionData.files + 1] =	mist.utils.deepCopy(fIndex)
				end
			end
			-- if we add more coalition specific data then bullsye should be categorized by coaliton. For now its just the bullseye table
            mist.DBs.missionData.bullseye = {}
		end

		mist.DBs.zonesByName = {}
		mist.DBs.zonesByNum = {}


		if env.mission.triggers and env.mission.triggers.zones then
			for zone_ind, zone_data in pairs(env.mission.triggers.zones) do
				if type(zone_data) == 'table' then
					local zone = mist.utils.deepCopy(zone_data)
					zone.point = {}	-- point is used by SSE
					zone.point.x = zone_data.x
					zone.point.y = 0
					zone.point.z = zone_data.y

					mist.DBs.zonesByName[zone_data.name] = zone
					mist.DBs.zonesByNum[#mist.DBs.zonesByNum + 1] = mist.utils.deepCopy(zone)	--[[deepcopy so that the zone in zones_by_name and the zone in
																								zones_by_num se are different objects.. don't want them linked.]]
				end
			end
		end

		mist.DBs.navPoints = {}
		mist.DBs.units = {}
		--Build mist.db.units and mist.DBs.navPoints
		for coa_name_miz, coa_data in pairs(env.mission.coalition) do
            local coa_name = coa_name_miz
            if string.lower(coa_name_miz) == 'neutrals' then
                coa_name = 'neutral'
            end
			if type(coa_data) == 'table' then
				mist.DBs.units[coa_name] = {}
                
                if coa_data.bullseye then 
                    mist.DBs.missionData.bullseye[coa_name] = {}
                    mist.DBs.missionData.bullseye[coa_name].x = coa_data.bullseye.x
                    mist.DBs.missionData.bullseye[coa_name].y = coa_data.bullseye.y
                end
				-- build nav points DB
				mist.DBs.navPoints[coa_name] = {}
				if coa_data.nav_points then --navpoints
					--mist.debug.writeData (mist.utils.serialize,{'NavPoints',coa_data.nav_points}, 'NavPoints.txt')
					for nav_ind, nav_data in pairs(coa_data.nav_points) do

						if type(nav_data) == 'table' then
							mist.DBs.navPoints[coa_name][nav_ind] = mist.utils.deepCopy(nav_data)

							mist.DBs.navPoints[coa_name][nav_ind].name = nav_data.callsignStr	-- name is a little bit more self-explanatory.
							mist.DBs.navPoints[coa_name][nav_ind].point = {}	-- point is used by SSE, support it.
							mist.DBs.navPoints[coa_name][nav_ind].point.x = nav_data.x
							mist.DBs.navPoints[coa_name][nav_ind].point.y = 0
							mist.DBs.navPoints[coa_name][nav_ind].point.z = nav_data.y
						end
					end
				end
				if coa_data.country then --there is a country table
					for cntry_id, cntry_data in pairs(coa_data.country) do

						local countryName = string.lower(cntry_data.name)
						mist.DBs.units[coa_name][countryName] = {}
						mist.DBs.units[coa_name][countryName].countryId = cntry_data.id

						if type(cntry_data) == 'table' then	--just making sure

							for obj_type_name, obj_type_data in pairs(cntry_data) do

								if obj_type_name == "helicopter" or obj_type_name == "ship" or obj_type_name == "plane" or obj_type_name == "vehicle" or obj_type_name == "static" then --should be an unncessary check

									local category = obj_type_name

									if ((type(obj_type_data) == 'table') and obj_type_data.group and (type(obj_type_data.group) == 'table') and (#obj_type_data.group > 0)) then	--there's a group!

										mist.DBs.units[coa_name][countryName][category] = {}

										for group_num, group_data in pairs(obj_type_data.group) do

											if group_data and group_data.units and type(group_data.units) == 'table' then	--making sure again- this is a valid group

												mist.DBs.units[coa_name][countryName][category][group_num] = {}
												local groupName = group_data.name
												if env.mission.version > 7 then
													groupName = env.getValueDictByKey(groupName)
												end
												mist.DBs.units[coa_name][countryName][category][group_num].groupName = groupName
												mist.DBs.units[coa_name][countryName][category][group_num].groupId = group_data.groupId
												mist.DBs.units[coa_name][countryName][category][group_num].category = category
												mist.DBs.units[coa_name][countryName][category][group_num].coalition = coa_name
												mist.DBs.units[coa_name][countryName][category][group_num].country = countryName
												mist.DBs.units[coa_name][countryName][category][group_num].countryId = cntry_data.id
												mist.DBs.units[coa_name][countryName][category][group_num].startTime = group_data.start_time
												mist.DBs.units[coa_name][countryName][category][group_num].task = group_data.task
												mist.DBs.units[coa_name][countryName][category][group_num].hidden = group_data.hidden

												mist.DBs.units[coa_name][countryName][category][group_num].units = {}

												mist.DBs.units[coa_name][countryName][category][group_num].radioSet = group_data.radioSet
												mist.DBs.units[coa_name][countryName][category][group_num].uncontrolled = group_data.uncontrolled
												mist.DBs.units[coa_name][countryName][category][group_num].frequency = group_data.frequency
												mist.DBs.units[coa_name][countryName][category][group_num].modulation = group_data.modulation

												for unit_num, unit_data in pairs(group_data.units) do
													local units_tbl = mist.DBs.units[coa_name][countryName][category][group_num].units	--pointer to the units table for this group

													units_tbl[unit_num] = {}
													if env.mission.version > 7 then
														units_tbl[unit_num].unitName = env.getValueDictByKey(unit_data.name)
													else
														units_tbl[unit_num].unitName = unit_data.name
													end
													units_tbl[unit_num].type = unit_data.type
													units_tbl[unit_num].skill = unit_data.skill	--will be nil for statics
													units_tbl[unit_num].unitId = unit_data.unitId
													units_tbl[unit_num].category = category
													units_tbl[unit_num].coalition = coa_name
													units_tbl[unit_num].country = countryName
													units_tbl[unit_num].countryId = cntry_data.id
													units_tbl[unit_num].heading = unit_data.heading
													units_tbl[unit_num].playerCanDrive = unit_data.playerCanDrive
													units_tbl[unit_num].alt = unit_data.alt
													units_tbl[unit_num].alt_type = unit_data.alt_type
													units_tbl[unit_num].speed = unit_data.speed
													units_tbl[unit_num].livery_id = unit_data.livery_id
													if unit_data.point then	--ME currently does not work like this, but it might one day
														units_tbl[unit_num].point = unit_data.point
													else
														units_tbl[unit_num].point = {}
														units_tbl[unit_num].point.x = unit_data.x
														units_tbl[unit_num].point.y = unit_data.y
													end
													units_tbl[unit_num].x = unit_data.x
													units_tbl[unit_num].y = unit_data.y

													units_tbl[unit_num].callsign = unit_data.callsign
													units_tbl[unit_num].onboard_num = unit_data.onboard_num
													units_tbl[unit_num].hardpoint_racks = unit_data.hardpoint_racks
													units_tbl[unit_num].psi = unit_data.psi


													units_tbl[unit_num].groupName = groupName
													units_tbl[unit_num].groupId = group_data.groupId

													if unit_data.AddPropAircraft then
														units_tbl[unit_num].AddPropAircraft = unit_data.AddPropAircraft
													end

													if category == 'static' then
														units_tbl[unit_num].categoryStatic = unit_data.category
														units_tbl[unit_num].shape_name = unit_data.shape_name
														if unit_data.mass then
															units_tbl[unit_num].mass = unit_data.mass
														end

														if unit_data.canCargo then
															units_tbl[unit_num].canCargo = unit_data.canCargo
														end
													end

												end --for unit_num, unit_data in pairs(group_data.units) do
											end --if group_data and group_data.units then
										end --for group_num, group_data in pairs(obj_type_data.group) do
									end --if ((type(obj_type_data) == 'table') and obj_type_data.group and (type(obj_type_data.group) == 'table') and (#obj_type_data.group > 0)) then
								end --if obj_type_name == "helicopter" or obj_type_name == "ship" or obj_type_name == "plane" or obj_type_name == "vehicle" or obj_type_name == "static" then
							end --for obj_type_name, obj_type_data in pairs(cntry_data) do
						end --if type(cntry_data) == 'table' then
					end --for cntry_id, cntry_data in pairs(coa_data.country) do
				end --if coa_data.country then --there is a country table
			end --if coa_name == 'red' or coa_name == 'blue' and type(coa_data) == 'table' then
		end --for coa_name, coa_data in pairs(mission.coalition) do

		mist.DBs.unitsByName = {}
		mist.DBs.unitsById = {}
		mist.DBs.unitsByCat = {}

		mist.DBs.unitsByCat.helicopter = {}	-- adding default categories
		mist.DBs.unitsByCat.plane = {}
		mist.DBs.unitsByCat.ship = {}
		mist.DBs.unitsByCat.static = {}
		mist.DBs.unitsByCat.vehicle = {}

		mist.DBs.unitsByNum = {}

		mist.DBs.groupsByName = {}
		mist.DBs.groupsById = {}
		mist.DBs.humansByName = {}
		mist.DBs.humansById = {}

		mist.DBs.dynGroupsAdded = {} -- will be filled by mist.dbUpdate from dynamically spawned groups
		mist.DBs.activeHumans = {}

		mist.DBs.aliveUnits = {}	-- will be filled in by the "updateAliveUnits" coroutine in mist.main.

		mist.DBs.removedAliveUnits = {} -- will be filled in by the "updateAliveUnits" coroutine in mist.main.

		mist.DBs.const = {}

		-- not accessible by SSE, must use static list :-/
		mist.DBs.const.callsigns = {
			['NATO'] = {
				['rules'] = {
					['groupLimit'] = 9,
				},
				['AWACS'] = {
					['Overlord'] = 1,
					['Magic'] = 2,
					['Wizard'] = 3,
					['Focus'] =	 4,
					['Darkstar'] =	 5,
				},
                ['TANKER'] = {
					['Texaco'] = 1,
					['Arco'] = 2,
					['Shell'] = 3,
				},
				['JTAC'] = {
					['Axeman'] = 1,
					['Darknight'] = 2,
					['Warrior']	= 3,
					['Pointer']	= 4,
					['Eyeball'] = 5,
					['Moonbeam'] = 6,
					['Whiplash'] = 7,
					['Finger'] = 8,
					['Pinpoint'] = 9,
					['Ferret'] = 10,
					['Shaba'] = 11,
					['Playboy'] = 12,
					['Hammer'] = 13,
					['Jaguar'] = 14,
					['Deathstar'] =	15,
					['Anvil'] = 16,
					['Firefly']	= 17,
					['Mantis'] = 18,
					['Badger'] = 19,
				},
				['aircraft'] = {
					['Enfield'] = 1,
					['Springfield'] = 2,
					['Uzi']	= 3,
					['Colt'] = 4,
					['Dodge'] =	5,
					['Ford'] = 6,
					['Chevy'] = 7,
					['Pontiac'] = 8,
				},

				['unique'] = {
					['A10'] = {
						['Hawg'] = 9,
						['Boar'] = 10,
						['Pig'] = 11,
						['Tusk'] = 12,
						['rules'] = {
							['canUseAircraft'] = true,
							['appliesTo'] = {
								'A-10C',
								'A-10A',
							},
						},
					},
				},
			},
		}
		mist.DBs.const.shapeNames = {
			["Landmine"] = "landmine",
			["FARP CP Blindage"] = "kp_ug",
			["Subsidiary structure C"] = "saray-c",
			["Barracks 2"] = "kazarma2",
			["Small house 2C"] = "dom2c",
			["Military staff"] = "aviashtab",
			["Tech hangar A"] = "ceh_ang_a",
			["Oil derrick"] = "neftevyshka",
			["Tech combine"] = "kombinat",
			["Garage B"] = "garage_b",
			["Airshow_Crowd"] = "Crowd1",
			["Hangar A"] = "angar_a",
			["Repair workshop"] = "tech",
			["Subsidiary structure D"] = "saray-d",
			["FARP Ammo Dump Coating"] = "SetkaKP",
			["Small house 1C area"] = "dom2c-all",
			["Tank 2"] = "airbase_tbilisi_tank_01",
			["Boiler-house A"] = "kotelnaya_a",
			["Workshop A"] = "tec_a",
			["Small werehouse 1"] = "s1",
			["Garage small B"] = "garagh-small-b",
			["Small werehouse 4"] = "s4",
			["Shop"] = "magazin",
			["Subsidiary structure B"] = "saray-b",
			["FARP Fuel Depot"] = "GSM Rus",
			["Coach cargo"] = "wagon-gruz",
			["Electric power box"] = "tr_budka",
			["Tank 3"] = "airbase_tbilisi_tank_02",
			["Red_Flag"] = "H-flag_R",
			["Container red 3"] = "konteiner_red3",
			["Garage A"] = "garage_a",
			["Hangar B"] = "angar_b",
			["Black_Tyre"] = "H-tyre_B",
			["Cafe"] = "stolovaya",
			["Restaurant 1"] = "restoran1",
			["Subsidiary structure A"] = "saray-a",
			["Container white"] = "konteiner_white",
			["Warehouse"] = "sklad",
			["Tank"] = "bak",
			["Railway crossing B"] = "pereezd_small",
			["Subsidiary structure F"] = "saray-f",
			["Farm A"] = "ferma_a",
			["Small werehouse 3"] = "s3",
			["Water tower A"] = "wodokachka_a",
			["Railway station"] = "r_vok_sd",
			["Coach a tank blue"] = "wagon-cisterna_blue",
			["Supermarket A"] = "uniwersam_a",
			["Coach a platform"] = "wagon-platforma",
			["Garage small A"] = "garagh-small-a",
			["TV tower"] = "tele_bash",
			["Comms tower M"] = "tele_bash_m",
			["Small house 1A"] = "domik1a",
			["Farm B"] = "ferma_b",
			["GeneratorF"] = "GeneratorF",
			["Cargo1"] = "ab-212_cargo",
			["Container red 2"] = "konteiner_red2",
			["Subsidiary structure E"] = "saray-e",
			["Coach a passenger"] = "wagon-pass",
			["Black_Tyre_WF"] = "H-tyre_B_WF",
			["Electric locomotive"] = "elektrowoz",
			["Shelter"] = "ukrytie",
			["Coach a tank yellow"] = "wagon-cisterna_yellow",
			["Railway crossing A"] = "pereezd_big",
			[".Ammunition depot"] = "SkladC",
			["Small werehouse 2"] = "s2",
			["Windsock"] = "H-Windsock_RW",
			["Shelter B"] = "ukrytie_b",
			["Fuel tank"] = "toplivo-bak",
			["Locomotive"] = "teplowoz",
			[".Command Center"] = "ComCenter",
			["Pump station"] = "nasos",
			["Black_Tyre_RF"] = "H-tyre_B_RF",
			["Coach cargo open"] = "wagon-gruz-otkr",
			["Subsidiary structure 3"] = "hozdomik3",
			["FARP Tent"] = "PalatkaB",
			["White_Tyre"] = "H-tyre_W",
			["Subsidiary structure G"] = "saray-g",
			["Container red 1"] = "konteiner_red1",
			["Small house 1B area"] = "domik1b-all",
			["Subsidiary structure 1"] = "hozdomik1",
			["Container brown"] = "konteiner_brown",
			["Small house 1B"] = "domik1b",
			["Subsidiary structure 2"] = "hozdomik2",
			["Chemical tank A"] = "him_bak_a",
			["WC"] = "WC",
			["Small house 1A area"] = "domik1a-all",
			["White_Flag"] = "H-Flag_W",
			["Airshow_Cone"] = "Comp_cone",
		}
		
		
		-- create mist.DBs.oldAliveUnits
		-- do
		-- local intermediate_alive_units = {}	-- between 0 and 0.5 secs old
		-- local function make_old_alive_units() -- called every 0.5 secs, makes the old_alive_units DB which is just a copy of alive_units that is 0.5 to 1 sec old
		-- if intermediate_alive_units then
		-- mist.DBs.oldAliveUnits = mist.utils.deepCopy(intermediate_alive_units)
		-- end
		-- intermediate_alive_units = mist.utils.deepCopy(mist.DBs.aliveUnits)
		-- timer.scheduleFunction(make_old_alive_units, nil, timer.getTime() + 0.5)
		-- end

		-- make_old_alive_units()
		-- end

		--Build DBs
		for coa_name, coa_data in pairs(mist.DBs.units) do
			for cntry_name, cntry_data in pairs(coa_data) do
				for category_name, category_data in pairs(cntry_data) do
					if type(category_data) == 'table' then
						for group_ind, group_data in pairs(category_data) do
							if type(group_data) == 'table' and group_data.units and type(group_data.units) == 'table' and #group_data.units > 0 then	-- OCD paradigm programming
								mist.DBs.groupsByName[group_data.groupName] = mist.utils.deepCopy(group_data)
								mist.DBs.groupsById[group_data.groupId] = mist.utils.deepCopy(group_data)
								for unit_ind, unit_data in pairs(group_data.units) do
									mist.DBs.unitsByName[unit_data.unitName] = mist.utils.deepCopy(unit_data)
									mist.DBs.unitsById[unit_data.unitId] = mist.utils.deepCopy(unit_data)

									mist.DBs.unitsByCat[unit_data.category] = mist.DBs.unitsByCat[unit_data.category] or {} -- future-proofing against new categories...
									table.insert(mist.DBs.unitsByCat[unit_data.category], mist.utils.deepCopy(unit_data))
									--dbLog:info('inserting $1', unit_data.unitName)
									table.insert(mist.DBs.unitsByNum, mist.utils.deepCopy(unit_data))

									if unit_data.skill and (unit_data.skill == "Client" or unit_data.skill == "Player") then
										mist.DBs.humansByName[unit_data.unitName] = mist.utils.deepCopy(unit_data)
										mist.DBs.humansById[unit_data.unitId] = mist.utils.deepCopy(unit_data)
										--if Unit.getByName(unit_data.unitName) then
										--	mist.DBs.activeHumans[unit_data.unitName] = mist.utils.deepCopy(unit_data)
										--	mist.DBs.activeHumans[unit_data.unitName].playerName = Unit.getByName(unit_data.unitName):getPlayerName()
										--end
									end
								end
							end
						end
					end
				end
			end
		end

		--DynDBs
		mist.DBs.MEunits = mist.utils.deepCopy(mist.DBs.units)
		mist.DBs.MEunitsByName = mist.utils.deepCopy(mist.DBs.unitsByName)
		mist.DBs.MEunitsById = mist.utils.deepCopy(mist.DBs.unitsById)
		mist.DBs.MEunitsByCat = mist.utils.deepCopy(mist.DBs.unitsByCat)
		mist.DBs.MEunitsByNum = mist.utils.deepCopy(mist.DBs.unitsByNum)
		mist.DBs.MEgroupsByName = mist.utils.deepCopy(mist.DBs.groupsByName)
		mist.DBs.MEgroupsById = mist.utils.deepCopy(mist.DBs.groupsById)

		mist.DBs.deadObjects = {}

		do
			local mt = {}

			function mt.__newindex(t, key, val)
				local original_key = key --only for duplicate runtime IDs.
				local key_ind = 1
				while mist.DBs.deadObjects[key] do
					--dbLog:warn('duplicate runtime id of previously dead object key: $1', key)
					key = tostring(original_key) .. ' #' .. tostring(key_ind)
					key_ind = key_ind + 1
				end

				if mist.DBs.aliveUnits and mist.DBs.aliveUnits[val.object.id_] then
					----dbLog:info('object found in alive_units')
					val.objectData = mist.utils.deepCopy(mist.DBs.aliveUnits[val.object.id_])
					local pos = Object.getPosition(val.object)
					if pos then
						val.objectPos = pos.p
					end
					val.objectType = mist.DBs.aliveUnits[val.object.id_].category

				elseif mist.DBs.removedAliveUnits and mist.DBs.removedAliveUnits[val.object.id_] then	-- it didn't exist in alive_units, check old_alive_units
					----dbLog:info('object found in old_alive_units')
					val.objectData = mist.utils.deepCopy(mist.DBs.removedAliveUnits[val.object.id_])
					local pos = Object.getPosition(val.object)
					if pos then
						val.objectPos = pos.p
					end
					val.objectType = mist.DBs.removedAliveUnits[val.object.id_].category

				else	--attempt to determine if static object...
					----dbLog:info('object not found in alive units or old alive units')
					local pos = Object.getPosition(val.object)
					if pos then
						local static_found = false
						for ind, static in pairs(mist.DBs.unitsByCat.static) do
							if ((pos.p.x - static.point.x)^2 + (pos.p.z - static.point.y)^2)^0.5 < 0.1 then --really, it should be zero...
								--dbLog:info('correlated dead static object to position')
								val.objectData = static
								val.objectPos = pos.p
								val.objectType = 'static'
								static_found = true
								break
							end
						end
						if not static_found then
							val.objectPos = pos.p
							val.objectType = 'building'
						end
					else
						val.objectType = 'unknown'
					end
				end
				rawset(t, key, val)
			end

			setmetatable(mist.DBs.deadObjects, mt)
		end

		do -- mist unitID funcs
			for id, idData in pairs(mist.DBs.unitsById) do
				if idData.unitId > mist.nextUnitId then
					mist.nextUnitId = mist.utils.deepCopy(idData.unitId)
				end
				if idData.groupId > mist.nextGroupId then
					mist.nextGroupId = mist.utils.deepCopy(idData.groupId)
				end
			end
		end


	end

	local function updateAliveUnits()	-- coroutine function
		local lalive_units = mist.DBs.aliveUnits -- local references for faster execution
		local lunits = mist.DBs.unitsByNum
		local ldeepcopy = mist.utils.deepCopy
		local lUnit = Unit
		local lremovedAliveUnits = mist.DBs.removedAliveUnits
		local updatedUnits = {}

		if #lunits > 0 then
			local units_per_run = math.ceil(#lunits/20)
			if units_per_run < 5 then
				units_per_run = 5
			end

			for i = 1, #lunits do
				if lunits[i].category ~= 'static' then -- can't get statics with Unit.getByName :(
					local unit = lUnit.getByName(lunits[i].unitName)
					if unit then
						----dbLog:info("unit named $1 alive!", lunits[i].unitName) -- spammy
						local pos = unit:getPosition()
						local newtbl = ldeepcopy(lunits[i])
						if pos then
							newtbl.pos = pos.p
						end
						newtbl.unit = unit
						--newtbl.rt_id = unit.id_
						lalive_units[unit.id_] = newtbl
						updatedUnits[unit.id_] = true
					end
				end
				if i%units_per_run == 0 then
					coroutine.yield()
				end
			end
			-- All units updated, remove any "alive" units that were not updated- they are dead!
			for unit_id, unit in pairs(lalive_units) do
				if not updatedUnits[unit_id] then
					lremovedAliveUnits[unit_id] = unit
					lalive_units[unit_id] = nil
				end
			end
		end
	end

	local function dbUpdate(event, objType)
		--dbLog:info('dbUpdate')
		local newTable = {}
		newTable.startTime =	0
		if type(event) == 'string' then -- if name of an object.
			local newObject
			if Group.getByName(event) then
				newObject = Group.getByName(event)
			elseif StaticObject.getByName(event) then
				newObject = StaticObject.getByName(event)
				--	log:info('its static')
			else
				log:warn('$1 is not a Group or Static Object. This should not be possible. Sent category is: $2', event, objType)
				return false
			end

			newTable.name = newObject:getName()
			newTable.groupId = tonumber(newObject:getID())
			newTable.groupName = newObject:getName()
			local unitOneRef
			if objType == 'static' then
				unitOneRef = newObject
				newTable.countryId = tonumber(newObject:getCountry())
				newTable.coalitionId = tonumber(newObject:getCoalition())
				newTable.category = 'static'
			else
				unitOneRef = newObject:getUnits()
				newTable.countryId = tonumber(unitOneRef[1]:getCountry())
				newTable.coalitionId = tonumber(unitOneRef[1]:getCoalition())
				newTable.category = tonumber(newObject:getCategory())
			end
			for countryData, countryId in pairs(country.id) do
				if newTable.country and string.upper(countryData) == string.upper(newTable.country) or countryId == newTable.countryId then
					newTable.countryId = countryId
					newTable.country = string.lower(countryData)
					for coaData, coaId in pairs(coalition.side) do
						if coaId == coalition.getCountryCoalition(countryId) then
							newTable.coalition = string.lower(coaData)
						end
					end
				end
			end
			for catData, catId in pairs(Unit.Category) do
				if objType == 'group' and Group.getByName(newTable.groupName):isExist() then
					if catId == Group.getByName(newTable.groupName):getCategory() then
						newTable.category = string.lower(catData)
					end
				elseif objType == 'static' and StaticObject.getByName(newTable.groupName):isExist() then
					if catId == StaticObject.getByName(newTable.groupName):getCategory() then
						newTable.category = string.lower(catData)
					end

				end
			end
			local gfound = false
			for index, data in pairs(mistAddedGroups) do
				if mist.stringMatch(data.name, newTable.groupName) == true then
					gfound = true
					newTable.task = data.task
					newTable.modulation = data.modulation
					newTable.uncontrolled = data.uncontrolled
					newTable.radioSet = data.radioSet
					newTable.hidden = data.hidden
					newTable.startTime = data.start_time
					mistAddedGroups[index] = nil
				end
			end

			if gfound == false then
				newTable.uncontrolled = false
				newTable.hidden = false
			end

			newTable.units = {}
			if objType == 'group' then
				for unitId, unitData in pairs(unitOneRef) do
					newTable.units[unitId] = {}
					newTable.units[unitId].unitName = unitData:getName()

					newTable.units[unitId].x = mist.utils.round(unitData:getPosition().p.x)
					newTable.units[unitId].y = mist.utils.round(unitData:getPosition().p.z)
					newTable.units[unitId].point = {}
					newTable.units[unitId].point.x = newTable.units[unitId].x
					newTable.units[unitId].point.y = newTable.units[unitId].y
					newTable.units[unitId].alt = mist.utils.round(unitData:getPosition().p.y)
					newTable.units[unitId].speed = mist.vec.mag(unitData:getVelocity())

					newTable.units[unitId].heading = mist.getHeading(unitData, true)

					newTable.units[unitId].type = unitData:getTypeName()
					newTable.units[unitId].unitId = tonumber(unitData:getID())


					newTable.units[unitId].groupName = newTable.groupName
					newTable.units[unitId].groupId = newTable.groupId
					newTable.units[unitId].countryId = newTable.countryId
					newTable.units[unitId].coalitionId = newTable.coalitionId
					newTable.units[unitId].coalition = newTable.coalition
					newTable.units[unitId].country = newTable.country
					local found = false
					for index, data in pairs(mistAddedObjects) do
						if mist.stringMatch(data.name, newTable.units[unitId].unitName) == true then
							found = true
							newTable.units[unitId].livery_id = data.livery_id
							newTable.units[unitId].skill = data.skill
							newTable.units[unitId].alt_type = data.alt_type
							newTable.units[unitId].callsign = data.callsign
							newTable.units[unitId].psi = data.psi
							mistAddedObjects[index] = nil
						end
						if found == false then
							newTable.units[unitId].skill = "High"
							newTable.units[unitId].alt_type = "BARO"
						end
						if newTable.units[unitId].alt_type == "RADIO" then -- raw postition MSL was grabbed for group, but spawn is AGL, so re-offset it
							newTable.units[unitId].alt = (newTable.units[unitId].alt - land.getHeight({x = newTable.units[unitId].x, y = newTable.units[unitId].y}))
						end
					end

				end
			else -- its a static
                newTable.category = 'static'
				newTable.units[1] = {}
				newTable.units[1].unitName = newObject:getName()
				newTable.units[1].category = 'static'
				newTable.units[1].x = mist.utils.round(newObject:getPosition().p.x)
				newTable.units[1].y = mist.utils.round(newObject:getPosition().p.z)
				newTable.units[1].point = {}
				newTable.units[1].point.x = newTable.units[1].x
				newTable.units[1].point.y = newTable.units[1].y
				newTable.units[1].alt = mist.utils.round(newObject:getPosition().p.y)
				newTable.units[1].heading = mist.getHeading(newObject, true)
				newTable.units[1].type = newObject:getTypeName()
				newTable.units[1].unitId = tonumber(newObject:getID())
				newTable.units[1].groupName = newTable.name
				newTable.units[1].groupId = newTable.groupId
				newTable.units[1].countryId = newTable.countryId
				newTable.units[1].country = newTable.country
				newTable.units[1].coalitionId = newTable.coalitionId
				newTable.units[1].coalition = newTable.coalition
				if newObject:getCategory() == 6 and newObject:getCargoDisplayName() then
					local mass = newObject:getCargoDisplayName()
					mass = string.gsub(mass, ' ', '')
					mass = string.gsub(mass, 'kg', '')
					newTable.units[1].mass = tonumber(mass)
					newTable.units[1].categoryStatic = 'Cargos'
					newTable.units[1].canCargo = true
					newTable.units[1].shape_name = 'ab-212_cargo'
				end

				----- search mist added objects for extra data if applicable
				for index, data in pairs(mistAddedObjects) do
					if mist.stringMatch(data.name, newTable.units[1].unitName) == true then
						newTable.units[1].shape_name = data.shape_name -- for statics
						newTable.units[1].livery_id = data.livery_id
						newTable.units[1].airdromeId = data.airdromeId
						newTable.units[1].mass = data.mass
						newTable.units[1].canCargo = data.canCargo
						newTable.units[1].categoryStatic = data.categoryStatic
						newTable.units[1].type = data.type
						mistAddedObjects[index] = nil
                        break
					end
				end
			end
		end
		--mist.debug.writeData(mist.utils.serialize,{'msg', newTable}, timer.getAbsTime() ..'Group.lua')
		newTable.timeAdded = timer.getAbsTime() -- only on the dynGroupsAdded table. For other reference, see start time
		--mist.debug.dumpDBs()
		--end
		--dbLog:info('endDbUpdate')
		return newTable
	end

	--[[DB update code... FRACK. I need to refactor some of it. 
	
	The problem is that the DBs need to account better for shared object names. Needs to write over some data and outright remove other.
	
	If groupName is used then entire group needs to be rewritten
		what to do with old groups units DB entries?. Names cant be assumed to be the same.
	
	
	-- new spawn event check.
	-- event handler filters everything into groups: tempSpawnedGroups
	-- this function then checks DBs to see if data has changed
	]]
	local function checkSpawnedEventsNew()
		if tempSpawnGroupsCounter > 0 then
			--[[local updatesPerRun = math.ceil(#tempSpawnedGroupsCounter/20)
			if updatesPerRun < 5 then
				updatesPerRun = 5
			end]]
			
			--dbLog:info('iterate')
			for name, gData in pairs(tempSpawnedGroups) do
				--env.info(name)
				local updated = false
                local stillExists = false
                if not gData.checked then 
                    tempSpawnedGroups[name].checked = true -- so if there was an error it will get cleared.
                    local _g = gData.gp or Group.getByName(name)
                    if mist.DBs.groupsByName[name] then
                        -- first check group level properties, groupId, countryId, coalition
                       -- dbLog:info('Found in DBs, check if updated')
                        local dbTable = mist.DBs.groupsByName[name]
                       -- dbLog:info(dbTable)
                        if gData.type ~= 'static' then
                           -- dbLog:info('Not static')
                          
                            if _g and _g:isExist() == true then 
                                stillExists = true
                                local _u = _g:getUnit(1)

                                if _u and (dbTable.groupId ~= tonumber(_g:getID()) or _u:getCountry() ~= dbTable.countryId or _u:getCoalition() ~= dbTable.coaltionId) then
                                    --dbLog:info('Group Data mismatch')
                                    updated = true
                                else
                                  --  dbLog:info('No Mismatch')
                                end
                            else
                                dbLog:warn('$1 : Group was not accessible', name)
                            end
                        end
                    end			
                    --dbLog:info('Updated: $1', updated)
                    if updated == false and gData.type ~= 'static' then -- time to check units
                        --dbLog:info('No Group Mismatch, Check Units')
                        if _g and _g:isExist() == true then 
                            stillExists = true
                            for index, uObject in pairs(_g:getUnits()) do
                                --dbLog:info(index)
                                if mist.DBs.unitsByName[uObject:getName()] then
                                    --dbLog:info('UnitByName table exists')
                                    local uTable = mist.DBs.unitsByName[uObject:getName()]
                                    if tonumber(uObject:getID()) ~= uTable.unitId or uObject:getTypeName() ~= uTable.type  then
                                        --dbLog:info('Unit Data mismatch')
                                        updated = true
                                        break
                                    end
                                end
                            end
                        end
                    else
                        stillExists = true
                    end

                    if stillExists == true and (updated == true or not mist.DBs.groupsByName[name]) then
                        --dbLog:info('Get Table')
                        writeGroups[#writeGroups+1] = {data = dbUpdate(name, gData.type), isUpdated = updated}
                    
                    end
                    -- Work done, so remove
                end
                tempSpawnedGroups[name] = nil
                tempSpawnGroupsCounter = tempSpawnGroupsCounter - 1
			end			
		end	
	end
	
	local function updateDBTables()
		local i = #writeGroups

		local savesPerRun = math.ceil(i/10)
		if savesPerRun < 5 then
			savesPerRun = 5
		end
		if i > 0 then
			--dbLog:info('updateDBTables')
			local ldeepCopy = mist.utils.deepCopy
			for x = 1, i do
				--dbLog:info(writeGroups[x])
				local newTable = writeGroups[x].data
				local updated = writeGroups[x].isUpdated
				local mistCategory
				if type(newTable.category) == 'string' then
					mistCategory = string.lower(newTable.category)
				end

				if string.upper(newTable.category) == 'GROUND_UNIT' then
					mistCategory = 'vehicle'
					newTable.category = mistCategory
				elseif string.upper(newTable.category) == 'AIRPLANE' then
					mistCategory = 'plane'
					newTable.category = mistCategory
				elseif string.upper(newTable.category) == 'HELICOPTER' then
					mistCategory = 'helicopter'
					newTable.category = mistCategory
				elseif string.upper(newTable.category) == 'SHIP' then
					mistCategory = 'ship'
					newTable.category = mistCategory
				end
				--dbLog:info('Update unitsBy')
				for newId, newUnitData in pairs(newTable.units) do
					--dbLog:info(newId)
					newUnitData.category = mistCategory
					if newUnitData.unitId then
						--dbLog:info('byId')
						mist.DBs.unitsById[tonumber(newUnitData.unitId)] = ldeepCopy(newUnitData)
					end
					--dbLog:info(updated)
					if mist.DBs.unitsByName[newUnitData.unitName] and updated == true then--if unit existed before and something was updated, write over the entry for a given unit name just in case.
						--dbLog:info('Updating Unit Tables')
						for i = 1, #mist.DBs.unitsByCat[mistCategory] do
							if mist.DBs.unitsByCat[mistCategory][i].unitName == newUnitData.unitName then
								--dbLog:info('Entry Found, Rewriting for unitsByCat')
								mist.DBs.unitsByCat[mistCategory][i] = ldeepCopy(newUnitData)
								break
							end
						end 
						for i = 1, #mist.DBs.unitsByNum do
							if mist.DBs.unitsByNum[i].unitName == newUnitData.unitName then
								--dbLog:info('Entry Found, Rewriting for unitsByNum')
								mist.DBs.unitsByNum[i] = ldeepCopy(newUnitData)
								break
							end
						end
						
					else
						--dbLog:info('Unitname not in use, add as normal')
						mist.DBs.unitsByCat[mistCategory][#mist.DBs.unitsByCat[mistCategory] + 1] = ldeepCopy(newUnitData)
						mist.DBs.unitsByNum[#mist.DBs.unitsByNum + 1] = ldeepCopy(newUnitData)
					end
					mist.DBs.unitsByName[newUnitData.unitName] = ldeepCopy(newUnitData)

					
				end
				-- this is a really annoying DB to populate. Gotta create new tables in case its missing
				--dbLog:info('write mist.DBs.units')
				if not mist.DBs.units[newTable.coalition] then
					mist.DBs.units[newTable.coalition] = {}
				end

				if not mist.DBs.units[newTable.coalition][newTable.country] then
					mist.DBs.units[newTable.coalition][(newTable.country)] = {}
					mist.DBs.units[newTable.coalition][(newTable.country)].countryId = newTable.countryId
				end
				if not mist.DBs.units[newTable.coalition][newTable.country][mistCategory] then
					mist.DBs.units[newTable.coalition][(newTable.country)][mistCategory] = {}
				end
				
				if updated == true then
					--dbLog:info('Updating DBsUnits')
					for i = 1, #mist.DBs.units[newTable.coalition][(newTable.country)][mistCategory] do
						if mist.DBs.units[newTable.coalition][(newTable.country)][mistCategory][i].groupName == newTable.groupName then
							--dbLog:info('Entry Found, Rewriting')
							mist.DBs.units[newTable.coalition][(newTable.country)][mistCategory][i] = ldeepCopy(newTable)
							break
						end
					end
				else
					mist.DBs.units[newTable.coalition][(newTable.country)][mistCategory][#mist.DBs.units[newTable.coalition][(newTable.country)][mistCategory] + 1] = ldeepCopy(newTable)
				end
				

				if newTable.groupId then
					mist.DBs.groupsById[newTable.groupId] = ldeepCopy(newTable)
				end

				mist.DBs.groupsByName[newTable.name] = ldeepCopy(newTable)
				mist.DBs.dynGroupsAdded[#mist.DBs.dynGroupsAdded + 1] = ldeepCopy(newTable)

				writeGroups[x] = nil
				if x%savesPerRun == 0 then
					coroutine.yield()
				end
			end
			if timer.getTime() > lastUpdateTime then
				lastUpdateTime = timer.getTime()
			end
			--dbLog:info('endUpdateTables')
		end
	end

	local function groupSpawned(event)
		-- dont need to add units spawned in at the start of the mission if mist is loaded in init line
		if event.id == world.event.S_EVENT_BIRTH and timer.getTime0() < timer.getAbsTime() then
			--dbLog:info('unitSpawnEvent')
			
				--table.insert(tempSpawnedUnits,(event.initiator))
				-------
				-- New functionality below. 
				-------
			if Object.getCategory(event.initiator) == 1 and not Unit.getPlayerName(event.initiator) then -- simple player check, will need to later check to see if unit was spawned with a player in a flight
				--dbLog:info('Object is a Unit')
				if Unit.getGroup(event.initiator) then
					--dbLog:info(Unit.getGroup(event.initiator):getName())
                    local g = Unit.getGroup(event.initiator)
					if not tempSpawnedGroups[g:getName()] then
						--dbLog:info('added')
						tempSpawnedGroups[g:getName()] = {type = 'group', gp = g}
						tempSpawnGroupsCounter = tempSpawnGroupsCounter + 1
					end
				else
					log:error('Group not accessible by unit in event handler. This is a DCS bug')
				end
			elseif Object.getCategory(event.initiator) == 3 or Object.getCategory(event.initiator) == 6 then
				--dbLog:info('Object is Static')
				tempSpawnedGroups[StaticObject.getName(event.initiator)] = {type = 'static'}
				tempSpawnGroupsCounter = tempSpawnGroupsCounter + 1
			end
				
			
		end
	end

	local function doScheduledFunctions()
		local i = 1
		while i <= #scheduledTasks do
			if not scheduledTasks[i].rep then -- not a repeated process
				if scheduledTasks[i].t <= timer.getTime() then
					local task = scheduledTasks[i] -- local reference
					table.remove(scheduledTasks, i)
					local err, errmsg = pcall(task.f, unpack(task.vars, 1, table.maxn(task.vars)))
					if not err then
						log:error('Error in scheduled function: $1', errmsg)
					end
					--task.f(unpack(task.vars, 1, table.maxn(task.vars)))	-- do the task, do not increment i
				else
					i = i + 1
				end
			else
				if scheduledTasks[i].st and scheduledTasks[i].st <= timer.getTime() then	 --if a stoptime was specified, and the stop time exceeded
					table.remove(scheduledTasks, i) -- stop time exceeded, do not execute, do not increment i
				elseif scheduledTasks[i].t <= timer.getTime() then
					local task = scheduledTasks[i] -- local reference
					task.t = timer.getTime() + task.rep	--schedule next run
					local err, errmsg = pcall(task.f, unpack(task.vars, 1, table.maxn(task.vars)))
					if not err then
						log:error('Error in scheduled function: $1' .. errmsg)
					end
					--scheduledTasks[i].f(unpack(scheduledTasks[i].vars, 1, table.maxn(scheduledTasks[i].vars)))	-- do the task
					i = i + 1
				else
					i = i + 1
				end
			end
		end
	end

	-- Event handler to start creating the dead_objects table
	local function addDeadObject(event)
		if event.id == world.event.S_EVENT_DEAD or event.id == world.event.S_EVENT_CRASH then
			if event.initiator and event.initiator.id_ and event.initiator.id_ > 0 then

				local id = event.initiator.id_	-- initial ID, could change if there is a duplicate id_ already dead.
				local val = {object = event.initiator} -- the new entry in mist.DBs.deadObjects.

				local original_id = id	--only for duplicate runtime IDs.
				local id_ind = 1
				while mist.DBs.deadObjects[id] do
					--log:info('duplicate runtime id of previously dead object id: $1', id)
					id = tostring(original_id) .. ' #' .. tostring(id_ind)
					id_ind = id_ind + 1
				end

				if mist.DBs.aliveUnits and mist.DBs.aliveUnits[val.object.id_] then
					--log:info('object found in alive_units')
					val.objectData = mist.utils.deepCopy(mist.DBs.aliveUnits[val.object.id_])
					local pos = Object.getPosition(val.object)
					if pos then
						val.objectPos = pos.p
					end
					val.objectType = mist.DBs.aliveUnits[val.object.id_].category
					--[[if mist.DBs.activeHumans[Unit.getName(val.object)] then
					--trigger.action.outText('remove via death: ' .. Unit.getName(val.object),20)
						mist.DBs.activeHumans[Unit.getName(val.object)] = nil
					end]]
				elseif mist.DBs.removedAliveUnits and mist.DBs.removedAliveUnits[val.object.id_] then	-- it didn't exist in alive_units, check old_alive_units
					--log:info('object found in old_alive_units')
					val.objectData = mist.utils.deepCopy(mist.DBs.removedAliveUnits[val.object.id_])
					local pos = Object.getPosition(val.object)
					if pos then
						val.objectPos = pos.p
					end
					val.objectType = mist.DBs.removedAliveUnits[val.object.id_].category

				else	--attempt to determine if static object...
					--log:info('object not found in alive units or old alive units')
					local pos = Object.getPosition(val.object)
					if pos then
						local static_found = false
						for ind, static in pairs(mist.DBs.unitsByCat.static) do
							if ((pos.p.x - static.point.x)^2 + (pos.p.z - static.point.y)^2)^0.5 < 0.1 then --really, it should be zero...
								--log:info('correlated dead static object to position')
								val.objectData = static
								val.objectPos = pos.p
								val.objectType = 'static'
								static_found = true
								break
							end
						end
						if not static_found then
							val.objectPos = pos.p
							val.objectType = 'building'
						end
					else
						val.objectType = 'unknown'
					end
				end
				mist.DBs.deadObjects[id] = val
			end
		end
	end

	--[[
		local function addClientsToActive(event)
			if event.id == world.event.S_EVENT_PLAYER_ENTER_UNIT or event.id == world.event.S_EVENT_BIRTH then
				log:info(event)
				if Unit.getPlayerName(event.initiator) then
					log:info(Unit.getPlayerName(event.initiator))
					local newU = mist.utils.deepCopy(mist.DBs.unitsByName[Unit.getName(event.initiator)])
					newU.playerName = Unit.getPlayerName(event.initiator)
					mist.DBs.activeHumans[Unit.getName(event.initiator)] = newU
					--trigger.action.outText('added: ' .. Unit.getName(event.initiator), 20)
				end
			elseif event.id == world.event.S_EVENT_PLAYER_LEAVE_UNIT and event.initiator then
				if mist.DBs.activeHumans[Unit.getName(event.initiator)] then
					mist.DBs.activeHumans[Unit.getName(event.initiator)] = nil
					-- trigger.action.outText('removed via control: ' .. Unit.getName(event.initiator), 20)
				end
			end
		end

	mist.addEventHandler(addClientsToActive)
	]]
    local function verifyDB()
        --log:warn('verfy Run')
        for coaName, coaId in pairs(coalition.side) do
            --env.info(coaName)
            local gps = coalition.getGroups(coaId)
            for i = 1, #gps do
                if gps[i] and Group.getSize(gps[i]) > 0 then
                    local gName = Group.getName(gps[i])
                    if not mist.DBs.groupsByName[gName] then
                            --env.info(Unit.getID(gUnits[j]) .. ' Not found in DB yet')
                        if not tempSpawnedGroups[gName] then
                            --dbLog:info('added')
                            tempSpawnedGroups[gName] = {type = 'group', gp = gps[i]}
                            tempSpawnGroupsCounter = tempSpawnGroupsCounter + 1
                        end
                    end
                end
            end
            local st = coalition.getStaticObjects(coaId)
            for i = 1, #st do
                local s = st[i]
                if StaticObject.isExist(s) then
                    if not mist.DBs.unitsByName[s:getName()] then
                        --env.info(StaticObject.getID(s) .. ' Not found in DB yet')
                        tempSpawnedGroups[s:getName()] = {type = 'static'}
                        tempSpawnGroupsCounter = tempSpawnGroupsCounter + 1
                    end
                end
            end
        
        end
    
    end

	--- init function.
	-- creates logger, adds default event handler
	-- and calls main the first time.
	-- @function mist.init
	function mist.init()
        
		-- create logger
		mist.log = mist.Logger:new("MIST", mistSettings.logLevel)
		dbLog = mist.Logger:new('MISTDB', 'warn')
		
		log = mist.log -- log shorthand
		-- set warning log level, showing only
		-- warnings and errors
		--log:setLevel("warning")

		log:info("initializing databases")
		initDBs()

		-- add event handler for group spawns
		mist.addEventHandler(groupSpawned)
		mist.addEventHandler(addDeadObject)
        
        log:warn('Init time: $1', timer.getTime())

		-- call main the first time therafter it reschedules itself.
		mist.main()
		--log:msg('MIST version $1.$2.$3 loaded', mist.majorVersion, mist.minorVersion, mist.build)
        
        mist.scheduleFunction(verifyDB, {}, timer.getTime() + 1)
		return
	end

	--- The main function.
	-- Run 100 times per second.
	-- You shouldn't call this function.
	function mist.main()
		timer.scheduleFunction(mist.main, {}, timer.getTime() + 0.01)	--reschedule first in case of Lua error

		updateTenthSecond = updateTenthSecond + 1
		if updateTenthSecond == 20 then
			updateTenthSecond = 0

			checkSpawnedEventsNew()
			
			if not coroutines.updateDBTables then
				coroutines.updateDBTables = coroutine.create(updateDBTables)
			end

			coroutine.resume(coroutines.updateDBTables)

			if coroutine.status(coroutines.updateDBTables) == 'dead' then
				coroutines.updateDBTables = nil
			end
		end

		--updating alive units
		updateAliveUnitsCounter = updateAliveUnitsCounter + 1
		if updateAliveUnitsCounter == 5 then
			updateAliveUnitsCounter = 0

			if not coroutines.updateAliveUnits then
				coroutines.updateAliveUnits = coroutine.create(updateAliveUnits)
			end

			coroutine.resume(coroutines.updateAliveUnits)

			if coroutine.status(coroutines.updateAliveUnits) == 'dead' then
				coroutines.updateAliveUnits = nil
			end
		end

		doScheduledFunctions()
	end -- end of mist.main

	--- Returns next unit id.
	-- @treturn number next unit id.
	function mist.getNextUnitId()
		mist.nextUnitId = mist.nextUnitId + 1
		if mist.nextUnitId > 6900 and mist.nextUnitId < 30000 then
			mist.nextUnitId = 30000
		end
		return mist.utils.deepCopy(mist.nextUnitId)
	end

	--- Returns next group id.
	-- @treturn number next group id.
	function mist.getNextGroupId()
		mist.nextGroupId = mist.nextGroupId + 1
		if mist.nextGroupId > 6900 and mist.nextGroupId < 30000 then
			mist.nextGroupId = 30000
		end
		return mist.utils.deepCopy(mist.nextGroupId)
	end

	--- Returns timestamp of last database update.
	-- @treturn timestamp of last database update
	function mist.getLastDBUpdateTime()
		return lastUpdateTime
	end

	--- Spawns a static object to the game world.
	-- @todo write good docs
	-- @tparam table staticObj table containing data needed for the object creation
	function mist.dynAddStatic(newObj)
        log:info(newObj)
		if newObj.units and newObj.units[1] then -- if its mist format
			for entry, val in pairs(newObj.units[1]) do
				if newObj[entry] and newObj[entry] ~= val or not newObj[entry] then
					newObj[entry] = val
				end
			end
		end
		--log:info(newObj)
		
		local cntry = newObj.country
		if newObj.countryId then
			cntry = newObj.countryId
		end
	
		local newCountry = ''

		for countryId, countryName in pairs(country.name) do
			if type(cntry) == 'string' then
				cntry = cntry:gsub("%s+", "_")
				if tostring(countryName) == string.upper(cntry) then
					newCountry = countryName
				end
			elseif type(cntry) == 'number' then
				if countryId == cntry then
					newCountry = countryName
				end
			end
		end
		
		if newCountry == '' then
			log:error("Country not found: $1", cntry)
			return false
		end
	
		if newObj.clone or not newObj.groupId then
			mistGpId = mistGpId + 1
			newObj.groupId = mistGpId
		end

		if newObj.clone or not newObj.unitId then
			mistUnitId = mistUnitId + 1
			newObj.unitId = mistUnitId
		end


        newObj.name = newObj.name or newObj.unitName
        
		if newObj.clone or not newObj.name then
			mistDynAddIndex[' static '] = mistDynAddIndex[' static '] + 1
			newObj.name = (newCountry .. ' static ' .. mistDynAddIndex[' static '])
		end

		if not newObj.dead then
			newObj.dead = false
		end

		if not newObj.heading then
			newObj.heading = math.random(360)
		end
		
		if newObj.categoryStatic then
			newObj.category = newObj.categoryStatic
		end
		if newObj.mass then
			newObj.category = 'Cargos'
		end
		
		if newObj.shapeName then
			newObj.shape_name = newObj.shapeName
		end
		
		if not newObj.shape_name then
			log:info('shape_name not present')
			if mist.DBs.const.shapeNames[newObj.type] then
				newObj.shape_name = mist.DBs.const.shapeNames[newObj.type]
			end
		end
		
		mistAddedObjects[#mistAddedObjects + 1] = mist.utils.deepCopy(newObj)
		if newObj.x and newObj.y and newObj.type and type(newObj.x) == 'number' and type(newObj.y) == 'number' and type(newObj.type) == 'string' then
			log:info(newObj)
			coalition.addStaticObject(country.id[newCountry], newObj)

			return newObj
		end
		log:error("Failed to add static object due to missing or incorrect value. X: $1, Y: $2, Type: $3", newObj.x, newObj.y, newObj.type)
		return false
	end

	--- Spawns a dynamic group into the game world.
	-- Same as coalition.add function in SSE. checks the passed data to see if its valid.
	-- Will generate groupId, groupName, unitId, and unitName if needed
	-- @tparam table newGroup table containting values needed for spawning a group.
	function mist.dynAdd(newGroup)

		--mist.debug.writeData(mist.utils.serialize,{'msg', newGroup}, 'newGroupOrig.lua')
		local cntry = newGroup.country
		if newGroup.countryId then
			cntry = newGroup.countryId
		end

		local groupType = newGroup.category
		local newCountry = ''
		-- validate data
		for countryId, countryName in pairs(country.name) do
			if type(cntry) == 'string' then
				cntry = cntry:gsub("%s+", "_")
				if tostring(countryName) == string.upper(cntry) then
					newCountry = countryName
				end
			elseif type(cntry) == 'number' then
				if countryId == cntry then
					newCountry = countryName
				end
			end
		end

		if newCountry == '' then
			log:error("Country not found: $1", cntry)
			return false
		end

		local newCat = ''
		for catName, catId in pairs(Unit.Category) do
			if type(groupType) == 'string' then
				if tostring(catName) == string.upper(groupType) then
					newCat = catName
				end
			elseif type(groupType) == 'number' then
				if catId == groupType then
					newCat = catName
				end
			end

			if catName == 'GROUND_UNIT' and (string.upper(groupType) == 'VEHICLE' or string.upper(groupType) == 'GROUND') then
				newCat = 'GROUND_UNIT'
			elseif catName == 'AIRPLANE' and string.upper(groupType) == 'PLANE' then
				newCat = 'AIRPLANE'
			end
		end
		local typeName
		if newCat == 'GROUND_UNIT' then
			typeName = ' gnd '
		elseif newCat == 'AIRPLANE' then
			typeName = ' air '
		elseif newCat == 'HELICOPTER' then
			typeName = ' hel '
		elseif newCat == 'SHIP' then
			typeName = ' shp '
		elseif newCat == 'BUILDING' then
			typeName = ' bld '
		end
		if newGroup.clone or not newGroup.groupId then
			mistDynAddIndex[typeName] = mistDynAddIndex[typeName] + 1
			mistGpId = mistGpId + 1
			newGroup.groupId = mistGpId
		end
		if newGroup.groupName or newGroup.name then
			if newGroup.groupName then
				newGroup.name = newGroup.groupName
			elseif newGroup.name then
				newGroup.name = newGroup.name
			end
		end

		if newGroup.clone and mist.DBs.groupsByName[newGroup.name] or not newGroup.name then
			newGroup.name = tostring(newCountry .. tostring(typeName) .. mistDynAddIndex[typeName])
		end

		if not newGroup.hidden then
			newGroup.hidden = false
		end

		if not newGroup.visible then
			newGroup.visible = false
		end

		if (newGroup.start_time and type(newGroup.start_time) ~= 'number') or not newGroup.start_time then
			if newGroup.startTime then
				newGroup.start_time = mist.utils.round(newGroup.startTime)
			else
				newGroup.start_time = 0
			end
		end


		for unitIndex, unitData in pairs(newGroup.units) do
			local originalName = newGroup.units[unitIndex].unitName or newGroup.units[unitIndex].name
			if newGroup.clone or not unitData.unitId then
				mistUnitId = mistUnitId + 1
				newGroup.units[unitIndex].unitId = mistUnitId
			end
			if newGroup.units[unitIndex].unitName or newGroup.units[unitIndex].name then
				if newGroup.units[unitIndex].unitName then
					newGroup.units[unitIndex].name = newGroup.units[unitIndex].unitName
				elseif newGroup.units[unitIndex].name then
					newGroup.units[unitIndex].name = newGroup.units[unitIndex].name
				end
			end
			if newGroup.clone or not unitData.name then
				newGroup.units[unitIndex].name = tostring(newGroup.name .. ' unit' .. unitIndex)
			end

			if not unitData.skill then
				newGroup.units[unitIndex].skill = 'Random'
			end

			if newCat == 'AIRPLANE' or newCat == 'HELICOPTER' then
				if newGroup.units[unitIndex].alt_type and newGroup.units[unitIndex].alt_type ~= 'BARO' or not newGroup.units[unitIndex].alt_type then
					newGroup.units[unitIndex].alt_type = 'RADIO'
				end
				if not unitData.speed then
					if newCat == 'AIRPLANE' then
						newGroup.units[unitIndex].speed = 150
					elseif newCat == 'HELICOPTER' then
						newGroup.units[unitIndex].speed = 60
					end
				end
				if not unitData.payload then
					newGroup.units[unitIndex].payload = mist.getPayload(originalName)
				end
				if not unitData.alt then
					if newCat == 'AIRPLANE' then
						newGroup.units[unitIndex].alt = 2000
						newGroup.units[unitIndex].alt_type = 'RADIO'
						newGroup.units[unitIndex].speed = 150
					elseif newCat == 'HELICOPTER' then
						newGroup.units[unitIndex].alt = 500
						newGroup.units[unitIndex].alt_type = 'RADIO'
						newGroup.units[unitIndex].speed = 60
					end
				end
				
			elseif newCat == 'GROUND_UNIT' then
				if nil == unitData.playerCanDrive then
					unitData.playerCanDrive = true
				end
			
			end
			mistAddedObjects[#mistAddedObjects + 1] = mist.utils.deepCopy(newGroup.units[unitIndex])
		end
		mistAddedGroups[#mistAddedGroups + 1] = mist.utils.deepCopy(newGroup)
		if newGroup.route then
            if newGroup.route and not newGroup.route.points then
                if newGroup.route[1] then
                    local copyRoute = mist.utils.deepCopy(newGroup.route)
                    newGroup.route = {}
                    newGroup.route.points = copyRoute
                end
            end
		else -- if aircraft and no route assigned. make a quick and stupid route so AI doesnt RTB immediately
			if newCat == 'AIRPLANE' or newCat == 'HELICOPTER' then
				newGroup.route = {}
				newGroup.route.points = {}
				newGroup.route.points[1] = {}
			end
		end
		newGroup.country = newCountry


		--mist.debug.writeData(mist.utils.serialize,{'msg', newGroup}, 'newGroup.lua')
        --log:warn(newGroup)
		-- sanitize table
		newGroup.groupName = nil
		newGroup.clone = nil
		newGroup.category = nil
		newGroup.country = nil

		newGroup.tasks = {}

		for unitIndex, unitData in pairs(newGroup.units) do
			newGroup.units[unitIndex].unitName = nil
		end

		coalition.addGroup(country.id[newCountry], Unit.Category[newCat], newGroup)

		return newGroup

	end

	--- Schedules a function.
	-- Modified Slmod task scheduler, superior to timer.scheduleFunction
	-- @tparam function f function to schedule
	-- @tparam table vars array containing all parameters passed to the function
	-- @tparam number t time in seconds from mission start to schedule the function to.
	-- @tparam[opt] number rep time between repetitions of the function
	-- @tparam[opt] number st time in seconds from mission start at which the function
	-- should stop to be rescheduled.
	-- @treturn number scheduled function id.
	function mist.scheduleFunction(f, vars, t, rep, st)
		--verify correct types
		assert(type(f) == 'function', 'variable 1, expected function, got ' .. type(f))
		assert(type(vars) == 'table' or vars == nil, 'variable 2, expected table or nil, got ' .. type(f))
		assert(type(t) == 'number', 'variable 3, expected number, got ' .. type(t))
		assert(type(rep) == 'number' or rep == nil, 'variable 4, expected number or nil, got ' .. type(rep))
		assert(type(st) == 'number' or st == nil, 'variable 5, expected number or nil, got ' .. type(st))
		if not vars then
			vars = {}
		end
		taskId = taskId + 1
		table.insert(scheduledTasks, {f = f, vars = vars, t = t, rep = rep, st = st, id = taskId})
		return taskId
	end

	--- Removes a scheduled function.
	-- @tparam number id function id
	-- @treturn boolean true if function was successfully removed, false otherwise.
	function mist.removeFunction(id)
		local i = 1
		while i <= #scheduledTasks do
			if scheduledTasks[i].id == id then
				table.remove(scheduledTasks, i)
                return true
			else
				i = i + 1
			end
		end
        return false
	end

	--- Registers an event handler.
	-- @tparam function f function handling event
	-- @treturn number id of the event handler
	function mist.addEventHandler(f) --id is optional!
		local handler = {}
		idNum = idNum + 1
		handler.id = idNum
		handler.f = f
		function handler:onEvent(event)
			self.f(event)
		end
		world.addEventHandler(handler)
		return handler.id
	end

	--- Removes event handler with given id.
	-- @tparam number id event handler id
	-- @treturn boolean true on success, false otherwise
	function mist.removeEventHandler(id)
		for key, handler in pairs(world.eventHandlers) do
			if handler.id and handler.id == id then
				world.eventHandlers[key] = nil
				return true
			end
		end
		return false
	end
end

-- Begin common funcs
do
	--- Returns MGRS coordinates as string.
	-- @tparam string MGRS MGRS coordinates
	-- @tparam number acc the accuracy of each easting/northing.
	-- Can be: 0, 1, 2, 3, 4, or 5.
	function mist.tostringMGRS(MGRS, acc)
		if acc == 0 then
			return MGRS.UTMZone .. ' ' .. MGRS.MGRSDigraph
		else
			return MGRS.UTMZone .. ' ' .. MGRS.MGRSDigraph .. ' ' .. string.format('%0' .. acc .. 'd', mist.utils.round(MGRS.Easting/(10^(5-acc)), 0))
			.. ' ' .. string.format('%0' .. acc .. 'd', mist.utils.round(MGRS.Northing/(10^(5-acc)), 0))
		end
	end

	--[[acc:
	in DM: decimal point of minutes.
	In DMS: decimal point of seconds.
	position after the decimal of the least significant digit:
	So:
	42.32 - acc of 2.
	]]
	function mist.tostringLL(lat, lon, acc, DMS)

		local latHemi, lonHemi
		if lat > 0 then
			latHemi = 'N'
		else
			latHemi = 'S'
		end

		if lon > 0 then
			lonHemi = 'E'
		else
			lonHemi = 'W'
		end

		lat = math.abs(lat)
		lon = math.abs(lon)

		local latDeg = math.floor(lat)
		local latMin = (lat - latDeg)*60

		local lonDeg = math.floor(lon)
		local lonMin = (lon - lonDeg)*60

		if DMS then	-- degrees, minutes, and seconds.
			local oldLatMin = latMin
			latMin = math.floor(latMin)
			local latSec = mist.utils.round((oldLatMin - latMin)*60, acc)

			local oldLonMin = lonMin
			lonMin = math.floor(lonMin)
			local lonSec = mist.utils.round((oldLonMin - lonMin)*60, acc)

			if latSec == 60 then
				latSec = 0
				latMin = latMin + 1
			end

			if lonSec == 60 then
				lonSec = 0
				lonMin = lonMin + 1
			end

			local secFrmtStr -- create the formatting string for the seconds place
			if acc <= 0 then	-- no decimal place.
				secFrmtStr = '%02d'
			else
				local width = 3 + acc	-- 01.310 - that's a width of 6, for example.
				secFrmtStr = '%0' .. width .. '.' .. acc .. 'f'
			end

			return string.format('%02d', latDeg) .. ' ' .. string.format('%02d', latMin) .. '\' ' .. string.format(secFrmtStr, latSec) .. '"' .. latHemi .. '	 '
			.. string.format('%02d', lonDeg) .. ' ' .. string.format('%02d', lonMin) .. '\' ' .. string.format(secFrmtStr, lonSec) .. '"' .. lonHemi

		else	-- degrees, decimal minutes.
			latMin = mist.utils.round(latMin, acc)
			lonMin = mist.utils.round(lonMin, acc)

			if latMin == 60 then
				latMin = 0
				latDeg = latDeg + 1
			end

			if lonMin == 60 then
				lonMin = 0
				lonDeg = lonDeg + 1
			end

			local minFrmtStr -- create the formatting string for the minutes place
			if acc <= 0 then	-- no decimal place.
				minFrmtStr = '%02d'
			else
				local width = 3 + acc	-- 01.310 - that's a width of 6, for example.
				minFrmtStr = '%0' .. width .. '.' .. acc .. 'f'
			end

			return string.format('%02d', latDeg) .. ' ' .. string.format(minFrmtStr, latMin) .. '\'' .. latHemi .. '	 '
			.. string.format('%02d', lonDeg) .. ' ' .. string.format(minFrmtStr, lonMin) .. '\'' .. lonHemi

		end
	end

	--[[ required: az - radian
		required: dist - meters
		optional: alt - meters (set to false or nil if you don't want to use it).
		optional: metric - set true to get dist and alt in km and m.
		precision will always be nearest degree and NM or km.]]
	function mist.tostringBR(az, dist, alt, metric)
		az = mist.utils.round(mist.utils.toDegree(az), 0)

		if metric then
			dist = mist.utils.round(dist/1000, 0)
		else
			dist = mist.utils.round(mist.utils.metersToNM(dist), 0)
		end

		local s = string.format('%03d', az) .. ' for ' .. dist

		if alt then
			if metric then
				s = s .. ' at ' .. mist.utils.round(alt, 0)
			else
				s = s .. ' at ' .. mist.utils.round(mist.utils.metersToFeet(alt), 0)
			end
		end
		return s
	end

	function mist.getNorthCorrection(gPoint)	--gets the correction needed for true north
		local point = mist.utils.deepCopy(gPoint)
		if not point.z then --Vec2; convert to Vec3
			point.z = point.y
			point.y = 0
		end
		local lat, lon = coord.LOtoLL(point)
		local north_posit = coord.LLtoLO(lat + 1, lon)
		return math.atan2(north_posit.z - point.z, north_posit.x - point.x)
	end

	--- Returns skill of the given unit.
	-- @tparam string unitName unit name
	-- @return skill of the unit
	function mist.getUnitSkill(unitName)
		if mist.DBs.unitsByName[unitName] then
			if Unit.getByName(unitName) then
				local lunit = Unit.getByName(unitName)
				local data = mist.DBs.unitsByName[unitName]
				if data.unitName == unitName and data.type == lunit:getTypeName() and data.unitId == tonumber(lunit:getID()) and data.skill then
					return data.skill
				end
			end
		end
		log:error("Unit not found in DB: $1", unitName)
		return false
	end

	--- Returns an array containing a group's units positions.
	--	e.g.
	--		{
	--			[1] = {x = 299435.224, y = -1146632.6773},
	--			[2] = {x = 663324.6563, y = 322424.1112}
	--		}
	--	@tparam number|string groupIdent group id or name
	--	@treturn table array containing positions of each group member
	function mist.getGroupPoints(groupIdent)
		-- search by groupId and allow groupId and groupName as inputs
		local gpId = groupIdent
		if type(groupIdent) == 'string' and not tonumber(groupIdent) then
			if mist.DBs.MEgroupsByName[groupIdent] then
				gpId = mist.DBs.MEgroupsByName[groupIdent].groupId
			else
				log:error("Group not found in mist.DBs.MEgroupsByName: $1", groupIdent)
			end
		end

		for coa_name, coa_data in pairs(env.mission.coalition) do
			if  type(coa_data) == 'table' then
				if coa_data.country then --there is a country table
					for cntry_id, cntry_data in pairs(coa_data.country) do
						for obj_type_name, obj_type_data in pairs(cntry_data) do
							if obj_type_name == "helicopter" or obj_type_name == "ship" or obj_type_name == "plane" or obj_type_name == "vehicle" then	-- only these types have points
								if ((type(obj_type_data) == 'table') and obj_type_data.group and (type(obj_type_data.group) == 'table') and (#obj_type_data.group > 0)) then	--there's a group!
									for group_num, group_data in pairs(obj_type_data.group) do
										if group_data and group_data.groupId == gpId then -- this is the group we are looking for
											if group_data.route and group_data.route.points and #group_data.route.points > 0 then
												local points = {}
												for point_num, point in pairs(group_data.route.points) do
													if not point.point then
														points[point_num] = { x = point.x, y = point.y }
													else
														points[point_num] = point.point	--it's possible that the ME could move to the point = Vec2 notation.
													end
												end
												return points
											end
											return
										end	--if group_data and group_data.name and group_data.name == 'groupname'
									end --for group_num, group_data in pairs(obj_type_data.group) do
								end --if ((type(obj_type_data) == 'table') and obj_type_data.group and (type(obj_type_data.group) == 'table') and (#obj_type_data.group > 0)) then
							end --if obj_type_name == "helicopter" or obj_type_name == "ship" or obj_type_name == "plane" or obj_type_name == "vehicle" or obj_type_name == "static" then
						end --for obj_type_name, obj_type_data in pairs(cntry_data) do
					end --for cntry_id, cntry_data in pairs(coa_data.country) do
				end --if coa_data.country then --there is a country table
			end --if coa_name == 'red' or coa_name == 'blue' and type(coa_data) == 'table' then
		end --for coa_name, coa_data in pairs(mission.coalition) do
	end

	--- getUnitAttitude(unit) return values.
	-- Yaw, AoA, ClimbAngle - relative to earth reference
	-- DOES NOT TAKE INTO ACCOUNT WIND.
	-- @table attitude
	-- @tfield number Heading in radians, range of 0 to 2*pi,
	-- relative to true north.
	-- @tfield number Pitch in radians, range of -pi/2 to pi/2
	-- @tfield number Roll in radians, range of 0 to 2*pi,
	-- right roll is positive direction.
	-- @tfield number Yaw in radians, range of -pi to pi,
	-- right yaw is positive direction.
	-- @tfield number AoA in radians, range of -pi to pi,
	-- rotation of aircraft to the right in comparison to
	-- flight direction being positive.
	-- @tfield number ClimbAngle in radians, range of -pi/2 to pi/2

	--- Returns the attitude of a given unit.
	-- Will work on any unit, even if not an aircraft.
	-- @tparam Unit unit unit whose attitude is returned.
	-- @treturn table @{attitude}
	function mist.getAttitude(unit)
		local unitpos = unit:getPosition()
		if unitpos then

			local Heading = math.atan2(unitpos.x.z, unitpos.x.x)

			Heading = Heading + mist.getNorthCorrection(unitpos.p)

			if Heading < 0 then
				Heading = Heading + 2*math.pi	-- put heading in range of 0 to 2*pi
			end
			---- heading complete.----

			local Pitch = math.asin(unitpos.x.y)
			---- pitch complete.----

			-- now get roll:
			--maybe not the best way to do it, but it works.

			--first, make a vector that is perpendicular to y and unitpos.x with cross product
			local cp = mist.vec.cp(unitpos.x, {x = 0, y = 1, z = 0})

			--now, get dot product of of this cross product with unitpos.z
			local dp = mist.vec.dp(cp, unitpos.z)

			--now get the magnitude of the roll (magnitude of the angle between two vectors is acos(vec1.vec2/|vec1||vec2|)
			local Roll = math.acos(dp/(mist.vec.mag(cp)*mist.vec.mag(unitpos.z)))

			--now, have to get sign of roll.
			-- by convention, making right roll positive
			-- to get sign of roll, use the y component of unitpos.z.	For right roll, y component is negative.

			if unitpos.z.y > 0 then -- left roll, flip the sign of the roll
				Roll = -Roll
			end
			---- roll complete. ----

			--now, work on yaw, AoA, climb, and abs velocity
			local Yaw
			local AoA
			local ClimbAngle

			-- get unit velocity
			local unitvel = unit:getVelocity()
			if mist.vec.mag(unitvel) ~= 0 then --must have non-zero velocity!
				local AxialVel = {}	--unit velocity transformed into aircraft axes directions

				--transform velocity components in direction of aircraft axes.
				AxialVel.x = mist.vec.dp(unitpos.x, unitvel)
				AxialVel.y = mist.vec.dp(unitpos.y, unitvel)
				AxialVel.z = mist.vec.dp(unitpos.z, unitvel)

				--Yaw is the angle between unitpos.x and the x and z velocities
				--define right yaw as positive
				Yaw = math.acos(mist.vec.dp({x = 1, y = 0, z = 0}, {x = AxialVel.x, y = 0, z = AxialVel.z})/mist.vec.mag({x = AxialVel.x, y = 0, z = AxialVel.z}))

				--now set correct direction:
				if AxialVel.z > 0 then
					Yaw = -Yaw
				end

				-- AoA is angle between unitpos.x and the x and y velocities
				AoA = math.acos(mist.vec.dp({x = 1, y = 0, z = 0}, {x = AxialVel.x, y = AxialVel.y, z = 0})/mist.vec.mag({x = AxialVel.x, y = AxialVel.y, z = 0}))

				--now set correct direction:
				if AxialVel.y > 0 then
					AoA = -AoA
				end

				ClimbAngle = math.asin(unitvel.y/mist.vec.mag(unitvel))
			end
			return { Heading = Heading, Pitch = Pitch, Roll = Roll, Yaw = Yaw, AoA = AoA, ClimbAngle = ClimbAngle}
		else
			log:error("Couldn't get unit's position")
		end
	end

	--- Returns heading of given unit.
	-- @tparam Unit unit unit whose heading is returned.
	-- @param rawHeading
	-- @treturn number heading of the unit, in range
	-- of 0 to 2*pi.
	function mist.getHeading(unit, rawHeading)
		local unitpos = unit:getPosition()
		if unitpos then
			local Heading = math.atan2(unitpos.x.z, unitpos.x.x)
			if not rawHeading then
				Heading = Heading + mist.getNorthCorrection(unitpos.p)
			end
			if Heading < 0 then
				Heading = Heading + 2*math.pi	-- put heading in range of 0 to 2*pi
			end
			return Heading
		end
	end

	--- Returns given unit's pitch
	-- @tparam Unit unit unit whose pitch is returned.
	-- @treturn number pitch of given unit
	function mist.getPitch(unit)
		local unitpos = unit:getPosition()
		if unitpos then
			return math.asin(unitpos.x.y)
		end
	end

	--- Returns given unit's roll.
	-- @tparam Unit unit unit whose roll is returned.
	-- @treturn number roll of given unit
	function mist.getRoll(unit)
		local unitpos = unit:getPosition()
		if unitpos then
			-- now get roll:
			--maybe not the best way to do it, but it works.

			--first, make a vector that is perpendicular to y and unitpos.x with cross product
			local cp = mist.vec.cp(unitpos.x, {x = 0, y = 1, z = 0})

			--now, get dot product of of this cross product with unitpos.z
			local dp = mist.vec.dp(cp, unitpos.z)

			--now get the magnitude of the roll (magnitude of the angle between two vectors is acos(vec1.vec2/|vec1||vec2|)
			local Roll = math.acos(dp/(mist.vec.mag(cp)*mist.vec.mag(unitpos.z)))

			--now, have to get sign of roll.
			-- by convention, making right roll positive
			-- to get sign of roll, use the y component of unitpos.z.	For right roll, y component is negative.

			if unitpos.z.y > 0 then -- left roll, flip the sign of the roll
				Roll = -Roll
			end
			return Roll
		end
	end

	--- Returns given unit's yaw.
	-- @tparam Unit unit unit whose yaw is returned.
	-- @treturn number yaw of given unit.
	function mist.getYaw(unit)
		local unitpos = unit:getPosition()
		if unitpos then
			-- get unit velocity
			local unitvel = unit:getVelocity()
			if mist.vec.mag(unitvel) ~= 0 then --must have non-zero velocity!
				local AxialVel = {}	--unit velocity transformed into aircraft axes directions

				--transform velocity components in direction of aircraft axes.
				AxialVel.x = mist.vec.dp(unitpos.x, unitvel)
				AxialVel.y = mist.vec.dp(unitpos.y, unitvel)
				AxialVel.z = mist.vec.dp(unitpos.z, unitvel)

				--Yaw is the angle between unitpos.x and the x and z velocities
				--define right yaw as positive
				local Yaw = math.acos(mist.vec.dp({x = 1, y = 0, z = 0}, {x = AxialVel.x, y = 0, z = AxialVel.z})/mist.vec.mag({x = AxialVel.x, y = 0, z = AxialVel.z}))

				--now set correct direction:
				if AxialVel.z > 0 then
					Yaw = -Yaw
				end
				return Yaw
			end
		end
	end

	--- Returns given unit's angle of attack.
	-- @tparam Unit unit unit to get AoA from.
	-- @treturn number angle of attack of the given unit.
	function mist.getAoA(unit)
		local unitpos = unit:getPosition()
		if unitpos then
			local unitvel = unit:getVelocity()
			if mist.vec.mag(unitvel) ~= 0 then --must have non-zero velocity!
				local AxialVel = {}	--unit velocity transformed into aircraft axes directions

				--transform velocity components in direction of aircraft axes.
				AxialVel.x = mist.vec.dp(unitpos.x, unitvel)
				AxialVel.y = mist.vec.dp(unitpos.y, unitvel)
				AxialVel.z = mist.vec.dp(unitpos.z, unitvel)

				-- AoA is angle between unitpos.x and the x and y velocities
				local AoA = math.acos(mist.vec.dp({x = 1, y = 0, z = 0}, {x = AxialVel.x, y = AxialVel.y, z = 0})/mist.vec.mag({x = AxialVel.x, y = AxialVel.y, z = 0}))

				--now set correct direction:
				if AxialVel.y > 0 then
					AoA = -AoA
				end
				return AoA
			end
		end
	end

	--- Returns given unit's climb angle.
	-- @tparam Unit unit unit to get climb angle from.
	-- @treturn number climb angle of given unit.
	function mist.getClimbAngle(unit)
		local unitpos = unit:getPosition()
		if unitpos then
			local unitvel = unit:getVelocity()
			if mist.vec.mag(unitvel) ~= 0 then --must have non-zero velocity!
				return math.asin(unitvel.y/mist.vec.mag(unitvel))
			end
		end
	end

	--[[--
	Unit name table.
	Many Mist functions require tables of unit names, which are known
	in Mist as UnitNameTables. These follow a special set of shortcuts
	borrowed from Slmod. These shortcuts alleviate the problem of entering
	huge lists of unit names by hand, and in many cases, they remove the
	need to even know the names of the units in the first place!

	These are the unit table "short-cut" commands:

	Prefixes:
			"[-u]<unit name>" - subtract this unit if its in the table
			"[g]<group name>" - add this group to the table
			"[-g]<group name>" - subtract this group from the table
			"[c]<country name>"	- add this country's units
			"[-c]<country name>" - subtract this country's units if any are in the table

	Stand-alone identifiers
			"[all]" - add all units
			"[-all]" - subtract all units (not very useful by itself)
			"[blue]" - add all blue units
			"[-blue]" - subtract all blue units
			"[red]" - add all red coalition units
			"[-red]" - subtract all red units

	Compound Identifiers:
			"[c][helicopter]<country name>"	- add all of this country's helicopters
			"[-c][helicopter]<country name>" - subtract all of this country's helicopters
			"[c][plane]<country name>"	- add all of this country's planes
			"[-c][plane]<country name>" - subtract all of this country's planes
			"[c][ship]<country name>"	- add all of this country's ships
			"[-c][ship]<country name>" - subtract all of this country's ships
			"[c][vehicle]<country name>"	- add all of this country's vehicles
			"[-c][vehicle]<country name>" - subtract all of this country's vehicles

			"[all][helicopter]" -	add all helicopters
			"[-all][helicopter]" - subtract all helicopters
			"[all][plane]" - add all	planes
			"[-all][plane]" - subtract all planes
			"[all][ship]" - add all ships
			"[-all][ship]" - subtract all ships
			"[all][vehicle]" - add all vehicles
			"[-all][vehicle]" - subtract all vehicles

			"[blue][helicopter]" -	add all blue coalition helicopters
			"[-blue][helicopter]" - subtract all blue coalition helicopters
			"[blue][plane]" - add all blue coalition planes
			"[-blue][plane]" - subtract all blue coalition planes
			"[blue][ship]" - add all blue coalition ships
			"[-blue][ship]" - subtract all blue coalition ships
			"[blue][vehicle]" - add all blue coalition vehicles
			"[-blue][vehicle]" - subtract all blue coalition vehicles

			"[red][helicopter]" -	add all red coalition helicopters
			"[-red][helicopter]" - subtract all red coalition helicopters
			"[red][plane]" - add all red coalition planes
			"[-red][plane]" - subtract all red coalition planes
			"[red][ship]" - add all red coalition ships
			"[-red][ship]" - subtract all red coalition ships
			"[red][vehicle]" - add all red coalition vehicles
			"[-red][vehicle]" - subtract all red coalition vehicles

	Country names to be used in [c] and [-c] short-cuts:
			Turkey
			Norway
			The Netherlands
			Spain
			11
			UK
			Denmark
			USA
			Georgia
			Germany
			Belgium
			Canada
			France
			Israel
			Ukraine
			Russia
			South Ossetia
			Abkhazia
			Italy
			Australia
			Austria
			Belarus
			Bulgaria
			Czech Republic
			China
			Croatia
			Finland
			Greece
			Hungary
			India
			Iran
			Iraq
			Japan
			Kazakhstan
			North Korea
			Pakistan
			Poland
			Romania
			Saudi Arabia
			Serbia, Slovakia
			South Korea
			Sweden
			Switzerland
			Syria
			USAF Aggressors

	Do NOT use a '[u]' notation for single units. Single units are referenced
	the same way as before: Simply input their names as strings.

	These unit tables are evaluated in order, and you cannot subtract a unit
	from a table before it is added. For example:

			{'[blue]', '[-c]Georgia'}

	will evaluate to all of blue coalition except those units owned by the
	country named "Georgia"; however:

			{'[-c]Georgia', '[blue]'}

	will evaluate to all of the units in blue coalition, because the addition
	of all units owned by blue coalition occurred AFTER the subtraction of all
	units owned by Georgia (which actually subtracted nothing at all, since
	there were no units in the table when the subtraction occurred).

	More examples:

			{'[blue][plane]', '[-c]Georgia', '[-g]Hawg 1'}

	Evaluates to all blue planes, except those blue units owned by the country
	named "Georgia" and the units in the group named "Hawg1".


			{'[g]arty1', '[g]arty2', '[-u]arty1_AD', '[-u]arty2_AD', 'Shark 11' }

	Evaluates to the unit named "Shark 11", plus all the units in groups named
	"arty1" and "arty2" except those that are named "arty1\_AD" and "arty2\_AD".

	@table UnitNameTable
	]]

	--- Returns a table containing unit names.
	-- @tparam table tbl sequential strings
	-- @treturn table @{UnitNameTable}
	function mist.makeUnitTable(tbl)
		--Assumption: will be passed a table of strings, sequential
		--log:info(tbl)
		local units_by_name = {}

		local l_munits = mist.DBs.units	--local reference for faster execution
		for i = 1, #tbl do
			local unit = tbl[i]
			if unit:sub(1,4) == '[-u]' then --subtract a unit
				if units_by_name[unit:sub(5)] then -- 5 to end
				units_by_name[unit:sub(5)] = nil	--remove
			end
		elseif unit:sub(1,3) == '[g]' then -- add a group
			for coa, coa_tbl in pairs(l_munits) do
				for country, country_table in pairs(coa_tbl) do
					for unit_type, unit_type_tbl in pairs(country_table) do
						if type(unit_type_tbl) == 'table' then
							for group_ind, group_tbl in pairs(unit_type_tbl) do
								if type(group_tbl) == 'table' and group_tbl.groupName == unit:sub(4) then
									-- index 4 to end
									for unit_ind, unit in pairs(group_tbl.units) do
										units_by_name[unit.unitName] = true	--add
									end
								end
							end
						end
					end
				end
			end
		elseif unit:sub(1,4) == '[-g]' then -- subtract a group
			for coa, coa_tbl in pairs(l_munits) do
				for country, country_table in pairs(coa_tbl) do
					for unit_type, unit_type_tbl in pairs(country_table) do
						if type(unit_type_tbl) == 'table' then
							for group_ind, group_tbl in pairs(unit_type_tbl) do
								if type(group_tbl) == 'table' and group_tbl.groupName == unit:sub(5) then
									-- index 5 to end
									for unit_ind, unit in pairs(group_tbl.units) do
										if units_by_name[unit.unitName] then
											units_by_name[unit.unitName] = nil --remove
										end
									end
								end
							end
						end
					end
				end
			end
		elseif unit:sub(1,3) == '[c]' then -- add a country
			local category = ''
			local country_start = 4
			if unit:sub(4,15) == '[helicopter]' then
				category = 'helicopter'
				country_start = 16
			elseif unit:sub(4,10) == '[plane]' then
				category = 'plane'
				country_start = 11
			elseif unit:sub(4,9) == '[ship]' then
				category = 'ship'
				country_start = 10
			elseif unit:sub(4,12) == '[vehicle]' then
				category = 'vehicle'
				country_start = 13
			end
			for coa, coa_tbl in pairs(l_munits) do
				for country, country_table in pairs(coa_tbl) do
					if country == string.lower(unit:sub(country_start)) then	 -- match
						for unit_type, unit_type_tbl in pairs(country_table) do
							if type(unit_type_tbl) == 'table' and (category == '' or unit_type == category) then
								for group_ind, group_tbl in pairs(unit_type_tbl) do
									if type(group_tbl) == 'table' then
										for unit_ind, unit in pairs(group_tbl.units) do
											units_by_name[unit.unitName] = true	--add
										end
									end
								end
							end
						end
					end
				end
			end
		elseif unit:sub(1,4) == '[-c]' then -- subtract a country
			local category = ''
			local country_start = 5
			if unit:sub(5,16) == '[helicopter]' then
				category = 'helicopter'
				country_start = 17
			elseif unit:sub(5,11) == '[plane]' then
				category = 'plane'
				country_start = 12
			elseif unit:sub(5,10) == '[ship]' then
				category = 'ship'
				country_start = 11
			elseif unit:sub(5,13) == '[vehicle]' then
				category = 'vehicle'
				country_start = 14
			end
			for coa, coa_tbl in pairs(l_munits) do
				for country, country_table in pairs(coa_tbl) do
					if country == string.lower(unit:sub(country_start)) then	 -- match
						for unit_type, unit_type_tbl in pairs(country_table) do
							if type(unit_type_tbl) == 'table' and (category == '' or unit_type == category) then
								for group_ind, group_tbl in pairs(unit_type_tbl) do
									if type(group_tbl) == 'table' then
										for unit_ind, unit in pairs(group_tbl.units) do
											if units_by_name[unit.unitName] then
												units_by_name[unit.unitName] = nil	--remove
											end
										end
									end
								end
							end
						end
					end
				end
			end
		elseif unit:sub(1,6) ==	'[blue]' then -- add blue coalition
			local category = ''
			if unit:sub(7) == '[helicopter]' then
				category = 'helicopter'
			elseif unit:sub(7) == '[plane]' then
				category = 'plane'
			elseif unit:sub(7) == '[ship]' then
				category = 'ship'
			elseif unit:sub(7) == '[vehicle]' then
				category = 'vehicle'
			end
			for coa, coa_tbl in pairs(l_munits) do
				if coa == 'blue' then
					for country, country_table in pairs(coa_tbl) do
						for unit_type, unit_type_tbl in pairs(country_table) do
							if type(unit_type_tbl) == 'table' and (category == '' or unit_type == category) then
								for group_ind, group_tbl in pairs(unit_type_tbl) do
									if type(group_tbl) == 'table' then
										for unit_ind, unit in pairs(group_tbl.units) do
											units_by_name[unit.unitName] = true	--add
										end
									end
								end
							end
						end
					end
				end
			end
		elseif unit:sub(1,7) == '[-blue]' then -- subtract blue coalition
			local category = ''
			if unit:sub(8) == '[helicopter]' then
				category = 'helicopter'
			elseif unit:sub(8) == '[plane]' then
				category = 'plane'
			elseif unit:sub(8) == '[ship]' then
				category = 'ship'
			elseif unit:sub(8) == '[vehicle]' then
				category = 'vehicle'
			end
			for coa, coa_tbl in pairs(l_munits) do
				if coa == 'blue' then
					for country, country_table in pairs(coa_tbl) do
						for unit_type, unit_type_tbl in pairs(country_table) do
							if type(unit_type_tbl) == 'table' and (category == '' or unit_type == category) then
								for group_ind, group_tbl in pairs(unit_type_tbl) do
									if type(group_tbl) == 'table' then
										for unit_ind, unit in pairs(group_tbl.units) do
											if units_by_name[unit.unitName] then
												units_by_name[unit.unitName] = nil	--remove
											end
										end
									end
								end
							end
						end
					end
				end
			end
		elseif unit:sub(1,5) == '[red]' then -- add red coalition
			local category = ''
			if unit:sub(6) == '[helicopter]' then
				category = 'helicopter'
			elseif unit:sub(6) == '[plane]' then
				category = 'plane'
			elseif unit:sub(6) == '[ship]' then
				category = 'ship'
			elseif unit:sub(6) == '[vehicle]' then
				category = 'vehicle'
			end
			for coa, coa_tbl in pairs(l_munits) do
				if coa == 'red' then
					for country, country_table in pairs(coa_tbl) do
						for unit_type, unit_type_tbl in pairs(country_table) do
							if type(unit_type_tbl) == 'table' and (category == '' or unit_type == category) then
								for group_ind, group_tbl in pairs(unit_type_tbl) do
									if type(group_tbl) == 'table' then
										for unit_ind, unit in pairs(group_tbl.units) do
											units_by_name[unit.unitName] = true	--add
										end
									end
								end
							end
						end
					end
				end
			end
		elseif unit:sub(1,6) == '[-red]' then -- subtract red coalition
			local category = ''
			if unit:sub(7) == '[helicopter]' then
				category = 'helicopter'
			elseif unit:sub(7) == '[plane]' then
				category = 'plane'
			elseif unit:sub(7) == '[ship]' then
				category = 'ship'
			elseif unit:sub(7) == '[vehicle]' then
				category = 'vehicle'
			end
			for coa, coa_tbl in pairs(l_munits) do
				if coa == 'red' then
					for country, country_table in pairs(coa_tbl) do
						for unit_type, unit_type_tbl in pairs(country_table) do
							if type(unit_type_tbl) == 'table' and (category == '' or unit_type == category) then
								for group_ind, group_tbl in pairs(unit_type_tbl) do
									if type(group_tbl) == 'table' then
										for unit_ind, unit in pairs(group_tbl.units) do
											if units_by_name[unit.unitName] then
												units_by_name[unit.unitName] = nil	--remove
											end
										end
									end
								end
							end
						end
					end
				end
			end
		elseif unit:sub(1,5) == '[all]' then -- add all of a certain category (or all categories)
			local category = ''
			if unit:sub(6) == '[helicopter]' then
				category = 'helicopter'
			elseif unit:sub(6) == '[plane]' then
				category = 'plane'
			elseif unit:sub(6) == '[ship]' then
				category = 'ship'
			elseif unit:sub(6) == '[vehicle]' then
				category = 'vehicle'
			end
			for coa, coa_tbl in pairs(l_munits) do
				for country, country_table in pairs(coa_tbl) do
					for unit_type, unit_type_tbl in pairs(country_table) do
						if type(unit_type_tbl) == 'table' and (category == '' or unit_type == category) then
							for group_ind, group_tbl in pairs(unit_type_tbl) do
								if type(group_tbl) == 'table' then
									for unit_ind, unit in pairs(group_tbl.units) do
										units_by_name[unit.unitName] = true	--add
									end
								end
							end
						end
					end
				end
			end
		elseif unit:sub(1,6) == '[-all]' then -- subtract all of a certain category (or all categories)
			local category = ''
			if unit:sub(7) == '[helicopter]' then
				category = 'helicopter'
			elseif unit:sub(7) == '[plane]' then
				category = 'plane'
			elseif unit:sub(7) == '[ship]' then
				category = 'ship'
			elseif unit:sub(7) == '[vehicle]' then
				category = 'vehicle'
			end
			for coa, coa_tbl in pairs(l_munits) do
				for country, country_table in pairs(coa_tbl) do
					for unit_type, unit_type_tbl in pairs(country_table) do
						if type(unit_type_tbl) == 'table' and (category == '' or unit_type == category) then
							for group_ind, group_tbl in pairs(unit_type_tbl) do
								if type(group_tbl) == 'table' then
									for unit_ind, unit in pairs(group_tbl.units) do
										if units_by_name[unit.unitName] then
											units_by_name[unit.unitName] = nil	--remove
										end
									end
								end
							end
						end
					end
				end
			end
		else -- just a regular unit
			units_by_name[unit] = true	--add
		end
	end

	local units_tbl = {}	-- indexed sequentially
	for unit_name, val in pairs(units_by_name) do
		if val then
			units_tbl[#units_tbl + 1] = unit_name	-- add all the units to the table
		end
	end


	units_tbl.processed = timer.getTime()	--add the processed flag
	return units_tbl
end

function mist.getDeadMapObjsInZones(zone_names)
	-- zone_names: table of zone names
	-- returns: table of dead map objects (indexed numerically)
	local map_objs = {}
	local zones = {}
	for i = 1, #zone_names do
		if mist.DBs.zonesByName[zone_names[i]] then
			zones[#zones + 1] = mist.DBs.zonesByName[zone_names[i]]
		end
	end
	for obj_id, obj in pairs(mist.DBs.deadObjects) do
		if obj.objectType and obj.objectType == 'building' then --dead map object
			for i = 1, #zones do
				if ((zones[i].point.x - obj.objectPos.x)^2 + (zones[i].point.z - obj.objectPos.z)^2)^0.5 <= zones[i].radius then
					map_objs[#map_objs + 1] = mist.utils.deepCopy(obj)
				end
			end
		end
	end
	return map_objs
end

function mist.getDeadMapObjsInPolygonZone(zone)
	-- zone_names: table of zone names
	-- returns: table of dead map objects (indexed numerically)
	local map_objs = {}
	for obj_id, obj in pairs(mist.DBs.deadObjects) do
		if obj.objectType and obj.objectType == 'building' then --dead map object
			if mist.pointInPolygon(obj.objectPos, zone) then
				map_objs[#map_objs + 1] = mist.utils.deepCopy(obj)
			end
		end
	end
	return map_objs
end

function mist.pointInPolygon(point, poly, maxalt) --raycasting point in polygon. Code from http://softsurfer.com/Archive/algorithm_0103/algorithm_0103.htm
	--[[local type_tbl = {
		point = {'table'},
		poly = {'table'},
		maxalt = {'number', 'nil'},
		}

	local err, errmsg = mist.utils.typeCheck('mist.pointInPolygon', type_tbl, {point, poly, maxalt})
	assert(err, errmsg)
	]]
	point = mist.utils.makeVec3(point)
	local px = point.x
	local pz = point.z
	local cn = 0
	local newpoly = mist.utils.deepCopy(poly)

	if not maxalt or (point.y <= maxalt) then
		local polysize = #newpoly
		newpoly[#newpoly + 1] = newpoly[1]

		newpoly[1] = mist.utils.makeVec3(newpoly[1])

		for k = 1, polysize do
			newpoly[k+1] = mist.utils.makeVec3(newpoly[k+1])
			if ((newpoly[k].z <= pz) and (newpoly[k+1].z > pz)) or ((newpoly[k].z > pz) and (newpoly[k+1].z <= pz)) then
				local vt = (pz - newpoly[k].z) / (newpoly[k+1].z - newpoly[k].z)
				if (px < newpoly[k].x + vt*(newpoly[k+1].x - newpoly[k].x)) then
					cn = cn + 1
				end
			end
		end

		return cn%2 == 1
	else
		return false
	end
end

function mist.getUnitsInPolygon(unit_names, polyZone, max_alt)
	local units = {}

	for i = 1, #unit_names do
		units[#units + 1] = Unit.getByName(unit_names[i])
	end

	local inZoneUnits = {}
	for i =1, #units do
		if units[i]:isActive() and mist.pointInPolygon(units[i]:getPosition().p, polyZone, max_alt) then
			inZoneUnits[#inZoneUnits + 1] = units[i]
		end
	end

	return inZoneUnits
end

function mist.getUnitsInZones(unit_names, zone_names, zone_type)

	zone_type = zone_type or 'cylinder'
	if zone_type == 'c' or zone_type == 'cylindrical' or zone_type == 'C' then
		zone_type = 'cylinder'
	end
	if zone_type == 's' or zone_type == 'spherical' or zone_type == 'S' then
		zone_type = 'sphere'
	end

	assert(zone_type == 'cylinder' or zone_type == 'sphere', 'invalid zone_type: ' .. tostring(zone_type))

	local units = {}
	local zones = {}

	for k = 1, #unit_names do
		local unit = Unit.getByName(unit_names[k])
		if unit then
			units[#units + 1] = unit
		end
	end


	for k = 1, #zone_names do
		local zone = trigger.misc.getZone(zone_names[k])
		if zone then
			zones[#zones + 1] = {radius = zone.radius, x = zone.point.x, y = zone.point.y, z = zone.point.z}
		end
	end

	local in_zone_units = {}

	for units_ind = 1, #units do
		for zones_ind = 1, #zones do
			if zone_type == 'sphere' then	--add land height value for sphere zone type
				local alt = land.getHeight({x = zones[zones_ind].x, y = zones[zones_ind].z})
				if alt then
					zones[zones_ind].y = alt
				end
			end
			local unit_pos = units[units_ind]:getPosition().p
            if unit_pos and units[units_ind]:isActive() == true then
				if zone_type == 'cylinder' and (((unit_pos.x - zones[zones_ind].x)^2 + (unit_pos.z - zones[zones_ind].z)^2)^0.5 <= zones[zones_ind].radius) then
					in_zone_units[#in_zone_units + 1] = units[units_ind]
					break
				elseif zone_type == 'sphere' and (((unit_pos.x - zones[zones_ind].x)^2 + (unit_pos.y - zones[zones_ind].y)^2 + (unit_pos.z - zones[zones_ind].z)^2)^0.5 <= zones[zones_ind].radius) then
					in_zone_units[#in_zone_units + 1] = units[units_ind]
					break
				end
			end
		end
	end
	return in_zone_units
end

function mist.getUnitsInMovingZones(unit_names, zone_unit_names, radius, zone_type)

	zone_type = zone_type or 'cylinder'
	if zone_type == 'c' or zone_type == 'cylindrical' or zone_type == 'C' then
		zone_type = 'cylinder'
	end
	if zone_type == 's' or zone_type == 'spherical' or zone_type == 'S' then
		zone_type = 'sphere'
	end

	assert(zone_type == 'cylinder' or zone_type == 'sphere', 'invalid zone_type: ' .. tostring(zone_type))

	local units = {}
	local zone_units = {}

	for k = 1, #unit_names do
		local unit = Unit.getByName(unit_names[k])
		if unit then
			units[#units + 1] = unit
		end
	end

	for k = 1, #zone_unit_names do
		local unit = Unit.getByName(zone_unit_names[k])
		if unit then
			zone_units[#zone_units + 1] = unit
		end
	end

	local in_zone_units = {}

	for units_ind = 1, #units do
		for zone_units_ind = 1, #zone_units do
			local unit_pos = units[units_ind]:getPosition().p
			local zone_unit_pos = zone_units[zone_units_ind]:getPosition().p
			if unit_pos and zone_unit_pos and units[units_ind]:isActive() == true then
				if zone_type == 'cylinder' and (((unit_pos.x - zone_unit_pos.x)^2 + (unit_pos.z - zone_unit_pos.z)^2)^0.5 <= radius) then
					in_zone_units[#in_zone_units + 1] = units[units_ind]
					break
				elseif zone_type == 'sphere' and (((unit_pos.x - zone_unit_pos.x)^2 + (unit_pos.y - zone_unit_pos.y)^2 + (unit_pos.z - zone_unit_pos.z)^2)^0.5 <= radius) then
					in_zone_units[#in_zone_units + 1] = units[units_ind]
					break
				end
			end
		end
	end
	return in_zone_units
end

function mist.getUnitsLOS(unitset1, altoffset1, unitset2, altoffset2, radius)
	log:info("$1, $2, $3, $4, $5", unitset1, altoffset1, unitset2, altoffset2, radius)
	radius = radius or math.huge
	local unit_info1 = {}
	local unit_info2 = {}

	-- get the positions all in one step, saves execution time.
	for unitset1_ind = 1, #unitset1 do
		local unit1 = Unit.getByName(unitset1[unitset1_ind])
		if unit1 and unit1:isActive() == true then
			unit_info1[#unit_info1 + 1] = {}
			unit_info1[#unit_info1].unit = unit1
			unit_info1[#unit_info1].pos	= unit1:getPosition().p
		end
	end

	for unitset2_ind = 1, #unitset2 do
		local unit2 = Unit.getByName(unitset2[unitset2_ind])
		if unit2 and unit2:isActive() == true then
			unit_info2[#unit_info2 + 1] = {}
			unit_info2[#unit_info2].unit = unit2
			unit_info2[#unit_info2].pos	= unit2:getPosition().p
		end
	end

	local LOS_data = {}
	-- now compute los
	for unit1_ind = 1, #unit_info1 do
		local unit_added = false
		for unit2_ind = 1, #unit_info2 do
			if radius == math.huge or (mist.vec.mag(mist.vec.sub(unit_info1[unit1_ind].pos, unit_info2[unit2_ind].pos)) < radius) then -- inside radius
				local point1 = { x = unit_info1[unit1_ind].pos.x, y = unit_info1[unit1_ind].pos.y + altoffset1, z = unit_info1[unit1_ind].pos.z}
				local point2 = { x = unit_info2[unit2_ind].pos.x, y = unit_info2[unit2_ind].pos.y + altoffset2, z = unit_info2[unit2_ind].pos.z}
				if land.isVisible(point1, point2) then
					if unit_added == false then
						unit_added = true
						LOS_data[#LOS_data + 1] = {}
						LOS_data[#LOS_data].unit = unit_info1[unit1_ind].unit
						LOS_data[#LOS_data].vis = {}
						LOS_data[#LOS_data].vis[#LOS_data[#LOS_data].vis + 1] = unit_info2[unit2_ind].unit
					else
						LOS_data[#LOS_data].vis[#LOS_data[#LOS_data].vis + 1] = unit_info2[unit2_ind].unit
					end
				end
			end
		end
	end

	return LOS_data
end

function mist.getAvgPoint(points)
	local avgX, avgY, avgZ, totNum = 0, 0, 0, 0
	for i = 1, #points do
		local nPoint = mist.utils.makeVec3(points[i])
		if nPoint.z then
			avgX = avgX + nPoint.x
			avgY = avgY + nPoint.y
			avgZ = avgZ + nPoint.z
			totNum = totNum + 1
		end
	end
	if totNum ~= 0 then
		return {x = avgX/totNum, y = avgY/totNum, z = avgZ/totNum}
	end
end

--Gets the average position of a group of units (by name)
function mist.getAvgPos(unitNames)
	local avgX, avgY, avgZ, totNum = 0, 0, 0, 0
	for i = 1, #unitNames do
		local unit
		if Unit.getByName(unitNames[i]) then
			unit = Unit.getByName(unitNames[i])
		elseif StaticObject.getByName(unitNames[i]) then
			unit = StaticObject.getByName(unitNames[i])
		end
		if unit then
			local pos = unit:getPosition().p
			if pos then -- you never know O.o
				avgX = avgX + pos.x
				avgY = avgY + pos.y
				avgZ = avgZ + pos.z
				totNum = totNum + 1
			end
		end
	end
	if totNum ~= 0 then
		return {x = avgX/totNum, y = avgY/totNum, z = avgZ/totNum}
	end
end

function mist.getAvgGroupPos(groupName)
	if type(groupName) == 'string' and Group.getByName(groupName) and Group.getByName(groupName):isExist() == true then
		groupName = Group.getByName(groupName)
	end
	local units = {}
	for i = 1, groupName:getSize() do
		table.insert(units, groupName:getUnit(i):getName())
	end

	return mist.getAvgPos(units)

end

--[[ vars for mist.getMGRSString:
vars.units - table of unit names (NOT unitNameTable- maybe this should change).
vars.acc - integer between 0 and 5, inclusive
]]
function mist.getMGRSString(vars)
	local units = vars.units
	local acc = vars.acc or 5
	local avgPos = mist.getAvgPos(units)
	if avgPos then
		return mist.tostringMGRS(coord.LLtoMGRS(coord.LOtoLL(avgPos)), acc)
	end
end

--[[ vars for mist.getLLString
vars.units - table of unit names (NOT unitNameTable- maybe this should change).
vars.acc - integer, number of numbers after decimal place
vars.DMS - if true, output in degrees, minutes, seconds.	Otherwise, output in degrees, minutes.
]]
function mist.getLLString(vars)
	local units = vars.units
	local acc = vars.acc or 3
	local DMS = vars.DMS
	local avgPos = mist.getAvgPos(units)
	if avgPos then
		local lat, lon = coord.LOtoLL(avgPos)
		return mist.tostringLL(lat, lon, acc, DMS)
	end
end

--[[
vars.units- table of unit names (NOT unitNameTable- maybe this should change).
vars.ref -	vec3 ref point, maybe overload for vec2 as well?
vars.alt - boolean, if used, includes altitude in string
vars.metric - boolean, gives distance in km instead of NM.
]]
function mist.getBRString(vars)
	local units = vars.units
	local ref = mist.utils.makeVec3(vars.ref, 0)	-- turn it into Vec3 if it is not already.
	local alt = vars.alt
	local metric = vars.metric
	local avgPos = mist.getAvgPos(units)
	if avgPos then
		local vec = {x = avgPos.x - ref.x, y = avgPos.y - ref.y, z = avgPos.z - ref.z}
		local dir = mist.utils.getDir(vec, ref)
		local dist = mist.utils.get2DDist(avgPos, ref)
		if alt then
			alt = avgPos.y
		end
		return mist.tostringBR(dir, dist, alt, metric)
	end
end

-- Returns the Vec3 coordinates of the average position of the concentration of units most in the heading direction.
--[[ vars for mist.getLeadingPos:
vars.units - table of unit names
vars.heading - direction
vars.radius - number
vars.headingDegrees - boolean, switches heading to degrees
]]
function mist.getLeadingPos(vars)
	local units = vars.units
	local heading = vars.heading
	local radius = vars.radius
	if vars.headingDegrees then
		heading = mist.utils.toRadian(vars.headingDegrees)
	end

	local unitPosTbl = {}
	for i = 1, #units do
		local unit = Unit.getByName(units[i])
		if unit and unit:isExist() then
			unitPosTbl[#unitPosTbl + 1] = unit:getPosition().p
		end
	end
	if #unitPosTbl > 0 then	-- one more more units found.
		-- first, find the unit most in the heading direction
		local maxPos = -math.huge

		local maxPosInd	-- maxPos - the furthest in direction defined by heading; maxPosInd =
		for i = 1, #unitPosTbl do
			local rotatedVec2 = mist.vec.rotateVec2(mist.utils.makeVec2(unitPosTbl[i]), heading)
			if (not maxPos) or maxPos < rotatedVec2.x then
				maxPos = rotatedVec2.x
				maxPosInd = i
			end
		end

		--now, get all the units around this unit...
		local avgPos
		if radius then
			local maxUnitPos = unitPosTbl[maxPosInd]
			local avgx, avgy, avgz, totNum = 0, 0, 0, 0
			for i = 1, #unitPosTbl do
				if mist.utils.get2DDist(maxUnitPos, unitPosTbl[i]) <= radius then
					avgx = avgx + unitPosTbl[i].x
					avgy = avgy + unitPosTbl[i].y
					avgz = avgz + unitPosTbl[i].z
					totNum = totNum + 1
				end
			end
			avgPos = { x = avgx/totNum, y = avgy/totNum, z = avgz/totNum}
		else
			avgPos = unitPosTbl[maxPosInd]
		end

		return avgPos
	end
end

--[[ vars for mist.getLeadingMGRSString:
vars.units - table of unit names
vars.heading - direction
vars.radius - number
vars.headingDegrees - boolean, switches heading to degrees
vars.acc - number, 0 to 5.
]]
function mist.getLeadingMGRSString(vars)
	local pos = mist.getLeadingPos(vars)
	if pos then
		local acc = vars.acc or 5
		return mist.tostringMGRS(coord.LLtoMGRS(coord.LOtoLL(pos)), acc)
	end
end

--[[ vars for mist.getLeadingLLString:
vars.units - table of unit names
vars.heading - direction, number
vars.radius - number
vars.headingDegrees - boolean, switches heading to degrees
vars.acc - number of digits after decimal point (can be negative)
vars.DMS -	boolean, true if you want DMS.
]]
function mist.getLeadingLLString(vars)
	local pos = mist.getLeadingPos(vars)
	if pos then
		local acc = vars.acc or 3
		local DMS = vars.DMS
		local lat, lon = coord.LOtoLL(pos)
		return mist.tostringLL(lat, lon, acc, DMS)
	end
end

--[[ vars for mist.getLeadingBRString:
vars.units - table of unit names
vars.heading - direction, number
vars.radius - number
vars.headingDegrees - boolean, switches heading to degrees
vars.metric - boolean, if true, use km instead of NM.
vars.alt - boolean, if true, include altitude.
vars.ref - vec3/vec2 reference point.
]]
function mist.getLeadingBRString(vars)
	local pos = mist.getLeadingPos(vars)
	if pos then
		local ref = vars.ref
		local alt = vars.alt
		local metric = vars.metric

		local vec = {x = pos.x - ref.x, y = pos.y - ref.y, z = pos.z - ref.z}
		local dir = mist.utils.getDir(vec, ref)
		local dist = mist.utils.get2DDist(pos, ref)
		if alt then
			alt = pos.y
		end
		return mist.tostringBR(dir, dist, alt, metric)
	end
end

end

--- Group functions.
-- @section groups
do -- group functions scope

	--- Check table used for group creation.
	-- @tparam table groupData table to check.
	-- @treturn boolean true if a group can be spawned using
	-- this table, false otherwise.
	function mist.groupTableCheck(groupData)
		-- return false if country, category
		-- or units are missing
		if not groupData.country or
			not groupData.category or
			not groupData.units then
			return false
		end
		-- return false if unitData misses
		-- x, y or type
		for unitId, unitData in pairs(groupData.units) do
			if not unitData.x or
				not unitData.y or
				not unitData.type then
					return false
			end
		end
		-- everything we need is here return true
		return true
	end

	--- Returns group data table of give group.
	function mist.getCurrentGroupData(gpName)
		local dbData = mist.getGroupData(gpName)

		if Group.getByName(gpName) and Group.getByName(gpName):isExist() == true then
			local newGroup = Group.getByName(gpName)
			local newData = {}
			newData.name = gpName
			newData.groupId = tonumber(newGroup:getID())
			newData.category = newGroup:getCategory()
			newData.groupName = gpName
			newData.hidden = dbData.hidden

			if newData.category == 2 then
				newData.category = 'vehicle'
			elseif newData.category == 3 then
				newData.category = 'ship'
			end

			newData.units = {}
			local newUnits = newGroup:getUnits()
			for unitNum, unitData in pairs(newGroup:getUnits()) do
				newData.units[unitNum] = {}
                local uName = unitData:getName()

                if mist.DBs.unitsByName[uName] and unitData:getTypeName() ==  mist.DBs.unitsByName[uName].type and mist.DBs.unitsByName[uName].unitId == tonumber(unitData:getID()) then -- If old data matches most of new data
                    newData.units[unitNum] = mist.utils.deepCopy(mist.DBs.unitsByName[uName])
                else
                    newData.units[unitNum].unitId = tonumber(unitData:getID())
                    newData.units[unitNum].type = unitData:getTypeName()
                    newData.units[unitNum].skill = mist.getUnitSkill(uName)
                    newData.country = string.lower(country.name[unitData:getCountry()])
                    newData.units[unitNum].callsign = unitData:getCallsign()
                    newData.units[unitNum].unitName = uName
                end

				newData.units[unitNum].x = unitData:getPosition().p.x
				newData.units[unitNum].y = unitData:getPosition().p.z
                newData.units[unitNum].point = {x = newData.units[unitNum].x, y = newData.units[unitNum].y}
                newData.units[unitNum].heading = mist.getHeading(unitData, true) -- added to DBs
				newData.units[unitNum].alt = unitData:getPosition().p.y
                newData.units[unitNum].speed = mist.vec.mag(unitData:getVelocity())
               
			end

			return newData
		elseif StaticObject.getByName(gpName) and StaticObject.getByName(gpName):isExist() == true then
			local staticObj = StaticObject.getByName(gpName)
			dbData.units[1].x = staticObj:getPosition().p.x
			dbData.units[1].y = staticObj:getPosition().p.z
			dbData.units[1].alt = staticObj:getPosition().p.y
			dbData.units[1].heading = mist.getHeading(staticObj, true)

			return dbData
		end

	end

	function mist.getGroupData(gpName)
		local found = false
		local newData = {}
		if mist.DBs.groupsByName[gpName] then
			newData = mist.utils.deepCopy(mist.DBs.groupsByName[gpName])
			found = true
		end

		if found == false then
			for groupName, groupData in pairs(mist.DBs.groupsByName) do
				if mist.stringMatch(groupName, gpName) == true then
					newData = mist.utils.deepCopy(groupData)
					newData.groupName = groupName
					found = true
					break
				end
			end
		end

		local payloads
		if newData.category == 'plane' or newData.category == 'helicopter' then
			payloads = mist.getGroupPayload(newData.groupName)
		end
		if found == true then
			--newData.hidden = false -- maybe add this to DBs

			for unitNum, unitData in pairs(newData.units) do
				newData.units[unitNum] = {}

				newData.units[unitNum].unitId = unitData.unitId
				--newData.units[unitNum].point = unitData.point
				newData.units[unitNum].x = unitData.point.x
				newData.units[unitNum].y = unitData.point.y
				newData.units[unitNum].alt = unitData.alt
				newData.units[unitNum].alt_type = unitData.alt_type
				newData.units[unitNum].speed = unitData.speed
				newData.units[unitNum].type = unitData.type
				newData.units[unitNum].skill = unitData.skill
				newData.units[unitNum].unitName = unitData.unitName
				newData.units[unitNum].heading = unitData.heading -- added to DBs
				newData.units[unitNum].playerCanDrive = unitData.playerCanDrive -- added to DBs


				if newData.category == 'plane' or newData.category == 'helicopter' then
					newData.units[unitNum].payload = payloads[unitNum]
					newData.units[unitNum].livery_id = unitData.livery_id
					newData.units[unitNum].onboard_num = unitData.onboard_num
					newData.units[unitNum].callsign = unitData.callsign
					newData.units[unitNum].AddPropAircraft = unitData.AddPropAircraft
				end
				if newData.category == 'static' then
					newData.units[unitNum].categoryStatic = unitData.categoryStatic
					newData.units[unitNum].mass = unitData.mass
					newData.units[unitNum].canCargo = unitData.canCargo
					newData.units[unitNum].shape_name = unitData.shape_name
				end
			end
			--log:info(newData)
			return newData
		else
			log:error('$1 not found in MIST database', gpName)
			return
		end
	end

	function mist.getPayload(unitIdent)
		-- refactor to search by groupId and allow groupId and groupName as inputs
		local unitId = unitIdent
		if type(unitIdent) == 'string' and not tonumber(unitIdent) then
			if mist.DBs.MEunitsByName[unitIdent] then
				unitId = mist.DBs.MEunitsByName[unitIdent].unitId
			else
				log:error("Unit not found in mist.DBs.MEunitsByName: $1", unitIdent)
			end
		end
		local gpId = mist.DBs.MEunitsById[unitId].groupId

		if gpId and unitId then
			for coa_name, coa_data in pairs(env.mission.coalition) do
				if (coa_name == 'red' or coa_name == 'blue') and type(coa_data) == 'table' then
					if coa_data.country then --there is a country table
						for cntry_id, cntry_data in pairs(coa_data.country) do
							for obj_type_name, obj_type_data in pairs(cntry_data) do
								if obj_type_name == "helicopter" or obj_type_name == "ship" or obj_type_name == "plane" or obj_type_name == "vehicle" then	-- only these types have points
									if ((type(obj_type_data) == 'table') and obj_type_data.group and (type(obj_type_data.group) == 'table') and (#obj_type_data.group > 0)) then	--there's a group!
										for group_num, group_data in pairs(obj_type_data.group) do
											if group_data and group_data.groupId == gpId then
												for unitIndex, unitData in pairs(group_data.units) do --group index
													if unitData.unitId == unitId then
														return unitData.payload
													end
												end
											end
										end
									end
								end
							end
						end
					end
				end
			end
		else
			log:error('Need string or number. Got: $1', type(unitIdent))
			return false
		end
		log:warn("Couldn't find payload for unit: $1", unitIdent)
		return
	end

	function mist.getGroupPayload(groupIdent)
		local gpId = groupIdent
		if type(groupIdent) == 'string' and not tonumber(groupIdent) then
			if mist.DBs.MEgroupsByName[groupIdent] then
				gpId = mist.DBs.MEgroupsByName[groupIdent].groupId
			else
				log:error('$1 not found in mist.DBs.MEgroupsByName', groupIdent)
			end
		end

		if gpId then
			for coa_name, coa_data in pairs(env.mission.coalition) do
				if type(coa_data) == 'table' then
					if coa_data.country then --there is a country table
						for cntry_id, cntry_data in pairs(coa_data.country) do
							for obj_type_name, obj_type_data in pairs(cntry_data) do
								if obj_type_name == "helicopter" or obj_type_name == "ship" or obj_type_name == "plane" or obj_type_name == "vehicle" then	-- only these types have points
									if ((type(obj_type_data) == 'table') and obj_type_data.group and (type(obj_type_data.group) == 'table') and (#obj_type_data.group > 0)) then	--there's a group!
										for group_num, group_data in pairs(obj_type_data.group) do
											if group_data and group_data.groupId == gpId then
												local payloads = {}
												for unitIndex, unitData in pairs(group_data.units) do --group index
													payloads[unitIndex] = unitData.payload
												end
												return payloads
											end
										end
									end
								end
							end
						end
					end
				end
			end
		else
			log:error('Need string or number. Got: $1', type(groupIdent))
			return false
		end
		log:warn("Couldn't find payload for group: $1", groupIdent)
		return

	end
    
    function mist.getValidRandomPoint(vars)
    
    
    end

	function mist.teleportToPoint(vars) -- main teleport function that all of teleport/respawn functions call
		--log:info(vars)
        local point = vars.point
		local gpName
		if vars.gpName then
			gpName = vars.gpName
		elseif vars.groupName then
			gpName = vars.groupName
		else
			log:error('Missing field groupName or gpName in variable table')
		end

		local action = vars.action

		local disperse = vars.disperse or false
		local maxDisp = vars.maxDisp or 200
		local radius = vars.radius or 0
		local innerRadius = vars.innerRadius

		local route = vars.route
		local dbData = false

		local newGroupData
		if gpName and not vars.groupData then
			if string.lower(action) == 'teleport' or string.lower(action) == 'tele' then
				newGroupData = mist.getCurrentGroupData(gpName)
			elseif string.lower(action) == 'respawn' then
				newGroupData = mist.getGroupData(gpName)
				dbData = true
			elseif string.lower(action) == 'clone' then
				newGroupData = mist.getGroupData(gpName)
				newGroupData.clone = 'order66'
				dbData = true
			else
				action = 'tele'
				newGroupData = mist.getCurrentGroupData(gpName)
			end
		else
			action = 'tele'
			newGroupData = vars.groupData
		end
		
		--log:info('get Randomized Point')
		local diff = {x = 0, y = 0}
		local newCoord, origCoord 
        
        local validTerrain = {'LAND', 'ROAD', 'SHALLOW_WATER', 'WATER', 'RUNWAY'}
        if string.lower(newGroupData.category) == 'ship' then
            validTerrain = {'SHALLOW_WATER' , 'WATER'}
        elseif string.lower(newGroupData.category) == 'vehicle' then
            validTerrain = {'LAND', 'ROAD'}
        end
        local offsets = {}
		if point and radius >= 0 then
			local valid = false
            -- new thoughts
            --[[ Get AVG position of group and max radius distance to that avg point, otherwise use disperse data to get zone area to check
            if disperse then
            
            else
                
            end
            -- ]]
            
            
            

            

             ---- old
			for i = 1, 100	do
				newCoord = mist.getRandPointInCircle(point, radius, innerRadius)
				if mist.isTerrainValid(newCoord, validTerrain) then
					origCoord = mist.utils.deepCopy(newCoord)
					diff = {x = (newCoord.x - newGroupData.units[1].x), y = (newCoord.y - newGroupData.units[1].y)}
					valid = true
					break
				end
			end
			if valid == false then
				log:error('Point supplied in variable table is not a valid coordinate. Valid coords: $1', validTerrain)
				return false
			end
		end
		if not newGroupData.country and mist.DBs.groupsByName[newGroupData.groupName].country then
			newGroupData.country = mist.DBs.groupsByName[newGroupData.groupName].country
		end
		if not newGroupData.category and mist.DBs.groupsByName[newGroupData.groupName].category then
			newGroupData.category = mist.DBs.groupsByName[newGroupData.groupName].category
		end
        --log:info(point)
		for unitNum, unitData in pairs(newGroupData.units) do
			--log:info(unitNum)
            if disperse then
                local unitCoord 
                if maxDisp and type(maxDisp) == 'number' and unitNum ~= 1 then
					for i = 1, 100 do 
                        unitCoord = mist.getRandPointInCircle(origCoord, maxDisp)
                        if mist.isTerrainValid(unitCoord, validTerrain) == true then
                            --log:warn('Index: $1, Itered: $2. AT: $3', unitNum, i, unitCoord)
                            break
                        end                        
                    end
                    
					--else
					--newCoord = mist.getRandPointInCircle(zone.point, zone.radius)
				end
                if unitNum == 1 then
                    unitCoord = mist.utils.deepCopy(newCoord)
                end
                if unitCoord then 
                    newGroupData.units[unitNum].x = unitCoord.x
                    newGroupData.units[unitNum].y = unitCoord.y
                end
			else
				newGroupData.units[unitNum].x = unitData.x + diff.x
				newGroupData.units[unitNum].y = unitData.y + diff.y
			end
			if point then
				if (newGroupData.category == 'plane' or newGroupData.category == 'helicopter')	then
                    if point.z and point.y > 0 and point.y > land.getHeight({newGroupData.units[unitNum].x, newGroupData.units[unitNum].y}) + 10 then
						newGroupData.units[unitNum].alt = point.y
						--log:info('far enough from ground')
					else
						
						if newGroupData.category == 'plane' then
							--log:info('setNewAlt')
							newGroupData.units[unitNum].alt = land.getHeight({newGroupData.units[unitNum].x, newGroupData.units[unitNum].y}) + math.random(300, 9000)
						else
							newGroupData.units[unitNum].alt = land.getHeight({newGroupData.units[unitNum].x, newGroupData.units[unitNum].y}) + math.random(200, 3000)
						end
					end
				end
			end
		end

		if newGroupData.start_time then
			newGroupData.startTime = newGroupData.start_time
		end

		if newGroupData.startTime and newGroupData.startTime ~= 0 and dbData == true then
			local timeDif = timer.getAbsTime() - timer.getTime0()
			if timeDif > newGroupData.startTime then
				newGroupData.startTime = 0
			else
				newGroupData.startTime = newGroupData.startTime - timeDif
			end

		end

		if route then
			newGroupData.route = route
		end
		--log:info(newGroupData)
		--mist.debug.writeData(mist.utils.serialize,{'teleportToPoint', newGroupData}, 'newGroupData.lua')
		if string.lower(newGroupData.category) == 'static' then
			--log:info(newGroupData)
			return mist.dynAddStatic(newGroupData)
		end
		return mist.dynAdd(newGroupData)

	end

	function mist.respawnInZone(gpName, zone, disperse, maxDisp)

		if type(gpName) == 'table' and gpName:getName() then
			gpName = gpName:getName()
		elseif type(gpName) == 'table' and gpName[1]:getName() then
			gpName = math.random(#gpName)
		else
			gpName = tostring(gpName)
		end

		if type(zone) == 'string' then
			zone = trigger.misc.getZone(zone)
		elseif type(zone) == 'table' and not zone.radius then
			zone = trigger.misc.getZone(zone[math.random(1, #zone)])
		end
		local vars = {}
		vars.gpName = gpName
		vars.action = 'respawn'
		vars.point = zone.point
		vars.radius = zone.radius
		vars.disperse = disperse
		vars.maxDisp = maxDisp
		return mist.teleportToPoint(vars)
	end

	function mist.cloneInZone(gpName, zone, disperse, maxDisp)
		--log:info('cloneInZone')
		if type(gpName) == 'table' then
			gpName = gpName:getName()
		else
			gpName = tostring(gpName)
		end

		if type(zone) == 'string' then
			zone = trigger.misc.getZone(zone)
		elseif type(zone) == 'table' and not zone.radius then
			zone = trigger.misc.getZone(zone[math.random(1, #zone)])
		end
		local vars = {}
		vars.gpName = gpName
		vars.action = 'clone'
		vars.point = zone.point
		vars.radius = zone.radius
		vars.disperse = disperse
		vars.maxDisp = maxDisp
		--log:info('do teleport')
		return mist.teleportToPoint(vars)
	end

	function mist.teleportInZone(gpName, zone, disperse, maxDisp) -- groupName, zoneName or table of Zone Names, keepForm is a boolean
		if type(gpName) == 'table' and gpName:getName() then
			gpName = gpName:getName()
		else
			gpName = tostring(gpName)
		end

		if type(zone) == 'string' then
			zone = trigger.misc.getZone(zone)
		elseif type(zone) == 'table' and not zone.radius then
			zone = trigger.misc.getZone(zone[math.random(1, #zone)])
		end

		local vars = {}
		vars.gpName = gpName
		vars.action = 'tele'
		vars.point = zone.point
		vars.radius = zone.radius
		vars.disperse = disperse
		vars.maxDisp = maxDisp
		return mist.teleportToPoint(vars)
	end

	function mist.respawnGroup(gpName, task)
		local vars = {}
		vars.gpName = gpName
		vars.action = 'respawn'
		if task and type(task) ~= 'number' then
			vars.route = mist.getGroupRoute(gpName, 'task')
		end
		local newGroup = mist.teleportToPoint(vars)
		if task and type(task) == 'number' then
			local newRoute = mist.getGroupRoute(gpName, 'task')
			mist.scheduleFunction(mist.goRoute, {newGroup, newRoute}, timer.getTime() + task)
		end
		return newGroup
	end

	function mist.cloneGroup(gpName, task)
		local vars = {}
		vars.gpName = gpName
		vars.action = 'clone'
		if task and type(task) ~= 'number' then
			vars.route = mist.getGroupRoute(gpName, 'task')
		end
		local newGroup = mist.teleportToPoint(vars)
		if task and type(task) == 'number' then
			local newRoute = mist.getGroupRoute(gpName, 'task')
			mist.scheduleFunction(mist.goRoute, {newGroup, newRoute}, timer.getTime() + task)
		end
		return newGroup
	end

	function mist.teleportGroup(gpName, task)
		local vars = {}
		vars.gpName = gpName
		vars.action = 'teleport'
		if task and type(task) ~= 'number' then
			vars.route = mist.getGroupRoute(gpName, 'task')
		end
		local newGroup = mist.teleportToPoint(vars)
		if task and type(task) == 'number' then
			local newRoute = mist.getGroupRoute(gpName, 'task')
			mist.scheduleFunction(mist.goRoute, {newGroup, newRoute}, timer.getTime() + task)
		end
		return newGroup
	end

	function mist.spawnRandomizedGroup(groupName, vars) -- need to debug
		if Group.getByName(groupName) and Group.getByName(groupName):isExist() == true then
			local gpData = mist.getGroupData(groupName)
			gpData.units = mist.randomizeGroupOrder(gpData.units, vars)
			gpData.route = mist.getGroupRoute(groupName, 'task')

			mist.dynAdd(gpData)
		end

		return true
	end

	function mist.randomizeNumTable(vars)
		local newTable = {}

		local excludeIndex = {}
		local randomTable = {}

		if vars and vars.exclude and type(vars.exclude) == 'table' then
			for index, data in pairs(vars.exclude) do
				excludeIndex[data] = true
			end
		end

		local low, hi, size

		if vars.size then
			size = vars.size
		end

		if vars and vars.lowerLimit and type(vars.lowerLimit) == 'number' then
			low = mist.utils.round(vars.lowerLimit)
		else
			low = 1
		end

		if vars and vars.upperLimit and type(vars.upperLimit) == 'number' then
			hi = mist.utils.round(vars.upperLimit)
		else
			hi = size
		end

		local choices = {}
		-- add to exclude list and create list of what to randomize
		for i = 1, size do
			if not (i >= low and i <= hi) then

				excludeIndex[i] = true
			end
			if not excludeIndex[i] then
				table.insert(choices, i)
			else
				newTable[i] = i
			end
		end

		for ind, num in pairs(choices) do
			local found = false
			local x = 0
			while found == false do
				x = mist.random(size) -- get random number from list
				local addNew = true
				for index, _ in pairs(excludeIndex) do
					if index == x then
						addNew = false
						break
					end
				end
				if addNew == true then
					excludeIndex[x] = true
					found = true
				end
				excludeIndex[x] = true

			end
			newTable[num] = x
		end
		--[[
		for i = 1, #newTable do
			log:info(newTable[i])
		end
		]]
		return newTable
	end

	function mist.randomizeGroupOrder(passedUnits, vars)
		-- figure out what to exclude, and send data to other func
		local units = passedUnits

		if passedUnits.units then
			units = passUnits.units
		end

		local exclude = {}
		local excludeNum = {}
		if vars and vars.excludeType and type(vars.excludeType) == 'table' then
			exclude = vars.excludeType
		end

		if vars and vars.excludeNum and type(vars.excludeNum) == 'table' then
			excludeNum = vars.excludeNum
		end

		local low, hi

		if vars and vars.lowerLimit and type(vars.lowerLimit) == 'number' then
			low = mist.utils.round(vars.lowerLimit)
		else
			low = 1
		end

		if vars and vars.upperLimit and type(vars.upperLimit) == 'number' then
			hi = mist.utils.round(vars.upperLimit)
		else
			hi = #units
		end


		local excludeNum = {}
		for unitIndex, unitData in pairs(units) do
			if unitIndex >= low and unitIndex	<= hi then -- if within range
				local found = false
				if #exclude > 0 then
					for excludeType, index in pairs(exclude) do -- check if excluded
						if mist.stringMatch(excludeType, unitData.type) then -- if excluded
							excludeNum[unitIndex] = unitIndex
							found = true
						end
					end
				end
			else -- unitIndex is either to low, or to high: added to exclude list
				excludeNum[unitIndex] = unitId
			end
		end

		local newGroup = {}
		local newOrder = mist.randomizeNumTable({exclude = excludeNum, size = #units})

		for unitIndex, unitData in pairs(units) do
			for i = 1, #newOrder do
				if newOrder[i] == unitIndex then
					newGroup[i] = mist.utils.deepCopy(units[i]) -- gets all of the unit data
					newGroup[i].type = mist.utils.deepCopy(unitData.type)
					newGroup[i].skill = mist.utils.deepCopy(unitData.skill)
					newGroup[i].unitName = mist.utils.deepCopy(unitData.unitName)
					newGroup[i].unitIndex = mist.utils.deepCopy(unitData.unitIndex) -- replaces the units data with a new type
				end
			end
		end
		return newGroup
	end

	function mist.random(firstNum, secondNum) -- no support for decimals
		local lowNum, highNum
		if not secondNum then
			highNum = firstNum
			lowNum = 1
		else
			lowNum = firstNum
			highNum = secondNum
		end
		local total = 1
		if math.abs(highNum - lowNum + 1) < 50 then -- if total values is less than 50
			total = math.modf(50/math.abs(highNum - lowNum + 1)) -- make x copies required to be above 50
		end
		local choices = {}
		for i = 1, total do -- iterate required number of times
			for x = lowNum, highNum do -- iterate between the range
				choices[#choices +1] = x -- add each entry to a table
			end
		end
		local rtnVal = math.random(#choices) -- will now do a math.random of at least 50 choices
		for i = 1, 10 do
			rtnVal = math.random(#choices) -- iterate a few times for giggles
		end
		return choices[rtnVal]
	end

	function mist.stringMatch(s1, s2, bool)
		local exclude = {'%-', '%(', '%)', '%_', '%[', '%]', '%.', '%#', '% ', '%{', '%}', '%$', '%%', '%?', '%+', '%^'}
		if type(s1) == 'string' and type(s2) == 'string' then
			for i , str in pairs(exclude) do
				s1 = string.gsub(s1, str, '')
				s2 = string.gsub(s2, str, '')
			end
			if not bool then
				s1 = string.lower(s1)
				s2 = string.lower(s2)
			end
			--log:info('Comparing: $1 and $2', s1, s2)
			if s1 == s2 then
				return true
			else
				return false
			end
		else
			log:error('Either the first or second variable were not a string')
			return false
		end
	end

	mist.matchString = mist.stringMatch -- both commands work because order out type of I

	--[[ scope:
{
	units = {...},	-- unit names.
	coa = {...}, -- coa names
	countries = {...}, -- country names
	CA = {...}, -- looks just like coa.
	unitTypes = { red = {}, blue = {}, all = {}, Russia = {},}
}


scope examples:

{	units = { 'Hawg11', 'Hawg12' }, CA = {'blue'} }

{ countries = {'Georgia'}, unitTypes = {blue = {'A-10C', 'A-10A'}}}

{ coa = {'all'}}

{unitTypes = { blue = {'A-10C'}}}
]]
end

--- Utility functions.
-- E.g. conversions between units etc.
-- @section mist.utils
do -- mist.util scope
	mist.utils = {}

	--- Converts angle in radians to degrees.
	-- @param angle angle in radians
	-- @return angle in degrees
	function mist.utils.toDegree(angle)
		return angle*180/math.pi
	end

	--- Converts angle in degrees to radians.
	-- @param angle angle in degrees
	-- @return angle in degrees
	function mist.utils.toRadian(angle)
		return angle*math.pi/180
	end

	--- Converts meters to nautical miles.
	-- @param meters distance in meters
	-- @return distance in nautical miles
	function mist.utils.metersToNM(meters)
		return meters/1852
	end

	--- Converts meters to feet.
	-- @param meters distance in meters
	-- @return distance in feet
	function mist.utils.metersToFeet(meters)
		return meters/0.3048
	end

	--- Converts nautical miles to meters.
	-- @param nm distance in nautical miles
	-- @return distance in meters
	function mist.utils.NMToMeters(nm)
		return nm*1852
	end

	--- Converts feet to meters.
	-- @param feet distance in feet
	-- @return distance in meters
	function mist.utils.feetToMeters(feet)
		return feet*0.3048
	end

	--- Converts meters per second to knots.
	-- @param mps speed in m/s
	-- @return speed in knots
	function mist.utils.mpsToKnots(mps)
		return mps*3600/1852
	end

	--- Converts meters per second to kilometers per hour.
	-- @param mps speed in m/s
	-- @return speed in km/h
	function mist.utils.mpsToKmph(mps)
		return mps*3.6
	end

	--- Converts knots to meters per second.
	-- @param knots speed in knots
	-- @return speed in m/s
	function mist.utils.knotsToMps(knots)
		return knots*1852/3600
	end

	--- Converts kilometers per hour to meters per second.
	-- @param kmph speed in km/h
	-- @return speed in m/s
	function mist.utils.kmphToMps(kmph)
		return kmph/3.6
	end
	
	function mist.utils.kelvinToCelsius(t)
		return t - 273.15
	end
	
	function mist.utils.FahrenheitToCelsius(f)
		return (f - 32) * (5/9)
	end
	
	function mist.utils.celsiusToFahrenheit(c)
		return c*(9/5)+32
	end
	
	function mist.utils.converter(t1, t2, val)
		if type(t1) == 'string' then
			t1 = string.lower(t1)
		end
		if type(t2) == 'string' then
			t2 = string.lower(t2)
		end
		if val and type(val) ~= 'number' then
			if tonumber(val) then
				val = tonumber(val)
			else
				log:warn("Value given is not a number: $1", val)
				return 0
			end
		end
		
		-- speed
		if t1 == 'mps' then
			if t2 == 'kmph' then
				return val * 3.6
			elseif t2 == 'knots' or t2 == 'knot' then
				return val * 3600/1852
			end
		elseif t1 == 'kmph' then
			if t2 == 'mps' then
				return val/3.6
			elseif t2 == 'knots' or t2 == 'knot' then
				return  val*0.539957
			end
		elseif t1 == 'knot' or t1 == 'knots' then
			if t2 == 'kmph' then
				return val * 1.852
			elseif t2 == 'mps' then
				return  val * 0.514444	
			end
			
		-- Distance
		elseif t1 == 'feet' or t1 == 'ft' then
			if t2 == 'nm' then
				return val/6076.12
			elseif t2 == 'km' then
				return (val*0.3048)/1000
			elseif t2 == 'm' then
				return val*0.3048
			end
		elseif t1 == 'nm' then
			if t2 == 'feet' or t2 == 'ft' then
				return val*6076.12
			elseif t2 == 'km' then
				return val*1.852
			elseif t2 == 'm' then
				return val*1852
			end
		elseif t1 == 'km' then
			if t2 == 'nm' then
				return val/1.852
			elseif t2 == 'feet' or t2 == 'ft' then
				return	(val/0.3048)*1000
			elseif t2 == 'm' then
				return val*1000
			end
		elseif t1 == 'm' then
			if t2 == 'nm' then
				return val/1852
			elseif t2 == 'km' then
				return val/1000
			elseif t2 == 'feet' or t2 == 'ft' then
				return val/0.3048
			end
			
		-- Temperature
		elseif t1 == 'f' or t1 == 'fahrenheit' then
			if t2 == 'c' or t2 == 'celsius' then
				return (val - 32) * (5/9)
			elseif t2 == 'k' or t2 == 'kelvin' then
				return (val + 459.67) * (5/9)
			end
		elseif t1 == 'c' or t1 == 'celsius' then
			if t2 == 'f' or t2 == 'fahrenheit' then
				return val*(9/5)+32
			elseif t2 == 'k' or t2 == 'kelvin' then
				return val + 273.15
			end
		elseif t1 == 'k' or t1 == 'kelvin' then
			if t2 == 'c' or t2 == 'celsius' then
				return val - 273.15
			elseif t2 == 'f' or t2 == 'fahrenheit' then
				return ((val*(9/5))-459.67)
			end
		
		-- Pressure
		elseif t1 == 'p' or t1 == 'pascal' or t1 == 'pascals' then
			if t2 == 'hpa' or t2 == 'hectopascal' then
				return val/100
			elseif t2 == 'mmhg' then
				return val * 0.00750061561303
			elseif t2 == 'inhg' then
				return val * 0.0002953
			end
		elseif t1 == 'hpa' or t1 == 'hectopascal' then
			if t2 == 'p' or t2 == 'pascal' or t2 == 'pascals' then
				return val*100
			elseif t2 == 'mmhg' then
				return val * 0.00750061561303
			elseif t2 == 'inhg' then
				return val * 0.02953
			end
		elseif t1 == 'mmhg' then
			if t2 == 'p' or t2 == 'pascal' or t2 == 'pascals' then
				return  val / 0.00750061561303
			elseif t2 == 'hpa' or t2 == 'hectopascal' then
				return val * 1.33322
			elseif t2 == 'inhg' then
				return val/25.4
			end
		elseif t1 == 'inhg' then
			if t2 == 'p' or t2 == 'pascal' or t2 == 'pascals' then
				return val*3386.39
			elseif t2 == 'mmhg' then
				return val*25.4
			elseif t2 == 'hpa' or t2 == 'hectopascal' then
				return val * 33.8639
			end
		else
			log:warn("First value doesn't match with list. Value given: $1", t1)
		end
		log:warn("Match not found. Unable to convert: $1 into $2", t1, t2)
	
	end
	
	mist.converter = mist.utils.converter
	
	function mist.utils.getQFE(point, inchHg)
		
		local t, p = 0, 0
		if atmosphere.getTemperatureAndPressure then
			t, p = atmosphere.getTemperatureAndPressure(mist.utils.makeVec3GL(point))
		end
		if p == 0 then
			local h = land.getHeight(mist.utils.makeVec2(point))/0.3048 -- convert to feet
			if inchHg then
				return (env.mission.weather.qnh - (h/30)) * 0.0295299830714
			else
				return env.mission.weather.qnh - (h/30)
			end
		else 
			if inchHg then
				return mist.converter('p', 'inhg', p)
			else
				return mist.converter('p', 'hpa', p)
			end
		end

	end
	--- Converts a Vec3 to a Vec2.
	-- @tparam Vec3 vec the 3D vector
	-- @return vector converted to Vec2
	function mist.utils.makeVec2(vec)
		if vec.z then
			return {x = vec.x, y = vec.z}
		else
			return {x = vec.x, y = vec.y}	-- it was actually already vec2.
		end
	end

	--- Converts a Vec2 to a Vec3.
	-- @tparam Vec2 vec the 2D vector
	-- @param y optional new y axis (altitude) value. If omitted it's 0.
	function mist.utils.makeVec3(vec, y)
		if not vec.z then
			if vec.alt and not y then
				y = vec.alt
			elseif not y then
				y = 0
			end
			return {x = vec.x, y = y, z = vec.y}
		else
			return {x = vec.x, y = vec.y, z = vec.z}	-- it was already Vec3, actually.
		end
	end

	--- Converts a Vec2 to a Vec3 using ground level as altitude.
	-- The ground level at the specific point is used as altitude (y-axis)
	-- for the new vector. Optionally a offset can be specified.
	-- @tparam Vec2 vec the 2D vector
	-- @param[opt] offset offset to be applied to the ground level
	-- @return new 3D vector
	function mist.utils.makeVec3GL(vec, offset)
		local adj = offset or 0

		if not vec.z then
			return {x = vec.x, y = (land.getHeight(vec) + adj), z = vec.y}
		else
			return {x = vec.x, y = (land.getHeight({x = vec.x, y = vec.z}) + adj), z = vec.z}
		end
	end

	--- Returns the center of a zone as Vec3.
	-- @tparam string|table zone trigger zone name or table
	-- @treturn Vec3 center of the zone
	function mist.utils.zoneToVec3(zone)
		local new = {}
		if type(zone) == 'table' then
			if zone.point then
				new.x = zone.point.x
				new.y = zone.point.y
				new.z = zone.point.z
			elseif zone.x and zone.y and zone.z then
				return zone
			end
			return new
		elseif type(zone) == 'string' then
			zone = trigger.misc.getZone(zone)
			if zone then
				new.x = zone.point.x
				new.y = zone.point.y
				new.z = zone.point.z
				return new
			end
		end
	end

	--- Returns heading-error corrected direction.
	-- True-north corrected direction from point along vector vec.
	-- @tparam Vec3 vec
	-- @tparam Vec2 point
	-- @return heading-error corrected direction from point.
	function mist.utils.getDir(vec, point)
		local dir = math.atan2(vec.z, vec.x)
		if point then
			dir = dir + mist.getNorthCorrection(point)
		end
		if dir < 0 then
			dir = dir + 2 * math.pi	-- put dir in range of 0 to 2*pi
		end
		return dir
	end

	--- Returns distance in meters between two points.
	-- @tparam Vec2|Vec3 point1 first point
	-- @tparam Vec2|Vec3 point2 second point
	-- @treturn number distance between given points.
	function mist.utils.get2DDist(point1, point2)
		point1 = mist.utils.makeVec3(point1)
		point2 = mist.utils.makeVec3(point2)
		return mist.vec.mag({x = point1.x - point2.x, y = 0, z = point1.z - point2.z})
	end

	--- Returns distance in meters between two points in 3D space.
	-- @tparam Vec3 point1 first point
	-- @tparam Vec3 point2 second point
	-- @treturn number distancen between given points in 3D space.
	function mist.utils.get3DDist(point1, point2)
		return mist.vec.mag({x = point1.x - point2.x, y = point1.y - point2.y, z = point1.z - point2.z})
	end

	--- Creates a waypoint from a vector.
	-- @tparam Vec2|Vec3 vec position of the new waypoint
	-- @treturn Waypoint a new waypoint to be used inside paths.
	function mist.utils.vecToWP(vec)
		local newWP = {}
		newWP.x = vec.x
		newWP.y = vec.y
		if vec.z then
			newWP.alt = vec.y
			newWP.y = vec.z
		else
			newWP.alt = land.getHeight({x = vec.x, y = vec.y})
		end
		return newWP
	end

	--- Creates a waypoint from a unit.
	-- This function also considers the units speed.
	-- The alt_type of this waypoint is set to "BARO".
	-- @tparam Unit pUnit Unit whose position and speed will be used.
	-- @treturn Waypoint new waypoint.
	function mist.utils.unitToWP(pUnit)
		local unit = mist.utils.deepCopy(pUnit)
		if type(unit) == 'string' then
			if Unit.getByName(unit) then
				unit = Unit.getByName(unit)
			end
		end
		if unit:isExist() == true then
			local new = mist.utils.vecToWP(unit:getPosition().p)
			new.speed = mist.vec.mag(unit:getVelocity())
			new.alt_type = "BARO"

			return new
		end
		log:error("$1 not found or doesn't exist", pUnit)
		return false
	end

	--- Creates a deep copy of a object.
	-- Usually this object is a table.
	-- See also: from http://lua-users.org/wiki/CopyTable
	-- @param object object to copy
	-- @return copy of object
	function mist.utils.deepCopy(object)
		local lookup_table = {}
		local function _copy(object)
			if type(object) ~= "table" then
				return object
			elseif lookup_table[object] then
				return lookup_table[object]
			end
			local new_table = {}
			lookup_table[object] = new_table
			for index, value in pairs(object) do
				new_table[_copy(index)] = _copy(value)
			end
			return setmetatable(new_table, getmetatable(object))
		end
		return _copy(object)
	end

	--- Simple rounding function.
	-- From http://lua-users.org/wiki/SimpleRound
	-- use negative idp for rounding ahead of decimal place, positive for rounding after decimal place
	-- @tparam number num number to round
	-- @param idp
	function mist.utils.round(num, idp)
		local mult = 10^(idp or 0)
		return math.floor(num * mult + 0.5) / mult
	end

	--- Rounds all numbers inside a table.
	-- @tparam table tbl table in which to round numbers
	-- @param idp
	function mist.utils.roundTbl(tbl, idp)
		for id, val in pairs(tbl) do
			if type(val) == 'number' then
				tbl[id] = mist.utils.round(val, idp)
			end
		end
		return tbl
	end

	--- Executes the given string.
	-- borrowed from Slmod
	-- @tparam string s string containing LUA code.
	-- @treturn boolean true if successfully executed, false otherwise
	function mist.utils.dostring(s)
		local f, err = loadstring(s)
		if f then
			return true, f()
		else
			return false, err
		end
	end

	--- Checks a table's types.
	-- This function checks a tables types against a specifically forged type table.
	-- @param fname
	-- @tparam table type_tbl
	-- @tparam table var_tbl
	-- @usage -- specifically forged type table
	-- type_tbl = {
	--						 {'table', 'number'},
	--						 'string',
	--						 'number',
	--						 'number',
	--						 {'string','nil'},
	--						 {'number', 'nil'}
	--					 }
	-- -- my_tbl index 1 must be a table or a number;
	-- -- index 2, a string; index 3, a number;
	-- -- index 4, a number; index 5, either a string or nil;
	-- -- and index 6, either a number or nil.
	-- mist.utils.typeCheck(type_tbl, my_tb)
	-- @return true if table passes the check, false otherwise.
	function mist.utils.typeCheck(fname, type_tbl, var_tbl)
		-- log:info('type check')
		for type_key, type_val in pairs(type_tbl) do
			-- log:info('type_key: $1 type_val: $2', type_key, type_val)

			--type_key can be a table of accepted keys- so try to find one that is not nil
			local type_key_str = ''
			local act_key = type_key -- actual key within var_tbl - necessary to use for multiple possible key variables.	Initialize to type_key
			if type(type_key) == 'table' then

				for i = 1, #type_key do
					if i ~= 1 then
						type_key_str = type_key_str .. '/'
					end
					type_key_str = type_key_str .. tostring(type_key[i])
					if var_tbl[type_key[i]] ~= nil then
						act_key = type_key[i]	-- found a non-nil entry, make act_key now this val.
					end
				end
			else
				type_key_str = tostring(type_key)
			end

			local err_msg = 'Error in function ' .. fname .. ', parameter "' .. type_key_str .. '", expected: '
			local passed_check = false

			if type(type_tbl[type_key]) == 'table' then
				-- log:info('err_msg, before: $1', err_msg)
				for j = 1, #type_tbl[type_key] do

					if j == 1 then
						err_msg = err_msg .. type_tbl[type_key][j]
					else
						err_msg = err_msg .. ' or ' .. type_tbl[type_key][j]
					end

					if type(var_tbl[act_key]) == type_tbl[type_key][j] then
						passed_check = true
					end
				end
				-- log:info('err_msg, after: $1', err_msg)
			else
				-- log:info('err_msg, before: $1', err_msg)
				err_msg = err_msg .. type_tbl[type_key]
				-- log:info('err_msg, after: $1', err_msg)
				if type(var_tbl[act_key]) == type_tbl[type_key] then
					passed_check = true
				end

			end

			if not passed_check then
				err_msg = err_msg .. ', got ' .. type(var_tbl[act_key])
				return false, err_msg
			end
		end
		return true
	end

	--- Serializes the give variable to a string.
	-- borrowed from slmod
	-- @param var variable to serialize
	-- @treturn string variable serialized to string
	function mist.utils.basicSerialize(var)
		if var == nil then
			return "\"\""
		else
			if ((type(var) == 'number') or
					(type(var) == 'boolean') or
					(type(var) == 'function') or
					(type(var) == 'table') or
					(type(var) == 'userdata') ) then
			return tostring(var)
		elseif type(var) == 'string' then
			var = string.format('%q', var)
			return var
		end
	end
end

--- Serialize value
-- borrowed from slmod (serialize_slmod)
-- @param name
-- @param value value to serialize
-- @param level
function mist.utils.serialize(name, value, level)
	--Based on ED's serialize_simple2
	local function basicSerialize(o)
		if type(o) == "number" then
			return tostring(o)
		elseif type(o) == "boolean" then
			return tostring(o)
		else -- assume it is a string
			return mist.utils.basicSerialize(o)
		end
	end

	local function serializeToTbl(name, value, level)
		local var_str_tbl = {}
		if level == nil then
			level = ""
		end
		if level ~= "" then 
			level = level.."" 
		end
		table.insert(var_str_tbl, level .. name .. " = ")

		if type(value) == "number" or type(value) == "string" or type(value) == "boolean" then
			table.insert(var_str_tbl, basicSerialize(value) ..	",\n")
		elseif type(value) == "table" then
			table.insert(var_str_tbl, "\n"..level.."{\n")

			for k,v in pairs(value) do -- serialize its fields
				local key
				if type(k) == "number" then
					key = string.format("[%s]", k)
				else
					key = string.format("[%q]", k)
				end
				table.insert(var_str_tbl, mist.utils.serialize(key, v, level.."	"))

			end
			if level == "" then
				table.insert(var_str_tbl, level.."} -- end of "..name.."\n")

			else
				table.insert(var_str_tbl, level.."}, -- end of "..name.."\n")

			end
		else
			log:error('Cannot serialize a $1', type(value))
		end
		return var_str_tbl
	end

	local t_str = serializeToTbl(name, value, level)

	return table.concat(t_str)
end

--- Serialize value supporting cycles.
-- borrowed from slmod (serialize_wcycles)
-- @param name
-- @param value value to serialize
-- @param saved
function mist.utils.serializeWithCycles(name, value, saved)
	--mostly straight out of Programming in Lua
	local function basicSerialize(o)
		if type(o) == "number" then
			return tostring(o)
		elseif type(o) == "boolean" then
			return tostring(o)
		else -- assume it is a string
			return mist.utils.basicSerialize(o)
		end
	end

	local t_str = {}
	saved = saved or {}			 -- initial value
	if ((type(value) == 'string') or (type(value) == 'number') or (type(value) == 'table') or (type(value) == 'boolean')) then
		table.insert(t_str, name .. " = ")
		if type(value) == "number" or type(value) == "string" or type(value) == "boolean" then
			table.insert(t_str, basicSerialize(value) ..	"\n")
		else

			if saved[value] then		-- value already saved?
				table.insert(t_str, saved[value] .. "\n")
			else
				saved[value] = name	 -- save name for next time
				table.insert(t_str, "{}\n")
				for k,v in pairs(value) do			-- save its fields
					local fieldname = string.format("%s[%s]", name, basicSerialize(k))
					table.insert(t_str, mist.utils.serializeWithCycles(fieldname, v, saved))
				end
			end
		end
		return table.concat(t_str)
	else
		return ""
	end
end

--- Serialize a table to a single line string.
-- serialization of a table all on a single line, no comments, made to replace old get_table_string function
-- borrowed from slmod
-- @tparam table tbl table to serialize.
-- @treturn string string containing serialized table
function mist.utils.oneLineSerialize(tbl)
	if type(tbl) == 'table' then --function only works for tables!

		local tbl_str = {}

		tbl_str[#tbl_str + 1] = '{ '

		for ind,val in pairs(tbl) do -- serialize its fields
			if type(ind) == "number" then
				tbl_str[#tbl_str + 1] = '['
				tbl_str[#tbl_str + 1] = tostring(ind)
				tbl_str[#tbl_str + 1] = '] = '
			else --must be a string
				tbl_str[#tbl_str + 1] = '['
				tbl_str[#tbl_str + 1] = mist.utils.basicSerialize(ind)
				tbl_str[#tbl_str + 1] = '] = '
			end

			if ((type(val) == 'number') or (type(val) == 'boolean')) then
				tbl_str[#tbl_str + 1] = tostring(val)
				tbl_str[#tbl_str + 1] = ', '
			elseif type(val) == 'string' then
				tbl_str[#tbl_str + 1] = mist.utils.basicSerialize(val)
				tbl_str[#tbl_str + 1] = ', '
			elseif type(val) == 'nil' then -- won't ever happen, right?
				tbl_str[#tbl_str + 1] = 'nil, '
			elseif type(val) == 'table' then
				tbl_str[#tbl_str + 1] = mist.utils.oneLineSerialize(val)
				tbl_str[#tbl_str + 1] = ', '	 --I think this is right, I just added it
			else
				log:warn('Unable to serialize value type $1 at index $2', mist.utils.basicSerialize(type(val)), tostring(ind))
			end

		end
		tbl_str[#tbl_str + 1] = '}'
		return table.concat(tbl_str)
    else
        return  mist.utils.basicSerialize(tbl)
	end
end

--- Returns table in a easy readable string representation.
-- this function is not meant for serialization because it uses
-- newlines for better readability.
-- @param tbl table to show
-- @param loc
-- @param indent
-- @param tableshow_tbls
-- @return human readable string representation of given table
function mist.utils.tableShow(tbl, loc, indent, tableshow_tbls) --based on serialize_slmod, this is a _G serialization
	tableshow_tbls = tableshow_tbls or {} --create table of tables
	loc = loc or ""
	indent = indent or ""
	if type(tbl) == 'table' then --function only works for tables!
		tableshow_tbls[tbl] = loc

		local tbl_str = {}

		tbl_str[#tbl_str + 1] = indent .. '{\n'

		for ind,val in pairs(tbl) do -- serialize its fields
			if type(ind) == "number" then
				tbl_str[#tbl_str + 1] = indent
				tbl_str[#tbl_str + 1] = loc .. '['
				tbl_str[#tbl_str + 1] = tostring(ind)
				tbl_str[#tbl_str + 1] = '] = '
			else
				tbl_str[#tbl_str + 1] = indent
				tbl_str[#tbl_str + 1] = loc .. '['
				tbl_str[#tbl_str + 1] = mist.utils.basicSerialize(ind)
				tbl_str[#tbl_str + 1] = '] = '
			end

			if ((type(val) == 'number') or (type(val) == 'boolean')) then
				tbl_str[#tbl_str + 1] = tostring(val)
				tbl_str[#tbl_str + 1] = ',\n'
			elseif type(val) == 'string' then
				tbl_str[#tbl_str + 1] = mist.utils.basicSerialize(val)
				tbl_str[#tbl_str + 1] = ',\n'
			elseif type(val) == 'nil' then -- won't ever happen, right?
				tbl_str[#tbl_str + 1] = 'nil,\n'
			elseif type(val) == 'table' then
				if tableshow_tbls[val] then
					tbl_str[#tbl_str + 1] = tostring(val) .. ' already defined: ' .. tableshow_tbls[val] .. ',\n'
				else
					tableshow_tbls[val] = loc ..	'[' .. mist.utils.basicSerialize(ind) .. ']'
					tbl_str[#tbl_str + 1] = tostring(val) .. ' '
					tbl_str[#tbl_str + 1] = mist.utils.tableShow(val,	loc .. '[' .. mist.utils.basicSerialize(ind).. ']', indent .. '    ', tableshow_tbls)
					tbl_str[#tbl_str + 1] = ',\n'
				end
			elseif type(val) == 'function' then
				if debug and debug.getinfo then
					local fcnname = tostring(val)
					local info = debug.getinfo(val, "S")
					if info.what == "C" then
						tbl_str[#tbl_str + 1] = string.format('%q', fcnname .. ', C function') .. ',\n'
					else
						if (string.sub(info.source, 1, 2) == [[./]]) then
							tbl_str[#tbl_str + 1] = string.format('%q', fcnname .. ', defined in (' .. info.linedefined .. '-' .. info.lastlinedefined .. ')' .. info.source) ..',\n'
						else
							tbl_str[#tbl_str + 1] = string.format('%q', fcnname .. ', defined in (' .. info.linedefined .. '-' .. info.lastlinedefined .. ')') ..',\n'
						end
					end

				else
					tbl_str[#tbl_str + 1] = 'a function,\n'
				end
			else
				tbl_str[#tbl_str + 1] = 'unable to serialize value type ' .. mist.utils.basicSerialize(type(val)) .. ' at index ' .. tostring(ind)
			end
		end

		tbl_str[#tbl_str + 1] = indent .. '}'
		return table.concat(tbl_str)
	end
end
end

--- Debug functions
-- @section mist.debug
do -- mist.debug scope
	mist.debug = {}

	--- Dumps the global table _G.
	-- This dumps the global table _G to a file in
	-- the DCS\Logs directory.
	-- This function requires you to disable script sanitization
	-- in $DCS_ROOT\Scripts\MissionScripting.lua to access lfs and io
	-- libraries.
	-- @param fname
	function mist.debug.dump_G(fname)
		if lfs and io then
			local fdir = lfs.writedir() .. [[Logs\]] .. fname
			local f = io.open(fdir, 'w')
			f:write(mist.utils.tableShow(_G))
			f:close()
			log:info('Wrote debug data to $1', fdir)
			--trigger.action.outText(errmsg, 10)
		else
			log:alert('insufficient libraries to run mist.debug.dump_G, you must disable the sanitization of the io and lfs libraries in ./Scripts/MissionScripting.lua')
			--trigger.action.outText(errmsg, 10)
		end
	end

	--- Write debug data to file.
	-- This function requires you to disable script sanitization
	-- in $DCS_ROOT\Scripts\MissionScripting.lua to access lfs and io
	-- libraries.
	-- @param fcn
	-- @param fcnVars
	-- @param fname
	function mist.debug.writeData(fcn, fcnVars, fname)
		if lfs and io then
			local fdir = lfs.writedir() .. [[Logs\]] .. fname
			local f = io.open(fdir, 'w')
			f:write(fcn(unpack(fcnVars, 1, table.maxn(fcnVars))))
			f:close()
			log:info('Wrote debug data to $1', fdir)
			local errmsg = 'mist.debug.writeData wrote data to ' .. fdir
			trigger.action.outText(errmsg, 10)
		else
			local errmsg = 'Error: insufficient libraries to run mist.debug.writeData, you must disable the sanitization of the io and lfs libraries in ./Scripts/MissionScripting.lua'
			log:alert(errmsg)
			trigger.action.outText(errmsg, 10)
		end
	end

	--- Write mist databases to file.
	-- This function requires you to disable script sanitization
	-- in $DCS_ROOT\Scripts\MissionScripting.lua to access lfs and io
	-- libraries.
	function mist.debug.dumpDBs()
		for DBname, DB in pairs(mist.DBs) do
			if type(DB) == 'table' and type(DBname) == 'string' then
				mist.debug.writeData(mist.utils.serialize, {DBname, DB}, 'mist_DBs_' .. DBname .. '.lua')
			end
		end
	end
end

--- 3D Vector functions
-- @section mist.vec
do -- mist.vec scope
	mist.vec = {}

	--- Vector addition.
	-- @tparam Vec3 vec1 first vector
	-- @tparam Vec3 vec2 second vector
	-- @treturn Vec3 new vector, sum of vec1 and vec2.
	function mist.vec.add(vec1, vec2)
		return {x = vec1.x + vec2.x, y = vec1.y + vec2.y, z = vec1.z + vec2.z}
	end

	--- Vector substraction.
	-- @tparam Vec3 vec1 first vector
	-- @tparam Vec3 vec2 second vector
	-- @treturn Vec3 new vector, vec2 substracted from vec1.
	function mist.vec.sub(vec1, vec2)
		return {x = vec1.x - vec2.x, y = vec1.y - vec2.y, z = vec1.z - vec2.z}
	end

	--- Vector scalar multiplication.
	-- @tparam Vec3 vec vector to multiply
	-- @tparam number mult scalar multiplicator
	-- @treturn Vec3 new vector multiplied with the given scalar
	function mist.vec.scalarMult(vec, mult)
		return {x = vec.x*mult, y = vec.y*mult, z = vec.z*mult}
	end

	mist.vec.scalar_mult = mist.vec.scalarMult

	--- Vector dot product.
	-- @tparam Vec3 vec1 first vector
	-- @tparam Vec3 vec2 second vector
	-- @treturn number dot product of given vectors
	function mist.vec.dp (vec1, vec2)
		return vec1.x*vec2.x + vec1.y*vec2.y + vec1.z*vec2.z
	end

	--- Vector cross product.
	-- @tparam Vec3 vec1 first vector
	-- @tparam Vec3 vec2 second vector
	-- @treturn Vec3 new vector, cross product of vec1 and vec2.
	function mist.vec.cp(vec1, vec2)
		return { x = vec1.y*vec2.z - vec1.z*vec2.y, y = vec1.z*vec2.x - vec1.x*vec2.z, z = vec1.x*vec2.y - vec1.y*vec2.x}
	end

	--- Vector magnitude
	-- @tparam Vec3 vec vector
	-- @treturn number magnitude of vector vec
	function mist.vec.mag(vec)
		return (vec.x^2 + vec.y^2 + vec.z^2)^0.5
	end

	--- Unit vector
	-- @tparam Vec3 vec
	-- @treturn Vec3 unit vector of vec
	function mist.vec.getUnitVec(vec)
		local mag = mist.vec.mag(vec)
		return { x = vec.x/mag, y = vec.y/mag, z = vec.z/mag }
	end

	--- Rotate vector.
	-- @tparam Vec2 vec2 to rotoate
	-- @tparam number theta
	-- @return Vec2 rotated vector.
	function mist.vec.rotateVec2(vec2, theta)
		return { x = vec2.x*math.cos(theta) - vec2.y*math.sin(theta), y = vec2.x*math.sin(theta) + vec2.y*math.cos(theta)}
	end
end

--- Flag functions.
-- The mist "Flag functions" are functions that are similar to Slmod functions
-- that detect a game condition and set a flag when that game condition is met.
--
-- They are intended to be used by persons with little or no experience in Lua
-- programming, but with a good knowledge of the DCS mission editor.
-- @section mist.flagFunc
do -- mist.flagFunc scope
	mist.flagFunc = {}

	--- Sets a flag if map objects are destroyed inside a zone.
	-- Once this function is run, it will start a continuously evaluated process
	-- that will set a flag true if map objects (such as bridges, buildings in
	-- town, etc.) die (or have died) in a mission editor zone (or set of zones).
	-- This will only happen once; once the flag is set true, the process ends.
	-- @usage
	-- -- Example vars table
	-- vars = {
	--	 zones = { "zone1", "zone2" }, -- can also be a single string
	--	 flag = 3, -- number of the flag
	--	 stopflag = 4, -- optional number of the stop flag
	--	 req_num = 10, -- optional minimum amount of map objects needed to die
	-- }
	-- mist.flagFuncs.mapobjs_dead_zones(vars)
	-- @tparam table vars table containing parameters.
	function mist.flagFunc.mapobjs_dead_zones(vars)
		--[[vars needs to be:
zones = table or string,
flag = number,
stopflag = number or nil,
req_num = number or nil

AND used by function,
initial_number

]]
		-- type_tbl
		local type_tbl = {
			[{'zones', 'zone'}] = {'table', 'string'},
			flag = {'number', 'string'},
			[{'stopflag', 'stopFlag'}] = {'number', 'string', 'nil'},
			[{'req_num', 'reqnum'}] = {'number', 'nil'},
		}

		local err, errmsg = mist.utils.typeCheck('mist.flagFunc.mapobjs_dead_zones', type_tbl, vars)
		assert(err, errmsg)
		local zones = vars.zones or vars.zone
		local flag = vars.flag
		local stopflag = vars.stopflag or vars.stopFlag or -1
		local req_num = vars.req_num or vars.reqnum or 1
		local initial_number = vars.initial_number

		if type(zones) == 'string' then
			zones = {zones}
		end

		if not initial_number then
			initial_number = #mist.getDeadMapObjsInZones(zones)
		end

		if stopflag == -1 or (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == false) then
			if (#mist.getDeadMapObjsInZones(zones) - initial_number) >= req_num and trigger.misc.getUserFlag(flag) == 0 then
				trigger.action.setUserFlag(flag, true)
				return
			else
				mist.scheduleFunction(mist.flagFunc.mapobjs_dead_zones, {{zones = zones, flag = flag, stopflag = stopflag, req_num = req_num, initial_number = initial_number}}, timer.getTime() + 1)
			end
		end
	end

	--- Sets a flag if map objects are destroyed inside a polygon.
	-- Once this function is run, it will start a continuously evaluated process
	-- that will set a flag true if map objects (such as bridges, buildings in
	-- town, etc.) die (or have died) in a polygon.
	-- This will only happen once; once the flag is set true, the process ends.
	-- @usage
	-- -- Example vars table
	-- vars = {
	--	 zone = {
	--		 [1] = mist.DBs.unitsByName['NE corner'].point,
	--		 [2] = mist.DBs.unitsByName['SE corner'].point,
	--		 [3] = mist.DBs.unitsByName['SW corner'].point,
	--		 [4] = mist.DBs.unitsByName['NW corner'].point
	--	 }
	--	 flag = 3, -- number of the flag
	--	 stopflag = 4, -- optional number of the stop flag
	--	 req_num = 10, -- optional minimum amount of map objects needed to die
	-- }
	-- mist.flagFuncs.mapobjs_dead_zones(vars)
	-- @tparam table vars table containing parameters.
	function mist.flagFunc.mapobjs_dead_polygon(vars)
		--[[vars needs to be:
zone = table,
flag = number,
stopflag = number or nil,
req_num = number or nil

AND used by function,
initial_number

]]
		-- type_tbl
		local type_tbl = {
			[{'zone', 'polyzone'}] = 'table',
			flag = {'number', 'string'},
			[{'stopflag', 'stopFlag'}] = {'number', 'string', 'nil'},
			[{'req_num', 'reqnum'}] = {'number', 'nil'},
		}

		local err, errmsg = mist.utils.typeCheck('mist.flagFunc.mapobjs_dead_polygon', type_tbl, vars)
		assert(err, errmsg)
		local zone = vars.zone or vars.polyzone
		local flag = vars.flag
		local stopflag = vars.stopflag or vars.stopFlag or -1
		local req_num = vars.req_num or vars.reqnum or 1
		local initial_number = vars.initial_number

		if not initial_number then
			initial_number = #mist.getDeadMapObjsInPolygonZone(zone)
		end

		if stopflag == -1 or (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == false) then
			if (#mist.getDeadMapObjsInPolygonZone(zone) - initial_number) >= req_num and trigger.misc.getUserFlag(flag) == 0 then
				trigger.action.setUserFlag(flag, true)
				return
			else
				mist.scheduleFunction(mist.flagFunc.mapobjs_dead_polygon, {{zone = zone, flag = flag, stopflag = stopflag, req_num = req_num, initial_number = initial_number}}, timer.getTime() + 1)
			end
		end
	end

	--- Sets a flag if unit(s) is/are inside a polygon.
	-- @tparam table vars @{unitsInPolygonVars}
	-- @usage -- set flag 11 to true as soon as any blue vehicles
	-- -- are inside the polygon shape created off of the waypoints
	-- -- of the group forest1
	-- mist.flagFunc.units_in_polygon {
	--		units = {'[blue][vehicle]'},
	--		zone = mist.getGroupPoints('forest1'),
	--		flag = 11
	-- }
	function mist.flagFunc.units_in_polygon(vars)
		--[[vars needs to be:
units = table,
zone = table,
flag = number,
stopflag = number or nil,
maxalt = number or nil,
interval	= number or nil,
req_num = number or nil
toggle = boolean or nil
unitTableDef = table or nil
]]
		-- type_tbl
		local type_tbl = {
			[{'units', 'unit'}] = 'table',
			[{'zone', 'polyzone'}] = 'table',
			flag = {'number', 'string'},
			[{'stopflag', 'stopFlag'}] = {'number', 'string', 'nil'},
			[{'maxalt', 'alt'}] = {'number', 'nil'},
			interval = {'number', 'nil'},
			[{'req_num', 'reqnum'}] = {'number', 'nil'},
			toggle = {'boolean', 'nil'},
			unitTableDef = {'table', 'nil'},
		}

		local err, errmsg = mist.utils.typeCheck('mist.flagFunc.units_in_polygon', type_tbl, vars)
		assert(err, errmsg)
		local units = vars.units or vars.unit
		local zone = vars.zone or vars.polyzone
		local flag = vars.flag
		local stopflag = vars.stopflag or vars.stopFlag or -1
		local interval = vars.interval or 1
		local maxalt = vars.maxalt or vars.alt
		local req_num = vars.req_num or vars.reqnum or 1
		local toggle = vars.toggle or nil
		local unitTableDef = vars.unitTableDef

		if not units.processed then
			unitTableDef = mist.utils.deepCopy(units)
		end

		if (units.processed and units.processed < mist.getLastDBUpdateTime()) or not units.processed then -- run unit table short cuts
			if unitTableDef then
				units = mist.makeUnitTable(unitTableDef)
			end
		end

		if stopflag == -1 or (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == 0) then
			local num_in_zone = 0
			for i = 1, #units do
				local unit = Unit.getByName(units[i])
				if unit then
					local pos = unit:getPosition().p
					if mist.pointInPolygon(pos, zone, maxalt) then
						num_in_zone = num_in_zone + 1
						if num_in_zone >= req_num and trigger.misc.getUserFlag(flag) == 0 then
							trigger.action.setUserFlag(flag, true)
							break
						end
					end
				end
			end
			if toggle and (num_in_zone < req_num) and trigger.misc.getUserFlag(flag) > 0 then
				trigger.action.setUserFlag(flag, false)
			end
			-- do another check in case stopflag was set true by this function
			if (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == 0) then
				mist.scheduleFunction(mist.flagFunc.units_in_polygon, {{units = units, zone = zone, flag = flag, stopflag = stopflag, interval = interval, req_num = req_num, maxalt = maxalt, toggle = toggle, unitTableDef = unitTableDef}}, timer.getTime() + interval)
			end
		end

	end

	--- Sets a flag if unit(s) is/are inside a trigger zone.
	-- @todo document
	function mist.flagFunc.units_in_zones(vars)
		--[[vars needs to be:
	units = table,
	zones = table,
	flag = number,
	stopflag = number or nil,
	zone_type = string or nil,
	req_num = number or nil,
	interval	= number or nil
	toggle = boolean or nil
	]]
		-- type_tbl
		local type_tbl = {
			units = 'table',
			zones = 'table',
			flag = {'number', 'string'},
			[{'stopflag', 'stopFlag'}] = {'number', 'string', 'nil'},
			[{'zone_type', 'zonetype'}] = {'string', 'nil'},
			[{'req_num', 'reqnum'}] = {'number', 'nil'},
			interval = {'number', 'nil'},
			toggle = {'boolean', 'nil'},
			unitTableDef = {'table', 'nil'},
		}

		local err, errmsg = mist.utils.typeCheck('mist.flagFunc.units_in_zones', type_tbl, vars)
		assert(err, errmsg)
		local units = vars.units
		local zones = vars.zones
		local flag = vars.flag
		local stopflag = vars.stopflag or vars.stopFlag or -1
		local zone_type = vars.zone_type or vars.zonetype or 'cylinder'
		local req_num = vars.req_num or vars.reqnum or 1
		local interval = vars.interval or 1
		local toggle = vars.toggle or nil
		local unitTableDef = vars.unitTableDef

		if not units.processed then
			unitTableDef = mist.utils.deepCopy(units)
		end
		
		if (units.processed and units.processed < mist.getLastDBUpdateTime()) or not units.processed then -- run unit table short cuts
			if unitTableDef then
				units = mist.makeUnitTable(unitTableDef)
			end
		end

		if stopflag == -1 or (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == false) then

			local in_zone_units = mist.getUnitsInZones(units, zones, zone_type)

			if #in_zone_units >= req_num and trigger.misc.getUserFlag(flag) == 0 then
				trigger.action.setUserFlag(flag, true)
			elseif #in_zone_units < req_num and toggle then
				trigger.action.setUserFlag(flag, false)
			end
			-- do another check in case stopflag was set true by this function
			if (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == false) then
				mist.scheduleFunction(mist.flagFunc.units_in_zones, {{units = units, zones = zones, flag = flag, stopflag = stopflag, zone_type = zone_type, req_num = req_num, interval = interval, toggle = toggle, unitTableDef = unitTableDef}}, timer.getTime() + interval)
			end
		end

	end

	--- Sets a flag if unit(s) is/are inside a moving zone.
	-- @todo document
	function mist.flagFunc.units_in_moving_zones(vars)
		--[[vars needs to be:
	units = table,
	zone_units = table,
	radius = number,
	flag = number,
	stopflag = number or nil,
	zone_type = string or nil,
	req_num = number or nil,
	interval	= number or nil
	toggle = boolean or nil
	]]
		-- type_tbl
		local type_tbl = {
			units = 'table',
			[{'zone_units', 'zoneunits'}]	= 'table',
			radius = 'number',
			flag = {'number', 'string'},
			[{'stopflag', 'stopFlag'}] = {'number', 'string', 'nil'},
			[{'zone_type', 'zonetype'}] = {'string', 'nil'},
			[{'req_num', 'reqnum'}] = {'number', 'nil'},
			interval = {'number', 'nil'},
			toggle = {'boolean', 'nil'},
			unitTableDef = {'table', 'nil'},
			zUnitTableDef = {'table', 'nil'},
		}

		local err, errmsg = mist.utils.typeCheck('mist.flagFunc.units_in_moving_zones', type_tbl, vars)
		assert(err, errmsg)
		local units = vars.units
		local zone_units = vars.zone_units or vars.zoneunits
		local radius = vars.radius
		local flag = vars.flag
		local stopflag = vars.stopflag or vars.stopFlag or -1
		local zone_type = vars.zone_type or vars.zonetype or 'cylinder'
		local req_num = vars.req_num or vars.reqnum or 1
		local interval = vars.interval or 1
		local toggle = vars.toggle or nil
		local unitTableDef = vars.unitTableDef
		local zUnitTableDef = vars.zUnitTableDef

		if not units.processed then
			unitTableDef = mist.utils.deepCopy(units)
		end

		if not zone_units.processed then
			zUnitTableDef = mist.utils.deepCopy(zone_units)
		end

		if (units.processed and units.processed < mist.getLastDBUpdateTime()) or not units.processed then -- run unit table short cuts
			if unitTableDef then
				units = mist.makeUnitTable(unitTableDef)
			end
		end

		if (zone_units.processed and zone_units.processed < mist.getLastDBUpdateTime()) or not zone_units.processed then -- run unit table short cuts
			if zUnitTableDef then
				zone_units = mist.makeUnitTable(zUnitTableDef)
			end
			
		end

		if stopflag == -1 or (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == false) then

			local in_zone_units = mist.getUnitsInMovingZones(units, zone_units, radius, zone_type)

			if #in_zone_units >= req_num and trigger.misc.getUserFlag(flag) == 0 then
				trigger.action.setUserFlag(flag, true)
			elseif #in_zone_units < req_num and toggle then
				trigger.action.setUserFlag(flag, false)
			end
			-- do another check in case stopflag was set true by this function
			if (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == false) then
				mist.scheduleFunction(mist.flagFunc.units_in_moving_zones, {{units = units, zone_units = zone_units, radius = radius, flag = flag, stopflag = stopflag, zone_type = zone_type, req_num = req_num, interval = interval, toggle = toggle, unitTableDef = unitTableDef, zUnitTableDef = zUnitTableDef}}, timer.getTime() + interval)
			end
		end

	end

	--- Sets a flag if units have line of sight to each other.
	-- @todo document
	function mist.flagFunc.units_LOS(vars)
		--[[vars needs to be:
unitset1 = table,
altoffset1 = number,
unitset2 = table,
altoffset2 = number,
flag = number,
stopflag = number or nil,
radius = number or nil,
interval	= number or nil,
req_num = number or nil
toggle = boolean or nil
]]
		-- type_tbl
		local type_tbl = {
			[{'unitset1', 'units1'}] = 'table',
			[{'altoffset1', 'alt1'}] = 'number',
			[{'unitset2', 'units2'}] = 'table',
			[{'altoffset2', 'alt2'}] = 'number',
			flag = {'number', 'string'},
			[{'stopflag', 'stopFlag'}] = {'number', 'string', 'nil'},
			[{'req_num', 'reqnum'}] = {'number', 'nil'},
			interval = {'number', 'nil'},
			radius = {'number', 'nil'},
			toggle = {'boolean', 'nil'},
			unitTableDef1 = {'table', 'nil'},
			unitTableDef2 = {'table', 'nil'},
		}

		local err, errmsg = mist.utils.typeCheck('mist.flagFunc.units_LOS', type_tbl, vars)
		assert(err, errmsg)
		local unitset1 = vars.unitset1 or vars.units1
		local altoffset1 = vars.altoffset1 or vars.alt1
		local unitset2 = vars.unitset2 or vars.units2
		local altoffset2 = vars.altoffset2 or vars.alt2
		local flag = vars.flag
		local stopflag = vars.stopflag or vars.stopFlag or -1
		local interval = vars.interval or 1
		local radius = vars.radius or math.huge
		local req_num = vars.req_num or vars.reqnum or 1
		local toggle = vars.toggle or nil
		local unitTableDef1 = vars.unitTableDef1
		local unitTableDef2 = vars.unitTableDef2

		if not unitset1.processed then
			unitTableDef1 = mist.utils.deepCopy(unitset1)
		end

		if not unitset2.processed then
			unitTableDef2 = mist.utils.deepCopy(unitset2)
		end

		if (unitset1.processed and unitset1.processed < mist.getLastDBUpdateTime()) or not unitset1.processed then -- run unit table short cuts
			if unitTableDef1 then
				unitset1 = mist.makeUnitTable(unitTableDef1)
			end
		end

		if (unitset2.processed and unitset2.processed < mist.getLastDBUpdateTime()) or not unitset2.processed then -- run unit table short cuts
			if unitTableDef2 then
				unitset2 = mist.makeUnitTable(unitTableDef2)
			end
		end


		if stopflag == -1 or (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == false) then

			local unitLOSdata = mist.getUnitsLOS(unitset1, altoffset1, unitset2, altoffset2, radius)

			if #unitLOSdata >= req_num and trigger.misc.getUserFlag(flag) == 0 then
				trigger.action.setUserFlag(flag, true)
			elseif #unitLOSdata < req_num and toggle then
				trigger.action.setUserFlag(flag, false)
			end
			-- do another check in case stopflag was set true by this function
			if (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == false) then
				mist.scheduleFunction(mist.flagFunc.units_LOS, {{unitset1 = unitset1, altoffset1 = altoffset1, unitset2 = unitset2, altoffset2 = altoffset2, flag = flag, stopflag = stopflag, radius = radius, req_num = req_num, interval = interval, toggle = toggle, unitTableDef1 = unitTableDef1, unitTableDef2 = unitTableDef2}}, timer.getTime() + interval)
			end
		end
	end

	--- Sets a flag if group is alive.
	-- @todo document
	function mist.flagFunc.group_alive(vars)
		--[[vars
groupName
flag
toggle
interval
stopFlag

]]
		local type_tbl = {
			[{'group', 'groupname', 'gp', 'groupName'}] = 'string',
			flag = {'number', 'string'},
			[{'stopflag', 'stopFlag'}] = {'number', 'string', 'nil'},
			interval = {'number', 'nil'},
			toggle = {'boolean', 'nil'},
		}

		local err, errmsg = mist.utils.typeCheck('mist.flagFunc.group_alive', type_tbl, vars)
		assert(err, errmsg)

		local groupName = vars.groupName or vars.group or vars.gp or vars.Groupname
		local flag = vars.flag
		local stopflag = vars.stopflag or vars.stopFlag or -1
		local interval = vars.interval or 1
		local toggle = vars.toggle or nil


		if stopflag == -1 or (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == false) then
			if Group.getByName(groupName) and Group.getByName(groupName):isExist() == true and #Group.getByName(groupName):getUnits() > 0 then
				if trigger.misc.getUserFlag(flag) == 0 then
					trigger.action.setUserFlag(flag, true)
				end
			else
				if toggle then
					trigger.action.setUserFlag(flag, false)
				end
			end
		end

		if (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == false) then
			mist.scheduleFunction(mist.flagFunc.group_alive, {{groupName = groupName, flag = flag, stopflag = stopflag, interval = interval, toggle = toggle}}, timer.getTime() + interval)
		end

	end

	--- Sets a flag if group is dead.
	-- @todo document
	function mist.flagFunc.group_dead(vars)
		local type_tbl = {
			[{'group', 'groupname', 'gp', 'groupName'}] = 'string',
			flag = {'number', 'string'},
			[{'stopflag', 'stopFlag'}] = {'number', 'string', 'nil'},
			interval = {'number', 'nil'},
			toggle = {'boolean', 'nil'},
		}

		local err, errmsg = mist.utils.typeCheck('mist.flagFunc.group_dead', type_tbl, vars)
		assert(err, errmsg)

		local groupName = vars.groupName or vars.group or vars.gp or vars.Groupname
		local flag = vars.flag
		local stopflag = vars.stopflag or vars.stopFlag or -1
		local interval = vars.interval or 1
		local toggle = vars.toggle or nil


		if stopflag == -1 or (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == false) then
			if (Group.getByName(groupName) and Group.getByName(groupName):isExist() == false) or (Group.getByName(groupName) and #Group.getByName(groupName):getUnits() < 1) or not Group.getByName(groupName) then
				if trigger.misc.getUserFlag(flag) == 0 then
					trigger.action.setUserFlag(flag, true)
				end
			else
				if toggle then
					trigger.action.setUserFlag(flag, false)
				end
			end
		end

		if (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == false) then
			mist.scheduleFunction(mist.flagFunc.group_dead, {{groupName = groupName, flag = flag, stopflag = stopflag, interval = interval, toggle = toggle}}, timer.getTime() + interval)
		end
	end

	--- Sets a flag if less than given percent of group is alive.
	-- @todo document
	function mist.flagFunc.group_alive_less_than(vars)
		local type_tbl = {
			[{'group', 'groupname', 'gp', 'groupName'}] = 'string',
			percent = 'number',
			flag = {'number', 'string'},
			[{'stopflag', 'stopFlag'}] = {'number', 'string', 'nil'},
			interval = {'number', 'nil'},
			toggle = {'boolean', 'nil'},
		}

		local err, errmsg = mist.utils.typeCheck('mist.flagFunc.group_alive_less_than', type_tbl, vars)
		assert(err, errmsg)

		local groupName = vars.groupName or vars.group or vars.gp or vars.Groupname
		local flag = vars.flag
		local percent = vars.percent
		local stopflag = vars.stopflag or vars.stopFlag or -1
		local interval = vars.interval or 1
		local toggle = vars.toggle or nil


		if stopflag == -1 or (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == false) then
			if Group.getByName(groupName) and Group.getByName(groupName):isExist() == true then
				if Group.getByName(groupName):getSize()/Group.getByName(groupName):getInitialSize() < percent/100 then
					if trigger.misc.getUserFlag(flag) == 0 then
						trigger.action.setUserFlag(flag, true)
					end
				else
					if toggle then
						trigger.action.setUserFlag(flag, false)
					end
				end
			else
				if trigger.misc.getUserFlag(flag) == 0 then
					trigger.action.setUserFlag(flag, true)
				end
			end
		end

		if (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == false) then
			mist.scheduleFunction(mist.flagFunc.group_alive_less_than, {{groupName = groupName, flag = flag, stopflag = stopflag, interval = interval, toggle = toggle, percent = percent}}, timer.getTime() + interval)
		end
	end

	--- Sets a flag if more than given percent of group is alive.
	-- @todo document
	function mist.flagFunc.group_alive_more_than(vars)
		local type_tbl = {
			[{'group', 'groupname', 'gp', 'groupName'}] = 'string',
			percent = 'number',
			flag = {'number', 'string'},
			[{'stopflag', 'stopFlag'}] = {'number', 'string', 'nil'},
			interval = {'number', 'nil'},
			toggle = {'boolean', 'nil'},
		}

		local err, errmsg = mist.utils.typeCheck('mist.flagFunc.group_alive_more_than', type_tbl, vars)
		assert(err, errmsg)

		local groupName = vars.groupName or vars.group or vars.gp or vars.Groupname
		local flag = vars.flag
		local percent = vars.percent
		local stopflag = vars.stopflag or vars.stopFlag or -1
		local interval = vars.interval or 1
		local toggle = vars.toggle or nil


		if stopflag == -1 or (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == false) then
			if Group.getByName(groupName) and Group.getByName(groupName):isExist() == true then
				if Group.getByName(groupName):getSize()/Group.getByName(groupName):getInitialSize() > percent/100 then
					if trigger.misc.getUserFlag(flag) == 0 then
						trigger.action.setUserFlag(flag, true)
					end
				else
					if toggle and trigger.misc.getUserFlag(flag) == 1 then
						trigger.action.setUserFlag(flag, false)
					end
				end
			else --- just in case
				if toggle and trigger.misc.getUserFlag(flag) == 1 then
					trigger.action.setUserFlag(flag, false)
				end
			end
		end

		if (type(trigger.misc.getUserFlag(stopflag)) == 'number' and trigger.misc.getUserFlag(stopflag) == 0) or (type(trigger.misc.getUserFlag(stopflag)) == 'boolean' and trigger.misc.getUserFlag(stopflag) == false) then
			mist.scheduleFunction(mist.flagFunc.group_alive_more_than, {{groupName = groupName, flag = flag, stopflag = stopflag, interval = interval, toggle = toggle, percent = percent}}, timer.getTime() + interval)
		end
	end

	mist.flagFunc.mapobjsDeadPolygon = mist.flagFunc.mapobjs_dead_polygon
	mist.flagFunc.mapobjsDeadZones = mist.flagFunc.Mapobjs_dead_zones
	mist.flagFunc.unitsInZones = mist.flagFunc.units_in_zones
	mist.flagFunc.unitsInMovingZones = mist.flagFunc.units_in_moving_zones
	mist.flagFunc.unitsInPolygon = mist.flagFunc.units_in_polygon
	mist.flagFunc.unitsLOS = mist.flagFunc.units_LOS
	mist.flagFunc.groupAlive = mist.flagFunc.group_alive
	mist.flagFunc.groupDead = mist.flagFunc.group_dead
	mist.flagFunc.groupAliveMoreThan = mist.flagFunc.group_alive_more_than
	mist.flagFunc.groupAliveLessThan = mist.flagFunc.group_alive_less_than

end

--- Message functions.
-- Messaging system
-- @section mist.msg
do -- mist.msg scope
	local messageList = {}
	-- this defines the max refresh rate of the message box it honestly only needs to
	-- go faster than this for precision timing stuff (which could be its own function)
	local messageDisplayRate = 0.1
	local messageID = 0
	local displayActive = false
	local displayFuncId = 0

	local caSlots = false
	local caMSGtoGroup = false

	if env.mission.groundControl then -- just to be sure?
		for index, value in pairs(env.mission.groundControl) do
			if type(value) == 'table' then
				for roleName, roleVal in pairs(value) do
					for rIndex, rVal in pairs(roleVal) do
                        if env.mission.groundControl[index][roleName][rIndex] > 0 then
                            caSlots = true
                            break
                        end
						
					end
				end
			elseif type(value) == 'boolean' and value == true then
				caSlots = true
				break
			end
		end
	end

	local function mistdisplayV5()
		--[[thoughts to improve upon
		event handler based activeClients table.
		display messages only when there is an update
		possibly co-routine it.
		]]
	end

	local function mistdisplayV4()
		local activeClients = {}

		for clientId, clientData in pairs(mist.DBs.humansById) do
			if Unit.getByName(clientData.unitName) and Unit.getByName(clientData.unitName):isExist() == true then
				activeClients[clientData.groupId] = clientData.groupName
			end
		end

		--[[if caSlots == true and caMSGtoGroup == true then

		end]]


		if #messageList > 0 then
			if displayActive == false then
				displayActive = true
			end
			--mist.debug.writeData(mist.utils.serialize,{'msg', messageList}, 'messageList.lua')
			local msgTableText = {}
			local msgTableSound = {}

			for messageId, messageData in pairs(messageList) do
				if messageData.displayedFor > messageData.displayTime then
					messageData:remove()	-- now using the remove/destroy function.
				else
					if messageData.displayedFor then
						messageData.displayedFor = messageData.displayedFor + messageDisplayRate
					end
					local nextSound = 1000
					local soundIndex = 0

					if messageData.multSound and #messageData.multSound > 0 then
						for index, sData in pairs(messageData.multSound) do
							if sData.time <= messageData.displayedFor and sData.played == false and sData.time < nextSound then -- find index of the next sound to be played
								nextSound = sData.time
								soundIndex = index
							end
						end
						if soundIndex ~= 0 then
							messageData.multSound[soundIndex].played = true
						end
					end

					for recIndex, recData in pairs(messageData.msgFor) do -- iterate recipiants
						if recData == 'RED' or recData == 'BLUE' or activeClients[recData] then -- rec exists
							if messageData.text then -- text
								if not msgTableText[recData] then -- create table entry for text
									msgTableText[recData] = {}
									msgTableText[recData].text = {}
									if recData == 'RED' or recData == 'BLUE' then
										msgTableText[recData].text[1] = '-------Combined Arms Message-------- \n'
									end
									msgTableText[recData].text[#msgTableText[recData].text + 1] = messageData.text
									msgTableText[recData].displayTime = messageData.displayTime - messageData.displayedFor
								else -- add to table entry and adjust display time if needed
									if recData == 'RED' or recData == 'BLUE' then
										msgTableText[recData].text[#msgTableText[recData].text + 1] = '\n ---------------- Combined Arms Message: \n'
									else
										msgTableText[recData].text[#msgTableText[recData].text + 1] = '\n ---------------- \n'
									end
									msgTableText[recData].text[#msgTableText[recData].text + 1] = messageData.text
									if msgTableText[recData].displayTime < messageData.displayTime - messageData.displayedFor then
										msgTableText[recData].displayTime = messageData.displayTime - messageData.displayedFor
									else
										msgTableText[recData].displayTime = 1
									end
								end
							end
							if soundIndex ~= 0 then
								msgTableSound[recData] = messageData.multSound[soundIndex].file
							end
						end
					end


				end
			end
			------- new display

			if caSlots == true and caMSGtoGroup == false then
				if msgTableText.RED then
					trigger.action.outTextForCoalition(coalition.side.RED, table.concat(msgTableText.RED.text), msgTableText.RED.displayTime, true)

				end
				if msgTableText.BLUE then
					trigger.action.outTextForCoalition(coalition.side.BLUE, table.concat(msgTableText.BLUE.text), msgTableText.BLUE.displayTime, true)
				end
			end

			for index, msgData in pairs(msgTableText) do
				if type(index) == 'number' then -- its a groupNumber
					trigger.action.outTextForGroup(index, table.concat(msgData.text), msgData.displayTime, true)
				end
			end
			--- new audio
			if msgTableSound.RED then
				trigger.action.outSoundForCoalition(coalition.side.RED, msgTableSound.RED)
			end
			if msgTableSound.BLUE then
				trigger.action.outSoundForCoalition(coalition.side.BLUE, msgTableSound.BLUE)
			end


			for index, file in pairs(msgTableSound) do
				if type(index) == 'number' then -- its a groupNumber
					trigger.action.outSoundForGroup(index, file)
				end
			end
		else
			mist.removeFunction(displayFuncId)
			displayActive = false
		end

	end

	local typeBase = {
		['Mi-8MT'] = {'Mi-8MTV2', 'Mi-8MTV', 'Mi-8'},
		['MiG-21Bis'] = {'Mig-21'},
		['MiG-15bis'] = {'Mig-15'},
		['FW-190D9'] = {'FW-190'},
		['Bf-109K-4'] = {'Bf-109'},
	}

	--[[function mist.setCAGroupMSG(val)
	if type(val) == 'boolean' then
		caMSGtoGroup = val
		return true
	end
	return false
end]]

	mist.message = {

		add = function(vars)
			local function msgSpamFilter(recList, spamBlockOn)
				for id, name in pairs(recList) do
					if name == spamBlockOn then
						--	log:info('already on recList')
						return recList
					end
				end
				--log:info('add to recList')
				table.insert(recList, spamBlockOn)
				return recList
			end

			--[[
			local vars = {}
			vars.text = 'Hello World'
			vars.displayTime = 20
			vars.msgFor = {coa = {'red'}, countries = {'Ukraine', 'Georgia'}, unitTypes = {'A-10C'}}
			mist.message.add(vars)

			Displays the message for all red coalition players. Players belonging to Ukraine and Georgia, and all A-10Cs on the map

			]]


			local new = {}
			new.text = vars.text -- The actual message
			new.displayTime = vars.displayTime -- How long will the message appear for
			new.displayedFor = 0 -- how long the message has been displayed so far
			new.name = vars.name	 -- ID to overwrite the older message (if it exists) Basically it replaces a message that is displayed with new text.
			new.addedAt = timer.getTime()
			new.update = true

			if vars.multSound and vars.multSound[1] then
				new.multSound = vars.multSound
			else
				new.multSound = {}
			end

			if vars.sound or vars.fileName then -- converts old sound file system into new multSound format
				local sound = vars.sound
				if vars.fileName then
					sound = vars.fileName
				end
				new.multSound[#new.multSound+1] = {time = 0.1, file = sound}
			end

			if #new.multSound > 0 then
				for i, data in pairs(new.multSound) do
					data.played = false
				end
			end

			local newMsgFor = {} -- list of all groups message displays for
			for forIndex, forData in pairs(vars.msgFor) do
				for list, listData in pairs(forData) do
					for clientId, clientData in pairs(mist.DBs.humansById) do
						forIndex = string.lower(forIndex)
						if type(listData) == 'string' then
							listData = string.lower(listData)
						end
						if (forIndex == 'coa' and (listData == string.lower(clientData.coalition) or listData == 'all')) or (forIndex == 'countries' and string.lower(clientData.country) == listData) or (forIndex == 'units' and string.lower(clientData.unitName) == listData) then --
							newMsgFor = msgSpamFilter(newMsgFor, clientData.groupId) -- so units dont get the same message twice if complex rules are given
							--table.insert(newMsgFor, clientId)
						elseif forIndex == 'unittypes' then
							for typeId, typeData in pairs(listData) do
								local found = false
								for clientDataEntry, clientDataVal in pairs(clientData) do
									if type(clientDataVal) == 'string' then
										if mist.matchString(list, clientDataVal) == true or list == 'all' then
											local sString = typeData
											for rName, pTbl in pairs(typeBase) do -- just a quick check to see if the user may have meant something and got the specific type of the unit wrong
												for pIndex, pName in pairs(pTbl) do
													if mist.stringMatch(sString, pName) then
														sString = rName
													end
												end
											end
											if sString == clientData.type then
												found = true
												newMsgFor = msgSpamFilter(newMsgFor, clientData.groupId) -- sends info oto other function to see if client is already recieving the current message.
												--table.insert(newMsgFor, clientId)
											end
										end
									end
									if found == true then	-- shouldn't this be elsewhere too?
										break
									end
								end
							end

						end
					end
					for coaData, coaId in pairs(coalition.side) do
						if string.lower(forIndex) == 'coa' or string.lower(forIndex) == 'ca' then
							if listData == string.lower(coaData) or listData == 'all' then
								newMsgFor = msgSpamFilter(newMsgFor, coaData)
							end
						end
					end
				end
			end

			if #newMsgFor > 0 then
				new.msgFor = newMsgFor -- I swear its not confusing

			else
				return false
			end


			if vars.name and type(vars.name) == 'string' then
				for i = 1, #messageList do
					if messageList[i].name then
						if messageList[i].name == vars.name then
							--log:info('updateMessage')
							messageList[i].displayedFor = 0
							messageList[i].addedAt = timer.getTime()
							messageList[i].sound = new.sound
							messageList[i].text = new.text
							messageList[i].msgFor = new.msgFor
							messageList[i].multSound = new.multSound
							messageList[i].update = true
							return messageList[i].messageID
						end
					end
				end
			end

			messageID = messageID + 1
			new.messageID = messageID

			--mist.debug.writeData(mist.utils.serialize,{'msg', new}, 'newMsg.lua')


			messageList[#messageList + 1] = new

			local mt = { __index =	mist.message}
			setmetatable(new, mt)

			if displayActive == false then
				displayActive = true
				displayFuncId = mist.scheduleFunction(mistdisplayV4, {}, timer.getTime() + messageDisplayRate, messageDisplayRate)
			end

			return messageID

		end,

		remove = function(self)	-- Now a self variable; the former functionality taken up by mist.message.removeById.
			for i, msgData in pairs(messageList) do
				if messageList[i] == self then
					table.remove(messageList, i)
					return true --removal successful
				end
			end
			return false -- removal not successful this script fails at life!
		end,

		removeById = function(id)	-- This function is NOT passed a self variable; it is the remove by id function.
			for i, msgData in pairs(messageList) do
				if messageList[i].messageID == id then
					table.remove(messageList, i)
					return true --removal successful
				end
			end
			return false -- removal not successful this script fails at life!
		end,
	}

	--[[ vars for mist.msgMGRS
vars.units - table of unit names (NOT unitNameTable- maybe this should change).
vars.acc - integer between 0 and 5, inclusive
vars.text - text in the message
vars.displayTime - self explanatory
vars.msgFor - scope
]]
	function mist.msgMGRS(vars)
		local units = vars.units
		local acc = vars.acc
		local text = vars.text
		local displayTime = vars.displayTime
		local msgFor = vars.msgFor

		local s = mist.getMGRSString{units = units, acc = acc}
		local newText
		if text then
			if string.find(text, '%%s') then	-- look for %s
				newText = string.format(text, s)	-- insert the coordinates into the message
			else
				-- just append to the end.
				newText = text .. s
			end
		else
			newText = s
		end
		mist.message.add{
			text = newText,
			displayTime = displayTime,
			msgFor = msgFor
		}
	end

	--[[ vars for mist.msgLL
vars.units - table of unit names (NOT unitNameTable- maybe this should change) (Yes).
vars.acc - integer, number of numbers after decimal place
vars.DMS - if true, output in degrees, minutes, seconds.	Otherwise, output in degrees, minutes.
vars.text - text in the message
vars.displayTime - self explanatory
vars.msgFor - scope
]]
	function mist.msgLL(vars)
		local units = vars.units	-- technically, I don't really need to do this, but it helps readability.
		local acc = vars.acc
		local DMS = vars.DMS
		local text = vars.text
		local displayTime = vars.displayTime
		local msgFor = vars.msgFor

		local s = mist.getLLString{units = units, acc = acc, DMS = DMS}
		local newText
		if text then
			if string.find(text, '%%s') then	-- look for %s
				newText = string.format(text, s)	-- insert the coordinates into the message
			else
				-- just append to the end.
				newText = text .. s
			end
		else
			newText = s
		end

		mist.message.add{
			text = newText,
			displayTime = displayTime,
			msgFor = msgFor
		}

	end

	--[[
vars.units- table of unit names (NOT unitNameTable- maybe this should change).
vars.ref -	vec3 ref point, maybe overload for vec2 as well?
vars.alt - boolean, if used, includes altitude in string
vars.metric - boolean, gives distance in km instead of NM.
vars.text - text of the message
vars.displayTime
vars.msgFor - scope
]]
	function mist.msgBR(vars)
		local units = vars.units	-- technically, I don't really need to do this, but it helps readability.
		local ref = vars.ref -- vec2/vec3 will be handled in mist.getBRString
		local alt = vars.alt
		local metric = vars.metric
		local text = vars.text
		local displayTime = vars.displayTime
		local msgFor = vars.msgFor

		local s = mist.getBRString{units = units, ref = ref, alt = alt, metric = metric}
		local newText
		if text then
			if string.find(text, '%%s') then	-- look for %s
				newText = string.format(text, s)	-- insert the coordinates into the message
			else
				-- just append to the end.
				newText = text .. s
			end
		else
			newText = s
		end

		mist.message.add{
			text = newText,
			displayTime = displayTime,
			msgFor = msgFor
		}

	end

	-- basically, just sub-types of mist.msgBR... saves folks the work of getting the ref point.
	--[[
vars.units- table of unit names (NOT unitNameTable- maybe this should change).
vars.ref -	string red, blue
vars.alt - boolean, if used, includes altitude in string
vars.metric - boolean, gives distance in km instead of NM.
vars.text - text of the message
vars.displayTime
vars.msgFor - scope
]]
	function mist.msgBullseye(vars)
		if mist.DBs.missionData.bullseye[string.lower(vars.ref)] then
			vars.ref = mist.DBs.missionData.bullseye[string.lower(vars.ref)]
			mist.msgBR(vars)
		end
	end

	--[[
vars.units- table of unit names (NOT unitNameTable- maybe this should change).
vars.ref -	unit name of reference point
vars.alt - boolean, if used, includes altitude in string
vars.metric - boolean, gives distance in km instead of NM.
vars.text - text of the message
vars.displayTime
vars.msgFor - scope
]]
	function mist.msgBRA(vars)
		if Unit.getByName(vars.ref) and Unit.getByName(vars.ref):isExist() == true then
			vars.ref = Unit.getByName(vars.ref):getPosition().p
			if not vars.alt then
				vars.alt = true
			end
			mist.msgBR(vars)
		end
	end

	--[[ vars for mist.msgLeadingMGRS:
vars.units - table of unit names
vars.heading - direction
vars.radius - number
vars.headingDegrees - boolean, switches heading to degrees (optional)
vars.acc - number, 0 to 5.
vars.text - text of the message
vars.displayTime
vars.msgFor - scope
]]
	function mist.msgLeadingMGRS(vars)
		local units = vars.units	-- technically, I don't really need to do this, but it helps readability.
		local heading = vars.heading
		local radius = vars.radius
		local headingDegrees = vars.headingDegrees
		local acc = vars.acc
		local text = vars.text
		local displayTime = vars.displayTime
		local msgFor = vars.msgFor

		local s = mist.getLeadingMGRSString{units = units, heading = heading, radius = radius, headingDegrees = headingDegrees, acc = acc}
		local newText
		if text then
			if string.find(text, '%%s') then	-- look for %s
				newText = string.format(text, s)	-- insert the coordinates into the message
			else
				-- just append to the end.
				newText = text .. s
			end
		else
			newText = s
		end

		mist.message.add{
			text = newText,
			displayTime = displayTime,
			msgFor = msgFor
		}


	end

	--[[ vars for mist.msgLeadingLL:
vars.units - table of unit names
vars.heading - direction, number
vars.radius - number
vars.headingDegrees - boolean, switches heading to degrees (optional)
vars.acc - number of digits after decimal point (can be negative)
vars.DMS -	boolean, true if you want DMS. (optional)
vars.text - text of the message
vars.displayTime
vars.msgFor - scope
]]
	function mist.msgLeadingLL(vars)
		local units = vars.units	-- technically, I don't really need to do this, but it helps readability.
		local heading = vars.heading
		local radius = vars.radius
		local headingDegrees = vars.headingDegrees
		local acc = vars.acc
		local DMS = vars.DMS
		local text = vars.text
		local displayTime = vars.displayTime
		local msgFor = vars.msgFor

		local s = mist.getLeadingLLString{units = units, heading = heading, radius = radius, headingDegrees = headingDegrees, acc = acc, DMS = DMS}
		local newText

		if text then
			if string.find(text, '%%s') then	-- look for %s
				newText = string.format(text, s)	-- insert the coordinates into the message
			else
				-- just append to the end.
				newText = text .. s
			end
		else
			newText = s
		end

		mist.message.add{
			text = newText,
			displayTime = displayTime,
			msgFor = msgFor
		}

	end

	--[[
vars.units - table of unit names
vars.heading - direction, number
vars.radius - number
vars.headingDegrees - boolean, switches heading to degrees	(optional)
vars.metric - boolean, if true, use km instead of NM. (optional)
vars.alt - boolean, if true, include altitude. (optional)
vars.ref - vec3/vec2 reference point.
vars.text - text of the message
vars.displayTime
vars.msgFor - scope
]]
	function mist.msgLeadingBR(vars)
		local units = vars.units	-- technically, I don't really need to do this, but it helps readability.
		local heading = vars.heading
		local radius = vars.radius
		local headingDegrees = vars.headingDegrees
		local metric = vars.metric
		local alt = vars.alt
		local ref = vars.ref -- vec2/vec3 will be handled in mist.getBRString
		local text = vars.text
		local displayTime = vars.displayTime
		local msgFor = vars.msgFor

		local s = mist.getLeadingBRString{units = units, heading = heading, radius = radius, headingDegrees = headingDegrees, metric = metric, alt = alt, ref = ref}
		local newText

		if text then
			if string.find(text, '%%s') then	-- look for %s
				newText = string.format(text, s)	-- insert the coordinates into the message
			else
				-- just append to the end.
				newText = text .. s
			end
		else
			newText = s
		end

		mist.message.add{
			text = newText,
			displayTime = displayTime,
			msgFor = msgFor
		}
	end
end

--- Demo functions.
-- @section mist.demos
do -- mist.demos scope
	mist.demos = {}

	function mist.demos.printFlightData(unit)
		if unit:isExist() then
			local function printData(unit, prevVel, prevE, prevTime)
				local angles = mist.getAttitude(unit)
				if angles then
					local Heading = angles.Heading
					local Pitch = angles.Pitch
					local Roll = angles.Roll
					local Yaw = angles.Yaw
					local AoA = angles.AoA
					local ClimbAngle = angles.ClimbAngle

					if not Heading then
						Heading = 'NA'
					else
						Heading = string.format('%12.2f', mist.utils.toDegree(Heading))
					end

					if not Pitch then
						Pitch = 'NA'
					else
						Pitch = string.format('%12.2f', mist.utils.toDegree(Pitch))
					end

					if not Roll then
						Roll = 'NA'
					else
						Roll = string.format('%12.2f', mist.utils.toDegree(Roll))
					end

					local AoAplusYaw = 'NA'
					if AoA and Yaw then
						AoAplusYaw = string.format('%12.2f', mist.utils.toDegree((AoA^2 + Yaw^2)^0.5))
					end

					if not Yaw then
						Yaw = 'NA'
					else
						Yaw = string.format('%12.2f', mist.utils.toDegree(Yaw))
					end

					if not AoA then
						AoA = 'NA'
					else
						AoA = string.format('%12.2f', mist.utils.toDegree(AoA))
					end

					if not ClimbAngle then
						ClimbAngle = 'NA'
					else
						ClimbAngle = string.format('%12.2f', mist.utils.toDegree(ClimbAngle))
					end
					local unitPos = unit:getPosition()
					local unitVel = unit:getVelocity()
					local curTime = timer.getTime()
					local absVel = string.format('%12.2f', mist.vec.mag(unitVel))


					local unitAcc = 'NA'
					local Gs = 'NA'
					local axialGs = 'NA'
					local transGs = 'NA'
					if prevVel and prevTime then
						local xAcc = (unitVel.x - prevVel.x)/(curTime - prevTime)
						local yAcc = (unitVel.y - prevVel.y)/(curTime - prevTime)
						local zAcc = (unitVel.z - prevVel.z)/(curTime - prevTime)

						unitAcc = string.format('%12.2f', mist.vec.mag({x = xAcc, y = yAcc, z = zAcc}))
						Gs = string.format('%12.2f', mist.vec.mag({x = xAcc, y = yAcc + 9.81, z = zAcc})/9.81)
						axialGs = string.format('%12.2f', mist.vec.dp({x = xAcc, y = yAcc + 9.81, z = zAcc}, unitPos.x)/9.81)
						transGs = string.format('%12.2f', mist.vec.mag(mist.vec.cp({x = xAcc, y = yAcc + 9.81, z = zAcc}, unitPos.x))/9.81)
					end

					local E = 0.5*mist.vec.mag(unitVel)^2 + 9.81*unitPos.p.y

					local energy = string.format('%12.2e', E)

					local dEdt = 'NA'
					if prevE and prevTime then
						dEdt = string.format('%12.2e', (E - prevE)/(curTime - prevTime))
					end

					trigger.action.outText(string.format('%-25s', 'Heading: ') .. Heading .. ' degrees\n' .. string.format('%-25s', 'Roll: ') .. Roll .. ' degrees\n' .. string.format('%-25s', 'Pitch: ') .. Pitch
							.. ' degrees\n' .. string.format('%-25s', 'Yaw: ') .. Yaw .. ' degrees\n' .. string.format('%-25s', 'AoA: ') .. AoA .. ' degrees\n' .. string.format('%-25s', 'AoA plus Yaw: ') .. AoAplusYaw .. ' degrees\n' .. string.format('%-25s', 'Climb Angle: ') ..
							ClimbAngle .. ' degrees\n' .. string.format('%-25s', 'Absolute Velocity: ') .. absVel .. ' m/s\n' .. string.format('%-25s', 'Absolute Acceleration: ') .. unitAcc ..' m/s^2\n'
							.. string.format('%-25s', 'Axial G loading: ') .. axialGs .. ' g\n' .. string.format('%-25s', 'Transverse G loading: ') .. transGs .. ' g\n' .. string.format('%-25s', 'Absolute G loading: ') .. Gs .. ' g\n' .. string.format('%-25s', 'Energy: ') .. energy .. ' J/kg\n' .. string.format('%-25s', 'dE/dt: ') .. dEdt ..' J/(kg*s)', 1)
					return unitVel, E, curTime
				end
			end

			local function frameFinder(unit, prevVel, prevE, prevTime)
				if unit:isExist() then
					local currVel = unit:getVelocity()
					if prevVel and (prevVel.x ~= currVel.x or prevVel.y ~= currVel.y or prevVel.z ~= currVel.z) or (prevTime and (timer.getTime() - prevTime) > 0.25) then
						prevVel, prevE, prevTime = printData(unit, prevVel, prevE, prevTime)
					end
					mist.scheduleFunction(frameFinder, {unit, prevVel, prevE, prevTime}, timer.getTime() + 0.005)	-- it can't go this fast, limited to the 100 times a sec check right now.
				end
			end


			local curVel = unit:getVelocity()
			local curTime = timer.getTime()
			local curE = 0.5*mist.vec.mag(curVel)^2 + 9.81*unit:getPosition().p.y
			frameFinder(unit, curVel, curE, curTime)

		end

	end

end
do
	--[[ stuff for marker panels
		marker.add() add marker. Point of these functions is to simplify process and to store all mark panels added. 
		-- generates Id if not specified or if multiple marks created.
		-- makes marks for countries by creating a mark for each client group in the country
		-- can create multiple marks if needed for groups and countries.
		-- adds marks to table for parsing and removing
		-- Uses similar structure as messages. Big differences is it doesn't only mark to groups.
			If to All, then mark is for All
			if to coa mark is to coa
			if to specific units, mark is to group
			
			
		--------
		STUFF TO Check
		--------
		If mark added to a group before a client joins slot is synced.
		Mark made for cliet A in Slot A. Client A leaves, Client B joins in slot A. What do they see?
		
		May need to automate process...

	]]
	--[[
	local typeBase = {
		['Mi-8MT'] = {'Mi-8MTV2', 'Mi-8MTV', 'Mi-8'},
		['MiG-21Bis'] = {'Mig-21'},
		['MiG-15bis'] = {'Mig-15'},
		['FW-190D9'] = {'FW-190'},
		['Bf-109K-4'] = {'Bf-109'},
	}
	
	
	local mId = 1337
	
	mist.marker = {}
	mist.marker.list = {}
	local function markSpamFilter(recList, spamBlockOn)
		
		for id, name in pairs(recList) do
			if name == spamBlockOn then
				log:info('already on recList')
				return recList
			end
		end
		log:info('add to recList')
		table.insert(recList, spamBlockOn)
		return recList
	end
	
	local function iterate()
		mId = mId + 1
		return mId
	end
	
	function mist.marker.add(pos, text, markFor, id)
		log:warn('markerFunc')
		log:info('Pos: $1, Text: $2, markFor: $3, id: $4', pos, text, markFor, id)
		if not id then

		else

		end
		local markType = 'all'
		local markForTable = {}
		if pos then
			pos = mist.utils.makeVec3(pos)
		end
		if text and type(text) ~= string then
			text = tostring(text)
		else
			text = ''
		end

		if markFor then
			if type(markFor) == 'number' then -- groupId
				if mist.DBs.groupsById[markFor] then	
					markType = 'group'
				end
			elseif type(markFor) == 'string' then -- groupName
				if mist.DBs.groupsByName[markFor] then	
					markType = 'group'
					markFor = mist.DBs.groupsByName[markFor].groupId
				end
			elseif type(markFor) == 'table' then -- multiple groupName, country, coalition, all
				markType = 'table'
				log:info(markFor)
				for forIndex, forData in pairs(markFor) do -- need to rethink this part and organization. Gotta be a more logical way to send messages to coa, groups, or all. 
					log:info(forIndex)
					log:info(forData)
					for list, listData in pairs(forData) do
						log:info(listData)
						forIndex = string.lower(forIndex)
						if type(listData) == 'string' then
							listData = string.lower(listData)
						end
						if listData == 'all' then
							markType = 'all'
							break
						elseif (forIndex == 'coa' or forIndex == 'ca') then -- mark for coa or CA. 
							for name, index in pairs (coalition.side) do
								if listData == string.lower(name) then
									markType = 'coalition'
								end
							end
						elseif (forIndex == 'countries' and string.lower(clientData.country) == listData) or (forIndex == 'units' and string.lower(clientData.unitName) == listData) then
							markForTable = markSpamFilter(markForTable, clientData.groupId)
						elseif forIndex == 'unittypes' then -- mark to group
						-- iterate play units
							for clientId, clientData in pairs(mist.DBs.humansById) do
								for typeId, typeData in pairs(listData) do
									log:info(typeData)
									local found = false
									if list == 'all' or clientData.coalition and type(clientData.coalition) == 'string' and mist.stringMatch(clientData.coalition, list) then
										if mist.matchString(typeData, clientData.type) then
											found = true
										else
											-- check other known names for aircraft
										end
									end
									if found == true then
										markForTable = markSpamFilter(markForTable, clientData.groupId) -- sends info to other function to see if client is already recieving the current message.
									end
									for clientDataEntry, clientDataVal in pairs(clientData) do
										if type(clientDataVal) == 'string' then
											
											if mist.matchString(list, clientDataVal) == true or list == 'all' then
												local sString = typeData
												for rName, pTbl in pairs(typeBase) do -- just a quick check to see if the user may have meant something and got the specific type of the unit wrong
													for pIndex, pName in pairs(pTbl) do
														if mist.stringMatch(sString, pName) then
															sString = rName
														end
													end
												end
												if mist.stringMatch(sString, clientData.type) then
													found = true
													markForTable = markSpamFilter(markForTable, clientData.groupId) -- sends info oto other function to see if client is already recieving the current message.
													--table.insert(newMsgFor, clientId)
												end
											end
										end
										if found == true then	-- shouldn't this be elsewhere too?
											break
										end
									end
								end

							end
						end
					end
				end
			end
		else
			markType = 'all'
		end
		

		

		
		
		if markType ~= 'table' then
			local newId = iterate()
			local data = {markId = newId, text = text, pos = pos, markType = markType, markFor = markFor}

			-- create marks
			if markType == 'coa' then
				trigger.action.markToCoalition(newId, text, pos, markFor)
			elseif markType == 'group' then
				trigger.action.markToGroup(newId, text, pos, markFor)
			else
				trigger.action.markToAll(iterate(), text, pos)
			end
			table.insert(mist.marker.list, data) -- add to the DB
		else
			if #markForTable > 0 then
				log:info('iterate')
				for i = 1, #markForTable do
					local newId = iterate()
					local data = {markId = newId, text = text, pos = pos, markFor = markFor}
					log:info(data)
					table.insert(mist.marker.list, data)
					trigger.action.markToGroup(newId, text, pos, markForTable[i])
				end
			end
		end
		
		
		
	end
	
	function mist.marker.remove(id)
		for i, data in pairs(mist.marker.list) do
			if id == data.markId then
				trigger.action.removeMark(id)
			end
		end
	end
	
	function mist.marker.get(id)
	
	end
	
	function mist.marker.coords(pos, cType, markFor, id) -- wrapper function to just display coordinates of a specific format at location
		
	
	end
    ]]
end
--- Time conversion functions.
-- @section mist.time
do -- mist.time scope
	mist.time = {}
	-- returns a string for specified military time
	-- theTime is optional
	-- if present current time in mil time is returned
	-- if number or table the time is converted into mil tim
	function mist.time.convertToSec(timeTable)

		local timeInSec = 0
		if timeTable and type(timeTable) == 'number' then
			timeInSec = timeTable
		elseif timeTable and type(timeTable) == 'table' and (timeTable.d or timeTable.h or timeTable.m or timeTable.s) then
			if timeTable.d and type(timeTable.d) == 'number' then
				timeInSec = timeInSec + (timeTable.d*86400)
			end
			if timeTable.h and type(timeTable.h) == 'number' then
				timeInSec = timeInSec + (timeTable.h*3600)
			end
			if timeTable.m and type(timeTable.m) == 'number' then
				timeInSec = timeInSec + (timeTable.m*60)
			end
			if timeTable.s and type(timeTable.s) == 'number' then
				timeInSec = timeInSec + timeTable.s
			end

		end
		return timeInSec
	end

	function mist.time.getDHMS(timeInSec)
		if timeInSec and type(timeInSec) == 'number' then
			local tbl = {d = 0, h = 0, m = 0, s = 0}
			if timeInSec > 86400 then
				while timeInSec > 86400 do
					tbl.d = tbl.d + 1
					timeInSec = timeInSec - 86400
				end
			end
			if timeInSec > 3600 then
				while timeInSec > 3600 do
					tbl.h = tbl.h + 1
					timeInSec = timeInSec - 3600
				end
			end
			if timeInSec > 60 then
				while timeInSec > 60 do
					tbl.m = tbl.m + 1
					timeInSec = timeInSec - 60
				end
			end
			tbl.s = timeInSec
			return tbl
		else
			log:error("Didn't recieve number")
			return
		end
	end

	function mist.getMilString(theTime)
		local timeInSec = 0
		if theTime then
			timeInSec = mist.time.convertToSec(theTime)
		else
			timeInSec = mist.utils.round(timer.getAbsTime(), 0)
		end

		local DHMS = mist.time.getDHMS(timeInSec)

		return tostring(string.format('%02d', DHMS.h) .. string.format('%02d',DHMS.m))
	end

	function mist.getClockString(theTime, hour)
		local timeInSec = 0
		if theTime then
			timeInSec = mist.time.convertToSec(theTime)
		else
			timeInSec = mist.utils.round(timer.getAbsTime(), 0)
		end
		local DHMS = mist.time.getDHMS(timeInSec)
		if hour then
			if DHMS.h > 12 then
				DHMS.h = DHMS.h - 12
				return tostring(string.format('%02d', DHMS.h) .. ':' .. string.format('%02d',DHMS.m)	.. ':' .. string.format('%02d',DHMS.s) .. ' PM')
			else
				return tostring(string.format('%02d', DHMS.h) .. ':' .. string.format('%02d',DHMS.m)	.. ':' .. string.format('%02d',DHMS.s) .. ' AM')
			end
		else
			return tostring(string.format('%02d', DHMS.h) .. ':' .. string.format('%02d',DHMS.m)	.. ':' .. string.format('%02d',DHMS.s))
		end
	end

	-- returns the date in string format
	-- both variables optional
	-- first val returns with the month as a string
	-- 2nd val defins if it should be written the American way or the wrong way.
	function mist.time.getDate(convert)
		local cal = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31} -- 
		local date = {}
		
		if not env.mission.date then -- Not likely to happen. Resaving mission auto updates this to remove it.
			date.d = 0
			date.m = 6
			date.y = 2011
		else 
			date.d = env.mission.date.Day
			date.m = env.mission.date.Month
			date.y = env.mission.date.Year
		end
		local start = 86400
		local timeInSec = mist.utils.round(timer.getAbsTime())
		if convert and type(convert) == 'number' then
			timeInSec = convert
		end
		if timeInSec > 86400 then
			while start < timeInSec do
				if date.d >= cal[date.m] then
					if date.m == 2 and date.d == 28 then -- HOLY COW we can edit years now. Gotta re-add this!
						if date.y % 4 == 0 and date.y % 100 == 0 and date.y % 400 ~= 0 or date.y % 4 > 0 then
							date.m = date.m + 1
							date.d = 0
						end
						--date.d = 29
					else
						date.m = date.m + 1
						date.d = 0
					end
				end
				if date.m == 13 then
					date.m = 1
					date.y = date.y + 1
				end
				date.d = date.d + 1
				start = start + 86400
				
			end
		end
		return date
	end

	function mist.time.relativeToStart(time)
		if type(time) == 'number' then
			return time - timer.getTime0()
		end
	end

	function mist.getDateString(rtnType, murica, oTime) -- returns date based on time
		local word = {'January', 'Feburary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' } -- 'etc
		local curTime = 0
		if oTime then
			curTime = oTime
		else
			curTime = mist.utils.round(timer.getAbsTime())
		end
		local tbl = mist.time.getDate(curTime)

		if rtnType then
			if murica then
				return tostring(word[tbl.m] .. ' ' .. tbl.d .. ' ' .. tbl.y)
			else
				return tostring(tbl.d .. ' ' .. word[tbl.m] .. ' ' .. tbl.y)
			end
		else
			if murica then
				return tostring(tbl.m .. '.' .. tbl.d .. '.' .. tbl.y)
			else
				return tostring(tbl.d .. '.' .. tbl.m .. '.' .. tbl.y)
			end
		end
	end
	--WIP
	function mist.time.milToGame(milString, rtnType) --converts a military time. By default returns the abosolute time that event would occur. With optional value it returns how many seconds from time of call till that time.
		local curTime = mist.utils.round(timer.getAbsTime())
		local milTimeInSec = 0

		if milString and type(milString) == 'string' and string.len(milString) >= 4 then
			local hr = tonumber(string.sub(milString, 1, 2))
			local mi = tonumber(string.sub(milString, 3))
			milTimeInSec = milTimeInSec + (mi*60) + (hr*3600)
		elseif milString and type(milString) == 'table' and (milString.d or milString.h or milString.m or milString.s) then
			milTimeInSec = mist.time.convertToSec(milString)
		end

		local startTime = timer.getTime0()
		local daysOffset = 0
		if startTime > 86400 then
			daysOffset = mist.utils.round(startTime/86400)
			if daysOffset > 0 then
				milTimeInSec = milTimeInSec *daysOffset
			end
		end

		if curTime > milTimeInSec then
			milTimeInSec = milTimeInSec + 86400
		end
		if rtnType then
			milTimeInSec = milTimeInSec - startTime
		end
		return milTimeInSec
	end


end

--- Group task functions.
-- @section tasks
do -- group tasks scope
	mist.ground = {}
	mist.fixedWing = {}
	mist.heli = {}
	mist.air = {}
	mist.air.fixedWing = {}
	mist.air.heli = {}

	--- Tasks group to follow a route.
	-- This sets the mission task for the given group.
	-- Any wrapped actions inside the path (like enroute
	-- tasks) will be executed.
	-- @tparam Group group group to task.
	-- @tparam table path containing
	-- points defining a route.
	function mist.goRoute(group, path)
		local misTask = {
			id = 'Mission',
			params = {
				route = {
					points = mist.utils.deepCopy(path),
				},
			},
		}
		if type(group) == 'string' then
			group = Group.getByName(group)
		end
		if group then
			local groupCon = group:getController()
			if groupCon then
                log:warn(misTask)
				groupCon:setTask(misTask)
				return true
			end
		end
		return false
	end

	-- same as getGroupPoints but returns speed and formation type along with vec2 of point}
	function mist.getGroupRoute(groupIdent, task)
		-- refactor to search by groupId and allow groupId and groupName as inputs
		local gpId = groupIdent
			if mist.DBs.MEgroupsByName[groupIdent] then
				gpId = mist.DBs.MEgroupsByName[groupIdent].groupId
			else
				log:error('$1 not found in mist.DBs.MEgroupsByName', groupIdent)
			end

		for coa_name, coa_data in pairs(env.mission.coalition) do
			if type(coa_data) == 'table' then
				if coa_data.country then --there is a country table
					for cntry_id, cntry_data in pairs(coa_data.country) do
						for obj_type_name, obj_type_data in pairs(cntry_data) do
							if obj_type_name == "helicopter" or obj_type_name == "ship" or obj_type_name == "plane" or obj_type_name == "vehicle" then	-- only these types have points
								if ((type(obj_type_data) == 'table') and obj_type_data.group and (type(obj_type_data.group) == 'table') and (#obj_type_data.group > 0)) then	--there's a group!
									for group_num, group_data in pairs(obj_type_data.group) do
										if group_data and group_data.groupId == gpId	then -- this is the group we are looking for
											if group_data.route and group_data.route.points and #group_data.route.points > 0 then
												local points = {}

												for point_num, point in pairs(group_data.route.points) do
													local routeData = {}
													if env.mission.version > 7 then
														routeData.name = env.getValueDictByKey(point.name)
													else
														routeData.name = point.name
													end
													if not point.point then
														routeData.x = point.x
														routeData.y = point.y
													else
														routeData.point = point.point	--it's possible that the ME could move to the point = Vec2 notation.
													end
													routeData.form = point.action
													routeData.speed = point.speed
													routeData.alt = point.alt
													routeData.alt_type = point.alt_type
													routeData.airdromeId = point.airdromeId
													routeData.helipadId = point.helipadId
													routeData.type = point.type
													routeData.action = point.action
													if task then
														routeData.task = point.task
													end
													points[point_num] = routeData
												end

												return points
											end
											log:error('Group route not defined in mission editor for groupId: $1', gpId)
											return
										end	--if group_data and group_data.name and group_data.name == 'groupname'
									end --for group_num, group_data in pairs(obj_type_data.group) do
								end --if ((type(obj_type_data) == 'table') and obj_type_data.group and (type(obj_type_data.group) == 'table') and (#obj_type_data.group > 0)) then
							end --if obj_type_name == "helicopter" or obj_type_name == "ship" or obj_type_name == "plane" or obj_type_name == "vehicle" or obj_type_name == "static" then
						end --for obj_type_name, obj_type_data in pairs(cntry_data) do
					end --for cntry_id, cntry_data in pairs(coa_data.country) do
				end --if coa_data.country then --there is a country table
			end --if coa_name == 'red' or coa_name == 'blue' and type(coa_data) == 'table' then
		end --for coa_name, coa_data in pairs(mission.coalition) do
	end

	-- function mist.ground.buildPath() end -- ????

	function mist.ground.patrolRoute(vars)
		--log:info('patrol')
		local tempRoute = {}
		local useRoute = {}
		local gpData = vars.gpData
		if type(gpData) == 'string' then
			gpData = Group.getByName(gpData)
		end

		local useGroupRoute
		if not vars.useGroupRoute then
			useGroupRoute = vars.gpData
		else
			useGroupRoute = vars.useGroupRoute
		end
		local routeProvided = false
		if not vars.route then
			if useGroupRoute then
				tempRoute = mist.getGroupRoute(useGroupRoute)
			end
		else
			useRoute = vars.route
			local posStart = mist.getLeadPos(gpData)
			useRoute[1] = mist.ground.buildWP(posStart, useRoute[1].action, useRoute[1].speed)
			routeProvided = true
		end


		local overRideSpeed = vars.speed or 'default'
		local pType = vars.pType
		local offRoadForm = vars.offRoadForm or 'default'
		local onRoadForm = vars.onRoadForm or 'default'

		if routeProvided == false and #tempRoute > 0 then
			local posStart = mist.getLeadPos(gpData)


			useRoute[#useRoute + 1] = mist.ground.buildWP(posStart, offRoadForm, overRideSpeed)
			for i = 1, #tempRoute do
				local tempForm = tempRoute[i].action
				local tempSpeed = tempRoute[i].speed

				if offRoadForm == 'default' then
					tempForm = tempRoute[i].action
				end
				if onRoadForm == 'default' then
					onRoadForm = 'On Road'
				end
				if (string.lower(tempRoute[i].action) == 'on road' or	string.lower(tempRoute[i].action) == 'onroad' or string.lower(tempRoute[i].action) == 'on_road') then
					tempForm = onRoadForm
				else
					tempForm = offRoadForm
				end

				if type(overRideSpeed) == 'number' then
					tempSpeed = overRideSpeed
				end


				useRoute[#useRoute + 1] = mist.ground.buildWP(tempRoute[i], tempForm, tempSpeed)
			end

			if pType and string.lower(pType) == 'doubleback' then
				local curRoute = mist.utils.deepCopy(useRoute)
				for i = #curRoute, 2, -1 do
					useRoute[#useRoute + 1] = mist.ground.buildWP(curRoute[i], curRoute[i].action, curRoute[i].speed)
				end
			end

			useRoute[1].action = useRoute[#useRoute].action -- make it so the first WP matches the last WP
		end

		local cTask3 = {}
		local newPatrol = {}
		newPatrol.route = useRoute
		newPatrol.gpData = gpData:getName()
		cTask3[#cTask3 + 1] = 'mist.ground.patrolRoute('
		cTask3[#cTask3 + 1] = mist.utils.oneLineSerialize(newPatrol)
		cTask3[#cTask3 + 1] = ')'
		cTask3 = table.concat(cTask3)
		local tempTask = {
			id = 'WrappedAction',
			params = {
				action = {
					id = 'Script',
					params = {
						command = cTask3,

					},
				},
			},
		}
		
		useRoute[#useRoute].task = tempTask
		log:info(useRoute)
		mist.goRoute(gpData, useRoute)

		return
	end

	function mist.ground.patrol(gpData, pType, form, speed)
		local vars = {}

		if type(gpData) == 'table' and gpData:getName() then
			gpData = gpData:getName()
		end

		vars.useGroupRoute = gpData
		vars.gpData = gpData
		vars.pType = pType
		vars.offRoadForm = form
		vars.speed = speed

		mist.ground.patrolRoute(vars)

		return
	end

	-- No longer accepts path
	function mist.ground.buildWP(point, overRideForm, overRideSpeed)

		local wp = {}
		wp.x = point.x

		if point.z then
			wp.y = point.z
		else
			wp.y = point.y
		end
		local form, speed

		if point.speed and not overRideSpeed then
			wp.speed = point.speed
		elseif type(overRideSpeed) == 'number' then
			wp.speed = overRideSpeed
		else
			wp.speed = mist.utils.kmphToMps(20)
		end

		if point.form and not overRideForm then
			form = point.form
		else
			form = overRideForm
		end

		if not form then
			wp.action = 'Cone'
		else
			form = string.lower(form)
			if form == 'off_road' or form == 'off road' then
				wp.action = 'Off Road'
			elseif form == 'on_road' or form == 'on road' then
				wp.action = 'On Road'
			elseif form == 'rank' or form == 'line_abrest' or form == 'line abrest' or form == 'lineabrest'then
				wp.action = 'Rank'
			elseif form == 'cone' then
				wp.action = 'Cone'
			elseif form == 'diamond' then
				wp.action = 'Diamond'
			elseif form == 'vee' then
				wp.action = 'Vee'
			elseif form == 'echelon_left' or form == 'echelon left' or form == 'echelonl' then
				wp.action = 'EchelonL'
			elseif form == 'echelon_right' or form == 'echelon right' or form == 'echelonr' then
				wp.action = 'EchelonR'
			else
				wp.action = 'Cone' -- if nothing matched
			end
		end

		wp.type = 'Turning Point'

		return wp

	end

	function mist.fixedWing.buildWP(point, WPtype, speed, alt, altType)

		local wp = {}
		wp.x = point.x

		if point.z then
			wp.y = point.z
		else
			wp.y = point.y
		end

		if alt and type(alt) == 'number' then
			wp.alt = alt
		else
			wp.alt = 2000
		end

		if altType then
			altType = string.lower(altType)
			if altType == 'radio' or altType == 'agl' then
				wp.alt_type = 'RADIO'
			elseif altType == 'baro' or altType == 'asl' then
				wp.alt_type = 'BARO'
			end
		else
			wp.alt_type = 'RADIO'
		end

		if point.speed then
			speed = point.speed
		end

		if point.type then
			WPtype = point.type
		end

		if not speed then
			wp.speed = mist.utils.kmphToMps(500)
		else
			wp.speed = speed
		end

		if not WPtype then
			wp.action =	'Turning Point'
		else
			WPtype = string.lower(WPtype)
			if WPtype == 'flyover' or WPtype == 'fly over' or WPtype == 'fly_over' then
				wp.action =	'Fly Over Point'
			elseif WPtype == 'turningpoint' or WPtype == 'turning point' or WPtype == 'turning_point' then
				wp.action =	'Turning Point'
			else
				wp.action = 'Turning Point'
			end
		end

		wp.type = 'Turning Point'
		return wp
	end

	function mist.heli.buildWP(point, WPtype, speed, alt, altType)

		local wp = {}
		wp.x = point.x

		if point.z then
			wp.y = point.z
		else
			wp.y = point.y
		end

		if alt and type(alt) == 'number' then
			wp.alt = alt
		else
			wp.alt = 500
		end

		if altType then
			altType = string.lower(altType)
			if altType == 'radio' or altType == 'agl' then
				wp.alt_type = 'RADIO'
			elseif altType == 'baro' or altType == 'asl' then
				wp.alt_type = 'BARO'
			end
		else
			wp.alt_type = 'RADIO'
		end

		if point.speed then
			speed = point.speed
		end

		if point.type then
			WPtype = point.type
		end

		if not speed then
			wp.speed = mist.utils.kmphToMps(200)
		else
			wp.speed = speed
		end

		if not WPtype then
			wp.action =	'Turning Point'
		else
			WPtype = string.lower(WPtype)
			if WPtype == 'flyover' or WPtype == 'fly over' or WPtype == 'fly_over' then
				wp.action =	'Fly Over Point'
			elseif WPtype == 'turningpoint' or WPtype == 'turning point' or WPtype == 'turning_point' then
				wp.action = 'Turning Point'
			else
				wp.action =	'Turning Point'
			end
		end

		wp.type = 'Turning Point'
		return wp
	end

	-- need to return a Vec3 or Vec2?
	function mist.getRandPointInCircle(p, radius, innerRadius, maxA, minA)
		local point = mist.utils.makeVec3(p)
        local theta = 2*math.pi*math.random()
		local minR = innerRadius or 0
		if maxA and not minA then
			theta = math.rad(math.random(0, maxA - math.random()))
		elseif maxA and minA and minA < maxA then
			theta = math.rad(math.random(minA, maxA) - math.random())
		end
		local rad = math.random() + math.random()
		if rad > 1 then
			rad = 2 - rad
		end

		local radMult
		if minR and minR <= radius then
			--radMult = (radius - innerRadius)*rad + innerRadius
			radMult = radius * math.sqrt((minR^2 + (radius^2 - minR^2) * math.random()) / radius^2)
		else
			radMult = radius*rad
		end

		local rndCoord
		if radius > 0 then
			rndCoord = {x = math.cos(theta)*radMult + point.x, y = math.sin(theta)*radMult + point.z}
		else
			rndCoord = {x = point.x, y = point.z}
		end
		return rndCoord
	end

	function mist.getRandomPointInZone(zoneName, innerRadius, maxA, minA)
		if type(zoneName) == 'string' and type(trigger.misc.getZone(zoneName)) == 'table' then
			return mist.getRandPointInCircle(trigger.misc.getZone(zoneName).point, trigger.misc.getZone(zoneName).radius, innerRadius, maxA, minA)
		end
		return false
	end
	
	function mist.getRandomPointInPoly(zone)
		local avg = mist.getAvgPoint(zone)
		local radius = 0
		local minR = math.huge
		local newCoord = {}
		for i = 1, #zone do
			if mist.utils.get2DDist(avg, zone[i]) > radius then
				radius = mist.utils.get2DDist(avg, zone[i])
			end
			if mist.utils.get2DDist(avg, zone[i]) < minR then
				minR = mist.utils.get2DDist(avg, zone[i])
			end
		end
		local lSpawnPos = {}
		for j = 1, 100 do
			newCoord = mist.getRandPointInCircle(avg, radius)
			if mist.pointInPolygon(newCoord, zone) then
				break
			end
			if j == 100 then
				newCoord = mist.getRandPointInCircle(avg, 50000)
				log:warn("Failed to find point in poly; Giving random point from center of the poly")
			end
		end
		return newCoord
	end

	function mist.groupToRandomPoint(vars)
		local group = vars.group --Required
		local point = vars.point --required
		local radius = vars.radius or 0
		local innerRadius = vars.innerRadius
		local form = vars.form or 'Cone'
		local heading = vars.heading or math.random()*2*math.pi
		local headingDegrees = vars.headingDegrees
		local speed = vars.speed or mist.utils.kmphToMps(20)


		local useRoads
		if not vars.disableRoads then
			useRoads = true
		else
			useRoads = false
		end

		local path = {}

		if headingDegrees then
			heading = headingDegrees*math.pi/180
		end

		if heading >= 2*math.pi then
			heading = heading - 2*math.pi
		end

		local rndCoord = mist.getRandPointInCircle(point, radius, innerRadius)

		local offset = {}
		local posStart = mist.getLeadPos(group)
		if posStart then
			offset.x = mist.utils.round(math.sin(heading - (math.pi/2)) * 50 + rndCoord.x, 3)
			offset.z = mist.utils.round(math.cos(heading + (math.pi/2)) * 50 + rndCoord.y, 3)
			path[#path + 1] = mist.ground.buildWP(posStart, form, speed)


			if useRoads == true and ((point.x - posStart.x)^2 + (point.z - posStart.z)^2)^0.5 > radius * 1.3 then
				path[#path + 1] = mist.ground.buildWP({x = posStart.x + 11, z = posStart.z + 11}, 'off_road', speed)
				path[#path + 1] = mist.ground.buildWP(posStart, 'on_road', speed)
				path[#path + 1] = mist.ground.buildWP(offset, 'on_road', speed)
			else
				path[#path + 1] = mist.ground.buildWP({x = posStart.x + 25, z = posStart.z + 25}, form, speed)
			end
		end
		path[#path + 1] = mist.ground.buildWP(offset, form, speed)
		path[#path + 1] = mist.ground.buildWP(rndCoord, form, speed)

		mist.goRoute(group, path)

		return
	end

	function mist.groupRandomDistSelf(gpData, dist, form, heading, speed)
		local pos = mist.getLeadPos(gpData)
		local fakeZone = {}
		fakeZone.radius = dist or math.random(300, 1000)
		fakeZone.point = {x = pos.x, y = pos.y, z = pos.z}
		mist.groupToRandomZone(gpData, fakeZone, form, heading, speed)

		return
	end

	function mist.groupToRandomZone(gpData, zone, form, heading, speed)
		if type(gpData) == 'string' then
			gpData = Group.getByName(gpData)
		end

		if type(zone) == 'string' then
			zone = trigger.misc.getZone(zone)
		elseif type(zone) == 'table' and not zone.radius then
			zone = trigger.misc.getZone(zone[math.random(1, #zone)])
		end

		if speed then
			speed = mist.utils.kmphToMps(speed)
		end

		local vars = {}
		vars.group = gpData
		vars.radius = zone.radius
		vars.form = form
		vars.headingDegrees = heading
		vars.speed = speed
		vars.point = mist.utils.zoneToVec3(zone)

		mist.groupToRandomPoint(vars)

		return
	end

	function mist.isTerrainValid(coord, terrainTypes) -- vec2/3 and enum or table of acceptable terrain types
		if coord.z then
			coord.y = coord.z
		end
		local typeConverted = {}

		if type(terrainTypes) == 'string' then -- if its a string it does this check
			for constId, constData in pairs(land.SurfaceType) do
				if string.lower(constId) == string.lower(terrainTypes) or string.lower(constData) == string.lower(terrainTypes) then
					table.insert(typeConverted, constId)
				end
			end
		elseif type(terrainTypes) == 'table' then -- if its a table it does this check
			for typeId, typeData in pairs(terrainTypes) do
				for constId, constData in pairs(land.SurfaceType) do
					if string.lower(constId) == string.lower(typeData) or string.lower(constData) == string.lower(typeData) then
						table.insert(typeConverted, constId)
					end
				end
			end
		end
		for validIndex, validData in pairs(typeConverted) do
			if land.getSurfaceType(coord) == land.SurfaceType[validData] then
				log:info('Surface is : $1', validData)
                return true
			end
		end
		return false
	end

	function mist.terrainHeightDiff(coord, searchSize)
		local samples = {}
		local searchRadius = 5
		if searchSize then
			searchRadius = searchSize
		end
		if type(coord) == 'string' then
			coord = mist.utils.zoneToVec3(coord)
		end

		coord = mist.utils.makeVec2(coord)

		samples[#samples + 1] = land.getHeight(coord)
		for i = 0, 360, 30 do
			samples[#samples + 1] = land.getHeight({x = (coord.x + (math.sin(math.rad(i))*searchRadius)), y = (coord.y + (math.cos(math.rad(i))*searchRadius))})
			if searchRadius >= 20 then -- if search radius is sorta large, take a sample halfway between center and outer edge
				samples[#samples + 1] = land.getHeight({x = (coord.x + (math.sin(math.rad(i))*(searchRadius/2))), y = (coord.y + (math.cos(math.rad(i))*(searchRadius/2)))})
			end
		end
		local tMax, tMin = 0, 1000000
		for index, height in pairs(samples) do
			if height > tMax then
				tMax = height
			end
			if height < tMin then
				tMin = height
			end
		end
		return mist.utils.round(tMax - tMin, 2)
	end

	function mist.groupToPoint(gpData, point, form, heading, speed, useRoads)
		if type(point) == 'string' then
			point = trigger.misc.getZone(point)
		end
		if speed then
			speed = mist.utils.kmphToMps(speed)
		end

		local vars = {}
		vars.group = gpData
		vars.form = form
		vars.headingDegrees = heading
		vars.speed = speed
		vars.disableRoads = useRoads
		vars.point = mist.utils.zoneToVec3(point)
		mist.groupToRandomPoint(vars)

		return
	end

	function mist.getLeadPos(group)
		if type(group) == 'string' then -- group name
			group = Group.getByName(group)
		end
		
		local units = group:getUnits()

		local leader = units[1]
		if Unit.getLife(leader) == 0 or not Unit.isExist(leader) then	-- SHOULD be good, but if there is a bug, this code future-proofs it then.
			local lowestInd = math.huge
			for ind, unit in pairs(units) do
				if Unit.isExist(unit) and ind < lowestInd then
					lowestInd = ind
					return unit:getPosition().p
				end
			end
		end
		if leader and Unit.isExist(leader) then	-- maybe a little too paranoid now...
			return leader:getPosition().p
		end
	end

end

--- Database tables.
-- @section mist.DBs

--- Mission data
-- @table mist.DBs.missionData
-- @field startTime mission start time
-- @field theatre mission theatre/map e.g. Caucasus
-- @field version mission version
-- @field files mission resources

--- Tables used as parameters.
-- @section varTables

--- mist.flagFunc.units_in_polygon parameter table.
-- @table unitsInPolygonVars
-- @tfield table unit name table @{UnitNameTable}.
-- @tfield table zone table defining a polygon.
-- @tfield number|string flag flag to set to true.
-- @tfield[opt] number|string stopflag if set to true the function
-- will stop evaluating.
-- @tfield[opt] number maxalt maximum altitude (MSL) for the
-- polygon.
-- @tfield[opt] number req_num minimum number of units that have
-- to be in the polygon.
-- @tfield[opt] number interval sets the interval for
-- checking if units are inside of the polygon in seconds. Default: 1.
-- @tfield[opt] boolean toggle switch the flag to false if required
-- conditions are not met. Default: false.
-- @tfield[opt] table unitTableDef
--- Logger class.
-- @type mist.Logger
do -- mist.Logger scope
	mist.Logger = {}

	--- parses text and substitutes keywords with values from given array.
	-- @param text string containing keywords to substitute with values
	-- or a variable.
	-- @param ... variables to use for substitution in string.
	-- @treturn string new string with keywords substituted or
	-- value of variable as string.
	local function formatText(text, ...)
		if type(text) ~= 'string' then
			if type(text) == 'table' then
				text = mist.utils.oneLineSerialize(text)
			else
				text = tostring(text)
			end
		else
			for index,value in ipairs(arg) do
				-- TODO: check for getmetatabel(value).__tostring
				if type(value) == 'table' then
					value = mist.utils.oneLineSerialize(value)
				else
					value = tostring(value)
				end
				text = text:gsub('$' .. index, value)
			end
		end
    local fName = nil
    local cLine = nil
		if debug then
			local dInfo = debug.getinfo(3)
			fName = dInfo.name
			cLine = dInfo.currentline
			-- local fsrc = dinfo.short_src
			--local fLine = dInfo.linedefined
		end
		if fName and cLine then
			return fName .. '|' .. cLine .. ': ' .. text
		elseif cLine then
			return cLine .. ': ' .. text
		else
			return ' ' .. text
		end
	end

	local function splitText(text)
		local tbl = {}
		while text:len() > 4000 do
			local sub = text:sub(1, 4000)
			text = text:sub(4001)
			table.insert(tbl, sub)
		end
		table.insert(tbl, text)
		return tbl
	end

	--- Creates a new logger.
	-- Each logger has it's own tag and log level.
	-- @tparam string tag tag which appears at the start of
	-- every log line produced by this logger.
	-- @tparam[opt] number|string level the log level defines which messages
	-- will be logged and which will be omitted. Log level 3 beeing the most verbose
	-- and 0 disabling all output. This can also be a string. Allowed strings are:
	-- "none" (0), "error" (1), "warning" (2) and "info" (3).
	-- @usage myLogger = mist.Logger:new("MyScript")
	-- @usage myLogger = mist.Logger:new("MyScript", 2)
	-- @usage myLogger = mist.Logger:new("MyScript", "info")
	-- @treturn mist.Logger
	function mist.Logger:new(tag, level)
		local l = {tag = tag}
		setmetatable(l, self)
		self.__index = self
		l:setLevel(level)
		return l
	end

	--- Sets the level of verbosity for this logger.
	-- @tparam[opt] number|string level the log level defines which messages
	-- will be logged and which will be omitted. Log level 3 beeing the most verbose
	-- and 0 disabling all output. This can also[ be a string. Allowed strings are:
	-- "none" (0), "error" (1), "warning" (2) and "info" (3).
	-- @usage myLogger:setLevel("info")
	-- @usage -- log everything
	--myLogger:setLevel(3)
	function mist.Logger:setLevel(level)
		if not level then
			self.level = 2
		else
			if type(level) == 'string' then
				if level == 'none' or level == 'off' then
					self.level = 0
				elseif level == 'error' then
					self.level = 1
				elseif level == 'warning' or level == 'warn' then
					self.level = 2
				elseif level == 'info' then
					self.level = 3
				end
			elseif type(level) == 'number' then
				self.level = level
			else
				self.level = 2
			end
		end
	end

	--- Logs error and shows alert window.
	-- This logs an error to the dcs.log and shows a popup window,
	-- pausing the simulation. This works always even if logging is
	-- disabled by setting a log level of "none" or 0.
	-- @tparam string text the text with keywords to substitute.
	-- @param ... variables to be used for substitution.
	-- @usage myLogger:alert("Shit just hit the fan! WEEEE!!!11")
	function mist.Logger:alert(text, ...)
		text = formatText(text, unpack(arg))
		if text:len() > 4000 then
			local texts = splitText(text)
			for i = 1, #texts do
				if i == 1 then
					env.error(self.tag .. '|' .. texts[i], true)
				else
					env.error(texts[i])
				end
			end
		else
			env.error(self.tag .. '|' .. text, true)
		end
	end

	--- Logs a message, disregarding the log level.
	-- @tparam string text the text with keywords to substitute.
	-- @param ... variables to be used for substitution.
	-- @usage myLogger:msg("Always logged!")
	function mist.Logger:msg(text, ...)
		text = formatText(text, unpack(arg))
		if text:len() > 4000 then
			local texts = splitText(text)
			for i = 1, #texts do
				if i == 1 then
					env.info(self.tag .. '|' .. texts[i])
				else
					env.info(texts[i])
				end
			end
		else
			env.info(self.tag .. '|' .. text)
		end
	end

	--- Logs an error.
	-- logs a message prefixed with this loggers tag to dcs.log as
	-- long as at least the "error" log level (1) is set.
	-- @tparam string text the text with keywords to substitute.
	-- @param ... variables to be used for substitution.
	-- @usage myLogger:error("Just an error!")
	-- @usage myLogger:error("Foo is $1 instead of $2", foo, "bar")
	function mist.Logger:error(text, ...)
		if self.level >= 1 then
			text = formatText(text, unpack(arg))
			if text:len() > 4000 then
				local texts = splitText(text)
				for i = 1, #texts do
					if i == 1 then
						env.error(self.tag .. '|' .. texts[i])
					else
						env.error(texts[i])
					end
				end
			else
				env.error(self.tag .. '|' .. text, mistSettings.errorPopup)
			end
		end
	end

	--- Logs a warning.
	-- logs a message prefixed with this loggers tag to dcs.log as
	-- long as at least the "warning" log level (2) is set.
	-- @tparam string text the text with keywords to substitute.
	-- @param ... variables to be used for substitution.
	-- @usage myLogger:warn("Mother warned you! Those $1 from the interwebs are $2", {"geeks", 1337})
	function mist.Logger:warn(text, ...)
		if self.level >= 2 then
			text = formatText(text, unpack(arg))
			if text:len() > 4000 then
				local texts = splitText(text)
				for i = 1, #texts do
					if i == 1 then
						env.warning(self.tag .. '|' .. texts[i])
					else
						env.warning(texts[i])
					end
				end
			else
				env.warning(self.tag .. '|' .. text, mistSettings.warnPopup)
			end
		end
	end

	--- Logs a info.
	-- logs a message prefixed with this loggers tag to dcs.log as
	-- long as the highest log level (3) "info" is set.
	-- @tparam string text the text with keywords to substitute.
	-- @param ... variables to be used for substitution.
	-- @see warn
	function mist.Logger:info(text, ...)
		if self.level >= 3 then
			text = formatText(text, unpack(arg))
			if text:len() > 4000 then
				local texts = splitText(text)
				for i = 1, #texts do
					if i == 1 then
						env.info(self.tag .. '|' .. texts[i])
					else
						env.info(texts[i])
					end
				end
			else
				env.info(self.tag .. '|' .. text, mistSettings.infoPopup)
			end
		end
	end

end


-- initialize mist
mist.init()
env.info(('Mist version ' .. mist.majorVersion .. '.' .. mist.minorVersion .. '.' .. mist.build .. ' loaded.'))

-- vim: noet:ts=2:sw=2
