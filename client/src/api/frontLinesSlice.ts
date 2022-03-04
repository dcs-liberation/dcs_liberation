import { RootState } from "../app/store";
import FrontLine from "./frontline";
import { PayloadAction, createSlice } from "@reduxjs/toolkit";

interface FrontLinesState {
  fronts: { [key: string]: FrontLine };
}

const initialState: FrontLinesState = {
  fronts: {},
};

export const frontLinesSlice = createSlice({
  name: "frontLines",
  initialState,
  reducers: {
    setFrontLines: (state, action: PayloadAction<FrontLine[]>) => {
      state.fronts = {};
      for (const front of action.payload) {
        state.fronts[front.id] = front;
      }
    },
    addFrontLine: (state, action: PayloadAction<FrontLine>) => {
      const front = action.payload;
      state.fronts[front.id] = front;
    },
    updateFrontLine: (state, action: PayloadAction<FrontLine>) => {
      const front = action.payload;
      state.fronts[front.id] = front;
    },
    deleteFrontLine: (state, action: PayloadAction<string>) => {
      delete state.fronts[action.payload];
    },
  },
});

export const { setFrontLines, addFrontLine, updateFrontLine, deleteFrontLine } =
  frontLinesSlice.actions;

export const selectFrontLines = (state: RootState) => state.frontLines;

export default frontLinesSlice.reducer;
