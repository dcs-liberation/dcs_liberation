import { LatLng } from "leaflet";

export default interface Combat {
  id: string;
  flight_position: LatLng | null;
  target_positions: LatLng[] | null;
  footprint: LatLng[][] | null;
}
