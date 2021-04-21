--[[
Export script for LotATC drawings

Allows to export certain DCS Liberation objects as predefined drawing in LotATC. 

This script runs at mission startup and generates a drawing JSON file to be imported
in LotATC.
]]

LotAtcExportConfig = {
    ["exportRedAA"] = false,
    ["exportBlueAA"] = false,
    ["exportSymbols"] = false,
    ["exportVersion"] = "2.2.0",
    ["drawingBasePath"] = nil,
    ["redColor"] = "#7FE32000",
    ["blueColor"] = "#7F0084FF"
}

local function factionName(isFriend)
    if isFriend then
        return "BLUE"
    else
        return "RED"
    end
end

local function uuid()
    local random = math.random
    local template ='xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
    return string.gsub(template, '[xy]', function (c)
        local v = (c == 'x') and random(0, 0xf) or random(8, 0xb)
        return string.format('%x', v)
    end)
end

local function ends_with(str, ending)
    return ending == "" or str:sub(-#ending) == ending
 end

local function combine(path1, path2)
    if not ends_with(path1, "\\") then
        path1 = path1 .. "\\"
    end

    return path1 .. path2
end

local function lotatcExport_get_aa_nato_name(unit, isFriend)
    if not redIADS or not blueIADS then
        return nil
    end

    -- logger:info(string.format("DCSLiberation|LotATC Export plugin - try get NATO name for unit %s", unit.dcsGroupName))

    local iads = redIADS
    if isFriend then
        iads = blueIADS
    end

    local samSite = iads:getSAMSiteByGroupName(unit.dcsGroupName)
    if samSite and samSite.natoName then
        -- logger:info(string.format("DCSLiberation|LotATC Export plugin - NATO name is %s", samSite.natoName))
        return samSite.natoName
    else
        return nil
    end
end

local function lotatcExport_get_name(unit, isFriend)
    local classification = "SAM"

    if string.find(unit.dcsGroupName, "|EWR|", 1, true) then
        classification = "EWR"
    elseif string.find(unit.dcsGroupName, "|AA", 1, true) then
        classification = "AAA"
    end

    local natoName = lotatcExport_get_aa_nato_name(unit, isFriend)

    local name = nil
    if not natoName then
        name = string.format("%s|%s", unit.name, classification)
    else
        name = string.format("%s|%s|%s", unit.name, classification, natoName)
    end

    return name, classification
end

local function lotatc_write_json(filename, json)
    logger:info(string.format("DCSLiberation|LotATC Export plugin - writing %s", filename))

    local function Write()
        local fp = io.open(filename, 'w')
        if fp then
            fp:write(json)
            fp:close()
        end
    end

    if pcall(Write) then
    else
        logger:error("Unable to write LotATC export file to %s", filename)
    end
end

local function lotatcExport_threat_circles_for_faction(faction, color, isFriend)
    local drawings = {}

    for _,aa in pairs(faction) do
        logger:info(string.format("DCSLiberation|LotATC Export plugin - exporting threat circle for %s", aa.dcsGroupName))

        local convLat, convLon = coord.LOtoLL({x = aa.positionX, y = 0, z = aa.positionY})

        local name = lotatcExport_get_name(aa, isFriend)

        table.insert(drawings,
        {
            ["author"] = "DCSLiberation",
            ["brushStyle"] = 1,
            ["color"] = color,
            ["colorBg"] = "#00000000",
            ["id"] = string.format("{%s}", uuid()),
            ["longitude"] = convLon,
            ["latitude"] = convLat,
            ["radius"] = tonumber(aa.range),
            ["lineWidth"] = 2,
            ["name"] = name,
            ["shared"] = true,
            ["timestamp"] = "",
            ["type"] = "circle",
            ["text"] = name,
            ["font"] = {
                ["color"] = color,
                ["font"] = "Lato"
            }
        })
    end

    local lotatcData = {
        ["name"] = "Threat Circles " .. factionName(isFriend),
        ["enable"] = "true",
        ["version"] = LotAtcExportConfig.exportVersion,
        ["drawings"] = drawings
    }

    local drawings_json = json:encode(lotatcData)
    return drawings_json
end

local function lotatcExport_symbols_for_faction(faction, color, isFriend)
    local drawings = {}

    for _,aa in pairs(faction) do
        logger:info(string.format("DCSLiberation|LotATC Export plugin - exporting AA symbol for %s", aa.dcsGroupName))

        local convLat, convLon = coord.LOtoLL({x = aa.positionX, y = 0, z = aa.positionY})

        local name = lotatcExport_get_name(aa, isFriend)

        local classification = "hostile"
        if isFriend then
            classification = "friend"
        end

        local sub_dimension = "none"

        if string.find(aa.dcsGroupName, "|EWR|", 1, true) then
            sub_dimension = "ew"
        end

        table.insert(drawings,
        {
            ["author"] = "DCSLiberation",
            ["brushStyle"] = 1,
            ["classification"] = {
                ["classification"] = classification,
                ["dimension"] = "land_unit",
                ["sub_dimension"] = sub_dimension
            },
            ["color"] = color,
            ["colorBg"] = "#33FF0000",
            ["font"] = {
                ["color"] = color,
                ["font"] = "Lato"
            },
            ["id"] = string.format("{%s}", uuid()),
            ["longitude"] = convLon,
            ["latitude"] = convLat,
            ["lineWidth"] = 2,
            ["name"] = name,
            ["shared"] = true,
            ["timestamp"] = "",
            ["type"] = "symbol",
            ["text"] = name
        })
    end

    local lotatcData = {
        ["name"] = "Threat Symbols " .. factionName(isFriend),
        ["enable"] = "true",
        ["version"] = LotAtcExportConfig.exportVersion,
        ["drawings"] = drawings,
    }

    local drawings_json = json:encode(lotatcData)
    return drawings_json
end

local function lotatc_export_faction(faction, color, factionPath, isFriend)
    local exportBasePathFaction = combine(LotAtcExportConfig.drawingBasePath, factionPath)
    lfs.mkdir(exportBasePathFaction)

    local exportFileName = combine(exportBasePathFaction, "threatZones.json")
    local json = lotatcExport_threat_circles_for_faction(faction, color, isFriend)
    lotatc_write_json(exportFileName, json)

    if LotAtcExportConfig.exportSymbols then
        exportFileName = combine(exportBasePathFaction, "threatSymbols.json")
        json = lotatcExport_symbols_for_faction(faction, color, isFriend);
        lotatc_write_json(exportFileName, json)
    end
end

function LotatcExport()

    if not json then
        local message = "Unable to export LotATC drawings, JSON library is not loaded!"
        logger:error(message)
        return
    end

    if not LotAtcExportConfig.drawingBasePath then
        local message = "No writable export path for LotATC drawings. Set environment variable LOTATC_DRAWINGS_DIR pointing to your export path."
        logger:error(message)
        return
    end

    local message = "Export LotATC drawings to "..LotAtcExportConfig.drawingBasePath
    logger:info(message)

    -- The RED AA is exported to the blue folder and vice versa. If a BLUE GCI connects he/she
    -- wants to see the RED AA.

    if LotAtcExportConfig.exportRedAA then
        lotatc_export_faction(dcsLiberation.RedAA, LotAtcExportConfig.redColor, [[blue\]], false)
    end

    if LotAtcExportConfig.exportBlueAA then
        lotatc_export_faction(dcsLiberation.BlueAA, LotAtcExportConfig.blueColor, [[red\]], true)
    end
end
