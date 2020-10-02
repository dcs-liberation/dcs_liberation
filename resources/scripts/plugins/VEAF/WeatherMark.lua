-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- WeatherMark Script for DCS World
-- Version 1.0
-- By funkyfranky (2018)
-- 
-- Features:
-- ---------
-- * Offers easy access to weather data at all points of the map.
-- * Reports temperature, QFE pressure, wind direction and strength, wind strength classification according to Beaufort scale.
-- * Output of weather data in metric or imperial units.
-- * Optionally, the altitude can be specified at which the weather data is evaluated.
-- * Works with static and dynamic weather.
-- * Works with all current and future maps (Caucasus, NTTR, Normandy, PG, ...)
-- 
-- Prerequisite:
-- ------------
-- * This script requires DCS 2.5.1 or higher. Note that the script uses only the pure DCS API, i.e. NO other framework like MIST, MOOSE, etc required.
-- 
-- Load the script:
-- ----------------
-- 1.) Download the script and save it anywhere on your hard drive.
-- 2.) Open your mission in the mission editor.
-- 3.) At a new trigger:
--     * TYPE   "4 MISSION START"
--     * ACTION "DO SCRIPT FILE"
--     * OPEN --> Browse to the location where you saved the script and click OK.
-- 4.) Save the mission and start it.
-- 5.) Have fun :)
-- 
-- Basic Usage:
-- ------------
-- 1.) Place a mark on the F10 map.
-- 2.) As text enter "weather report".
-- 3.) Click somewhere else on the map to submit the new text.
-- 4.) The original mark will disappear and a new mark with the weather data at the point the mark was set is created.
-- 
-- Options:
-- --------
-- Type "weather report, imperial" to get weather report in imperial units independent of default unit system.
-- Type "weather report, metric" to get weather report in metric units independent of default unit system.
-- Type "weather report, alt 1000" to get weather report at that location but at an ASL altitude of 1000 meters for feet, depending on default unit system.
-- Type "weather report, alt 1000, imperial" to get weather at that location at an altitude of 1000 feet independent of default unit system.
-- Type "weather report, alt 1000, metric" to get weather at that location at an altitude of 1000 meters independent of default unit system.
-- Type "weather set, metric" to set the default unit system to metric units.
-- Type "weather set, imperial" to set the default unit system to imperial units.
-- 
-- *** NOTE ***
-- * All keywords are CaSE inSenSITvE.
-- * Instead of "weather report" you can also type "weather request" or "weather mark". All three commands are equivalent.
-- * Commas are the speparators between options ==> They are IMPORTANT!
-- 
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Weathermark Table.
weathermark={}

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- User settings. Choose main key phrase and default unit system.
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Set default unit system. Possible values:
-- "metric"   ==> Pressure in hPa and mmHg, Temperature in Celsius, Wind speed in meters per second, altitude in meters.
-- "imperial" ==> Pressure in hPa and inHg, Temperature in Fahrenheit, Wind speed in knots, altitude in feet.
weathermark.unitsystem="metric"

--- Key phrase to look for in the mark text which triggers the weather report.
weathermark.keyphrase="weather"

--- DCS bug regarding wrong marker vector components was fixed. If so, set to true! 
weathermark.DCSbugfixed=true

--- Enable debug mode ==> give more output to DCS log file.
weathermark.Debug=false

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Do not change anything below unless you know what you are doing!
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Version.
weathermark.version="1.1"

--- Identifier. All output in DCS.log will start with this.
weathermark.id="WeatherMark "

--- Enable/Disable error boxes displayed on screen.
env.setErrorMessageBoxEnabled(false)

--- Initial Marker id.
weathermark.markid=10000

--- Unit conversion factors.
weathermark.meter2feet=3.28084
weathermark.hPa2mmHg=0.7500615613030
weathermark.hPa2inHg=0.0295299830714
weathermark.mps2knots=1.94384

--- Enumerators.
weathermark.imperial="imperial"
weathermark.metric="metric"

-- Version info.
env.info(weathermark.id..string.format("Loading version %s", weathermark.version))
env.info(weathermark.id..string.format("Keyphrase   = %s", weathermark.keyphrase))
env.info(weathermark.id..string.format("Unit system = %s", weathermark.unitsystem))

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Event handler.
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Event handler.
weathermark.eventHandler={}

--- Handle world events.
function weathermark.eventHandler:onEvent(Event)

  -- Only interested in S_EVENT_MARK_*
  if Event == nil or Event.idx == nil then
    return true
  end

  -- Debug output.
  if Event.id==world.event.S_EVENT_MARK_ADDED then
    weathermark.info(weathermark.id.."S_EVENT_MARK_ADDED")
  elseif Event.id==world.event.S_EVENT_MARK_CHANGE then
    weathermark.info(weathermark.id.."S_EVENT_MARK_CHANGE")
  elseif Event.id==world.event.S_EVENT_MARK_REMOVED then
    weathermark.info(weathermark.id.."S_EVENT_MARK_REMOVED")    
  end
  weathermark.info(string.format("Event id        = %s", tostring(Event.id)))
  weathermark.info(string.format("Event time      = %s", tostring(Event.time)))
  weathermark.info(string.format("Event idx       = %s", tostring(Event.idx)))
  weathermark.info(string.format("Event coalition = %s", tostring(Event.coalition)))
  weathermark.info(string.format("Event group id  = %s", tostring(Event.groupID)))
  weathermark.info(string.format("Event pos X     = %s", tostring(Event.pos.x)))
  weathermark.info(string.format("Event pos Y     = %s", tostring(Event.pos.y)))
  weathermark.info(string.format("Event pos Z     = %s", tostring(Event.pos.z)))
  if Event.initiator~=nil then
    local _unitname=Event.initiator:getName()
    weathermark.info(string.format("Event ini unit  = %s", tostring(_unitname)))
  end
  weathermark.info(string.format("Event text      = \n%s", tostring(Event.text)))
  

  -- Call event function when a marker has changed, i.e. text was entered or changed.
  if Event.id==world.event.S_EVENT_MARK_CHANGE then
    weathermark._OnEventMarkChange(Event)
  end

end 

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Event handler functions.
------------------------------------------------------------------------------------------------------------------------------------------------------------- 

--- Function executed when a mark has changed. This happens when text is entered or changed. 
function weathermark._OnEventMarkChange(Event)

  -- Check if marker has a text and the "weater report" keyphrase.
  if Event.text~=nil and Event.text:lower():find(weathermark.keyphrase) then
   
    -- Convert (wrong x-->z, z-->x) vec3
    -- TODO: This needs to be "fixed", once DCS gives the correct numbers for x and z.
    local vec3
    if weathermark.DCSbugfixed then
      vec3={x=Event.pos.x, y=Event.pos.y, z=Event.pos.z}
    else
      vec3={x=Event.pos.z, y=Event.pos.y, z=Event.pos.x}
    end
   
    -- By default, alt of mark point is always 5 m! Adjust for the correct ASL height.
    vec3.y=weathermark._GetLandHeight(vec3)

    -- Analyse the mark point text and extract the keywords.
    local _options=weathermark._MarkTextAnalysis(Event.text)
    
    if _options then
      -- Check options set commands and return.
      if _options.set then
        if _options.unitsystem then
          weathermark.unitsystem=_options.unitsystem
          weathermark.info(weathermark.id..string.format("Global option unitsystem changed to %s.", _options.unitsystem))
          -- Delete old mark.
          weathermark.info(weathermark.id..string.format("Removing mark # %d.", Event.idx))
          trigger.action.removeMark(Event.idx)
        end
        return
      end
    else
      -- None of the keywords matched.
      return
    end
    
    -- Ajust manual altitude from meters to feet if unit system is imperial.
    if _options.alt then
      if (_options.unitsystem and _options.unitsystem=="imperial") or (_options.unitsystem==nil and weathermark.unitsystem=="imperial") then
        _options.alt=_options.alt/weathermark.meter2feet
      end
    end 
        
    -- Get weather report text.
	local _report=nil;
	if _options.laste then
      _report = weathermark._Laste(vec3, _options.alt)
	else
      _report = weathermark._WeatherReport(vec3, _options.alt, _options.unitsystem or weathermark.unitsystem)
    end

    -- Add a new mark with weather report info.
    weathermark.markid=weathermark.markid+1
    if Event.groupID > 0 then
      weathermark.info(weathermark.id..string.format("Mark # %d added for group ID %d.", weathermark.markid, Event.groupID))
      trigger.action.markToGroup(weathermark.markid, _report, vec3, Event.groupID, false, "Weather Mark added for own group.")      
    else
      weathermark.info(weathermark.id..string.format("Mark # %d added for coalition %d.", weathermark.markid, Event.coalition))
      trigger.action.markToCoalition(weathermark.markid, _report, vec3, Event.coalition, false, "Weather Mark added for own coalition.")      
    end
    
    -- Delete old mark.
    weathermark.info(weathermark.id..string.format("Removing mark # %d.", Event.idx))
    trigger.action.removeMark(Event.idx)
     
  end

end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Analyse the mark text and extract keywords.
------------------------------------------------------------------------------------------------------------------------------------------------------------- 

--- Extract keywords from mark text.
function weathermark._MarkTextAnalysis(text)

  weathermark.info(weathermark.id..string.format("MarkTextAnalysis text:\n%s", text))
 
  -- Option parameters extracted from the mark text. 
  local switch={}
  switch.report=false
  switch.set=false
  switch.laste=false

  -- Check for correct keywords.
  if text:lower():find(weathermark.keyphrase.." report") or text:lower():find(weathermark.keyphrase.." request") or text:lower():find(weathermark.keyphrase.." mark") then
    switch.report=true
  elseif text:lower():find(weathermark.keyphrase.." set") then
    switch.set=true
  elseif text:lower():find(weathermark.keyphrase.." laste") then
    switch.laste=true
  else
    weathermark.info(weathermark.id..'WARNING: NEITHER "REPORT"/"REQUEST"/"LASTE" nor "SET" keywords specified!')
    return nil
  end
    
  -- keywords are split by ","
  local keywords=weathermark._split(text, ",")

  for _,keyphrase in pairs(keywords) do
  
    -- Split keyphrase by space. First one is the key and second, ... the parameter(s) until the next comma.
    local str=weathermark._split(keyphrase, " ")
    local key=str[1]
    local val=str[2]
    
    if (switch.report or switch.set) and keyphrase:lower():find("imperial") then
    
      switch.unitsystem="imperial"
      weathermark.info(weathermark.id..string.format("Keyword unit = %s", switch.unitsystem))
      
    elseif (switch.report or switch.set) and keyphrase:lower():find("metric") then
    
      switch.unitsystem="metric"
      weathermark.info(weathermark.id..string.format("Keyword unit = %s", switch.unitsystem))
      
    elseif switch.report and key:lower():find("alt") then
      
      -- Set altitude.
      switch.alt=tonumber(val)      
      weathermark.info(weathermark.id..string.format("Keyword alt = %d", val))
      
    end
    
  end
  
  return switch
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Main weather report.
------------------------------------------------------------------------------------------------------------------------------------------------------------- 

--- Just print LASTE (used in A-10C)
function weathermark._Laste(vec3)

	-- LASTE is in Flight Level (x100ft) and T°C
	alt=weathermark._GetLandHeight(vec3)

    local function getLASTEat(vec3, alt)
        local T,_=atmosphere.getTemperatureAndPressure({x=vec3.x, y=alt, z=vec3.z})
        local Dir,Vel=weathermark._GetWind(vec3, alt)
        local laste = string.format("\nFL%02d W%03d/%02d T%d", alt * weathermark.meter2feet / 1000, Dir, Vel * weathermark.mps2knots, T-273.15)
        return laste
    end

    local text=""
	text=text.."LASTE:"
	text=text..getLASTEat(vec3, alt) -- alt +0ft
	text=text..getLASTEat(vec3, alt+610) -- alt +2000ft
	text=text..getLASTEat(vec3, alt+1830) -- alt +6000ft
	text=text..getLASTEat(vec3, alt+3660) -- alt +12000ft

	return text
end

--- Weather Report. Report pressure QFE/QNH, temperature, wind at certain location.
function weathermark._WeatherReport(vec3, alt, unitsystem)
  
  -- Debug output.
  weathermark.info(weathermark.id..string.format("Weather report coordinates:"))
  weathermark.info(weathermark.id..string.format("vec3 x = %s", tostring(vec3.x)))
  weathermark.info(weathermark.id..string.format("vec3 y = %s", tostring(vec3.y)))
  weathermark.info(weathermark.id..string.format("vec3 z = %s", tostring(vec3.z)))
  weathermark.info(weathermark.id..string.format("alt    = %s", tostring(alt)))
  weathermark.info(weathermark.id..string.format("units  = %s", tostring(unitsystem)))
  
  -- Get Temperature [K] and Pressure [Pa] at vec3.
  local T
  local Pqfe
  if alt then
    -- At user specified altitude.
    T,Pqfe=atmosphere.getTemperatureAndPressure({x=vec3.x, y=alt, z=vec3.z})
  else
    -- One meter above the surface.
    T,Pqfe=atmosphere.getTemperatureAndPressure(vec3)
  end
  
  -- Get pressure at sea level.
  local _,Pqnh=atmosphere.getTemperatureAndPressure({x=vec3.x, y=0, z=vec3.z})
  
  -- Convert pressure from Pascal to hecto Pascal.
  Pqfe=Pqfe/100
  Pqnh=Pqnh/100 
   
  -- Pressure unit conversion hPa --> mmHg or inHg
  local _Pqnh=string.format("%.1f mmHg", Pqnh * weathermark.hPa2mmHg)
  local _Pqfe=string.format("%.1f mmHg", Pqfe * weathermark.hPa2mmHg)
  -- Imperial units inch Hg.
  if unitsystem=="imperial" then 
    _Pqnh=string.format("%.2f inHg", Pqnh * weathermark.hPa2inHg)
    _Pqfe=string.format("%.2f inHg", Pqfe * weathermark.hPa2inHg)
  end
 
  -- Temperature unit conversion: Kelvin to Celsius or Fahrenheit.
  T=T-273.15
  local _T=string.format('%d°C', T)
  if unitsystem=="imperial" then
    _T=string.format('%d°F', weathermark._CelsiusToFahrenheit(T))
  end

  -- Get wind direction and speed.
  local Dir,Vel=weathermark._GetWind(vec3, alt)
  
  -- Get Beaufort wind scale.
  local Bn,Bd=weathermark._BeaufortScale(Vel)
  
  -- Formatted wind direction.
  local Ds = string.format('%03d°', Dir)
    
  -- Velocity in player units.
  local Vs=string.format('%.1f m/s', Vel) 
  if unitsystem=="imperial" then
    Vs=string.format("%.1f knots", Vel * weathermark.mps2knots)
  end
  
  -- Altitude.
  local _alt=alt or vec3.y
  local _Alt=string.format("%d m", _alt)
  if unitsystem=="imperial" then
    _Alt=string.format("%d ft", _alt * weathermark.meter2feet)
  end
  
    
  -- Weather report text.
  -- NOTE, there is big problem with the text. If there are too many \n or the text is too long, DCS crashes!
  -- This happens always when you have 5 or more \n or even with just 4 \n and for example one long line which alse breaks the text into another line.
  local text="" 
  text=text..string.format("Altitude %s ASL\n",_Alt)
  text=text..string.format("QFE  %.1f hPa = %s\n", Pqfe,_Pqfe)
  --text=text..string.format("QNH %.1f hPa = %s\n", Pqnh,_Pqnh)
  text=text..string.format("Temperature %s\n",_T)
  text=text..string.format("Wind from %s at %s (%s)", Ds, Vs, Bd)
  
  weathermark.info(string.format("WeatherMark Report:\n%s", text))
  return text
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Helper functions.
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Debug output to dcs.log file.
function weathermark.info(text)
  if weathermark.Debug then
    env.info(text)
  end
end

--- Returns the wind direction (from) and strength.
function weathermark._GetWind(vec3, height)

  local point={x=vec3.x, y=vec3.y, z=vec3.z}
  
  if height then
    point.y=height
  else
    point.y=vec3.y
  end
  
  -- Get wind velocity vector.
  local windvec3  = atmosphere.getWind(point)
  local direction = math.deg(math.atan2(windvec3.z, windvec3.x))
  
  if direction < 0 then
    direction = direction + 360
  end
  
  -- Convert TO direction to FROM direction. 
  if direction > 180 then
    direction = direction-180
  else
    direction = direction+180
  end
  
  -- Calc 2D strength.
  local strength=math.sqrt((windvec3.x)^2+(windvec3.z)^2)
  
  -- Return wind direction and strength km/h.
  return direction, strength, windvec3
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Return the height of the land at the coordinate.
function weathermark._GetLandHeight(vec3)
  local vec2 = {x=vec3.x, y=vec3.z}
  -- We add 1 m "safety margin" because data from getlandheight gives the surface and wind at or below the surface is zero!
  return land.getHeight(vec2)+1
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Beaufort scale: returns Beaufort number and wind description as a function of wind speed in m/s.
function weathermark._BeaufortScale(speed)
  local bn=nil
  local bd=nil
  if speed<0.51 then
    bn=0
    bd="Calm"
  elseif speed<2.06 then
    bn=1
    bd="Light Air"
  elseif speed<3.60 then
    bn=2
    bd="Light Breeze"
  elseif speed<5.66 then
    bn=3
    bd="Gentle Breeze"
  elseif speed<8.23 then
    bn=4
    bd="Moderate Breeze"
  elseif speed<11.32 then
    bn=5
    bd="Fresh Breeze"
  elseif speed<14.40 then
    bn=6
    bd="Strong Breeze"
  elseif speed<17.49 then
    bn=7
    bd="Moderate Gale"
  elseif speed<21.09 then
    bn=8
    bd="Fresh Gale"
  elseif speed<24.69 then
    bn=9
    bd="Strong Gale"
  elseif speed<28.81 then
    bn=10
    bd="Storm"
  elseif speed<32.92 then
    bn=11
    bd="Violent Storm"
  else
    bn=12
    bd="Hurricane"
  end
  return bn,bd
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Convert Celsius to Fahrenheit.
weathermark._CelsiusToFahrenheit = function(Celsius)
  return Celsius * 9/5 + 32 
end

--- Split string. C.f. http://stackoverflow.com/questions/1426954/split-string-in-lua
function weathermark._split(str, sep)
  local result = {}
  local regex = ("([^%s]+)"):format(sep)
  for each in str:gmatch(regex) do
    table.insert(result, each)
  end
  return result
end

--- Create wind profile.
function weathermark._WindvsAlt()
  weathermark.info("FF Weather curve")
  local alt=0
  for i=1,2000 do
    local dir,vel,vec3=weathermark._GetWind({x=0, y=0, z=0}, alt)
    weathermark.info(string.format("%.3f;%.3f;%.1f;%.3f,%.3f;%.3f", alt, vel, dir, vec3.x, vec3.y, vec3.z))
    alt=alt+10
  end
end
--weathermark._WindvsAlt()

-------------------------------------------------------------------------------------------------------------------------------------------------------------
--- Add event handler.
-------------------------------------------------------------------------------------------------------------------------------------------------------------

world.addEventHandler(weathermark.eventHandler)

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------------