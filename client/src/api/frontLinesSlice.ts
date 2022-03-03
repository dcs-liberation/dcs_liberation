import { PayloadAction, createSlice } from "@reduxjs/toolkit";

import FrontLine from "./frontline";
import { RootState } from "../app/store";

interface FrontLinesState {
  fronts: FrontLine[];
}

const initialState: FrontLinesState = {
  fronts: [],
};

export const frontLinesSlice = createSlice({
  name: "frontLines",
  initialState,
  reducers: {
    setFrontLines: (state, action: PayloadAction<FrontLine[]>) => {
      state.fronts = action.payload;
    },
  },
});

export const { setFrontLines } = frontLinesSlice.actions;

export const selectFrontLines = (state: RootState) => state.frontLines;

export default frontLinesSlice.reducer;
