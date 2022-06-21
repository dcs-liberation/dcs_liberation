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
  liberationApi,
  ControlPoint,
  Flight,
  FrontLine,
  SupplyRoute,
  Tgo,
} from "./liberationApi";
import { navMeshUpdated } from "./navMeshSlice";
import { updateTgo } from "./tgosSlice";
import { threatZonesUpdated } from "./threatZonesSlice";
import { unculledZonesUpdated } from "./unculledZonesSlice";
import { LatLng } from "leaflet";
import { updateIadsConnection } from "./iadsNetworkSlice";
import { IadsConnection } from "./_liberationApi";
import { supplyRoutesUpdated, supplyRoutesDeleted } from "./supplyRoutesSlice";

interface GameUpdateEvents {
  updated_flight_positions: { [id: string]: LatLng };
  new_combats: Combat[];
  updated_combats: Combat[];
  ended_combats: string[];
  navmesh_updates: boolean[];
  unculled_zones_updated: boolean;
  threat_zones_updated: boolean;
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
  updated_supply_routes: SupplyRoute[];
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

  for (const blue of events.navmesh_updates) {
    dispatch(
      liberationApi.endpoints.getNavmesh.initiate({ forPlayer: blue })
    ).then((result) => {
      if (result.data) {
        dispatch(navMeshUpdated({ blue: blue, mesh: result.data }));
      }
    });
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

  if (events.threat_zones_updated) {
    dispatch(liberationApi.endpoints.getThreatZones.initiate()).then(
      (result) => {
        if (result.data) {
          dispatch(threatZonesUpdated(result.data));
        }
      }
    );
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

  dispatch(supplyRoutesDeleted(events.updated_supply_routes.map(route => route.id)));
  dispatch(supplyRoutesUpdated(events.updated_supply_routes));
  /* for (const route of events.updated_supply_routes) {
    dispatch(supplyRoutesDeleted(route.id));
    dispatch(supplyRoutesUpdated(route as SupplyRoute));
  } */

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
