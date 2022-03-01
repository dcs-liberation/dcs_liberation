import "./LiberationMap.css";

import { BasemapLayer } from "react-esri-leaflet";
import ControlPointsLayer from "../controlpointslayer";
import FlightPlansLayer from "../flightplanslayer";
import { LatLng } from "leaflet";
import { MapContainer } from "react-leaflet";

interface GameProps {
  mapCenter: LatLng;
}

export default function LiberationMap(props: GameProps) {
  return (
    <MapContainer zoom={8} center={props.mapCenter}>
      <BasemapLayer name="ImageryClarity" />
      <ControlPointsLayer />
      <FlightPlansLayer blue={true} />
      <FlightPlansLayer blue={false} />
    </MapContainer>
  );
}
