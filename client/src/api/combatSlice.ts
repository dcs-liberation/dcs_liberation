import { RootState } from "../app/store";
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
    setCombat: (state, action: PayloadAction<Combat[]>) => {
      state.combat = {};
      for (const combat of action.payload) {
        state.combat[combat.id] = combat;
      }
    },
    newCombat: (state, action: PayloadAction<Combat>) => {
      const combat = action.payload;
      state.combat[combat.id] = combat;
    },
    updateCombat: (state, action: PayloadAction<Combat>) => {
      const combat = action.payload;
      state.combat[combat.id] = combat;
    },
    endCombat: (state, action: PayloadAction<string>) => {
      delete state.combat[action.payload];
    },
  },
});

export const { setCombat, newCombat, updateCombat, endCombat } =
  combatSlice.actions;

export const selectCombat = (state: RootState) => state.combat;

export default combatSlice.reducer;
