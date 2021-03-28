
function lotatcExport_generateJson()
    
	if not json then
        local message = "Unable to export LotATC drawings, JSON library is not loaded!"
        logger:error(message)
        messageAll(message)
    end
	
	local random = math.random
	local function uuid()
		local template ='xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
		return string.gsub(template, '[xy]', function (c)
			local v = (c == 'x') and random(0, 0xf) or random(8, 0xb)
			return string.format('%x', v)
		end)
	end
	
	drawings = {}
	
	for _,redAA in pairs(dcsLiberation.RedAA) do
		env.info(string.format("DCSLiberation|LotATC Export plugin - exporting %s", redAA.dcsGroupName))
		
		local convLat, convLon = coord.LOtoLL({x = redAA.positionX, y = 0, z = redAA.positionY})
		
		table.insert(drawings,
		{
			["author"] = "DCSLiberation",
			["brushStyle"] = 1,
			["color"] = "#64E32000",
			["colorBg"] = "#00ff0000",
			["id"] = string.format("{%s}", uuid()),
			["longitude"] = convLon,
			["latitude"] = convLat,
			["radius"] = tonumber(redAA.range),
			["lineWidth"] = 1,
			["name"] = string.format("%s|%s", redAA.name, redAA.dcsGroupName),
			["shared"] = True,
			["timestamp"] = "",
			["type"] = "circle",
			["text"] = string.format("%s|%s", redAA.name, redAA.dcsGroupName),
			["font"] = {
				["color"] = "#64E32000",
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
    local drawings_json = lotatcExport_generateJson();
	
	local fp = io.open(dcsLiberation.installPath.."/red.json", 'w')
    fp:write(drawings_json)
    fp:close()
end

lotatcExport()
