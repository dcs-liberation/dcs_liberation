import "./LiberationMap.css";

import { LayersControl, MapContainer, ScaleControl } from "react-leaflet";

import { BasemapLayer } from "react-esri-leaflet";
import ControlPointsLayer from "../controlpointslayer";
import FlightPlansLayer from "../flightplanslayer";
import { LatLng } from "leaflet";
import { TgoType } from "../../api/tgo";
import TgosLayer from "../tgoslayer/TgosLayer";

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
        {Object.values(TgoType).map((type) => {
          return (
            <LayersControl.Overlay name={type} checked>
              <TgosLayer type={type as TgoType} />
            </LayersControl.Overlay>
          );
        })}
        <LayersControl.Overlay name="All blue flight plans" checked>
          <FlightPlansLayer blue={true} />
        </LayersControl.Overlay>
        <LayersControl.Overlay name="All red flight plans">
          <FlightPlansLayer blue={false} />
        </LayersControl.Overlay>
      </LayersControl>
    </MapContainer>
  );
}
