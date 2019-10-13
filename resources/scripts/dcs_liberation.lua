local jsonlib = {{json_file_abs_location}}
json = loadfile(jsonlib)()

logger = mist.Logger:new("DCSLiberation", "info")

debriefing_file_location = {{debriefing_file_location}}

killed_aircrafts = {}
killed_ground_units = {}
weapons_fired = {}
base_capture_events = {}
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
    local fp = io.open(debriefing_file_location, 'w')
    local game_state = {
        ["killed_aircrafts"] = killed_aircrafts,
        ["killed_ground_units"] = killed_ground_units,
        ["weapons_fired"] = weapons_fired,
        ["base_capture_events"] = base_capture_events,
        ["mission_ended"] = mission_ended,
    }
    fp:write(json:encode(game_state))
    fp:close()
    --messageAll("Done writing DCS Liberation state.")
end

mist.scheduleFunction(write_state, {}, timer.getTime() + 10, 60, timer.getTime() + 3600)

activeWeapons = {}
local function onEvent(event)
   if event.id == world.event.S_EVENT_CRASH and event.initiator then
       messageAll("Destroyed  :" .. event.initiator.getName(event.initiator))
       killed_aircrafts[#killed_aircrafts + 1] = event.initiator.getName(event.initiator)
   end

    if event.id == world.event.S_EVENT_DEAD and event.initiator then
        killed_ground_units[#killed_ground_units + 1] = event.initiator.getName(event.initiator)
    end

    if event.id == world.event.S_EVENT_SHOT and event.weapon then
        weapons_fired[#weapons_fired + 1] = event.weapon.getTypeName(event.weapon)
    end

    if event.id == world.event.S_EVENT_BASE_CAPTURED and event.place then
        messageAll("Base captured  :" .. event.place.getName(event.place))
        base_capture_events[#base_capture_events + 1] = event.place.getID(event.place) .. "||" .. event.place.getCoalition(event.place) .. "||" .. event.place.getName(event.place)
    end

    if event.id == world.event.S_EVENT_MISSION_END then
        mission_ended = true
        write_state()
    end

end

mist.addEventHandler(onEvent)