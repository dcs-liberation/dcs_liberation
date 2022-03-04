import { LatLng } from "leaflet";

export enum TgoType {
  AIR_DEFENSE = "Air defenses",
  FACTORY = "Factories",
  SHIP = "Ships",
  OTHER = "Other ground objects",
}

export interface Tgo {
  id: string;
  name: string;
  control_point_name: string;
  category: string;
  blue: boolean;
  position: LatLng;
  units: string[];
  threat_ranges: number[];
  detection_ranges: number[];
  dead: boolean;
  sidc: string;
}

export default Tgo;
