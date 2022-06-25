import { AppDispatch } from "../app/store";
import { gameUnloaded } from "./actions";
import backend from "./backend";
import Combat from "./combat";
import { endCombat, newCombat, updateCombat } from "./combatSlice";
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
  Tgo,
  UnculledZone,
} from "./liberationApi";
import { navMeshUpdated } from "./navMeshSlice";
import { updateTgo } from "./tgosSlice";
import { threatZonesUpdated } from "./threatZonesSlice";
import { unculledZonesUpdated } from "./unculledZonesSlice";
import { LatLng } from "leaflet";
import { updateIadsConnection } from "./iadsNetworkSlice";
<<<<<<< develop-FixMap-Mesh&Threats
import { IadsConnection, NavMesh, ThreatZones } from "./_liberationApi";
=======
>>>>>>> develop

interface GameUpdateEvents {
  updated_flight_positions: { [id: string]: LatLng };
  new_combats: Combat[];
  updated_combats: Combat[];
  ended_combats: string[];
<<<<<<< develop-FixMap-Mesh&Threats
  navmesh_updates: {blue: boolean, mesh: NavMesh}[];
  unculled_zones_updated: boolean;
  threat_zones_updated: {blue: boolean, zones: ThreatZones}[];
=======
  navmesh_updates: boolean[];
  updated_unculled_zones: UnculledZone[];
  threat_zones_updated: boolean;
>>>>>>> develop
  new_flights: Flight[];
  updated_flights: Flight[];
  deleted_flights: string[];
  selected_flight: string | null;
  deselected_flight: boolean;
  updated_front_lines: FrontLine[];
  deleted_front_lines: string[];
  updated_tgos: string[];
  updated_control_points: ControlPoint[];
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

  for (const combat of events.new_combats) {
    dispatch(newCombat(combat));
  }

  for (const combat of events.updated_combats) {
    dispatch(updateCombat(combat));
  }

  for (const id of events.ended_combats) {
    dispatch(endCombat(id));
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

  for (const id of events.updated_tgos) {
    backend.get(`/tgos/${id}`).then((response) => {
      const tgo = response.data as Tgo;
      dispatch(updateTgo(tgo));
    });
    backend.get(`/iads-network/for-tgo/${id}`).then((response) => {
      for (const connection of response.data) {
        dispatch(updateIadsConnection(connection as IadsConnection));
      }
    });
  }

  if (events.updated_control_points.length > 0) {
      dispatch(updateControlPoint(events.updated_control_points));
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
