--[[

2 October 2020
FrozenDroid:
- Added error handling to all event handler and scheduled functions. Lua script errors can no longer bring the server down.
- Added some extra checks to which weapons to handle, make sure they actually have a warhead (how come S-8KOM's don't have a warhead field...?)
28 October 2020
FrozenDroid: 
- Uncommented error logging, actually made it an error log which shows a message box on error.
- Fixed the too restrictive weapon filter (took out the HE warhead requirement)
--]]


local weaponDamageEnable = 1
local killRangeMultiplier = 0.3
local staticDamageRangeMultiplier = 0.1
local stunRangeMultiplier = 1.0

local suppressedGroups = {}
local tracked_weapons = {}
local USearchArray = {}
WpnHandler = {}

local function getDistance(point1, point2)

  local x1 = point1.x
  local y1 = point1.y
  local z1 = point1.z
  local x2 = point2.x
  local y2 = point2.y
  local z2 = point2.z
  local dX = math.abs(x1-x2)
  local dZ = math.abs(z1-z2)
  local distance = math.sqrt(dX*dX + dZ*dZ)

  return distance

end

local function getDistance3D(point1, point2)

  local x1 = point1.x
  local y1 = point1.y
  local z1 = point1.z
  local x2 = point2.x
  local y2 = point2.y
  local z2 = point2.z

  local dX = math.abs(x1-x2)
  local dY = math.abs(y1-y2)
  local dZ = math.abs(z1-z2)
  local distance = math.sqrt(dX*dX + dZ*dZ + dY*dY)

  return distance

end

local function suppress(suppArray)
  
  suppressedGroups[suppArray[1]:getName()] = {["SuppGroup"] = suppArray[1], ["SuppTime"] = suppArray[2]}
  if suppArray[1]:getController() then
    suppArray[1]:getController():setOnOff(false)
--  env.info("Group: "..suppArray[1]:getName().." suppressed")
  end

end

local function unSuppress(unSuppGroup)
--    env.info("In unSuppress")
    if unSuppGroup:isExist() and unSuppGroup:getController() then
      unSuppGroup:getController():setOnOff(true)
  --    env.info("Got controller")
  --    env.info("Suppressed group removed from table")
      suppressedGroups[unSuppGroup:getName()] = nil    
  end
end

local function ifFoundS(foundItem, impactPoint)
--  trigger.action.outText("Found Static", 10)
--  env.info("Found static in kill range")
  local point1 = foundItem:getPoint()
  point1.y = point1.y + 2
  local point2 = impactPoint
  point2.y = point2.y + 2
  if land.isVisible(point1, point2) == true then
--    env.info("Static"..foundItem:getID().. "Destroyed by script")                         
    trigger.action.explosion(point1, 5)
  end  
end

local function ifFoundU(foundItem, USearchArray)

--  env.info("Found Unit")
  local point1 = foundItem:getPoint()
--  env.info("Got point")
  point1.y = point1.y + 5
  local point2 = USearchArray.point
  point2.y = point2.y + 5
  if land.isVisible(point1, point2) == true then
--    env.info("is visible LOS")
    local distanceFrom = getDistance(point1, point2)  
--    env.info("got distance: "..distanceFrom)
    if distanceFrom < USearchArray.exMass*killRangeMultiplier then
      trigger.action.explosion(foundItem:getPoint(), 1)
 --     env.info("Unit: "..foundItem:getName().." was destroyed by script")    
    -- else    
    --   local suppTimer = math.random(30,100)
    --   local suppArray = {foundItem:getGroup(), suppTimer}
    --   suppress(suppArray)    
   end
  end         

end

local function track_wpns()
--  env.info("Weapon Track Start")
  for wpn_id_, wpnData in pairs(tracked_weapons) do  
  
    if wpnData.wpn:isExist() then  -- just update position and direction.
      wpnData.pos = wpnData.wpn:getPosition().p
      wpnData.dir = wpnData.wpn:getPosition().x
      wpnData.exMass = wpnData.wpn:getDesc().warhead.explosiveMass
      --wpnData.lastIP = land.getIP(wpnData.pos, wpnData.dir, 50)
    else -- wpn no longer exists, must be dead.
--      trigger.action.outText("Weapon impacted, mass of weapon warhead is " .. wpnData.exMass, 2)
      local ip = land.getIP(wpnData.pos, wpnData.dir, 20)  -- terrain intersection point with weapon's nose.  Only search out 20 meters though.
      local impactPoint
      if not ip then -- use last calculated IP
        impactPoint = wpnData.pos
--        trigger.action.outText("Impact Point:\nPos X: " .. impactPoint.x .. "\nPos Z: " .. impactPoint.z, 2)
      else -- use intersection point
        impactPoint = ip
--        trigger.action.outText("Impact Point:\nPos X: " .. impactPoint.x .. "\nPos Z: " .. impactPoint.z, 2)
      end 
      local staticRadius = wpnData.exMass*staticDamageRangeMultiplier
--     trigger.action.outText("Static Radius :"..staticRadius, 10)      
     local VolS =
        {
          id = world.VolumeType.SPHERE,
          params =
          {
            point = impactPoint,
            radius = staticRadius
          }
        }
      local VolU =
        {
          id = world.VolumeType.SPHERE,
          params =
          { 
            point = impactPoint,
            radius = wpnData.exMass*stunRangeMultiplier
          }
        }  
--      env.info("Static search radius: " ..wpnData.exMass*staticDamageRangeMultiplier)                                      
--      env.warning("Begin Search")
--      trigger.action.outText("Beginning Searches", 10)
      world.searchObjects(Object.Category.STATIC, VolS, ifFoundS,impactPoint)
      USearchArray = {["point"] = impactPoint, ["exMass"] = wpnData.exMass}
      world.searchObjects(Object.Category.UNIT, VolU, ifFoundU, USearchArray)       
--      env.warning("Finished Search")
      tracked_weapons[wpn_id_] = nil -- remove from tracked weapons first.         
    end
  end
--  env.info("Weapon Track End")
end

local function checkSuppression()
--  env.info("Checking suppression")
  for i, group in pairs(suppressedGroups) do  
--    env.info("Check group exists, #".. i)
    if group.SuppGroup:isExist() then
--      env.info("It does")
     group.SuppTime = group.SuppTime - 10   
     if group.SuppTime < 1 then 
--      env.info("SuppTime < 1")  
      unSuppress(group.SuppGroup)       
     end  
   else  
    suppressedGroups[group.SuppGroup:getName()] = nil    
   end
  end
--  env.info("Ending suppression check")
end

function onWpnEvent(event)
  if event.id == world.event.S_EVENT_SHOT then
    if event.weapon then
      local ordnance = event.weapon
      local weapon_desc = ordnance:getDesc()
      if (weapon_desc.category == 3 or weapon_desc.category == 2 or weapon_desc.category == 1) and not (weapon_desc.missileCategory == 1 or weapon_desc.missileCategory == 2 or weapon_desc.missileCategory == 3) and weapon_desc.warhead and weapon_desc.warhead.explosiveMass and event.initiator then
        tracked_weapons[event.weapon.id_] = { wpn = ordnance, init = event.initiator:getName(), pos = ordnance:getPoint(), dir = ordnance:getPosition().x, exMass = weapon_desc.warhead.explosiveMass }
--        env.info("Tracking " .. event.initiator:getName())
      end
    end
  end
end

function WpnHandler:onEvent(event)
  protectedCall(onWpnEvent, event)
end

function protectedCall(...)
  local status, retval = pcall(...)
  if not status then
    env.error("Splash damage script error... gracefully caught! " .. retval, true)
  end
end

if (weaponDamageEnable == 1) then
  timer.scheduleFunction(function() 
      protectedCall(track_wpns)
      return timer.getTime() + 1
    end, 
    {}, 
    timer.getTime() + 0.5
  )

  timer.scheduleFunction(function() 
      protectedCall(checkSuppression) 
      return timer.getTime() + 1
    end, 
    {}, 
    timer.getTime() + 10
  )

  world.addEventHandler(WpnHandler)
end
