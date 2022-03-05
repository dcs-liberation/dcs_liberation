import { apiSlice } from "../api/api";
import combatReducer from "../api/combatSlice";
import controlPointsReducer from "../api/controlPointsSlice";
import flightsReducer from "../api/flightsSlice";
import frontLinesReducer from "../api/frontLinesSlice";
import supplyRoutesReducer from "../api/supplyRoutesSlice";
import tgosReducer from "../api/tgosSlice";
import { Action, ThunkAction, configureStore } from "@reduxjs/toolkit";

export const store = configureStore({
  reducer: {
    combat: combatReducer,
    controlPoints: controlPointsReducer,
    flights: flightsReducer,
    frontLines: frontLinesReducer,
    supplyRoutes: supplyRoutesReducer,
    tgos: tgosReducer,
    [apiSlice.reducerPath]: apiSlice.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(apiSlice.middleware),
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
