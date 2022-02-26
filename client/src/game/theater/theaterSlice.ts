import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { RootState } from "../../app/store";
import { ControlPoint } from "../controlpoint";

interface TheaterState {
  controlPoints: ControlPoint[];
}

const initialState: TheaterState = {
  controlPoints: [],
};

export const theaterSlice = createSlice({
  name: "theater",
  initialState,
  reducers: {
    setControlPoints: (state, action: PayloadAction<ControlPoint[]>) => {
      state.controlPoints = action.payload;
    },
  },
});

export const { setControlPoints } = theaterSlice.actions;

export const selectControlPoints = (state: RootState) =>
  state.theater.controlPoints;

export default theaterSlice.reducer;
