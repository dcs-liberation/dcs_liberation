# 2.1.0

## Features/Improvements :

* **[Campaign Generator]** Added Syria map support
* **[Campaign Generator]** Added 4 campaigns for the Syria map
* **[Campaign Generator]** Added 2 smaller scale campaign for Persian Gulf map
* **[Units/Factions]** Added factions for Syria map : Syria 2011, Arab Armies 1973,1968,1948, Israel 1973, 1948
* **[Base Menu]** Budget is visible in recruitment menu. (Thanks to Github contributor root0fall)
* **[Misc]** Added error message in mission when state file can not be written.


## Fixed issues :

* **[Mission Generator]** Caucasus terrain improvement on exclusions zone (added forests between Vaziani and Beslan to exlusion zones)

# 2.0.11

## Features/Improvements :

* **[Units/Factions]** Added Mig-31, Su-30, Mi-24V, Mi-28N to Russia 2010 faction.
* **[Units/Factions]** Added F-15E to USA 2005 and USA 1990 factions.
* **[Mission Generator]** Added a parameter to choose whether the JTACs should use smoke markers or not

## Fixed issues : 

* **[Units/Factions]** Fixed big performance issue in new release UI that occurred only when running the .exe
* **[Units/Factions]** Fixed mission generation not working with Libya faction
* **[Units/Factions]** Fixed OH-58D not being used by AI
* **[Units/Factions]** Typo in UK 1990 name (fixed by bwRavencl)
* **[Units/Factions]** Fixed Tanker Tacan channel not being the same as the briefing one. (Sorry)
* **[Mission Generator]** Neutral airbases services will now be disabled. (Not possible to refuel or re-arm there)
* **[Mission Generator]** AI will be configured to limit afterburner usage
* **[Mission Generator]** JTAC will not use laser codes above 1688 anymore
* **[Mission Generator]** JTAC units were misconfigured and would not be invisible/immortal. 
* **[Mission Generator]** Increased JTAC status message duration to 25s, so you have more time to enter coordinates;
* **[Mission Generator]** Destroyed units carcass will not appear on airfields to avoid having a destroyed vehicle blocking a runway or taxiway.


# 2.0.10

## Features/Improvements :
* **[Misc]** Now possible to save game in a different file, and to open DCS Liberation savegame files. (You are not restricted to a single save file anymore)
* **[UI/UX]** New dark UI Theme and default theme improvement by Deus
* **[UI/UX]** New "satellite" map backgrounds
* **[UX]** Base menu is opened with a single mouse click
* **[Units/Factions/Mods]** Added Community A-4E-C support for faction Bluefor Cold War
* **[Units/Factions/Mods]** Added MB-339PAN support for faction Bluefor Cold War  
* **[Units/Factions/Mods]** Added Rafale AI mod support
* **[Units/Factions/Mods]** Added faction "France Modded" with units from frenchpack v3.5 mod
* **[Units/Factions/Mods]** Added faction "Insurgent modded" with Insurgent units from frenchpack v3.5 mod (Toyota truck)
* **[Units/Factions/Mods]** Added factions Canada 2005, Australia 2005, Japan 2005, USA Aggressors, PMC
* **[New Game Wizard]** Added the list of required mods for modded factions.
* **[New Game Wizard]** No more RED vs BLUE opposing faction restrictions.
* **[New Game Wizard]** New campaign generation settings added : No aircraft carrier, no lha, no navy, invert map starting positions.
* **[Mission Generator]** Artillery units will start firing mission after a random delay. It should reduces lag spikes induced by artillery strikes by spreading them out.
* **[Mission Generator]** Ground units will retreat after taking too much casualties. Artillery units will retreat if engaged.
* **[Mission Generator]** The briefing will now contain the carrier ATC frequency
* **[Mission Generator]** The briefing contains a small situation update.
* **[Mission Generator]** Previously destroyed units are visible in the mission. (And added a performance settings to disable this behaviour)
* **[Mission Generator]*c* Basic JTAC on Frontlines
* **[Campaign Generator]** Added Tarawa in caucasus campaigns
* **[Campaign Generator]** Tuned the various existing campaign parameters
* **[Campaign Generator]** Added small campaign : "Russia" on Caucasus Theater 

## Fixed issues :
* **[Mission Generator]** Carrier will sail into the wind, not in the same direction
* **[Mission Generator]** Carrier cold start was not working (flight was starting warm even when cold was selected)
* **[Mission Generator]** Carrier group ships are more spread out
* **[Mission Generator]** Fixed wrong radio frequency for german WW2 warbirds
* **[Mission Generator]** Fixed FW-190A8 spawning with bomb rack for CAP missions
* **[Mission Generator]** Fixed A-20G spawning with no payload
* **[Mission Generator]** Fixed Su-33 spawning too heavy to take off from carrier
* **[Mission Generator]** Fixed Harrier AV-8B spawning too heavy to take off from tarawa
* **[Mission Generator]** Base defense units were not controllable with Combined Arms
* **[Mission Generator]** Tanker speed was too low
* **[Mission Generator]** Tanker TACAN settings were wrong
* **[Mission Generator]** AI aircraft should start datalink ON (EPLRS)
* **[Mission Generator]** Base defense units should not spawn on runway and or taxyway. (The chance for this to happen should now be really really low)
* **[Mission Generator]** Fixed all flights starting "In flight" after playing a few missions (parking slot reset issue)
* **[Mission Script/Performance]** Mission lua script will not listen to weapons fired event anymore and register every fired weapons. This should improve performance especially in WW2 scenarios or when rocket artillery is firing. 
* **[Campaign Generator]** Carrier name will now not appear for faction who do not have carriers
* **[Campaign Generator]** SA-10 sites will now have a tracking radar.
* **[Units/Factions]** Remove JF-17 from USA 2005 faction
* **[Units/Factions]** Remove AJS-37 from Russia 2010
* **[Units/Factions]** Removed Oliver Hazard Perry from cold war factions (too powerful sam system for the era)
* **[Bug]** On the persian gulf full map campaign, the two carriers were sharing the same id, this was causing a lot of bugs
* **[Performance]** Tuned the culling setting so that you cannot run into situation where no friendly or enemy AI flights are generated
* **[Other]** Application doesn't gracefully exit.
* **[Other]** Other minor fixes, and multiples factions small changes

# 2.0 RC 9

## Features/Improvements :
* **[UI/UX]** New icons from contributor Deus

## Fixed issues :
* **[Mission Generator]** Carrier TACAN was wrongfully set up as an A/A TACAN
* **[Campaign Generator]** Fixed issue with Russian navy group generator causing a random crash on campaign creation.

# 2.0 RC 8

## Fixed issues :
* **[Mission Generator]** Frequency for P-47D-30 changed to 124Mhz (Generated mission with 251Mhz would not work)
* **[Mission Generator]** Reduced the maximum number of uboat per generated group
* **[Mission Generator]** Fixed an issue with the WW2 LST groups (superposed units).
* **[UI]** Fixed issue with the zoom

# 2.0 RC 7

## Features/Improvements :

* **[Units/Factions]** Added P-47D-30 for factions allies_1944
* **[Units/Factions]** Added factions : Bluefor Coldwar, Germany 1944 Easy

* **[Campaign/Map]** Added a campaign in the Channel map
* **[Campaign/Map]** Changed the Normandy campaign map
* **[Campaign/Map]** Added new campaign Normandy Small

* **[Mission Generator]** AI Flight generator has been reworked
* **[Mission Generator]** Add PP points for JF-17 on STRIKE missions
* **[Mission Generator]** Add ST point for F-14B on STRIKE missions
* **[Mission Generator]** Flights with client slots will never be delayed
* **[Mission Generator]** AI units can start from parking (With a new setting in Settings Window to disable it)
* **[Mission Generator]** Tacan for carrier will only be in Mode X from now
* **[Mission Generator]** RTB waypoints for autogenerated flights

* **[Flight Planner]** Added CAS mission generator
* **[Flight Planner]** Added CAP mission generator
* **[Flight Planner]** Added SEAD mission generator
* **[Flight Planner]** Added STRIKE mission generator
* **[Flight Planner]** Added buttons to add autogenerated waypoints (ASCEND, DESCEND, RTB)
* **[Flight Planner]** Improved waypoint list
* **[Flight Planner]** WW2 factions uses different parameters for flight planning.

* **[Settings]** Added settings to disallow external views
* **[Settings]** Added settings to choose F10 Map mode (All, Allies only, Player only, Fog of War, Map Only)
* **[Settings]** Added settings to choose whether to auto-generate objective marks on the F10 map

* **[Info Panel]** Added information about destroyed buildings in info panel
* **[Info Panel]** Added information about destroyed units at SAM site in info panel
* **[Debriefing]** Added information about units destroyed outside the frontline in the debriefing window
* **[Debriefing]** Added destroyed buildings in the debriefing window

* **[Map]** Tooltip now contains the list of building for Strike targets on the map
* **[Map]** Added "Oil derrick" building
* **[Map]** Added "ww2 bunker" building (WW2)
* **[Map]** Added "ally camp" building (WW2)
* **[Map]** Added "V1 Site" (WW2)

* **[Misc]** Made it possible to setup DCS Saved Games directory and DCS installation directory manually at first start
* **[Misc]** Added culling performance settings 

## Fixed issues :

* **[Units/Factions]** Replaced S3-B Tanker by KC130 for most factions (More fuel)
* **[Units/Factions]** WW2 factions will not have offshore oil station and other modern buildings generated. No more third-reich operated offshore stations will spawn on normandy's coast. 
* **[Units/Factions]** Aircraft carrier will try to move in the wind direction
* **[Units/Factions]** Missing icons added for some aircraft

* **[Mission Generator]** When playing as RED the activation trigger would not be properly generated
* **[Mission Generator]** FW-190A8 is now properly considered as a flyable aircraft
* **[Mission Generator]** Changed "strike" payload for Su-24M that was ineffective
* **[Mission Generator]** Changed "strike" payload for JF-17 to use LS-6 bombs instead of GBU
* **[Mission Generator]** Change power station template. (Buildings could end up superposed).

* **[Maps/Campaign]** Now using Vasiani airbase instead of Soganlung airport in Caucasus campaigns (more parking slot)
* **[Info Panel]** Message displayed on base capture event stated that the enemy captured an airbase, while it was the player who captured it.
* **[Map View]** Graphical glitch on map when one building of an objective was destroyed, but not the others 
* **[Mission Planner]** The list of flights was not updated on departure time change. 


# 2.0 RC 6

Saves file from RC5 are not compatible with the new version. 
Sorry :(

## Features/Improvements :
* **[Units/Factions]** Supercarrier support (You have to go to settings to enable it, if you have the supercarrier module)
* **[Units/Factions]** Added 'Modern Bluefor' factions, containing all most popular DCS flyable units
* **[Units/Factions]** Factions US 2005 / 1990 will now sometimes have Arleigh Burke class ships instead of Perry as carrier escorts 
* **[Units/Factions]** Added support for newest WW2 Units
* **[Campaign logic]** When a base is captured, refill the "base defenses" group with units for the new owner.
* **[Mission Generator]** Carrier ICLS channel will now be configured (check your briefing)
* **[Mission Generator]** SAM units will spawn on RED Alarm state
* **[Mission Generator]** AI Flight planner now creates its own STRIKE flights
* **[Mission Generator]** AI units assigned to Strike flight will now actually engage the buildings they have been assigned.
* **[Mission Generator]** Added performance settings to allow disabling : smoke, artillery strike, moving units, infantry, SAM Red alert mode.
* **[Mission Generator]** Using Late Activation & Trigger in attempt to improve performance & reduce stutter (Previously they were spawned through 'ETA' feature)
* **[UX]** : Improved flight selection behaviour in the Mission Planning Window
 
## Fixed issues :
* **[Mission Generator]** Payloads were not correctly assigned in the release version. 
* **[Mission Generator]** Game generation does not work when "no night mission" settings was selected and the current time was "day"
* **[Mission Generator]** Game generation does not work when the player selected faction has no AWACS
* **[Mission Generator]** Planned flights will spawn even if their home base has been captured or is being contested by enemy ground units. 
* **[Campaign Generator]** Base defenses would not be generated on Normandy map and in some rare cases on others maps as well
* **[Mission Planning]** CAS waypoints created from the "Predefined waypoint selector" would not be at the exact location of the frontline
* **[Naming]** CAP mission flown from airbase are not named BARCAP anymore (CAP from carrier is still named BARCAP)