import { MapContainer } from "react-leaflet";
import { BasemapLayer } from "react-esri-leaflet";
import { ControlPointsLayer } from "../controlpointslayer/ControlPointsLayer";
import "./LiberationMap.css";
import { LatLng } from "leaflet";
import { FlightPlansLayer } from "../flightplanslayer/FlightPlansLayer";

interface GameProps {
  mapCenter: LatLng;
}

export function LiberationMap(props: GameProps) {
  return (
    <MapContainer zoom={8} center={props.mapCenter}>
      <BasemapLayer name="ImageryClarity" />
      <ControlPointsLayer />
      <FlightPlansLayer blue={true} />
      <FlightPlansLayer blue={false} />
    </MapContainer>
  );
}
