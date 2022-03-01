import { LatLng } from "leaflet";
import { Waypoint } from "./waypoint";

export interface Flight {
  id: string;
  blue: boolean;
  position: LatLng;
  sidc: string;
  waypoints: Waypoint[] | null;
}
