-------------------------------------------------------------------------------------------------------------------------------------------------------------
-- configuration file for the LotATC Export script
--
-- This configuration is tailored for a mission generated by DCS Liberation
-- see https://github.com/Khopa/dcs_liberation
-------------------------------------------------------------------------------------------------------------------------------------------------------------

-- LotATC Export plugin - configuration
env.info("DCSLiberation|LotATC Export plugin - configuration")

if dcsLiberation then
    env.info("DCSLiberation|LotATC Export plugin - configuration dcsLiberation")

    exportRedAA = true
    exportBlueAA = false

    -- retrieve specific options values
    if dcsLiberation.plugins then
        env.info("DCSLiberation|LotATC Export plugin - configuration dcsLiberation.plugins")
    
        if dcsLiberation.plugins.lotatc then
            env.info("DCSLiberation|LotATC Export plugin - dcsLiberation.plugins.lotatcExport")
            exportRedAA = dcsLiberation.plugins.lotatc.exportRedAA
            env.info(string.format("DCSLiberation|LotATC Export plugin - exportRedAA = %s",tostring(exportRedAA)))
            exportBlueAA = dcsLiberation.plugins.lotatc.exportBlueAA
            env.info(string.format("DCSLiberation|LotATC Export plugin - exportBlueAA = %s",tostring(exportBlueAA)))
        end
    end
    
    -- actual configuration code
    if LotAtcExportConfig then 
        LotAtcExportConfig.exportRedAA = exportRedAA
        LotAtcExportConfig.exportBlueAA = exportBlueAA

        lotatcExport()
    end

end