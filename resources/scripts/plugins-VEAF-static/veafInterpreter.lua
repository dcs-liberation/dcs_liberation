-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- VEAF interpreter for DCS World
-- By Zip (2019)
--
-- Features:
-- ---------
-- * interprets a command and a position, and executes one of the VEAF script commands as if it had been requested in a map marker
-- * Possibilities : 
-- *    - at mission start, have pre-placed units trigger specific commands
-- *    - serve as a base for activating commands in Combat Zones (see veafCombatZone.lua)
-- * Works with all current and future maps (Caucasus, NTTR, Normandy, PG, ...)
--
-- Prerequisite:
-- ------------
-- * This script requires DCS 2.5.1 or higher and MIST 4.3.74 or higher.
-- * It also requires the base veaf.lua script library (version 1.0 or higher)
-- * TODO the rest of the scripts
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
--     * TODO the rest of the scripts
--     * ACTION "DO SCRIPT FILE"
--     * OPEN --> Browse to the location of this script and click OK.
--     * ACTION "DO SCRIPT"
--     * set the script command to "veafInterpreter.initialize()" and click OK.
-- 4.) Save the mission and start it.
-- 5.) Have fun :)
--
-- Basic Usage:
-- ------------
-- 1.) Place a unit on the map in the mission editor
-- 2.) As the unit name, specify #veafInterpreter["<command>"] where command can be any VEAF command (e.g. "_spawn group, name redconvoy-lightdef"). Suffixes will be ignored (useful when copy/pasting units in the mission editor)
-- 4.) The command will be processed when the mission starts.
-- 5.) The original unit will disappear.
--
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- veafInterpreter Table.
veafInterpreter = {}

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Global settings. Stores the script constants
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Identifier. All output in DCS.log will start with this.
veafInterpreter.Id = "INTERPRETER - "

--- Version.
veafInterpreter.Version = "1.0.2"

-- trace level, specific to this module
veafInterpreter.Trace = false

--- Key phrase to look for in the unit name which triggers the interpreter.
veafInterpreter.Starter = "#veafInterpreter%[\""
veafInterpreter.Trailer = "\"%]"

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Do not change anything below unless you know what you are doing!
-------------------------------------------------------------------------------------------------------------------------------------------------------------

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Utility methods
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafInterpreter.logError(message)
    veaf.logError(veafInterpreter.Id .. message)
end

function veafInterpreter.logInfo(message)
    veaf.logInfo(veafInterpreter.Id .. message)
end

function veafInterpreter.logDebug(message)
    veaf.logDebug(veafInterpreter.Id .. message)
end

function veafInterpreter.logTrace(message)
    if message and veafInterpreter.Trace then 
        veaf.logTrace(veafInterpreter.Id .. message)
    end
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Analyse the text
-------------------------------------------------------------------------------------------------------------------------------------------------------------
function veafInterpreter.interpret(text)
    veafInterpreter.logTrace(string.format("veafInterpreter.interpret([%s])",text))
    local result = nil
    local p1, p2 = text:find(veafInterpreter.Starter)
    if p2 then 
      -- starter has been found
      text = text:sub(p2 + 1)
      p1, p2 = text:find(veafInterpreter.Trailer)
      if p1 then
        -- trailer has been found
        result = text:sub(1, p1 - 1)
      end
    end
    return result
end

function veafInterpreter.execute(command, position, coalition, route, spawnedGroups, doNotBypassSecurity)
    if command == nil then return end
    if position == nil then return end
    veafInterpreter.logTrace(string.format("veafInterpreter.execute([%s],[%s])",command, veaf.vecToString(position)))

    -- for spawn choose by default the coalition opposing the unit in which the intepreter command is stored ; the SPAWN and CAS module will also invert, and voilà !
    local invertedCoalition = 1
    if coalition == 1 then
        invertedCoalition = 2
    end

    local commandExecuted = false
    spawnedGroups = spawnedGroups or {}

    -- check for shortcuts
    if veafShortcuts.executeCommand(position, command, coalition, spawnedGroups) then
        commandExecuted = true
    -- check for SPAWN module commands
    elseif veafSpawn.executeCommand(position, command, invertedCoalition, doNotBypassSecurity or true, spawnedGroups) then
        commandExecuted = true
    -- check for NAMED POINT module commands
    elseif veafNamedPoints.executeCommand(position, {text=command, coalition=-1}, doNotBypassSecurity or true) then
        commandExecuted = true
    elseif veafCasMission.executeCommand(position, command, invertedCoalition, doNotBypassSecurity or true) then
        commandExecuted = true
    elseif veafSecurity.executeCommand(position, command, doNotBypassSecurity or true) then
        commandExecuted = true
    else
        commandExecuted = false
    end

    if commandExecuted then
        veafInterpreter.logTrace(string.format("spawnedGroups = [%s]", veaf.p(spawnedGroups)))
        if route and spawnedGroups then
            for _, newGroup in pairs(spawnedGroups) do
                veafInterpreter.logTrace(string.format("newGroup = [%s]", veaf.p(newGroup)))
                mist.goRoute(newGroup, route)
            end
        end
    end

    return commandExecuted

end

function veafInterpreter.processObject(unitName)
    veafInterpreter.logTrace(string.format("veafInterpreter.processObject([%s])", unitName))
    local command = veafInterpreter.interpret(unitName)
    if command then 
        -- found an interpretable command
        veafInterpreter.logDebug(string.format("found an interpretable command : [%s]", command))
        local unit = Unit.getByName(unitName)
        if unit then
            local position = unit:getPosition().p
            veafInterpreter.logTrace(string.format("found the unit at : [%s]", veaf.vecToString(position)))
            local groupName = unit:getGroup():getName()
            veafInterpreter.logTrace(string.format("groupName = [%s]", groupName))
            local route = mist.getGroupRoute(groupName, 'task')
            veafInterpreter.logTrace(string.format("route = [%s]", veaf.p(route)))
            if veafInterpreter.execute(command, position, unit:getCoalition(), route) then 
                unit:destroy()
            end
        end
    end
end
-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- initialisation
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafInterpreter.initialize()
    -- the following code is liberally adapted from MiST (thanks Grimes !)
    local l_units = mist.DBs.units	--local reference for faster execution
    for coa, coa_tbl in pairs(l_units) do
        for country, country_table in pairs(coa_tbl) do
            for unit_type, unit_type_tbl in pairs(country_table) do
                if type(unit_type_tbl) == 'table' then
                    for group_ind, group_tbl in pairs(unit_type_tbl) do
                        if type(group_tbl) == 'table' then
                            for unit_ind, mist_unit in pairs(group_tbl.units) do
                                local unitName = mist_unit.unitName
                                veafInterpreter.logTrace(string.format("initialize - checking unit [%s]", unitName))
                                veafInterpreter.processObject(unitName)
                            end
                        end
                    end
                end
            end
        end
    end
end

veafInterpreter.logInfo(string.format("Loading version %s", veafInterpreter.Version))


