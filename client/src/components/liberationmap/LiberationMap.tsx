import "./LiberationMap.css";

import { MapContainer, ScaleControl } from "react-leaflet";

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
      <BasemapLayer name="ImageryClarity" />
      <ScaleControl />
      <ControlPointsLayer />
      <FlightPlansLayer blue={true} />
      <FlightPlansLayer blue={false} />
    </MapContainer>
  );
}
