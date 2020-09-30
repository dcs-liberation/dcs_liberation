-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- VEAF move units for DCS World
-- By mitch (2018)
--
-- Features:
-- ---------
-- * Listen to marker change events and execute move commands, with optional parameters
-- * Possibilities : 
-- *    - move a specific group to a marker point, at a specific speed
-- *    - create a new tanker flightplan, moving a specific tanker group
-- * Works with all current and future maps (Caucasus, NTTR, Normandy, PG, ...)
--
-- Prerequisite:
-- ------------
-- * This script requires DCS 2.5.1 or higher and MIST 4.3.74 or higher.
-- * It also requires the base veaf.lua script library (version 1.0 or higher)
-- * It also requires the base veafMarkers.lua script library (version 1.0 or higher)
--
-- Load the script:
-- ----------------
-- 1.) Download the script and save it anywhere on your hard drive.
-- 2.) Open your mission in the mission editor.
-- 3.) Add a new trigger:
--     * TYPE   "4 MISSION START"
--     * ACTION "DO SCRIPT FILE"
--     * OPEN --> Browse to the location of MIST and click OK.
--     * ACTION "DO SCRIPT FILE"
--     * OPEN --> Browse to the location of veaf.lua and click OK.
--     * ACTION "DO SCRIPT FILE"
--     * OPEN --> Browse to the location of veafMarkers.lua and click OK.
--     * ACTION "DO SCRIPT FILE"
--     * OPEN --> Browse to the location of this script and click OK.
--     * ACTION "DO SCRIPT"
--     * set the script command to "veafMove.initialize()" and click OK.
-- 4.) Save the mission and start it.
-- 5.) Have fun :)
--
-- Basic Usage:
-- ------------
-- 1.) Place a mark on the F10 map.
-- 2.) As text enter "veaf move group" or "veaf move tanker"
-- 3.) Click somewhere else on the map to submit the new text.
-- 4.) The command will be processed. A message will appear to confirm this
-- 5.) The original mark will disappear.
--
-- Options:
-- --------
-- Type "_move group, name [groupname]" to move the specified group to the marker point
--      add ", speed [speed]" to make the group move and at the specified speed (in knots)
-- Type "_move tanker, name [groupname]" to create a new tanker flight plan and move the specified tanker.
--      add ", speed [speed]" to make the tanker move and execute its refuel mission at the specified speed (in knots)
--      add ", alt [altitude]" to specify the refuel leg altitude (in feet)
--
-- *** NOTE ***
-- * All keywords are CaSE inSenSITvE.
-- * Commas are the separators between options ==> They are IMPORTANT!
--
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- veafMove Table.
veafMove = {}

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Global settings. Stores the script constants
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Identifier. All output in DCS.log will start with this.
veafMove.Id = "MOVE - "

--- Version.
veafMove.Version = "1.6.0"

-- trace level, specific to this module
veafMove.Trace = false

--- Key phrase to look for in the mark text which triggers the command.
veafMove.Keyphrase = "_move"

veafMove.RadioMenuName = "MOVE"

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Do not change anything below unless you know what you are doing!
-------------------------------------------------------------------------------------------------------------------------------------------------------------

veafMove.rootPath = nil

--- Initial Marker id.
veafMove.markid = 20000

traceMarkerId = 6548
debugMarkers = {}

veafMove.Tankers = {}
-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Utility methods
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafMove.logInfo(message)
    veaf.logInfo(veafMove.Id .. message)
end

function veafMove.logDebug(message)
    veaf.logDebug(veafMove.Id .. message)
end

function veafMove.logTrace(message)
    if message and veafMove.Trace then
        veaf.logTrace(veafMove.Id .. message)
    end
end

function veafMove.logMarker(id, message, position, markersTable)
    if veafMove.Trace then 
        return veaf.logMarker(id, veafMove.Id, message, position, markersTable)
    end
end


-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Event handler functions.
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Function executed when a mark has changed. This happens when text is entered or changed.
function veafMove.onEventMarkChange(eventPos, event)
    if veafMove.executeCommand(eventPos, event.text, event.coalition) then 
        
        -- Delete old mark.
        veafMove.logTrace(string.format("Removing mark # %d.", event.idx))
        trigger.action.removeMark(event.idx)

    end
end

function veafMove.executeCommand(eventPos, eventText, eventCoalition, bypassSecurity)
    
    -- choose by default the coalition opposing the player who triggered the event
    local coalition = 1
    if eventCoalition == 1 then
        coalition = 2
    end

    -- Check if marker has a text and the veafMove.keyphrase keyphrase.
    if eventText ~= nil and eventText:lower():find(veafMove.Keyphrase) then

        -- Analyse the mark point text and extract the keywords.
        local options = veafMove.markTextAnalysis(eventText)
        local result = false

        if options then
            -- Check options commands
            if options.moveGroup then
                result = veafMove.moveGroup(eventPos, options.groupName, options.speed, options.altitude)
            elseif options.moveTanker then
                result = veafMove.moveTanker(eventPos, options.groupName, options.speed, options.altitude, options.hdg, options.distance)
            elseif options.moveAfac then
                result = veafMove.moveAfac(eventPos, options.groupName, options.speed, options.altitude)
            end
        else
            -- None of the keywords matched.
            return false
        end

        return result
    end
end
-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Analyse the mark text and extract keywords.
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Extract keywords from mark text.
function veafMove.markTextAnalysis(text)

    -- Option parameters extracted from the mark text.
    local switch = {}
    switch.moveGroup = false
    switch.moveTanker = false
    switch.moveAfac = false

    -- the name of the group to move ; mandatory
    switch.groupName = ""

    -- speed in knots
    switch.speed = -1 -- defaults to original speed

    -- tanker refuel leg altitude in feet
    switch.altitude = -1 -- defaults to tanker original altitude

    -- tanker refuel leg heading in degrees
    switch.hdg = nil -- defaults to original heading

    -- tanker refuel leg distance in degrees
    switch.distance = nil -- defaults to original distance

    -- Check for correct keywords.
    if text:lower():find(veafMove.Keyphrase .. " group") then
        switch.moveGroup = true
        switch.speed = 20
    elseif text:lower():find(veafMove.Keyphrase .. " tanker") then
        switch.moveTanker = true
        switch.speed = -1
        switch.altitude = -1
    elseif text:lower():find(veafMove.Keyphrase .. " afac") then
        switch.moveAfac = true
        switch.speed = 300
        switch.altitude = 15000
    else
        return nil
    end

    -- keywords are split by ","
    local keywords = veaf.split(text, ",")

    for _, keyphrase in pairs(keywords) do
        -- Split keyphrase by space. First one is the key and second, ... the parameter(s) until the next comma.
        local str = veaf.breakString(veaf.trim(keyphrase), " ")
        local key = str[1]
        local val = str[2]

        if key:lower() == "name" then
            -- Set group name
            veafMove.logDebug(string.format("Keyword name = %s", val))
            switch.groupName = val
        end

        if key:lower() == "speed" then
            -- Set speed.
            veafMove.logDebug(string.format("Keyword speed = %d", val))
            local nVal = tonumber(val)
            switch.speed = nVal
        end

        if key:lower() == "hdg" then
            -- Set heading.
            veafMove.logDebug(string.format("Keyword hdg = %d", val))
            local nVal = tonumber(val)
            switch.hdg = nVal
        end

        if key:lower() == "distance" then
            -- Set distance.
            veafMove.logDebug(string.format("Keyword distance = %d", val))
            local nVal = tonumber(val)
            switch.distance = nVal
        end

        if key:lower() == "alt" then
            -- Set altitude.
            veafMove.logDebug(string.format("Keyword alt = %d", val))
            local nVal = tonumber(val)
            switch.altitude = nVal
        end

    end

    -- check mandatory parameter "group"
    if not(switch.groupName) then return nil end
    return switch
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Group move command
-------------------------------------------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------------
-- veafMove.moveGroup
-- @param point eventPos
-- @param string groupName the group name to move on
-- @param float speed in knots
------------------------------------------------------------------------------
function veafMove.moveGroup(eventPos, groupName, speed, altitude)
    veafMove.logDebug("veafMove.moveGroup(groupName = " .. groupName .. ", speed = " .. speed .. ", altitude=".. altitude)
    veafMove.logDebug(string.format("veafMove.moveGroup: eventPos  x=%.1f z=%.1f", eventPos.x, eventPos.z))

    local result = veaf.moveGroupTo(groupName, eventPos, speed, altitude)
    if not(result) then
        trigger.action.outText(groupName .. ' not found for move group command' , 10)
    end
    return result
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Tanker move command
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafMove.moveTanker(eventPos, groupName, speed, alt, hdg, distance)
    veafMove.logDebug(string.format("veafMove.moveTanker(groupName=%s, speed=%s, alt=%s, hdg=%s, distance=%s)",tostring(groupName), tostring(speed), tostring(alt), tostring(hdg), tostring(distance)))
    veafMove.logTrace(string.format("eventPos=%s",veaf.p(eventPos)))
    if veafMove.Trace then veaf.cleanupLogMarkers(debugMarkers) end
    
	local unitGroup = Group.getByName(groupName)
	if unitGroup == nil then
        veafMove.logInfo(groupName .. ' not found for move tanker command')
		trigger.action.outText(groupName .. ' not found for move tanker command' , 10)
		return false
	end

    local tankerData = veaf.getGroupData(groupName)
    if not(tankerData) then
        local text = "Cannot move tanker " .. groupName .. " ; cannot find group"
        veafMove.logInfo(text)
        trigger.action.outText(text)
        return
    end

    local route = veaf.findInTable(tankerData, "route")
    local points = veaf.findInTable(route, "points")
    if points then
        veafMove.logTrace("found a " .. #points .. "-points route for tanker " .. groupName)
        -- modify the last 3 points
        local idxPoint1 = #points-2
        local idxPoint2 = #points-1
        local idxPoint3 = #points

        -- point1 is the point where the tanker should move
        local point1 = points[idxPoint1]
        veafMove.logTrace("found point1")
        traceMarkerId = veafMove.logMarker(traceMarkerId, "point1", point1, debugMarkers)
        local moveVector = {
            x = point1.x - eventPos.x,
            y = point1.y - eventPos.z,
        }
        veafMove.logTrace(string.format("moveVector=%s",veaf.p(moveVector)))
        -- move to event position
        point1.x = eventPos.x
        point1.y = eventPos.z
        if speed > -1 then 
            point1.speed = speed/1.94384  -- speed in m/s
        end
        if alt > -1 then 
            point1.alt = alt * 0.3048 -- in meters
        end
        veafMove.logTrace(string.format("newPoint1=%s",veaf.p(point1)))
        traceMarkerId = veafMove.logMarker(traceMarkerId, "newPoint1", point1, debugMarkers)

        -- point 2 is the start of the tanking Orbit
        local point2 = points[idxPoint2]
        local foundOrbit = false
        local task1 = veaf.findInTable(point2, "task")
        if task1 then
            local tasks = task1.params.tasks
            if (tasks) then
                veaf.mainLogTrace("found " .. #tasks .. " tasks")
                for j, task in pairs(tasks) do
                    veaf.mainLogTrace("found task #" .. j)
                    if task.params then
                        veaf.mainLogTrace("has .params")
                        if task.id and task.id == "Orbit" then
                            veaf.mainLogDebug("Found a ORBIT task for tanker " .. groupName)
                            foundOrbit = true
                            if speed > -1 then 
                                task.params.speed = speed/1.94384  -- speed in m/s
                                point2.speed = speed/1.94384  -- speed in m/s
                            end
                            if alt > -1 then 
                                task.params.altitude = alt * 0.3048 -- in meters
                                point2.alt = alt * 0.3048 -- in meters
                            end
                        end
                    end
                end
            end
        end
        if not foundOrbit then 
            local text = "Cannot move tanker " .. groupName .. " because it has no ORBIT task defined"
            veafMove.logInfo(text)
            trigger.action.outText(text)
            return
        end
        veafMove.logTrace("found point2")
        traceMarkerId = veafMove.logMarker(traceMarkerId, "point2", point2, debugMarkers)
        -- apply vector to position
        point2.x = point2.x - moveVector.x
        point2.y = point2.y - moveVector.y
        veafMove.logTrace(string.format("newPoint2=%s",veaf.p(point2)))
        traceMarkerId = veafMove.logMarker(traceMarkerId, "newPoint2", point2, debugMarkers)

        -- point 3 is the end of the tanking Orbit
        local point3 = points[idxPoint3]
        veafMove.logTrace("found point3")
        traceMarkerId = veafMove.logMarker(traceMarkerId, "point3", point3, debugMarkers)
        -- change geometry of tanking orbit, if hdg and/or distance are set
        if hdg ~= nil or distance ~= nil then 
            local lastVector = moveVector
            local distance = distance
            local hdg = hdg

            -- if distance is not set, compute distance between point2 and point3
            if distance == nil then
                distance = math.sqrt((point3.x - point2.x)^2+(point3.y - point2.y)^2)
            else
                -- convert distance to meters
                distance = mist.utils.NMToMeters(distance)
            end

            -- if hdg is not set, compute heading between point2 and point3
            if hdg == nil then
                hdg = math.floor(math.deg(math.atan2(point3.y - point2.y, point3.x - point2.x)))
                if hdg < 0 then
                  hdg = hdg + 360
                end
            end
            veafMove.logTrace(string.format("distance=%s",veaf.p(distance)))
            veafMove.logTrace(string.format("hdg=%s",veaf.p(hdg)))
            
            -- compute last move vector
            local headingRad = mist.utils.toRadian(hdg)
            veafMove.logTrace(string.format("headingRad=%s",veaf.p(headingRad)))
            lastVector = {
                x = distance * math.cos(headingRad),
                y = distance * math.sin(headingRad),
            }
            -- apply vector to position
            point3.x = point2.x + lastVector.x
            point3.y = point2.y + lastVector.y
        else
            -- apply vector to position
            point3.x = point3.x - moveVector.x
            point3.y = point3.y - moveVector.y
        end
        if speed > -1 then 
            point3.speed = speed/1.94384  -- speed in m/s
        end
        if alt > -1 then 
            point3.alt = alt * 0.3048 -- in meters
        end
        veafMove.logTrace("newpoint3="..veaf.p(point3))
        traceMarkerId = veafMove.logMarker(traceMarkerId, "newpoint3", point3, debugMarkers)

        -- replace whole mission
        veafMove.logDebug("Resetting moved tanker mission")
        -- replace the mission
        local mission = { 
            id = 'Mission', 
            params = tankerData
        }
        local controller = unitGroup:getController()
        controller:setTask(mission)
        
        return true
    else
        return false
    end
end

------------------------------------------------------------------------------
-- veafMove.moveAfac
-- @param point eventPos
-- @param string groupName 
-- @param float speed in knots
-- @param float hdg heading (0-359)
-- @param float distance in Nm
-- @param float alt in feet
------------------------------------------------------------------------------
function veafMove.moveAfac(eventPos, groupName, speed, alt)
    if not speed then
        speed = 300
    end
    if not alt then
        alt = 20000
    end
    veafMove.logDebug("veafMove.moveAfac(groupName = " .. groupName .. ", speed = " .. speed .. ", alt = " .. alt)
    veafMove.logDebug(string.format("veafMove.moveAfac: eventPos  x=%.1f z=%.1f", eventPos.x, eventPos.z))

	local unitGroup = Group.getByName(groupName)
	if unitGroup == nil then
        veafMove.logInfo(groupName .. ' not found for move afac command')
		trigger.action.outText(groupName .. ' not found for move afac command' , 10)
		return false
	end

	-- teleport position
	local teleportPosition = {
		["x"] = eventPos.x + 5 * 1852 * math.cos(mist.utils.toRadian(180)),
        ["y"] = eventPos.z + 5 * 1852 * math.sin(mist.utils.toRadian(180)),
        ["alt"] = alt * 0.3048 -- in meters
	}

    -- starting position
	local fromPosition = {
		["x"] = eventPos.x,
		["y"] = eventPos.z
	}
	
	local mission = { 
		id = 'Mission', 
		params = { 
			["communication"] = true,
			["start_time"] = 0,
			["task"] = "AFAC",
			route = { 
				points = { 
					-- first point
					[1] = { 
						["type"] = "Turning Point",
						["action"] = "Turning Point",
						["x"] = fromPosition.x,
						["y"] = fromPosition.y,
						["alt"] = alt * 0.3048, -- in meters
						["alt_type"] = "BARO", 
						["speed"] = speed/1.94384,  -- speed in m/s
						["speed_locked"] = boolean, 
						["task"] = 
						{
							["id"] = "ComboTask",
							["params"] = 
							{
                                ["tasks"] = 
                                {
                                    [1] = 
                                    {
                                        ["number"] = 1,
                                        ["auto"] = false,
                                        ["id"] = "Orbit",
                                        ["enabled"] = true,
                                        ["params"] = 
                                        {
                                            ["altitude"] = alt * 0.3048, -- in meters,
                                            ["pattern"] = "Circle",
                                            ["speed"] = speed/1.94384,  -- speed in m/s
                                            ["altitudeEdited"] = true,
                                            ["speedEdited"] = true,
                                        }, -- end of ["params"]
                                    }, -- end of [1]
                                }, -- end of ["tasks"]
                            }, -- end of ["params"]
						}, -- end of ["task"]
					}, -- enf of [1]
				}, 
			} 
		} 
	}

    local vars = { groupName = groupName, point = teleportPosition, action = "teleport" }
    local grp = mist.teleportToPoint(vars)

    -- JTAC needs to be invisible and immortal
    local _setImmortal = {
        id = 'SetImmortal',
        params = {
            value = true
        }
    }
    -- invisible to AI, Shagrat
    local _setInvisible = {
        id = 'SetInvisible',
        params = {
            value = true
        }
    }

    -- replace whole mission
    local controller = unitGroup:getController()
	controller:setTask(mission)
    Controller.setCommand(controller, _setImmortal)
    Controller.setCommand(controller, _setInvisible)
    
    return true
end

-- prepare tanker units
function veafMove.findAllTankers()
    local TankerTypeNames = {"KC130", "KC-135", "KC135MPRS", "KJ-2000", "IL-78M"}
    veafMove.logTrace(string.format("findAllTankers()"))
    local result = {}
    local units = mist.DBs.unitsByName -- local copy for faster execution
    for name, unit in pairs(units) do
        veafMove.logTrace(string.format("name=%s, unit.type=%s", veaf.p(name), veaf.p(unit.type)))
        --veafMove.logTrace(string.format("unit=%s", veaf.p(unit)))
        --local unit = Unit.getByName(name)
        if unit then 
            for _, tankerTypeName in pairs(TankerTypeNames) do
                if tankerTypeName:lower() == unit.type:lower() then
                    table.insert(result, unit.groupName)
                end
            end
        end
    end
    return result
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Radio menu and help
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Build a radio menu to move the Arco tanker
function veafMove.moveTankerToMe(parameters)
    local tankerName, unitName = veaf.safeUnpack(parameters)
    veafMove.logDebug(string.format("veafMove.moveTankerToMe(tankerName=%s, unitName=%s)",tankerName,unitName))
    local unit = Unit.getByName(unitName)
    if unit then
        veafMove.moveTanker(unit:getPosition().p, tankerName, -1, -1) -- -1 means to use the currently defined speed and altitude
        veaf.outTextForUnit(unitName, string.format("%s - Moving to your position right away !", tankerName), 10)
    end
end

--- Build the initial radio menu
function veafMove.buildRadioMenu()
    veafMove.logDebug(string.format("veafMove.buildRadioMenu()"))
    veafMove.rootPath = veafRadio.addSubMenu(veafMove.RadioMenuName)
    if not(veafRadio.skipHelpMenus) then
        veafRadio.addCommandToSubmenu("HELP", veafMove.rootPath, veafMove.help, nil, veafRadio.USAGE_ForGroup)
    end
    for _, tankerUnitName in pairs(veafMove.Tankers) do
        local tankerName = tankerUnitName
        if veafAssets then
            veafMove.logTrace(string.format("searching for asset name %s", tankerUnitName))
            local asset = veafAssets.get(tankerUnitName)
            if asset then 
                tankerName = asset.description
                veafMove.logTrace(string.format("found asset name : %s", tankerName))
            end
        end
        local menuName = string.format("Move %s to me", tankerName)
        local moveTankerPath = veafRadio.addSubMenu(menuName, veafMove.rootPath)
        veafRadio.addCommandToSubmenu(menuName , moveTankerPath, veafMove.moveTankerToMe, tankerUnitName, veafRadio.USAGE_ForGroup)    
    end
end

function veafMove.help(unitName)
    local text = 
        'Create a marker and type "_move <group|tanker|afac>, name <groupname> " in the text\n' ..
        'This will issue a move command to the specified group in the DCS world\n' ..
        'Type "_move group, name [groupname]" to move the specified group to the marker point\n' ..
        '     add ", speed [speed]" to make the group move and at the specified speed (in knots)\n' ..
        'Type "_move tanker, name [groupname]" to create a new tanker flight plan and move the specified tanker.\n' ..
        '     add ", speed [speed]" to make the tanker move and execute its refuel mission at the specified speed (in knots)\n' ..
        '     add ", alt [altitude]" to specify the refuel leg altitude (in feet)\n' ..
        'Type "_move afac, name [groupname]" to create a new JTAC flight plan and move the specified afac drone.\n' ..
        '     add ", speed [speed]" to make the tanker move and execute its mission at the specified speed (in knots)\n' ..
        '     add ", alt [altitude]" to specify the altitude at which the drone will circle (in feet)'
    veaf.outTextForUnit(unitName, text, 30)
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- initialisation
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafMove.initialize()
    if #veafMove.Tankers == 0 then
        -- find all existing Tankers
        veafMove.Tankers = veafMove.findAllTankers()
    end
    veafMove.buildRadioMenu()
    veafMarkers.registerEventHandler(veafMarkers.MarkerChange, veafMove.onEventMarkChange)
end

veafMove.logInfo(string.format("Loading version %s", veafMove.Version))


