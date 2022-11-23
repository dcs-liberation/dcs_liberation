-- the state.json file will be updated according to this schedule, and also on each destruction or capture event
local WRITESTATE_SCHEDULE_IN_SECONDS = 60

logger = mist.Logger:new("DCSLiberation", "info")
logger:info("Check that json.lua is loaded : json = "..tostring(json))

killed_aircrafts = {} -- killed aircraft will be added via S_EVENT_CRASH event
killed_ground_units = {} -- killed units will be added via S_EVENT_DEAD event
base_capture_events = {}
destroyed_objects_positions = {} -- will be added via S_EVENT_DEAD event
mission_ended = false

local function ends_with(str, ending)
   return ending == "" or str:sub(-#ending) == ending
end

local function messageAll(message)
    local msg = {}
    msg.text = message
    msg.displayTime = 25
    msg.msgFor = {coa = {'all'}}
    mist.message.add(msg)
end

function write_state()
    local _debriefing_file_location = debriefing_file_location
    if not debriefing_file_location then 
        _debriefing_file_location = "[nil]"
    end

    local fp = io.open(_debriefing_file_location, 'w')
    local game_state = {
        ["killed_aircrafts"] = killed_aircrafts,
        ["killed_ground_units"] = killed_ground_units,
        ["base_capture_events"] = base_capture_events,
        ["mission_ended"] = mission_ended,
        ["destroyed_objects_positions"] = destroyed_objects_positions,
    }
    if not json then
        local message = string.format("Unable to save DCS Liberation state to %s, JSON library is not loaded !", _debriefing_file_location)
        logger:error(message)
        messageAll(message)
    end
    fp:write(json:encode(game_state))
    fp:close()
end

local function canWrite(name)
    local f = io.open(name, "w")
    if f then
        f:close()
        return true
    end
    return false
end

local function testDebriefingFilePath(folderPath, folderName, useCurrentStamping)
    if folderPath then
        local filePath = nil
        if not ends_with(folderPath, "\\") then
            folderPath = folderPath .. "\\"
        end
        if useCurrentStamping then
            filePath = string.format("%sstate-%s.json",folderPath, tostring(os.time()))
        else 
            filePath = string.format("%sstate.json",folderPath)
        end
        local isOk = canWrite(filePath)
        if isOk then 
            logger:info(string.format("The state.json file will be created in %s : (%s)",folderName, filePath))
            return filePath
        end
    end
    return nil
end

local function discoverDebriefingFilePath()   
    -- establish a search pattern into the following modes
    -- 1. Environment variable LIBERATION_EXPORT_DIR, to support dedicated server hosting
    -- 2. Embedded DCS Liberation dcsLiberation.installPath (set by the app to its install path), to support locally hosted single player
    -- 3. System temporary folder, as set in the TEMP environment variable
    -- 4. Working directory.
    
    local useCurrentStamping = nil
    if os then  
        useCurrentStamping = os.getenv("LIBERATION_EXPORT_STAMPED_STATE")
    end

    local installPath = nil
    if dcsLiberation then 
        installPath = dcsLiberation.installPath 
    end
    
    if os then
        local result = nil
        -- try using the LIBERATION_EXPORT_DIR environment variable
        result = testDebriefingFilePath(os.getenv("LIBERATION_EXPORT_DIR"), "LIBERATION_EXPORT_DIR", useCurrentStamping)
        if result then
            return result
        end
        -- no joy ? maybe there is a valid path in the mission ?
        result = testDebriefingFilePath(installPath, "the DCS Liberation install folder", useCurrentStamping)
        if result then
            return result
        end
        -- there's always the possibility of using the system temporary folder
        result = testDebriefingFilePath(os.getenv("TEMP"), "TEMP", useCurrentStamping)
        if result then
            return result
        end
    end

    -- nothing worked, let's try the last resort folder : current directory.
    if lfs then
        return testDebriefingFilePath(lfs.writedir().."Missions\\", "the working directory", useCurrentStamping)
    end
    
    return nil
end

debriefing_file_location = discoverDebriefingFilePath()

write_state_error_handling = function()
    local _debriefing_file_location = debriefing_file_location
    if not debriefing_file_location then 
        _debriefing_file_location = "[nil]"
        logger:error("Unable to find where to write DCS Liberation state")
    end

    if pcall(write_state) then
    else
	    messageAll("Unable to write DCS Liberation state to ".._debriefing_file_location..
                "\nYou can abort the mission in DCS Liberation.\n"..
                "\n\nPlease fix your setup in DCS Liberation, make sure you are pointing to the right installation directory from the File/Preferences menu. Then after fixing the path restart DCS Liberation, and then restart DCS."..
                "\n\nYou can also try to fix the issue manually by replacing the file <dcs_installation_directory>/Scripts/MissionScripting.lua by the one provided there : <dcs_liberation_folder>/resources/scripts/MissionScripting.lua. And then restart DCS. (This will also have to be done again after each DCS update)"..
                "\n\nIt's not worth playing, the state of the mission will not be recorded.")
    end

    -- reschedule
    mist.scheduleFunction(write_state_error_handling, {}, timer.getTime() + WRITESTATE_SCHEDULE_IN_SECONDS)
end

activeWeapons = {}
local function onEvent(event)
   if event.id == world.event.S_EVENT_CRASH and event.initiator then
       killed_aircrafts[#killed_aircrafts + 1] = event.initiator.getName(event.initiator)
       write_state()
   end

    if event.id == world.event.S_EVENT_DEAD and event.initiator then
        killed_ground_units[#killed_ground_units + 1] = event.initiator.getName(event.initiator)
        local position = event.initiator.getPosition(event.initiator)
        local destruction = {}
        destruction.x = position.p.x
        destruction.y = position.p.y
        destruction.z = position.p.z
        destruction.type = event.initiator:getTypeName()
        destruction.orientation = mist.getHeading(event.initiator) * 57.3
        destroyed_objects_positions[#destroyed_objects_positions + 1] = destruction
        write_state()
    end

    if event.id == world.event.S_EVENT_MISSION_END then
        mission_ended = true
        write_state()
    end

end

mist.addEventHandler(onEvent)

-- create the state.json file and start the scheduling
write_state_error_handling()