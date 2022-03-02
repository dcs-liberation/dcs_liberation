import { deselectFlight, selectFlight } from "./flightsSlice";

import { AppDispatch } from "../app/store";
import { Flight } from "./flight";
import { LatLng } from "leaflet";

// Placeholder. We don't use this yet. This is just here so we can flesh out the
// update events model.
interface FrozenCombat {}

interface GameUpdateEvents {
  updated_flight_positions: { [id: string]: LatLng };
  new_combats: FrozenCombat[];
  updated_combats: FrozenCombat[];
  ended_combats: string[];
  navmesh_updates: boolean[];
  unculled_zones_updated: boolean;
  threat_zones_updated: boolean;
  new_flights: Flight[];
  updated_flights: string[];
  deleted_flights: string[];
  selected_flight: string | null;
  deselected_flight: boolean;
}

export const handleStreamedEvents = (
  dispatch: AppDispatch,
  events: GameUpdateEvents
) => {
  if (events.deselected_flight) {
    dispatch(deselectFlight());
  }
  if (events.selected_flight != null) {
    dispatch(selectFlight(events.selected_flight));
  }
};
