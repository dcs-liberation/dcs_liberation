import { LatLng } from "leaflet";
import { Polygon } from "react-leaflet";

interface ThreatZoneProps {
  poly: number[][];
  blue: boolean;
}

export default function ThreatZone(props: ThreatZoneProps) {
  const color = props.blue ? "#0084ff" : "#c85050";
  // TODO: Fix response model so the type can be used directly.
  const positions = props.poly.map(([lat, lng]) => new LatLng(lat, lng));
  return (
    <Polygon
      positions={positions}
      color={color}
      weight={1}
      fill
      fillOpacity={0.4}
      noClip
      interactive={false}
    />
  );
}
