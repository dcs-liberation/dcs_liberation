-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- VEAF carrier command and functions for DCS World
-- By zip (2018)
--
-- Features:
-- ---------
-- * Radio menus allow starting and ending carrier operations. Carriers go back to their initial point when operations are ended
-- * Works with all current and future maps (Caucasus, NTTR, Normandy, PG, ...)
--
-- Prerequisite:
-- ------------
-- * This script requires DCS 2.5.1 or higher and MIST 4.3.74 or higher.
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
--     * OPEN --> Browse to the location of veaf.lua and click OK.
--     * ACTION "DO SCRIPT FILE"
--     * OPEN --> Browse to the location of veafRadio.lua and click OK.
--     * ACTION "DO SCRIPT FILE"
--     * OPEN --> Browse to the location of this script and click OK.
--     * ACTION "DO SCRIPT"
--     * set the script command to "veafRadio.initialize();veafCarrierOperations.initialize()" and click OK.
-- 4.) Save the mission and start it.
-- 5.) Have fun :)
--
-- Basic Usage:
-- ------------
-- Use the F10 radio menu to start and end carrier operations for every detected carrier group (having a group name like "CSG-*")
--
-------------------------------------------------------------------------------------------------------------------------------------------------------------

veafCarrierOperations = {}

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Global settings. Stores the script constants
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Identifier. All output in DCS.log will start with this.
veafCarrierOperations.Id = "CARRIER - "

--- Version.
veafCarrierOperations.Version = "1.5.0"

-- trace level, specific to this module
veafCarrierOperations.Trace = false

--- All the carrier groups must comply with this name
veafCarrierOperations.CarrierGroupNamePattern = "^CSG-.*$"

veafCarrierOperations.RadioMenuName = "CARRIER OPS"

veafCarrierOperations.AllCarriers = 
{
    ["LHA_Tarawa"] = { runwayAngleWithBRC = 0, desiredWindSpeedOnDeck = 20},
    ["Stennis"] = { runwayAngleWithBRC = 9.05, desiredWindSpeedOnDeck = 25},
    ["CVN_71"] = { runwayAngleWithBRC = 9.05, desiredWindSpeedOnDeck = 25},
    ["KUZNECOW"] ={ runwayAngleWithBRC = 0, desiredWindSpeedOnDeck = 25}
}

veafCarrierOperations.ALT_FOR_MEASURING_WIND = 30 -- wind is measured at 30 meters, 10 meters above deck
veafCarrierOperations.ALIGNMENT_MANOEUVER_SPEED = 8 -- carrier speed when not yet aligned to the wind (in m/s)
veafCarrierOperations.MAX_OPERATIONS_DURATION = 45 -- operations are stopped after
veafCarrierOperations.SCHEDULER_INTERVAL = 2 -- scheduler runs every 2 minutes

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Do not change anything below unless you know what you are doing!
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Radio menus paths
veafCarrierOperations.rootPath = nil

--- Carrier groups data, for Carrier Operations commands
veafCarrierOperations.carriers = {}

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Utility methods
-------------------------------------------------------------------------------------------------------------------------------------------------------------
veafCarrierOperations.debugMarkersErasedAtEachStep = {}
veafCarrierOperations.debugMarkersForTanker = {}
veafCarrierOperations.traceMarkerId = 2727

function veafCarrierOperations.logError(message)
    veaf.logError(veafCarrierOperations.Id .. message)
end

function veafCarrierOperations.logInfo(message)
    veaf.logInfo(veafCarrierOperations.Id .. message)
end

function veafCarrierOperations.logDebug(message)
    veaf.logDebug(veafCarrierOperations.Id .. message)
end

function veafCarrierOperations.logTrace(message)
    if message and veafCarrierOperations.Trace then 
        veaf.logTrace(veafCarrierOperations.Id .. message)
    end
end

function veafCarrierOperations.logMarker(id, message, position, markersTable)
    if veafCarrierOperations.Trace then 
        return veaf.logMarker(id, veafCarrierOperations.Id, message, position, markersTable)
    end
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Carrier operations commands
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Start carrier operations ; changes the radio menu item to END and make the carrier move
function veafCarrierOperations.startCarrierOperations(parameters)
    local groupName, duration = veaf.safeUnpack(parameters)
    veafCarrierOperations.logDebug("startCarrierOperations(".. groupName .. ")")

    local carrier = veafCarrierOperations.carriers[groupName]

    if not(carrier) then
        local text = "Cannot find the carrier group "..groupName
        veafCarrierOperations.logError(text)
        trigger.action.outText(text, 5)
        return
    end

    -- find the actual carrier unit
    local group = Group.getByName(groupName)
    for _, unit in pairs(group:getUnits()) do
        local unitType = unit:getDesc()["typeName"]
        for knownCarrierType, data in pairs(veafCarrierOperations.AllCarriers) do
            if unitType == knownCarrierType then
                carrier.carrierUnitName = unit:getName()
                carrier.pedroUnitName = carrier.carrierUnitName .. " Pedro" -- rescue helo unit name
                carrier.tankerUnitName = carrier.carrierUnitName .. " S3B-Tanker" -- emergency tanker unit name
                carrier.tankerRouteSet = 0
                carrier.runwayAngleWithBRC = data.runwayAngleWithBRC
                carrier.desiredWindSpeedOnDeck = data.desiredWindSpeedOnDeck
                carrier.initialPosition = unit:getPosition().p
                veafCarrierOperations.logTrace("initialPosition="..veaf.vecToString(carrier.initialPosition))
                break
            end
        end
    end
    
    carrier.conductingAirOperations = true
    carrier.airOperationsStartedAt = timer.getTime()
    carrier.airOperationsEndAt = carrier.airOperationsStartedAt + duration * 60

    veafCarrierOperations.continueCarrierOperations(groupName) -- will update the *carrier* structure

    
    local text = 
        veafCarrierOperations.getAtcForCarrierOperations(groupName) ..
        "\nGetting a good alignment may require up to 5 minutes"

    veafCarrierOperations.logInfo(text)    
    trigger.action.outText(text, 25)
    
    -- change the menu
    veafCarrierOperations.logTrace("change the menu")
    veafCarrierOperations.rebuildRadioMenu()

end

--- Continue carrier operations ; make the carrier move according to the wind. Called by startCarrierOperations and by the scheduler.
function veafCarrierOperations.continueCarrierOperations(groupName)
    veafCarrierOperations.logDebug("continueCarrierOperations(".. groupName .. ")")

    local carrier = veafCarrierOperations.carriers[groupName]

    if not(carrier) then
        local text = "Cannot find the carrier group "..groupName
        veafCarrierOperations.logError(text)
        trigger.action.outText(text, 5)
        return
    end

    -- find the actual carrier unit
    local carrierUnit = Unit.getByName(carrier.carrierUnitName)
    
    -- take note of the starting position
    local startPosition = veaf.getAvgGroupPos(groupName)
    local currentHeading = 0
    if carrierUnit then 
        startPosition = carrierUnit:getPosition().p
        veafCarrierOperations.logTrace("startPosition (raw) ="..veaf.vecToString(startPosition))
        currentHeading = mist.utils.round(mist.utils.toDegree(mist.getHeading(carrierUnit)), 0)
    end    
    startPosition = { x=startPosition.x, z=startPosition.z, y=startPosition.y + veafCarrierOperations.ALT_FOR_MEASURING_WIND} -- on deck, 50 meters above the water
    veafCarrierOperations.logTrace("startPosition="..veaf.vecToString(startPosition))
    veaf.cleanupLogMarkers(veafCarrierOperations.debugMarkersErasedAtEachStep)
    veafCarrierOperations.traceMarkerId = veafCarrierOperations.logMarker(veafCarrierOperations.traceMarkerId, "startPosition", startPosition, veafCarrierOperations.debugMarkersErasedAtEachStep)
    local carrierDistanceFromInitialPosition = ((startPosition.x - carrier.initialPosition.x)^2 + (startPosition.z - carrier.initialPosition.z)^2)^0.5
    veafCarrierOperations.logTrace("carrierDistanceFromInitialPosition="..carrierDistanceFromInitialPosition)

    -- compute magnetic deviation at carrier position
    local magdev = veaf.round(mist.getNorthCorrection(startPosition) * 180 / math.pi,1)
    veafCarrierOperations.logTrace("magdev = " .. magdev)

    -- make the carrier move
    if startPosition ~= nil then
	
        --get wind info
        local wind = atmosphere.getWind(startPosition)
        local windspeed = mist.vec.mag(wind)
        veafCarrierOperations.logTrace("windspeed="..windspeed.." m/s")

        --get wind direction sorted
        local dir = veaf.round(math.atan2(wind.z, wind.x) * 180 / math.pi,0)
        if dir < 0 then
            dir = dir + 360 --converts to positive numbers		
        end
        if dir <= 180 then
            dir = dir + 180
        else
            dir = dir - 180
        end

        dir = dir + carrier.runwayAngleWithBRC --to account for angle of landing deck and movement of the ship
        
        if dir > 360 then
            dir = dir - 360
        end

        veafCarrierOperations.logTrace("dir="..dir .. " (true)")

        local speed = 1
        local desiredWindSpeedOnDeck = carrier.desiredWindSpeedOnDeck * 0.51444444444444444444
        if desiredWindSpeedOnDeck < 1 then desiredWindSpeedOnDeck = 1 end -- minimum 1 m/s 
        if windspeed < desiredWindSpeedOnDeck then
            speed = desiredWindSpeedOnDeck - windspeed 
        end
        veafCarrierOperations.logTrace("BRC speed="..speed.." m/s")

        -- compute a new waypoint
        local headingRad = mist.utils.toRadian(dir)
        local length = 4000
        local newWaypoint = {
            x = startPosition.x + length * math.cos(headingRad),
            z = startPosition.z + length * math.sin(headingRad),
            y = startPosition.y
        }
        veafCarrierOperations.logTrace("headingRad="..headingRad)
        veafCarrierOperations.logTrace("length="..length)
        veafCarrierOperations.logTrace("newWaypoint="..veaf.vecToString(newWaypoint))
        veafCarrierOperations.traceMarkerId = veafCarrierOperations.logMarker(veafCarrierOperations.traceMarkerId, "newWaypoint", newWaypoint, veafCarrierOperations.debugMarkersErasedAtEachStep)
        
        local actualSpeed = speed
        if math.abs(dir - currentHeading) > 15 then -- still aligning
            actualSpeed = veafCarrierOperations.ALIGNMENT_MANOEUVER_SPEED
        end
        veaf.moveGroupTo(groupName, newWaypoint, actualSpeed, 0)
        carrier.heading = dir
        carrier.speed = veaf.round(speed * 1.94384, 0)
        veafCarrierOperations.logTrace("carrier.heading = " .. carrier.heading .. " (true)")
        veafCarrierOperations.logTrace("carrier.heading = " .. carrier.heading + magdev .. " (mag)")
        veafCarrierOperations.logTrace("carrier.speed = " .. carrier.speed .. " kn")

        -- check if a Pedro group exists for this carrier
        if not(mist.getGroupData(carrier.pedroUnitName)) then
            veafCarrierOperations.logInfo("No Pedro group named " .. carrier.pedroUnitName)
        else
        -- prepare or correct the Pedro route (SH-60B, 250ft high, 1nm to the starboard side of the carrier, riding along at the same speed and heading)
            local pedroUnit = Unit.getByName(carrier.pedroUnitName)
            if (pedroUnit) then
                veafCarrierOperations.logDebug("found Pedro unit")
                -- check if unit is still alive
                if pedroUnit:getLife() < 1 then
                    pedroUnit = nil -- respawn when damaged
                end
            end
            
            -- spawn if needed
            if not(pedroUnit and carrier.pedroIsSpawned) then
                veafCarrierOperations.logDebug("respawning Pedro unit")
                local vars = {}
                vars.gpName = carrier.pedroUnitName
                vars.action = 'respawn'
                vars.point = startPosition
                vars.point.y = 100
                vars.radius = 500
                mist.teleportToPoint(vars)
                carrier.pedroIsSpawned = true
            end

            pedroUnit = Unit.getByName(carrier.pedroUnitName)
            local pedroGroup = Group.getByName(carrier.pedroUnitName) -- group has the same name as the unit
            if (pedroGroup) then
                veafCarrierOperations.logDebug("found Pedro group")
                
                -- waypoint #1 is 250m to port
                local offsetPointOnLand, offsetPoint = veaf.computeCoordinatesOffsetFromRoute(startPosition, newWaypoint, 0, 250)
                local pedroWaypoint1 = offsetPoint
                local distanceFromWP1 = ((pedroUnit:getPosition().p.x - pedroWaypoint1.x)^2 + (pedroUnit:getPosition().p.z - pedroWaypoint1.z)^2)^0.5
                if distanceFromWP1 > 500 then
                    veafCarrierOperations.logTrace("Pedro WP1 = " .. veaf.vecToString(pedroWaypoint1))
                    veafCarrierOperations.traceMarkerId = veafCarrierOperations.logMarker(veafCarrierOperations.traceMarkerId, "pedroWaypoint1", pedroWaypoint1, veafCarrierOperations.debugMarkersErasedAtEachStep)
                else
                    pedroWaypoint1 = nil
                end

                -- waypoint #2 is 250m to port, near the end of the carrier route
                local offsetPointOnLand, offsetPoint = veaf.computeCoordinatesOffsetFromRoute(startPosition, newWaypoint, length - 250, 250)
                local pedroWaypoint2 = offsetPoint
                veafCarrierOperations.logTrace("Pedro WP2 = " .. veaf.vecToString(pedroWaypoint2))
                veafCarrierOperations.traceMarkerId = veafCarrierOperations.logMarker(veafCarrierOperations.traceMarkerId, "pedroWaypoint2", pedroWaypoint2, veafCarrierOperations.debugMarkersErasedAtEachStep)

                local mission = { 
                    id = 'Mission', 
                    params = { 
                        ["communication"] = false,
                        ["start_time"] = 0,
                        ["task"] = "Transport",
                        route = { 
                            points = { }
                        } 
                    } 
                }

                if pedroWaypoint1 then 
                    mission.params.route.points = {
                        [1] = 
                        {
                            ["alt"] = 35,
                            ["action"] = "Turning Point",
                            ["alt_type"] = "BARO",
                            ["speed"] = 50,
                            ["type"] = "Turning Point",
                            ["x"] = pedroUnit:getPosition().p.x,
                            ["y"] = pedroUnit:getPosition().p.z,
                            ["speed_locked"] = true,
                        },
                        [2] = { 
                            ["type"] = "Turning Point",
                            ["action"] = "Turning Point",
                            ["x"] = pedroWaypoint1.x,
                            ["y"] = pedroWaypoint1.z,
                            ["alt"] = 35, -- in meters
                            ["alt_type"] = "BARO", 
                            ["speed"] = 50,
                            ["speed_locked"] = true, 
                        },
                        [3] = { 
                            ["type"] = "Turning Point",
                            ["action"] = "Turning Point",
                            ["x"] = pedroWaypoint2.x,
                            ["y"] = pedroWaypoint2.z,
                            ["alt"] = 35, -- in meters
                            ["alt_type"] = "BARO", 
                            ["speed"] = speed,  -- speed in m/s
                            ["speed_locked"] = true, 
                        },
                    } 
                else
                    mission.params.route.points = {
                        [1] = 
                        {
                            ["alt"] = 35,
                            ["action"] = "Turning Point",
                            ["alt_type"] = "BARO",
                            ["speed"] = 50,
                            ["type"] = "Turning Point",
                            ["x"] = pedroUnit:getPosition().p.x,
                            ["y"] = pedroUnit:getPosition().p.z,
                            ["speed_locked"] = true,
                        },
                        [2] = { 
                            ["type"] = "Turning Point",
                            ["action"] = "Turning Point",
                            ["x"] = pedroWaypoint2.x,
                            ["y"] = pedroWaypoint2.z,
                            ["alt"] = 35, -- in meters
                            ["alt_type"] = "BARO", 
                            ["speed"] = speed,  -- speed in m/s
                            ["speed_locked"] = true, 
                        },
                    } 
                end

                -- replace whole mission
                veafCarrierOperations.logDebug("Setting Pedro mission")
                local controller = pedroGroup:getController()
                controller:setTask(mission)

            end
        end


        -- check if a S3B-Tanker group exists for this carrier
        if not(mist.getGroupData(carrier.tankerUnitName)) then
            veafCarrierOperations.logInfo("No Tanker group named " .. carrier.tankerUnitName)
        else

            local routeTanker = (carrierDistanceFromInitialPosition > 18520)
            carrier.tankerRouteSet = carrier.tankerRouteSet + 1
            if carrier.tankerRouteSet <= 2 then
                -- prepare or correct the Tanker route (8000ft high, 10nm aft and 4nm to the starboard side of the carrier, refueling on BRC)
                local tankerUnit = Unit.getByName(carrier.tankerUnitName)
                if (tankerUnit) then
                    veafCarrierOperations.logDebug("found Tanker unit")
                    -- check if unit is still alive
                    if tankerUnit:getLife() < 1 then
                        tankerUnit = nil -- respawn when damaged
                    end
                end
                
                -- spawn if needed
                if not(tankerUnit and carrier.tankerIsSpawned) then
                    veafCarrierOperations.logDebug("respawning Tanker unit")
                    local vars = {}
                    vars.gpName = carrier.tankerUnitName
                    vars.action = 'respawn'
                    vars.point = startPosition
                    vars.point.y = 2500
                    vars.radius = 500
                    mist.teleportToPoint(vars)
                    carrier.tankerIsSpawned = true
                end

                tankerUnit = Unit.getByName(carrier.tankerUnitName)
                local tankerGroup = Group.getByName(carrier.tankerUnitName) -- group has the same name as the unit
                if (tankerGroup) then
                    veafCarrierOperations.logDebug("found Tanker group")
                    veafCarrierOperations.logTrace("groupName="..tankerGroup:getName())
                    
                    -- waypoint #1 is 5nm to port, 5nm to the front
                    local offsetPointOnLand, offsetPoint = veaf.computeCoordinatesOffsetFromRoute(startPosition, newWaypoint, 9000, 9000)
                    local tankerWaypoint1 = offsetPoint
                    veafCarrierOperations.logTrace("Tanker WP1 = " .. veaf.vecToString(tankerWaypoint1))
                    veaf.cleanupLogMarkers(veafCarrierOperations.debugMarkersForTanker)
                    veafCarrierOperations.traceMarkerId = veafCarrierOperations.logMarker(veafCarrierOperations.traceMarkerId, "tankerWaypoint1", tankerWaypoint1, veafCarrierOperations.debugMarkersForTanker)

                    -- waypoint #2 is 20nm ahead of waypoint #2, on BRC
                    local offsetPointOnLand, offsetPoint = veaf.computeCoordinatesOffsetFromRoute(startPosition, newWaypoint, 37000 + 9000, 9000)
                    local tankerWaypoint2 = offsetPoint
                    veafCarrierOperations.logTrace("Tanker WP2 = " .. veaf.vecToString(tankerWaypoint2))
                    veafCarrierOperations.traceMarkerId = veafCarrierOperations.logMarker(veafCarrierOperations.traceMarkerId, "tankerWaypoint2", tankerWaypoint2, veafCarrierOperations.debugMarkersForTanker)

                    local mission = { 
                        id = 'Mission', 
                        params = { 
                            ["communication"] = true,
                            ["start_time"] = 0,
                            ["task"] = "Refueling",
                            ["taskSelected"] = true,
                            ["route"] = 
                            {
                                ["points"] = 
                                {
                                    [1] = 
                                    {
                                        ["alt"] = 2500,
                                        ["action"] = "Turning Point",
                                        ["alt_type"] = "BARO",
                                        ["speed"] = 165,
                                        ["type"] = "Turning Point",
                                        ["x"] = startPosition.x,
                                        ["y"] = startPosition.z,
                                        ["speed_locked"] = true,
                                    },
                                    [2] = 
                                    {
                                        ["alt"] = 2500,
                                        ["action"] = "Turning Point",
                                        ["alt_type"] = "BARO",
                                        ["speed"] = 165,
                                        ["task"] = 
                                        {
                                            ["id"] = "ComboTask",
                                            ["params"] = 
                                            {
                                                ["tasks"] = 
                                                {
                                                    [1] = 
                                                    {
                                                        ["enabled"] = true,
                                                        ["auto"] = true,
                                                        ["id"] = "Tanker",
                                                        ["number"] = 1,
                                                    }, -- end of [1]
                                                    [2] = carrier.tankerData.tankerTacanTask
                                                }, -- end of ["tasks"]
                                            }, -- end of ["params"]
                                        }, -- end of ["task"]
                                        ["type"] = "Turning Point",
                                        ["ETA"] = 0,
                                        ["ETA_locked"] = true,
                                        ["x"] = startPosition.x,
                                        ["y"] = startPosition.z,
                                        ["speed_locked"] = true,
                                    },
                                    [3] = 
                                    {
                                        ["alt"] = 2500,
                                        ["action"] = "Turning Point",
                                        ["alt_type"] = "BARO",
                                        ["speed"] = 165,
                                        ["task"] = 
                                        {
                                            ["id"] = "ComboTask",
                                            ["params"] = 
                                            {
                                                ["tasks"] = 
                                                {
                                                    [1] = 
                                                    {
                                                        ["enabled"] = true,
                                                        ["auto"] = false,
                                                        ["id"] = "Orbit",
                                                        ["number"] = 1,
                                                        ["params"] = 
                                                        {
                                                            ["altitude"] = 2500,
                                                            ["pattern"] = "Race-Track",
                                                            ["speed"] = 165,
                                                        }, -- end of ["params"]
                                                    }, -- end of [1]
                                                }, -- end of ["tasks"]
                                            }, -- end of ["params"]
                                        }, -- end of ["task"]
                                        ["type"] = "Turning Point",
                                        ["x"] = tankerWaypoint1.x,
                                        ["y"] = tankerWaypoint1.z,
                                        ["speed_locked"] = true,
                                    },
                                    [4] = 
                                    {
                                        ["alt"] = 2500,
                                        ["action"] = "Turning Point",
                                        ["alt_type"] = "BARO",
                                        ["speed"] = 165,
                                        ["type"] = "Turning Point",
                                        ["x"] = tankerWaypoint2.x,
                                        ["y"] = tankerWaypoint2.z,
                                        ["speed_locked"] = true,
                                    }, -- end of [3]
                                }, -- end of ["points"]
                            }, -- end of ["route"]
                        }
                    }                

                    -- replace whole mission
                    veafCarrierOperations.logDebug("Setting Tanker mission")
                    local controller = tankerGroup:getController()
                    controller:setTask(mission)
                    carrier.tankerRouteIsSet = true

                end
            end
        end
    end   
end

--- Gets informations about current carrier operations
function veafCarrierOperations.getAtcForCarrierOperations(groupName, skipNavigationData)
    veafCarrierOperations.logDebug("getAtcForCarrierOperations(".. groupName .. ")")

    local carrier = veafCarrierOperations.carriers[groupName]
    local carrierUnit = Unit.getByName(carrier.carrierUnitName)
    local currentHeading = -1
    local currentSpeed = -1
    local startPosition = nil
    if carrierUnit then 
        currentHeading = mist.utils.round(mist.utils.toDegree(mist.getHeading(carrierUnit)), 0)
        currentSpeed = mist.utils.round(mist.utils.mpsToKnots(mist.vec.mag(carrierUnit:getVelocity())),0)
        startPosition = { x=carrierUnit:getPosition().p.x, z=carrierUnit:getPosition().p.z, y=veafCarrierOperations.ALT_FOR_MEASURING_WIND} -- on deck, 50 meters above the water
    end

    if not(carrier) then
        local text = "Cannot find the carrier group "..groupName
        veafCarrierOperations.logError(text)
        trigger.action.outText(text, 5)
        return
    end

    local result = ""
    local groupPosition = veaf.getAvgGroupPos(groupName)
    
    if carrier.conductingAirOperations then
        local remainingTime = veaf.round((carrier.airOperationsEndAt - timer.getTime()) /60, 1)
        result = "The carrier group "..groupName.." is conducting air operations :\n" ..
        "  - Base Recovery Course : " .. carrier.heading .. " (true) at " .. carrier.speed .. " kn\n" ..
        "  - Remaining time : " .. remainingTime .. " minutes\n"
        if carrier.tankerData then
            result = result ..
            "  - Tanker " .. carrier.tankerData.tankerCallsign .. " : TACAN " ..carrier.tankerData.tankerTacanChannel.. carrier.tankerData.tankerTacanMode ..", COMM " .. carrier.tankerData.tankerFrequency .. "\n"
        end
    else
        result = "The carrier group "..groupName.." is not conducting carrier air operations\n"
    end

    if not(skipNavigationData) then
        -- add current navigation data

        if currentHeading > -1 and currentSpeed > -1 then
            -- compute magnetic deviation at carrier position
            local magdev = veaf.round(mist.getNorthCorrection(startPosition) * 180 / math.pi,1)
            veafCarrierOperations.logTrace("magdev = " .. magdev)
            
            result = result ..
            "\n"..
            "Current navigation parameters\n" ..
            "  - Current heading (true) " .. veaf.round(currentHeading - magdev, 0) .. "\n" ..
            "  - Current heading (mag)  " .. veaf.round(currentHeading, 0) .. "\n" ..
            "  - Current speed " .. currentSpeed .. " kn\n"
        end
    end

    result = result .. "\n"..veaf.weatherReport(startPosition)

    return result
end

--- Gets informations about current carrier operations
function veafCarrierOperations.atcForCarrierOperations(parameters)
    local groupName, unitName = veaf.safeUnpack(parameters)
    veafCarrierOperations.logDebug("atcForCarrierOperations(".. groupName .. ")")
    local text = veafCarrierOperations.getAtcForCarrierOperations(groupName)
    veaf.outTextForUnit(unitName, text, 15)
end

--- Ends carrier operations ; changes the radio menu item to START and send the carrier back to its starting point
function veafCarrierOperations.stopCarrierOperations(groupName)
    veafCarrierOperations.logDebug("stopCarrierOperations(".. groupName .. ")")

    local carrier = veafCarrierOperations.carriers[groupName]

    if not(carrier) then
        local text = "Cannot find the carrier group "..groupName
        veafCarrierOperations.logError(text)
        trigger.action.outText(text, 5)
        return
    end

    local carrierUnit = Unit.getByName(carrier.carrierUnitName)
    local carrierPosition = carrierUnit:getPosition().p
    
    local text = "The carrier group "..groupName.." has stopped air operations ; it's moving back to its initial position"
    veafCarrierOperations.logInfo(text)
    trigger.action.outText(text, 5)
    carrier.conductingAirOperations = false
    carrier.stoppedAirOperations = true

    -- change the menu
    veafCarrierOperations.logTrace("change the menu")
    veafCarrierOperations.rebuildRadioMenu()

    -- make the Pedro land
    if (carrier.pedroIsSpawned) then
        carrier.pedroIsSpawned = false
        local pedroUnit = Unit.getByName(carrier.pedroUnitName)
        if (pedroUnit) then
            veafCarrierOperations.logDebug("found Pedro unit ; destroying it")
            pedroUnit:destroy()
        end
    end    

    -- make the tanker land
    if (carrier.tankerIsSpawned) then
        carrier.tankerIsSpawned = false
        local tankerUnit = Unit.getByName(carrier.tankerUnitName)
        if (tankerUnit) then
            veafCarrierOperations.logDebug("found tanker unit ; destroying it")
            tankerUnit:destroy()
        end
    end    

    veafCarrierOperations.doOperations()

end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Radio menu and help
-------------------------------------------------------------------------------------------------------------------------------------------------------------
--- Rebuild the radio menu
function veafCarrierOperations.rebuildRadioMenu()
    veafCarrierOperations.logDebug("veafCarrierOperations.rebuildRadioMenu()")

    -- find the carriers in the veafCarrierOperations.carriers table and prepare their menus
    for name, carrier in pairs(veafCarrierOperations.carriers) do
        veafCarrierOperations.logTrace("rebuildRadioMenu processing "..name)
        
        -- remove the start menu
        if carrier.startMenuName1 then
            veafCarrierOperations.logTrace("remove carrier.startMenuName1="..carrier.startMenuName1)
            veafRadio.delCommand(veafCarrierOperations.rootPath, carrier.startMenuName1)
        end
        if carrier.startMenuName2 then
            veafCarrierOperations.logTrace("remove carrier.startMenuName2="..carrier.startMenuName2)
            veafRadio.delCommand(veafCarrierOperations.rootPath, carrier.startMenuName2)
        end

        -- remove the stop menu
        if carrier.stopMenuName then
            veafCarrierOperations.logTrace("remove carrier.stopMenuName="..carrier.stopMenuName)
            veafRadio.delCommand(veafCarrierOperations.rootPath, carrier.stopMenuName)
        end

        -- remove the ATC menu (by player group)
        if carrier.getInfoMenuName then
            veafCarrierOperations.logTrace("remove carrier.getInfoMenuName="..carrier.getInfoMenuName)
            veafRadio.delCommand(veafCarrierOperations.rootPath, carrier.getInfoMenuName)
        end

        if carrier.conductingAirOperations then
            -- add the stop menu
            carrier.stopMenuName = name .. " - End air operations"
            veafCarrierOperations.logTrace("add carrier.stopMenuName="..carrier.stopMenuName)
            veafRadio.addSecuredCommandToSubmenu(carrier.stopMenuName, veafCarrierOperations.rootPath, veafCarrierOperations.stopCarrierOperations, name)
        else
            -- add the "start for veafCarrierOperations.MAX_OPERATIONS_DURATION" menu
            carrier.startMenuName1 = name .. " - Start carrier air operations for " .. veafCarrierOperations.MAX_OPERATIONS_DURATION .. " minutes"
            veafCarrierOperations.logTrace("add carrier.startMenuName1="..carrier.startMenuName1)
            veafRadio.addSecuredCommandToSubmenu(carrier.startMenuName1, veafCarrierOperations.rootPath, veafCarrierOperations.startCarrierOperations, { name, veafCarrierOperations.MAX_OPERATIONS_DURATION })

            -- add the "start for veafCarrierOperations.MAX_OPERATIONS_DURATION * 2" menu
            carrier.startMenuName2 = name .. " - Start carrier air operations for " .. veafCarrierOperations.MAX_OPERATIONS_DURATION * 2 .. " minutes"
            veafCarrierOperations.logTrace("add carrier.startMenuName2="..carrier.startMenuName2)
            veafRadio.addSecuredCommandToSubmenu(carrier.startMenuName2, veafCarrierOperations.rootPath, veafCarrierOperations.startCarrierOperations, { name, veafCarrierOperations.MAX_OPERATIONS_DURATION * 2 })
        end

        -- add the ATC menu (by player group)
        carrier.getInfoMenuName = name .. " - ATC - Request informations"
        veafCarrierOperations.logTrace("add carrier.getInfoMenuName="..carrier.getInfoMenuName)
        veafRadio.addCommandToSubmenu(carrier.getInfoMenuName, veafCarrierOperations.rootPath, veafCarrierOperations.atcForCarrierOperations, name, veafRadio.USAGE_ForGroup)

        veafRadio.refreshRadioMenu()
    end
end

--- Build the initial radio menu
function veafCarrierOperations.buildRadioMenu()
    veafCarrierOperations.logDebug("veafCarrierOperations.buildRadioMenu")

    veafCarrierOperations.rootPath = veafRadio.addSubMenu(veafCarrierOperations.RadioMenuName)

    -- build HELP menu for each group
    if not(veafRadio.skipHelpMenus) then
        veafRadio.addCommandToSubmenu("HELP", veafCarrierOperations.rootPath, veafCarrierOperations.help, nil, veafRadio.USAGE_ForGroup)
    end
    
    veafCarrierOperations.rebuildRadioMenu()
end

function veafCarrierOperations.help(unitName)
    local text =
        'Use the radio menus to start and end carrier operations\n' ..
        'START: carrier will find out the wind and set sail at optimum speed to achieve a 25kn headwind\n' ..
        '       the radio menu will show the recovery course and TACAN information\n' ..
        'END  : carrier will go back to its starting point (where it was when the START command was issued)\n' ..
        'RESET: carrier will go back to where it was when the mission started'

    veaf.outTextForUnit(unitName, text, 30)
end

function veafCarrierOperations.initializeCarrierGroups()
    -- find the carriers and add them to the veafCarrierOperations.carriers table, store its initial location and create the menus
    for name, group in pairs(mist.DBs.groupsByName) do
        veafCarrierOperations.logTrace("found group "..name)
        -- search groups with a carrier unit in the group
        local carrier = nil
            -- find the actual carrier unit
            local group = Group.getByName(name)
        if group then
            for _, unit in pairs(group:getUnits()) do
                local unitType = unit:getDesc()["typeName"]
                for knownCarrierType, data in pairs(veafCarrierOperations.AllCarriers) do
                    if unitType == knownCarrierType then
                        -- found a carrier, initialize the carrier group object if needed
                        if not carrier then 
                            veafCarrierOperations.carriers[name] = {}
                            carrier = veafCarrierOperations.carriers[name]
                            veafCarrierOperations.logTrace("found carrier !")
                        else
                            veafCarrierOperations.logWarning(string.format("more than one carrier in group %s", veaf.p(name)))
                        end
                        carrier.carrierUnit = unit
                        carrier.carrierUnitName = carrier.carrierUnit:getName()
                        carrier.runwayAngleWithBRC = data.runwayAngleWithBRC
                        carrier.desiredWindSpeedOnDeck = data.desiredWindSpeedOnDeck
                                carrier.pedroUnitName = carrier.carrierUnitName .. " Pedro" -- rescue helo unit name
                        local pedroUnit = Unit.getByName(carrier.pedroUnitName)
                        if pedroUnit then
                            pedroUnit:destroy()
                        end
                        carrier.tankerUnitName = carrier.carrierUnitName .. " S3B-Tanker" -- emergency tanker unit name
                        carrier.tankerData = veaf.getTankerData(carrier.tankerUnitName)
                        local tankerUnit = Unit.getByName(carrier.tankerUnitName)
                        if tankerUnit then
                            tankerUnit:destroy()
                        end
                        break
                    end
                end
            end

            if carrier then
            -- take note of the carrier route
            carrier.missionRoute = mist.getGroupRoute(name, 'task')
            if veafCarrierOperations.Trace then
                for num, point in pairs(carrier.missionRoute) do
                    veafCarrierOperations.traceMarkerId = veafCarrierOperations.logMarker(veafCarrierOperations.traceMarkerId, string.format("[%s] point %d", name, tostring(num)), point, nil)
                end
            end
        end
    end
end
end

function veafCarrierOperations.doOperations()
    veafCarrierOperations.logDebug("veafCarrierOperations.doOperations()")

    -- find the carriers in the veafCarrierOperations.carriers table and check if they are operating
    for name, carrier in pairs(veafCarrierOperations.carriers) do
        veafCarrierOperations.logDebug("checking " .. name)
        if carrier.conductingAirOperations then
            veafCarrierOperations.logDebug(name .. " is conducting operations ; checking course and ops duration")
            if carrier.airOperationsEndAt < timer.getTime() then
                -- time to stop operations
                veafCarrierOperations.logInfo(name .. " has been conducting operations long enough ; stopping ops")
                veafCarrierOperations.stopCarrierOperations(name)
            else
                local remainingTime = veaf.round((carrier.airOperationsEndAt - timer.getTime()) /60, 1)
                veafCarrierOperations.logDebug(name .. " will continue conducting operations for " .. remainingTime .. " more minutes")
                -- check and reset course
                veafCarrierOperations.continueCarrierOperations(name)
            end
        elseif carrier.stoppedAirOperations then
            veafCarrierOperations.logDebug(name .. " stopped conducting operations")
            carrier.stoppedAirOperations = false
            -- reset the carrier group route to its original route (set in the mission)
            if carrier.missionRoute then
                veafCarrierOperations.logDebug(string.format("resetting carrier %s route", name))
                veafCarrierOperations.logTrace("carrier.missionRoute="..veaf.p(carrier.missionRoute))
                local result = mist.goRoute(name, carrier.missionRoute)
            end
        else
            veafCarrierOperations.logDebug(name .. " is not conducting operations")
        end
    end
end

--- This function is called at regular interval (see veafCarrierOperations.SCHEDULER_INTERVAL) and manages the carrier operations schedules
--- It will make any carrier group that has started carrier operations maintain a correct course for recovery, even if wind changes.
--- Also, it will stop carrier operations after a set time (see veafCarrierOperations.MAX_OPERATIONS_DURATION).
function veafCarrierOperations.operationsScheduler()
    veafCarrierOperations.logDebug("veafCarrierOperations.operationsScheduler()")

    veafCarrierOperations.doOperations()

    veafCarrierOperations.logDebug("veafCarrierOperations.operationsScheduler() - rescheduling in " .. veafCarrierOperations.SCHEDULER_INTERVAL * 60 .. " s")
    mist.scheduleFunction(veafCarrierOperations.operationsScheduler,{},timer.getTime() + veafCarrierOperations.SCHEDULER_INTERVAL * 60)
end

------------------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- initialisation
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafCarrierOperations.initialize()
    veafCarrierOperations.initializeCarrierGroups()
    veafCarrierOperations.buildRadioMenu()
    veafCarrierOperations.operationsScheduler()
end

veafCarrierOperations.logInfo(string.format("Loading version %s", veafCarrierOperations.Version))

--- Enable/Disable error boxes displayed on screen.
env.setErrorMessageBoxEnabled(false)



