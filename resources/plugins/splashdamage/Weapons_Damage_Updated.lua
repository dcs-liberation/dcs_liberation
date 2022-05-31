

--[[
2 October 2020
FrozenDroid:
- Added error handling to all event handler and scheduled functions. Lua script errors can no longer bring the server down.
- Added some extra checks to which weapons to handle, make sure they actually have a warhead (how come S-8KOM's don't have a warhead field...?)
28 October 2020
FrozenDroid: 
- Uncommented error logging, actually made it an error log which shows a message box on error.
- Fixed the too restrictive weapon filter (took out the HE warhead requirement)
29 May 2022
Ghosti:
- Implemented generating extra explosions near BLU-97/B hits to simulate the missing submunitions which are omitted by ED
  due to performance reasons. This is an attempt at making the A-model JSOW more useful against groups of soft targets.
--]]

explTable = {
	["FAB_100"]	=	45,
	["FAB_250"]	=	100,
	["FAB_250M54TU"]=	100,
	["FAB_500"]	=	213,
	["FAB_1500"]	=	675,
	["BetAB_500"]	=	98,
	["BetAB_500ShP"]=	107,
	["KH-66_Grom"]	=	108,
	["M_117"]	=	201,
	["Mk_81"]	=	60,
	["Mk_82"]	=	118,
	["AN_M64"]	=	121,
	["Mk_83"]	=	274,
	["Mk_84"]	=	582,
	["MK_82AIR"]	=	118,
	["MK_82SNAKEYE"]=	118,
	["GBU_10"]	=	582,
	["GBU_12"]	=	118,
	["GBU_16"]	=	274,
	["KAB_1500Kr"]	=	675,
	["KAB_500Kr"]	=	213,
	["KAB_500"]	=	213,
	["GBU_31"]	=	582,
	["GBU_31_V_3B"]	=	582,
	["GBU_31_V_2B"]	=	582,
	["GBU_31_V_4B"]	=	582,
	["GBU_32_V_2B"]	=	202,
	["GBU_38"]	=	118,
	["AGM_62"]	=	400,
	["GBU_24"]	=	582,
	["X_23"]	=	111,
	["X_23L"]	=	111,
	["X_28"]	=	160,
	["X_25ML"]	=	89,
	["X_25MP"]	=	89,
	["X_25MR"]	=	140,
	["X_58"]	=	140,
	["X_29L"]	=	320,
	["X_29T"]	=	320,
	["X_29TE"]	=	320,
	["AGM_84E"]	=	488,
	["AGM_88C"]	=	89,
	["AGM_122"]	=	15,
	["AGM_123"]	=	274,
	["AGM_130"]	=	582,
	["AGM_119"]	=	176,
    ["AGM_154A"]  = 100,                           -- AGM-154A - JSOW CEB (CBU-type) - 145 BLU-97/B Combined Effects Bomb (CEB) submunitions
	["AGM_154C"]	=	305,
	["S-24A"]	=	24,
	--["S-24B"]	=	123,
	["S-25OF"]	=	194,
	["S-25OFM"]	=	150,
	["S-25O"]	=	150,
	["S_25L"]	=	190,
	["S-5M"]	=	1,
	["C_8"]		=	4,
	["C_8OFP2"]	=	3,
	["C_13"]	=	21,
	["C_24"]	=	123,
	["C_25"]	=	151,
	["HYDRA_70M15"]	=	2,
	["Zuni_127"]	=	5,
	["ARAKM70BHE"]	=	4,
	["BR_500"]	=	118,
	["Rb 05A"]	=	217,
	["HEBOMB"]	=	40,
	["HEBOMBD"]	=	40,
	["MK-81SE"]	=	60,
	["AN-M57"]	=	56,
	["AN-M64"]	=	180,
	["AN-M65"]	=	295,
	["AN-M66A2"]	=	536,
    ["CBU_87"] = 100,                              --CBU-87 - 202 x CEM Cluster Bomb
    ["CBU_103"] = 100,                             --CBU-103 - 202 x CEM, CBU with WCMD
}

clusterWeaps = {
  ["AGM_154A"]  = 145,                           -- AGM-154A - JSOW CEB (CBU-type) - 145 BLU-97/B Combined Effects Bomb (CEB) submunitions
  ["CBU_87"] = 202,                              -- CBU-87 - 202 x CEM Cluster Bomb
  ["CBU_103"] = 202,                             -- CBU-103 - 202 x CEM, CBU with WCMD
}

local clusterEffectsEnable = 1
WpnHandler = {}
tracked_weapons = {}
tracked_clusters = {}
shell_max_flight_time = 30
cluster_max_flight_time = 30
cluster_munition_distribution_radius = 75
refreshRate = 0.1

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

local function vec3Mag(speedVec)

	mag = speedVec.x*speedVec.x + speedVec.y*speedVec.y+speedVec.z*speedVec.z
	mag = math.sqrt(mag)
	--trigger.action.outText("X = " .. speedVec.x ..", y = " .. speedVec.y .. ", z = "..speedVec.z, 10)
	--trigger.action.outText("Speed = " .. mag, 1)
	return mag

end

local function lookahead(speedVec)

	speed = vec3Mag(speedVec)
	dist = speed * refreshRate * 1.5 
	return dist

end

local function track_wpns()
--  env.info("Weapon Track Start")
	for wpn_id_, wpnData in pairs(tracked_weapons) do   
		if wpnData.wpn:isExist() then  -- just update speed, position and direction.
			wpnData.pos = wpnData.wpn:getPosition().p
			wpnData.dir = wpnData.wpn:getPosition().x
			wpnData.speed = wpnData.wpn:getVelocity()
      --wpnData.lastIP = land.getIP(wpnData.pos, wpnData.dir, 50)
		else -- wpn no longer exists, must be dead.
          if clusterWeaps[wpnData.name] then
            if wpnData.init then
              if explTable[wpnData.name] then
                --env.info(wpnData.init.." opened a cluster "..wpnData.name)
                tracked_clusters[wpnData.init] = { wpn = wpnData.name, init = wpnData.init, time = timer.getAbsTime() }
              end
            end
          else

--      trigger.action.outText("Weapon impacted, mass of weapon warhead is " .. wpnData.exMass, 2)
			local ip = land.getIP(wpnData.pos, wpnData.dir, lookahead(wpnData.speed))  -- terrain intersection point with weapon's nose.  Only search out 20 meters though.
			local impactPoint
			if not ip then -- use last calculated IP
				impactPoint = wpnData.pos
	--      	trigger.action.outText("Impact Point:\nPos X: " .. impactPoint.x .. "\nPos Z: " .. impactPoint.z, 2)
			else -- use intersection point
				impactPoint = ip
	--        trigger.action.outText("Impact Point:\nPos X: " .. impactPoint.x .. "\nPos Z: " .. impactPoint.z, 2)
			end
			--env.info("Weapon is gone") -- Got to here -- 
			--trigger.action.outText("Weapon Type was: ".. wpnData.name, 20)
			if explTable[wpnData.name] then
					--env.info("triggered explosion size: "..explTable[wpnData.name])
					trigger.action.explosion(impactPoint, explTable[wpnData.name])
					--trigger.action.smoke(impactPoint, 0)
			end
	      end
		  tracked_weapons[wpn_id_] = nil -- remove from tracked weapons first.         
		end
	end
--  env.info("Weapon Track End")
end

function onWpnEvent(event)
  if event.id == world.event.S_EVENT_SHOT then
    if event.weapon then
      local ordnance = event.weapon
      local weapon_desc = ordnance:getDesc()
      if (weapon_desc.category ~= 0) and event.initiator then
		if (weapon_desc.category == 1) then
			if (weapon_desc.MissileCategory ~= 1 and weapon_desc.MissileCategory ~= 2) then
				tracked_weapons[event.weapon.id_] = { wpn = ordnance, init = event.initiator:getName(), pos = ordnance:getPoint(), dir = ordnance:getPosition().x, name = ordnance:getTypeName(), speed = ordnance:getVelocity() }
			end
		else
			tracked_weapons[event.weapon.id_] = { wpn = ordnance, init = event.initiator:getName(), pos = ordnance:getPoint(), dir = ordnance:getPosition().x, name = ordnance:getTypeName(), speed = ordnance:getVelocity() }
		end
      end
    end
  elseif event.id == world.event.S_EVENT_HIT then
    if event.target and event.initiator and tracked_clusters[event.initiator:getName()] ~= nil then
      local weapon = tracked_clusters[event.initiator:getName()].wpn
      local shoot_time = tracked_clusters[event.initiator:getName()].time
      local flight_time = shell_max_flight_time
      if clusterWeaps[weapon] then
        flight_time = cluster_max_flight_time
      end
      if event.time > shoot_time + flight_time then
        -- Max shell flight time exceeded, remove from shooter array if exists
        --env.info("Removing "..event.initiator:getName().." from tracked submunitions")
        tracked_clusters[event.initiator:getName()] = nil -- remove from tracked submunitions
      end
      --env.info(weapon.." hit a target")
      if event.target then
        local impactPoint = event.target:getPosition().p
        if clusterEffectsEnable and explTable[weapon] then
          --env.info(weapon.." hit "..event.target:getTypeName())
          --env.info('Impact point was at: X: ' .. impactPoint.x .. ' Y: ' .. impactPoint.y .. ' Z: ' .. impactPoint.z)
          if clusterWeaps[weapon] then
            for i=1,clusterWeaps[weapon]
            do
              cluster_radius = math.random(0,cluster_munition_distribution_radius)
              cluster_angle = 2 * math.pi * (math.random())
              blastPoint = {
                x = impactPoint.x + cluster_radius * math.cos(cluster_angle),
                y = impactPoint.y,
                z = impactPoint.z + cluster_radius * math.sin(cluster_angle)
              }
              --env.info('Generating cluster bomb explosion at: X: ' .. blastPoint.x .. ' Y: ' .. blastPoint.y .. ' Z: ' .. blastPoint.z)
			  trigger.action.explosion(blastPoint, explTable[weapon])
            end
          else
			trigger.action.explosion(impactPoint, explTable[weapon])
          end
        end
      end
    end
  end
end

local function protectedCall(...)
  local status, retval = pcall(...)
  if not status then
    env.warning("Splash damage script error... gracefully caught! " .. retval, true)
  end
end


function WpnHandler:onEvent(event)
  protectedCall(onWpnEvent, event)
end

function weaponDamage(clusterEffects)
  env.info(string.format("Weapons Damage Mod running. Cluster munition damage updates enabled: %s",tostring(clusterEffects)))
  clusterEffectsEnable = clusterEffects

  timer.scheduleFunction(function()
      protectedCall(track_wpns)
      return timer.getTime() + refreshRate
    end, 
    {}, 
    timer.getTime() + refreshRate
  )
  world.addEventHandler(WpnHandler)
end
