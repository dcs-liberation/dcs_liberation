import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { ControlPoint } from "./liberationApi";
import { PayloadAction, createSlice } from "@reduxjs/toolkit";

interface ControlPointsState {
  controlPoints: { [key: string]: ControlPoint };
}

const initialState: ControlPointsState = {
  controlPoints: {},
};

export const controlPointsSlice = createSlice({
  name: "controlPoints",
  initialState,
  reducers: {
    updateControlPoint: (state, action: PayloadAction<ControlPoint[]>) => {
      for (const cp of action.payload) {
        state.controlPoints[cp.id] = cp;
      }
    },
  },
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      state.controlPoints = action.payload.control_points.reduce(
        (acc: { [key: string]: ControlPoint }, curr) => {
          acc[curr.id] = curr;
          return acc;
        },
        {}
      );
    });
    builder.addCase(gameUnloaded, (state) => {
      state.controlPoints = {};
    });
  },
});

export const { updateControlPoint } = controlPointsSlice.actions;

export const selectControlPoints = (state: RootState) => state.controlPoints;

export default controlPointsSlice.reducer;
