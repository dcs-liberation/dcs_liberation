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
    ["basePath"] = dcsLiberation.savedGamesPath..[[\Mods\services\LotAtc\userdb\drawings\]],
    ["redColor"] = "#7FE32000",
    ["blueColor"] = "#7F0084FF"
}

local function uuid()
    local random = math.random
    local template ='xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
    return string.gsub(template, '[xy]', function (c)
        local v = (c == 'x') and random(0, 0xf) or random(8, 0xb)
        return string.format('%x', v)
    end)
end

local function lotatcExport_get_aa_nato_name(unit, isFriend)
    if not redIADS or not blueIADS then
        return nil
    end

    env.info(string.format("DCSLiberation|LotATC Export plugin - try get NATO name for unit %s", unit.dcsGroupName))

    local iads = redIADS
    if isFriend then
        iads = blueIADS
    end

    local samSite = iads:getSAMSiteByGroupName(unit.dcsGroupName)
    if samSite and samSite.natoName then
        env.info(string.format("DCSLiberation|LotATC Export plugin - NATO name is %s", samSite.natoName))
        return samSite.natoName
    else
        return nil
    end
end

local function lotatcExport_get_name(unit, isFriend)
    local classification = "SAM"

    if string.find(unit.dcsGroupName, "|EWR|", 1, true) then
        classification = "EWR"
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
    env.info(string.format("DCSLiberation|LotATC Export plugin - writing %s", filename))
    local fp = io.open(filename, 'w')
    if fp then
        fp:write(json)
        fp:close()
    end
end

local function lotatcExport_threat_circles_for_faction(faction, color, isFriend)
    local drawings = {}

    for _,aa in pairs(faction) do
        env.info(string.format("DCSLiberation|LotATC Export plugin - exporting threat circle for %s", aa.dcsGroupName))

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
        ["enabled"] = "true",
        ["version"] = LotAtcExportConfig.exportVersion,
        ["drawings"] = drawings
    }

    local drawings_json = json:encode(lotatcData)
    return drawings_json
end

local function lotatcExport_symbols_for_faction(faction, color, isFriend)
    local drawings = {}

    for _,aa in pairs(faction) do
        env.info(string.format("DCSLiberation|LotATC Export plugin - exporting AA symbol for %s", aa.dcsGroupName))

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
        ["enabled"] = "true",
        ["version"] = LotAtcExportConfig.exportVersion,
        ["drawings"] = drawings
    }

    local drawings_json = json:encode(lotatcData)
    return drawings_json
end

local function lotatc_export_faction(faction, color, faction_path, isFriend)
    local exportBasePathFaction = LotAtcExportConfig.basePath..faction_path
    lfs.mkdir(exportBasePathFaction)

    local exportFileName = exportBasePathFaction.."threatZones.json"
    local json = lotatcExport_threat_circles_for_faction(faction, color, isFriend);
    lotatc_write_json(exportFileName, json)

    if LotAtcExportConfig.exportSymbols then
        exportFileName = exportBasePathFaction.."threatSymbols.json"
        json = lotatcExport_symbols_for_faction(faction, color, isFriend);
        lotatc_write_json(exportFileName, json)
    end
end

function LotatcExport()

    if not json then
        local message = "Unable to export LotATC drawings, JSON library is not loaded!"
        logger:error(message)
        messageAll(message)
    end

    if LotAtcExportConfig.exportRedAA then
        lotatc_export_faction(dcsLiberation.RedAA, LotAtcExportConfig.redColor, [[red\]], false)
    end

    if LotAtcExportConfig.exportBlueAA then
        lotatc_export_faction(dcsLiberation.BlueAA, LotAtcExportConfig.blueColor, [[blue\]], true)
    end
end
