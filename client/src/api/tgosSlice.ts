import { PayloadAction, createSlice } from "@reduxjs/toolkit";

import { RootState } from "../app/store";
import { Tgo } from "./tgo";

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
    setTgos: (state, action: PayloadAction<Tgo[]>) => {
      state.tgos = {};
      for (const tgo of action.payload) {
        state.tgos[tgo.id] = tgo;
      }
    },
    updateTgo: (state, action: PayloadAction<Tgo>) => {
      const tgo = action.payload;
      state.tgos[tgo.id] = tgo;
    },
  },
});

export const { setTgos, updateTgo } = tgosSlice.actions;

export const selectTgos = (state: RootState) => state.tgos;

export default tgosSlice.reducer;
