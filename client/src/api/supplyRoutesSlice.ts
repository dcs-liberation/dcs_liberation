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
      //console.log(action.payload);
      //state.routes = action.payload;
      for (const route of action.payload) {
        state.routes[route.id] = route;
        //console.log(`Updated ${route.id}`);
        //console.log(route);
      }
      /* console.log(action.payload);
      const points = action.payload.points;
      if (points) {
        delete state.routes[id];
        state.routes[id] = action.payload;
        console.log("Updating route with points");
      } else if (id in state.routes) {
        // update all things except points?
        state.routes[id].blue = action.payload.blue;
        state.routes[id].is_sea = action.payload.is_sea;
        state.routes[id].front_active = action.payload.front_active;
        state.routes[id].active_transports = action.payload.active_transports;
        console.log("Updating (existing) route without points");
      } else {
        console.log("Trying to update a route that doesn't exist without points...");
      } */
    },
    deleted: (state, action: PayloadAction<string[]>) => {
      for (const id of action.payload) {
        delete state.routes[id];
        //console.log(`Deleting ${id}`);
      }
      //const id = action.payload;
      //delete state.routes[id];
    },
  },
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      //state.routes = action.payload.supply_routes;
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

export const { updated: supplyRoutesUpdated, deleted: supplyRoutesDeleted } = supplyRoutesSlice.actions;
