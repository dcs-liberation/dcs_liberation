-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- VEAF combat zone functions for DCS World
-- By zip (2019-20)
--
-- Features:
-- ---------
-- * Zones can be defined in the mission editor that are then managed by this script.
-- * For each zone, a specific radio sub-menu is created, allowing common actions on all specific zone (get coordinates, enemy presence, weather, pop smoke and flares, read a briefing, stop and start dynamic activity on the zone, etc.)
-- * Works with all current and future maps (Caucasus, NTTR, Normandy, PG, ...)
--
-- Prerequisite:
-- ------------
-- * This script requires DCS 2.5.1 or higher and MIST 4.3.74 or higher.
-- * It also requires the base veaf.lua script library (version 1.0 or higher)
-- TODO
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
-- TODO
--     * ACTION "DO SCRIPT FILE"
--     * OPEN --> Browse to the location of this script and click OK.
--     * ACTION "DO SCRIPT"
--     * set the script command to "veafCombatZone.initialize()" and click OK.
-- 4.) Save the mission and start it.
-- 5.) Have fun :)
--
-- Basic Usage:
-- ------------
-- TODO
--
-------------------------------------------------------------------------------------------------------------------------------------------------------------

veafCombatZone = {}

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Global settings. Stores the script constants
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Identifier. All output in DCS.log will start with this.
veafCombatZone.Id = "COMBAT ZONE - "

--- Version.
veafCombatZone.Version = "1.3.0"

-- trace level, specific to this module
veafCombatZone.Debug = false
veafCombatZone.Trace = false

--- Number of seconds between each check of the zone watchdog function
veafCombatZone.SecondsBetweenWatchdogChecks = 60

--- Number of seconds between each smoke request on the zones
veafCombatZone.SecondsBetweenSmokeRequests = 180

--- Number of seconds between each flare request on the zones
veafCombatZone.SecondsBetweenFlareRequests = 120

veafCombatZone.DefaultSpawnRadiusForUnits = 50

veafCombatZone.DefaultSpawnRadiusForStatics = 0

veafCombatZone.RadioMenuName = "COMBAT ZONES"

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Do not change anything below unless you know what you are doing!
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Radio menus paths
veafCombatZone.rootPath = nil

-- Zones list (table of VeafCombatZone objects)
veafCombatZone.zonesList = {}

-- Zones dictionary (map of VeafCombatZone objects by zone name)
veafCombatZone.zonesDict = {}

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Utility methods
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafCombatZone.logError(message)
    veaf.logError(veafCombatZone.Id .. message)
end

function veafCombatZone.logInfo(message)
    veaf.logInfo(veafCombatZone.Id .. message)
end

function veafCombatZone.logDebug(message)
    if message and veafCombatZone.Debug then 
        veaf.logDebug(veafCombatZone.Id .. message)
    end
end

function veafCombatZone.logTrace(message)
    if message and veafCombatZone.Trace then 
        veaf.logTrace(veafCombatZone.Id .. message)
    end
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- VeafCombatZoneElement object
-------------------------------------------------------------------------------------------------------------------------------------------------------------
VeafCombatZoneElement =
{
    -- name
    name,
    -- position on the map
    position,
    -- if true, this is a simple dcs static
    dcsStatic,
    -- if true, this is a simple dcs group
    dcsGroup,
    -- if true, this is a VEAF command
    veafCommand,
    --  coalition (0 = neutral, 1 = red, 2 = blue)
    coalition,
    -- route, only for veaf commands (groups already have theirs)
    route,
    -- spawn radius in meters (randomness introduced in the respawn mechanism)
    spawnRadius,
    -- spawn chance in percent (xx chances in 100 that the unit is spawned - or the command run)
    spawnChance,
    -- grouping elements (spawnGroup) so that a certain number (spawnCount) is guaranteed to spawn, by running the spawn random chance computation as often as necessary
    spawnGroup,
    -- grouping elements (spawnGroup) so that a certain number (spawnCount) is guaranteed to spawn, by running the spawn random chance computation as often as necessary
    spawnCount
}
VeafCombatZoneElement.__index = VeafCombatZoneElement

function VeafCombatZoneElement:new ()
    local self = setmetatable({}, VeafCombatZoneElement)
    self.name = nil
    self.position = nil
    self.dcsStatic = false
    self.dcsGroup = false
    self.veafCommand = nil
    self.route = nil
    self.coalition = nil
    self.spawnRadius = 0
    self.spawnChance = 100
    self.spawnGroup = nil
    self.spawnCount = 1
    return self
end

---
--- setters and getters
---

function VeafCombatZoneElement:setName(value)
    self.name = value
    return self
end

function VeafCombatZoneElement:getName()
    return self.name
end

function VeafCombatZoneElement:setPosition(value)
    veafCombatZone.logTrace(string.format("VeafCombatZoneElement:setPosition(value=[%s])",veaf.p(value)))
    self.position = value
    return self
end

function VeafCombatZoneElement:getPosition()
    veafCombatZone.logTrace(string.format("VeafCombatZoneElement:getPosition()=[%s]",veaf.p(self.position or "")))
    return self.position
end

function VeafCombatZoneElement:setDcsStatic(value)
    self.dcsStatic = value
    return self
end

function VeafCombatZoneElement:isDcsStatic()
    return self.dcsStatic
end

function VeafCombatZoneElement:setDcsGroup(value)
    self.dcsGroup = value
    return self
end

function VeafCombatZoneElement:isDcsGroup()
    return self.dcsGroup
end

function VeafCombatZoneElement:setVeafCommand(value)
    self.veafCommand = value
    return self
end

function VeafCombatZoneElement:getVeafCommand()
    return self.veafCommand
end

function VeafCombatZoneElement:setRoute(value)
    self.route = value
    return self
end

function VeafCombatZoneElement:getRoute()
    return self.route
end

function VeafCombatZoneElement:setCoalition(value)
    self.coalition = value
    return self
end

function VeafCombatZoneElement:getCoalition()
    return self.coalition
end

function VeafCombatZoneElement:setSpawnRadius(value)
    self.spawnRadius = tonumber(value)
    return self
end

function VeafCombatZoneElement:getSpawnRadius()
    return self.spawnRadius
end

function VeafCombatZoneElement:setSpawnChance(value)
    self.spawnChance = tonumber(value)
    return self
end

function VeafCombatZoneElement:getSpawnChance()
    return self.spawnChance
end

function VeafCombatZoneElement:setSpawnGroup(value)
    self.spawnGroup = value
    return self
end

function VeafCombatZoneElement:getSpawnGroup()
    return self.spawnGroup
end

function VeafCombatZoneElement:setSpawnCount(value)
    self.spawnCount = tonumber(value)
    return self
end

function VeafCombatZoneElement:getSpawnCount()
    return self.spawnCount
end

---
--- other methods
---

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- VeafCombatZone object
-------------------------------------------------------------------------------------------------------------------------------------------------------------

VeafCombatZone = 
{
    -- zone name (human-friendly)
    friendlyName,
    -- technical zone name (in the mission editor)
    missionEditorZoneName,
    -- mission briefing
    briefing,
    -- list of defined objectives
    objectives,
    -- list of the elements defined in the zone
    elements,
    -- the zone center
    zoneCenter,
    -- zone is active
    active,
    -- zone is a training zone
    training,
    -- DCS groups that have been spawned (for cleaning up later)
    spawnedGroups,
    --- Radio menus paths
    radioMarkersPath,
    radioTargetInfoPath,
    radioRootPath,
    -- the watchdog function checks for zone objectives completion
    watchdogFunctionId,
    -- "pop smoke" command reset function id
    smokeResetFunctionId,
    -- "pop flare" command reset function id
    flareResetFunctionId
}
VeafCombatZone.__index = VeafCombatZone

function VeafCombatZone:new()
    local self = setmetatable({}, VeafCombatZone)
    self.friendlyName = nil
    self.missionEditorZoneName = nil
    self.briefing = nil
    self.objectives = {}
    self.elements = {}
    self.elementGroups = {}
    self.zoneCenter = nil
    self.active = false
    self.training = false
    self.spawnedGroups = {}
    self.radioMarkersPath = nil
    self.radioTargetInfoPath = nil
    self.radioRootPath = nil
    self.watchdogFunctionId = nil
    self.smokeResetFunctionId = nil
    self.flareResetFunctionId = nil
    return self
end

---
--- setters and getters
---
function VeafCombatZone:getRadioMenuName()
    return self:getFriendlyName()
end

function VeafCombatZone:setFriendlyName(value)
    self.friendlyName = value
    return self
end

function VeafCombatZone:getFriendlyName()
    return self.friendlyName
end

function VeafCombatZone:setBriefing(value)
    self.briefing = value
    return self
end

function VeafCombatZone:getBriefing()
    return self.briefing
end

function VeafCombatZone:setMissionEditorZoneName(value)
    self.missionEditorZoneName = value
    return self
end

function VeafCombatZone:getMissionEditorZoneName()
    return self.missionEditorZoneName
end

function VeafCombatZone:isActive()
    return self.active
end

function VeafCombatZone:setActive(value)
    self.active = value
    return self
end

function VeafCombatZone:isTraining()
    return self.training
end

function VeafCombatZone:setTraining(value)
    self.training = value
    return self
end

function VeafCombatZone:getCenter()
    return self.zoneCenter
end

function VeafCombatZone:addSpawnedGroup(groupOrName)
    local groupName = groupOrName   
    if type(groupName) ~= "string" then 
        groupName = tostring(groupName)    
    end
    veafCombatZone.logDebug(string.format("VeafCombatZone[%s]:addSpawnedGroup(%s)",self.missionEditorZoneName or "", groupName or ""))
    if not self.spawnedGroups then 
        self.spawnedGroups = {}
    end
    table.insert(self.spawnedGroups, groupName)
    return self
end

function VeafCombatZone:getSpawnedGroups()
    veafCombatZone.logDebug(string.format("VeafCombatZone[%s]:getSpawnedGroup()",self.missionEditorZoneName or ""))
    veafCombatZone.logDebug(veaf.serialize("self.spawnedGroups", self.spawnedGroups))
    return self.spawnedGroups
end

function VeafCombatZone:clearSpawnedGroups()
    self.spawnedGroups = {}
    return self
end


function VeafCombatZone:addZoneElement(element)
    veafCombatZone.logDebug(string.format("VeafCombatZone[%s]:addZoneElement(%s)",self.missionEditorZoneName or "", element:getName()))
    if not self.elements then 
        self.elements = {}
    end
    if not self.elementGroups then 
        self.elementGroups = {}
    end
    table.insert(self.elements, element)
    if not self.elementGroups[element:getSpawnGroup()] then
        local elementGroup = {}
        elementGroup.spawnGroup = element:getSpawnGroup()
        elementGroup.spawnCount = element:getSpawnCount()
        elementGroup.elements = {}
        self.elementGroups[element:getSpawnGroup()] = elementGroup
    end
    local elementGroup = self.elementGroups[element:getSpawnGroup()]
    table.insert(elementGroup.elements, element)
    return self
end

function VeafCombatZone:getZoneElements()
    veafCombatZone.logDebug(string.format("VeafCombatZone[%s]:getZoneElement()",self.missionEditorZoneName or ""))
    veafCombatZone.logTrace(veaf.serialize("self.elements", self.elements))
    return self.elements
end

function VeafCombatZone:getZoneElementsGroups()
    veafCombatZone.logDebug(string.format("VeafCombatZone[%s]:getZoneElementsGroups()",self.missionEditorZoneName or ""))
    return self.elementGroups
end

---
--- other methods
---
function VeafCombatZone:scheduleWatchdogFunction()
    veafCombatZone.logDebug(string.format("VeafCombatZone[%s]:scheduleWatchdogFunction()",self.missionEditorZoneName or ""))
    self.watchdogFunctionId = mist.scheduleFunction(veafCombatZone.CompletionCheck,{self.missionEditorZoneName},timer.getTime()+veafCombatZone.SecondsBetweenWatchdogChecks)
    return self
end

function VeafCombatZone:unscheduleWatchdogFunction()
    veafCombatZone.logDebug(string.format("VeafCombatZone[%s]:unscheduleWatchdogFunction()",self.missionEditorZoneName or ""))
    if self.watchdogFunctionId then
        mist.removeFunction(self.watchdogFunctionId)
    end
    self.watchdogFunctionId = nil
    return self
end

function VeafCombatZone:addObjective(value)
    table.insert(self.objectives, value)
    return self
end

function VeafCombatZone:addDefaultObjectives()
    -- TODO
    return self
end

function VeafCombatZone:initialize()
    veafCombatZone.logDebug(string.format("VeafCombatZone[%s]:initialize()",self.missionEditorZoneName or ""))

    -- check parameters
    if not self.missionEditorZoneName then 
        return self 
    end
    if not self.friendlyName then 
        self:setFriendlyName(self.missionEditorZoneName)
    end
    if #self.objectives == 0 then
        self:addDefaultObjectives()
    end

    -- find the trigger zone center
    self.zoneCenter = mist.utils.zoneToVec3(self.missionEditorZoneName)
    if not self.zoneCenter then 
        local message = string.format("Trigger zone [%s] does not exist in the mission !",self.missionEditorZoneName)
        veafCombatZone.logError(message)
        trigger.action.outText(message,5)
        return self
    end
    veafCombatZone.logTrace(string.format("zone center = [%s]",veaf.vecToString(self.zoneCenter)))  

    -- find units in the trigger zone
    local units
    units, _ = veaf.safeUnpack(veafCombatZone.findUnitsInTriggerZone(self.missionEditorZoneName))

    -- process special commands in the units 
    local alreadyAddedGroups = {}
    for _,unit in pairs(units) do
        local zoneElement = VeafCombatZoneElement:new()
        zoneElement:setCoalition(unit:getCoalition())
        local unitName = unit:getName()
        veafCombatZone.logTrace(string.format("processing unit [%s] of coalition [%d]", unitName, unit:getCoalition()))
        zoneElement:setPosition(unit:getPosition().p)
        local spawnRadius, command, chance 
        local _, _, spawnRadius = unitName:lower():find("#spawnradius%s*=%s*(%d+)")
        local _, _, command = unitName:lower():find("#command%s*=%s*\"([^\"]+)\"")
        local _, _, spawnChance = unitName:lower():find("#spawnchance%s*=%s*(%d+)")
        local _, _, spawnGroup = unitName:lower():find("#spawngroup%s*=%s*\"([^\"]+)\"")
        local _, _, spawnCount = unitName:lower():find("#spawncount%s*=%s*(%d+)")
        if spawnRadius then 
            veafCombatZone.logTrace(string.format("spawnRadius = [%d]", spawnRadius))
            zoneElement:setSpawnRadius(spawnRadius)
        end
        if spawnChance then 
            veafCombatZone.logTrace(string.format("spawnChance = [%d]", spawnChance))
            zoneElement:setSpawnChance(spawnChance)
        end
        if spawnCount then 
            veafCombatZone.logTrace(string.format("spawnCount = [%d]", spawnCount))
            zoneElement:setSpawnCount(spawnCount)
        end
        if spawnGroup then 
            veafCombatZone.logTrace(string.format("spawnGroup = [%s]", spawnGroup))
            zoneElement:setSpawnGroup(spawnGroup)
        end
        if command then 
            -- it's a fake unit transporting a VEAF command
            veafCombatZone.logTrace(string.format("command = [%s]", command))
            zoneElement:setVeafCommand(command)
            local groupName = unit:getGroup():getName()
            zoneElement:setName(groupName)
            veafCombatZone.logTrace(string.format("groupName = [%s]", groupName))
            local route = mist.getGroupRoute(groupName, 'task')
            zoneElement:setRoute(route)
            if not zoneElement:getSpawnGroup() then zoneElement:setSpawnGroup(groupName) end -- default the spawn group to the group name in case there is no spawn group  defined
        else
            -- it's a group or a static unit
            local groupName = nil
            if unit:getCategory() == 3 then
                groupName = unitName -- default for static objects = groups themselves
                zoneElement:setDcsStatic(true)
                if not zoneElement:getSpawnRadius() then 
                    zoneElement:setSpawnRadius(veafCombatZone.DefaultSpawnRadiusForStatics)
                end
            else
                groupName = unit:getGroup():getName()
                zoneElement:setDcsGroup(true)
                if not zoneElement:getSpawnRadius() then 
                    zoneElement:setSpawnRadius(veafCombatZone.DefaultSpawnRadiusForUnits)
                end
            end
            if not zoneElement:getSpawnGroup() then zoneElement:setSpawnGroup(groupName) end -- default the spawn group to the group name in case there is no spawn group  defined
            if not alreadyAddedGroups[groupName] then 
                -- add a group element
                veafCombatZone.logTrace(string.format("adding group [%s]", groupName))
                alreadyAddedGroups[groupName] = groupName
                zoneElement:setName(groupName)
            else
                veafCombatZone.logTrace(string.format("skipping group [%s]", groupName))
                zoneElement = nil -- don't add this element, it's a group that has already been added
            end
        end

        if zoneElement then self:addZoneElement(zoneElement) end
    end

    -- deactivate the zone
    veafCombatZone.logTrace("desactivate the zone")
    self:desactivate()

    -- remove all units in the trigger zone (we want it CLEAN !)
    local units, groupNames = veaf.safeUnpack(veafCombatZone.findUnitsInTriggerZone(self.missionEditorZoneName))
    for _, groupName in pairs(groupNames) do

        veafCombatZone.logTrace(string.format("destroying group [%s]",groupName))
        local group = Group.getByName(groupName)
        if not group then 
            group = StaticObject.getByName(groupName)
        end
        if group then
            group:destroy()
        end
    end 

    return self
end

function VeafCombatZone:getInformation()
    veafCombatZone.logDebug(string.format("VeafCombatZone[%s]:getInformation()",self.missionEditorZoneName or ""))
    local message =      "COMBAT ZONE "..self:getFriendlyName().." \n\n"
    if (self:getBriefing()) then
        message = message .. "BRIEFING: \n"
        message = message .. self:getBriefing()
        message = message .. "\n\n"
    end
    if self:isActive() then

        -- generate information dispatch
        local nbShipsR = 0
        local nbVehiclesR = 0
        local nbInfantryR = 0
        local nbStaticsR = 0
        local nbShipsB = 0
        local nbVehiclesB = 0
        local nbInfantryB = 0
        local nbStaticsB = 0
        local unitsByTypeR = {}
        local unitsByTypeB = {}

        for _, groupName in pairs(self:getSpawnedGroups()) do
            local group = Group.getByName(groupName)
            if group then
                for _, u in pairs(group:getUnits()) do
                    local coa = u:getCoalition()
                    if u:getCategory() == 3 then
                        if coa == 1 then 
                            nbStaticsR = nbStaticsR + 1
                        elseif coa == 2 then
                            nbStaticsB = nbStaticsB + 1
                        end
                    else
                        local typeName = u:getTypeName()
                        if typeName then 
                            local unit = veafUnits.findUnit(typeName)
                            if unit then 
                                if coa == 1 then
                                    if not(unitsByTypeR[typeName]) then 
                                        unitsByTypeR[typeName] = 0
                                    end
                                    unitsByTypeR[typeName] = unitsByTypeR[typeName] + 1
                                    if unit.vehicle then
                                        nbVehiclesR = nbVehiclesR + 1
                                    elseif unit.naval then 
                                        nbShipsR = nbShipsR + 1
                                    else
                                        nbInfantryR = nbInfantryR + 1
                                    end
                                elseif coa == 2 then
                                    if not(unitsByTypeB[typeName]) then 
                                        unitsByTypeB[typeName] = 0
                                    end
                                    unitsByTypeB[typeName] = unitsByTypeB[typeName] + 1
                                    if unit.vehicle then
                                        nbVehiclesB = nbVehiclesB + 1
                                    elseif unit.naval then 
                                        nbShipsB = nbShipsB + 1
                                    else
                                        nbInfantryB = nbInfantryB + 1
                                    end
                                end
                            end
                        end
                    end
                end
            end
        end

        if nbShipsB+nbStaticsB+nbVehiclesB+nbInfantryB > 0 then
            local msgs = {}
            if nbShipsB > 0 then
                table.insert(msgs, nbShipsB .. " ship(s)")
            end
            if nbStaticsB > 0 then
                table.insert(msgs, nbStaticsB .. " structure(s)")
            end
            if nbVehiclesB > 0 then
                table.insert(msgs, nbVehiclesB .. " vehicle(s)")
            end
            if nbInfantryB > 0 then
                table.insert(msgs, nbInfantryB .. " soldier(s)")
            end
            message = message .. "FRIENDS: ".. table.concat(msgs, ",") .." remaining.\n"
            if self:isTraining() then 
                local firstUnit = true
                for name, count in pairs(unitsByTypeB) do
                    local separator = ", "
                    if firstUnit then 
                        separator = ""
                        firstUnit = false
                    end
                    message = message .. string.format("%s%d %s",separator, count, name)
                end
                message = message .. "\n"
            end
        end       
        if nbShipsR+nbStaticsR+nbVehiclesR+nbInfantryR > 0 then
            local msgs = {}
            if nbShipsR > 0 then
                table.insert(msgs, nbShipsR .. " ship(s)")
            end
            if nbStaticsR > 0 then
                table.insert(msgs, nbStaticsR .. " structure(s)")
            end
            if nbVehiclesR > 0 then
                table.insert(msgs, nbVehiclesR .. " vehicle(s)")
            end
            if nbInfantryR > 0 then
                table.insert(msgs, nbInfantryR .. " soldier(s)")
            end
            message = message .. "ENEMIES: ".. table.concat(msgs, ",") .." remaining.\n"
            if self:isTraining() then 
                local firstUnit = true
                for name, count in pairs(unitsByTypeR) do
                    local separator = ", "
                    if firstUnit then 
                        separator = ""
                        firstUnit = false
                    end
                    message = message .. string.format("%s%d %s",separator, count, name)
                end
                message = message .. "\n"
            end
        end
        message = message .. "\n"

        -- add coordinates and position from bullseye
        local zoneCenter = self:getCenter()
        local lat, lon = coord.LOtoLL(zoneCenter)
        local mgrsString = mist.tostringMGRS(coord.LLtoMGRS(lat, lon), 3)
        local bullseye = mist.utils.makeVec3(mist.DBs.missionData.bullseye.blue, 0)
        local vec = {x = zoneCenter.x - bullseye.x, y = zoneCenter.y - bullseye.y, z = zoneCenter.z - bullseye.z}
        local dir = mist.utils.round(mist.utils.toDegree(mist.utils.getDir(vec, bullseye)), 0)
        local dist = mist.utils.get2DDist(zoneCenter, bullseye)
        local distMetric = mist.utils.round(dist/1000, 0)
        local distImperial = mist.utils.round(mist.utils.metersToNM(dist), 0)
        local fromBullseye = string.format('%03d', dir) .. ' for ' .. distMetric .. 'km /' .. distImperial .. 'nm'

        message = message .. "LAT LON (decimal): " .. mist.tostringLL(lat, lon, 2) .. ".\n"
        message = message .. "LAT LON (DMS)    : " .. mist.tostringLL(lat, lon, 0, true) .. ".\n"
        message = message .. "MGRS/UTM         : " .. mgrsString .. ".\n"
        message = message .. "FROM BULLSEYE    : " .. fromBullseye .. ".\n"
        message = message .. "\n"

        -- get altitude, qfe and wind information
        message = message .. veaf.weatherReport(zoneCenter, nil, true)
    else
        message = message .. "zone is not yet active."
    end

    return message
end

-- activate the zone
function VeafCombatZone:activate()
    veafCombatZone.logTrace(string.format("VeafCombatZone[%s]:activate()",self:getMissionEditorZoneName()))
    self:setActive(true)
    
    for _, zoneElementGroup in pairs(self:getZoneElementsGroups()) do
        veafCombatZone.logTrace(string.format("processing spawnGroup [%s]",zoneElementGroup.spawnGroup))
        local spawnCount = zoneElementGroup.spawnCount
        veafCombatZone.logTrace(string.format("spawnCount = [%d]",spawnCount))
        local tries = 10
        alreadySpawnedElements = {}
        local shuffledIndexes = {}
        for i=1,#zoneElementGroup.elements do
            local zoneElement = zoneElementGroup.elements[i]
            alreadySpawnedElements[zoneElement:getName()]=false 
            table.insert(shuffledIndexes, i)
        end
        veaf.shuffle(shuffledIndexes)
        while spawnCount > 0 and tries > 0 do
            veafCombatZone.logTrace(string.format("tries = [%d]",tries))
            tries = tries - 1
            
            for i=1,#shuffledIndexes do
                local zoneElement = zoneElementGroup.elements[shuffledIndexes[i]]
                if spawnCount > 0 then
                    if not alreadySpawnedElements[zoneElement:getName()] then
                        veafCombatZone.logTrace(string.format("processing element [%s]",zoneElement:getName()))
                        local chance = math.random(0, 100)
                        if tries == 1 then chance = 0 end -- force chance if in the last try
                        veafCombatZone.logTrace(string.format("chance = [%d]",chance))
                        veafCombatZone.logTrace(string.format("spawnChance = [%d]",zoneElement:getSpawnChance()))
                        if chance <= zoneElement:getSpawnChance() then
                            veafCombatZone.logTrace(string.format("chance hit (%d <= %d)",chance, zoneElement:getSpawnChance()))
                            spawnCount = spawnCount - 1
                            alreadySpawnedElements[zoneElement:getName()]=true
                            local position = zoneElement:getPosition()
                            if zoneElement:getSpawnRadius() > 0 then
                                veafCombatZone.logTrace(string.format("position=[%s]",veaf.vecToString(position)))
                                veafCombatZone.logTrace(string.format("spawnRadius=[%s]",zoneElement:getSpawnRadius()))
                                local mistP = mist.getRandPointInCircle(position, zoneElement:getSpawnRadius())
                                veafCombatZone.logTrace(string.format("mistP=[%s]",veaf.vecToString(mistP)))
                                position = {x = mistP.x, y = position.y, z = mistP.y}
                            end
                            if zoneElement:isDcsStatic() or zoneElement:isDcsGroup() then
                                veafCombatZone.logTrace(string.format("respawning group [%s] at position [%s]",zoneElement:getName(), veaf.vecToString(position)))
                                local vars = {}
                                vars.gpName = zoneElement:getName()
                                vars.name = zoneElement:getName()
                                vars.route = mist.getGroupRoute(vars.gpName, 'task')
                                vars.action = 'respawn'
                                vars.point = position
                                local newGroup = mist.teleportToPoint(vars)
                                if type(newGroup) == 'table' then
                                    veafCombatZone.logTrace(string.format("[%s]:activate() - mist.teleportToPoint([%s])", self:getMissionEditorZoneName(), zoneElement:getName()))
                                    self:addSpawnedGroup(newGroup.name)
                                else
                                    veafCombatZone.logTrace(string.format("[%s]:activate() - mist.teleportToPoint([%s]) failed", self:getMissionEditorZoneName(), zoneElement:getName()))
                                end
                            elseif zoneElement:getVeafCommand() then
                                veafCombatZone.logTrace(string.format("executing command [%s] at position [%s]",zoneElement:getName(), veaf.vecToString(position)))
                                local spawnedGroups = {}
                                veafInterpreter.execute(zoneElement:getVeafCommand(), position, zoneElement:getCoalition(), nil, spawnedGroups)
                                for _, newGroup in pairs(spawnedGroups) do
                                    veafCombatZone.logTrace(string.format("[%s].addSpawnedGroup", zoneElement:getName()))
                                    self:addSpawnedGroup(newGroup)
                                    veafCombatZone.logTrace(string.format("newGroup = [%s]", newGroup))
                                    local route = zoneElement:getRoute()
                                    local result = mist.goRoute(newGroup, route)
                                end
                            end
                        else 
                            veafCombatZone.logTrace(string.format("chance missed (%d > %d)",chance, zoneElement:getSpawnChance()))
                        end
                    else
                        veafCombatZone.logTrace(string.format("already spawned [%s]",zoneElement:getName()))
                    end
                end
            end
        end
    end

    -- start the completion watchdog
    self:scheduleWatchdogFunction()

    -- refresh the radio menu
    self:updateRadioMenu()

    return self
end

-- desactivate the zone
function VeafCombatZone:desactivate()
    veafCombatZone.logDebug(string.format("VeafCombatZone[%s]:desactivate()",self.missionEditorZoneName or ""))
    self:setActive(false)
    self:unscheduleWatchdogFunction()

    for _, groupName in pairs(self:getSpawnedGroups()) do
        veafCombatZone.logTrace(string.format("trying to destroy group [%s]",groupName))
        local group = Group.getByName(groupName)
        if not group then 
            group = StaticObject.getByName(groupName)
            if group then
                veafCombatZone.logTrace(string.format("found static [%s]",group:getName()))
            else
                veafCombatZone.logInfo(string.format("cannot find static [%s]",groupName))
            end
        end
        if group then
            veafCombatZone.logTrace(string.format("destroying group [%s]",group:getName()))
            group:destroy()
        end
    end
    self:clearSpawnedGroups()

    -- refresh the radio menu
    self:updateRadioMenu()

    return self
end

-- check if there are still units in zone
function VeafCombatZone:completionCheck()
    veafCombatZone.logDebug(string.format("VeafCombatZone[%s]:completionCheck()",self.missionEditorZoneName or ""))
    local nbUnitsR = 0
    local nbUnitsB = 0

    for _, groupName in pairs(self:getSpawnedGroups()) do
        local group = Group.getByName(groupName)
        if group then
            for _, unit in pairs(group:getUnits()) do
                local coa = unit:getCoalition()
                if coa == 1 then
                    nbUnitsR = nbUnitsR + 1
                elseif coa == 2 then
                    nbUnitsB = nbUnitsB + 1
                end
            end
        else
            local static = StaticObject.getByName(groupName)
            if static then
                local coa = static:getCoalition()
                if coa == 1 then
                    nbUnitsR = nbUnitsR + 1
                elseif coa == 2 then
                    nbUnitsB = nbUnitsB + 1
                end
            end
        end
    end

    veafCombatZone.logTrace(string.format("nbUnitsB=%d",nbUnitsB))
    veafCombatZone.logTrace(string.format("nbUnitsR=%d",nbUnitsR))

    if nbUnitsR == 0 then 
        -- everyone is dead, let's end this mess
        local message = string.format([[
Well done ! All enemies in zone %s have been destroyed or routed.
The zone will now be desactivated.
You can replay by activating it again, in the radio menu.]], self:getFriendlyName())
        trigger.action.outText(message, 15)
        self:desactivate()
    else
        -- reschedule
        self:scheduleWatchdogFunction()
    end
end


-- pop a smoke marker over the zone
function VeafCombatZone:popSmoke()
    veafCombatZone.logDebug(string.format("VeafCombatZone[%s]:popSmoke()",self.missionEditorZoneName or ""))
    veafCombatZone.logTrace(string.format("self:getCenter()=%s",veaf.vecToString(self:getCenter())))
    local smokePoint = self:getCenter()
    if self:isTraining() then 
        -- compute the barycenter of all remaining units
        local totalPosition = {x = 0,y = 0,z = 0}
        local units, _ = veaf.safeUnpack(veafCombatZone.findUnitsInTriggerZone(self.missionEditorZoneName))
        for count = 1,#units do
            if units[count] then 
                totalPosition = mist.vec.add(totalPosition,Unit.getPosition(units[count]).p)
            end
        end
        if #units > 0 then
            smokePoint = mist.vec.scalar_mult(totalPosition,1/#units)
        end
    end
    veafCombatZone.logTrace(string.format("smokePoint=%s",veaf.vecToString(smokePoint)))
    veafSpawn.spawnSmoke(smokePoint, trigger.smokeColor.Red)
    self.smokeResetFunctionId = mist.scheduleFunction(veafCombatZone.SmokeReset,{self.missionEditorZoneName},timer.getTime()+veafCombatZone.SecondsBetweenSmokeRequests)
    trigger.action.outText(string.format("Copy RED smoke requested on %s !", self:getFriendlyName()),5)
    self:updateRadioMenu()

    return self
end

-- pop an illumination  flare over a zone
function VeafCombatZone:popFlare()
    veafCombatZone.logDebug(string.format("VeafCombatZone[%s]:popFlare()",self.missionEditorZoneName or ""))
    veafCombatZone.logTrace(string.format("self:getCenter()=%s",veaf.vecToString(self:getCenter())))

    veafSpawn.spawnIlluminationFlare(self:getCenter())
    self.flareResetFunctionId = mist.scheduleFunction(veafCombatZone.FlareReset,{self.missionEditorZoneName},timer.getTime()+veafCombatZone.SecondsBetweenFlareRequests)
    trigger.action.outText(string.format("Copy illumination flare requested on %s !", self:getFriendlyName()),5)
    self:updateRadioMenu()

    return self
end

-- updates the radio menu according to the zone state
function VeafCombatZone:updateRadioMenu(inBatch)
    veafCombatZone.logDebug(string.format("VeafCombatZone[%s]:updateRadioMenu(%s)",self.missionEditorZoneName or "", tostring(inBatch)))
    
    -- do not update the radio menu if not yet initialized
    if not veafCombatZone.rootPath then
        return self
    end

    -- reset the radio menu
    if self.radioRootPath then
        veafCombatZone.logTrace("reset the radio submenu")
        veafRadio.clearSubmenu(self.radioRootPath)
    else
        veafCombatZone.logTrace("add the radio submenu")
        self.radioRootPath = veafRadio.addSubMenu(self:getRadioMenuName(), veafCombatZone.rootPath)
    end

    -- populate the radio menu
    veafCombatZone.logTrace("populate the radio menu")
    -- global commands
    veafRadio.addCommandToSubmenu("Get info", self.radioRootPath, veafCombatZone.GetInformationOnZone, self.missionEditorZoneName, veafRadio.USAGE_ForAll)
    if self:isActive() then
        -- zone is active, set up accordingly (desactivate zone, get information, pop smoke, etc.)
        veafCombatZone.logTrace("zone is active")
        veafRadio.addCommandToSubmenu('Desactivate zone', self.radioRootPath, veafCombatZone.DesactivateZone, self.missionEditorZoneName, veafRadio.USAGE_ForAll)
        if self.smokeResetFunctionId then 
            veafRadio.addCommandToSubmenu('Smoke not available', self.radioRootPath, veaf.emptyFunction, nil, veafRadio.USAGE_ForAll)
        else
            veafRadio.addCommandToSubmenu('Request RED smoke on target', self.radioRootPath, veafCombatZone.SmokeZone, self.missionEditorZoneName, veafRadio.USAGE_ForAll)
        end
        if self.flareResetFunctionId then 
            veafRadio.addCommandToSubmenu('Flare not available', self.radioRootPath, veaf.emptyFunction, nil, veafRadio.USAGE_ForAll)
        else
            veafRadio.addCommandToSubmenu('Request illumination flare on target', self.radioRootPath, veafCombatZone.LightUpZone, self.missionEditorZoneName, veafRadio.USAGE_ForAll)
        end
    else
        -- zone is not active, set up accordingly (activate zone)
        veafCombatZone.logTrace("zone is not active")
        veafRadio.addCommandToSubmenu('Activate zone', self.radioRootPath, veafCombatZone.ActivateZone, self.missionEditorZoneName, veafRadio.USAGE_ForAll)
    end

    if not inBatch then veafRadio.refreshRadioMenu() end
    return self
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- global functions
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafCombatZone.GetZone(zoneName)
    veafCombatZone.logDebug(string.format("veafCombatZone.GetZone([%s])",zoneName or ""))
    veafCombatZone.logDebug(string.format("Searching for zone with name [%s]", zoneName))
    local zone = veafCombatZone.zonesDict[zoneName]
    if not zone then 
        local message = string.format("VeafCombatZone [%s] was not found !",zoneName)
        veafCombatZone.logError(message)
        trigger.action.outText(message,5)
    end
    return zone
end

-- add a zone
function veafCombatZone.AddZone(zone)
    veafCombatZone.logDebug(string.format("veafCombatZone.AddZone([%s])",zone.missionEditorZoneName or ""))
    veafCombatZone.logInfo(string.format("Adding zone [%s]", zone.missionEditorZoneName))
    zone:initialize()
    table.insert(veafCombatZone.zonesList, zone)
    veafCombatZone.zonesDict[zone.missionEditorZoneName] = zone
    return zone
end

-- activate a zone by number
function veafCombatZone.ActivateZoneNumber(number, silent)
    local zone = veafCombatZone.zonesList[number]
    if zone then 
        veafCombatZone.ActivateZone(zone:getMissionEditorZoneName(), silent)
    end
end

-- activate a zone
function veafCombatZone.ActivateZone(zoneName, silent)
    veafCombatZone.logDebug(string.format("veafCombatZone.ActivateZone([%s])",zoneName or ""))
    local zone = veafCombatZone.GetZone(zoneName)
    zone:activate()
    if not silent then
        trigger.action.outText("VeafCombatZone "..zone:getFriendlyName().." has been activated.", 10)
        mist.scheduleFunction(veafCombatZone.GetInformationOnZone,{{zoneName}},timer.getTime()+1)
    end
end

-- desactivate a zone by number
function veafCombatZone.DesactivateZoneNumber(number, silent)
    local zone = veafCombatZone.zonesList[number]
    if zone then 
        veafCombatZone.DesactivateZone(zone:getMissionEditorZoneName(), silent)
    end
end

-- desactivate a zone by name
function veafCombatZone.DesactivateZone(zoneName, silent)
    veafCombatZone.logDebug(string.format("veafCombatZone.DesactivateZone([%s])",zoneName or ""))
    local zone = veafCombatZone.GetZone(zoneName)
    zone:desactivate()
    if not silent then
        trigger.action.outText("VeafCombatZone "..zone:getFriendlyName().." has been desactivated.", 10)
    end
end

-- print information about a zone
function veafCombatZone.GetInformationOnZone(parameters)
    local zoneName, unitName = veaf.safeUnpack(parameters)
    veafCombatZone.logDebug(string.format("veafCombatZone.GetInformationOnZone([%s])",zoneName or ""))
    local zone = veafCombatZone.GetZone(zoneName)
    local text = zone:getInformation()
    if unitName then
        veaf.outTextForUnit(unitName, text, 30)
    else
        trigger.action.outText(text, 30)
    end
end

-- pop a smoke over a zone
function veafCombatZone.SmokeZone(zoneName)
    veafCombatZone.logDebug(string.format("veafCombatZone.SmokeZone([%s])",zoneName or ""))
    local zone = veafCombatZone.GetZone(zoneName)
    zone:popSmoke()
end

-- pop an illumination  flare over a zone
function veafCombatZone.LightUpZone(zoneName)
    veafCombatZone.logDebug(string.format("veafCombatZone.LightUpZone([%s])",zoneName or ""))
    local zone = veafCombatZone.GetZone(zoneName)
    zone:popFlare()
end

-- reset the "pop smoke" menus
function veafCombatZone.SmokeReset(zoneName)
    veafCombatZone.logDebug(string.format("veafCombatZone.SmokeReset([%s])",zoneName or ""))
    local zone = veafCombatZone.GetZone(zoneName)
    zone.smokeResetFunctionId = nil
    zone:updateRadioMenu()
end

-- reset the "pop flare" menus
function veafCombatZone.FlareReset(zoneName)
    veafCombatZone.logDebug(string.format("veafCombatZone.FlareReset([%s])",zoneName or ""))
    local zone = veafCombatZone.GetZone(zoneName)
    zone.flareResetFunctionId = nil
    zone:updateRadioMenu()
end

-- call the completion watchdog methods
function veafCombatZone.CompletionCheck(zoneName)
    veafCombatZone.logDebug(string.format("veafCombatZone.CompletionCheck([%s])",zoneName or ""))
    local zone = veafCombatZone.GetZone(zoneName)
    zone:completionCheck()
end

---
--- lists all units and statics (and their groups names) in a trigger zone
---
function veafCombatZone.findUnitsInTriggerZone(triggerZoneName)
    local triggerZone = trigger.misc.getZone(triggerZoneName)
    
    local units_by_name = {}
    local l_units = mist.DBs.units	--local reference for faster execution
    local units = {}
    local groupNames = {}
    local alreadyAddedGroups = {}
    local zoneCoordinates = {}
    zoneCoordinates = {radius = triggerZone.radius, x = triggerZone.point.x, y = triggerZone.point.y, z = triggerZone.point.z}
    
    -- the following code is liberally adapted from MiST (thanks Grimes !)
    for coa, coa_tbl in pairs(l_units) do
        for country, country_table in pairs(coa_tbl) do
            for unit_type, unit_type_tbl in pairs(country_table) do
                if type(unit_type_tbl) == 'table' then
                    for group_ind, group_tbl in pairs(unit_type_tbl) do
                        if type(group_tbl) == 'table' then
                            for unit_ind, mist_unit in pairs(group_tbl.units) do
                                local unitName = mist_unit.unitName
                                local unit = Unit.getByName(unitName)
                                if not unit then 
                                    unit = StaticObject.getByName(unitName)
                                end
                                if unit then
                                    local unit_pos = unit:getPosition().p
                                    if unit_pos then
                                        if (((unit_pos.x - zoneCoordinates.x)^2 + (unit_pos.z - zoneCoordinates.z)^2)^0.5 <= zoneCoordinates.radius) then
                                            veafCombatZone.logTrace(string.format("adding unit [%s]", unitName))
                                            veafCombatZone.logTrace(string.format("unit:getCategory() = [%d]", unit:getCategory()))
                                            local groupName = nil
                                            if (unit:getCategory() == 3) or (unit:getCategory() == 4) then
                                                groupName = unitName -- default for static objects = groups themselves
                                            else
                                                groupName = unit:getGroup():getName()
                                            end
                                            veafCombatZone.logTrace(string.format("groupName = %s", groupName))
                                            if string.sub(groupName:upper(),1,string.len(triggerZoneName))==triggerZoneName:upper() then
                                                units[#units + 1] = unit
                                                if not alreadyAddedGroups[groupName] then 
                                                    alreadyAddedGroups[groupName] = groupName
                                                    groupNames[#groupNames + 1] = groupName
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
    end

    veafCombatZone.logTrace(string.format("found %d units (%d groups) in zone", #units, #groupNames))   
    return {units, groupNames}
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Radio menu and help
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Build the initial radio menu
function veafCombatZone.buildRadioMenu()
    veafCombatZone.logDebug("buildRadioMenu()")
    veafCombatZone.rootPath = veafRadio.addMenu(veafCombatZone.RadioMenuName)
    if not(veafRadio.skipHelpMenus) then
        veafRadio.addCommandToSubmenu("HELP", veafCombatZone.rootPath, veafCombatZone.help, nil, veafRadio.USAGE_ForGroup)
    end
        
    -- sort the zones alphabetically
    names = {}
    sortedZones = {}
    for _, zone in pairs(veafCombatZone.zonesDict) do
        table.insert(sortedZones, {name=zone:getMissionEditorZoneName(), sort=zone:getFriendlyName()})
    end
    function compare(a,b)
		if not(a) then 
			a = {}
		end
		if not(a["sort"]) then 
			a["sort"] = 0
		end
		if not(b) then 
			b = {}
		end
		if not(b["sort"]) then 
			b["sort"] = 0
		end	
        return a["sort"] < b["sort"]
    end     
    table.sort(sortedZones, compare)
    for i = 1, #sortedZones do
        table.insert(names, sortedZones[i].name)
    end

    veafCombatZone.logTrace("veafCombatZone.buildRadioMenu() - dumping names")
    for i = 1, #names do
        veafCombatZone.logTrace("veafCombatZone.buildRadioMenu().names -> " .. names[i])
    end
    
    for _, zoneName in pairs(names) do
        local zone = veafCombatZone.GetZone(zoneName)
        zone:updateRadioMenu(true)
    end
    
    veafRadio.refreshRadioMenu()
end

function veafCombatZone.help(unitName)
    local text =
        'Combat zones are defined by the mission maker, and listed here\n' ..
        'You can activate and desactivate them at will,\n' ..
        'as well as ask for information, JTAC laser and smoke.'

    veaf.outTextForUnit(unitName, text, 30)
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- initialisation
-------------------------------------------------------------------------------------------------------------------------------------------------------------
function veafCombatZone.initialize()
    veafCombatZone.logInfo("Initializing module")
    veafCombatZone.buildRadioMenu()
end

veafCombatZone.logInfo(string.format("Loading version %s", veafCombatZone.Version))
