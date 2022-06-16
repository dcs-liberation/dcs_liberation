import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { UnculledZone } from "./liberationApi";
import { PayloadAction, createSlice } from "@reduxjs/toolkit";

interface UnculledZonesState {
  zones: UnculledZone[];
}

const initialState: UnculledZonesState = {
  zones: [],
};

export const unculledZonesSlice = createSlice({
  name: "unculledZonesState",
  initialState,
  reducers: {
    updated: (state, action: PayloadAction<UnculledZone[]>) => {
      state.zones = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      state.zones = action.payload.unculled_zones;
    });
    builder.addCase(gameUnloaded, (state) => {
      state.zones = initialState.zones;
    });
  },
});

export const { updated: unculledZonesUpdated } = unculledZonesSlice.actions;

export const selectUnculledZones = (state: RootState) => state.unculledZones;

export default unculledZonesSlice.reducer;
