import { Action, ThunkAction, configureStore } from "@reduxjs/toolkit";

import controlPointsReducer from "../api/controlPointsSlice";
import flightsReducer from "../api/flightsSlice";

export const store = configureStore({
  reducer: {
    flights: flightsReducer,
    controlPoints: controlPointsReducer,
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
