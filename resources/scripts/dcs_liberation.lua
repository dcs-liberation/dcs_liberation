local jsonlib = lfs.writedir() .. "Scripts\\DCSLiberation\\json.lua"
json = loadfile(jsonlib)()

killed_aircrafts = {};
killed_ground_units = {};
weapons_fired = {}

local function messageAll(message)
    local msg = {}
    msg.text = message
    msg.displayTime = 25
    msg.msgFor = {coa = {'all'}}
    mist.message.add(msg)
end

write_state = function()
    log("Writing DCS Liberation State...")
    local stateFile = lfs.writedir()..[[Scripts\DCSLiberation\state.json]]
    local fp = io.open(stateFile, 'w')
    local game_state = {
        ["killed_aircrafts"] = killed_aircrafts,
        ["killed_ground_units"] = killed_ground_units,
        ["weapons_fired"] = weapons_fired,
    }
    fp:write(json:encode(game_state))
    fp:close()
    log("Done writing DCS Liberation state.")
end

mist.scheduleFunction(write_state, {}, timer.getTime() + 10, 60, timer.getTime() + 3600)

activeWeapons = {}
local function onCrash(event)
   if event.id == world.event.S_EVENT_CRASH and event.initiator then
       messageAll("Crash :" .. event.initiator.getName(event.initiator))
       killed_aircrafts[#killed_aircrafts + 1] = event.initiator.getName(event.initiator)
   end

    if event.id == world.event.S_EVENT_DEAD and event.initiator then
        killed_ground_units[#killed_ground_units + 1] = event.initiator.getName(event.initiator)
    end

    if event.id == world.event.S_EVENT_SHOT and event.weapon then
        weapons_fired[#weapons_fired + 1] = event.weapon.getTypeName(event.weapon)
    end
end



mist.addEventHandler(onCrash)