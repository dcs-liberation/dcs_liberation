import { AppDispatch } from "../app/store";
import { gameUnloaded } from "./actions";
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
  liberationApi,
  ControlPoint,
  Flight,
  FrontLine,
  IadsConnection,
  SupplyRoute,
  Tgo,
  UnculledZone,
} from "./liberationApi";
import { navMeshUpdated } from "./navMeshSlice";
import { updateTgo } from "./tgosSlice";
import { threatZonesUpdated } from "./threatZonesSlice";
import { unculledZonesUpdated } from "./unculledZonesSlice";
import { LatLng } from "leaflet";
import { updateIadsConnection, removeIadsConnection } from "./iadsNetworkSlice";
import { supplyRoutesUpdated } from "./supplyRoutesSlice";

interface GameUpdateEvents {
  updated_flight_positions: { [id: string]: LatLng };
  new_combats: Combat[];
  updated_combats: Combat[];
  ended_combats: string[];
  navmesh_updates: boolean[];
  updated_unculled_zones: UnculledZone[];
  threat_zones_updated: boolean;
  new_flights: Flight[];
  updated_flights: Flight[];
  deleted_flights: string[];
  selected_flight: string | null;
  deselected_flight: boolean;
  updated_front_lines: FrontLine[];
  deleted_front_lines: string[];
  updated_tgos: Tgo[];
  updated_control_points: ControlPoint[];
  updated_supply_routes: SupplyRoute[];
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

  if (events.updated_unculled_zones.length > 0) {
    dispatch(unculledZonesUpdated(events.updated_unculled_zones));
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

  if (events.updated_supply_routes.length > 0) {
    dispatch(supplyRoutesUpdated(events.updated_supply_routes));
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
