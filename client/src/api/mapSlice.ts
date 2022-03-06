import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { createSlice } from "@reduxjs/toolkit";
import { LatLngLiteral } from "leaflet";

interface MapState {
  center: LatLngLiteral;
}

const initialState: MapState = {
  center: { lat: 0, lng: 0 },
};

const mapSlice = createSlice({
  name: "map",
  initialState: initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      if (action.payload.map_center != null) {
        state.center = action.payload.map_center;
      }
    });
    builder.addCase(gameUnloaded, (state) => {
      state.center = { lat: 0, lng: 0 };
    });
  },
});

export const selectMapCenter = (state: RootState) => state.map.center;

export default mapSlice.reducer;
