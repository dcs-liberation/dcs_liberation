import { AppDispatch } from "../app/store";
import { gameUnloaded } from "./actions";
import Combat from "./combat";
import { endCombats, newCombats, updateCombats } from "./combatSlice";
import { updateControlPoint } from "./controlPointsSlice";
import {
  deselectFlight,
  registerFlights,
  selectFlight,
  unregisterFlights,
  updateFlights,
  updateFlightPositions,
} from "./flightsSlice";
import {
  deleteFrontLine,
  updateFrontLine,
} from "./frontLinesSlice";
import reloadGameState from "./gamestate";
import {
  ControlPoint,
  Flight,
  FrontLine,
  IadsConnection,
  NavMesh,
  Tgo,
  ThreatZones,
  UnculledZone,
} from "./liberationApi";
import { navMeshUpdated } from "./navMeshSlice";
import { updateTgo } from "./tgosSlice";
import { threatZonesUpdated } from "./threatZonesSlice";
import { unculledZonesUpdated } from "./unculledZonesSlice";
import { LatLng } from "leaflet";
import { updateIadsConnection, removeIadsConnection } from "./iadsNetworkSlice";

interface GameUpdateEvents {
  updated_flight_positions: { [id: string]: LatLng };
  new_combats: Combat[];
  updated_combats: Combat[];
  ended_combats: string[];
  navmesh_updates: {blue: boolean, mesh: NavMesh}[];
  updated_unculled_zones: UnculledZone[];
  threat_zones_updated: {blue: boolean, zones: ThreatZones}[];
  new_flights: Flight[];
  updated_flights: Flight[];
  deleted_flights: string[];
  selected_flight: string | null;
  deselected_flight: boolean;
  updated_front_lines: FrontLine[];
  deleted_front_lines: string[];
  updated_tgos: Tgo[];
  updated_control_points: ControlPoint[];
  updated_iads: IadsConnection[];
  deleted_iads: string[];
  reset_on_map_center: LatLng | null;
  game_unloaded: boolean;
  new_turn: boolean;
}

export const handleStreamedEvents = (
  dispatch: AppDispatch,
  events: GameUpdateEvents
) => {
  if (Object.keys(events.updated_flight_positions).length) {
    dispatch(
      updateFlightPositions(Object.entries(events.updated_flight_positions))
    );
  }

  if (events.new_combats.length > 0) {
    dispatch(newCombats(events.new_combats));
  }

  if (events.updated_combats.length > 0) {
    dispatch(updateCombats(events.updated_combats));
  }

  if (events.ended_combats.length > 0) {
    dispatch(endCombats(events.ended_combats));
  }

  if (Object.keys(events.navmesh_updates).length > 0) {
    dispatch(navMeshUpdated(events.navmesh_updates));
  }

  if (events.updated_unculled_zones.length > 0) {
    dispatch(unculledZonesUpdated(events.updated_unculled_zones));
  }

  if (Object.keys(events.threat_zones_updated).length > 0) {
    dispatch(threatZonesUpdated(events.threat_zones_updated));
  }

  if (events.new_flights.length > 0) {
    dispatch(registerFlights(events.new_flights));
  }

  if (events.updated_flights.length > 0) {
    dispatch(updateFlights(events.updated_flights));
  }

  if (events.deleted_flights.length > 0) {
    dispatch(unregisterFlights(events.deleted_flights));
  }

  if (events.deselected_flight) {
    dispatch(deselectFlight());
  }

  if (events.selected_flight != null) {
    dispatch(selectFlight(events.selected_flight));
  }

  if (events.updated_front_lines.length > 0) {
    dispatch(updateFrontLine(events.updated_front_lines));
  }

  if (events.deleted_front_lines.length > 0) {
    dispatch(deleteFrontLine(events.deleted_front_lines));
  }

  if (events.updated_tgos.length > 0) {
    dispatch(updateTgo(events.updated_tgos));
  }

  if (events.updated_control_points.length > 0) {
      dispatch(updateControlPoint(events.updated_control_points));
  }

  if (events.deleted_iads.length > 0) {
    dispatch(removeIadsConnection(events.deleted_iads));
  }

  if (events.updated_iads.length > 0) {
    dispatch(updateIadsConnection(events.updated_iads));
  }

  if (events.reset_on_map_center != null) {
    reloadGameState(dispatch);
  }

  if (events.game_unloaded) {
    dispatch(gameUnloaded());
  }

  if (events.new_turn) {
    reloadGameState(dispatch, true);
  }
};
