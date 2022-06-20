import { AppDispatch } from "../app/store";
import { gameUnloaded } from "./actions";
import backend from "./backend";
import Combat from "./combat";
import { endCombat, newCombat, updateCombat } from "./combatSlice";
import { updateControlPoint } from "./controlPointsSlice";
import {
  deselectFlight,
  registerFlight,
  selectFlight,
  unregisterFlight,
  updateFlight,
  updateFlightPositions,
} from "./flightsSlice";
import {
  addFrontLine,
  deleteFrontLine,
  updateFrontLine,
} from "./frontLinesSlice";
import reloadGameState from "./gamestate";
import {
  ControlPoint,
  Flight,
  FrontLine,
  Tgo,
} from "./liberationApi";
import { navMeshUpdated, INavMeshUpdate } from "./navMeshSlice";
import { updateTgo } from "./tgosSlice";
import { threatZonesUpdated, IThreatZoneUpdate } from "./threatZonesSlice";
import { unculledZonesUpdated } from "./unculledZonesSlice";
import { LatLng } from "leaflet";
import { updateIadsConnection } from "./iadsNetworkSlice";
import { IadsConnection, NavMesh, ThreatZones } from "./_liberationApi";

interface GameUpdateEvents {
  updated_flight_positions: { [id: string]: LatLng };
  new_combats: Combat[];
  updated_combats: Combat[];
  ended_combats: string[];
  navmesh_updates: {blue: boolean, mesh: NavMesh}[];
  unculled_zones_updated: boolean;
  threat_zones_updated: {blue: boolean, zones: ThreatZones}[];
  new_flights: Flight[];
  updated_flights: string[];
  deleted_flights: string[];
  selected_flight: string | null;
  deselected_flight: boolean;
  new_front_lines: FrontLine[];
  updated_front_lines: string[];
  deleted_front_lines: string[];
  updated_tgos: string[];
  updated_control_points: number[];
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

  for (const [blue, navmesh] of Object.entries(events.navmesh_updates)) {
    const data = {blue: (blue === "true"), mesh: navmesh}
    dispatch(navMeshUpdated( data as unknown as INavMeshUpdate ));
  }

  if (events.unculled_zones_updated) {
    backend.get(`/map-zones/unculled`).then(
      (result) => {
        if (result.data) {
          dispatch(unculledZonesUpdated(result.data));
        }
      }
    );
  }

  for (const [blue, zones] of Object.entries(events.threat_zones_updated)) {
    const data = {blue: (blue === "true"), zones: zones}
    dispatch(threatZonesUpdated( data as unknown as IThreatZoneUpdate ));

  }

  for (const flight of events.new_flights) {
    dispatch(registerFlight(flight));
  }

  for (const id of events.updated_flights) {
    backend.get(`/flights/${id}?with_waypoints=true`).then((response) => {
      const flight = response.data as Flight;
      dispatch(updateFlight(flight));
    });
  }

  for (const id of events.deleted_flights) {
    dispatch(unregisterFlight(id));
  }

  if (events.deselected_flight) {
    dispatch(deselectFlight());
  }

  if (events.selected_flight != null) {
    dispatch(selectFlight(events.selected_flight));
  }

  for (const front of events.new_front_lines) {
    dispatch(addFrontLine(front));
  }

  for (const id of events.updated_front_lines) {
    backend.get(`/front-lines/${id}`).then((response) => {
      const front = response.data as FrontLine;
      dispatch(updateFrontLine(front));
    });
  }

  for (const id of events.deleted_front_lines) {
    dispatch(deleteFrontLine(id));
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

  for (const id of events.updated_control_points) {
    backend.get(`/control-points/${id}`).then((response) => {
      const cp = response.data as ControlPoint;
      dispatch(updateControlPoint(cp));
    });
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
