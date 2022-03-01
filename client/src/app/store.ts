import { Action, ThunkAction, configureStore } from "@reduxjs/toolkit";

import atoReducer from "../game/ato/atoSlice";
import theaterReducer from "../game/theater/theaterSlice";

export const store = configureStore({
  reducer: {
    atos: atoReducer,
    theater: theaterReducer,
  },
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
