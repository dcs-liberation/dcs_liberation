import { selectMapCenter } from "../../api/mapSlice";
import { useAppSelector } from "../../app/hooks";
import AircraftLayer from "../aircraftlayer";
import AirDefenseRangeLayer from "../airdefenserangelayer";
import CombatLayer from "../combatlayer";
import ControlPointsLayer from "../controlpointslayer";
import CullingExclusionZones from "../cullingexclusionzones/CullingExclusionZones";
import FlightPlansLayer from "../flightplanslayer";
import FrontLinesLayer from "../frontlineslayer";
import Iadsnetworklayer from "../iadsnetworklayer";
import NavMeshLayer from "../navmesh/NavMeshLayer";
import LeafletRuler from "../ruler/Ruler";
import SupplyRoutesLayer from "../supplyrouteslayer";
import TerrainZonesLayers from "../terrainzones/TerrainZonesLayers";
import TgosLayer from "../tgoslayer/TgosLayer";
import { CoalitionThreatZones } from "../threatzones";
import { WaypointDebugZonesControls } from "../waypointdebugzones/WaypointDebugZonesControls";
import "./LiberationMap.css";
import { Map } from "leaflet";
import { useEffect, useRef } from "react";
import { BasemapLayer } from "react-esri-leaflet";
import { LayersControl, MapContainer, ScaleControl } from "react-leaflet";

export default function LiberationMap() {
  const map = useRef<Map>(null);
  const mapCenter = useAppSelector(selectMapCenter);
  useEffect(() => {
    map.current?.setView(mapCenter, 8, { animate: true, duration: 1 });
  });
  return (
    <MapContainer zoom={8} zoomControl={false} ref={map}>
      <ScaleControl />
      <LeafletRuler />
      <LayersControl collapsed={false}>
        <LayersControl.BaseLayer name="Imagery Clarity" checked>
          <BasemapLayer name="ImageryClarity" />
        </LayersControl.BaseLayer>
        <LayersControl.BaseLayer name="Imagery Firefly">
          <BasemapLayer name="ImageryFirefly" />
        </LayersControl.BaseLayer>
        <LayersControl.BaseLayer name="Topographic">
          <BasemapLayer name="Topographic" />
        </LayersControl.BaseLayer>
        <LayersControl.Overlay name="Control points" checked>
          <ControlPointsLayer />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Aircraft" checked>
          <AircraftLayer />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Active combat" checked>
          <CombatLayer />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Air defenses" checked>
          <TgosLayer categories={["aa"]} />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Factories" checked>
          <TgosLayer categories={["factory"]} />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Ships" checked>
          <TgosLayer categories={["ship"]} />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Other ground objects" checked>
          <TgosLayer categories={["aa", "factory", "ship"]} exclude />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Supply routes" checked>
          <SupplyRoutesLayer />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Front lines" checked>
          <FrontLinesLayer />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Enemy SAM threat range" checked>
          <AirDefenseRangeLayer blue={false} />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Enemy SAM detection range">
          <AirDefenseRangeLayer blue={false} detection />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Enemy IADS Network">
          <Iadsnetworklayer blue={false} />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Allied SAM threat range">
          <AirDefenseRangeLayer blue={true} />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Allied SAM detection range">
          <AirDefenseRangeLayer blue={true} detection />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Allied IADS Network">
          <Iadsnetworklayer blue={true} />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Selected blue flight plan">
          <FlightPlansLayer blue={true} selectedOnly />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="All blue flight plans" checked>
          <FlightPlansLayer blue={true} />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="All red flight plans">
          <FlightPlansLayer blue={false} />
        </LayersControl.Overlay>
      </LayersControl>
      <LayersControl position="topleft">
        <CoalitionThreatZones blue={true} />
        <CoalitionThreatZones blue={false} />
        <LayersControl.Overlay name="Blue navmesh">
          <NavMeshLayer blue={true} />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="Red navmesh">
          <NavMeshLayer blue={false} />
        </LayersControl.Overlay>
        <TerrainZonesLayers />
        <CullingExclusionZones />
        <WaypointDebugZonesControls />
      </LayersControl>
    </MapContainer>
  );
}
