import { ThreatZoneFilter, ThreatZonesLayer } from "./ThreatZonesLayer";
import { LayersControl } from "react-leaflet";

interface CoalitionThreatZonesProps {
  blue: boolean;
}

export function CoalitionThreatZones(props: CoalitionThreatZonesProps) {
  const color = props.blue ? "Blue" : "Red";
  return (
    <>
      <LayersControl.Overlay name={`${color} threat zones: full`}>
        <ThreatZonesLayer blue={props.blue} filter={ThreatZoneFilter.FULL} />
      </LayersControl.Overlay>
      <LayersControl.Overlay name={`${color} threat zones: aircraft`}>
        <ThreatZonesLayer
          blue={props.blue}
          filter={ThreatZoneFilter.AIRCRAFT}
        />
      </LayersControl.Overlay>
      <LayersControl.Overlay name={`${color} threat zones: air defenses`}>
        <ThreatZonesLayer
          blue={props.blue}
          filter={ThreatZoneFilter.AIR_DEFENSES}
        />
      </LayersControl.Overlay>
      <LayersControl.Overlay name={`${color} threat zones: radar SAMs`}>
        <ThreatZonesLayer
          blue={props.blue}
          filter={ThreatZoneFilter.RADAR_SAMS}
        />
      </LayersControl.Overlay>
    </>
  );
}
