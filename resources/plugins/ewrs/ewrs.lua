--[[
	Early Warning Radar Script - 1.5.3 - 07/11/2016

	Allows use of units with radars to provide Bearing Range and Altitude information via text display to player aircraft

	Features:
		- Uses in-game radar information to detect targets so terrain masking, beaming, low altitude flying, etc is effective for avoiding detection
		- Dynamic. If valid units with radar are created during a mission (eg. via chopper with CTLD), they will be added to the EWRS radar network
		- Can allow / disable BRA messages to fighters or sides
		- Uses player aircraft or mission bullseye for BRA reference, can be changed via F10 radio menu or restricted to one reference in the script settings
		- Can switch between imperial (feet, knots, NM) or metric (meters, km/h, km) measurements using F10 radio menu
		- Ability to change the message display time and automated update interval
		- Can choose to disable automated messages and allow players to request BRA from F10 menu
		- Can allow players to request Bogey Dope at any time through F10 radio menu

	Built and Tested in DCS 1.5 - See https://github.com/Bob7heBuilder/EWRS for the latest version

	This script uses MIST 4.0.57 or later - https://github.com/mrSkortch/MissionScriptingTools

	At the moment, because of limitations within DCS to not show messages to individual units, the reference, measurements, and messages
	are done per group. So a group of 4 fighters will each receive 4 BRA messages. Each message however, will have the player's name
	in it, that its refering to. Its unfortunate, but nothing I can do about it.

	Changes:
	- 1.3 - Added Option to allow picture report to be requested thru F10 menu instead of an automated display
			- Fixed bug where a known unit type would sometimes still display as ???
	- 1.4 - Added setting to be able to limit the amount of threats displayed in a picture report
			- Added option to enable Bogey Dopes
				* Mission designer can turn on / off in script settings
				* Pilots can request thru the F10 menu and it will show the BRA to the nearest hostile aircraft that has
				been detected. It will always reference the requesting pilot's own aircraft.
			- Finally implemented a cleaner workaround for some ground units being detected and listed in picture report
	- 1.4.1 - Added some ships to search radar list, you will need to remove the comment markers (--) at the start of the line to activate
	- 1.5 - Added ability to request picture of friendly aircraft positions referencing your own aircraft - Mission designer chooses if this feature is active or not
	- 1.5.1 - Added Gazelle to acCategories
	- 1.5.2 - Added F5E to acCategories
	- 1.5.3 - Fixed bug with maxThreatDisplay set at 0 not displaying any threats
			- Added Mistral Gazelle
			- Added C-101CC
]]

ewrs = {} --DO NOT REMOVE
ewrs.HELO = 1
ewrs.ATTACK = 2
ewrs.FIGHTER = 3

----SCRIPT OPTIONS----

ewrs.messageUpdateInterval = 30 --How often EWRS will update automated BRA messages (seconds)
ewrs.messageDisplayTime = 25 --How long EWRS BRA messages will show for (seconds)
ewrs.restrictToOneReference = false -- Disables the ability to change the BRA calls from pilot's own aircraft or bullseye. If this is true, set ewrs.defaultReference to the option you want to restrict to.
ewrs.defaultReference = "self" --The default reference for BRA calls - can be changed via f10 radio menu if ewrs.restrictToOneReference is false (self or bulls)
ewrs.defaultMeasurements = "imperial" --Default measurement units - can be changed via f10 radio menu (imperial or metric)
ewrs.disableFightersBRA = false -- disables BRA messages to fighters when true
ewrs.enableRedTeam = true -- enables / disables EWRS for the red team
ewrs.enableBlueTeam = true -- enables / disables EWRS for the blue team
ewrs.disableMessageWhenNoThreats = true -- disables message when no threats are detected - Thanks Rivvern - NOTE: If using ewrs.onDemand = true, this has no effect
ewrs.useImprovedDetectionLogic = true --this makes the messages more realistic. If the radar doesn't know the type or distance to the detected threat, it will be reflected in the picture report / BRA message
ewrs.onDemand = false --Setting to true will disable the automated messages to everyone and will add an F10 menu to get picture / BRA message.
ewrs.maxThreatDisplay = 5 -- Max amounts of threats to display on picture report (0 will display all)
ewrs.allowBogeyDope = true -- Allows pilots to request a bogey dope even with the automated messages running. It will display only the cloest threat, and will always reference the players own aircraft.
ewrs.allowFriendlyPicture = true -- Allows pilots to request picture of friendly aircraft
ewrs.maxFriendlyDisplay = 5 -- Limits the amount of friendly aircraft shown on friendly picture

--[[
Units with radar to use as part of the EWRS radar network
If you want to shorten the range of SAM radar detection, use their track radars instead of their search radars
NOTE that track radars require a search radar to detect targets (but the search radars do not need to be included in the list)
I haven't tested detection with ships (that have radar), but should work.
]]
ewrs.validSearchRadars = {
"p-10 s125 sr",			--SA-3 Search Radar
"Kub 1S91 str",			--SA-6 Search and Track Radar
"S-300PS 64H6E sr",		--SA-10 Search Radar
"S-300 PS 40B6MD sr",	--SA-10 Search Radar
"SA-11 Buk SR 9518M1",	--SA-11 Search Radar
"55G6 EWR",				--Early Warning Radar
"1L13 EWR",				--Early Warning Radar
"A-50",					--AWACS
"E-2D",					--AWACS
"E-3A",					--AWACS
"Roland Radar",			--Roland Search Radar
"Hawk sr",				--Hawk SAM Search Radar
"Patriot str",			--Patriot SAM Search and Track Radar

--Ships - I've left these commented out because I don't know which ones have radar
--and which ones don't. Just remove the comment to activate them (the '--' at the start of the line)

--"MOSCOW",				-- CG 1164 Moskva
--"TICONDEROG",			-- CG-60 Normandy
--"PIOTR",				-- CGN 1144.2 Pyotr Velikiy
--"KUZNECOW",			-- CV 1143.5 Admiral Kuzentsov
--"VINSON",				-- CVN-70 Carl Vinson
--"REZKY",				-- FF 1135M Rezky
--"NEUSTRASH",			-- FFG 11540 Neustrashimy
--"PERRY",				-- FFG-7CL Oliver Hazzard Perry
--"ALBATROS",			-- FFL 1124.4 Grisha
--"MOLNIYA",			-- FSG 1241.1MP Molniya
}

--[[
Aircraft Type ENUMs
This is used to restrict BRA messages to fighters
Change the ewrs.TYPE for each aircraft (in ewrs.acCategories) to suit your needs
For now, BRA will be displayed to everyone unless ewrs.disableFightersBRA is true.
When this is true, anything in the list below that == ewrs.FIGHTER will NOT receive BRA messages
]]
ewrs.acCategories = { --Have I left anything out? Please let me know if I have
[ "A-10A"          ] = ewrs.ATTACK  ,
[ "A-10C"          ] = ewrs.ATTACK  ,
[ "Bf-109K-4"      ] = ewrs.ATTACK  ,
[ "C-101EB"        ] = ewrs.ATTACK  ,
[ "C-101CC"		   ] = ewrs.ATTACK  ,
[ "F-15C"          ] = ewrs.FIGHTER ,
[ "F-5E-3"		   ] = ewrs.ATTACK	,
[ "FW-190D9"       ] = ewrs.ATTACK  ,
[ "F-86F Sabre"	   ] = ewrs.FIGHTER ,
[ "Hawk"           ] = ewrs.ATTACK  ,
[ "Ka-50"          ] = ewrs.HELO    ,
[ "L-39C"		   ] = ewrs.ATTACK	,
[ "L-39ZA"         ] = ewrs.ATTACK  ,
[ "Mi-8MT"         ] = ewrs.HELO    ,
[ "MiG-15bis"      ] = ewrs.ATTACK  ,
[ "MiG-21Bis"      ] = ewrs.ATTACK  ,
[ "MiG-29A"		   ] = ewrs.FIGHTER	,
[ "MiG-29S"		   ] = ewrs.FIGHTER	,
[ "M-2000C"		   ] = ewrs.FIGHTER	,
[ "P-51D"          ] = ewrs.ATTACK	,
[ "SA342M"		   ] = ewrs.HELO	,
[ "SA342L"		   ] = ewrs.HELO	,
[ "SA342Mistral"   ] = ewrs.HELO	,
[ "Su-25"          ] = ewrs.ATTACK	,
[ "Su-25T"         ] = ewrs.ATTACK	,
[ "Su-27"          ] = ewrs.FIGHTER	,
[ "Su-33"		   ] = ewrs.FIGHTER ,
[ "TF-51D"         ] = ewrs.ATTACK	,
[ "UH-1H"          ] = ewrs.HELO	,
[ "J-11A"          ] = ewrs.FIGHTER	,
}

----END OF SCRIPT OPTIONS----


----INTERNAL FUNCTIONS ***** Be Careful changing things below here ***** ----


function ewrs.getDistance(obj1PosX, obj1PosZ, obj2PosX, obj2PosZ)
	local xDiff = obj1PosX - obj2PosX
	local yDiff = obj1PosZ - obj2PosZ
	return math.sqrt(xDiff * xDiff + yDiff * yDiff) -- meters
end

function ewrs.getBearing(obj1PosX, obj1PosZ, obj2PosX, obj2PosZ)
    local bearing = math.atan2(obj2PosZ - obj1PosZ, obj2PosX - obj1PosX)
    if bearing < 0 then
        bearing = bearing + 2 * math.pi
    end
    bearing = bearing * 180 / math.pi
    return bearing    -- degrees
end

function ewrs.getHeading(vec)
    local heading = math.atan2(vec.z,vec.x)
    if heading < 0 then
        heading = heading + 2 * math.pi
    end
    heading = heading * 180 / math.pi
    return heading -- degrees
end

function ewrs.getSpeed(velocity)
	local speed = math.sqrt(velocity.x^2 + velocity.y^2 + velocity.z^2) --m/s
	return speed -- m/s
end

function ewrs.update()
	timer.scheduleFunction(ewrs.update, nil, timer.getTime() + 5)
	ewrs.buildActivePlayers()
	ewrs.buildF10Menu()
end

function ewrs.buildThreatTable(activePlayer, bogeyDope)
	local function sortRanges(v1,v2)
		return v1.range < v2.range
	end

	local targets = {}
	if activePlayer.side == 2 then
		targets = ewrs.currentlyDetectedRedUnits
	else
		targets = ewrs.currentlyDetectedBlueUnits
	end

	local bogeyDope = bogeyDope or false
	local referenceX
	local referenceZ
	if ewrs.groupSettings[tostring(activePlayer.groupID)].reference == "self" or bogeyDope then
		local _self = Unit.getByName(activePlayer.unitname)
		local selfpos = _self:getPosition()
		referenceX = selfpos.p.x
		referenceZ = selfpos.p.z
	else
		local bullseye = coalition.getMainRefPoint(activePlayer.side)
		referenceX = bullseye.x
		referenceZ = bullseye.z
	end

	local threatTable = {}

	for k,v in pairs(targets) do
		local velocity = v["object"]:getVelocity()
		local bogeypos = v["object"]:getPosition()
		local bogeyType = nil
		if ewrs.useImprovedDetectionLogic then
			if v["type"] then
				bogeyType = v["object"]:getTypeName()
			else
				bogeyType = "  ???  "
			end
		else
			bogeyType = v["object"]:getTypeName()
		end

		local bearing = ewrs.getBearing(referenceX,referenceZ,bogeypos.p.x,bogeypos.p.z)
		local heading = ewrs.getHeading(velocity)
		local range = ewrs.getDistance(referenceX,referenceZ,bogeypos.p.x,bogeypos.p.z) -- meters
		local altitude = bogeypos.p.y --meters
		local speed = ewrs.getSpeed(velocity) --m/s

		if ewrs.groupSettings[tostring(activePlayer.groupID)].measurements == "metric" then
			range = range / 1000 --change to KM
			speed = mist.utils.mpsToKmph(speed)
			--altitude already in meters
		else
			range = mist.utils.metersToNM(range)
			speed = mist.utils.mpsToKnots(speed)
			altitude = mist.utils.metersToFeet(altitude)
		end

		if ewrs.useImprovedDetectionLogic then
			if not v["distance"] then
				range = ewrs.notAvailable
			end
		end

		local j = #threatTable + 1
		threatTable[j] = {}
		threatTable[j].unitType = bogeyType
		threatTable[j].bearing = bearing
		threatTable[j].range = range
		threatTable[j].altitude = altitude
		threatTable[j].speed = speed
		threatTable[j].heading = heading
	end

	table.sort(threatTable,sortRanges)

	return threatTable
end

function ewrs.outText(activePlayer, threatTable, bogeyDope, greeting)
	local status, result = pcall(function()

		local message = {}
		local altUnits
		local speedUnits
		local rangeUnits
		local bogeyDope = bogeyDope or false
		if ewrs.groupSettings[tostring(activePlayer.groupID)].measurements == "metric" then
			altUnits = "m"
			speedUnits = "Km/h"
			rangeUnits = "Km"
		else
			altUnits = "ft"
			speedUnits = "Knts"
			rangeUnits = "NM"
		end

		if #threatTable >= 1 then
			local maxThreats = nil
			local messageGreeting = nil
			if greeting == nil then
				if bogeyDope then
					maxThreats = 1
					messageGreeting = "EWRS Bogey Dope for: " .. activePlayer.player
				else
					if ewrs.maxThreatDisplay == 0 then
						maxThreats = 999
					else
						maxThreats = ewrs.maxThreatDisplay
					end
					messageGreeting = "EWRS Picture Report for: " .. activePlayer.player .. " -- Reference: " .. ewrs.groupSettings[tostring(activePlayer.groupID)].reference
				end
			else
				messageGreeting = greeting
				maxThreats = ewrs.maxFriendlyDisplay
			end

			--Display table
			table.insert(message, "\n")
			table.insert(message, messageGreeting)
			table.insert(message, "\n\n")
			table.insert(message, string.format( "%-16s", "TYPE"))
			table.insert(message, string.format( "%-12s", "BRG"))
			table.insert(message, string.format( "%-12s", "RNG"))
			table.insert(message, string.format( "%-21s", "ALT"))
			table.insert(message, string.format( "%-15s", "SPD"))
			table.insert(message, string.format( "%-3s", "HDG"))
			table.insert(message, "\n")

			for k = 1, maxThreats do
				if threatTable[k] == nil then break end
				table.insert(message, "\n")
				table.insert(message, string.format( "%-16s", threatTable[k].unitType))
				if threatTable[k].range == ewrs.notAvailable then
					table.insert(message, string.format( "%-12s", " "))
					table.insert(message, string.format( "%-12s", "POSITION"))
					table.insert(message, string.format( "%-21s", " "))
					table.insert(message, string.format( "%-15s", "UNKNOWN"))
					table.insert(message, string.format( "%-3s", " "))
				else
					table.insert(message, string.format( "%03d", threatTable[k].bearing))
					table.insert(message, string.format( "%8.1f %s", threatTable[k].range, rangeUnits))
					table.insert(message, string.format( "%9d %s", threatTable[k].altitude, altUnits))
					table.insert(message, string.format( "%9d %s", threatTable[k].speed, speedUnits))
					table.insert(message, string.format( "         %03d", threatTable[k].heading))
				end
				table.insert(message, "\n")
			end
			trigger.action.outTextForGroup(activePlayer.groupID, table.concat(message), ewrs.messageDisplayTime)
		else
			if (not ewrs.disableMessageWhenNoThreats) or (ewrs.onDemand) and greeting == nil then
				trigger.action.outTextForGroup(activePlayer.groupID, "\nEWRS Picture Report for: " .. activePlayer.player .. "\n\nNo targets detected", ewrs.messageDisplayTime)
			end
			if greeting ~= nil then
				trigger.action.outTextForGroup(activePlayer.groupID, "\nEWRS Friendly Picture for: " .. activePlayer.player .. "\n\nNo friendlies detected", ewrs.messageDisplayTime)
			end
		end
	end)
	if not status then
		env.error(string.format("EWRS outText Error: %s", result))
	end
end

function ewrs.displayMessageToAll()
	local status, result = pcall(function()
		timer.scheduleFunction(ewrs.displayMessageToAll, nil, timer.getTime() + ewrs.messageUpdateInterval)
		ewrs.findRadarUnits()
		ewrs.getDetectedTargets()
		for i = 1, #ewrs.activePlayers do
			if ewrs.groupSettings[tostring(ewrs.activePlayers[i].groupID)].messages then
				if ewrs.activePlayers[i].side == 1 and #ewrs.redEwrUnits > 0 or ewrs.activePlayers[i].side == 2 and #ewrs.blueEwrUnits > 0 then
					ewrs.outText(ewrs.activePlayers[i], ewrs.buildThreatTable(ewrs.activePlayers[i]))
				end -- if ewrs.activePlayers[i].side == 1 and #ewrs.redEwrUnits > 0 or ewrs.activePlayers[i].side == 2 and #ewrs.blueEwrUnits > 0 then
			end -- if ewrs.groupSettings[tostring(ewrs.activePlayers[i].groupID)].messages then
		end -- for i = 1, #ewrs.activePlayers do
	end)
	if not status then
		env.error(string.format("EWRS displayMessageToAll Error: %s", result))
	end
end

function ewrs.onDemandMessage(args)
	local status, result = pcall(function()
		ewrs.findRadarUnits()
		ewrs.getDetectedTargets()
		for i = 1, #ewrs.activePlayers do
			if ewrs.activePlayers[i].groupID == args[1] then
				ewrs.outText(ewrs.activePlayers[i], ewrs.buildThreatTable(ewrs.activePlayers[i],args[2]),args[2])
			end
		end
	end)
	if not status then
		env.error(string.format("EWRS onDemandMessage Error: %s", result))
	end
end

function ewrs.buildFriendlyTable(friendlyNames,activePlayer)
	local function sortRanges(v1,v2)
		return v1.range < v2.range
	end

	local units = {}
	for i =1, #friendlyNames do
		local unit = Unit.getByName(friendlyNames[i])
		if unit ~= nil and unit:isActive() then

			table.insert(units,unit)
		else
			--env.error("Friendly Picture - Unit not found: "..friendlyNames[i]) -- Client Planes that are not active will fall into here.
		end
	end

	local _self = Unit.getByName(activePlayer.unitname)
	local selfpos = _self:getPosition()
	local referenceX = selfpos.p.x
	local referenceZ = selfpos.p.z

	local friendlyTable = {}

	for k,v in pairs(units) do
		local velocity = v:getVelocity()
		local pos = v:getPosition()
		local bogeyType = v:getTypeName()
		if pos.p.x ~= selfpos.p.x and pos.p.z ~= selfpos.p.z then --same position as self, means its you!

			local bearing = ewrs.getBearing(referenceX,referenceZ,pos.p.x,pos.p.z)
			local heading = ewrs.getHeading(velocity)
			local range = ewrs.getDistance(referenceX,referenceZ,pos.p.x,pos.p.z) -- meters
			local altitude = pos.p.y --meters
			local speed = ewrs.getSpeed(velocity) --m/s

			if ewrs.groupSettings[tostring(activePlayer.groupID)].measurements == "metric" then
				range = range / 1000 --change to KM
				speed = mist.utils.mpsToKmph(speed)
				--altitude already in meters
			else
				range = mist.utils.metersToNM(range)
				speed = mist.utils.mpsToKnots(speed)
				altitude = mist.utils.metersToFeet(altitude)
			end

			local j = #friendlyTable + 1
			friendlyTable[j] = {}
			friendlyTable[j].unitType = bogeyType
			friendlyTable[j].bearing = bearing
			friendlyTable[j].range = range
			friendlyTable[j].altitude = altitude
			friendlyTable[j].speed = speed
			friendlyTable[j].heading = heading
		else
			--env.info("Friendly Picture - Found Self")
		end
	end

	table.sort(friendlyTable,sortRanges)

	return friendlyTable
end

function ewrs.friendlyPicture(args)
	local status, result = pcall(function()
		for i = 1, #ewrs.activePlayers do
			if ewrs.activePlayers[i].groupID == args[1] then
				local sideString = nil
				if  ewrs.activePlayers[i].side == 1 then
					sideString = "[red]"
				else
					sideString = "[blue]"
				end
				local filter = {sideString.."[helicopter]", sideString.."[plane]"}
				local friendlies = mist.makeUnitTable(filter) --find a way to do this only once if there is more then 1 person in a group
				local friendlyTable = ewrs.buildFriendlyTable(friendlies,ewrs.activePlayers[i])
				local greeting = "EWRS Friendly Picture for: " .. ewrs.activePlayers[i].player
				ewrs.outText(ewrs.activePlayers[i],friendlyTable,false,greeting)
			end
		end
	end)
	if not status then
		env.error(string.format("EWRS friendlyPicture Error: %s", result))
	end
end

function ewrs.buildActivePlayers()
	local status, result = pcall(function()
		local filter = { "[all][plane]","[all][helicopter]"}
		local all_vecs = mist.makeUnitTable(filter)
		ewrs.activePlayers = {}
		for i = 1, #all_vecs do
			local vec = Unit.getByName(all_vecs[i])
			if vec ~= nil and Unit.isActive(vec) then
				playerName = Unit.getPlayerName(vec)
				local groupID = ewrs.getGroupId(vec)
				if playerName ~= nil then
					unitCategory = ewrs.acCategories[Unit.getTypeName(vec)]
					if ewrs.disableFightersBRA and unitCategory == ewrs.FIGHTER then
						--DONT DO ANYTHING
					else
						local group = Unit.getGroup(vec)
						if ewrs.enableBlueTeam and Unit.getCoalition(vec) == 2 then
							ewrs.addPlayer(playerName, groupID, vec)
						elseif ewrs.enableRedTeam and Unit.getCoalition(vec) == 1 then
							ewrs.addPlayer(playerName, groupID, vec)
						end
					end
				end
			end
		end
	end) -- pcall

	if not status then
		env.error(string.format("EWRS buildActivePlayers Error: %s", result))
	end
end

--THANK YOU ciribob http://forums.eagle.ru/showpost.php?p=2499638&postcount=5
--And Stonehouse for pointing me there
function ewrs.getGroupId(_unit) --Temp fix for client groups not being accessable

    local _unitDB =  mist.DBs.unitsById[tonumber(_unit:getID())]
    if _unitDB ~= nil and _unitDB.groupId then
        return _unitDB.groupId
    end

    return nil
end

function ewrs.getGroupCategory(unit)
	local unitDB = mist.DBs.unitsById[tonumber(unit:getID())]
	 if unitDB ~= nil and unitDB.category then
        return unitDB.category
    end

    return nil
end

function ewrs.addPlayer(playerName, groupID, unit )
	local status, result = pcall(function()
		local i = #ewrs.activePlayers + 1
		ewrs.activePlayers[i] = {}
		ewrs.activePlayers[i].player = playerName
		ewrs.activePlayers[i].groupID = groupID
		ewrs.activePlayers[i].unitname = unit:getName()
		ewrs.activePlayers[i].side = unit:getCoalition()

		-- add default settings to settings table if it hasn't been done yet
		if ewrs.groupSettings[tostring(groupID)] == nil then
			ewrs.addGroupSettings(tostring(groupID))
		end
	end)
	if not status then
		env.error(string.format("EWRS addPlayer Error: %s", result))
	end
end

-- filters units so ones detected by multiple radar sites still only get listed once
-- Filters out anything that isn't a plane or helicopter
function ewrs.filterUnits(units)
	local newUnits = {}
	for k,v in pairs(units) do
		local valid = true
		if v["object"]:getCategory() ~= Object.Category.UNIT then --rare but i've had it detect missiles
			valid = false
		end
		if valid then --another check cause it seems AI radar can detected some ground units
			local category = ewrs.getGroupCategory(v["object"])
			if category ~= "plane" and category ~= "helicopter" then valid = false end
		end

		if valid then
			for nk,nv in pairs (newUnits) do --recursive loop, can't see a way around this
				if v["object"]:getName() == nv["object"]:getName() then
					valid = false
					--update already found unit incase the first detection(s) didn't know type or distance
					if v["type"] then
						nv["type"] = true
					end
					if v["distance"] then
						nv["distance"] = true
					end
				end
			end
		end

		if valid then
			table.insert(newUnits, v)
		end
	end
	return newUnits
end

function ewrs.getDetectedTargets()
	if #ewrs.blueEwrUnits > 0 then
		ewrs.currentlyDetectedRedUnits = ewrs.findDetectedTargets("red")
	end
	if #ewrs.redEwrUnits > 0 then
		ewrs.currentlyDetectedBlueUnits = ewrs.findDetectedTargets("blue")
	end
end

function ewrs.findDetectedTargets(side)
	local units = {}
	local ewrUnits = {}

	if side == "red" then
		ewrUnits = ewrs.blueEwrUnits
	elseif side == "blue" then
		ewrUnits = ewrs.redEwrUnits
	end

	for n = 1, #ewrUnits do
		local ewrUnit = Unit.getByName(ewrUnits[n])
		if ewrUnit ~= nil then
			local ewrControl = ewrUnit:getGroup():getController()
			local detectedTargets = ewrControl:getDetectedTargets(Controller.Detection.RADAR)
			for k,v in pairs (detectedTargets) do
				table.insert(units, v)
			end
		end
	end
	return ewrs.filterUnits(units)
end

function ewrs.findRadarUnits()
	local filter = {}
	if ewrs.enableBlueTeam and ewrs.enableRedTeam then
		filter = { "[all][plane]", "[all][vehicle]", "[all][ship]"}
	elseif ewrs.enableBlueTeam then
		filter = { "[blue][plane]", "[blue][vehicle]", "[blue][ship]"}
	elseif ewrs.enableRedTeam then
		filter = { "[red][plane]", "[red][vehicle]", "[red][ship]"}
	end
	local all_vecs = mist.makeUnitTable(filter)
	local redUnits = {}
	local blueUnits = {}

	for i = 1, #all_vecs do
		local vec = Unit.getByName(all_vecs[i])

		if vec ~= nil then
			if Unit.isActive(vec) then
				local vec_type = Unit.getTypeName(vec)
				for n = 1, #ewrs.validSearchRadars do
					if ewrs.validSearchRadars[n] == vec_type and Unit.getCoalition(vec) == 2 then
						table.insert(blueUnits, Unit.getName(vec))
						break
					end
					if ewrs.validSearchRadars[n] == vec_type and Unit.getCoalition(vec) == 1 then
						table.insert(redUnits, Unit.getName(vec))
						break
					end
				end --for n = 1, #ewrs.validSearchRadars do
			end --if Unit.isActive(vec) then
		end --if vec ~= nil then
	end --for i = 1, #all_vecs do
	ewrs.blueEwrUnits = blueUnits
	ewrs.redEwrUnits = redUnits
end

function ewrs.addGroupSettings(groupID)
	ewrs.groupSettings[groupID] = {}
	ewrs.groupSettings[groupID].reference = ewrs.defaultReference
	ewrs.groupSettings[groupID].measurements = ewrs.defaultMeasurements
	ewrs.groupSettings[groupID].messages = true
end

function ewrs.setGroupReference(args)
	local groupID = args[1]
	ewrs.groupSettings[tostring(groupID)].reference = args[2]
	trigger.action.outTextForGroup(groupID,"Reference changed to "..args[2],ewrs.messageDisplayTime)
end

function ewrs.setGroupMeasurements(args)
	local groupID = args[1]
	ewrs.groupSettings[tostring(groupID)].measurements = args[2]
	trigger.action.outTextForGroup(groupID,"Measurement units changed to "..args[2],ewrs.messageDisplayTime)
end

function ewrs.setGroupMessages(args)
	local groupID = args[1]
	local onOff
	if args[2] then onOff = "on" else onOff = "off" end
	ewrs.groupSettings[tostring(groupID)].messages = args[2]
	trigger.action.outTextForGroup(groupID,"Picture reports for group turned "..onOff,ewrs.messageDisplayTime)
end

function ewrs.buildF10Menu()
	local status, result = pcall(function()
		for i = 1, #ewrs.activePlayers do
			local groupID = ewrs.activePlayers[i].groupID
			local stringGroupID = tostring(groupID)
			if ewrs.builtF10Menus[stringGroupID] == nil then
				local rootPath = missionCommands.addSubMenuForGroup(groupID, "EWRS")

				if ewrs.allowBogeyDope then
					missionCommands.addCommandForGroup(groupID, "Request Bogey Dope",rootPath,ewrs.onDemandMessage,{groupID,true})
				end

				if ewrs.onDemand then
					missionCommands.addCommandForGroup(groupID, "Request Picture",rootPath,ewrs.onDemandMessage,{groupID})
				end

				if ewrs.allowFriendlyPicture then
					missionCommands.addCommandForGroup(groupID, "Request Friendly Picture",rootPath,ewrs.friendlyPicture,{groupID})
				end

				if not ewrs.restrictToOneReference then
					local referenceSetPath = missionCommands.addSubMenuForGroup(groupID,"Set GROUP's reference point", rootPath)
					missionCommands.addCommandForGroup(groupID, "Set to Bullseye",referenceSetPath,ewrs.setGroupReference,{groupID, "bulls"})
					missionCommands.addCommandForGroup(groupID, "Set to Self",referenceSetPath,ewrs.setGroupReference,{groupID, "self"})
				end

				local measurementsSetPath = missionCommands.addSubMenuForGroup(groupID,"Set GROUP's measurement units",rootPath)
				missionCommands.addCommandForGroup(groupID, "Set to Imperial (feet, knts)",measurementsSetPath,ewrs.setGroupMeasurements,{groupID, "imperial"})
				missionCommands.addCommandForGroup(groupID, "Set to Metric (meters, km/h)",measurementsSetPath,ewrs.setGroupMeasurements,{groupID, "metric"})

				if not ewrs.onDemand then
					local messageOnOffPath = missionCommands.addSubMenuForGroup(groupID, "Turn Picture Report On/Off",rootPath)
					missionCommands.addCommandForGroup(groupID, "Message ON", messageOnOffPath, ewrs.setGroupMessages, {groupID, true})
					missionCommands.addCommandForGroup(groupID, "Message OFF", messageOnOffPath, ewrs.setGroupMessages, {groupID, false})
				end

				ewrs.builtF10Menus[stringGroupID] = true
			end
		end
	end)

	if not status then
		env.error(string.format("EWRS buildF10Menu Error: %s", result))
	end
end

--temp fix for ground units being detected by radar - FIXED
--[[ Leaving this here just in case I introduce threat based filtering, saves me writing it again
ewrs.validThreats = {
["A-10A"] = true,
["A-10C"] = true,
["A-50"] = true,
["AH-1W"] = true,
["AH-64A"] = true,
["AH-64D"] = true,
["An-26B"] = true,
["An-30M"] = true,
["B-1B"] = true,
["B-52H"] = true,
["Bf-109K-4"] = true,
["C-101CC"] = true,
["C-101EB"] = true,
["C-130"] = true,
["C-17A"] = true,
["CH-47D"] = true,
["CH-53E"] = true,
["E-2D"] = true,
["E-2C"] = true,
["E-3A"] = true,
["F-111F"] = true,
["F-117A"] = true,
["F-14A"] = true,
["F-15C"] = true,
["F-15E"] = true,
["F-16A"] = true,
["F-16A MLU"] = true,
["F-16C bl.50"] = true,
["F-16C bl.52d"] = true,
["F-4E"] = true,
["F-5E"] = true,
["F-5E-3"] = true,
["F-86F Sabre"] = true,
["F/A-18A"] = true,
["F/A-18C"] = true,
["FW-190D9"] = true,
["Hawk"] = true,
["IL-76MD"] = true,
["IL-78M"] = true,
["KC-135"] = true,
["Ka-27"] = true,
["Ka-50"] = true,
["Ka-52"] = true,
["L-39C"] = true,
["L-39ZA"] = true,
["M-2000C"] = true,
["MQ-9 Reaper"] = true,
["Mi-24V"] = true,
["Mi-26"] = true,
["Mi-28N"] = true,
["Mi-8MT"] = true,
["MiG-15bis"] = true,
["MiG-21Bis"] = true,
["MiG-23MLD"] = true,
["MiG-25PD"] = true,
["MiG-25RBT"] = true,
["MiG-27K"] = true,
["MiG-29A"] = true,
["MiG-29G"] = true,
["MiG-29K"] = true,
["MiG-29S"] = true,
["MiG-31"] = true,
["Mirage 2000-5"] = true,
["OH-58D"] = true,
["P-51D"] = true,
["RQ-1A Predator"] = true,
["S-3B"] = true,
["S-3B Tanker"] = true,
["SH-3W"] = true,
["SH-60B"] = true,
["Su-17M4"] = true,
["Su-24M"] = true,
["Su-24MR"] = true,
["Su-25"] = true,
["Su-25T"] = true,
["Su-25TM"] = true,
["Su-27"] = true,
["Su-30"] = true,
["Su-33"] = true,
["Su-34"] = true,
["TF-51D"] = true,
["Tornado GR4"] = true,
["Tornado IDS"] = true,
["Tu-142"] = true,
["Tu-160"] = true,
["Tu-22M3"] = true,
["Tu-95MS"] = true,
["UH-1H"] = true,
["UH-60A"] = true,
["Yak-40"] = true,
}
]]

--SCRIPT INIT
ewrs.currentlyDetectedRedUnits = {}
ewrs.currentlyDetectedBlueUnits = {}
ewrs.redEwrUnits = {}
ewrs.blueEwrUnits = {}
ewrs.activePlayers = {}
ewrs.groupSettings = {}
ewrs.builtF10Menus = {}
ewrs.notAvailable = 999999

ewrs.update()
if not ewrs.onDemand then
	timer.scheduleFunction(ewrs.displayMessageToAll, nil, timer.getTime() + ewrs.messageUpdateInterval)
end
trigger.action.outText("EWRS by Steggles is now running",15)
env.info("EWRS Running")

--[[
TODO:
	- Add check on friendly picture to not give one if no AWACS / EWR units are active. Doesn't use radar info anyway. Maybe just leave it to help out people with SA? Feedback Please!!
	- Clean up functions and arguments from bogeyDope and friendly picture additions
	- Threat based filtering if theres interest.
]]