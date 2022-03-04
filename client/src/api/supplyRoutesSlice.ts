import { RootState } from "../app/store";
import SupplyRoute from "./supplyroute";
import { PayloadAction, createSlice } from "@reduxjs/toolkit";

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
    setSupplyRoutes: (state, action: PayloadAction<SupplyRoute[]>) => {
      state.routes = action.payload;
    },
  },
});

export const { setSupplyRoutes } = supplyRoutesSlice.actions;

export const selectSupplyRoutes = (state: RootState) => state.supplyRoutes;

export default supplyRoutesSlice.reducer;
