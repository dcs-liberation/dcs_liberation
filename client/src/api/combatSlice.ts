import { gameLoaded, gameUnloaded } from "./actions";
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
      // still need to pass this from back-end, initialize empty...
      state.combat = {};
      /* state.combat = action.payload.combat.reduce(
        (acc: { [key: string]: Tgo }, curr) => {
          acc[curr.id] = curr;
          return acc;
        },
        {}
      ); */
    });
    builder.addCase(gameUnloaded, (state) => {
      state.combat = {};
    });
  },
});

export const { updateCombats, endCombats } = combatSlice.actions;

export const selectCombat = (state: RootState) => state.combat;

export default combatSlice.reducer;
