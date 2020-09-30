-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- VEAF remote callback functions for DCS World
-- By zip (2020)
--
-- Features:
-- ---------
-- * This module offers support for calling script from a web server
--
-- Prerequisite:
-- ------------
-- * This script requires DCS 2.5.1 or higher and MIST 4.3.74 or higher.
-- * It also requires NIOD !
-- * It also requires all the veaf scripts !
--
-- Basic Usage:
-- ------------
-- TODO
--
-------------------------------------------------------------------------------------------------------------------------------------------------------------

veafRemote = {}

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Global settings. Stores the script constants
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Identifier. All output in DCS.log will start with this.
veafRemote.Id = "REMOTE - "

--- Version.
veafRemote.Version = "1.1.0"

-- trace level, specific to this module
veafRemote.Trace = false

-- if false, SLMOD will not be called for regular commands
veafRemote.USE_SLMOD = false

-- if false, SLMOD will never be called
veafRemote.USE_SLMOD_FOR_SPECIAL_COMMANDS = true

veafRemote.SecondsBetweenFlagMonitorChecks = 5

veafRemote.CommandStarter = "_remote"

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Do not change anything below unless you know what you are doing!
-------------------------------------------------------------------------------------------------------------------------------------------------------------

veafRemote.monitoredFlags = {}
veafRemote.monitoredCommands = {}
veafRemote.maxMonitoredFlag = 27000

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Utility methods
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafRemote.logError(message)
    veaf.logError(veafRemote.Id .. message)
end

function veafRemote.logInfo(message)
    veaf.logInfo(veafRemote.Id .. message)
end

function veafRemote.logDebug(message)
    veaf.logDebug(veafRemote.Id .. message)
end

function veafRemote.logTrace(message)
    if message and veafRemote.Trace then 
        veaf.logTrace(veafRemote.Id .. message)
    end
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- SLMOD monitoring
-------------------------------------------------------------------------------------------------------------------------------------------------------------
function veafRemote.monitorWithSlModSpecialCommand(command, script, requireAdmin, flag, coalition)
    mist.scheduleFunction(veafRemote._monitorWithSlMod, {command, script, flag, coalition, requireAdmin, true}, timer.getTime()+5)    
end

function veafRemote.monitorWithSlMod(command, script, requireAdmin, flag, coalition)
    mist.scheduleFunction(veafRemote._monitorWithSlMod, {command, script, flag, coalition, requireAdmin, false}, timer.getTime()+5)    
end

function veafRemote._monitorWithSlMod(command, script, flag, coalition, requireAdmin, isSpecialCommand)
    
    local actualFlag = flag
    if not actualFlag then
        actualFlag = veafRemote.maxMonitoredFlag + 1
        veafRemote.maxMonitoredFlag = actualFlag
    end
    
    local actualCoalition = coalition or "all"
    
    local actualRequireAdmin = requireAdmin
    if actualRequireAdmin == nil then
        actualRequireAdmin = true
    end
    
    local isSpecialCommand = isSpecialCommand
    if isSpecialCommand == nil then
        isSpecialCommand = false
    end

    veafRemote.logTrace(string.format("setting remote configuration for command=[%s], script=[%s], flag=[%d], requireAdmin=[%s], coalition=[%s]",tostring(command), tostring(script), actualFlag, tostring(actualRequireAdmin), tostring(actualCoalition)))
    veafRemote.monitoredCommands[command:lower()] = {script=script, requireAdmin=requireAdmin}
    if veafRemote.USE_SLMOD or (veafRemote.USE_SLMOD_FOR_SPECIAL_COMMANDS and isSpecialCommand) then 
        if slmod  then
            slmod.chat_cmd(command, actualFlag, -1, actualCoalition, actualRequireAdmin)
            veafRemote.startMonitoringFlag(actualFlag, script)
        end
    end
end

function veafRemote.startMonitoringFlag(flag, scriptToExecute)
    -- reset the flag
    trigger.action.setUserFlag(flag, false)
    veafRemote.monitoredFlags[flag] = scriptToExecute
    veafRemote._monitorFlags()
end

function veafRemote._monitorFlags()
    --veafRemote.logTrace("veafRemote._monitorFlags()")
    for flag, scriptToExecute in pairs(veafRemote.monitoredFlags) do
        --veafRemote.logTrace(string.format("veafRemote._monitorFlags() - checking flag %s", flag))
        local flagValue = trigger.misc.getUserFlag(flag)
        --veafRemote.logTrace(string.format("veafRemote._monitorFlags() - flagValue = [%d]", flagValue))
        if flagValue > 0 then
            -- call the script
            veafRemote.logDebug(string.format("veafRemote._monitorFlags() - flag %s was TRUE", flag))
            veafRemote.logDebug(string.format("veafRemote._monitorFlags() - calling lua code [%s]", scriptToExecute))
            local result, err = mist.utils.dostring(scriptToExecute)
            if result then
                veafRemote.logDebug(string.format("veafRemote._monitorFlags() - lua code was successfully called for flag [%s]", flag))
            else
                veafRemote.logError(string.format("veafRemote._monitorFlags() - error [%s] calling lua code for flag [%s]", err, flag))
            end
            -- reset the flag
            trigger.action.setUserFlag(flag, false)
            veafRemote.logDebug(string.format("veafRemote._monitorFlags() - flag [%s] was reset", flag))
        else
            --veafRemote.logTrace(string.format("veafRemote._monitorFlags() - flag %s was FALSE or not set", flag))
        end
    end
    mist.scheduleFunction(veafRemote._monitorFlags, nil, timer.getTime()+veafRemote.SecondsBetweenFlagMonitorChecks)    
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- NIOD callbacks
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafRemote.addNiodCallback(name, parameters, code)
    if niod then 
        veafRemote.logInfo("Adding NIOD function "..name)
        niod.functions[name] = function(payload)
        -- start of inline function
            
            veafRemote.logDebug(string.format("niod callback [%s] was called with payload %s", veaf.p(name), veaf.p(payload)))
            
            local errors = {}
            
            -- check mandatory parameters presence
            for parameterName, parameterData in pairs(parameters) do
                veafRemote.logTrace(string.format("checking if parameter [%s] is mandatory", veaf.p(parameterName)))
                if parameterData and parameterData.mandatory then 
                    if not (payload and payload[parameterName]) then 
                        local text = "missing mandatory parameter "..parameterName
                        veafRemote.logTrace(text)
                        table.insert(errors, text)
                    end
                end
            end
            
            -- check parameters type
            if payload then 
                for parameterName, value in pairs(payload) do
                    local parameter = parameters[parameterName]
                    if not parameter then 
                        table.insert(errors, "unknown parameter "..parameterName)
                    elseif value and not(type(value) == parameter.type) then
                        local text =  string.format("parameter %s should have type %s, has %s ", parameterName, parameter.type, type(value))
                        veafRemote.logTrace(text)
                        table.insert(errors, text)
                    end
                end
            end
            
            -- stop on error
            if #errors > 0 then
                local errorMessage = ""
                for _, error in pairs(errors) do
                    errorMessage = errorMessage .. "\n" .. error
                end
                veafRemote.logError(string.format("niod callback [%s] was called with incorrect parameters :", veaf.p(name), errorMessage))
                return errorMessage
            else
                veafRemote.logTrace(string.format("payload = %s", veaf.p(payload)))
                veafRemote.logTrace(string.format("unpacked payload = %s", veaf.p(veaf.safeUnpack(payload))))
                local status, retval = pcall(code,veaf.safeUnpack(payload))
                if status then
                    return retval
                else
                    return "an error occured : "..veaf.p(status)
                end
            end

        end -- of inline function

    else
        veafRemote.logError("NIOD is not loaded !")
    end
end

function veafRemote.addNiodCommand(name, command)
    veafRemote.addNiodCallback(
        name, 
        {
            parameters={   mandatory=false, type="string"}, 
            x={   mandatory=false, type="number"}, 
            y={   mandatory=false, type="number"}, 
            z={   mandatory=false, type="number"}, 
            silent={    mandatory=false, type="boolean"}
        },
        function(parameters, x, y, z, silent)
            veaf.logDebug(string.format("niod->command %s (%s, %s, %s, %s, %s)", veaf.p(parameters), veaf.p(x), veaf.p(y), veaf.p(z), veaf.p(silent)))
            return veafRemote.executeCommand({x=x or 0, y=y or 0, z=z or 0}, command..parameters, 99)
        end
    )
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- default endpoints list
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafRemote.buildDefaultList()
    local TEST = false

    -- add standard commands
    veafRemote.monitorWithSlModSpecialCommand("-veaf test", [[trigger.action.outText("VEAF - test command received from remote, flag=66600", 10)]], false, 66600)
    veafRemote.monitorWithSlModSpecialCommand("-veaf login", [[veafSecurity.authenticate(1)]])
    veafRemote.monitorWithSlModSpecialCommand("-veaf logout", [[veafSecurity.logout(true)]])

    -- add all the combat missions
    if veafCombatMission then
        for _, mission in pairs(veafCombatMission.missionsDict) do
            local missionName = mission:getName()
            veafRemote.logTrace(string.format("Adding %s", missionName))
            veafRemote.monitorWithSlMod("-veaf start-silent-" .. missionName, [[ veafCombatMission.ActivateMission("]] .. missionName .. [[", true) ]])
            veafRemote.monitorWithSlMod("-veaf stop-silent-" .. missionName, [[ veafCombatMission.DesactivateMission("]] .. missionName .. [[", true) ]])
            veafRemote.monitorWithSlMod("-veaf start-" .. missionName, [[ veafCombatMission.ActivateMission("]] .. missionName .. [[", false) ]])
            veafRemote.monitorWithSlMod("-veaf stop-" .. missionName, [[ veafCombatMission.DesactivateMission("]] .. missionName .. [[", false) ]])
        end
    end

    if TEST then

        -- test
        veafRemote.addNiodCallback(
            "test", 
            {
                param1S_M={  mandatory=true, type="string"}, 
                param2S={  mandatory=false, type="string"}, 
                param3N={  mandatory=false, type="number"}, 
                param4B={  mandatory=false, type="boolean"}, 
            },
            function(param1S_M, param2S, param3N, param4B)
                local text = string.format("niod.test(%s, %s, %s, %s)", veaf.p(param1S_M), veaf.p(param2S), veaf.p(param3N), veaf.p(param4B))
                veafRemote.logDebug(text)
                trigger.action.outText(text, 15)
            end
        )
        -- login
        veafRemote.addNiodCallback(
            "login", 
            {
                password={  mandatory=true, type="string"}, 
                timeout={   mandatory=false, type="number"}, 
                silent={    mandatory=false, type="boolean"}
            },
            function(password, timeout, silent)
                veafRemote.logDebug(string.format("niod.login(%s, %s, %s)",veaf.p(password), veaf.p(timeout),veaf.p(silent))) -- TODO remove password from log
                if veafSecurity.checkPassword_L1(password) then
                    veafSecurity.authenticate(silent, timeout)
                    return "Mission is unlocked"
                else
                    return "wrong password"
                end
            end
        )

    end
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Event handler functions.
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Function executed when a mark has changed. This happens when text is entered or changed.
function veafRemote.onEventMarkChange(eventPos, event)
    -- Check if marker has a text and contains an alias
    if event.text ~= nil then
        
        -- Analyse the mark point text and extract the keywords.
        local command, password = veafRemote.markTextAnalysis(event.text)

        if command then

            -- do the magic
            if veafRemote.executeCommand(command, password) then 
                -- Delete old mark.
                veafRemote.logTrace(string.format("Removing mark # %d.", event.idx))
                trigger.action.removeMark(event.idx)
            end
        end
    end
end

--- Extract keywords from mark text.
function veafRemote.markTextAnalysis(text)
    veafRemote.logTrace(string.format("veafRemote.markTextAnalysis(text=[%s])", tostring(text)))
  
    if text then 
        -- extract command and password
        local password, command = text:match(veafRemote.CommandStarter.."#?([^%s]*)%s+(.+)")
        if command then
            veafRemote.logTrace(string.format("command = [%s]", command))
            return command, password
        end
    end
    return nil
end

-- execute a command
function veafRemote.executeCommand(command, password)
    local command = command or ""
    local password = password or ""
    veafRemote.logDebug(string.format("veafRemote.ExecuteCommand([%s])",command))
    if not(veafSecurity.checkPassword_L1(password)) then
        veafRemote.logError(string.format("veafRemote.ExecuteCommand([%s]) - bad or missing password",command))
        trigger.action.outText("Bad or missing password",5)
        return false
    end
    local commandData = veafRemote.monitoredCommands[command:lower()]
    if commandData then 
        local scriptToExecute = commandData.script
        veafRemote.logTrace(string.format("found script [%s] for command [%s]", scriptToExecute, command))
        local authorized = (not(commandData.requireAdmin)) or (veafSecurity.checkSecurity_L9(password))
        if not authorized then 
            return false
        else
        local result, err = mist.utils.dostring(scriptToExecute)
        if result then
            veafRemote.logDebug(string.format("veafRemote.executeCommand() - lua code was successfully called for script [%s]", scriptToExecute))
            return true
        else
            veafRemote.logError(string.format("veafRemote.executeCommand() - error [%s] calling lua code for script [%s]", err, scriptToExecute))
            return false
        end
        end
    else
        veafRemote.logError(string.format("veafRemote.ExecuteCommand : cannot find command [%s]",command or ""))
    end
    return false
end


-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- initialisation
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafRemote.initialize()
    veafRemote.logInfo("Initializing module")
    veafRemote.buildDefaultList()
    veafMarkers.registerEventHandler(veafMarkers.MarkerChange, veafRemote.onEventMarkChange)
end

veafRemote.logInfo(string.format("Loading version %s", veafRemote.Version))
