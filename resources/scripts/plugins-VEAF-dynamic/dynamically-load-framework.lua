VEAF_DYNAMIC_PATH = [[d:\dev\_VEAF\VEAF-Mission-Creation-Tools]]
VEAF_DYNAMIC_MISSIONPATH = [[d:\dev\_VEAF\dcs_liberation\resources\scripts\plugins]]

env.info("DYNAMIC LOADING")

local script = VEAF_DYNAMIC_PATH .. "/src/scripts/community/mist.lua"
assert(loadfile(script))()

local script = VEAF_DYNAMIC_PATH .. "/src/scripts/community/Moose.lua"
assert(loadfile(script))()

local script = VEAF_DYNAMIC_PATH .. "/src/scripts/community/CTLD.lua"
assert(loadfile(script))()

local script = VEAF_DYNAMIC_PATH .. "/src/scripts/community/WeatherMark.lua"
assert(loadfile(script))()

local script = VEAF_DYNAMIC_PATH .. "/src/scripts/VeafDynamicLoader.lua"
assert(loadfile(script))()

local script = VEAF_DYNAMIC_MISSIONPATH .. "/missionConfig.lua"
assert(loadfile(script))()
