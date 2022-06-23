import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { SupplyRoute } from "./liberationApi";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface SupplyRoutesState {
  routes: { [id: string]: SupplyRoute };
  //routes: SupplyRoute[];
}

const initialState: SupplyRoutesState = {
  routes: {},
};

export const supplyRoutesSlice = createSlice({
  name: "supplyRoutes",
  initialState,
  reducers: {
    updated: (state, action: PayloadAction<SupplyRoute[]>) => {
      for (const route of action.payload) {
        const id = route.id;
        let points = route.points;
        if (points) {
          state.routes[id] = route;
        } else if (id in state.routes) {
          points = state.routes[id].points;
          state.routes[id] = route;
          state.routes[id].points = points;
        } else {
          console.log("Trying to update a route that doesn't exist without points...");
        }
      }
    },
  },
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      //state.routes = action.payload.supply_routes;
      state.routes = {}
      for (const route of action.payload.supply_routes)
      {
        state.routes[route.id] = route;
      }
    });
    builder.addCase(gameUnloaded, (state) => {
      state.routes = {};
    });
  },
});

export const selectSupplyRoutes = (state: RootState) => state.supplyRoutes;

export default supplyRoutesSlice.reducer;

export const { updated: supplyRoutesUpdated } = supplyRoutesSlice.actions;
