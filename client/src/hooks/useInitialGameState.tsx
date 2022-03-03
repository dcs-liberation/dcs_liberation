import { ControlPoint } from "../api/controlpoint";
import { Flight } from "../api/flight";
import FrontLine from "../api/frontline";
import SupplyRoute from "../api/supplyroute";
import Tgo from "../api/tgo";
import backend from "../api/backend";
import { registerFlight } from "../api/flightsSlice";
import { setControlPoints } from "../api/controlPointsSlice";
import { setFrontLines } from "../api/frontLinesSlice";
import { setSupplyRoutes } from "../api/supplyRoutesSlice";
import { setTgos } from "../api/tgosSlice";
import { useAppDispatch } from "../app/hooks";
import { useEffect } from "react";

// TODO: This should probably be distinct useControlPoints, useFlights, etc that
// are smart enough to only initialize once which get called in the components
// that use them rather than forcibly loading the whole game in the root
// component.
export const useInitialGameState = () => {
  const dispatch = useAppDispatch();
  useEffect(() => {
    backend
      .get("/control-points")
      .catch((error) => console.log(`Error fetching control points: ${error}`))
      .then((response) => {
        if (response != null) {
          dispatch(setControlPoints(response.data as ControlPoint[]));
        }
      });
    backend
      .get("/tgos")
      .catch((error) => console.log(`Error fetching TGOs: ${error}`))
      .then((response) => {
        if (response != null) {
          dispatch(setTgos(response.data as Tgo[]));
        }
      });
    backend
      .get("/supply-routes")
      .catch((error) => console.log(`Error fetching supply routes: ${error}`))
      .then((response) => {
        if (response != null) {
          dispatch(setSupplyRoutes(response.data as SupplyRoute[]));
        }
      });
    backend
      .get("/front-lines")
      .catch((error) => console.log(`Error fetching front-lines: ${error}`))
      .then((response) => {
        if (response != null) {
          dispatch(setFrontLines(response.data as FrontLine[]));
        }
      });
    backend
      .get("/flights?with_waypoints=true")
      .catch((error) => console.log(`Error fetching flights: ${error}`))
      .then((response) => {
        if (response != null) {
          for (const flight of response.data) {
            dispatch(registerFlight(flight as Flight));
          }
        }
      });
  });
};

export default useInitialGameState;
