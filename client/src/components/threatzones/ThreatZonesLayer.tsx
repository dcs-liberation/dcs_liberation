import { selectThreatZones } from "../../api/threatZonesSlice";
import { useAppSelector } from "../../app/hooks";
import ThreatZone from "./ThreatZone";
import { LayerGroup } from "react-leaflet";

export enum ThreatZoneFilter {
  FULL,
  AIRCRAFT,
  AIR_DEFENSES,
  RADAR_SAMS,
}

interface ThreatZonesLayerProps {
  blue: boolean;
  filter: ThreatZoneFilter;
}

export function ThreatZonesLayer(props: ThreatZonesLayerProps) {
  const allZones = useAppSelector(selectThreatZones).zones;
  const zones = props.blue ? allZones.blue : allZones.red;
  var filtered;
  switch (props.filter) {
    case ThreatZoneFilter.FULL:
      filtered = zones.full;
      break;
    case ThreatZoneFilter.AIRCRAFT:
      filtered = zones.aircraft;
      break;
    case ThreatZoneFilter.AIR_DEFENSES:
      filtered = zones.air_defenses;
      break;
    case ThreatZoneFilter.RADAR_SAMS:
      filtered = zones.radar_sams;
      break;
  }
  return (
    <LayerGroup>
      {filtered.map((poly, idx) => (
        <ThreatZone key={idx} poly={poly} blue={props.blue} />
      ))}
    </LayerGroup>
  );
}
