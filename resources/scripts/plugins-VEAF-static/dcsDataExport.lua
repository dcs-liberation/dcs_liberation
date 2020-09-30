-- execute(dofile) this script at the end of
-- of 'DCS World\MissionEditor\modules\me_mission.lua'
-- base.dofile("d:\\dev\\VEAF-Mission-Creation-Tools\\scripts\\community\\dcsDataExport.lua")

-------------------------------------------------------------------------------
-- settings
-------------------------------------------------------------------------------

--local export_path = [[c:\Users\dpier\Saved Games\DCS.openbeta\Logs\ObjectDB\]]
local export_path = [[.\]]

-------------------------------------------------------------------------------
-- helper functions
-------------------------------------------------------------------------------

local function writeln(file, text)
    file:write(text.."\r\n")
end

local function safe_name(name)
    local safeName = name
    safeName = string.gsub(safeName, "[-()/., *'+`#%[%]]", "_")
    safeName = string.gsub(safeName, "_*$", "")  -- strip __ from end
    safeName = string.gsub(safeName, "^([0-9])", "_%1")
    if safeName == 'None' then
        safeName = 'None_'
    end
    return safeName
end

local function has_value (tab, val)
    for index, value in ipairs(tab) do
        if value == val then
            return true
        end
    end

    return false
end

mist = {}
mist.utils = {}

--- Serializes the give variable to a string.
-- borrowed from slmod
-- @param var variable to serialize
-- @treturn string variable serialized to string
function mist.utils.basicSerialize(var)
    if var == nil then
        return "\"\""
    else
        if ((type(var) == 'number') or
                (type(var) == 'boolean') or
                (type(var) == 'function') or
                (type(var) == 'table') or
                (type(var) == 'userdata') ) then
            return tostring(var)
        elseif type(var) == 'string' then
            var = string.format('%q', var)
            return var
        end
    end
end

--- Serialize value
-- borrowed from slmod (serialize_slmod)
-- @param name
-- @param value value to serialize
-- @param level
function mist.utils.serialize(name, value, level)
	--Based on ED's serialize_simple2
	local function basicSerialize(o)
		if type(o) == "number" then
			return tostring(o)
		elseif type(o) == "boolean" then
			return tostring(o)
		else -- assume it is a string
			return mist.utils.basicSerialize(o)
		end
	end

	local function serializeToTbl(name, value, level)
		local var_str_tbl = {}
		if level == nil then
			level = ""
		end
		if level ~= "" then 
			level = level.."" 
		end
		table.insert(var_str_tbl, level .. name .. " = ")

		if type(value) == "number" or type(value) == "string" or type(value) == "boolean" then
			table.insert(var_str_tbl, basicSerialize(value) ..	",\n")
		elseif type(value) == "table" then
			table.insert(var_str_tbl, "\n"..level.."{\n")

			for k,v in pairs(value) do -- serialize its fields
				local key
				if type(k) == "number" then
					key = string.format("[%s]", k)
				else
					key = string.format("[%q]", k)
				end
				table.insert(var_str_tbl, mist.utils.serialize(key, v, level.."	"))

			end
			if level == "" then
				table.insert(var_str_tbl, level.."} -- end of "..name.."\n")

			else
				table.insert(var_str_tbl, level.."}, -- end of "..name.."\n")

			end
		else
			log:error('Cannot serialize a $1', type(value))
		end
		return var_str_tbl
	end

	local t_str = serializeToTbl(name, value, level)

	return table.concat(t_str)
end

local function _sortUnits(u1,u2)
    if u1 and u1.category and u2 and u2.category then
        if string.lower(u1.category) == string.lower(u2.category) then 
            if u1 and u1.name and u2 and u2.name then
                return string.lower(u1.name) < string.lower(u2.name)
            else
                return string.lower(u1) < string.lower(u2)
            end
        else
            return string.lower(u1.category) < string.lower(u2.category)
        end
    else
        return string.lower(u1) < string.lower(u2)
    end
end

local function browseUnits(out, database, defaultCategory, fullDcsUnit)
    for _, unit in pairs(database) do
        if fullDcsUnit then
            out[unit["type"]] = unit
        else
            out[unit["type"]] = {}
            local u = out[unit["type"]]
            u.category = unit["category"]
            if not u.category then 
                u.category = defaultCategory
            end
            u.type = unit["type"]
            u.name = unit["Name"]
            u.description = unit["DisplayName"]
            u.aliases = {}
            if unit["Aliases"] then 
                for _, alias in pairs(unit["Aliases"]) do
                    table.insert(u.aliases, alias)
                end
            end
            if unit["attribute"] then
                for _, attr in pairs(unit["attribute"]) do
                    if type(attr) == "string" then
                        if attr:lower() == "ships" then u.naval = true end
                        if attr:lower() == "air" then u.air = true end
                        if attr:lower() == "infantry" then u.infantry = true end
                        if attr:lower() == "vehicles" then u.vehicle = true end
                    end
                end
            end
        end
    end
end

local units = {}
local fullDcsUnit = false
browseUnits(units, db.Units.Planes.Plane, "Plane", fullDcsUnit)
browseUnits(units, db.Units.Helicopters.Helicopter, "Helicopter", fullDcsUnit)
browseUnits(units, db.Units.Cars.Car, "Vehicle", fullDcsUnit)
browseUnits(units, db.Units.Ships.Ship, "Ship", fullDcsUnit)
browseUnits(units, db.Units.Fortifications.Fortification, "Fortification", fullDcsUnit)
browseUnits(units, db.Units.GroundObjects.GroundObject, "GroundObject", fullDcsUnit)
browseUnits(units, db.Units.Warehouses.Warehouse, "Warehouse", fullDcsUnit)
browseUnits(units, db.Units.Cargos.Cargo, "Cargo", fullDcsUnit)
local values = {}
if fullDcsUnit then
    values = units    
else
    for _,v in pairs(units) do
        table.insert(values,v)
    end
    table.sort(values, _sortUnits)
end
local file = io.open(export_path.."units.lua", "w")
writeln(file, mist.utils.serialize("units", values))
file:close()
