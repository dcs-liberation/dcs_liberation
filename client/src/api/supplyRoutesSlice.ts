import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { SupplyRoute } from "./liberationApi";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface SupplyRoutesState {
  routes: SupplyRoute[];
}

const initialState: SupplyRoutesState = {
  routes: [],
};

export const supplyRoutesSlice = createSlice({
  name: "supplyRoutes",
  initialState,
  reducers: {
    updated: (state, action: PayloadAction<SupplyRoute[]>) => {
      state.routes = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      state.routes = action.payload.supply_routes;
    });
    builder.addCase(gameUnloaded, (state) => {
      state.routes = [];
    });
  },
});

export const selectSupplyRoutes = (state: RootState) => state.supplyRoutes;

export default supplyRoutesSlice.reducer;

export const { updated: supplyRoutesUpdated } = supplyRoutesSlice.actions;
