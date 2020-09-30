-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- VEAF cas command and functions for DCS World
-- By zip (2018)
--
-- Features:
-- ---------
-- * Listen to marker change events and creates a CAS training mission, with optional parameters
-- * Possibilities :
-- *    - create a CAS target group, protected by SAM, AAA and manpads, to use for CAS training
-- * Works with all current and future maps (Caucasus, NTTR, Normandy, PG, ...)
--
-- Prerequisite:
-- ------------
-- * This script requires DCS 2.5.1 or higher and MIST 4.3.74 or higher.
-- * It also requires the base veaf.lua script library (version 1.0 or higher)
-- * It also requires the veafMarkers.lua script library (version 1.0 or higher)
-- * It also requires the veafSpawn.lua script library (version 1.0 or higher)
-- * It also requires the dcsUnits.lua script library (version 1.0 or higher)
-- * It also requires the veafUnits.lua script library (version 1.0 or higher)
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
--     * OPEN --> Browse to the location of veafSpawn.lua and click OK.
--     * ACTION "DO SCRIPT FILE"
--     * OPEN --> Browse to the location of this script and click OK.
--     * ACTION "DO SCRIPT"
--     * set the script command to "veafCasMission.initialize()" and click OK.
-- 4.) Save the mission and start it.
-- 5.) Have fun :)
--
-- Basic Usage:
-- ------------
-- 1.) Place a mark on the F10 map.
-- 2.) As text enter "_cas"
-- 3.) Click somewhere else on the map to submit the new text.
-- 4.) The command will be processed. A message will appear to confirm this
-- 5.) The original mark will disappear.
--
-- Options:
-- --------
-- Type "veaf cas mission" to create a default CAS target group
--      add ", defense 0" to completely disable air defenses
--      add ", defense [1-5]" to specify air defense cover (1 = light, 5 = heavy)
--      add ", size [1-5]" to change the group size (1 = small, 5 = huge)
--      add ", armor [1-5]" to specify armor presence (1 = light, 5 = heavy)
--      add ", spacing [1-5]" to change the groups spacing (1 = dense, 3 = default, 5 = sparse)
--
-- *** NOTE ***
-- * All keywords are CaSE inSenSITvE.
-- * Commas are the separators between options ==> They are IMPORTANT!
--
-------------------------------------------------------------------------------------------------------------------------------------------------------------

veafCasMission = {}

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Global settings. Stores the script constants
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Identifier. All output in DCS.log will start with this.
veafCasMission.Id = "CAS MISSION - "

--- Version.
veafCasMission.Version = "1.8.0"

-- trace level, specific to this module
veafCasMission.Trace = false

--- Key phrase to look for in the mark text which triggers the command.
veafCasMission.Keyphrase = "_cas"

--- Number of seconds between each check of the CAS group watchdog function
veafCasMission.SecondsBetweenWatchdogChecks = 15

--- Number of seconds between each smoke request on the CAS targets group
veafCasMission.SecondsBetweenSmokeRequests = 180

--- Number of seconds between each flare request on the CAS targets group
veafCasMission.SecondsBetweenFlareRequests = 120

--- Name of the CAS targets vehicles group 
veafCasMission.RedCasGroupName = "Red CAS Group"

veafCasMission.RadioMenuName = "CAS MISSION"

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Do not change anything below unless you know what you are doing!
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Radio menus paths
veafCasMission.targetMarkersPath = nil
veafCasMission.targetInfoPath = nil
veafCasMission.rootPath = nil

-- CAS Group watchdog function id
veafCasMission.groupAliveCheckTaskID = 'none'

-- Smoke reset function id
veafCasMission.smokeResetTaskID = 'none'

-- Flare reset function id
veafCasMission.flareResetTaskID = 'none'

veafCasMission.SIDE_RED = 1
veafCasMission.SIDE_BLUE = 2

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Utility methods
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafCasMission.logError(message)
    veaf.logError(veafCasMission.Id .. message)
end

function veafCasMission.logInfo(message)
    veaf.logInfo(veafCasMission.Id .. message)
end

function veafCasMission.logDebug(message)
    veaf.logDebug(veafCasMission.Id .. message)
end

function veafCasMission.logTrace(message)
    if message and veafCasMission.Trace then
        veaf.logTrace(veafCasMission.Id .. message)
    end
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Event handler functions.
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Function executed when a mark has changed. This happens when text is entered or changed.
function veafCasMission.onEventMarkChange(eventPos, event)
    -- choose by default the coalition of the player who triggered the event
    local coalition = event.coalition
    veafCasMission.logTrace(string.format("coalition=%d", coalition))

    if veafCasMission.executeCommand(eventPos, event.text, coalition) then        
        -- Delete old mark.
        veafCasMission.logTrace(string.format("Removing mark # %d.", event.idx))
        trigger.action.removeMark(event.idx)
    end
end

function veafCasMission.executeCommand(eventPos, eventText, eventCoalition, bypassSecurity)
    -- Check if marker has a text and the veafCasMission.keyphrase keyphrase.
    if eventText ~= nil and eventText:lower():find(veafCasMission.Keyphrase) then

        -- Analyse the mark point text and extract the keywords.
        local options = veafCasMission.markTextAnalysis(eventText, eventCoalition)

        if options then
            -- Check options commands
            if options.casmission then

                if not options.side then
                    if eventCoalition == 1 then
                        options.side = 2
                    else
                        options.side = 1
                    end
                end

                -- create the group
                veafCasMission.generateCasMission(eventPos, options.size, options.defense, options.armor, options.spacing, options.disperseOnAttack, options.side)
                return true
            end
        end
    end
    return false
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Analyse the mark text and extract keywords.
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Extract keywords from mark text.
function veafCasMission.markTextAnalysis(text)

    -- Option parameters extracted from the mark text.
    local switch = {}
    switch.casmission = false

    -- size ; ranges from 1 to 5, 5 being the biggest.
    switch.size = 1

    -- defenses force ; ranges from 1 to 5, 5 being the toughest.
    switch.defense = 1

    -- armor force ; ranges from 1 to 5, 5 being the strongest and most modern.
    switch.armor = 1

    -- spacing ; ranges from 1 to 5, 1 being the default and 5 being the widest spacing.
    switch.spacing = 1

    -- disperse on attack ; self explanatory, if keyword is present the option will be set to true
    switch.disperseOnAttack = false

    -- password
    switch.password = nil

    -- coalition
    switch.side = nil

    -- Check for correct keywords.
    if text:lower():find(veafCasMission.Keyphrase) then
        switch.casmission = true
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

        if key:lower() == "password" then
            -- Unlock the command
            veafSpawn.logDebug(string.format("Keyword password", val))
            switch.password = val
        end

        if switch.casmission and key:lower() == "size" then
            -- Set size.
            veafCasMission.logDebug(string.format("Keyword size = %d", val))
            local nVal = tonumber(val)
            if nVal <= 5 and nVal >= 1 then
                switch.size = nVal
            end
        end

        if switch.casmission and key:lower() == "defense" then
            -- Set defense.
            veafCasMission.logDebug(string.format("Keyword defense = %d", val))
            local nVal = tonumber(val)
            if nVal <= 5 and nVal >= 0 then
                switch.defense = nVal
            end
        end

        if switch.casmission and key:lower() == "armor" then
            -- Set armor.
            veafCasMission.logDebug(string.format("Keyword armor = %d", val))
            local nVal = tonumber(val)
            if nVal <= 5 and nVal >= 0 then
                switch.armor = nVal
            end
        end

        if switch.casmission and key:lower() == "spacing" then
            -- Set spacing.
            veafCasMission.logDebug(string.format("Keyword spacing = %d", val))
            local nVal = tonumber(val)
            if nVal <= 5 and nVal >= 1 then
                switch.spacing = nVal
            end
        end

        if key:lower() == "side" then
            -- Set side
            veafCasMission.logTrace(string.format("Keyword side = %s", val))
            if val:upper() == "BLUE" then
                switch.side = veafCasMission.SIDE_BLUE
            else
                switch.side = veafCasMission.SIDE_RED
            end
        end

        if switch.casmission and key:lower() == "disperse" then
            -- Set disperse on attack.
            veafCasMission.logDebug("Keyword disperse is set")
            switch.disperseOnAttack = true
        end

    end

    return switch
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- CAS target group generation and management
-------------------------------------------------------------------------------------------------------------------------------------------------------------

local function _addDefenseForGroups(group, side, defense, multiple)
    veafCasMission.logTrace(string.format("_addDefenseForGroups(defense=[%s], side=[%s], multiple=[%s])", defense  or "", side or "", multiple or ""))
    for _ = 1, multiple do
        if defense > 5 then
            -- defense > 5 : add a SA9/13, a SA8 and a Tunguska (resp. M1097 Avenger and a M6 Linebacker)
            if side == veafCasMission.SIDE_BLUE then
                table.insert(group.units, { "M1097 Avenger", random })
                table.insert(group.units, { "M6 Linebacker", random })
            else
                table.insert(group.units, { veaf.randomlyChooseFrom({"Strela-1 9P31", "Strela-10M3"}), random })
                table.insert(group.units, { "Osa 9A33 ln", random })
                table.insert(group.units, { "2S6 Tunguska", random })
            end
        elseif defense == 5 then
            -- defense = 5 : add a SA8 and a Tunguska (resp. M1097 Avenger and a M6 Linebacker)
            if side == veafCasMission.SIDE_BLUE then
                table.insert(group.units, { "M1097 Avenger", random })
                table.insert(group.units, { "M6 Linebacker", random })
            else
                table.insert(group.units, { "Osa 9A33 ln", random })
                table.insert(group.units, { "2S6 Tunguska", random })
            end
        elseif defense == 4 then
            -- defense = 4 : add a Shilka and a Tunguska (resp. Gepard and a M6 Linebacker)
            if side == veafCasMission.SIDE_BLUE then
                table.insert(group.units, { "Gepard", random })
                table.insert(group.units, { "M6 Linebacker", random })
            else
                table.insert(group.units, { "ZSU-23-4 Shilka", random })
                table.insert(group.units, { "2S6 Tunguska", random })
            end
        elseif defense == 3 then
            -- defense = 3 : add a SA9/SA13 (resp. a M6 Linebacker)
            if side == veafCasMission.SIDE_BLUE then
                table.insert(group.units, { "M6 Linebacker", random })
            else
                table.insert(group.units, { veaf.randomlyChooseFrom({"Strela-1 9P31", "Strela-10M3"}), random })
            end
        elseif defense == 2 then
            -- defense = 2 : add a Shilka (resp. a Gepard)
            if side == veafCasMission.SIDE_BLUE then
                table.insert(group.units, { "Gepard", random })
            else
                table.insert(group.units, { "ZSU-23-4 Shilka", random })
            end
        elseif defense == 1 then
            -- defense = 1 : add a ZU23 on a truck (resp. a Vulcan)
            if side == veafCasMission.SIDE_BLUE then
                table.insert(group.units, { "Vulcan", random })
            else
                table.insert(group.units, { "Ural-375 ZU-23", random })
            end
        end
    end
    --veafCasMission.logTrace(string.format("group.units=%s", veaf.p(group.units)))
end

--- Generates an air defense group
function veafCasMission.generateAirDefenseGroup(groupName, defense, side)
    side = side or veafCasMission.SIDE_RED
    
    -- generate a primary air defense platoon
    local _actualDefense = defense
    if defense > 0 then
        -- roll a dice : 20% chance to get a -1 (lower) difficulty, 30% chance to get a +1 (higher) difficulty, and 50% to get what was asked for
        local _dice = math.random(100)
        veafCasMission.logTrace("_dice = " .. _dice)
        if _dice <= 20 then
            _actualDefense = defense - 1
        elseif _dice > 80 then
            _actualDefense = defense + 1
        end
    end
    if _actualDefense > 5 then _actualDefense = 5 end
    if _actualDefense < 0 then _actualDefense = 0 end
    veafCasMission.logTrace("_actualDefense = " .. _actualDefense)
    local _groupDefinition = "generateAirDefenseGroup-BLUE-"
    if side == veafCasMission.SIDE_RED then
        _groupDefinition = "generateAirDefenseGroup-RED-"
    end
    _groupDefinition = _groupDefinition .. tostring(_actualDefense)
    veafCasMission.logTrace("_groupDefinition = " .. _groupDefinition)

    group = veafUnits.findGroup(_groupDefinition)
    if not group then
        veafCasMission.logError(string.format("veafCasMission.generateAirDefenseGroup cannot find group [%s]", _groupDefinition or ""))
    end
    group.description = groupName
    group.groupName = groupName
    
    veafCasMission.logTrace("#group.units = " .. #group.units)
    return group
end

--- Generates a transport company and its air defenses
function veafCasMission.generateTransportCompany(groupName, defense, side, size)
    veafCasMission.logTrace(string.format("veafCasMission.generateTransportCompany(groupName=[%s], defense=[%s], side=[%s], size=[%s])", groupName or "", defense  or "", side or "", size or ""))
    side = side or veafCasMission.SIDE_RED
    local groupCount = math.floor((size or math.random(10, 15)))
    veafCasMission.logTrace(string.format("groupCount=%s", tostring(groupCount)))
    local group = {
            disposition = { h = groupCount, w = groupCount},
            units = {},
            description = groupName,
            groupName = groupName,
        }
    -- generate a transport company
    local transportType
  
    for _ = 1, groupCount do
        if veaf.config.ww2 then
            if side == veafCasMission.SIDE_BLUE then
                transportType = veaf.randomlyChooseFrom({"Bedford_MWD", "CCKW_353", "Willys_MB"})
            else
                transportType = veaf.randomlyChooseFrom({"Blitz_36-6700A", "Horch_901_typ_40_kfz_21", "Kubelwagen_82", "Sd_Kfz_7", "Sd_Kfz_2" })
            end
        else
            if side == veafCasMission.SIDE_BLUE then
                transportType = veaf.randomlyChooseFrom({"APC M1025 HMMWV", "Transport M818", "HEMTT TFFT", "M978 HEMTT Tanker"})
            else
                transportType = veaf.randomlyChooseFrom({'ATMZ-5', 'Ural-4320 APA-5D', 'SKP-11', 'GAZ-66', 'KAMAZ Truck', 'Ural-375', 'Ural-4320T', 'ZIL-131 KUNG' })
            end
        end
        table.insert(group.units, { transportType, random})
    end

    -- add an air defense vehicle every 10 vehicles
    local nbDefense = groupCount / 10 + 1
    if nbDefense == 0 then
        nbDefense = 1
    end
    veafCasMission.logDebug("nbDefense = " .. nbDefense)
    if not veaf.config.ww2 then
        _addDefenseForGroups(group, side, defense, nbDefense)
    else
        -- nothing, there are no mobile defense units in WW2
    end

    return group
end

--- Generates an armor platoon and its air defenses
function veafCasMission.generateArmorPlatoon(groupName, defense, armor, side, size)
    veafCasMission.logTrace(string.format("veafCasMission.generateArmorPlatoon(groupName=[%s], defense=[%s], armor=[%s], side=[%s], size=[%s])", groupName or "", defense  or "", armor or "", side or "", size or ""))
    side = side or veafCasMission.SIDE_RED
    
    -- generate an armor platoon
    local groupCount = math.floor((size or math.random(3, 6)) * (math.random(8, 12)/10))
    veafCasMission.logTrace(string.format("groupCount=%s", tostring(groupCount)))
    local group = {
            disposition = { h = groupCount, w = groupCount},
            units = {},
            description = groupName,
            groupName = groupName,
        }
    if group.disposition.h < 4 then 
        group.disposition.h = 4
        group.disposition.w = 4
    end
    local armorType
    local armorRand
    for _ = 1, groupCount do
        if armor <= 2 then
            if veaf.config.ww2 then
                if side == veafCasMission.SIDE_BLUE then
                    armorType = veaf.randomlyChooseFrom({"M30_CC", "M10_GMC"})
                else
                    armorType = veaf.randomlyChooseFrom({"Sd_Kfz_251", "Sd_Kfz_234_2_Puma"})
                end
            else
                if side == veafCasMission.SIDE_BLUE then
                    armorType = veaf.randomlyChooseFrom({'IFV Marder', 'IFV MCV-80', 'IFV LAV-25', 'M-2 Bradley'})
                else
                    armorType = veaf.randomlyChooseFrom({'BRDM-2', 'BMD-1', 'BMP-1'})
                end
            end
        elseif armor == 3 then
            if veaf.config.ww2 then
                if side == veafCasMission.SIDE_BLUE then
                    armorType = veaf.randomlyChooseFrom({"M30_CC", "M10_GMC", "Centaur_IV",})
                else
                    armorType = veaf.randomlyChooseFrom({"Sd_Kfz_251", "Sd_Kfz_234_2_Puma", "Elefant_SdKfz_184"})
                end
            else
                if side == veafCasMission.SIDE_BLUE then
                    armorType = veaf.randomlyChooseFrom({'M-2 Bradley', 'M-2 Bradley', 'M-60'})
                else
                    armorType = veaf.randomlyChooseFrom({'BMP-1', 'BMP-2', 'T-55'})
                end
            end
        elseif armor == 4 then
            if veaf.config.ww2 then
                if side == veafCasMission.SIDE_BLUE then
                    armorType = veaf.randomlyChooseFrom({"Centaur_IV", "Churchill_VII", "Cromwell_IV"})
                else
                    armorType = veaf.randomlyChooseFrom({"Pz_IV_H", "Tiger_I", "Tiger_II_H","Stug_III","Stug_IV"})
                end
            else
                if side == veafCasMission.SIDE_BLUE then
                    armorType = veaf.randomlyChooseFrom({'M-2 Bradley', 'M-2 Bradley', 'M-60', 'MBT Leopard 1A3'})
                else
                    armorType = veaf.randomlyChooseFrom({'BMP-1', 'BMP-2', 'T-55', 'T-72B'})
                end
            end
        elseif armor >= 5 then
            if veaf.config.ww2 then
                if side == veafCasMission.SIDE_BLUE then
                    armorType = veaf.randomlyChooseFrom({"Centaur_IV", "Churchill_VII", "Cromwell_IV", "M4_Sherman", "M4A4_Sherman_FF"}, armor-5)
                else
                    armorType = veaf.randomlyChooseFrom({"Pz_IV_H", "Tiger_I", "Tiger_II_H","Stug_III","Stug_IV", "JagdPz_IV", "Jagdpanther_G1", "Pz_V_Panther_G"}, armor-5)
                end
            else
                if side == veafCasMission.SIDE_BLUE then
                    armorType = veaf.randomlyChooseFrom({'M-2 Bradley', 'M-2 Bradley', 'MBT Leopard 1A3', 'M-1 Abrams'}, armor-5)
                else
                    armorType = veaf.randomlyChooseFrom({'BMP-2', 'BMP-3', 'T-72B', 'T-80UD', 'T-90'}, armor-5)
                end
            end
        end
        table.insert(group.units, { armorType, random })
    end

    -- add air defense vehicles
    if not veaf.config.ww2 then
        _addDefenseForGroups(group, side, defense, 1)
    else
        -- nothing, there are no mobile defense units in WW2
    end

    return group
end

--- Generates an infantry group along with its manpad units and tranport vehicles
function veafCasMission.generateInfantryGroup(groupName, defense, armor, side, size)
    side = side or veafCasMission.SIDE_RED
    veafCasMission.logTrace(string.format("veafCasMission.generateInfantryGroup(groupName=%s, defense=%d, armor=%d)",groupName, defense, armor))
    -- generate an infantry group
    local groupCount = math.floor((size or math.random(3, 6)) * (math.random(8, 12)/10))
    veafCasMission.logTrace(string.format("groupCount=%s", tostring(groupCount)))
    local group = {
            disposition = { h = groupCount, w = groupCount},
            units = {},
            description = groupName,
            groupName = groupName,
        }
    if group.disposition.h < 4 then 
        group.disposition.h = 4
        group.disposition.w = 4
    end
    for _ = 1, groupCount do
        local rand = math.random(3)
        local unitType = nil
        if rand == 1 then
            if side == veafCasMission.SIDE_BLUE then
                unitType = 'Soldier M249'
            else
                unitType = 'Soldier RPG'
            end
        elseif rand == 2 then
            if side == veafCasMission.SIDE_BLUE then
                unitType = 'Soldier M4'
            else
                unitType = 'Paratrooper AKS-74'
            end
        else
            if side == veafCasMission.SIDE_BLUE then
                unitType = 'Soldier M4'
            else
                unitType = 'Soldier AK'
            end
        end
        table.insert(group.units, { unitType })
    end

    -- add a transport vehicle or an APC/IFV
    if armor > 3 then
        if side == veafCasMission.SIDE_BLUE then
            table.insert(group.units, { "M-2 Bradley", cell=11, random })
        else
            table.insert(group.units, { "BMP-1", cell=11, random })
        end
    elseif armor > 0 then
        if side == veafCasMission.SIDE_BLUE then
            table.insert(group.units, { "IFV Marder", cell=11, random })
        else
            table.insert(group.units, { "BTR-80", cell=11, random })
        end
    else
        if side == veafCasMission.SIDE_BLUE then
            table.insert(group.units, { "M 818", cell=11, random })
        else
            table.insert(group.units, { "GAZ-3308", cell=11, random })
        end
    end

    -- add manpads if needed
    if defense > 3 then
        for _ = 1, math.random(1,defense-2) do
            -- for defense = 4-5, spawn a modern Igla-S team
            if side == veafCasMission.SIDE_BLUE then
                table.insert(group.units, { "Stinger comm", random })
                table.insert(group.units, { "Soldier stinger", random })
            else
                table.insert(group.units, { "SA-18 Igla-S comm", random })
                table.insert(group.units, { "SA-18 Igla-S manpad", random })
            end
        end
    elseif defense > 0 then
        for _ = 1, math.random(1,defense) do
            -- for defense = 1-3, spawn an older Igla team
            if side == veafCasMission.SIDE_BLUE then
                table.insert(group.units, { "Stinger comm", random })
                table.insert(group.units, { "Soldier stinger", random })
            else
                table.insert(group.units, { "SA-18 Igla comm", random })
                table.insert(group.units, { "SA-18 Igla manpad", random })
            end
        end
    else
        -- for defense = 0, don't spawn any manpad
    end

    return group
end

function veafCasMission.placeGroup(groupDefinition, spawnPosition, spacing, resultTable)
    if spawnPosition ~= nil and groupDefinition ~= nil then
        veafCasMission.logTrace(string.format("veafCasMission.placeGroup(#groupDefinition.units=%d)",#groupDefinition.units))

        -- process the group 
        veafCasMission.logTrace("process the group")
        local group = veafUnits.processGroup(groupDefinition)
        
        -- place its units
        groupPosition = { x = spawnPosition.x, z = spawnPosition.y }
        local hdg = math.random(359)
        local group, cells = veafUnits.placeGroup(group, veaf.placePointOnLand(groupPosition), spacing+3, hdg)
        if veaf.Trace then 
            veafUnits.traceGroup(group, cells)
        end
        
        -- add the units to the result units list
        if not resultTable then 
            resultTable = {}
        end
        for _,u in pairs(group.units) do
            table.insert(resultTable, u)
        end
    end
    veafCasMission.logTrace(string.format("#resultTable=%d",#resultTable))
    return resultTable
end

--- Generates a complete CAS target group
function veafCasMission.generateCasGroup(country, casGroupName, spawnSpot, size, defense, armor, spacing, disperseOnAttack, side)
    veafCasMission.logTrace("side = " .. tostring(side))
    side = side or veafCasMission.SIDE_RED
    local units = {}
    local groupId = 1234 + math.random(1000)
    local zoneRadius = (size+spacing)*350
    veafCasMission.logTrace("zoneRadius = " .. zoneRadius)
    
    -- generate between size-2 and size+1 infantry groups
    local infantryGroupsCount = math.random(math.max(1, size-2), size + 1)
    veafCasMission.logTrace("infantryGroupsCount = " .. infantryGroupsCount)
    for infantryGroupNumber = 1, infantryGroupsCount do
        local groupName = casGroupName .. " - Infantry Section " .. infantryGroupNumber
        local group = veafCasMission.generateInfantryGroup(groupName, defense, armor, side)
        local groupPosition = veaf.findPointInZone(spawnSpot, zoneRadius, false)
        veafCasMission.placeGroup(group, groupPosition, spacing, units)
    end

    if armor > 0 then
        -- generate between size-2 and size+1 armor platoons
        local armorPlatoonsCount = math.random(math.max(1, size-2), size + 1)
        veafCasMission.logTrace("armorPlatoonsCount = " .. armorPlatoonsCount)
        for armorGroupNumber = 1, armorPlatoonsCount do
            local groupName = casGroupName .. " - Armor Platoon " .. armorGroupNumber
            local groupPosition = veaf.findPointInZone(spawnSpot, zoneRadius, false)
            local group = veafCasMission.generateArmorPlatoon(groupName, defense, armor, side)
            veafCasMission.placeGroup(group, groupPosition, spacing, units)
        end
    end

    if defense > 0 then
        -- generate between 1 and 2 air defense groups
        local airDefenseGroupsCount = 1
        if defense > 3 then
            airDefenseGroupsCount = 2
        end
        veafCasMission.logTrace("airDefenseGroupsCount = " .. airDefenseGroupsCount)
        for airDefenseGroupNumber = 1, airDefenseGroupsCount do
            local groupName = casGroupName .. " - Air Defense Group ".. airDefenseGroupNumber
            local groupPosition = veaf.findPointInZone(spawnSpot, zoneRadius, false)
            local group = veafCasMission.generateAirDefenseGroup(groupName, defense, side)
            veafCasMission.placeGroup(group, groupPosition, spacing, units)
        end
    end

    -- generate between 1 and size transport companies
    local transportCompaniesCount = math.random(1, size)
    veafCasMission.logTrace("transportCompaniesCount = " .. transportCompaniesCount)
    for transportCompanyGroupNumber = 1, transportCompaniesCount do
        local groupName = casGroupName .. " - Transport Company " .. transportCompanyGroupNumber
        local groupPosition = veaf.findPointInZone(spawnSpot, zoneRadius, false)
        local group = veafCasMission.generateTransportCompany(groupName, defense, side)
        veafCasMission.placeGroup(group, groupPosition, spacing, units)
    end

    return units
end

--- Generates a CAS mission
function veafCasMission.generateCasMission(spawnSpot, size, defense, armor, spacing, disperseOnAttack, side)
    if veafCasMission.groupAliveCheckTaskID ~= 'none' then
        trigger.action.outText("A CAS target group already exists !", 5)
        return
    end
    local country = veaf.getCountryForCoalition(side)
    local units = veafCasMission.generateCasGroup(country, veafCasMission.RedCasGroupName, spawnSpot, size, defense, armor, spacing, disperseOnAttack, side)

    -- prepare the actual DCS units
    local dcsUnits = {}
    for i=1, #units do
        local unit = units[i]
        local unitType = unit.typeName
        local unitName = veafCasMission.RedCasGroupName .. " / " .. unit.displayName .. " #" .. i
        
        local spawnPosition = unit.spawnPoint
        
        -- check if position is correct for the unit type
        if veafUnits.checkPositionForUnit(spawnPosition, unit) then
            local toInsert = {
                    ["x"] = spawnPosition.x,
                    ["y"] = spawnPosition.z,
                    ["alt"] = spawnPosition.y,
                    ["type"] = unitType,
                    ["name"] = unitName,
                    ["speed"] = 0,
                    ["skill"] = "Random",
                    ["heading"] = 0
            }
            table.insert(dcsUnits, toInsert)
        end
    end

    -- actually spawn groups
    mist.dynAdd({country = country, category = "GROUND_UNIT", name = veafCasMission.RedCasGroupName, hidden = false, units = dcsUnits})

    -- set AI options
    local controller = Group.getByName(veafCasMission.RedCasGroupName):getController()
    controller:setOption(9, 2) -- set alarm state to red
    controller:setOption(AI.Option.Ground.id.DISPERSE_ON_ATTACK, disperseOnAttack) -- set disperse on attack according to the option

    -- Move reaper
    -- TODO

    -- build menu for each player
    veafRadio.addCommandToSubmenu('Target information', veafCasMission.rootPath, veafCasMission.reportTargetInformation, nil, veafRadio.USAGE_ForGroup)

    -- add radio menus for commands
    veafRadio.addSecuredCommandToSubmenu('Skip current objective', veafCasMission.rootPath, veafCasMission.skipCasTarget)
    veafCasMission.targetMarkersPath = veafRadio.addSubMenu("Target markers", veafCasMission.rootPath)
    veafRadio.addCommandToSubmenu('Request smoke on target area', veafCasMission.targetMarkersPath, veafCasMission.smokeCasTargetGroup)
    veafRadio.addCommandToSubmenu('Request illumination flare over target area', veafCasMission.targetMarkersPath, veafCasMission.flareCasTargetGroup)

    local nbVehicles, nbInfantry = veafUnits.countInfantryAndVehicles(veafCasMission.RedCasGroupName)
    local message =      "TARGET: Group of " .. nbVehicles .. " vehicles and " .. nbInfantry .. " soldiers. See F10 radio menu for details\n"
    trigger.action.outText(message,5)

    veafRadio.refreshRadioMenu()

    -- start checking for targets destruction
    veafCasMission.casGroupWatchdog()
end

-- Ask a report
-- @param int groupId
function veafCasMission.reportTargetInformation(unitName)
    -- generate information dispatch
    local nbVehicles, nbInfantry = veafUnits.countInfantryAndVehicles(veafCasMission.RedCasGroupName)

    local message =      "TARGET: Group of " .. nbVehicles .. " vehicles and " .. nbInfantry .. " soldiers.\n"
    message = message .. "\n"

    -- add coordinates and position from bullseye
    local averageGroupPosition = veaf.getAveragePosition(veafCasMission.RedCasGroupName)
    local lat, lon = coord.LOtoLL(averageGroupPosition)
    local mgrsString = mist.tostringMGRS(coord.LLtoMGRS(lat, lon), 3)
    local bullseye = mist.utils.makeVec3(mist.DBs.missionData.bullseye.blue, 0)
    local vec = {x = averageGroupPosition.x - bullseye.x, y = averageGroupPosition.y - bullseye.y, z = averageGroupPosition.z - bullseye.z}
    local dir = mist.utils.round(mist.utils.toDegree(mist.utils.getDir(vec, bullseye)), 0)
    local dist = mist.utils.get2DDist(averageGroupPosition, bullseye)
    local distMetric = mist.utils.round(dist/1000, 0)
    local distImperial = mist.utils.round(mist.utils.metersToNM(dist), 0)
    local fromBullseye = string.format('%03d', dir) .. ' for ' .. distMetric .. 'km /' .. distImperial .. 'nm'

    message = message .. "LAT LON (decimal): " .. mist.tostringLL(lat, lon, 2) .. ".\n"
    message = message .. "LAT LON (DMS)    : " .. mist.tostringLL(lat, lon, 0, true) .. ".\n"
    message = message .. "MGRS/UTM         : " .. mgrsString .. ".\n"
    message = message .. "FROM BULLSEYE    : " .. fromBullseye .. ".\n"
    message = message .. "\n"

    message = message .. veaf.weatherReport(averageGroupPosition, nil, true)

    -- send message only for the unit
    veaf.outTextForUnit(unitName, message, 30)
end

--- add a smoke marker over the target area
function veafCasMission.smokeCasTargetGroup()
    veafCasMission.logTrace("veafCasMission.smokeCasTargetGroup START")
    veafSpawn.spawnSmoke(veaf.getAveragePosition(veafCasMission.RedCasGroupName), trigger.smokeColor.Red)
    trigger.action.outText('Copy smoke requested, RED smoke on the deck!',5)
    veafRadio.delCommand(veafCasMission.targetMarkersPath, 'Request smoke on target area')
    veafRadio.addCommandToSubmenu('Target is marked with red smoke', veafCasMission.targetMarkersPath, veaf.emptyFunction)
    veafCasMission.smokeResetTaskID = mist.scheduleFunction(veafCasMission.smokeReset,{},timer.getTime()+veafCasMission.SecondsBetweenSmokeRequests)
    veafRadio.refreshRadioMenu()
end

--- Reset the smoke request radio menu
function veafCasMission.smokeReset()
    veafRadio.delCommand(veafCasMission.targetMarkersPath, 'Target is marked with red smoke')
    veafRadio.addCommandToSubmenu('Request smoke on target area', veafCasMission.targetMarkersPath, veafCasMission.smokeCasTargetGroup)
    trigger.action.outText('Smoke marker available',5)
    veafRadio.refreshRadioMenu()
end

--- add an illumination flare over the target area
function veafCasMission.flareCasTargetGroup()
    veafSpawn.spawnIlluminationFlare(veaf.getAveragePosition(veafCasMission.RedCasGroupName))
	trigger.action.outText('Copy illumination flare requested, illumination flare over target area!',5)
    veafRadio.delCommand(veafCasMission.targetMarkersPath, 'Request illumination flare over target area')
    veafRadio.addCommandToSubmenu('Target area is marked with illumination flare', veafCasMission.targetMarkersPath, veaf.emptyFunction)
    veafCasMission.flareResetTaskID = mist.scheduleFunction(veafCasMission.flareReset,{},timer.getTime()+veafCasMission.SecondsBetweenFlareRequests)
    veafRadio.refreshRadioMenu()
end

--- Reset the flare request radio menu
function veafCasMission.flareReset()
    veafRadio.delCommand(veafCasMission.targetMarkersPath, 'Target area is marked with illumination flare')
    veafRadio.addCommandToSubmenu('Request illumination flare over target area', veafCasMission.targetMarkersPath, veafCasMission.flareCasTargetGroup)
    trigger.action.outText('Target illumination available',5)
    veafRadio.refreshRadioMenu()
end

--- Checks if the vehicles group is still alive, and if not announces the end of the CAS mission
function veafCasMission.casGroupWatchdog() 
    local nbVehicles, nbInfantry = veafUnits.countInfantryAndVehicles(veafCasMission.RedCasGroupName)
    if nbVehicles > 0 then
        veafCasMission.logTrace("Group is still alive with "..nbVehicles.." vehicles and "..nbInfantry.." soldiers")
        veafCasMission.groupAliveCheckTaskID = mist.scheduleFunction(veafCasMission.casGroupWatchdog,{},timer.getTime()+veafCasMission.SecondsBetweenWatchdogChecks)
    else
        trigger.action.outText("CAS objective group destroyed!", 5)
        veafCasMission.cleanupAfterMission()
    end
end

--- Called from the "Skip target" radio menu : remove the current CAS target group
function veafCasMission.skipCasTarget()
    veafCasMission.cleanupAfterMission()
    trigger.action.outText("CAS objective group cleaned up.", 5)
end

--- Cleanup after either mission is ended or aborted
function veafCasMission.cleanupAfterMission()
    veafCasMission.logTrace("skipCasTarget START")

    -- destroy vehicles and infantry groups
    veafCasMission.logTrace("destroy vehicles group")
    local group = Group.getByName(veafCasMission.RedCasGroupName)
    if group and group:isExist() == true then
        group:destroy()
    end
    veafCasMission.logTrace("destroy infantry group")
    group = Group.getByName(veafCasMission.RedCasGroupName)
    if group and group:isExist() == true then
        group:destroy()
    end

    -- remove the watchdog function
    veafCasMission.logTrace("remove the watchdog function")
    if veafCasMission.groupAliveCheckTaskID ~= 'none' then
        mist.removeFunction(veafCasMission.groupAliveCheckTaskID)
    end
    veafCasMission.groupAliveCheckTaskID = 'none'

    
    veafCasMission.logTrace("update the radio menu 1")
    veafRadio.delCommand(veafCasMission.rootPath, 'Target information')

    veafCasMission.logTrace("update the radio menu 2")
    veafRadio.delCommand(veafCasMission.rootPath, 'Skip current objective')
    veafCasMission.logTrace("update the radio menu 3")
    veafRadio.delCommand(veafCasMission.rootPath, 'Get current objective situation')
    veafCasMission.logTrace("update the radio menu 4")
    veafRadio.delSubmenu(veafCasMission.targetMarkersPath, veafCasMission.rootPath)

    veafRadio.refreshRadioMenu()
    veafCasMission.logTrace("skipCasTarget DONE")

end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Radio menu and help
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Build the initial radio menu
function veafCasMission.buildRadioMenu()
    veafCasMission.rootPath = veafRadio.addSubMenu(veafCasMission.RadioMenuName)
    if not(veafRadio.skipHelpMenus) then
        veafRadio.addCommandToSubmenu("HELP", veafCasMission.rootPath, veafCasMission.help, nil, veafRadio.USAGE_ForGroup)
    end
end

function veafCasMission.help(unitName)
    local text =
        'Create a marker and type "_cas" in the text\n' ..
        'This will create a default CAS target group\n' ..
        'You can add options (comma separated) :\n' ..
        '   "defense 0" completely disables air defenses\n' ..
        '   "defense [1-5]" specifies air defense cover (1 = light, 5 = heavy)\n' ..
        '   "size [1-5]" changes the group size (1 = small, 5 = huge)\n' ..
        '   "armor [1-5]" specifies armor presence (1 = light, 5 = heavy)\n' ..
        '   "spacing [1-5]" changes the groups spacing (1 = dense, 3 = default, 5 = sparse)'

    veaf.outTextForUnit(unitName, text, 30)
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- initialisation
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafCasMission.initialize()
    veafCasMission.buildRadioMenu()
    veafMarkers.registerEventHandler(veafMarkers.MarkerChange, veafCasMission.onEventMarkChange)
end

veafCasMission.logInfo(string.format("Loading version %s", veafCasMission.Version))

--- Enable/Disable error boxes displayed on screen.
env.setErrorMessageBoxEnabled(false)



