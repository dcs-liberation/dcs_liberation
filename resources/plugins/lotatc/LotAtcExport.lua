--[[
Export script for LotATC drawings

Allows to export certain DCS Liberation objects as predefined drawing in LotATC. 

This script runs at mission startup and generates a drawing JSON file to be imported
in LotATC.
]]

LotAtcExportConfig = {
    ["exportRedAA"] = true,
    ["exportBlueAA"] = false
}

function lotatcExport_for_faction(faction, color)
    local random = math.random
    local function uuid()
        local template ='xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
        return string.gsub(template, '[xy]', function (c)
            local v = (c == 'x') and random(0, 0xf) or random(8, 0xb)
            return string.format('%x', v)
        end)
    end

    drawings = {}

    for _,aa in pairs(faction) do
        env.info(string.format("DCSLiberation|LotATC Export plugin - exporting %s", aa.dcsGroupName))

        local convLat, convLon = coord.LOtoLL({x = aa.positionX, y = 0, z = aa.positionY})

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
            ["name"] = string.format("%s|%s", aa.name, aa.dcsGroupName),
            ["shared"] = True,
            ["timestamp"] = "",
            ["type"] = "circle",
            ["text"] = string.format("%s|%s", aa.name, aa.dcsGroupName),
            ["font"] = {
                ["color"] = color,
                ["font"] = "Lato"
            }
        })
    end

    lotatcData = {
        ["enabled"] = "true",
        ["version"] = "2.2.0",
        ["drawings"] = drawings
    }
    
    local drawings_json = json:encode(lotatcData)
    return drawings_json
end

function lotatcExport()

    if not json then
        local message = "Unable to export LotATC drawings, JSON library is not loaded!"
        logger:error(message)
        messageAll(message)
    end

    local exportBasePath = dcsLiberation.savedGamesPath..[[\Mods\services\LotAtc\userdb\drawings\]]
    local drawings_json = nil

    if LotAtcExportConfig.exportRedAA then
        drawings_json = lotatcExport_for_faction(dcsLiberation.RedAA, "#7FE32000");

        local exportBasePathRed = exportBasePath..[[red\]]
        lfs.mkdir(exportBasePathRed)

        local exportFileName = exportBasePathRed.."threatZones.json"

        env.info(string.format("DCSLiberation|LotATC Export plugin - writing %s", exportFileName))

        local fp = io.open(exportFileName, 'w')
        if fp then
            fp:write(drawings_json)
            fp:close()
        end
    end

    if LotAtcExportConfig.exportBlueAA then
        drawings_json = lotatcExport_for_faction(dcsLiberation.BlueAA, "#7F0084FF");

        local exportBasePathBlue = exportBasePath..[[blue\]]
        lfs.mkdir(exportBasePathBlue)

        local exportFileName = exportBasePathBlue.."threatZones.json"

        env.info(string.format("DCSLiberation|LotATC Export plugin - writing %s", exportFileName))

        local fp = io.open(exportFileName, 'w')
        if fp then
            fp:write(drawings_json)
            fp:close()
        end
    end
end

