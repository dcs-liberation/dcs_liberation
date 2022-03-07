import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { FrontLine } from "./liberationApi";
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
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      state.fronts = action.payload.front_lines.reduce(
        (acc: { [key: string]: FrontLine }, curr) => {
          acc[curr.id] = curr;
          return acc;
        },
        {}
      );
    });
    builder.addCase(gameUnloaded, (state) => {
      state.fronts = {};
    });
  },
});

export const { addFrontLine, updateFrontLine, deleteFrontLine } =
  frontLinesSlice.actions;

export const selectFrontLines = (state: RootState) => state.frontLines;

export default frontLinesSlice.reducer;
