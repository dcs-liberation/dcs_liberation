import {
  ControlPoint,
  Flight,
  FrontLine,
  NavMeshes,
  SupplyRoute,
  Tgo,
  ThreatZoneContainer,
} from "./liberationApi";
import { LatLngLiteral } from "leaflet";

export default interface Game {
  control_points: ControlPoint[];
  tgos: Tgo[];
  supply_routes: SupplyRoute[];
  front_lines: FrontLine[];
  flights: Flight[];
  threat_zones: ThreatZoneContainer;
  navmeshes: NavMeshes;
  map_center: LatLngLiteral | null;
}
