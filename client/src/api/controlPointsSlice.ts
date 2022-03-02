import { PayloadAction, createSlice } from "@reduxjs/toolkit";

import { ControlPoint } from "./controlpoint";
import { RootState } from "../app/store";

interface ControlPointsState {
  controlPoints: ControlPoint[];
}

const initialState: ControlPointsState = {
  controlPoints: [],
};

export const controlPointsSlice = createSlice({
  name: "controlPoints",
  initialState,
  reducers: {
    setControlPoints: (state, action: PayloadAction<ControlPoint[]>) => {
      state.controlPoints = action.payload;
    },
  },
});

export const { setControlPoints } = controlPointsSlice.actions;

export const selectControlPoints = (state: RootState) => state.controlPoints;

export default controlPointsSlice.reducer;
