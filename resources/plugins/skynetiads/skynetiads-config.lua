-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- Mission configuration file for the Skynet-IADS framework
-- see https://github.com/walder/Skynet-IADS
--
-- This configuration is tailored for a mission generated by DCS Liberation
-- see https://github.com/dcs-liberation/dcs_liberation
-------------------------------------------------------------------------------------------------------------------------------------------------------------

-- Skynet-IADS plugin - configuration
env.info("DCSLiberation|Skynet-IADS plugin - configuration")

if dcsLiberation and SkynetIADS then

    -- specific options
    local createRedIADS = false
    local createBlueIADS = false
    local includeRedInRadio = false
    local includeBlueInRadio = false
    local debugRED = false
    local debugBLUE = false

    -- retrieve specific options values
    if dcsLiberation.plugins then
        if dcsLiberation.plugins.skynetiads then
            createRedIADS = dcsLiberation.plugins.skynetiads.createRedIADS
            createBlueIADS = dcsLiberation.plugins.skynetiads.createBlueIADS
            includeRedInRadio = dcsLiberation.plugins.skynetiads.includeRedInRadio
            includeBlueInRadio = dcsLiberation.plugins.skynetiads.includeBlueInRadio
            debugRED = dcsLiberation.plugins.skynetiads.debugRED
            debugBLUE = dcsLiberation.plugins.skynetiads.debugBLUE
        end
    end

    env.info(string.format("DCSLiberation|Skynet-IADS plugin - createRedIADS=%s",tostring(createRedIADS)))
    env.info(string.format("DCSLiberation|Skynet-IADS plugin - createBlueIADS=%s",tostring(createBlueIADS)))
    env.info(string.format("DCSLiberation|Skynet-IADS plugin - includeRedInRadio=%s",tostring(includeRedInRadio)))
    env.info(string.format("DCSLiberation|Skynet-IADS plugin - includeBlueInRadio=%s",tostring(includeBlueInRadio)))
    env.info(string.format("DCSLiberation|Skynet-IADS plugin - debugRED=%s",tostring(debugRED)))
    env.info(string.format("DCSLiberation|Skynet-IADS plugin - debugBLUE=%s",tostring(debugBLUE)))

    -- actual configuration code
    local function initializeIADSElement(iads, iads_unit, element)
        if element.ConnectionNode then
            for i,cn in pairs(element.ConnectionNode) do
                env.info(string.format("DCSLiberation|Skynet-IADS plugin - adding IADS ConnectionNode %s", cn))
                connection_node = StaticObject.getByName(cn .. " object") -- pydcs adds ' object' to the unit name for static elements
                iads_unit:addConnectionNode(connection_node)
            end
        end
        if element.PowerSource then
            for i,ps in pairs(element.PowerSource) do
                env.info(string.format("DCSLiberation|Skynet-IADS plugin - adding IADS PowerSource %s", ps))
                power_source = StaticObject.getByName(ps .. " object") -- pydcs adds ' object' to the unit name for static elements
                iads_unit:addPowerSource(power_source)
            end
        end
        if element.PD then
            for i,pd in pairs(element.PD) do
                env.info(string.format("DCSLiberation|Skynet-IADS plugin - adding IADS Point Defence %s", pd))
                point_defence = iads:addSAMSite(pd)
                iads_unit:addPointDefence(point_defence)
                iads_unit:setIgnoreHARMSWhilePointDefencesHaveAmmo(true)
            end
        end
    end

    local function initializeIADS(iads, coalition, inRadio, debug)

        local coalitionPrefix = "BLUE"
        if coalition == 1 then
            coalitionPrefix = "RED"
        end

        if debug then
            env.info("adding debug information")
            local iadsDebug = iads:getDebugSettings()
            iadsDebug.IADSStatus = true
            iadsDebug.samWentDark = true
            iadsDebug.contacts = true
            iadsDebug.radarWentLive = true
            iadsDebug.noWorkingCommmandCenter = true
            iadsDebug.ewRadarNoConnection = true
            iadsDebug.samNoConnection = true
            iadsDebug.jammerProbability = true
            iadsDebug.addedEWRadar = true
            iadsDebug.hasNoPower = true
            iadsDebug.harmDefence = true
            iadsDebug.samSiteStatusEnvOutput = true
            iadsDebug.earlyWarningRadarStatusEnvOutput = true
        end

        --add general EWR units like carrier to the IADS:
        iads:addEarlyWarningRadarsByPrefix(coalitionPrefix .. "|EWR|")

        -- add the AWACS
        if dcsLiberation.AWACs then
            for _, data in pairs(dcsLiberation.AWACs) do
                env.info(string.format("DCSLiberation|Skynet-IADS plugin - processing AWACS %s", data.dcsGroupName))
                local group = Group.getByName(data.dcsGroupName)
                if group then
                    if group:getCoalition() == coalition then
                        local unit = group:getUnit(1)
                        if unit then
                            local unitName = unit:getName()
                            env.info(string.format("DCSLiberation|Skynet-IADS plugin - adding AWACS %s", unitName))
                            iads:addEarlyWarningRadar(unitName)
                        end
                    end
                end
            end
        end

        -- add the IADS Elements: SAM, EWR, and Command Centers
        if dcsLiberation.IADS then
            coalition_iads = dcsLiberation.IADS[coalitionPrefix]
            if coalition_iads.Ewr then
                for _,unit in pairs(coalition_iads.Ewr) do
                    env.info(string.format("DCSLiberation|Skynet-IADS plugin - processing IADS EWR %s", unit.dcsGroupName))
                    iads_unit = iads:addEarlyWarningRadar(unit.dcsGroupName)
                    initializeIADSElement(iads, iads_unit, unit)
                end
            end
            if coalition_iads.Sam then
                for _,unit in pairs(coalition_iads.Sam) do
                    env.info(string.format("DCSLiberation|Skynet-IADS plugin - processing IADS SAM %s", unit.dcsGroupName))
                    iads_unit = iads:addSAMSite(unit.dcsGroupName)
                    initializeIADSElement(iads, iads_unit, unit)
                end
            end
            if coalition_iads.SamAsEwr then
                for _,unit in pairs(coalition_iads.SamAsEwr) do
                    env.info(string.format("DCSLiberation|Skynet-IADS plugin - processing IADS SAM as EWR %s", unit.dcsGroupName))
                    iads_unit = iads:addSAMSite(unit.dcsGroupName)
                    iads_unit:setActAsEW(true)
                    initializeIADSElement(iads, iads_unit, unit)
                end
            end
            if coalition_iads.CommandCenter then
                for _,unit in pairs(coalition_iads.CommandCenter) do
                    env.info(string.format("DCSLiberation|Skynet-IADS plugin - processing IADS Command Center %s", unit.dcsGroupName))
                    commandCenter = StaticObject.getByName(unit.dcsGroupName .. " object") -- pydcs adds ' object' to the unit name for static elements
                    iads_unit = iads:addCommandCenter(commandCenter)
                    initializeIADSElement(iads, iads_unit, unit)
                end
            end
        end

        if inRadio then
            --activate the radio menu to toggle IADS Status output
            env.info("DCSLiberation|Skynet-IADS plugin - adding in radio menu")
            iads:addRadioMenu()
        end

        --activate the IADS
        iads:setupSAMSitesAndThenActivate()
    end

    ------------------------------------------------------------------------------------------------------------------------------------------------------------
    -- create the IADS networks
    -------------------------------------------------------------------------------------------------------------------------------------------------------------
    if createRedIADS then
        env.info("DCSLiberation|Skynet-IADS plugin - creating red IADS")
        redIADS = SkynetIADS:create("IADS")
        initializeIADS(redIADS, 1, includeRedInRadio, debugRED) -- RED
    end

    if createBlueIADS then
        env.info("DCSLiberation|Skynet-IADS plugin - creating blue IADS")
        blueIADS = SkynetIADS:create("IADS")
        initializeIADS(blueIADS, 2, includeBlueInRadio, debugBLUE) -- BLUE
    end

end