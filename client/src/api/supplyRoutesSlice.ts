import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { SupplyRoute } from "./liberationApi";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface SupplyRoutesState {
  //routes: { [id: string]: SupplyRoute };
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
      console.log(action.payload);
      state.routes = action.payload;
      /* console.log(action.payload);
      const id = action.payload.id;
      const points = action.payload.points;
      if (points) {
        delete state.routes[id];
        state.routes[id] = action.payload;
        console.log("Updating route with points");
      } else if (id in state.routes) {
        // update all things except points?
        console.log("Updating (existing) route without points");
      } else {
        console.log("Trying to update a route that doesn't exist without points...");
      } */
    },
  },
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      state.routes = action.payload.supply_routes;
      /* for (const route of action.payload.supply_routes)
      {
        state.routes[route.id] = route;
      } */
    });
    builder.addCase(gameUnloaded, (state) => {
      state.routes = [];
    });
  },
});

export const selectSupplyRoutes = (state: RootState) => state.supplyRoutes;

export default supplyRoutesSlice.reducer;

export const { updated: supplyRoutesUpdated } = supplyRoutesSlice.actions;
