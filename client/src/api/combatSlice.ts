import { RootState } from "../app/store";
import { gameLoaded, gameUnloaded } from "./actions";
import Combat from "./combat";
import { PayloadAction, createSlice } from "@reduxjs/toolkit";

interface CombatState {
  combat: { [key: string]: Combat };
}

const initialState: CombatState = {
  combat: {},
};

export const combatSlice = createSlice({
  name: "combat",
  initialState,
  reducers: {
    newCombats: (state, action: PayloadAction<Combat[]>) => {
      for (const combat of action.payload) {
        state.combat[combat.id] = combat;
      }
    },
    updateCombats: (state, action: PayloadAction<Combat[]>) => {
      for (const combat of action.payload) {
        state.combat[combat.id] = combat;
      }
    },
    endCombats: (state, action: PayloadAction<string[]>) => {
      for (const cID of action.payload) {
        delete state.combat[cID];
      }
    },
  },
  extraReducers: (builder) => {
    builder.addCase(gameLoaded, (state, action) => {
      state.combat = {};
    });
    builder.addCase(gameUnloaded, (state) => {
      state.combat = {};
    });
  },
});

export const { newCombats, updateCombats, endCombats } =
  combatSlice.actions;

export const selectCombat = (state: RootState) => state.combat;

export default combatSlice.reducer;
