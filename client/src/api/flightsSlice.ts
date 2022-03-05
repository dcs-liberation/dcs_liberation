import { RootState } from "../app/store";
import { Flight } from "./flight";
import { PayloadAction, createSlice } from "@reduxjs/toolkit";
import { LatLng } from "leaflet";

interface FlightsState {
  flights: { [id: string]: Flight };
  selected: Flight | null;
}

const initialState: FlightsState = {
  flights: {},
  selected: null,
};

export const flightsSlice = createSlice({
  name: "flights",
  initialState,
  reducers: {
    clearFlights: (state) => {
      state.flights = {};
    },
    registerFlight: (state, action: PayloadAction<Flight>) => {
      const flight = action.payload;
      if (flight.id in state.flights) {
        console.log(`Overriding flight with ID: ${flight.id}`);
      }
      state.flights[flight.id] = flight;
    },
    unregisterFlight: (state, action: PayloadAction<string>) => {
      const id = action.payload;
      delete state.flights[id];
    },
    updateFlight: (state, action: PayloadAction<Flight>) => {
      const flight = action.payload;
      state.flights[flight.id] = flight;
    },
    deselectFlight: (state) => {
      state.selected = null;
    },
    selectFlight: (state, action: PayloadAction<string>) => {
      const id = action.payload;
      state.selected = state.flights[id];
    },
    updateFlightPositions: (
      state,
      action: PayloadAction<[string, LatLng][]>
    ) => {
      for (const [id, position] of action.payload) {
        state.flights[id].position = position;
      }
    },
  },
});

export const {
  clearFlights,
  registerFlight,
  unregisterFlight,
  updateFlight,
  deselectFlight,
  selectFlight,
  updateFlightPositions,
} = flightsSlice.actions;

export const selectFlights = (state: RootState) => state.flights;

export default flightsSlice.reducer;
