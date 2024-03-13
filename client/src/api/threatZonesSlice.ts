import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { ThreatZoneContainer, ThreatZones } from "./liberationApi";
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

export interface IThreatZoneUpdate {
  blue: boolean;
  zones: ThreatZones;
}

export const threatZonesSlice = createSlice({
  name: "threatZonesState",
  initialState,
  reducers: {
    updated: (state, action: PayloadAction<IThreatZoneUpdate[]>) => {
      for (const [blue, zones] of Object.entries(action.payload)) {
        const data = {blue: (blue === "true"), zones: zones} as unknown as IThreatZoneUpdate
        if (data.blue) {
          state.zones.blue = data.zones;
        } else {
          state.zones.red = data.zones;
        }
      }
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
