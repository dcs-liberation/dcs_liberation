import { LatLng } from "../../api/liberationApi";
import { Polygon } from "react-leaflet";

interface ThreatZoneProps {
  poly: LatLng[][];
  blue: boolean;
}

export default function ThreatZone(props: ThreatZoneProps) {
  const color = props.blue ? "#0084ff" : "#c85050";
  return (
    <Polygon
      positions={props.poly}
      color={color}
      weight={1}
      fill
      fillOpacity={0.4}
      noClip
      interactive={false}
    />
  );
}
