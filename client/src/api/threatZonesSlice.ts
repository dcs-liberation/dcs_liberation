import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { ThreatZoneContainer } from "./liberationApi";
import { PayloadAction, createSlice } from "@reduxjs/toolkit";

interface ThreatZonesState {
  zones: ThreatZoneContainer;
}

const initialState: ThreatZonesState = {
  zones: {
    blue: {
      full: [],
      aircraft: [],
      air_defenses: [],
      radar_sams: [],
    },
    red: {
      full: [],
      aircraft: [],
      air_defenses: [],
      radar_sams: [],
    },
  },
};

export const threatZonesSlice = createSlice({
  name: "threatZonesState",
  initialState,
  reducers: {
    updated: (state, action: PayloadAction<ThreatZoneContainer>) => {
      state.zones = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      state.zones = action.payload.threat_zones;
    });
    builder.addCase(gameUnloaded, (state) => {
      state.zones = initialState.zones;
    });
  },
});

export const { updated: threatZonesUpdated } = threatZonesSlice.actions;

export const selectThreatZones = (state: RootState) => state.threatZones;

export default threatZonesSlice.reducer;
