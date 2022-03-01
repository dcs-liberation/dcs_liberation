import { LatLng } from "leaflet";

export interface ControlPoint {
  id: number;
  name: string;
  blue: boolean;
  position: LatLng;
  mobile: boolean;
  destination: LatLng | null;
  sidc: string;
}
