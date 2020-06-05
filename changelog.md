#2.0 RC 7

##Features/Improvements :
* **[Units/Factions]** Added P-47D-30 for factions allies_1944
* **[Mission Generator]** CAP flights have been slightly reworked
* **[Mission Generator]** Add PP points for JF-17 on STRIKE missions
* **[Mission Generator]** Add ST point for F-14B on STRIKE missions
* **[Mission Generator]** Flights with client slots will never be delayed
* **[Mission Generator]** AI units can start from parking

##Fixed issues :
* **[Mission Generator]** When playing as RED the activation trigger would not be properly generated
* **[Mission Generator]** Changed "strike" payload for Su-24M
* **[Mission Generator]** FW-190A8 is now properly considered as flyable

#2.0 RC 6

Saves file from RC5 are not compatible with the new version. 
Sorry :(

##Features/Improvements :

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
 
##Fixed issues :

* **[Mission Generator]** Payloads were not correctly assigned in the release version. 
* **[Mission Generator]** Game generation does not work when "no night mission" settings was selected and the current time was "day"
* **[Mission Generator]** Game generation does not work when the player selected faction has no AWACS
* **[Mission Generator]** Planned flights will spawn even if their home base has been captured or is being contested by enemy ground units. 
* **[Campaign Generator]** Base defenses would not be generated on Normandy map and in some rare cases on others maps as well
* **[Mission Planning]** CAS waypoints created from the "Predefined waypoint selector" would not be at the exact location of the frontline
* **[Naming]** CAP mission flown from airbase are not named BARCAP anymore (CAP from carrier is still named BARCAP)
