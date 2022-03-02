import "./LiberationMap.css";

import { LayersControl, MapContainer, ScaleControl } from "react-leaflet";

import { BasemapLayer } from "react-esri-leaflet";
import ControlPointsLayer from "../controlpointslayer";
import FlightPlansLayer from "../flightplanslayer";
import { LatLng } from "leaflet";

interface GameProps {
  mapCenter: LatLng;
}

export default function LiberationMap(props: GameProps) {
  return (
    <MapContainer zoom={8} center={props.mapCenter} zoomControl={false}>
      <ScaleControl />
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
        <FlightPlansLayer blue={true} />
        <FlightPlansLayer blue={false} />
      </LayersControl>
    </MapContainer>
  );
}
