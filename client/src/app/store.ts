import { baseApi } from "../api/baseApi";
import combatReducer from "../api/combatSlice";
import controlPointsReducer from "../api/controlPointsSlice";
import flightsReducer from "../api/flightsSlice";
import frontLinesReducer from "../api/frontLinesSlice";
import iadsNetworkReducer from "../api/iadsNetworkSlice";
import mapReducer from "../api/mapSlice";
import navMeshReducer from "../api/navMeshSlice";
import supplyRoutesReducer from "../api/supplyRoutesSlice";
import tgosReducer from "../api/tgosSlice";
import threatZonesReducer from "../api/threatZonesSlice";
import unculledZonesReducer from "../api/unculledZonesSlice";
import {
  Action,
  PreloadedState,
  ThunkAction,
  combineReducers,
  configureStore,
} from "@reduxjs/toolkit";

const rootReducer = combineReducers({
  combat: combatReducer,
  controlPoints: controlPointsReducer,
  flights: flightsReducer,
  frontLines: frontLinesReducer,
  map: mapReducer,
  navmeshes: navMeshReducer,
  supplyRoutes: supplyRoutesReducer,
  iadsNetwork: iadsNetworkReducer,
  tgos: tgosReducer,
  threatZones: threatZonesReducer,
  [baseApi.reducerPath]: baseApi.reducer,
  unculledZones: unculledZonesReducer,
});

export function setupStore(preloadedState?: PreloadedState<RootState>) {
  return configureStore({
    reducer: rootReducer,
    middleware: (getDefaultMiddleware) =>
      getDefaultMiddleware().concat(baseApi.middleware),
    preloadedState: preloadedState,
  });
}

export type AppStore = ReturnType<typeof setupStore>;
export type AppDispatch = AppStore["dispatch"];
export type RootState = ReturnType<typeof rootReducer>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
