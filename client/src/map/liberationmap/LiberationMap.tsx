import { MapContainer } from "react-leaflet";
import { BasemapLayer } from "react-esri-leaflet";
import { ControlPointsLayer } from "../controlpointslayer/ControlPointsLayer";
import "./LiberationMap.css";
import { LatLng } from "leaflet";

interface GameProps {
  mapCenter: LatLng;
}

export function LiberationMap(props: GameProps) {
  return (
    <MapContainer zoom={8} center={props.mapCenter}>
      <BasemapLayer name="ImageryClarity" />
      <ControlPointsLayer />
    </MapContainer>
  );
}
