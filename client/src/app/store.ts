import { Action, ThunkAction, configureStore } from "@reduxjs/toolkit";

import controlPointsReducer from "../api/controlPointsSlice";
import flightsReducer from "../api/flightsSlice";
import supplyRoutesReducer from "../api/supplyRoutesSlice";
import tgosReducer from "../api/tgosSlice";

export const store = configureStore({
  reducer: {
    flights: flightsReducer,
    controlPoints: controlPointsReducer,
    supplyRoutes: supplyRoutesReducer,
    tgos: tgosReducer,
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
