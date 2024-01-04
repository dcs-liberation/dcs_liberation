# Hit Points Generator
The scripts in this folder creates/updates hit point data for units and static objects in DCS 
and updates the unit YAML files in Liberation.

# Usage

1. Run *mission.py*, which will generate a DCS mission file *hit_points_generator.miz* in the 
same folder as *mission.py*.
2. Run the mission *hit_points_generator.miz* in DCS, wait a few seconds and exit the mission. 
This mission should generate a file *hit_points_data.csv* in the same folder as *mission.py*.
This mission requires the sanitizing of the Lua *io* module to be commented out in 
MissionScripting.lua, but this should already be the case when running Liberation.
3. Run *update.py*, which will update the YAML files in Liberation's *resources* folder, adding 
the hit_points data if it does not exist or overwriting it if it does. Note that *update.py*
will need to be updated if the file location with the Liberation code is changed.
