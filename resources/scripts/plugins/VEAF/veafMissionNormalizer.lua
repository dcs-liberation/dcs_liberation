-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- VEAF mission normalizer tool for DCS World
-- By Zip (2020)
--
-- Features:
-- ---------
-- This tool processes all files in a mission, apply filters to normalize them and writes them back.
-- Usually, DCSW Mission Editor shuffles the data in the mission files each time the mission is saved, making it all but impossible to compare with a previous version.
-- With this tool, it becomes easy to compare mission files after an edition in DCS World Mission Editor.
--
-- Prerequisite:
-- ------------
-- * The mission file archive must already be exploded ; the script only works on the mission files, not directly on the .miz archive
--
-- Basic Usage:
-- ------------
-- The following workflow should be used :
-- * explode the mission (unzip it)
-- * run the normalizer on the exploded mission
-- * version the exploded mission files (save it, back it up, commit it to a source control system, whatever fits your routine)
-- * compile the mission (zip the exploded files again)
-- * edit the compiled mission with DCSW Mission Editor
-- * explode the mission (unzip it)
-- * run the normalizer on the exploded mission
-- * now you can run a comparison between the exploded mission and its previous version
--
-- Call the script by running it in a lua environment ; it needs the veafMissionEditor library, so the script working directory must contain the veafMissionEditor.lua file
--
-- veafMissionNormalizer.lua <mission folder path> [-debug|-trace]
--
-- Command line options:
-- * <mission folder path> the path to the exploded mission files (no trailing backslash)
-- * -debug if set, the script will output some information ; useful to find out which units were edited
-- * -trace if set, the script will output a lot of information : useful to understand what went wrong
--
-------------------------------------------------------------------------------------------------------------------------------------------------------------

veafMissionNormalizer = {}

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Global settings. Stores the script constants
-------------------------------------------------------------------------------------------------------------------------------------------------------------

--- Identifier. All output in the log will start with this.
veafMissionNormalizer.Id = "NORMALIZER - "

--- Version.
veafMissionNormalizer.Version = "1.1.0"

-- trace level, specific to this module
veafMissionNormalizer.Trace = false
veafMissionNormalizer.Debug = false

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Do not change anything below unless you know what you are doing!
-------------------------------------------------------------------------------------------------------------------------------------------------------------

veafMissionNormalizer.KeysToSortById = {}
veafMissionNormalizer.KeysToSortById["country"] = true

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Utility methods
-------------------------------------------------------------------------------------------------------------------------------------------------------------

function veafMissionNormalizer.logError(message)
  print(veafMissionNormalizer.Id .. message)
end

function veafMissionNormalizer.logInfo(message)
  print(veafMissionNormalizer.Id .. message)
end

function veafMissionNormalizer.logDebug(message)
  if message and veafMissionNormalizer.Debug then
    print(veafMissionNormalizer.Id .. message)
  end
end

function veafMissionNormalizer.logTrace(message)
  if message and veafMissionNormalizer.Trace then
    print(veafMissionNormalizer.Id .. message)
  end
end

-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Core methods
-------------------------------------------------------------------------------------------------------------------------------------------------------------
require("veafMissionEditor")

local function _sortTable(t, level)
  if level == nil then
    level = 0
  end

  -- this function sorts by the value of the "id" key
  local _sortById = function(a, b)
    if a and a["id"] then
      veafMissionNormalizer.logTrace(string.format("_sortById: a[id]=%s", tostring(a["id"])))
      local idA = a["id"]
      if type(idA) == "number" then
        idA = tonumber(idA)
      end
      if b and b["id"] then
        local idB = b["id"]
        if type(idB) == "number" then
          idB = tonumber(idB)
        end
        veafMissionNormalizer.logTrace(string.format("_sortById: b[id]=%s", tostring(b["id"])))
        return idA < idB
      else
        return false
      end
    else
      return false
    end
  end

  if (type(t) == "table") then
    -- recurse
    for key, value in pairs(t) do
      if veafMissionNormalizer.KeysToSortById[key] then
        local text = ""
        for i = 0, level do
          text = text .. "  "
        end
        veafMissionNormalizer.logDebug(string.format(text .. "sorting by id table [%s]", key))
        -- sort by id
        table.sort(value, _sortById)
      end
      _sortTable(value, level + 1)
    end
  end
end

function veafMissionNormalizer.normalizeMission(filePath)
  local dictionaryKeysThatAreActuallyUsed = {}
  local WHATS_IN_A_DICTIONARY_KEY = "DictKey_"
  local function _recursivelySearchForDictionaryKeysInTable(t, dictionaryKeys)
    for key, value in pairs(t) do
      if type(value) == "table" then
        _recursivelySearchForDictionaryKeysInTable(value, dictionaryKeys)
      elseif type(value) == "string" then
        if value:lower():sub(1, #WHATS_IN_A_DICTIONARY_KEY) == WHATS_IN_A_DICTIONARY_KEY:lower()  then
            dictionaryKeys[value:lower()] = value
        end
      end
    end
  end

  local function _processFunctionForMission(t)
    -- search for dictionary keys in the mission file
    _recursivelySearchForDictionaryKeysInTable(t, dictionaryKeysThatAreActuallyUsed)
    _sortTable(t)
    return t
  end

  local function _processFunctionForDictionary(t)
    -- only keep keys that have been referenced in dictionaryKeysThatAreActuallyUsed 
    local result = {}
    local nSkippedKeys = 0
    for key, value in pairs(t) do
      if dictionaryKeysThatAreActuallyUsed[key:lower()] then
        result[key] = value
      else
        veafMissionNormalizer.logDebug(string.format("removing unused dictionary key [%s]=%s" , key, tostring(value)))
        nSkippedKeys = nSkippedKeys + 1
      end
    end
    if nSkippedKeys > 0 then 
      veafMissionNormalizer.logInfo(string.format("removed %d unused keys from dictionary" , nSkippedKeys))
    end

    _sortTable(result)
    return result
  end


  -- normalize "mission" file
  local _filePath = filePath .. "\\mission"
  veafMissionEditor.editMission(_filePath, _filePath, "mission", _processFunctionForMission)

  -- normalize "dictionary" file
  _filePath = filePath .. "\\l10n\\DEFAULT\\dictionary"
  veafMissionEditor.editMission(_filePath, _filePath, "dictionary", _processFunctionForDictionary)

  -- normalize "warehouses" file
  _filePath = filePath .. "\\warehouses"
  veafMissionEditor.editMission(_filePath, _filePath, "warehouses")

  -- normalize "options" file
  -- _filePath = filePath .. "\\options"
  -- veafMissionEditor.editMission(_filePath, _filePath, "options")

  -- normalize "mapResource" file
  _filePath = filePath .. "\\l10n\\DEFAULT\\mapResource"
  veafMissionEditor.editMission(_filePath, _filePath, "mapResource")
end

veafMissionNormalizer.logDebug(string.format("#arg=%d", #arg))
local debug = false
local trace = false
for i = 0, #arg do
  veafMissionNormalizer.logDebug(string.format("arg[%d]=%s", i, arg[i]))
  if arg[i] and arg[i]:upper() == "-DEBUG" then
    debug = true
  end
  if arg[i] and arg[i]:upper() == "-TRACE" then
    trace = true
  end
end
if #arg < 1 then
  veafMissionNormalizer.logError("USAGE : veafMissionNormalizer.lua <mission folder path>")
  return
end
if debug or trace then
  veafMissionNormalizer.Debug = true
  veafMissionEditor.Debug = true
  if trace then
    veafMissionNormalizer.Trace = true
    veafMissionEditor.Trace = true
  end
else
  veafMissionNormalizer.Debug = false
  veafMissionEditor.Debug = false
  veafMissionNormalizer.Trace = false
  veafMissionEditor.Trace = false
end

local filePath = arg[1]
veafMissionNormalizer.normalizeMission(filePath)
