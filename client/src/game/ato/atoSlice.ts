import { PayloadAction, createSlice } from "@reduxjs/toolkit";

import { Flight } from "../flight";
import { RootState } from "../../app/store";

interface AtoState {
  blue: { [id: string]: Flight };
  red: { [id: string]: Flight };
}

const initialState: AtoState = {
  blue: {},
  red: {},
};

export const atoSlice = createSlice({
  name: "ato",
  initialState,
  reducers: {
    clearFlights: (state) => {
      state.blue = {};
      state.red = {};
    },
    registerFlight: (state, action: PayloadAction<Flight>) => {
      const flight = action.payload;
      const ato = flight.blue ? state.blue : state.red;
      if (flight.id in ato) {
        console.log(`Overriding flight with ID: ${flight.id}`);
      }
      ato[flight.id] = flight;
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
  },
});

export const { clearFlights, registerFlight, unregisterFlight } =
  atoSlice.actions;

export const selectAtos = (state: RootState) => state.atos;

export default atoSlice.reducer;
