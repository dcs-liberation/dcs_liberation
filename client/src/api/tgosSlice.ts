import { PayloadAction, createSlice } from "@reduxjs/toolkit";
import { Tgo, TgoType } from "./tgo";

import { RootState } from "../app/store";

interface TgosState {
  tgosByType: { [key: string]: Tgo[] };
}

const initialState: TgosState = {
  tgosByType: Object.fromEntries(
    Object.values(TgoType).map((key) => [key, []])
  ),
};

export const tgosSlice = createSlice({
  name: "tgos",
  initialState,
  reducers: {
    setTgos: (state, action: PayloadAction<Tgo[]>) => {
      state.tgosByType = initialState.tgosByType;
      for (const key of Object.values(TgoType)) {
        state.tgosByType[key] = [];
      }
      for (const tgo of action.payload) {
        var type;
        switch (tgo.category) {
          case "aa":
            type = TgoType.AIR_DEFENSE;
            break;
          case "factory":
            type = TgoType.FACTORY;
            break;
          case "ship":
            type = TgoType.SHIP;
            break;
          default:
            type = TgoType.OTHER;
            break;
        }
        state.tgosByType[type].push(tgo);
      }
    },
  },
});

export const { setTgos } = tgosSlice.actions;

export const selectTgos = (state: RootState) => state.tgos;

export default tgosSlice.reducer;
