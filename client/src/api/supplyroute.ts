import { LatLng } from "leaflet";

export interface SupplyRoute {
  points: LatLng[];
  front_active: boolean;
  is_sea: boolean;
  blue: boolean;
  active_transports: string[];
}

export default SupplyRoute;
