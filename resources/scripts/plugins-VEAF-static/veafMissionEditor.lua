-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- VEAF mission editor tool for DCS World
-- By zip (2020)
--
-- Features:
-- ---------
-- * This tool can read a mission file, apply filters on it and spit it back.
--
-- Prerequisite:
-- ------------
-- * The mission file archive must already be exploded
-- TODO
--
-- Basic Usage:
-- ------------
-- TODO
--
-------------------------------------------------------------------------------------------------------------------------------------------------------------

veafMissionEditor = {}

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Global settings. Stores the script constants
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Identifier. All output in the log will start with this.
veafMissionEditor.Id = "MISSION EDITOR - "

--- Version.
veafMissionEditor.Version = "1.1.0"

-- trace level, specific to this module
veafMissionEditor.Debug = false
veafMissionEditor.Trace = false

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Do not change anything below unless you know what you are doing!
-------------------------------------------------------------------------------------------------------------------------------------------------------------


-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Utility methods
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafMissionEditor.logError(message)
    print(veafMissionEditor.Id .. message)
end

function veafMissionEditor.logInfo(message)
    print(veafMissionEditor.Id .. message)
end

function veafMissionEditor.logDebug(message)
  if message and veafMissionEditor.Debug then 
    print(veafMissionEditor.Id .. message)
  end
end

function veafMissionEditor.logTrace(message)
  if message and veafMissionEditor.Trace then 
    print(veafMissionEditor.Id .. message)
  end
end

local function _sortNumberOrCaseInsensitive(a,b)
  if type(a) == "string" or type(b) == "string" then
    return string.lower(a) < string.lower(b)
  else
    return a < b
  end
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Core methods
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafMissionEditor.serialize(name, value, level)
  -- mostly based on slMod serializer 

  local function _basicSerialize(s)
    if s == nil then
      return "\"\""
    else
      if ((type(s) == 'number') or (type(s) == 'boolean') or (type(s) == 'function') or (type(s) == 'table') or (type(s) == 'userdata') ) then
        return tostring(s)
      elseif type(s) == 'string' then
        return string.format('%q', s)
      end
    end	
  end

  -----Based on ED's serialize_simple2
  local basicSerialize = function(o)
      if type(o) == "number" then
          return tostring(o)
      elseif type(o) == "boolean" then
          return tostring(o)
      else -- assume it is a string
          return _basicSerialize(o)
      end
  end

  local serialize_to_t = function(name, value, level)
      ----Based on ED's serialize_simple2

      local var_str_tbl = {}
      if level == nil then
          level = ""
      end
      if level ~= "" then
          level = level .. "  "
      end

      table.insert(var_str_tbl, level .. name .. " = ")

      if type(value) == "number" or type(value) == "string" or type(value) == "boolean" then
          table.insert(var_str_tbl, basicSerialize(value) .. ",\n")
      elseif type(value) == "table" then
          table.insert(var_str_tbl, "{\n")
          local tkeys = {}
          -- populate the table that holds the keys
          for k in pairs(value) do table.insert(tkeys, k) end
          -- sort the keys
          table.sort(tkeys, _sortNumberOrCaseInsensitive)
          -- use the keys to retrieve the values in the sorted order
          for _, k in ipairs(tkeys) do  -- serialize its fields
            local v = value[k]
              local key
              if type(k) == "number" then
                  key = string.format("[%s]", k)
              else
                  key = string.format("[%q]", k)
              end

              table.insert(var_str_tbl, veafMissionEditor.serialize(key, v, level .. "  "))
          end
          if level == "" then
              table.insert(var_str_tbl, level .. "} -- end of " .. name .. "\n")
          else
              table.insert(var_str_tbl, level .. "}, -- end of " .. name .. "\n")
          end
      else
          veafMissionEditor.logError("Cannot serialize a " .. type(value))
      end
      return var_str_tbl
  end

  local t_str = serialize_to_t(name, value, level)

  return table.concat(t_str)
end

--- Reads a mission file
function veafMissionEditor.readMissionFile(filePath, tableName)
    local file = assert(loadfile(filePath))
    if not file then
        veafMissionEditor.logError(string.format("Error while loading mission file [%s]",filePath))
        return
    end
    
    file()
    returner = loadstring("return "..tableName)
    local table = returner()
    return table
end

--- Processes a mission object
function veafMissionEditor.processMission(mission)
    return mission -- do nothing
end

function veafMissionEditor.writeMissionFile(filePath, tableAsLua)
    local file, e = io.open(filePath, "w+");
    if not file then
        veafMissionEditor.logError(string.format("Error while writing mission to file [%s]",filePath))
        return error(e);
    end

    --file:write(string.format("%s = \n%s",tableName, tableAsLua))
    file:write(tableAsLua)
    file:close();
end

function veafMissionEditor.editMission(inFilePath, outFilePath, tableName, processFunction)
    local _processFunction = processFunction
    if not _processFunction then 
        _processFunction = veafMissionEditor.processMission
    end

    veafMissionEditor.logDebug(string.format("Reading lua table from [%s]",inFilePath))
    local table = veafMissionEditor.readMissionFile(inFilePath, tableName)
    veafMissionEditor.logDebug("Processing lua table")
    table = _processFunction(table)
    veafMissionEditor.logDebug("Exporting table as lua")
    local tableAsLua = veafMissionEditor.serialize(tableName, table)
    veafMissionEditor.logDebug(string.format("Writing lua table to [%s]",outFilePath))
    veafMissionEditor.writeMissionFile(outFilePath, tableAsLua)
end

