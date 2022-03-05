import { Waypoint } from "./waypoint";
import { LatLng } from "leaflet";

export interface Flight {
  id: string;
  blue: boolean;
  position: LatLng | null;
  sidc: string;
  waypoints: Waypoint[] | null;
}
