-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- VEAF carrier command and functions for DCS World
-- By zip (2018)
--
-- Features:
-- ---------
-- New version using Moose.AIRBOSS
--
-- Prerequisite:
-- ------------
-- * This script requires DCS 2.5.1 or higher and MIST 4.3.74 or higher.
-- * It also requires Moose
-- * It also requires the base veaf.lua script library (version 1.0 or higher)
-- * It also requires the base veafRadio.lua script library (version 1.0 or higher)
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
--     * OPEN --> Browse to the location of MOOSE and click OK.
--     * ACTION "DO SCRIPT FILE"
--     * OPEN --> Browse to the location of veaf.lua and click OK.
--     * ACTION "DO SCRIPT FILE"
--     * OPEN --> Browse to the location of veafRadio.lua and click OK.
--     * ACTION "DO SCRIPT FILE"
--     * OPEN --> Browse to the location of this script and click OK.
--     * ACTION "DO SCRIPT"
--     * set the script command to "veafRadio.initialize();veafCarrierOperations2.initialize()" and click OK.
-- 4.) Save the mission and start it.
-- 5.) Have fun :)
--
-- Basic Usage:
-- ------------
-- Use the F10 radio menu to start and end carrier operations for every detected carrier group (having a group name like "CSG-*")
--
-------------------------------------------------------------------------------------------------------------------------------------------------------------

veafCarrierOperations2 = {}

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Global settings. Stores the script constants
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Identifier. All output in DCS.log will start with this.
veafCarrierOperations2.Id = "CARRIER2 - "

--- Version.
veafCarrierOperations2.Version = "2.0.3"

-- trace level, specific to this module
veafCarrierOperations2.Trace = false

veafCarrierOperations2.RadioMenuName = "CARRIER OPS 2"

---------------------------------------------------------------------------------------------------------------------------
-- Do not change anything below unless you know what you are doing!
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Radio menus paths
veafCarrierOperations2.rootPath = nil

--- Carrier info to store the status
veafCarrierOperations2.carrier = {}

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Utility methods
-------------------------------------------------------------------------------------------------------------------------------------------------------------
function veafCarrierOperations2.logError(message)
    veaf.logError(veafCarrierOperations2.Id .. message)
end

function veafCarrierOperations2.logInfo(message)
    veaf.logInfo(veafCarrierOperations2.Id .. message)
end

function veafCarrierOperations2.logDebug(message)
    veaf.logDebug(veafCarrierOperations2.Id .. message)
end

function veafCarrierOperations2.logTrace(message)
    if message and veafCarrierOperations2.Trace then 
        veaf.logTrace(veafCarrierOperations2.Id .. message)
    end
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Radio menu 
-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Start recovery function.
function veafCarrierOperations2.startRecovery(parameters)
    veafCarrierOperations2.logDebug(string.format("veafCarrierOperations2.startRecovery - parameters", veaf.p(parameters)))
    local params, unitName = veaf.safeUnpack(parameters)
    veafCarrierOperations2.logDebug(string.format("veafCarrierOperations2.startRecovery - params", veaf.p(params)))
    local case = params.case
    local time = params.time
    veafCarrierOperations2.logDebug(string.format("veafCarrierOperations2.startRecovery(%s, %d, %d)", unitName, case, time))
    veafCarrierOperations2.airbossCarrierObject.skipperTime=time
    veafCarrierOperations2.airbossCarrierObject.skipperSpeed=25
    veafCarrierOperations2.airbossCarrierObject.skipperOffset=math.random(0, 11)*30
    veafCarrierOperations2.airbossCarrierObject.skipperUturn=false
    veafCarrierOperations2.airbossCarrierObject:_SkipperStartRecovery(unitName, case)
end

-- Stop recovery function.
function veafCarrierOperations2.stopRecovery(unitName)
    veafCarrierOperations2.logDebug(string.format("veafCarrierOperations2.stopRecovery(%s)", unitName))
    veafCarrierOperations2.airbossCarrierObject:_SkipperStopRecovery(unitName)
end

--- Rebuild the radio menu
function veafCarrierOperations2.rebuildRadioMenu()
    veafCarrierOperations2.logDebug("veafCarrierOperations2.rebuildRadioMenu()")

    -- add specific protected recovery radio commands
    --veafRadio.addSecuredCommandToSubmenu( "Start CASE I - 45'",   veafCarrierOperations2.rootPath, veafCarrierOperations2.startRecovery, {case=1, time=45}, veafRadio.USAGE_ForGroup)
    veafRadio.addSecuredCommandToSubmenu( "Start CASE I - 90'",   veafCarrierOperations2.rootPath, veafCarrierOperations2.startRecovery, {case=1, time=90}, veafRadio.USAGE_ForGroup)
    veafRadio.addSecuredCommandToSubmenu( "Start CASE II - 90'",   veafCarrierOperations2.rootPath, veafCarrierOperations2.startRecovery, {case=2, time=90}, veafRadio.USAGE_ForGroup)
    veafRadio.addSecuredCommandToSubmenu( "Start CASE III - 90'",   veafCarrierOperations2.rootPath, veafCarrierOperations2.startRecovery, {case=3, time=90}, veafRadio.USAGE_ForGroup)
    veafRadio.addSecuredCommandToSubmenu( "Stop Recovery",   veafCarrierOperations2.rootPath, veafCarrierOperations2.stopRecovery, nil, veafRadio.USAGE_ForGroup)

    veafRadio.refreshRadioMenu()
end

--- Build the initial radio menu
function veafCarrierOperations2.buildRadioMenu()
    veafCarrierOperations2.logDebug("veafCarrierOperations2.buildRadioMenu")

    veafCarrierOperations2.rootPath = veafRadio.addSubMenu(veafCarrierOperations2.RadioMenuName)

    veafCarrierOperations2.rebuildRadioMenu()
end

function veafCarrierOperations2.initializeCarrierGroup()

    -- Create AIRBOSS object.
    veafCarrierOperations2.airbossCarrierObject=AIRBOSS:New(veafCarrierOperations2.carrier.carrierName)
    veafCarrierOperations2.airbossCarrierObject:SetLSORadio(veafCarrierOperations2.carrier.lsoFreq)
    veafCarrierOperations2.airbossCarrierObject:SetPatrolAdInfinitum()
    veafCarrierOperations2.airbossCarrierObject:SetDefaultMessageDuration(30) -- messages are displayed for 30 seconds

    -- Set folder of airboss sound files within miz file.
    veafCarrierOperations2.airbossCarrierObject:SetSoundfilesFolder("Airboss Soundfiles/")

    -- Single carrier menu optimization.
    veafCarrierOperations2.airbossCarrierObject:SetMenuSingleCarrier()

    -- Skipper menu.
    if veafCarrierOperations2.carrier.training then
        veafCarrierOperations2.airbossCarrierObject:SetMenuRecovery()
    end    
    veafCarrierOperations2.airbossCarrierObject:SetMenuSmokeZones(veafCarrierOperations2.carrier.training or false)
    veafCarrierOperations2.airbossCarrierObject:SetMenuMarkZones(veafCarrierOperations2.carrier.training or false)
  
    -- Remove landed AI planes from flight deck.
    veafCarrierOperations2.airbossCarrierObject:SetDespawnOnEngineShutdown()

    -- Set path or default.
    local path=""
    if lfs then
        path= lfs.writedir() .. "\\airboss"
    end


    -- Load all saved player grades from your "Saved Games\DCS\Airboss" folder (if lfs was desanitized).
    veafCarrierOperations2.airbossCarrierObject:Load(path)

    -- Automatically save player results to your "Saved Games\DCS" folder each time a player get a final grade from the LSO.
    veafCarrierOperations2.airbossCarrierObject:SetAutoSave(path)

    -- Enable trap sheet.
    veafCarrierOperations2.airbossCarrierObject:SetTrapSheet(path)

    -- Repeater for radio transmissions
    veafCarrierOperations2.airbossCarrierObject:SetRadioRelayLSO(veafCarrierOperations2.carrier.repeaterLso)
    veafCarrierOperations2.airbossCarrierObject:SetRadioRelayMarshal(veafCarrierOperations2.carrier.repeaterMarshal)

    -- S-3B Recovery Tanker spawning in air.
    local tanker=RECOVERYTANKER:New(veafCarrierOperations2.carrier.carrierName, veafCarrierOperations2.carrier.tankerName)
    tanker:SetTakeoffAir()
    tanker:SetRadio(veafCarrierOperations2.carrier.tankerFreq)
    tanker:SetModex(veafCarrierOperations2.carrier.tankerModex)
    tanker:SetTACAN(veafCarrierOperations2.carrier.tankerTacanChannel, veafCarrierOperations2.carrier.tankerTacanMorse)
    tanker:__Start(1)

    --- Function called when recovery tanker is started.
    function tanker:OnAfterStart(From,Event,To)
        
        -- Set recovery tanker.
        veafCarrierOperations2.airbossCarrierObject:SetRecoveryTanker(tanker)  
    end

    -- Rescue Helo with home base Lake Erie. Has to be a global object!
    rescuehelo=RESCUEHELO:New(veafCarrierOperations2.carrier.carrierName, veafCarrierOperations2.carrier.pedroName)
    rescuehelo:SetHomeBase(AIRBASE:FindByName(veafCarrierOperations2.carrier.pedroBase))
    rescuehelo:SetModex(veafCarrierOperations2.carrier.pedroModex)
    rescuehelo:__Start(1)

    --- Function called when a player gets graded by the LSO.
    function veafCarrierOperations2.airbossCarrierObject:OnAfterLSOGrade(From, Event, To, playerData, grade)
        local PlayerData=playerData --Ops.Airboss#AIRBOSS.PlayerData
        local Grade=grade --Ops.Airboss#AIRBOSS.LSOgrade
        
        
        local score=tonumber(Grade.points)
        local name=tostring(PlayerData.name)
        
        -- Report LSO grade to dcs.log file.
        env.info(string.format("Player %s scored %.1f", name, score))
    end

    -- Start airboss class.
    veafCarrierOperations2.airbossCarrierObject:Start()

end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- initialisation
-------------------------------------------------------------------------------------------------------------------------------------------------------------
function veafCarrierOperations2.setCarrierInfo(name, lsoFreq, marshallFreq)
    veafCarrierOperations2.carrier.carrierName = name
    veafCarrierOperations2.carrier.lsoFreq = lsoFreq
    veafCarrierOperations2.carrier.marshallFreq = marshallFreq
end

function veafCarrierOperations2.setTankerInfo(name, freq, tacanChannel, tacanMorse, modex)
    veafCarrierOperations2.carrier.tankerName = name
    veafCarrierOperations2.carrier.tankerFreq = freq
    veafCarrierOperations2.carrier.tankerTacanChannel = tacanChannel
    veafCarrierOperations2.carrier.tankerTacanMorse = tacanMorse
    veafCarrierOperations2.carrier.tankerModex = modex
end

function veafCarrierOperations2.setPedroInfo(name, base, modex)
    veafCarrierOperations2.carrier.pedroName = name
    veafCarrierOperations2.carrier.pedroBase = base
    veafCarrierOperations2.carrier.pedroModex = modex
end

function veafCarrierOperations2.setRepeaterInfo(lso, marshal)
    veafCarrierOperations2.carrier.repeaterLso = lso
    veafCarrierOperations2.carrier.repeaterMarshal = marshal
end

function veafCarrierOperations2.setTraining()
    veafCarrierOperations2.carrier.training = true
end

function veafCarrierOperations2.addRecoveryWindows()
    -- Add recovery windows 
    local duration = 30 * 60 -- every 30 minutes
    for seconds = env.mission.start_time+600, env.mission.start_time + 86400,3600 do 
        local startClock = UTILS.SecondsToClock(seconds)
        local endClock = UTILS.SecondsToClock(seconds+duration)
        local secondsToday = math.fmod(seconds,86400)  -- time mod a full day
        if secondsToday  < 6 * 3600 and secondsToday > 22 * 3600 then            
            -- night = CASE 3
            veafCarrierOperations2.airbossCarrierObject:AddRecoveryWindow( startClock, endClock, 3, 30, true, 21)
        elseif secondsToday < 8 * 3600 and secondsToday > 6 * 3600 then 
            -- dawn = CASE 2
            veafCarrierOperations2.airbossCarrierObject:AddRecoveryWindow( startClock, endClock, 2, 15, true, 23)
        elseif secondsToday < 20 * 3600 and secondsToday > 8 * 3600 then 
            -- day
            veafCarrierOperations2.airbossCarrierObject:AddRecoveryWindow( startClock, endClock, 1, nil, true, 25)
        elseif secondsToday < 22 * 3600 and secondsToday > 20 * 3600 then 
            -- sunset = CASE 2
            veafCarrierOperations2.airbossCarrierObject:AddRecoveryWindow( startClock, endClock, 2, 15, true, 23)
        end
    end
 end
   
function veafCarrierOperations2.initialize(noRadioMenu)
    veafCarrierOperations2.initializeCarrierGroup()
    if not (noRadioMenu or false) then veafCarrierOperations2.buildRadioMenu() end
end

veafCarrierOperations2.logInfo(string.format("Loading version %s", veafCarrierOperations2.Version))

--- Enable/Disable error boxes displayed on screen.
env.setErrorMessageBoxEnabled(false)



