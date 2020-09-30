-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- VEAF shortcuts supporting functions for DCS World
-- By zip (2020)
--
-- Features:
-- ---------
-- * This module offers support for commands aliases and radio menu shortcuts
--
-- Prerequisite:
-- ------------
-- * This script requires DCS 2.5.1 or higher and MIST 4.3.74 or higher.
-- * It also requires all the veaf scripts !
--
-- Basic Usage:
-- ------------
-- TODO
--
-------------------------------------------------------------------------------------------------------------------------------------------------------------

veafShortcuts = {}

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Global settings. Stores the script constants
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Identifier. All output in DCS.log will start with this.
veafShortcuts.Id = "SHORTCUTS - "

--- Version.
veafShortcuts.Version = "1.4.0"

-- trace level, specific to this module
veafShortcuts.Debug = false
veafShortcuts.Trace = false

veafShortcuts.RadioMenuName = "SHORTCUTS"

veafShortcuts.AliasStarter = "-"
-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Do not change anything below unless you know what you are doing!
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Radio menus paths
veafShortcuts.rootPath = nil

-- Aliases list (table of VeafAlias objects)
veafShortcuts.aliases = {}

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Utility methods
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafShortcuts.logError(message)
    veaf.logError(veafShortcuts.Id .. message)
end

function veafShortcuts.logInfo(message)
    veaf.logInfo(veafShortcuts.Id .. message)
end

function veafShortcuts.logDebug(message)
    if message and veafShortcuts.Debug then 
        veaf.logDebug(veafShortcuts.Id .. message)
    end
end

function veafShortcuts.logTrace(message)
    if message and veafShortcuts.Trace then 
        veaf.logTrace(veafShortcuts.Id .. message)
    end
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- VeafAlias object
-------------------------------------------------------------------------------------------------------------------------------------------------------------
VeafAlias =
{
    -- name
    name,
    -- description
    description,
    -- hidden from HELP
    hidden,
    -- the command that must be substituted to the alias
    veafCommand,
    -- list of parameters that will be randomized if not present
    randomParameters,
    -- if TRUE, security is bypassed
    bypassSecurity,
}
VeafAlias.__index = VeafAlias

function VeafAlias:new()
    local self = setmetatable({}, VeafAlias)
    self.veafCommand = nil
    self.bypassSecurity = false
    self.hidden = false
    self.randomParameters = {}
    self.description = nil
    return self
end

---
--- setters and getters
---

function VeafAlias:setName(value)
    veafShortcuts.logTrace(string.format("VeafAlias[%s]:setName([%s])", self.name or "", value or ""))
    self.name = value
    return self
end

function VeafAlias:getName()
    return self.name
end


function VeafAlias:setVeafCommand(value)
    veafShortcuts.logTrace(string.format("VeafAlias[%s]:setVeafCommand([%s])", self.name, value or ""))
    self.veafCommand = value
    return self
end

function VeafAlias:getVeafCommand()
    return self.veafCommand
end

function VeafAlias:addRandomParameter(name, low, high)
    veafShortcuts.logTrace(string.format("VeafAlias[%s]:addRandomParameter([%s], %s, %s)", self.name, name or "", low or "", high or ""))
    table.insert(self.randomParameters, { name = name, low = low or 1, high = high or 6})
    return self
end

function VeafAlias:getRandomParameters()
    return self.randomParameters
end

function VeafAlias:setDescription(value)
    veafShortcuts.logTrace(string.format("VeafAlias[%s]:setDescription([%s])", self.name, value or ""))
    self.description = value
    return self
end

function VeafAlias:getDescription()
    return self.description
end

function VeafAlias:setBypassSecurity(value)
    veafShortcuts.logTrace(string.format("VeafAlias[%s]:setBypassSecurity([%s])", self.name, tostring(value) or ""))
    self.bypassSecurity = value
    return self
end

function VeafAlias:isBypassSecurity()
    return self.bypassSecurity
end

function VeafAlias:setHidden(value)
    veafShortcuts.logTrace(string.format("VeafAlias[%s]:setHidden([%s])", self.name, tostring(value) or ""))
    self.hidden = value
    return self
end

function VeafAlias:isHidden()
    return self.hidden
end

---
--- other methods
---

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- global functions
-------------------------------------------------------------------------------------------------------------------------------------------------------------

-- search for an alias
function veafShortcuts.GetAlias(aliasName)
    veafShortcuts.logDebug(string.format("veafShortcuts.GetAlias([%s])",aliasName or ""))
    veafShortcuts.logDebug(string.format("Searching for alias with name [%s]", aliasName))

    -- find the desired alias in the aliases list
    local alias = nil

    for _, a in pairs(veafShortcuts.aliases) do
        if a:getName():lower() == aliasName:lower() then
            alias = a
            break
        end
    end
    
    if not alias then 
        local message = string.format("VeafAlias [%s] was not found !",aliasName)
        veafShortcuts.logError(message)
        trigger.action.outText(message,5)
    end

    return alias
end

-- add an alias
function veafShortcuts.AddAlias(alias)
    veafShortcuts.logDebug(string.format("veafShortcuts.AddAlias([%s])",alias:getName() or ""))
    veafShortcuts.logInfo(string.format("Adding alias [%s]", alias:getName()))
    table.insert(veafShortcuts.aliases, alias)
    return alias
end

-- execute an alias command
function veafShortcuts.ExecuteAlias(aliasName, remainingCommand, position, coalition, spawnedGroups)
    veafShortcuts.logDebug(string.format("veafShortcuts.ExecuteAlias([%s],[%s],[%d])",aliasName or "",remainingCommand or "",coalition or 99))
    local alias = veafShortcuts.GetAlias(aliasName)
    if alias then 
        veafShortcuts.logTrace(string.format("found VeafAlias[%s]",alias:getName() or ""))
        local command = alias:getVeafCommand()
        for _, parameter in pairs(alias:getRandomParameters()) do
            veafShortcuts.logTrace(string.format("randomizing [%s]",parameter.name or ""))
            local value = math.random(parameter.low, parameter.high)
            veafShortcuts.logTrace(string.format("got [%d]",value))
            command = string.format("%s, %s %d",command, parameter.name, value)
        end
        local command = command .. (remainingCommand or "")
        veafShortcuts.logTrace(string.format("command = [%s]",command or ""))
        -- check for shortcuts
        --if veafShortcuts.executeCommand(position, command, coalition) then
        --    return true
        -- check for SPAWN module commands
        --else
        if veafSpawn.executeCommand(position, command, coalitionForSpawn, doNotBypassSecurity or true, spawnedGroups) then
            return true
        -- check for NAMED POINT module commands
        elseif veafNamedPoints.executeCommand(position, {text=command, coalition=-1}, doNotBypassSecurity or true) then
            return true
        elseif veafCasMission.executeCommand(position, command, coalition, doNotBypassSecurity or true) then
            return true
        elseif veafSecurity.executeCommand(position, command, doNotBypassSecurity or true) then
            return true
        elseif veafMove.executeCommand(position, command, doNotBypassSecurity or true) then
            return true
        elseif veafRadio.executeCommand(position, command, coalition, doNotBypassSecurity or true) then
            return true
        else
            return false
        end
    else
        veafShortcuts.logError(string.format("veafShortcuts.ExecuteAlias : cannot find alias [%s]",aliasName or ""))
    end
    return false
end

function veafShortcuts.GetWeatherAtCurrentPosition(unitName)
    veafNamedPoints.logDebug(string.format("veafShortcuts.GetWeatherAtCurrentPosition(unitName=%s)",unitName))
    local unit = veafRadio.getHumanUnitOrWingman(unitName)
    if unit then
        local weatherReport = veaf.weatherReport(unit:getPosition().p, nil, true) -- include LASTE
        veaf.outTextForUnit(unitName, weatherReport, 30)
    end
end

function veafShortcuts.GetWeatherAtClosestPoint(unitName)
    veafNamedPoints.logDebug(string.format("veafShortcuts.GetWeatherAtClosestPoint(unitName=%s)",unitName))
    local unit = veafRadio.getHumanUnitOrWingman(unitName)
    if unit then
        local weatherReport = veaf.weatherReport(unit:getPosition().p, nil, true) -- include LASTE
        veaf.outTextForUnit(unitName, weatherReport, 30)
    end
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Event handler functions.
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Function executed when a mark has changed. This happens when text is entered or changed.
function veafShortcuts.onEventMarkChange(eventPos, event)
    if veafShortcuts.executeCommand(eventPos, event.text, event.coalition) then 
        
        -- Delete old mark.
        veafShortcuts.logTrace(string.format("Removing mark # %d.", event.idx))
        trigger.action.removeMark(event.idx)

    end
end

function veafShortcuts.executeCommand(eventPos, eventText, eventCoalition, spawnedGroups)
    -- Check if marker has a text and contains an alias
    if eventText ~= nil then
        
        -- Analyse the mark point text and extract the keywords.
        local alias, remainder = veafShortcuts.markTextAnalysis(eventText)

        if alias then

            -- do the magic
            if veafShortcuts.ExecuteAlias(alias, remainder, eventPos, eventCoalition, spawnedGroups) then 
                return true
            else 
                return false
            end
        end
    end

    -- None of the keywords matched.
    return false
end

--- Extract keywords from mark text.
function veafShortcuts.markTextAnalysis(text)
    if text then 
  
        veafShortcuts.logTrace(string.format("veafShortcuts.markTextAnalysis(text=[%s])", text))
    
        -- check for the alias starter
        if text:sub(1,1) == veafShortcuts.AliasStarter then
            veafShortcuts.logTrace("found veafShortcuts.AliasStarter")

            -- extract alias and remainder
            local alias = text:match("(-[%a%d]+)")
            if alias then
                veafShortcuts.logTrace(string.format("alias = [%s]", alias))
                local _, remainder = text:match("(-[%a%d]+)([, ].*)")
                if remainder then 
                    veafShortcuts.logTrace(string.format("remainder = [%s]", remainder))
                end
                return alias, remainder
            end
        end

    end
    return nil
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Radio menu and help
-------------------------------------------------------------------------------------------------------------------------------------------------------------
function veafShortcuts.helpAllAliases(unitName)
    local text = 'List of all aliases:\n'
            
    for _, a in pairs(veafShortcuts.aliases) do
        if not a:isHidden() then
            local line = a:getName()
            if a:getDescription() then
                line = line .. " -> " .. a:getDescription()
            end
            text = text .. line .. "\n"
        end
    end
    veaf.outTextForUnit(unitName, text, 30)
end

--- Build the initial radio menu
function veafShortcuts.buildRadioMenu()
    veafShortcuts.logDebug("buildRadioMenu()")
    
    --if veafRadio.skipHelpMenus then return end -- completely skip the menu since there are only help elements
    
    veafShortcuts.rootPath = veafRadio.addMenu(veafShortcuts.RadioMenuName)
    
    --if not(veafRadio.skipHelpMenus) then
        veafRadio.addCommandToSubmenu("HELP - all aliases", veafShortcuts.rootPath, veafShortcuts.helpAllAliases, nil, veafRadio.USAGE_ForAll)
    --end

    -- these ones need veafNamedPoints.lua
    --veafRadio.addCommandToSubmenu("Weather on closest point" , veafShortcuts.rootPath, veafNamedPoints.getWeatherAtClosestPoint, nil, veafRadio.USAGE_ForGroup)    
    --veafRadio.addCommandToSubmenu("ATC on closest point" , veafShortcuts.rootPath, veafNamedPoints.getAtcAtClosestPoint, nil, veafRadio.USAGE_ForGroup)    
    
    veafRadio.refreshRadioMenu()
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- initialisation
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafShortcuts.initialize()
    veafShortcuts.logInfo("Initializing module")
    veafShortcuts.buildDefaultList()
    veafShortcuts.buildRadioMenu()
    veafMarkers.registerEventHandler(veafMarkers.MarkerChange, veafShortcuts.onEventMarkChange)
end

veafShortcuts.logInfo(string.format("Loading version %s", veafShortcuts.Version))

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- default aliases list
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafShortcuts.buildDefaultList()
    -- generic sam groups
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-sam")
            :setDescription("Random SAM battery")
            :setVeafCommand("_spawn samgroup")
            :addRandomParameter("defense", 1, 5)
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-samLR")
            :setDescription("Random long range SAM battery")
            :setVeafCommand("_spawn samgroup")
            :addRandomParameter("defense", 4, 5)
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-samSR")
            :setDescription("Random short range SAM battery")
            :setVeafCommand("_spawn samgroup")
            :addRandomParameter("defense", 2, 3)
            :setBypassSecurity(true)
    )
    -- specific air defenses groups and units  
    veafShortcuts.AddAlias(
        VeafAlias:new()
        :setName("-sa2")
        :setDescription("SA-2 Guideline (S-75 Dvina) battery")
        :setVeafCommand("_spawn group, name sa2")
        :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
        :setName("-sa3")
        :setDescription("SA-3 Goa (S-125 Neva/Pechora) battery")
        :setVeafCommand("_spawn group, name sa3")
        :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-sa6")
            :setDescription("SA-6 Gainful (2K12 Kub) battery")
            :setVeafCommand("_spawn group, name sa6")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-sa8")
            :setDescription("SA-8 Osa (9K33 Osa) sam vehicle")
            :setVeafCommand("_spawn unit, name Osa 9A33 ln")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-sa9")
            :setDescription("SA-9 Strela-1 (9K31 Strela-1) sam vehicle")
            :setVeafCommand("_spawn unit, name Strela-1 9P31")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-sa10")
            :setDescription("SA-10 Grumble (S-300) battery")
            :setVeafCommand("_spawn group, name sa10")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-sa11")
            :setDescription("SA-11 Gadfly (9K37 Buk) battery")
            :setVeafCommand("_spawn group, name sa11")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-sa13")
            :setDescription("SA-13 Strela (9A35M3) sam vehicle")
            :setVeafCommand("_spawn unit, name Strela-10M3")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-sa15")
            :setDescription("SA-15 Gauntlet (9K330 Tor) sam vehicle")
            :setVeafCommand("_spawn unit, name sa15")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-sa18")
            :setDescription("SA-18 manpad soldier")
            :setVeafCommand("_spawn unit, name SA-18 Igla-S manpad")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-sa19")
            :setDescription("SA-19 Tunguska (2K22 Tunguska) sam vehicle")
            :setVeafCommand("_spawn unit, name 2S6 Tunguska")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-shilka")
            :setDescription("ZSU-23-4 Shilka AAA vehicle")
            :setVeafCommand("_spawn unit, name ZSU-23-4 Shilka")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-zu23")
            :setDescription("ZU-23 AAA vehicle")
            :setVeafCommand("_spawn unit, name Ural-375 ZU-23")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-manpads")
            :setDescription("mutiple SA-18 manpad soldier peppered in a wide radius")
            :setVeafCommand("_spawn unit, name SA-18 Igla-S manpad, radius 5000")
            :addRandomParameter("multiplier", 3, 6)
            :setBypassSecurity(true)
    )


    -- shortcuts to commands
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-point")
            :setDescription("Name a point on the map")
            :setVeafCommand("_name point")
            :setBypassSecurity(true)
    )
    -- veafShortcuts.AddAlias(
    --     VeafAlias:new()
    --         :setName("-login")
    --         :setDescription("Unlock the system")
    --         :setHidden(true)
    --         :setVeafCommand("_auth")
    --         :setBypassSecurity(true)
    -- )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-logout")
            :setDescription("Lock the system")
            :setHidden(true)
            :setVeafCommand("_auth logout")
            :setBypassSecurity(true)
    )
    -- shortcuts to specific groups
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-mortar")
            :setDescription("Mortar team")
            :setVeafCommand("_spawn group, name mortar, country USA")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-arty")
            :setDescription("M-109 artillery battery")
            :setVeafCommand("_spawn group, name M-109, country USA")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-cargoships")
            :setDescription("Cargo ships")
            :setVeafCommand("_spawn group, name cargoships-nodef, country RUSSIA, offroad, speed 60")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-escortedcargoships")
            :setDescription("Cargo ships (escorted)")
            :setVeafCommand("_spawn group, name cargoships-escorted, country RUSSIA, offroad, speed 60")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-combatships")
            :setDescription("Combat ships")
            :setVeafCommand("_spawn group, name combatships, country RUSSIA, offroad, speed 60")
            :setBypassSecurity(true)
    )
    -- shortcuts to dynamic groups
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-armor")
            :setDescription("Dynamic armor group")
            :setVeafCommand("_spawn armorgroup")
            :addRandomParameter("defense", 1, 3)
            :addRandomParameter("armor", 2, 4)
            :addRandomParameter("size", 4, 8)
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-infantry")
            :setDescription("Dynamic infantry section")
            :setVeafCommand("_spawn infantrygroup")
            :addRandomParameter("defense", 0, 5)
            :addRandomParameter("armor", 0, 5)
            :addRandomParameter("size", 4, 8)
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-transport")
            :setDescription("Dynamic transport company")
            :setVeafCommand("_spawn transportgroup")
            :addRandomParameter("defense", 0, 3)
            :addRandomParameter("size", 10, 25)
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-combat")
            :setDescription("Dynamic combat group")
            :setVeafCommand("_spawn combatgroup")
            :addRandomParameter("defense", 1, 3)
            :addRandomParameter("armor", 2, 4)
            :addRandomParameter("size", 1, 4)
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-cas")
            :setDescription("Generate a random CAS group for training")
            :setVeafCommand("_cas, disperse")
            :setBypassSecurity(true)
    )
    -- radio shortcuts
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-send")
            :setDescription("Send radio message - needs \"MESSAGE\"")
            :setVeafCommand("_radio transmit, message")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-play")
            :setDescription("Play sound over radio - needs \"FILENAME\"")
            :setVeafCommand("_radio play, path")
            :setBypassSecurity(true)
    )
    -- other shortcuts
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-convoy")
            :setDescription("Convoy - needs \", dest POINTNAME\"")
            :setVeafCommand("_spawn convoy")
            :addRandomParameter("defense", 0, 3)
            :addRandomParameter("armor", 0, 4)
            :addRandomParameter("size", 6, 15)
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-jtac")
            :setDescription("JTAC humvee")
            :setVeafCommand("_spawn jtac")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-shell")
            :setDescription("Artillery shelling of a zone with HE")
            :setVeafCommand("_spawn bomb")
            :addRandomParameter("shells", 25, 40)
            :addRandomParameter("radius", 350, 500)
            :addRandomParameter("power", 100, 300)
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-light")
            :setDescription("Illumination by artillery shelling of a zone")
            :setVeafCommand("_spawn flare, radius 1000")
            :addRandomParameter("shells", 20, 30)
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-smoke")
            :setDescription("Spawn a single white smoke")
            :setVeafCommand("_spawn smoke, color white, shells 1, radius 1")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-tanker")
            :setDescription("move a tanker to a specific location ; must follow with the tanker group name")
            :setVeafCommand("_move tanker, name")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-tankerlow")
            :setDescription("move a tanker to a specific location, altitude 10000 and speed 250 ; must follow with the tanker group name")
            :setVeafCommand("_move tanker, altitude 10000, speed 250, name")
            :setBypassSecurity(true)
    )
    veafShortcuts.AddAlias(
        VeafAlias:new()
            :setName("-tacan")
            :setDescription("create a portable TACAN beacon ; must follow with the tacan channel")
            :setVeafCommand("_spawn tacan, band X, channel")
            :setBypassSecurity(true)
    )
end
