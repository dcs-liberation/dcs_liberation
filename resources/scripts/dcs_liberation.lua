logger = mist.Logger:new("DCSLiberation", "info")
logger:info("Check that json.lua is loaded : json = "..tostring(json))

killed_aircrafts = {}
killed_ground_units = {}
weapons_fired = {}
base_capture_events = {}
destroyed_objects_positions = {}
mission_ended = false

local function messageAll(message)
    local msg = {}
    msg.text = message
    msg.displayTime = 25
    msg.msgFor = {coa = {'all'}}
    mist.message.add(msg)
end

write_state = function()
    --messageAll("Writing DCS Liberation State...")
    --logger.info("Writing DCS LIBERATION state")
    local fp = io.open(debriefing_file_location, 'w')
    local game_state = {
        ["killed_aircrafts"] = killed_aircrafts,
        ["killed_ground_units"] = killed_ground_units,
        ["weapons_fired"] = weapons_fired,
        ["base_capture_events"] = base_capture_events,
        ["mission_ended"] = mission_ended,
        ["destroyed_objects_positions"] = destroyed_objects_positions,
    }
    if not json then
        local message = string.format("Unable to save DCS Liberation state to %s, JSON library is not loaded !",debriefing_file_location)
        logger:error(message)
        messageAll(message)
    end
    fp:write(json:encode(game_state))
    fp:close()
    -- logger.info("Done writing DCS Liberation state")
    -- messageAll("Done writing DCS Liberation state.")
end


debriefing_file_location = nil
if not debriefing_file_location then
    if os then
        debriefing_file_location = os.getenv("LIBERATION_EXPORT_DIR")
        if debriefing_file_location then debriefing_file_location = debriefing_file_location .. "\\" end
    end
end
if not debriefing_file_location then
    if os then
        debriefing_file_location = os.getenv("TEMP")
        if debriefing_file_location then debriefing_file_location = debriefing_file_location .. "\\" end
    end
end
if not debriefing_file_location then
    if lfs then
        debriefing_file_location = lfs.writedir()
    end
end
if debriefing_file_location then
    debriefing_file_location = debriefing_file_location .. "state.json"
end

logger:info(string.format("DCS Liberation state will be written as json to [[%s]]",debriefing_file_location))

write_state_error_handling = function()
    if pcall(write_state) then
        -- messageAll("Written DCS Liberation state to "..debriefing_file_location)
    else
	    messageAll("Unable to write DCS Liberation state to "..debriefing_file_location..
                "\nYou can abort the mission in DCS Liberation.\n"..
                "\n\nPlease fix your setup in DCS Liberation, make sure you are pointing to the right installation directory from the File/Preferences menu. Then after fixing the path restart DCS Liberation, and then restart DCS."..
                "\n\nYou can also try to fix the issue manually by replacing the file <dcs_installation_directory>/Scripts/MissionScripting.lua by the one provided there : <dcs_liberation_folder>/resources/scripts/MissionScripting.lua. And then restart DCS. (This will also have to be done again after each DCS update)"..
                "\n\nIt's not worth playing, the state of the mission will not be recorded.")
    end
end

mist.scheduleFunction(write_state_error_handling, {}, timer.getTime() + 10, 60, timer.getTime() + 3600)

activeWeapons = {}
local function onEvent(event)
   if event.id == world.event.S_EVENT_CRASH and event.initiator then
       --messageAll("Destroyed  :" .. event.initiator.getName(event.initiator))
       killed_aircrafts[#killed_aircrafts + 1] = event.initiator.getName(event.initiator)
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
    end

    --if event.id == world.event.S_EVENT_SHOT and event.weapon then
    --    weapons_fired[#weapons_fired + 1] = event.weapon.getTypeName(event.weapon)
    --end

    if event.id == world.event.S_EVENT_BASE_CAPTURED and event.place then
        --messageAll("Base captured  :" .. event.place.getName(event.place))
        base_capture_events[#base_capture_events + 1] = event.place.getID(event.place) .. "||" .. event.place.getCoalition(event.place) .. "||" .. event.place.getName(event.place)
    end

    if event.id == world.event.S_EVENT_MISSION_END then
        mission_ended = true
        write_state()
    end

end

mist.addEventHandler(onEvent)