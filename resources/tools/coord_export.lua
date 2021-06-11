local function dump_coords()
    local coordinates = {}
    local bases = world.getAirbases()
    for i = 1, #bases do
        local base = bases[i]
        point = Airbase.getPoint(base)
        lat, lon, alt = coord.LOtoLL(point)
        coordinates[Airbase.getName(base)] = {
            ["point"] = point,
            ["LL"] = {
                ["lat"] = lat,
                ["lon"] = lon,
                ["alt"] = alt,
            },
        }
    end

    zero = {
        ["x"] = 0,
        ["y"] = 0,
        ["z"] = 0,
    }
    lat, lon, alt = coord.LOtoLL(zero)
    coordinates["zero"] = {
        ["point"] = zero,
        ["LL"] = {
            ["lat"] = lat,
            ["lon"] = lon,
            ["alt"] = alt,
        },
    }

    local fp = io.open(lfs.writedir() .. "\\coords.json", 'w')
    fp:write(json:encode(coordinates))
    fp:close()
end

dump_coords()