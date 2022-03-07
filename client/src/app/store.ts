import { baseApi } from "../api/baseApi";
import combatReducer from "../api/combatSlice";
import controlPointsReducer from "../api/controlPointsSlice";
import flightsReducer from "../api/flightsSlice";
import frontLinesReducer from "../api/frontLinesSlice";
import mapReducer from "../api/mapSlice";
import supplyRoutesReducer from "../api/supplyRoutesSlice";
import tgosReducer from "../api/tgosSlice";
import threatZonesReducer from "../api/threatZonesSlice";
import { Action, ThunkAction, configureStore } from "@reduxjs/toolkit";

export const store = configureStore({
  reducer: {
    combat: combatReducer,
    controlPoints: controlPointsReducer,
    flights: flightsReducer,
    frontLines: frontLinesReducer,
    map: mapReducer,
    supplyRoutes: supplyRoutesReducer,
    tgos: tgosReducer,
    threatZones: threatZonesReducer,
    [baseApi.reducerPath]: baseApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(baseApi.middleware),
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
