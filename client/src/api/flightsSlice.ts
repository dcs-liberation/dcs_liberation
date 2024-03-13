import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { Flight } from "./liberationApi";
import { PayloadAction, createSlice } from "@reduxjs/toolkit";
import { LatLng } from "leaflet";

interface FlightsState {
  flights: { [id: string]: Flight };
  selected: string | null;
}

const initialState: FlightsState = {
  flights: {},
  selected: null,
};

export const flightsSlice = createSlice({
  name: "flights",
  initialState,
  reducers: {
    registerFlights: (state, action: PayloadAction<Flight[]>) => {
      for (const flight of action.payload) {
        if (flight.id in state.flights) {
          console.log(`Overriding flight with ID: ${flight.id}`);
        }
        state.flights[flight.id] = flight;
      }
    },
    unregisterFlights: (state, action: PayloadAction<string[]>) => {
      for (const id of action.payload) {
        delete state.flights[id];
      }
    },
    updateFlights: (state, action: PayloadAction<Flight[]>) => {
      for (const flight of action.payload) {
        state.flights[flight.id] = flight;
      }
    },
    deselectFlight: (state) => {
      state.selected = null;
    },
    selectFlight: (state, action: PayloadAction<string>) => {
      state.selected = action.payload;
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
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      state.selected = null;
      state.flights = action.payload.flights.reduce(
        (acc: { [key: string]: Flight }, curr) => {
          acc[curr.id] = curr;
          return acc;
        },
        {}
      );
    });
    builder.addCase(gameUnloaded, (state) => {
      state.selected = null;
      state.flights = {};
    });
  },
});

export const {
  registerFlights,
  unregisterFlights,
  updateFlights,
  deselectFlight,
  selectFlight,
  updateFlightPositions,
} = flightsSlice.actions;

export const selectFlights = (state: RootState) => state.flights;
export const selectSelectedFlightId = (state: RootState) =>
  state.flights.selected;
export const selectSelectedFlight = (state: RootState) => {
  const id = state.flights.selected;
  return id ? state.flights.flights[id] : null;
};

export default flightsSlice.reducer;
