import { ControlPoint } from "./controlpoint";
import { Flight } from "./flight";
import FrontLine from "./frontline";
import { ThreatZoneContainer } from "./liberationApi";
import SupplyRoute from "./supplyroute";
import Tgo from "./tgo";
import { LatLngLiteral } from "leaflet";

export default interface Game {
  control_points: ControlPoint[];
  tgos: Tgo[];
  supply_routes: SupplyRoute[];
  front_lines: FrontLine[];
  flights: Flight[];
  threat_zones: ThreatZoneContainer;
  map_center: LatLngLiteral | null;
}
