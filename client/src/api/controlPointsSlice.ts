import { RootState } from "../app/store";
import { ControlPoint } from "./controlpoint";
import { PayloadAction, createSlice } from "@reduxjs/toolkit";

interface ControlPointsState {
  controlPoints: { [key: number]: ControlPoint };
}

const initialState: ControlPointsState = {
  controlPoints: {},
};

export const controlPointsSlice = createSlice({
  name: "controlPoints",
  initialState,
  reducers: {
    setControlPoints: (state, action: PayloadAction<ControlPoint[]>) => {
      state.controlPoints = {};
      for (const cp of action.payload) {
        state.controlPoints[cp.id] = cp;
      }
    },
    updateControlPoint: (state, action: PayloadAction<ControlPoint>) => {
      const cp = action.payload;
      state.controlPoints[cp.id] = cp;
    },
  },
});

export const { setControlPoints, updateControlPoint } =
  controlPointsSlice.actions;

export const selectControlPoints = (state: RootState) => state.controlPoints;

export default controlPointsSlice.reducer;
