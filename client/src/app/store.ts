import controlPointsReducer from "../api/controlPointsSlice";
import flightsReducer from "../api/flightsSlice";
import frontLinesReducer from "../api/frontLinesSlice";
import supplyRoutesReducer from "../api/supplyRoutesSlice";
import tgosReducer from "../api/tgosSlice";
import { Action, ThunkAction, configureStore } from "@reduxjs/toolkit";
import logger from "redux-logger";

export const store = configureStore({
  reducer: {
    flights: flightsReducer,
    frontLines: frontLinesReducer,
    controlPoints: controlPointsReducer,
    supplyRoutes: supplyRoutesReducer,
    tgos: tgosReducer,
  },
  // The logger middleware must be last or it won't log actions.
  middleware: [logger],
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
