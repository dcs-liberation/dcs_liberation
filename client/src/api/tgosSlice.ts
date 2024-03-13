import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import { Tgo } from "./liberationApi";
import { PayloadAction, createSlice } from "@reduxjs/toolkit";

interface TgosState {
  tgos: { [key: string]: Tgo };
}

const initialState: TgosState = {
  tgos: {},
};

export const tgosSlice = createSlice({
  name: "tgos",
  initialState,
  reducers: {
    updateTgo: (state, action: PayloadAction<Tgo[]>) => {
      for (const tgo of action.payload) {
        state.tgos[tgo.id] = tgo;
      }
    },
  },
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      state.tgos = action.payload.tgos.reduce(
        (acc: { [key: string]: Tgo }, curr) => {
          acc[curr.id] = curr;
          return acc;
        },
        {}
      );
    });
    builder.addCase(gameUnloaded, (state) => {
      state.tgos = {};
    });
  },
});

export const { updateTgo } = tgosSlice.actions;

export const selectTgos = (state: RootState) => state.tgos;

export default tgosSlice.reducer;
