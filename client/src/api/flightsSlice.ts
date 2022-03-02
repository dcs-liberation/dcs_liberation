import { PayloadAction, createSlice } from "@reduxjs/toolkit";

import { Flight } from "./flight";
import { RootState } from "../app/store";

interface FlightsState {
  blue: { [id: string]: Flight };
  red: { [id: string]: Flight };
  selected: Flight | null;
}

const initialState: FlightsState = {
  blue: {},
  red: {},
  selected: null,
};

export const flightsSlice = createSlice({
  name: "flights",
  initialState,
  reducers: {
    clearFlights: (state) => {
      state.blue = {};
      state.red = {};
    },
    registerFlight: (state, action: PayloadAction<Flight>) => {
      const flight = action.payload;
      const coalitionFlights = flight.blue ? state.blue : state.red;
      if (flight.id in coalitionFlights) {
        console.log(`Overriding flight with ID: ${flight.id}`);
      }
      coalitionFlights[flight.id] = flight;
    },
    unregisterFlight: (state, action: PayloadAction<string>) => {
      const id = action.payload;
      if (id in state.blue) {
        delete state.blue[id];
      } else if (id in state.red) {
        delete state.red[id];
      } else {
        console.log(
          `Could not delete flight with ID ${id} because no flight with that ` +
            `ID exists`
        );
      }
    },
    deselectFlight: (state) => {
      state.selected = null;
    },
    selectFlight: (state, action: PayloadAction<string>) => {
      const id = action.payload;
      state.selected = state.blue[id];
    },
  },
});

export const {
  clearFlights,
  registerFlight,
  unregisterFlight,
  deselectFlight,
  selectFlight,
} = flightsSlice.actions;

export const selectFlights = (state: RootState) => state.flights;

export default flightsSlice.reducer;
